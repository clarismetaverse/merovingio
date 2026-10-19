import copy,json,os,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import benchmark_ablation as b

class AblationTests(unittest.TestCase):
 def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.out=Path(self.tmp.name)
 def tearDown(self):self.tmp.cleanup()
 def payload(self,cond='compact_generic',shape='left',repeat=0):return b.build_payload(self.out,shape,repeat,cond)
 def test_exact_previous_workspace_and_frozen_assets(self):
  p,m,meta,audit,source=self.payload();prior=b.prior_call('left',0)
  self.assertEqual(p['state'],prior['model_input']['state']);self.assertEqual(source,prior['request_sha256'])
  self.assertEqual(len(p['questions']),20);self.assertEqual(sum(q['type']=='score' for q in p['questions'].values()),10)
  for q,info in meta.items():
   if info['primitive']=='score':self.assertEqual(p['questions'][q],prior['model_input']['questions'][q])
 def test_description_factor_changes_only_two_definitions(self):
  a=self.payload()[0];c=self.payload('explicit_generic')[0];self.assertEqual(a['questions'],c['questions']);self.assertEqual(a['assets'],c['assets'])
  state=copy.deepcopy(c['state']);changed=[]
  for alias,record in state['schema_hypotheses'].items():
   if 'definition' in record:changed.append(alias);record.pop('definition')
  self.assertEqual(len(changed),2);self.assertEqual(a['state'],state)
  text=json.dumps(b.EXPLANATIONS)
  for name in ('from_C','from_A','edge_link','no_op','reference_binding','C312','correct'):self.assertNotIn(name,text)
 def test_rubric_factor_preserves_workspace_and_instructions(self):
  a=self.payload()[0];c=self.payload('compact_concrete')[0];self.assertEqual(a['state'],c['state']);self.assertEqual(a['assets'],c['assets'])
  for q in a['questions']:self.assertEqual(a['questions'][q]['instructions'],c['questions'][q]['instructions'])
  self.assertTrue(all(a['questions'][q]['criteria']!=c['questions'][q]['criteria'] for q in a['questions']))
 def test_choice_reuses_score_wording_without_option_label_leak(self):
  for cond in b.CONDITIONS:
   p,m,meta,_,_=self.payload(cond)
   for q,info in meta.items():
    if info['primitive']!='choice':continue
    score=p['questions']['Q'+q[1:]];choice=p['questions'][q]
    self.assertEqual(score['instructions'],choice['instructions'])
    for label,level in info['label_levels'].items():
     self.assertEqual(choice['criteria'][label],score['criteria'][level]);self.assertNotIn(label,json.dumps(choice['instructions']))
    self.assertIn('none',choice['criteria'])
 def test_all_28_missed_and_12_negative_bindings_in_each_cell(self):
  for cond in b.CONDITIONS:
   info=[]
   for shape in b.base.geometry.SHAPES:
    for repeat in range(2):info.extend(v for v in self.payload(cond,shape,repeat)[2].values() if v['primitive']=='score')
   self.assertEqual(len(info),40);self.assertEqual(sum(v['reference_binding'] for v in info),28)
   self.assertEqual(sum(v['prior_missed_positive'] for v in info),28)
   self.assertEqual(sum(not v['reference_binding'] for v in info),12)
 def test_no_gold_method_or_source_names_in_model_input(self):
  for cond in b.CONDITIONS:
   p,*_=self.payload(cond);text=json.dumps({k:v for k,v in p.items() if k!='assets'})
   for name in ('GS_HIST','GS_PROP','from_C','from_A','edge_link','no_op','prior_score','reference_binding','reference_level','correct'):
    self.assertNotIn(name,text)
 def test_mixed_sanitization_drops_untrusted_text(self):
  p,*_=self.payload();raw={'answers':{},'usage':{'input_tokens':10,'secret':'sensitive'},'secret':'sensitive'}
  for q,question in p['questions'].items():
   if question['type']=='score':a={'score':3,'probabilities':{'0':0,'1':0,'2':0,'3':1},'confidence':1}
   else:
    label=next(iter(question['criteria']));a={'choice':label,'probabilities':{k:int(k==label) for k in question['criteria']},'confidence':1}
   a['secret']='sensitive';raw['answers'][q]=a
  clean=b.sanitize(raw,p['questions']);self.assertEqual(len(clean['answers']),20);self.assertNotIn('sensitive',json.dumps(clean))
  q=next(q for q,v in p['questions'].items() if v['type']=='choice');raw['answers'][q]['choice']='invalid'
  with self.assertRaises(ValueError):b.sanitize(raw,p['questions'])
 def test_offline_results_have_no_invented_scores(self):
  a=b.analyze([]);self.assertEqual(a['native_answers'],0)
  self.assertTrue(all(v['score']['n']==0 and v['choice']['n']==0 for v in a['by_condition'].values()))
 def test_analysis_preserves_false_positives_and_separates_threshold(self):
  p,m,meta,audit,_=self.payload();answers={}
  for q,info in meta.items():
   if info['primitive']=='score':
    answers[q]={'normalized_score':.7,'probabilities':{'0':0,'1':0,'2':.9,'3':.1},'confidence':.8,'reliability':None}
   else:
    label=next(k for k,v in info['label_levels'].items() if v==3)
    answers[q]={'choice':label,'confidence':.9,'reliability':None}
  call={'shape':'left','repeat':0,'condition':'compact_generic','question_metadata':meta,'response':{'answers':answers}}
  a=b.analyze([call]);s=a['by_condition']['compact_generic']
  self.assertEqual(s['score']['positive_bindings_recognized'],0)
  self.assertEqual(s['choice']['positive_bindings_recognized'],7)
  self.assertEqual(s['choice']['false_positive_n'],3)
  self.assertEqual(a['fixed_threshold_sensitivity']['compact_generic']['0.65']['false_positive_n'],3)
  self.assertEqual(a['fixed_threshold_sensitivity']['compact_generic']['0.75']['positive_recovered'],0)
 def test_actions_guard(self):
  with patch.dict(os.environ,{},clear=True):
   with self.assertRaises(SystemExit):b.main(self.out/'blocked',True)
   with self.assertRaises(RuntimeError):b.transport({})
  self.assertFalse((self.out/'blocked').exists())

if __name__=='__main__':unittest.main()

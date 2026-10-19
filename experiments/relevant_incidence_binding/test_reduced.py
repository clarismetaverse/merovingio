import copy,json,os,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import benchmark_reduced as b

class RelevantStateTests(unittest.TestCase):
 def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.out=Path(self.tmp.name)
 def tearDown(self):self.tmp.cleanup()
 def payload(self,replica=0,case='shared',condition='full_state'):return b.build_payload(self.out,replica,case,condition)
 def test_identical_questions_ids_contracts_and_assets(self):
  for replica in b.REPLICAS:
   for case in b.source.CASES:
    a=self.payload(replica,case)[0];c=self.payload(replica,case,'relevant_state')[0]
    self.assertEqual(a['questions'],c['questions']);self.assertEqual(a['assets'],c['assets']);self.assertEqual(a['state']['contracts'],c['state']['contracts'])
    self.assertEqual(len(a['questions']),2);self.assertEqual(len(c['state']['snapshots']),1)
 def test_retained_records_and_every_boundary_use_are_unchanged(self):
  a=self.payload()[0]['state'];c=self.payload(condition='relevant_state')[0]['state']
  for key in a:
   if key!='snapshots':self.assertEqual(a[key],c[key])
  for snapshot,data in c['snapshots'].items():
   for key,value in data['objects'].items():self.assertEqual(value,a['snapshots'][snapshot]['objects'][key])
   self.assertLess(len(data['objects']),len(a['snapshots'][snapshot]['objects']))
 def test_projection_is_closed_and_idempotent(self):
  p=self.payload(condition='relevant_state')[0];self.assertEqual(b.reduce_state(p['state'],p['questions']),p['state'])
  for snap in p['state']['snapshots'].values():
   objects=snap['objects']
   for record in objects.values():
    if record['type']=='point':continue
    ids=[]
    if 'vertices' in record:ids+=record['vertices']
    if 'endpoints' in record:ids+=record['endpoints']
    for use in record.get('boundary_uses',[]):ids+=[use['carrier']]+use['endpoints']
    self.assertTrue(all(i in objects for i in ids))
 def test_each_offered_witness_and_graph_binding_keeps_reference(self):
  for replica in b.REPLICAS:
   for case in b.source.CASES:
    p,meta,*_=self.payload(replica,case,'relevant_state')
    for m in meta.values():
     objects=p['state']['snapshots'][m['snapshot']]['objects']
     for label,w in m['option_witnesses'].items():self.assertEqual(b.source.check_witness(objects,w,m['schema'],m['query_scope_host']),m['option_failures'][label])
     self.assertEqual(b.source.all_bindings(objects,m['schema'],m['query_scope_host']),m['all_graph_bindings'])
 def test_preserves_wrong_carrier_decoys(self):
  p,meta,*_=self.payload(case='omitted_valid',condition='relevant_state')
  for m in meta.values():
   objects=p['state']['snapshots'][m['snapshot']]['objects'];names=m['aliases']
   self.assertTrue(all(names[n] in objects for n in ('S','T','Z','L','R','CL','H','OUT')))
   self.assertEqual(m['expected_choice'],'none');self.assertEqual(len(m['all_graph_bindings']),1)
 def test_budget_and_reference_classes(self):
  for condition in b.CONDITIONS:
   info=[]
   for replica in b.REPLICAS:
    for case in b.source.CASES:info+=list(self.payload(replica,case,condition)[1].values())
   self.assertEqual(len(info),24);self.assertEqual(sum(m['valid_listed_n'] for m in info),8)
 def test_full_baseline_is_exact_source_state(self):
  p,meta,*_=self.payload();prior=b.prior_call(0)
  state=copy.deepcopy(p['state']);self.assertEqual(state.pop('image_asset_manifest'),list(p['assets']))
  self.assertEqual(state,prior['model_input']['state'])
  for q,v in p['questions'].items():self.assertEqual(v,prior['model_input']['questions'][q])
 def test_no_oracle_or_case_leakage(self):
  p,*_=self.payload(case='distinct_coincident',condition='relevant_state');text=json.dumps({k:v for k,v in p.items() if k!='assets'})
  for term in ('expected_choice','option_failures','relevant_state','full_state','distinct_coincident','historical_answers','valid_listed_n'):
   self.assertNotIn(term,text)
 def test_empty_analysis_has_no_fake_answers(self):
  a=b.analyze([]);self.assertEqual(a['native_answers'],0);self.assertEqual(a['paired_summary']['n'],0)
 def test_actions_guard(self):
  with patch.dict(os.environ,{},clear=True):
   with self.assertRaises(SystemExit):b.main(self.out/'blocked',True)
   with self.assertRaises(RuntimeError):b.transport({})
   with self.assertRaises(SystemExit):b.diagnose(self.out/'blocked')
  self.assertFalse((self.out/'blocked').exists())

if __name__=='__main__':unittest.main()

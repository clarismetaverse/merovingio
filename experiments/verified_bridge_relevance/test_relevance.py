import copy,json,math,os,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import benchmark_relevance as b

class VerifiedRelevanceTests(unittest.TestCase):
 def test_all_bridges_pass_both_contracts_on_both_presentations(self):
  for replica in range(2):
   for method in b.METHODS:
    objects=b.objects_for(method,replica);cert=b.certificate(objects)
    self.assertTrue(cert['admissible'])
    for gs,w in cert['generic_space_bindings'].items():self.assertEqual(b.checker.check_witness(objects,w,b.GS[gs],'HOST'),[])

 def test_preverification_rejects_material_identity_and_partial_use(self):
  for mutation in ('identity','partial'):
   o=b.objects_for('from_C',0)
   use=next(u for u in o['REGION_1']['boundary_uses'] if u['carrier']=='BRIDGE')
   if mutation=='identity':o['OTHER']=copy.deepcopy(o['BRIDGE']);use['carrier']='OTHER'
   else:use['endpoints']=[use['endpoints'][0],use['endpoints'][0]]
   with self.assertRaises(ValueError):b.certificate(o)

 def test_transformation_preserves_metric_and_reverses_orientation(self):
  a=b.objects_for('from_A',0);c=b.objects_for('from_A',1)
  for u,v in (('A','B'),('B','C'),('C','A')):
   self.assertAlmostEqual(math.dist(a[u]['xy'],a[v]['xy']),math.dist(c[u]['xy'],c[v]['xy']),places=6)
  self.assertLess(b.checker.signed_area(b.checker.polygon(a,a['HOST']))*b.checker.signed_area(b.checker.polygon(c,c['HOST'])),0)

 def test_counterfactual_changes_only_active_objective(self):
  with tempfile.TemporaryDirectory() as t:
   for replica in range(2):
    cells=[b.build_payload(Path(t),replica,g) for g in b.GOALS]
    for payload,meta,audit in cells:
     state=copy.deepcopy(payload);state['state'].pop('active_objective')
     first=copy.deepcopy(cells[0][0]);first['state'].pop('active_objective')
     self.assertEqual(state,first);self.assertEqual(audit,cells[0][2])
     self.assertEqual(meta['candidate_mapping'],cells[0][1]['candidate_mapping'])
    self.assertEqual(len({m['reference_method'] for _,m,_ in cells}),3)

 def test_small_native_score_budget_and_certificates_grounded(self):
  with tempfile.TemporaryDirectory() as t:
   count=0
   for replica in range(2):
    for goal in b.GOALS:
     payload,meta,_=b.build_payload(Path(t),replica,goal);count+=len(payload['questions'])
     self.assertEqual(len(payload['questions']),6)
     self.assertEqual(set(payload['assets']),{'initial',*('image_'+c for c in meta['candidate_mapping'])})
     for c,method in meta['candidate_mapping'].items():
      supplied=payload['state']['admissible_bridges'][c]['verified_certificate']
      raw=b.certificate(b.objects_for(method,replica));relations=raw['direct_structural_relations']
      self.assertEqual(supplied['direct_structural_relations']['angular_fan_split_at_vertex'],meta['point_labels'][relations['angular_fan_split_at_vertex']])
      self.assertEqual(set(supplied['generic_space_bindings']),set(meta['gs_aliases'].values()))
      self.assertEqual(supplied['new_carrier']['material_id'],'S_'+c)
     for q in payload['questions'].values():self.assertEqual(q['type'],'score');self.assertEqual(len(q['criteria']),4)
   self.assertEqual(count,36)

 def test_observer_reference_and_weights_never_enter_input(self):
  forbidden={'reference_method','candidate_mapping','goal_vertex','geometry_certificates','weights','rank','expected_score','correct','reference_score','gold','question_metadata'}
  def walk(v):
   if isinstance(v,dict):
    self.assertFalse(set(v)&forbidden)
    for x in v.values():walk(x)
   elif isinstance(v,list):
    for x in v:walk(x)
  with tempfile.TemporaryDirectory() as t:
   for replica in range(2):
    for goal in b.GOALS:walk(b.build_payload(Path(t),replica,goal)[0])

 def test_neutral_images_have_no_correct_candidate_names(self):
  with tempfile.TemporaryDirectory() as t:
   p,m,a=b.build_payload(Path(t),0,'A')
   self.assertEqual(len(a),4)
   for item in a:
    data=(Path(t)/item['file']).read_bytes()
    self.assertEqual(__import__('hashlib').sha256(data).hexdigest(),item['sha256'])
    self.assertFalse(any(name in item['file'] for name in b.METHODS))

 def test_analyzer_preserves_ties_and_missing_answers(self):
  self.assertEqual(b.analyze([])['ranking_groups'],0)
  with tempfile.TemporaryDirectory() as t:
   payload,meta,_=b.build_payload(Path(t),0,'A')
   rec={**meta,'response':{'answers':{q:{'normalized_score':1} for q in payload['questions']},'usage':{}}}
   result=b.analyze([rec]);self.assertEqual(result['unique_reference_top'],0)
   self.assertEqual(result['reference_in_top_including_ties'],1);self.assertEqual(result['pairwise_reference_ties'],2)

 def test_actions_guard_and_no_offline_model_results(self):
  with patch.dict(os.environ,{},clear=True):
   with self.assertRaises(RuntimeError):b.transport({})
   with tempfile.TemporaryDirectory() as t:
    with self.assertRaises(SystemExit):b.main(Path(t),True)
    b.main(Path(t));r=json.loads((Path(t)/'results.json').read_text())
    self.assertEqual(r['analysis']['api_calls_attempted'],0);self.assertEqual(r['analysis']['native_score_answers'],0)
    self.assertTrue(all('response' not in c for c in r['calls']))

 def test_reference_depends_on_current_geometric_objective(self):
  for replica in range(2):
   for goal in b.GOALS:
    method=b.reference_method(replica,goal)
    self.assertEqual(b.certificate(b.objects_for(method,replica))['direct_structural_relations']['angular_fan_split_at_vertex'],goal)

if __name__=='__main__':unittest.main()

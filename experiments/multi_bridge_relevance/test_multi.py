import copy,json,math,os,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import benchmark_multi as b

class MultipleBridgeTests(unittest.TestCase):
 def test_all_candidates_pass_both_material_contracts(self):
  for replica in range(2):
   for method in b.METHODS:
    o=b.objects_for(method,replica);c=b.certificate(o)
    for gs,w in c['generic_space_bindings'].items():self.assertEqual(b.base.checker.check_witness(o,w,b.base.GS[gs],'HOST'),[])

 def test_metric_and_reflection_equivalence_is_checked(self):
  for replica in range(2):
   o={m:b.objects_for(m,replica) for m in b.METHODS}
   self.assertTrue(b.mirror_equivalent(o['from_A'],o['from_B']))
   self.assertFalse(b.mirror_equivalent(o['from_A'],o['from_A']))
   self.assertTrue(b.mirror_equivalent(o['from_C'],o['from_C']))
   self.assertEqual([m for m in b.METHODS if b.metric_facts(o[m])['region_pair_congruent_by_computed_side_lengths']],['from_C'])
   # All medians give equal areas; that alone must not certify congruent subfigures.
   for obj in o.values():self.assertLess(abs(b.metric_facts(obj)['region_areas'][0]-b.metric_facts(obj)['region_areas'][1]),b.base.checker.EPS)

 def test_mutating_geometry_breaks_equivalence(self):
  first=b.objects_for('from_A',0);second=b.objects_for('from_B',0);second['F']['xy'][0]+=1
  self.assertFalse(b.mirror_equivalent(first,second))

 def test_reference_is_partial_order_not_unique_answer(self):
  for replica in range(2):
   refs=[b.reference(replica,g) for g in b.GOALS]
   self.assertEqual([len(r['useful_methods']) for r in refs],[2,3,1])
   self.assertEqual(sum(len(r['equivalent_pairs']) for r in refs),5)
   self.assertEqual(sum(len(r['strict_pairs']) for r in refs),4)
   self.assertEqual(refs[0]['useful_methods'],['from_A','from_B'])
   self.assertEqual(refs[2]['useful_methods'],['from_C'])

 def test_objective_change_leaves_all_evidence_unchanged(self):
  with tempfile.TemporaryDirectory() as t:
   for replica in range(2):
    values=[]
    for goal in b.GOALS:
     p,m,a=b.build_payload(Path(t),replica,goal);p['state'].pop('active_objective');values.append((p,a))
    self.assertTrue(all(v==values[0] for v in values))

 def test_no_oracle_groups_or_policy_parameters_in_model_input(self):
  forbidden={'reference','reference_method','tiers','useful_methods','strict_pairs','equivalent_pairs','weights','delta','min_useful','expected_methods','gold','rank'}
  def walk(v):
   if isinstance(v,dict):
    self.assertFalse(set(v)&forbidden)
    for x in v.values():walk(x)
   elif isinstance(v,list):
    for x in v:walk(x)
  with tempfile.TemporaryDirectory() as t:
   for replica in range(2):
    for goal in b.GOALS:walk(b.build_payload(Path(t),replica,goal)[0])

 def test_six_requests_of_six_native_scores(self):
  with tempfile.TemporaryDirectory() as t:
   n=0
   for replica in range(2):
    for goal in b.GOALS:
     p,m,a=b.build_payload(Path(t),replica,goal);self.assertEqual(len(p['questions']),6);n+=len(p['questions'])
     for q in p['questions'].values():self.assertEqual(q['type'],'score');self.assertEqual(len(q['criteria']),4)
     self.assertEqual(len(a),4)
   self.assertEqual(n,36)

 def test_material_precheck_still_fails_closed(self):
  o=b.objects_for('from_A',0);use=next(u for u in o['REGION_1']['boundary_uses'] if u['carrier']=='BRIDGE');use['carrier']='OTHER'
  with self.assertRaises(ValueError):b.certificate(o)

 def test_set_policy_allows_empty_multiple_and_boundaries(self):
  self.assertEqual(b.select_set({'a':.4,'b':.3}),[])
  self.assertEqual(b.select_set({'a':.90,'b':.80,'c':.3}),['a','b'])
  self.assertEqual(b.select_set({'a':.90,'b':.79}),['a'])
  self.assertEqual(b.select_set({'a':2/3,'b':2/3}),['a','b'])

 def test_partial_order_metrics_do_not_force_exact_numeric_ties(self):
  ref=b.reference(0,'intact_anchor')
  result=b.assess({'from_A':.9,'from_B':.85,'from_C':.4},ref)
  self.assertTrue(result['exact_set_match']);self.assertTrue(result['equivalent_pairs'][0]['within_band']);self.assertFalse(result['spurious_unique_set'])
  self.assertTrue(all(p['win'] for p in result['strict_pairs']))
  failed=b.assess({'from_A':.9,'from_B':.7,'from_C':.95},ref)
  self.assertFalse(failed['exact_set_match']);self.assertFalse(failed['equivalent_pairs'][0]['within_band'])
  self.assertTrue(any(not p['win'] for p in failed['strict_pairs']))

 def test_transform_preserves_distances_and_reverses_orientation(self):
  first=b.objects_for('from_A',0);second=b.objects_for('from_A',1)
  for a,c in (('A','B'),('A','C'),('B','C')):self.assertAlmostEqual(math.dist(first[a]['xy'],first[c]['xy']),math.dist(second[a]['xy'],second[c]['xy']),places=6)
  self.assertLess(b.base.checker.signed_area(b.base.checker.polygon(first,first['HOST']))*b.base.checker.signed_area(b.base.checker.polygon(second,second['HOST'])),0)

 def test_offline_mode_and_actions_guard(self):
  with patch.dict(os.environ,{},clear=True):
   with tempfile.TemporaryDirectory() as t:
    with self.assertRaises(SystemExit):b.main(Path(t),True)
    b.main(Path(t));r=json.loads((Path(t)/'results.json').read_text())
    self.assertEqual(r['analysis']['api_calls_attempted'],0);self.assertEqual(r['analysis']['native_score_answers'],0);self.assertEqual(r['analysis']['groups'],0)

if __name__=='__main__':unittest.main()

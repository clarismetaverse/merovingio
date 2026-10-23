import copy,json,os,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import benchmark_classes as b

class ClassRelevanceTests(unittest.TestCase):
 def test_partition_is_independent_of_utility_and_reference(self):
  with patch.object(b.prior,'useful',side_effect=AssertionError('utility consulted')),patch.object(b.prior,'reference',side_effect=AssertionError('reference consulted')):
   for replica in range(2):self.assertEqual(b.class_partition(replica),[['from_A','from_B'],['from_C']])

 def test_each_member_and_class_is_actually_certified(self):
  for replica in range(2):
   for group in b.class_partition(replica):
    for method in group:self.assertEqual(len(b.prior.certificate(b.prior.objects_for(method,replica))['generic_space_bindings']),2)
    if len(group)>1:self.assertTrue(b.prior.mirror_equivalent(*(b.prior.objects_for(m,replica) for m in group)))
   for goal in b.GOALS:self.assertTrue(b.objective_invariant_under_reflection(replica,goal))

 def test_class_positions_and_member_order_are_balanced(self):
  groups=[list(b.class_layout(rep).values()) for rep in range(2)]
  self.assertEqual(list(map(len,groups[0])),[2,1]);self.assertEqual(list(map(len,groups[1])),[1,2])
  self.assertEqual(groups[0][0],list(reversed(groups[1][1])))

 def test_all_old_facts_objectives_and_image_bytes_are_frozen(self):
  with tempfile.TemporaryDirectory() as t:
   for rep in range(2):
    for goal in b.GOALS:
     p,m,a=b.build_payload(Path(t),rep,goal);old=b.archived(rep,goal)
     new=copy.deepcopy(p['state']);new.pop('certified_equivalence_classes');new.pop('class_scoring_policy')
     self.assertEqual(new,old['model_input']['state']);self.assertEqual(a,old['asset_audit'])
     for asset in a:self.assertEqual(__import__('hashlib').sha256((Path(t)/asset['file']).read_bytes()).hexdigest(),asset['sha256'])
     for q,question in p['questions'].items():self.assertEqual(question['criteria'],b.prior.LEVELS[m['question_metadata'][q]['axis']])

 def test_class_state_and_questions_stay_fixed_across_objectives(self):
  with tempfile.TemporaryDirectory() as t:
   for rep in range(2):
    values=[]
    for goal in b.GOALS:
     p,_,a=b.build_payload(Path(t),rep,goal);p['state'].pop('active_objective');values.append((p,a))
    self.assertTrue(all(v==values[0] for v in values))

 def test_no_gold_pooling_policy_or_historical_answers_in_input(self):
  forbidden={'reference','useful_methods','tiers','expected_classes','weights','min_useful','delta','historical_answers','historical_raw','historical_pooled','class_methods','rank','gold'}
  def walk(v):
   if isinstance(v,dict):
    self.assertFalse(set(v)&forbidden)
    for x in v.values():walk(x)
   elif isinstance(v,list):
    for x in v:walk(x)
  with tempfile.TemporaryDirectory() as t:
   for rep in range(2):
    for goal in b.GOALS:walk(b.build_payload(Path(t),rep,goal)[0])

 def test_budget_and_question_units_are_classes(self):
  n=0
  with tempfile.TemporaryDirectory() as t:
   for rep in range(2):
    for goal in b.GOALS:
     p,m,_=b.build_payload(Path(t),rep,goal);n+=len(p['questions']);self.assertEqual(len(p['questions']),4)
     for q in p['questions'].values():self.assertEqual(q['type'],'score');self.assertIn(q['instructions']['equivalence_class_ref'],p['state']['certified_equivalence_classes']);self.assertNotIn('candidate_ref',q['instructions'])
  self.assertEqual(n,24)

 def test_historical_mean_is_arithmetic_and_not_new_model_output(self):
  with tempfile.TemporaryDirectory() as t:
   _,m,_=b.build_payload(Path(t),0,b.GOALS[0]);h=b.historical_assessments(m)
   old=b.archived(0,b.GOALS[0]);values={}
   for q,answer in old['response']['answers'].items():
    meta=old['question_metadata'][q];method=old['candidate_mapping'][meta['candidate']];values.setdefault(method,[]).append(answer['normalized_score'])
   for c,members in m['class_methods'].items():self.assertAlmostEqual(h['pooled_class_scores'][c],sum(sum(values[x])/2 for x in members)/len(members))

 def test_internal_consistency_is_mechanical_and_cross_class_equivalence_is_separate(self):
  classes={'pair':['from_A','from_B'],'single':['from_C']}
  ref=b.prior.reference(0,'unanchored_decomposition')
  a=b.member_assessment({'pair':.9,'single':.85},classes,ref)
  self.assertTrue(a['exact_set_match']);self.assertEqual(len(a['cross_class_equivalent_pairs']),1);self.assertNotIn('equivalent_pairs',a)
  self.assertTrue(a['cross_class_equivalent_pairs'][0]['within_band'])
  bad=b.member_assessment({'pair':.9,'single':.6},classes,ref)
  self.assertFalse(bad['exact_set_match']);self.assertFalse(bad['cross_class_equivalent_pairs'][0]['within_band'])

 def test_empty_and_multiple_sets_remain_possible(self):
  classes={'pair':['from_A','from_B'],'single':['from_C']};ref=b.prior.reference(0,'intact_anchor')
  a=b.member_assessment({'pair':.3,'single':.2},classes,ref);self.assertTrue(a['empty_set'])
  a=b.member_assessment({'pair':.9,'single':.85},classes,ref);self.assertEqual(len(a['selected_classes']),2);self.assertFalse(a['exact_set_match'])
  a=b.member_assessment({'pair':.9,'single':.4},classes,ref);self.assertEqual(a['selected_methods'],['from_A','from_B']);self.assertTrue(a['exact_set_match'])

 def test_offline_guard_and_no_invented_scores(self):
  with patch.dict(os.environ,{},clear=True):
   with tempfile.TemporaryDirectory() as t:
    with self.assertRaises(SystemExit):b.main(Path(t),True)
    b.main(Path(t));r=json.loads((Path(t)/'results.json').read_text())
    self.assertEqual(r['analysis']['native_score_answers'],0);self.assertEqual(r['analysis']['groups'],0);self.assertEqual(r['analysis']['api_calls_attempted'],0)

 def test_certification_failure_cannot_be_hidden_by_class_construction(self):
  with patch.object(b.prior,'certificate',side_effect=ValueError('invalid_member')):
   with self.assertRaises(ValueError):b.class_partition(0)

if __name__=='__main__':unittest.main()

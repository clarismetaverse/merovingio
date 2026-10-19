import copy,json,os,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import benchmark_binding as b

class ConcreteBindingTests(unittest.TestCase):
 def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.out=Path(self.tmp.name)
 def tearDown(self):self.tmp.cleanup()
 def test_small_budget_and_transformation_invariant_reference(self):
  expected={'shared':(1,1),'distinct_coincident':(0,0),'partial_use':(0,0),'triangle_quadrilateral':(0,1),'wrong_host':(1,0),'omitted_valid':(0,0)}
  for replica in range(4):
   p,meta,audit=b.build_payload(self.out,replica)
   self.assertEqual(len(p['questions']),12);self.assertEqual(len(p['assets']),3)
   self.assertEqual(sum(m['valid_listed_n'] for m in meta.values()),4)
   for m in meta.values():self.assertEqual(m['valid_listed_n'],expected[m['case']][b.SCHEMAS.index(m['schema'])])
 def test_exact_one_material_reference_counterfactual(self):
  a=b.canonical('shared',37,1);c=b.canonical('distinct_coincident',37,1)
  self.assertNotEqual(a,c);c['R']['boundary_uses'][-1]['carrier']='S';self.assertEqual(a,c)
  x=b.render(a);y=b.render(b.canonical('distinct_coincident',37,1));self.assertEqual(x.tobytes(),y.tobytes())
 def test_complete_side_and_material_identity_are_independent_checks(self):
  w={'carrier':'S','regions':['L','R'],'host':'H'}
  self.assertEqual(b.check_witness(b.canonical('shared',0,1),w,b.SCHEMAS[0],'H'),[])
  self.assertIn('material_identity',b.check_witness(b.canonical('distinct_coincident',0,1),w,b.SCHEMAS[0],'H'))
  self.assertIn('incomplete_side_use',b.check_witness(b.canonical('partial_use',0,1),w,b.SCHEMAS[0],'H'))
 def test_scope_and_partition_are_distinct(self):
  objects=b.canonical('shared',0,1);w={'carrier':'S','regions':['L','R'],'host':'OUT'}
  self.assertEqual(b.check_witness(objects,w,b.SCHEMAS[0],'OUT'),[])
  self.assertIn('incomplete_host_partition',b.check_witness(objects,w,b.SCHEMAS[1],'OUT'))
  self.assertIn('wrong_scope_host',b.check_witness(objects,w,b.SCHEMAS[0],'H'))
 def test_coincident_region_decoy_and_unordered_pair(self):
  objects=b.canonical('shared',0,1)
  self.assertIn('material_identity',b.check_witness(objects,{'carrier':'S','regions':['CL','R'],'host':'H'},b.SCHEMAS[0],'H'))
  self.assertIn('overlapping_interiors',b.check_witness(objects,{'carrier':'AD','regions':['L','CL'],'host':'H'},b.SCHEMAS[0],'H'))
  self.assertEqual(b.check_witness(objects,{'carrier':'S','regions':['R','L'],'host':'H'},b.SCHEMAS[0],'H'),[])
 def test_omitted_witness_has_real_graph_binding(self):
  _,meta,_=b.build_payload(self.out,0)
  for m in meta.values():
   if m['case']=='omitted_valid':self.assertEqual(m['expected_choice'],'none');self.assertEqual(len(m['all_graph_bindings']),1)
 def test_inputs_contain_no_gold_or_case_names(self):
  p,meta,_=b.build_payload(self.out,2);text=json.dumps({k:v for k,v in p.items() if k!='assets'})
  for term in ('expected_choice','option_failures','all_graph_bindings','distinct_coincident','omitted_valid','wrong_host','GS_HIST','reference_binding'):
   self.assertNotIn(term,text)
  for q,m in meta.items():
   self.assertEqual(len(p['questions'][q]['criteria']),6)
   for label in m['option_witnesses']:self.assertNotIn(label,json.dumps(p['questions'][q]['instructions']))
 def test_every_offered_witness_is_well_typed(self):
  p,meta,_=b.build_payload(self.out,0)
  for m in meta.values():
   objects=p['state']['snapshots'][m['snapshot']]['objects']
   for w in m['option_witnesses'].values():
    self.assertEqual(objects[w['carrier']]['type'],'segment');self.assertEqual(objects[w['host']]['type'],'host')
    self.assertTrue(all(objects[k]['type']=='region' for k in w['regions']))
 def test_analysis_preserves_invalid_acceptances(self):
  p,meta,_=b.build_payload(self.out,0);answers={q:{'choice':next(iter(m['option_witnesses'])),'confidence':.9,'reliability':None} for q,m in meta.items()}
  result=b.analyze([{'replica':0,'question_metadata':meta,'response':{'answers':answers}}])
  self.assertEqual(result['native_answers'],12);self.assertGreater(sum(bool(r['selected_invalid_reasons']) for r in result['observations']),0)
  self.assertEqual(b.analyze([])['native_answers'],0)
 def test_actions_guard(self):
  with patch.dict(os.environ,{},clear=True):
   with self.assertRaises(SystemExit):b.main(self.out/'blocked',True)
   with self.assertRaises(RuntimeError):b.previous.transport({})
  self.assertFalse((self.out/'blocked').exists())

if __name__=='__main__':unittest.main()

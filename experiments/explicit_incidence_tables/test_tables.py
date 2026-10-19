import copy,json,os,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import benchmark_tables as b

class IncidenceTableTests(unittest.TestCase):
 def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.out=Path(self.tmp.name)
 def tearDown(self):self.tmp.cleanup()
 def payload(self,replica=0,case='shared',condition='graph'):return b.build_payload(self.out,replica,case,condition)
 def test_lossless_state_roundtrip_on_every_case(self):
  for replica in b.REPLICAS:
   for case in b.previous.source.CASES:
    graph=self.payload(replica,case)[0]['state'];tab=self.payload(replica,case,'incidence_tables')[0]['state']
    self.assertEqual(b.graph_state(tab),graph)
 def test_same_questions_assets_ids_and_contracts(self):
  a=self.payload()[0];c=self.payload(condition='incidence_tables')[0]
  self.assertEqual(a['questions'],c['questions']);self.assertEqual(a['assets'],c['assets'])
  self.assertEqual(a['state']['contracts'],c['state']['contracts'])
  self.assertEqual(a['state']['image_asset_manifest'],c['state']['image_asset_manifest'])
 def test_every_incidence_row_retains_carrier_endpoints_and_order(self):
  a=self.payload(case='partial_use')[0];c=self.payload(case='partial_use',condition='incidence_tables')[0]
  for ref,snapshot in a['state']['snapshots'].items():
   rows=c['state']['snapshots'][ref]['tables']['boundary_uses']['rows'];expected=[]
   for key,value in snapshot['objects'].items():
    for index,use in enumerate(value.get('boundary_uses',[])):expected.append([key,index,use['carrier'],*use['endpoints']])
   self.assertEqual(rows,expected)
 def test_no_silently_dropped_source_fields(self):
  p=self.payload()[0];objects=next(iter(p['state']['snapshots'].values()))['objects'];changed=copy.deepcopy(objects)
  next(iter(changed.values()))['extra_unrecognized_fact']='x'
  with self.assertRaises(AssertionError):b.encode_objects(changed)
 def test_graph_baseline_matches_exact_archived_input(self):
  p,_,_,_,_,source_hash=self.payload();old=b.prior_call(0,'shared')
  self.assertEqual({k:v for k,v in p.items() if k!='assets'},old['model_input']);self.assertEqual(source_hash,old['request_sha256'])
 def test_witness_failures_and_existing_bindings_are_preserved(self):
  for case in b.previous.source.CASES:
   p,meta,*_=self.payload(case=case,condition='incidence_tables');state=b.graph_state(p['state'])
   for m in meta.values():
    objects=state['snapshots'][m['snapshot']]['objects']
    self.assertEqual(b.previous.source.all_bindings(objects,m['schema'],m['query_scope_host']),m['all_graph_bindings'])
    for label,w in m['option_witnesses'].items():self.assertEqual(b.previous.source.check_witness(objects,w,m['schema'],m['query_scope_host']),m['option_failures'][label])
 def test_primary_inputs_have_no_gold_or_derived_comparison(self):
  p,meta,*_=self.payload(case='distinct_coincident',condition='incidence_tables');text=json.dumps({k:v for k,v in p.items() if k!='assets'})
  for term in ('expected_choice','option_failures','is_equal','is_full_side','valid_listed_n','historical_answers','distinct_coincident'):self.assertNotIn(term,text)
  for q,m in meta.items():
   for label in m['option_witnesses']:self.assertNotIn(label,json.dumps(p['questions'][q]['instructions']))
 def test_literal_controls_are_separate_and_use_real_ids(self):
  for replica in b.REPLICAS:
   p,meta=b.build_id_control(replica)
   self.assertNotIn('assets',p);self.assertNotIn('snapshots',p['state']);self.assertEqual(len(p['questions']),2)
   self.assertEqual({m['expected_relation'] for m in meta.values()},{'equal','distinct'})
   for q,m in meta.items():
    self.assertEqual(m['expected_relation']=='equal',m['operands']['left_id']==m['operands']['right_id'])
    self.assertNotIn(m['expected_choice'],json.dumps(p['questions'][q]['instructions']))
 def test_offline_analysis_has_no_invented_answers(self):
  a=b.analyze([]);self.assertEqual(a['native_answers'],0);self.assertEqual(a['literal_id_controls']['n'],0)
 def test_actions_guard(self):
  with patch.dict(os.environ,{},clear=True):
   with self.assertRaises(SystemExit):b.main(self.out/'blocked',True)
   with self.assertRaises(RuntimeError):b.previous.transport({})
  self.assertFalse((self.out/'blocked').exists())

if __name__=='__main__':unittest.main()

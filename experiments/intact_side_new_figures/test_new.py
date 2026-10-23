import copy,hashlib,json,math,os,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from PIL import Image
import benchmark_new as b

class NewFigureTests(unittest.TestCase):
 def test_three_hosts_are_new_nonsimilar_and_have_expected_angle_types(self):
  profiles=[]
  for figure,cfg in b.FIGURES.items():
   p=cfg['points'];dots=[]
   for vertex in 'ABC':
    others=[v for v in 'ABC' if v!=vertex];u=[p[others[0]][i]-p[vertex][i] for i in (0,1)];v=[p[others[1]][i]-p[vertex][i] for i in (0,1)];dots.append(sum(x*y for x,y in zip(u,v)))
   if figure.startswith('acute'):self.assertGreater(min(dots),0)
   elif figure.startswith('right'):self.assertEqual(min(dots),0)
   else:self.assertLess(min(dots),0)
   lengths=sorted(math.dist(p[x],p[y]) for x,y in (('A','B'),('B','C'),('C','A')))
   self.assertTrue(all(abs(lengths[i]-lengths[j])>1 for i in range(3) for j in range(i)))
   profiles.append([round(x/lengths[-1],6) for x in lengths])
  self.assertEqual(len({tuple(p) for p in profiles}),3)

 def test_all_bridges_pass_both_material_contracts_and_independent_reference(self):
  gold=[]
  for figure in b.FIGURES:
   for method in b.METHODS:
    objects=b.objects_for(figure,method);cert=b.previous.prior.certificate(objects)
    self.assertEqual(len(cert['generic_space_bindings']),2)
    yes,coverage=b.reference(objects);gold.append(yes)
    self.assertEqual(yes,method in ('A_to_near_C','B_to_near_C'))
    areas=cert['verified_metric_facts']['region_areas'];self.assertGreater(min(areas),100)
    base=[r for r in coverage['rows'] if set(r['original_side'])=={'A','B'}]
    self.assertAlmostEqual(sum(r['covered_fraction'] for r in base),1.)
    self.assertEqual(any(r['coverage']=='complete' for r in base),yes)
  self.assertEqual(sum(gold),6);self.assertEqual(len(gold),12)

 def test_checker_rejects_material_near_miss_and_incomplete_use(self):
  objects=b.objects_for('acute_scalene',b.METHODS[0]);witness={'carrier':'BRIDGE','regions':['REGION_0','REGION_1'],'host':'HOST'}
  objects['CLONE']=copy.deepcopy(objects['BRIDGE'])
  next(u for u in objects['REGION_1']['boundary_uses'] if u['carrier']=='BRIDGE')['carrier']='CLONE'
  for schema in b.base.GS.values():self.assertIn('material_identity',b.base.checker.check_witness(objects,witness,schema,'HOST'))
  with self.assertRaises(ValueError):b.previous.prior.certificate(objects)
  objects=b.objects_for('acute_scalene',b.METHODS[0]);use=next(u for u in objects['REGION_1']['boundary_uses'] if u['carrier']=='BRIDGE');use['endpoints']=[use['endpoints'][0],use['endpoints'][0]]
  for schema in b.base.GS.values():self.assertIn('incomplete_side_use',b.base.checker.check_witness(objects,witness,schema,'HOST'))

 def test_counterexamples_are_nearby_but_not_coincident_or_degenerate(self):
  for figure in b.FIGURES:
   for pair in b.PAIRS:
    relation=b.nearby_pair(figure,*pair)
    self.assertGreater(relation['relative_to_longest_host_side'],0)
    self.assertLessEqual(relation['relative_to_longest_host_side'],b.FIGURES[figure]['epsilon']+1e-8)
    self.assertNotEqual(b.objects_for(figure,pair[0])['BRIDGE'],b.objects_for(figure,pair[1])['BRIDGE'])

 def test_fixed_request_question_and_policy_match_previous_explicit_arm(self):
  old=json.loads((b.ROOT/'experiments/intact_side_diagnostic/live_results.json').read_text(encoding='utf-8'))
  old=next(c for c in old['calls'] if c['condition']=='explicit')['model_input']
  old_question=next(iter(old['questions'].values()))
  with tempfile.TemporaryDirectory() as t:
   count=0
   for figure in b.FIGURES:
    p,m,_=b.build_payload(Path(t),figure);count+=len(p['questions'])
    self.assertEqual(p['state']['active_objective']['description'],old['state']['active_objective']['description'])
    self.assertEqual(p['state']['evidence_policy'],old['state']['evidence_policy']);self.assertEqual(set(p['state']),set(old['state']))
    self.assertEqual(len(p['questions']),4)
    for q in p['questions'].values():
     self.assertEqual(q['type'],'noul');self.assertEqual(q['instructions']['question'],old_question['instructions']['question']);self.assertEqual(set(q),set(old_question))
    self.assertEqual(len(set(m['point_labels'].values())),7)
   self.assertEqual(count,12)

 def test_no_observer_labels_or_coverage_facts_enter_model_input(self):
  forbidden={'reference','gold','correct','figure','method','candidate_mapping','condition','nearby_pairs','epsilon','observer_only_coverage','certified_original_side_coverage','covered_intervals','covered_fraction','coverage','weights','composite','expected_answer'}
  def walk(value):
   if isinstance(value,dict):
    self.assertFalse(set(value)&forbidden)
    for v in value.values():walk(v)
   elif isinstance(value,list):
    for v in value:walk(v)
  with tempfile.TemporaryDirectory() as t:
   for figure in b.FIGURES:
    p,_,_=b.build_payload(Path(t),figure);walk(p)
    self.assertNotIn('long_context',json.dumps(p))

 def test_frozen_pngs_have_neutral_ids_no_embedded_text_and_exact_hashes(self):
  with tempfile.TemporaryDirectory() as t:
   for figure in b.FIGURES:
    p,m,assets=b.build_payload(Path(t),figure)
    self.assertEqual(len(assets),5)
    for asset in assets:
     path=Path(t)/asset['file'];self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),asset['sha256'])
     with Image.open(path) as im:self.assertEqual(im.size,(320,320));self.assertEqual(im.mode,'RGB');self.assertFalse(im.info)
    for method in b.METHODS:
     o=b.objects_for(figure,method)
     for point in [o[v]['xy'] for v in o if o[v]['type']=='point']:self.assertTrue(all(14<x<290 for x in point))

 def test_manifest_hash_uses_git_lf_representation_on_both_platforms(self):
  raw=b'{"fixture": 1}\r\n'
  with tempfile.TemporaryDirectory() as t,patch.object(b,'HERE',Path(t)):
   path=Path(t)/'fixtures/manifest.json';path.parent.mkdir();path.write_bytes(raw)
   expected=hashlib.sha256(raw.replace(b'\r\n',b'\n')).hexdigest();self.assertEqual(b.fixture_manifest_sha256(),expected)
   path.write_bytes(raw.replace(b'\r\n',b'\n'));self.assertEqual(b.fixture_manifest_sha256(),expected)

 def test_aliases_and_candidate_positions_are_not_fixed_by_reference(self):
  orders=[]
  for figure in b.FIGURES:
   mapping,labels,gs=b.layout(figure);orders.append(tuple(b.reference(b.objects_for(figure,m))[0] for m in mapping.values()))
   self.assertTrue(all(c.startswith('C') and c[1:].isdigit() for c in mapping))
  self.assertGreater(len(set(orders)),1)

 def test_live_guard_blocks_local_calls(self):
  with tempfile.TemporaryDirectory() as t,patch.dict(os.environ,{},clear=True),patch.object(b.previous,'transport') as transport:
   with self.assertRaises(SystemExit):b.main(Path(t),True)
   transport.assert_not_called()

 def test_offline_audit_has_zero_empirical_answers(self):
  from audit_new import audit
  with tempfile.TemporaryDirectory() as t:
   b.main(Path(t));result=audit(Path(t));self.assertEqual(result['requests_reconstructed'],3);self.assertEqual(result['native_noul_answers_verified'],0);self.assertEqual(result['material_contract_checks'],24)

 def test_partial_and_complete_live_reporting_with_mock_transport(self):
  from audit_new import audit
  def fixture(payload):return {'response':b.previous.sanitize({'model':'jev-1.14.0','answers':{q:{'type':'noul','noul':.25} for q in payload['questions']}},payload['questions']),'elapsed_seconds':0.}
  with tempfile.TemporaryDirectory() as t,patch.dict(os.environ,{'GITHUB_ACTIONS':'true','TYPESAFE_API_KEY':'test-only'},clear=True),patch.object(b.previous,'transport',side_effect=fixture) as transport:
   b.main(Path(t),True);self.assertEqual(transport.call_count,3);result=audit(Path(t));self.assertEqual(result['native_noul_answers_verified'],12)
  # Mock fixture lives only in a temporary directory and is not empirical data.

 def test_rejected_call_stops_without_retry_and_saves_failure(self):
  with tempfile.TemporaryDirectory() as t,patch.dict(os.environ,{'GITHUB_ACTIONS':'true','TYPESAFE_API_KEY':'test-only'},clear=True),patch.object(b.previous,'transport',return_value={'failure':'HTTP_403'}) as transport:
   with self.assertRaises(SystemExit):b.main(Path(t),True)
   self.assertEqual(transport.call_count,1);report=json.loads((Path(t)/'results.json').read_text());self.assertEqual(report['status'],'request_rejected');self.assertEqual(report['analysis']['native_noul_answers'],0)

if __name__=='__main__':unittest.main()

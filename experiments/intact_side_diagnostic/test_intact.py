import copy,json,os,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch,Mock
import benchmark_intact as b

class IntactSideTests(unittest.TestCase):
 def test_complete_partial_none_are_geometric_and_transform_invariant(self):
  for rep in range(2):
   for method in b.prior.METHODS:
    objects=b.prior.objects_for(method,rep);cert=b.coverage_certificate(objects,{v:v for v in 'ABCDEF'},'candidate')
    rows=cert['rows'];self.assertEqual(len(rows),6)
    base=[r for r in rows if set(r['original_side'])=={'A','B'}]
    self.assertEqual(any(r['coverage']=='complete' for r in base),b.prior.useful(objects,'intact_anchor'))
    self.assertEqual(sorted(r['covered_fraction'] for r in base),[.5,.5] if method=='from_C' else [0.,1.])
    self.assertEqual(sorted({tuple(r['original_side']) for r in rows}),[('A','B'),('B','C'),('C','A')])

 def test_interval_union_handles_reversal_overlap_gaps_and_clipping(self):
  f=lambda segments:b.projected_coverage([0,0],[10,0],segments)
  self.assertEqual(f([([5,0],[0,0]),([10,0],[5,0])])['coverage'],'complete')
  self.assertEqual(f([([-2,0],[7,0]),([5,0],[12,0])])['covered_intervals'],[[0.,1.]])
  self.assertEqual(f([([0,0],[4,0]),([6,0],[10,0])])['covered_fraction'],.8)
  self.assertEqual(f([([0,1],[10,1]),([0,0],[0,0])])['coverage'],'none')
  self.assertEqual(b.projected_coverage([10,0],[0,0],[([0,0],[4,0])])['covered_intervals'],[[.6,1.]])
  with self.assertRaises(ValueError):b.projected_coverage([0,0],[0,0],[])

 def test_coverage_uses_boundary_uses_not_endpoint_membership_or_gold(self):
  objects=b.prior.objects_for('from_A',0)
  objects['D']={'type':'point','xy':[(x+y)/2 for x,y in zip(objects['A']['xy'],objects['B']['xy'])]}
  # A,B remain region vertices, but shortening its actual boundary use removes full coverage.
  region=objects['REGION_0'];use=next(u for u in region['boundary_uses'] if set(u['endpoints'])=={'A','B'})
  use['endpoints']=['A','D']
  with patch.object(b.prior,'useful',side_effect=AssertionError('gold consulted')),patch.object(b.prior,'reference',side_effect=AssertionError('gold consulted')):
   cert=b.coverage_certificate(objects,{v:v for v in 'ABCDEF'},'X')
  self.assertFalse(any(r['coverage']=='complete' for r in cert['rows'] if set(r['original_side'])=={'A','B'}))

 def test_frozen_source_and_only_declared_interventions(self):
  with tempfile.TemporaryDirectory() as t:
   for rep in range(2):
    values={c:b.build_payload(Path(t),rep,c) for c in b.CONDITIONS}
    p,m,a=values['current'];old=b.archive.archived(rep,'intact_anchor')
    expected=copy.deepcopy(old['model_input']['state']);expected['evidence_policy']=b.POLICY
    self.assertEqual(p['state'],expected);self.assertEqual(a,old['asset_audit'])
    for condition in b.CONDITIONS:
     other,meta,audit=values[condition]
     self.assertEqual(other['questions'],p['questions']);self.assertEqual(other['assets'],p['assets']);self.assertEqual(audit,a)
     self.assertEqual(meta['candidate_mapping'],m['candidate_mapping']);self.assertEqual(meta['reference'],m['reference'])
    explicit=copy.deepcopy(values['explicit'][0]);explicit['state']['active_objective']['description']=p['state']['active_objective']['description']
    self.assertEqual(explicit,p)
    coverage=copy.deepcopy(values['coverage'][0]);coverage['state'].pop('certified_original_side_coverage')
    self.assertEqual(coverage,values['explicit'][0])

 def test_budget_and_one_binary_question_per_candidate_version(self):
  count=0
  with tempfile.TemporaryDirectory() as t:
   for rep in range(2):
    for condition in b.CONDITIONS:
     p,m,_=b.build_payload(Path(t),rep,condition);self.assertEqual(len(p['questions']),3);count+=3
     self.assertEqual({q['instructions']['candidate_ref'] for q in p['questions'].values()},set(m['candidate_mapping']))
     for q in p['questions'].values():self.assertEqual(set(q),{'type','instructions'});self.assertEqual(q['type'],'noul')
  self.assertEqual(count,18)

 def test_reference_not_sent_and_certificate_is_all_sides_without_verdicts(self):
  forbidden={'reference','gold','correct','useful_methods','tiers','condition','prior_request_sha256','candidate_meets_goal','expected_answer','composite','weights','historical_answers'}
  def walk(value):
   if isinstance(value,dict):
    self.assertFalse(set(value)&forbidden)
    for v in value.values():walk(v)
   elif isinstance(value,list):
    for v in value:walk(v)
  with tempfile.TemporaryDirectory() as t:
   for rep in range(2):
    for condition in b.CONDITIONS:walk(b.build_payload(Path(t),rep,condition)[0])
  source=Path(b.__file__).read_text(encoding='utf-8')
  self.assertNotIn('long_context',source)

 def test_certified_rows_use_same_candidate_region_and_point_ids(self):
  with tempfile.TemporaryDirectory() as t:
   p,m,_=b.build_payload(Path(t),1,'coverage');labels=m['point_labels']
   for candidate,cert in p['state']['certified_original_side_coverage'].items():
    for row in cert['rows']:
     self.assertIn(row['region'],['R_'+candidate+'_1','R_'+candidate+'_2'])
     self.assertTrue(set(row['original_side'])<=set(labels[v] for v in 'ABC'))
     index=int(row['region'][-1])-1
     if row['coverage']=='complete':self.assertTrue(set(row['original_side'])<=set(p['state']['admissible_bridges'][candidate]['region_vertex_cycles'][index]))

 def test_sanitizer_preserves_native_values_and_drops_free_text(self):
  raw={'model':'jev-1.14.0','answers':{'Q':{'type':'noul','noul':.42,'explanation':'secret','confidence':.3}},'usage':{'input_tokens':12,'other':'secret'},'debug':'secret'}
  clean=b.sanitize(raw,{'Q':{}});self.assertEqual(clean['answers']['Q']['noul'],.42);self.assertIsNone(clean['answers']['Q']['reliability']);self.assertIsNone(clean['usage']['total_tokens'])
  self.assertNotIn('secret',json.dumps(clean))
  for invalid in (True,float('nan'),1.1,None):
   changed=copy.deepcopy(raw);changed['answers']['Q']['noul']=invalid
   with self.assertRaises(ValueError):b.sanitize(changed,{'Q':{}})
  with self.assertRaises(ValueError):b.sanitize(raw,{'OTHER':{}})

 def test_actions_guard_prevents_local_network(self):
  request_module=Mock()
  with patch.dict(os.environ,{},clear=True),patch.dict(sys.modules,{'requests':request_module}):
   with self.assertRaises(RuntimeError):b.transport({})
   with tempfile.TemporaryDirectory() as t:
    with self.assertRaises(SystemExit):b.main(Path(t),True)
   request_module.post.assert_not_called()

 def test_transport_headers_sanitizes_errors_and_never_retries(self):
  with patch.dict(os.environ,{'GITHUB_ACTIONS':'true','TYPESAFE_API_KEY':'test-secret-only'},clear=True):
   request_module=Mock();request_module.post.return_value=Mock(status_code=403,text='sensitive')
   with patch.dict(sys.modules,{'requests':request_module}):
    post=request_module.post
    result=b.transport({'questions':{}});self.assertEqual(result['failure'],'HTTP_403');self.assertNotIn('sensitive',json.dumps(result));self.assertEqual(post.call_count,1)
    self.assertEqual(post.call_args.kwargs['headers']['TypeSafe-Danger-Zone-Images'],'true')
   request_module=Mock();request_module.post.side_effect=RuntimeError('sensitive')
   with patch.dict(sys.modules,{'requests':request_module}):
    post=request_module.post
    self.assertEqual(b.transport({})['failure'],'transport_or_noul_schema_failure');self.assertEqual(post.call_count,1)

 def test_metrics_include_negatives_ties_and_always_yes_baseline(self):
  with tempfile.TemporaryDirectory() as t:
   _,m,_=b.build_payload(Path(t),0,'current')
  m['response']={'answers':{q:{'noul':1.} for q in m['question_metadata']},'usage':{}}
  a=b.analyze([m])['by_condition']['current'];self.assertEqual(a['correct'],2);self.assertEqual(a['always_yes_correct'],2);self.assertEqual(a['matrix']['fp'],1)
  for answer in m['response']['answers'].values():answer['noul']=.5
  a=b.analyze([m])['by_condition']['current'];self.assertEqual(a['correct'],0);self.assertEqual(a['matrix']['abstain_positive'],2);self.assertEqual(a['matrix']['abstain_negative'],1)

 def test_offline_save_and_audit(self):
  from audit_intact import audit
  with tempfile.TemporaryDirectory() as t:
   out=Path(t);b.main(out);result=audit(out)
   self.assertEqual(result['requests_reconstructed'],6);self.assertEqual(result['native_noul_answers_verified'],0)
   self.assertIn('nessuna risposta', (out/'viewer.html').read_text(encoding='utf-8'))

 def test_partial_live_viewer_and_resume_keep_original_answers_without_network(self):
  source=Path(b.__file__).parent/'interrupted_run.json'
  with tempfile.TemporaryDirectory() as t:
   records,provenance=b.resume_records(source,Path(t))
   self.assertEqual(len(records),1);self.assertEqual(provenance['reused_requests'],1);self.assertEqual(provenance['repeated_requests'],0)
   old=json.loads(source.read_text(encoding='utf-8'));self.assertEqual(records[0]['response'],old['calls'][0]['response'])
   b.save(Path(t),old);self.assertIn('non disponibile',(Path(t)/'viewer.html').read_text(encoding='utf-8'))

 def test_resume_rejects_changed_requests(self):
  source=Path(b.__file__).parent/'interrupted_run.json';data=json.loads(source.read_text(encoding='utf-8'));data['calls'][0]['request_sha256']='bad'
  with tempfile.TemporaryDirectory() as t:
   path=Path(t)/'tampered.json';path.write_text(json.dumps(data),encoding='utf-8')
   with self.assertRaises(AssertionError):b.resume_records(path,Path(t))

 def test_resume_runner_sends_only_five_missing_requests_and_audits_combined_data(self):
  from audit_intact import audit
  source=Path(b.__file__).parent/'interrupted_run.json'
  def fake_transport(payload):
   # Synthetic transport fixture only; never saved as empirical results.
   return {'response':b.sanitize({'model':'jev-1.14.0','answers':{q:{'type':'noul','noul':.25} for q in payload['questions']}},payload['questions']),'elapsed_seconds':0.}
  with tempfile.TemporaryDirectory() as t,patch.dict(os.environ,{'GITHUB_ACTIONS':'true','TYPESAFE_API_KEY':'test-only','GITHUB_RUN_ID':'offline-test','GITHUB_SHA':'test-only'},clear=True),patch.object(b,'transport',side_effect=fake_transport) as transport:
   b.main(Path(t),True,source);self.assertEqual(transport.call_count,5)
   result=audit(Path(t));self.assertEqual(result['native_noul_answers_verified'],18);self.assertEqual(result['reused_requests'],1)

if __name__=='__main__':unittest.main()

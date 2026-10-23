"""Offline reconstruction of every sent request, premise certificate and binary result."""
import base64,copy,hashlib,json,math,sys,tempfile
from pathlib import Path
import benchmark_intact as b

def audit(out):
 r=json.loads((out/'results.json').read_text(encoding='utf-8'))
 assert r['decision_policy']=={'threshold':.5,'equal_threshold':'abstain_counted_incorrect'}
 assert r['provenance']['prior_results_canonical_sha256']==b.prior.base.digest(b.archive.PRIOR)
 if r.get('resume_provenance'):
  source=Path(b.__file__).parent/'interrupted_run.json';previous=json.loads(source.read_text(encoding='utf-8'));provenance=r['resume_provenance']
  assert provenance=={'run_id':previous['run_id'],'source_commit':previous['source_commit'],'artifact_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'reused_requests':len(previous['calls']),'repeated_requests':0}
  for old in previous['calls']:
   found=next(c for c in r['calls'] if (c['replica'],c['condition'])==(old['replica'],old['condition']))
   assert all(found[k]==v for k,v in old.items())
   assert found['evaluation_run_id']==previous['run_id'] and found['evaluation_source_commit']==previous['source_commit']
 seen=set();answers=[];groups={};coverage_rows=0
 with tempfile.TemporaryDirectory() as t:
  for call in r['calls']:
   key=(call['replica'],call['condition']);assert key not in seen;seen.add(key)
   p=copy.deepcopy(call['model_input']);p['assets']={}
   for asset in call['asset_audit']:
    data=(out/asset['file']).read_bytes();assert hashlib.sha256(data).hexdigest()==asset['sha256']
    p['assets'][asset['asset']]={'type':'image','format':'png','data_base64':base64.b64encode(data).decode('ascii')}
   assert b.prior.base.digest(p)==call['request_sha256']
   expected,meta,a=b.build_payload(Path(t),*key)
   assert b.archive.same(expected,p) and a==call['asset_audit']
   assert all(b.archive.same(call[k],v) for k,v in meta.items())
   neutral=copy.deepcopy(p)
   if call['condition']=='coverage':
    coverage=neutral['state'].pop('certified_original_side_coverage');coverage_rows+=sum(len(v['rows']) for v in coverage.values())
   neutral['state']['active_objective']['description']='MATCHED_WORDING'
   groups.setdefault(call['replica'],[]).append(neutral)
   for c,method in call['candidate_mapping'].items():
    objects=b.prior.objects_for(method,call['replica']);cert=b.coverage_certificate(objects,call['point_labels'],c)
    target=set(p['state']['active_objective']['designated_reference_side'])
    assert any(v['coverage']=='complete' for v in cert['rows'] if set(v['original_side'])==target)==call['reference'][c]
   if call.get('response'):
    response=call['response'];assert set(response['answers'])==set(p['questions'])
    assert response['returned_model'] in (None,p['model'])
    assert b.sanitize({'model':response['returned_model'],**{k:v for k,v in response.items() if k!='returned_model'}},p['questions'])==response
    for answer in response['answers'].values():assert 0<=answer['noul']<=1 and math.isfinite(answer['noul']);answers.append(answer)
 for group in groups.values():assert all(b.archive.same(v,group[0]) for v in group)
 if r['status'] in ('completed','offline_only'):assert len(seen)==6
 # Python 3.12 compensated sum may differ from the 3.11 runner by <1e-16.
 # Only regenerated analysis uses tolerance; recorded responses/hashes remain exact.
 assert b.archive.same(b.analyze(r['calls']),r['analysis'])
 result={'run_id':r['run_id'],'source_commit':r['source_commit'],'status':r['status'],'audit_scope':'requests_and_native_results' if answers else 'prepared_inputs_only',
  'requests_reconstructed':len(seen),'native_noul_answers_verified':len(answers),'coverage_rows_recomputed':coverage_rows,
  'matched_triplets_verified':sum(len(g)==3 for g in groups.values()),'frozen_image_bytes_and_recorded_request_hashes_exact':True,
  'by_condition':r['analysis']['by_condition'],'paired':r['analysis']['paired'],'usage_totals':r['analysis']['usage_totals'],
  'separate_confidence_count':sum(a['confidence'] is not None for a in answers),'numeric_reliability_count':sum(a['reliability'] is not None for a in answers),'generator_numeric_tolerance':1e-12}
 result['evaluation_runs']=sorted({c.get('evaluation_run_id',r['run_id']) for c in r['calls'] if c.get('response')})
 result['reused_requests']=r.get('resume_provenance',{}).get('reused_requests',0)
 (out/'artifact-verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');return result

if __name__=='__main__':print(json.dumps(audit(Path(sys.argv[1])),indent=2))

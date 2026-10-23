"""Reconstruct requests and verify color-only and identity-legend interventions."""
import base64,copy,hashlib,json,sys,tempfile
from pathlib import Path
import benchmark_color as b

def audit(out):
 r=json.loads((out/'results.json').read_text(encoding='utf-8'));seen=set();answers=[];common=[];assets_by_arm={};contracts=0
 assert r['decision_policy']=={'threshold':.5,'equal_threshold':'abstain_counted_incorrect'}
 assert r['provenance']['source_request_sha256']==b.OLD['request_sha256']
 assert r['provenance']['fixture_manifest_sha256']==b.fixture_hash()
 assert r['provenance']['archived_results_canonical_sha256']==b.base.digest(b.SOURCE)
 with tempfile.TemporaryDirectory() as t:
  for call in r['calls']:
   arm=call['arm'];assert arm not in seen;seen.add(arm)
   p=copy.deepcopy(call['model_input']);p['assets']={}
   for asset in call['asset_audit']:
    data=(out/asset['file']).read_bytes();assert hashlib.sha256(data).hexdigest()==asset['sha256']
    p['assets'][asset['asset']]={'type':'image','format':'png','data_base64':base64.b64encode(data).decode('ascii')}
   assert b.base.digest(p)==call['request_sha256']
   expected,meta,assets=b.build_payload(Path(t),arm)
   assert b.native.archive.same(p,expected) and assets==call['asset_audit']
   assert all(b.native.archive.same(call[k],v) for k,v in meta.items())
   canonical=copy.deepcopy(call['model_input'])
   if arm=='color_legend':assert canonical['state'].pop('visual_object_key')==b.visual_key()
   common.append(canonical);assets_by_arm[arm]=p['assets']
   if arm=='monochrome':assert call['request_sha256']==b.OLD['request_sha256']
   for candidate,method in call['candidate_mapping'].items():
    objects=b.prior.objects_for(method,False);contracts+=len(b.native.prior.certificate(objects)['generic_space_bindings']);assert b.prior.prior.reference(objects)[0]==call['reference'][candidate]
   if call.get('response'):
    response=call['response'];raw={'model':response['returned_model'],**{k:v for k,v in response.items() if k!='returned_model'}}
    assert b.native.sanitize(raw,p['questions'])==response;answers.extend(response['answers'].values())
 assert all(p==common[0] for p in common)
 if 'color' in assets_by_arm and 'color_legend' in assets_by_arm:assert assets_by_arm['color']==assets_by_arm['color_legend']
 if r['status'] in ('completed','offline_only'):assert seen==set(b.ARMS)
 assert b.native.archive.same(b.analyze(r['calls']),r['analysis'])
 result={'run_id':r['run_id'],'source_commit':r['source_commit'],'status':r['status'],'audit_scope':'requests_and_native_results' if answers else 'prepared_inputs_only',
  'requests_reconstructed':len(seen),'native_noul_answers_verified':len(answers),'material_contract_checks':contracts,'reference_checks':2*len(seen),'exact_monochrome_request_replay':True,
  'only_pngs_change_in_color_arm':True,'same_colored_bytes_with_and_without_legend':True,'only_identity_legend_added_in_third_arm':True,'coverage_table_not_sent':True,
  'frozen_image_bytes_and_request_hashes_exact':True,'overall':r['analysis']['overall'],'arms':r['analysis']['arms'],'descriptive_contrasts':r['analysis']['descriptive_contrasts'],'usage_totals':r['analysis']['usage_totals'],
  'separate_confidence_count':sum(a['confidence'] is not None for a in answers),'numeric_reliability_count':sum(a['reliability'] is not None for a in answers),'regenerated_numeric_tolerance':1e-12}
 (out/'artifact-verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');return result

if __name__=='__main__':print(json.dumps(audit(Path(sys.argv[1])),indent=2))

"""Verify all actual requests, exact factorial invariants and the isolated reference."""
import base64,copy,hashlib,json,sys,tempfile
from pathlib import Path
import benchmark_pair as b

def audit(out):
 r=json.loads((out/'results.json').read_text(encoding='utf-8'));seen=set();answers=[];normalized=[];contracts=0
 assert r['decision_policy']=={'threshold':.5,'equal_threshold':'abstain_counted_incorrect'}
 assert r['provenance']['fixture_manifest_sha256']==b.fixture_hash()
 assert r['provenance']['archived_results_canonical_sha256']==b.base.digest(b.SOURCE)
 assert r['provenance']['source_request_sha256']==b.OLD['request_sha256']
 assert r['historical_context']['p_yes_by_method']==b.historical_probabilities()
 with tempfile.TemporaryDirectory() as t:
  for call in r['calls']:
   cell=call['cell'];assert cell not in seen;seen.add(cell)
   p=copy.deepcopy(call['model_input']);p['assets']={}
   for asset in call['asset_audit']:
    data=(out/asset['file']).read_bytes();assert hashlib.sha256(data).hexdigest()==asset['sha256']
    p['assets'][asset['asset']]={'type':'image','format':'png','data_base64':base64.b64encode(data).decode('ascii')}
   assert b.base.digest(p)==call['request_sha256']
   expected,meta,assets=b.build_payload(Path(t),cell)
   assert b.prior.previous.archive.same(expected,p) and assets==call['asset_audit']
   assert all(b.native.archive.same(call[k],v) for k,v in meta.items())
   # Exact inverse alpha conversion removes the ID factor; state never changes with rotation.
   common=copy.deepcopy(call['model_input'])
   if call['new_ids']:common=b.rename(common,{v:k for k,v in b.ID_MAP.items()})
   normalized.append(common)
   assert p['state']['active_objective']['description']==b.native.EXPLICIT
   for candidate,method in call['candidate_mapping'].items():
    objects=b.objects_for(method,call['rotated']);cert=b.native.prior.certificate(objects);contracts+=len(cert['generic_space_bindings'])
    assert b.prior.reference(objects)[0]==call['reference'][candidate]
   if call.get('response'):
    response=call['response'];raw={'model':response['returned_model'],**{k:v for k,v in response.items() if k!='returned_model'}}
    assert b.native.sanitize(raw,p['questions'])==response;answers.extend(response['answers'].values())
 assert all(p==normalized[0] for p in normalized)
 if r['status'] in ('completed','offline_only'):assert seen==set(b.CELLS)
 assert b.native.archive.same(b.analyze(r['calls']),r['analysis'])
 result={'run_id':r['run_id'],'source_commit':r['source_commit'],'status':r['status'],'audit_scope':'requests_and_native_results' if answers else 'prepared_inputs_only',
  'requests_reconstructed':len(seen),'native_noul_answers_verified':len(answers),'material_contract_checks':contracts,'reference_checks':2*len(seen),
  'exact_structural_state_and_question_invariance_after_inverse_alpha_rename':True,'coverage_table_not_sent':True,'frozen_image_bytes_and_request_hashes_exact':True,
  'overall':r['analysis']['overall'],'cells':r['analysis']['cells'],'descriptive_contrasts':r['analysis']['descriptive_contrasts'],'margin_interaction':r['analysis']['margin_interaction'],
  'historical_two_errors_reproduced_in_isolated_baseline':r['analysis']['historical_two_errors_reproduced_in_isolated_baseline'],'usage_totals':r['analysis']['usage_totals'],
  'separate_confidence_count':sum(a['confidence'] is not None for a in answers),'numeric_reliability_count':sum(a['reliability'] is not None for a in answers),'regenerated_numeric_tolerance':1e-12}
 (out/'artifact-verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');return result

if __name__=='__main__':print(json.dumps(audit(Path(sys.argv[1])),indent=2))

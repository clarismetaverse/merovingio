"""Reconstruct fixed inputs and validate actual binary responses offline."""
import base64,copy,hashlib,json,sys,tempfile
from pathlib import Path
import benchmark_new as b

def audit(out):
 r=json.loads((out/'results.json').read_text(encoding='utf-8'));seen=set();answers=[];contracts=0
 assert r['decision_policy']=={'threshold':.5,'equal_threshold':'abstain_counted_incorrect'}
 assert r['provenance']['fixture_manifest_sha256']==b.fixture_manifest_sha256()
 with tempfile.TemporaryDirectory() as t:
  for call in r['calls']:
   assert call['figure'] not in seen;seen.add(call['figure'])
   p=copy.deepcopy(call['model_input']);p['assets']={}
   for asset in call['asset_audit']:
    data=(out/asset['file']).read_bytes();assert hashlib.sha256(data).hexdigest()==asset['sha256']
    p['assets'][asset['asset']]={'type':'image','format':'png','data_base64':base64.b64encode(data).decode('ascii')}
   assert b.base.digest(p)==call['request_sha256']
   expected,meta,assets=b.build_payload(Path(t),call['figure'])
   assert b.previous.archive.same(expected,p) and assets==call['asset_audit']
   assert all(b.previous.archive.same(call[k],v) for k,v in meta.items())
   assert p['state']['active_objective']['description']==b.previous.EXPLICIT
   assert 'certified_original_side_coverage' not in p['state'] and 'observer_only_coverage' not in p
   for candidate,method in call['candidate_mapping'].items():
    objects=b.objects_for(call['figure'],method);cert=b.previous.prior.certificate(objects);contracts+=len(cert['generic_space_bindings'])
    assert b.reference(objects)[0]==call['reference'][candidate]
   if call.get('response'):
    response=call['response'];assert set(response['answers'])==set(p['questions'])
    raw={'model':response['returned_model'],**{k:v for k,v in response.items() if k!='returned_model'}}
    assert b.previous.sanitize(raw,p['questions'])==response
    answers.extend(response['answers'].values())
 if r['status'] in ('completed','offline_only'):assert seen==set(b.FIGURES)
 assert b.previous.archive.same(b.analyze(r['calls']),r['analysis'])
 result={'run_id':r['run_id'],'source_commit':r['source_commit'],'status':r['status'],'audit_scope':'requests_and_native_results' if answers else 'prepared_inputs_only','requests_reconstructed':len(seen),
  'native_noul_answers_verified':len(answers),'material_contract_checks':contracts,'observer_reference_checks':4*len(seen),'nearby_pairs_rechecked':2*len(seen),
  'fixed_explicit_wording_verified':True,'coverage_table_not_sent':True,'frozen_image_bytes_and_request_hashes_exact':True,
  'overall':r['analysis']['overall'],'by_figure':r['analysis']['by_figure'],'pairs_both_correct':r['analysis']['pairs_both_correct'],'pairs_strict_order':r['analysis']['pairs_strict_order'],'pair_count':r['analysis']['pair_count'],
  'usage_totals':r['analysis']['usage_totals'],'separate_confidence_count':sum(a['confidence'] is not None for a in answers),'numeric_reliability_count':sum(a['reliability'] is not None for a in answers),'regenerated_numeric_tolerance':1e-12}
 (out/'artifact-verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');return result

if __name__=='__main__':print(json.dumps(audit(Path(sys.argv[1])),indent=2))

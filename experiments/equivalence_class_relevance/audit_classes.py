"""Reconstruct every actual class request and both archived baselines offline."""
import base64,hashlib,json,math,statistics,sys,tempfile
from pathlib import Path
import benchmark_classes as b

def audit(out):
 r=json.loads((out/'results.json').read_text(encoding='utf-8'))
 assert r['weights']==b.WEIGHTS and r['set_policy']=={'delta':b.DELTA,'min_useful':b.MIN_USEFUL,'sensitivity_deltas':list(b.SENSITIVITY_DELTAS)}
 assert r['provenance']['prior_results_canonical_sha256']==b.prior.base.digest(b.PRIOR)
 answers=[];groups={};pd=[];sd=[];material_checks=0;partition_checks=0
 with tempfile.TemporaryDirectory() as temporary:
  for call in r['calls']:
   p=json.loads(json.dumps(call['model_input']));p['assets']={}
   for asset in call['asset_audit']:
    data=(out/asset['file']).read_bytes();assert hashlib.sha256(data).hexdigest()==asset['sha256']
    p['assets'][asset['asset']]={'type':'image','format':'png','data_base64':base64.b64encode(data).decode('ascii')}
   assert b.prior.base.digest(p)==call['request_sha256']
   expected,meta,a=b.build_payload(Path(temporary),call['replica'],call['goal'])
   assert b.same({k:v for k,v in expected.items() if k!='assets'},call['model_input'])
   assert expected['assets']==p['assets'] and a==call['asset_audit']
   assert all(b.same(call[k],v) for k,v in meta.items())
   assert list(call['class_methods'])==list(meta['class_methods'])
   for members in b.class_partition(call['replica']):
    for m in members:assert b.prior.certificate(b.prior.objects_for(m,call['replica']))['admissible'];material_checks+=2
   partition_checks+=1
   neutral=json.loads(json.dumps(call['model_input']));neutral['state'].pop('active_objective')
   groups.setdefault(call['replica'],[]).append((neutral,call['asset_audit']))
   if call.get('response'):
    response=call['response'];assert set(response['answers'])==set(p['questions']);assert response['returned_model'] in (None,p['model'])
    for q,answer in response['answers'].items():
     assert answer['type']=='score' and math.isfinite(answer['score']) and 0<=answer['score']<=3
     assert abs(answer['normalized_score']-answer['score']/3)<1e-12
     probs=answer['probabilities'];assert set(probs)=={'0','1','2','3'} and all(0<=v<=1 for v in probs.values())
     pd.append(abs(sum(probs.values())-1));assert pd[-1]<.041
     sd.append(abs(answer['score']-sum(int(k)*v for k,v in probs.items())));answers.append(answer)
 for group in groups.values():assert all(b.same(pair[0],group[0][0]) and pair[1]==group[0][1] for pair in group)
 assert b.analyze(r['calls'])==r['analysis']
 a=r['analysis'];confidence=[v['confidence'] for v in answers if v['confidence'] is not None]
 report={'run_id':r['run_id'],'source_commit':r['source_commit'],'status':r['status'],'audit_scope':'requests_and_native_results' if answers else 'prepared_inputs_only',
  'requests_reconstructed':len(r['calls']),'native_score_answers_verified':len(answers),'material_contract_checks':material_checks,'isometry_partitions_rechecked':partition_checks,
  'objective_only_presentations_verified':sum(len(group)==3 for group in groups.values()),'recorded_hashes_and_frozen_asset_bytes_exact':True,
  'groups':a['groups'],'exact_set_matches':a['exact_set_matches'],'historical_raw_exact_set_matches':a['historical_raw_exact_set_matches'],
  'historical_pooled_exact_set_matches':a['historical_pooled_exact_set_matches'],'strict_class_wins':a['strict_class_wins'],'strict_class_total':a['strict_class_total'],
  'cross_class_equivalent_in_band':a['cross_class_equivalent_in_band'],'cross_class_equivalent_total':a['cross_class_equivalent_total'],
  'internal_class_equality_imposed_by_code_not_a_model_metric':True,'member_matrix':a['member_matrix'],'class_matrix':a['class_matrix'],'sensitivity':a['sensitivity'],
  'usage_totals':a['usage_totals'],'mean_reported_confidence':statistics.mean(confidence) if confidence else None,'numeric_reliability_count':sum(v['reliability'] is not None for v in answers),
  'max_probability_sum_deviation':max(pd,default=None),'max_native_score_expected_probability_deviation':max(sd,default=None),'source_scalar_reconstruction_tolerance':1e-12}
 (out/'artifact-verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');return report

if __name__=='__main__':print(json.dumps(audit(Path(sys.argv[1])),indent=2))

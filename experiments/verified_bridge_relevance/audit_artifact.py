"""Audit recorded requests and native results offline; never calls a model."""
import base64,hashlib,json,math,statistics,sys,tempfile
from pathlib import Path
import benchmark_relevance as b

def audit(out):
 r=json.loads((out/'results.json').read_text(encoding='utf-8'));pairs={};answers=[];certificates=0;sum_deltas=[];score_deltas=[]
 assert r['weights']==b.WEIGHTS
 with tempfile.TemporaryDirectory() as temp:
  for call in r['calls']:
   payload=json.loads(json.dumps(call['model_input']));payload['assets']={}
   for asset in call['asset_audit']:
    data=(out/asset['file']).read_bytes();assert hashlib.sha256(data).hexdigest()==asset['sha256']
    payload['assets'][asset['asset']]={'type':'image','format':'png','data_base64':base64.b64encode(data).decode('ascii')}
   assert b.digest(payload)==call['request_sha256']
   expected,meta,images=b.build_payload(Path(temp),call['replica'],call['goal_vertex'])
   # Local fonts may differ between hosts: verify recorded raster hashes, and compare all non-raster fields.
   assert {k:v for k,v in expected.items() if k!='assets'}==call['model_input']
   assert set(expected['assets'])==set(payload['assets'])
   assert all(call[k]==v for k,v in meta.items())
   for method in b.METHODS:
    cert=b.certificate(b.objects_for(method,call['replica']));assert len(cert['generic_space_bindings'])==2;certificates+=2
   base=json.loads(json.dumps(call['model_input']));base['state'].pop('active_objective')
   pairs.setdefault(call['replica'],[]).append((base,call['asset_audit']))
   response=call.get('response')
   if response:
    assert set(response['answers'])==set(payload['questions'])
    for q,a in response['answers'].items():
     assert a['type']=='score' and math.isfinite(a['score']) and 0<=a['score']<=3
     assert abs(a['normalized_score']-a['score']/3)<1e-12
     probs=a['probabilities'];assert set(probs)=={'0','1','2','3'} and all(0<=v<=1 for v in probs.values())
     sum_deltas.append(abs(sum(probs.values())-1));assert sum_deltas[-1]<.041
     score_deltas.append(abs(a['score']-sum(int(k)*v for k,v in probs.items())))
     answers.append(a)
 assert b.analyze(r['calls'])==r['analysis']
 for group in pairs.values():assert all(c==group[0] for c in group)
 confidence=[a['confidence'] for a in answers if a['confidence'] is not None]
 report={'run_id':r['run_id'],'source_commit':r['source_commit'],'status':r['status'],'audit_scope':'requests_and_native_results' if answers else 'prepared_inputs_only',
  'requests_reconstructed':len(r['calls']),'native_score_answers_verified':len(answers),'local_contract_checks':certificates,
  'objective_only_replicas':sum(len(g)==3 for g in pairs.values()),'all_image_hashes_verified':True,
  'rankings_recomputed':r['analysis']['ranking_groups'],'unique_reference_top':r['analysis']['unique_reference_top'],
  'pairwise_reference_wins':r['analysis']['pairwise_reference_wins'],'pairwise_reference_ties':r['analysis']['pairwise_reference_ties'],
  'goal_sensitive_bridges':r['analysis']['goal_sensitive_bridges'],'usage_totals':r['analysis']['usage_totals'],
  'mean_reported_confidence':statistics.mean(confidence) if confidence else None,'numeric_reliability_count':sum(a['reliability'] is not None for a in answers),
  'max_probability_sum_deviation':max(sum_deltas,default=None),'max_native_score_expected_probability_deviation':max(score_deltas,default=None)}
 (out/'artifact-verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');return report

if __name__=='__main__':print(json.dumps(audit(Path(sys.argv[1])),indent=2))

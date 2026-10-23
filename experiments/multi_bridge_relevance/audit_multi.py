"""Offline reconstruction of requests, certificates, partial orders and scores."""
import base64,hashlib,json,math,statistics,sys,tempfile
from pathlib import Path
import benchmark_multi as b

def same(a,c):
 if isinstance(a,dict):return isinstance(c,dict) and a.keys()==c.keys() and all(same(a[k],c[k]) for k in a)
 if isinstance(a,list):return isinstance(c,list) and len(a)==len(c) and all(same(x,y) for x,y in zip(a,c))
 if type(a) is float:return type(c) in (float,int) and math.isclose(a,c,rel_tol=1e-12,abs_tol=1e-12)
 return type(a) is type(c) and a==c

def audit(out):
 r=json.loads((out/'results.json').read_text(encoding='utf-8'));assert r['weights']==b.WEIGHTS
 assert r['set_policy']=={'delta':b.DELTA,'min_useful':b.MIN_USEFUL,'sensitivity_deltas':list(b.SENSITIVITY_DELTAS)}
 answers=[];groups={};prob_delta=[];score_delta=[];contract_checks=0
 with tempfile.TemporaryDirectory() as temp:
  for call in r['calls']:
   payload=json.loads(json.dumps(call['model_input']));payload['assets']={}
   for asset in call['asset_audit']:
    data=(out/asset['file']).read_bytes();assert hashlib.sha256(data).hexdigest()==asset['sha256']
    payload['assets'][asset['asset']]={'type':'image','format':'png','data_base64':base64.b64encode(data).decode('ascii')}
   assert b.base.digest(payload)==call['request_sha256']
   expected,meta,audit=b.build_payload(Path(temp),call['replica'],call['goal'])
   assert same({k:v for k,v in expected.items() if k!='assets'},call['model_input']);assert set(expected['assets'])==set(payload['assets'])
   assert all(same(call[k],v) for k,v in meta.items())
   for method in b.METHODS:
    cert=b.certificate(b.objects_for(method,call['replica']));assert len(cert['generic_space_bindings'])==2;contract_checks+=2
   neutral=json.loads(json.dumps(call['model_input']));neutral['state'].pop('active_objective')
   groups.setdefault(call['replica'],[]).append((neutral,call['asset_audit']))
   if call.get('response'):
    assert set(call['response']['answers'])==set(payload['questions'])
    assert call['response']['returned_model'] in (None,payload['model'])
    for q,a in call['response']['answers'].items():
     assert a['type']=='score' and math.isfinite(a['score']) and 0<=a['score']<=3
     assert abs(a['normalized_score']-a['score']/3)<1e-12
     probs=a['probabilities'];assert set(probs)=={'0','1','2','3'} and all(0<=v<=1 for v in probs.values())
     prob_delta.append(abs(sum(probs.values())-1));assert prob_delta[-1]<.041
     score_delta.append(abs(a['score']-sum(int(k)*v for k,v in probs.items())));answers.append(a)
 assert b.analyze(r['calls'])==r['analysis']
 for group in groups.values():assert all(v==group[0] for v in group)
 confidence=[a['confidence'] for a in answers if a['confidence'] is not None]
 report={'run_id':r['run_id'],'source_commit':r['source_commit'],'status':r['status'],'audit_scope':'requests_and_native_results' if answers else 'prepared_inputs_only',
  'requests_reconstructed':len(r['calls']),'native_score_answers_verified':len(answers),'contract_checks':contract_checks,'objective_only_replicas':sum(len(g)==3 for g in groups.values()),
  'partial_order_groups_recomputed':r['analysis']['groups'],'exact_set_matches':r['analysis']['exact_set_matches'],
  'equivalent_pairs_in_band':r['analysis']['equivalent_pairs_in_band'],'equivalent_pairs_total':r['analysis']['equivalent_pairs_total'],
  'useful_equivalent_pairs_in_band':r['analysis']['useful_equivalent_pairs_in_band'],'useful_equivalent_pairs_total':r['analysis']['useful_equivalent_pairs_total'],
  'strict_preference_wins':r['analysis']['strict_preference_wins'],'strict_preference_total':r['analysis']['strict_preference_total'],
  'spurious_unique_sets':r['analysis']['spurious_unique_sets'],'set_matrix':r['analysis']['set_matrix'],'sensitivity':r['analysis']['sensitivity'],
  'usage_totals':r['analysis']['usage_totals'],'mean_reported_confidence':statistics.mean(confidence) if confidence else None,
  'numeric_reliability_count':sum(a['reliability'] is not None for a in answers),'max_probability_sum_deviation':max(prob_delta,default=None),
  'max_native_score_expected_probability_deviation':max(score_delta,default=None),
  'recorded_request_hashes_exact':True,'source_float_reconstruction_tolerance':{'relative':1e-12,'absolute':1e-12}}
 (out/'artifact-verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');return report

if __name__=='__main__':print(json.dumps(audit(Path(sys.argv[1])),indent=2))

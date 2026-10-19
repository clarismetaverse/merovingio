"""Audit saved matched requests, frozen image bytes and relevance projection."""
import base64,hashlib,json,math,statistics,sys,tempfile
from pathlib import Path
import benchmark_reduced as b
out=Path(sys.argv[1]);r=json.loads((out/'results.json').read_text(encoding='utf-8'))
def same(a,c):
 if isinstance(a,dict):return a.keys()==c.keys() and all(same(a[k],c[k]) for k in a)
 if isinstance(a,list):return len(a)==len(c) and all(same(x,y) for x,y in zip(a,c))
 if isinstance(a,float):return isinstance(c,(int,float)) and math.isclose(a,c,rel_tol=1e-12,abs_tol=1e-12)
 return a==c
pairs={};answers=[];deviations=[]
with tempfile.TemporaryDirectory() as temporary:
 for call in r['calls']:
  payload={**call['model_input'],'assets':{}}
  for asset in call['asset_audit']:
   data=(out/asset['file']).read_bytes();assert hashlib.sha256(data).hexdigest()==asset['sha256']
   payload['assets'][asset['asset']]={'type':'image','format':'png','data_base64':base64.b64encode(data).decode('ascii')}
  assert hashlib.sha256(json.dumps(payload,sort_keys=True).encode()).hexdigest()==call['request_sha256']
  generated,meta,audit,stats,historical,source=b.build_payload(Path(temporary),call['replica'],call['case'],call['condition'])
  assert payload==generated;assert meta==call['question_metadata'];assert stats==call['state_sizes'];assert historical==call['historical_answers'];assert source==call['prior_request_sha256']
  response=call.get('response',{}).get('answers',{})
  if 'response' in call:assert response.keys()==payload['questions'].keys()
  for q,a in response.items():
   assert a['choice'] in payload['questions'][q]['criteria'];assert a['probabilities'].keys()==payload['questions'][q]['criteria'].keys()
   delta=abs(sum(a['probabilities'].values())-1);assert delta<.041;deviations.append(delta);answers.append(a)
  pairs.setdefault((call['replica'],call['case']),{})[call['condition']]=call
assert same(b.analyze(r['calls']),r['analysis'])
complete_pairs=0
for pair in pairs.values():
 if set(pair)!=set(b.CONDITIONS):continue
 full=pair['full_state'];reduced=pair['relevant_state'];a=full['model_input'];c=reduced['model_input']
 assert a['questions']==c['questions'];assert full['asset_audit']==reduced['asset_audit']
 assert b.reduce_state(a['state'],a['questions'])==c['state'];complete_pairs+=1
summary={
 'source_commit':r['source_commit'],'run_id':r['run_id'],'status':r['status'],'request_hashes_verified':len(r['calls']),'native_answers_verified':len(answers),
 'matched_two_question_blocks_verified':complete_pairs,'offered_witness_validity_and_existing_bindings_preserved':True,
 'projection_is_raw_object_reference_closure':True,'native_statistics_recomputed':True,
 'max_native_probability_sum_deviation':max(deviations,default=None),'mean_reported_confidence':statistics.mean(a['confidence'] for a in answers if a['confidence'] is not None) if answers else None,
 'numeric_answer_reliability_count':sum(a['reliability'] is not None for a in answers),
 'by_condition':{},'paired_summary':r['analysis']['paired_summary']}
for condition in b.CONDITIONS:
 calls=[c for c in r['calls'] if c['condition']==condition]
 usage={key:sum(c['response']['usage'][key] for c in calls if c.get('response',{}).get('usage',{}).get(key) is not None) if any(c.get('response',{}).get('usage',{}).get(key) is not None for c in calls) else None for key in ('input_tokens','output_tokens','total_tokens')}
 summary['by_condition'][condition]={
  'usage_totals':usage,'mean_state_utf8_bytes':statistics.mean(c['state_sizes'][condition]['state_utf8_bytes'] for c in calls) if calls else None,
  'mean_input_tokens':statistics.mean(c['response']['usage']['input_tokens'] for c in calls if 'response' in c) if any('response' in c for c in calls) else None,
  'mean_elapsed_seconds':statistics.mean(c['elapsed_seconds'] for c in calls if 'elapsed_seconds' in c) if any('elapsed_seconds' in c for c in calls) else None,
  'overall':r['analysis']['by_condition'][condition]['overall'],
  'by_case':r['analysis']['by_condition'][condition]['by_case'],
  'identity_pairs_both_correct':sum(p['both_correct'] for p in r['analysis']['by_condition'][condition]['identity_counterfactual_pairs'])}
(out/'artifact-verification.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
print(json.dumps(summary,indent=2))

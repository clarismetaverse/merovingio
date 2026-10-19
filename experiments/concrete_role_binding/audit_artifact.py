"""Reconstruct saved requests and independently recheck every proposed witness."""
import base64,collections,hashlib,json,math,statistics,sys,tempfile
from pathlib import Path
import benchmark_binding as b

out=Path(sys.argv[1]);r=json.loads((out/'results.json').read_text(encoding='utf-8'))
def same(a,c):
 if isinstance(a,dict):return a.keys()==c.keys() and all(same(a[k],c[k]) for k in a)
 if isinstance(a,list):return len(a)==len(c) and all(same(x,y) for x,y in zip(a,c))
 if isinstance(a,float):return isinstance(c,(int,float)) and math.isclose(a,c,rel_tol=1e-12,abs_tol=1e-12)
 return a==c
answers=[];deviations=[];identity_checks=0
with tempfile.TemporaryDirectory() as temporary:
 for call in r['calls']:
  payload={**call['model_input'],'assets':{}}
  for asset in call['asset_audit']:
   data=(out/asset['file']).read_bytes();assert hashlib.sha256(data).hexdigest()==asset['sha256']
   payload['assets'][asset['asset']]={'type':'image','format':'png','data_base64':base64.b64encode(data).decode('ascii')}
  assert hashlib.sha256(json.dumps(payload,sort_keys=True).encode()).hexdigest()==call['request_sha256']
  generated,meta,_=b.build_payload(Path(temporary),call['replica'])
  assert {k:v for k,v in generated.items() if k!='assets'}==call['model_input']
  assert meta==call['question_metadata'];assert len(payload['questions'])==12
  shared=next(m for m in meta.values() if m['case']=='shared')
  altered=next(m for m in meta.values() if m['case']=='distinct_coincident')
  states=payload['state']['snapshots'];x=states[shared['snapshot']];y=states[altered['snapshot']]
  assert x['image']==y['image'];changed=[]
  for object_id in x['objects']:
   if x['objects'][object_id]!=y['objects'][object_id]:changed.append(object_id)
  assert changed==[shared['aliases']['R']]
  repaired=json.loads(json.dumps(y['objects']));repaired[shared['aliases']['R']]['boundary_uses'][-1]['carrier']=shared['aliases']['S']
  assert repaired==x['objects'];identity_checks+=1
  response=call.get('response',{}).get('answers',{})
  if 'response' in call:assert response.keys()==payload['questions'].keys()
  for q,a in response.items():
   assert a['choice'] in payload['questions'][q]['criteria'];assert set(a['probabilities'])==set(payload['questions'][q]['criteria'])
   delta=abs(sum(a['probabilities'].values())-1);assert delta<.041;deviations.append(delta);answers.append(a)
   m=meta[q];objects=states[m['snapshot']]['objects']
   for label,witness in m['option_witnesses'].items():assert b.check_witness(objects,witness,m['schema'],m['query_scope_host'])==m['option_failures'][label]
assert same(b.analyze(r['calls']),r['analysis'])
rows=r['analysis']['observations'];error_reasons=collections.Counter(reason for row in rows for reason in row['selected_invalid_reasons'])
usage={key:sum(c['response']['usage'][key] for c in r['calls'] if c.get('response',{}).get('usage',{}).get(key) is not None) if any(c.get('response',{}).get('usage',{}).get(key) is not None for c in r['calls']) else None for key in ('input_tokens','output_tokens','total_tokens')}
summary={'run_id':r['run_id'],'source_commit':r['source_commit'],'status':r['status'],
 'request_hashes_verified':len(r['calls']),'native_answers_verified':len(answers),'single_field_pixel_identical_identity_pairs_verified':identity_checks,
 'all_offered_witnesses_rechecked':sum(len(m['option_witnesses']) for c in r['calls'] for m in c['question_metadata'].values()),
 'statistics_recomputed':True,'usage_totals':usage,'mean_reported_confidence':statistics.mean(a['confidence'] for a in answers if a['confidence'] is not None) if answers else None,
 'numeric_answer_reliability_count':sum(a['reliability'] is not None for a in answers),'max_native_probability_sum_deviation':max(deviations,default=None),
 'always_none_baseline_correct':sum(not row['listed_binding_exists'] for row in rows),'selected_invalid_witness_reasons':dict(error_reasons),
 'identity_pairs_both_correct':sum(p['both_correct'] for p in r['analysis']['identity_counterfactual_pairs']),
 'identity_pairs_n':len(r['analysis']['identity_counterfactual_pairs']),
 'overall':r['analysis']['overall'],'by_case':r['analysis']['by_case'],'by_schema':r['analysis']['by_schema']}
(out/'artifact-verification.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
print(json.dumps(summary,indent=2))

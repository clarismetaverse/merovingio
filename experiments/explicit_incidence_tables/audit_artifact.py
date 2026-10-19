"""Reconstruct actual requests and verify lossless tables without calling Jev."""
import base64,hashlib,json,math,statistics,sys,tempfile
from pathlib import Path
import benchmark_tables as b
out=Path(sys.argv[1]);r=json.loads((out/'results.json').read_text(encoding='utf-8'))
def same(a,c):
 if isinstance(a,dict):return a.keys()==c.keys() and all(same(a[k],c[k]) for k in a)
 if isinstance(a,list):return len(a)==len(c) and all(same(x,y) for x,y in zip(a,c))
 if isinstance(a,float):return isinstance(c,(int,float)) and math.isclose(a,c,rel_tol=1e-12,abs_tol=1e-12)
 return a==c
pairs={};answers=[];deltas=[];witnesses=0;roundtrips=0
with tempfile.TemporaryDirectory() as temporary:
 for call in r['calls']:
  p=dict(call['model_input'])
  if call['asset_audit']:
   p['assets']={}
   for asset in call['asset_audit']:
    data=(out/asset['file']).read_bytes();assert hashlib.sha256(data).hexdigest()==asset['sha256']
    p['assets'][asset['asset']]={'type':'image','format':'png','data_base64':base64.b64encode(data).decode('ascii')}
  assert hashlib.sha256(json.dumps(p,sort_keys=True).encode()).hexdigest()==call['request_sha256']
  if call['kind']=='id_control':
   generated,meta=b.build_id_control(call['replica']);assert p==generated and meta==call['question_metadata']
  else:
   generated,meta,audit,stats,old,prior_hash=b.build_payload(Path(temporary),call['replica'],call['case'],call['condition'])
   assert p==generated and meta==call['question_metadata'] and old==call['historical_answers']
   assert prior_hash==call['prior_request_sha256'];assert stats==call['state_sizes']
   state=b.graph_state(p['state'])
   if call['condition']=='incidence_tables':roundtrips+=1
   for m in meta.values():
    objects=state['snapshots'][m['snapshot']]['objects']
    for label,w in m['option_witnesses'].items():
     assert b.previous.source.check_witness(objects,w,m['schema'],m['query_scope_host'])==m['option_failures'][label];witnesses+=1
    assert b.previous.source.all_bindings(objects,m['schema'],m['query_scope_host'])==m['all_graph_bindings']
   pairs.setdefault((call['replica'],call['case']),{})[call['condition']]=call
  native=call.get('response',{}).get('answers',{})
  if 'response' in call:assert native.keys()==p['questions'].keys()
  for q,a in native.items():
   assert a['choice'] in p['questions'][q]['criteria'];assert a['probabilities'].keys()==p['questions'][q]['criteria'].keys()
   delta=abs(sum(a['probabilities'].values())-1);assert delta<.041;deltas.append(delta);answers.append(a)
assert same(b.analyze(r['calls']),r['analysis'])
complete=0
for pair in pairs.values():
 if set(pair)!=set(b.CONDITIONS):continue
 graph=pair['graph'];table=pair['incidence_tables']
 assert graph['model_input']['questions']==table['model_input']['questions'];assert graph['asset_audit']==table['asset_audit']
 assert b.graph_state(table['model_input']['state'])==graph['model_input']['state'];complete+=1
report={'source_commit':r['source_commit'],'run_id':r['run_id'],'status':r['status'],'audit_scope':'api_results_and_requests' if answers else 'prepared_inputs_only_no_api_results','api_calls_actually_attempted':r['analysis']['api_calls_attempted'],'request_hashes_verified':len(r['calls']),'native_answers_verified':len(answers),'paired_blocks_verified':complete,'table_roundtrips_verified':roundtrips,'candidate_witnesses_rechecked':witnesses,
 'max_native_probability_sum_deviation':max(deltas,default=None),'mean_reported_confidence':statistics.mean(a['confidence'] for a in answers if a['confidence'] is not None) if answers else None,'numeric_answer_reliability_count':sum(a['reliability'] is not None for a in answers),'paired_summary':r['analysis']['paired_summary'],'literal_id_controls':r['analysis']['literal_id_controls'],'by_condition':{}}
for kind in (*b.CONDITIONS,'id_control'):
 calls=[c for c in r['calls'] if c['kind']=='id_control'] if kind=='id_control' else [c for c in r['calls'] if c['kind']=='binding' and c['condition']==kind]
 usage={key:sum(c['response']['usage'][key] for c in calls if c.get('response',{}).get('usage',{}).get(key) is not None) if any(c.get('response',{}).get('usage',{}).get(key) is not None for c in calls) else None for key in ('input_tokens','output_tokens','total_tokens')}
 entry={'usage_totals':usage,'mean_elapsed_seconds':statistics.mean(c['elapsed_seconds'] for c in calls if 'elapsed_seconds' in c) if any('elapsed_seconds' in c for c in calls) else None}
 if kind!='id_control':entry.update(overall=r['analysis']['by_condition'][kind]['overall'],by_case=r['analysis']['by_condition'][kind]['by_case'],identity_pairs_both_correct=sum(p['both_correct'] for p in r['analysis']['by_condition'][kind]['identity_counterfactual_pairs']))
 report['by_condition'][kind]=entry
(out/'artifact-verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2))

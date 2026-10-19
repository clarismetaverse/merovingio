"""Independent artifact reconstruction and matched-intervention checks, no API."""
import base64,hashlib,json,math,statistics,sys,tempfile
from html.parser import HTMLParser
from pathlib import Path
out=Path(sys.argv[1]);repo=Path(sys.argv[2])
sys.path.insert(0,str(repo/'experiments/generic_binding_ablation'))
import benchmark_ablation as b
r=json.loads((out/'results.json').read_text(encoding='utf-8'))
def same(a,c):
 if isinstance(a,dict):return a.keys()==c.keys() and all(same(a[k],c[k]) for k in a)
 if isinstance(a,list):return len(a)==len(c) and all(same(x,y) for x,y in zip(a,c))
 if isinstance(a,float):return isinstance(c,(int,float)) and math.isclose(a,c,rel_tol=1e-12,abs_tol=1e-12)
 return a==c
native=[];pairs={};probability_deviations=[]
with tempfile.TemporaryDirectory() as folder:
 for call in r['calls']:
  p={**call['model_input'],'assets':{}}
  for asset in call['asset_audit']:
   data=(out/asset['file']).read_bytes()
   assert hashlib.sha256(data).hexdigest()==asset['sha256']
   p['assets'][asset['asset']]={'type':'image','format':'png','data_base64':base64.b64encode(data).decode('ascii')}
  assert hashlib.sha256(json.dumps(p,sort_keys=True).encode()).hexdigest()==call['request_sha256']
  generated,mapping,meta,audit,source=b.build_payload(Path(folder),call['shape'],call['repeat'],call['condition'])
  assert p==generated and call['question_metadata']==meta
  assert source==call['prior_full_request_sha256']
  assert len(p['questions'])==20
  answers=call.get('response',{}).get('answers',{})
  if 'response' in call:assert answers.keys()==p['questions'].keys()
  for q,a in answers.items():
   assert abs(sum(a['probabilities'].values())-1)<.031
   probability_deviations.append(abs(sum(a['probabilities'].values())-1))
   if a['type']=='score':assert math.isclose(a['normalized_score'],a['score']/3)
   else:assert a['choice'] in p['questions'][q]['criteria']
   native.append(a)
  pairs.setdefault((call['shape'],call['repeat']),{})[call['condition']]=call
assert same(b.analyze(r['calls']),r['analysis'])
for pair in pairs.values():
 assert set(pair)==set(b.CONDITIONS)
 assert pair['compact_generic']['model_input']['state']==pair['compact_concrete']['model_input']['state']
 assert pair['explicit_generic']['model_input']['state']==pair['explicit_concrete']['model_input']['state']
 assert len({json.dumps(c['asset_audit'],sort_keys=True) for c in pair.values()})==1
usage={key:sum(c['response']['usage'][key] for c in r['calls'] if c.get('response',{}).get('usage',{}).get(key) is not None) if any(c.get('response',{}).get('usage',{}).get(key) is not None for c in r['calls']) else None for key in ('input_tokens','output_tokens','total_tokens')}
observed=r['analysis']['observations'];disagreements={}
for cond in b.CONDITIONS:
 selected=[v for v in observed if v['condition']==cond]
 scores={(v['shape'],v['repeat'],v['candidate'],v['schema']):v for v in selected if v['primitive']=='score'}
 choices={(v['shape'],v['repeat'],v['candidate'],v['schema']):v for v in selected if v['primitive']=='choice'}
 keys=scores.keys()&choices.keys()
 disagreements[cond]={'paired_n':len(keys),'threshold_vs_choice':sum(scores[k]['predicted_binding']!=choices[k]['predicted_binding'] for k in keys),'modal_vs_choice':sum(scores[k]['modal_binding']!=choices[k]['predicted_binding'] for k in keys)}
report={
 'source_commit':r['source_commit'],'run_id':r['run_id'],'status':r['status'],
 'request_hashes_verified':len(r['calls']),'native_answers_verified':len(native),'original_source_requests_reconstructed':len(pairs),
 'description_rubric_and_asset_invariants_verified':True,'condition_statistics_recomputed':True,
 'usage_totals':usage,'max_native_probability_sum_deviation':max(probability_deviations,default=None),
 'native_rounding_policy':'Preserve server scores and rounded probabilities without renormalization.',
 'mean_reported_confidence':statistics.mean(a['confidence'] for a in native if a['confidence'] is not None) if native else None,
 'numeric_answer_reliability_count':sum(a['reliability'] is not None for a in native),
 'primitive_disagreements':disagreements,
 'by_condition':r['analysis']['by_condition'],'paired_score_effects':r['analysis']['paired_score_effects'],
 'fixed_threshold_sensitivity':r['analysis']['fixed_threshold_sensitivity'],
}
(out/'artifact-verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in ('by_condition','fixed_threshold_sensitivity')},indent=2))

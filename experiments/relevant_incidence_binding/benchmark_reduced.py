"""Matched full versus relevance-pruned state; identical witness questions and IDs."""
from __future__ import annotations
import argparse,base64,copy,hashlib,html,json,os,random,sys,time
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'experiments/concrete_role_binding'))
import benchmark_binding as source

SOURCE_PATH=ROOT/'experiments/concrete_role_binding/live_results.json'
PRIOR=json.loads(SOURCE_PATH.read_text(encoding='utf-8'))
REPLICAS=(0,3)
CONDITIONS=('full_state','relevant_state')
SEED=20261025
LIMITS=[
 'Two previously used replicas (0 and 3), all six near-counterexample cases and both schemas. Two questions per call, 24 calls, 48 total answers.',
 'The new full-state baseline also has two questions per call and the common image manifest. Compare historical responses descriptively; batch, run and manifest effects are not separately isolated.',
 'Only state is pruned. Contracts, object IDs, retained records, instructions, option labels/order and all original image assets are identical within every matched pair.',
 'The reduced state keeps one queried snapshot and the transitive object-reference closure of EVERY offered witness, not just the correct one. Every boundary-use record is preserved.',
 'Coordinates and polygon cycles remain because adjacency, containment and full host coverage cannot be checked from material incidences alone.',
 'No new geometry, equality table, binding validity flag, candidate-specific explanation, or oracle result is supplied to the model.',
 'The intervention removes both unqueried snapshots and unused objects. It does not separately identify their contributions or remove the unchanged image context.',
 'A null or partial effect in this pruning experiment cannot rule out all context effects or establish a general inability to bind IDs.',
 'Native answers are reported before deterministic rejection. This selects finite witnesses from supplied structural evidence, not free-form discovery, proof or autonomous visual extraction.',
 'Only Actions may call Jev with the repository secret and required images header. No native Score questions, retries or long-context header. Multiple images do not imply internal sequential reasoning.'
]

def prior_call(replica):return next(c for c in PRIOR['calls'] if c['replica']==replica)
def references(value,objects):
 if isinstance(value,dict):return set().union(*(references(v,objects) for v in value.values())) if value else set()
 if isinstance(value,list):return set().union(*(references(v,objects) for v in value)) if value else set()
 return {value} if isinstance(value,str) and value in objects else set()

def reduce_state(state,questions):
 snapshots={q['instructions']['snapshot_ref'] for q in questions.values()};assert len(snapshots)==1
 snapshot=next(iter(snapshots));objects=state['snapshots'][snapshot]['objects']
 keep=references(questions,objects)
 while True:
  expanded=keep|set().union(*(references(objects[k],objects) for k in keep))
  if expanded==keep:break
  keep=expanded
 result=copy.deepcopy(state)
 result['snapshots']={snapshot:{**copy.deepcopy(state['snapshots'][snapshot]),'objects':{k:copy.deepcopy(v) for k,v in objects.items() if k in keep}}}
 return result

def build_payload(out,replica,case,condition):
 if replica not in REPLICAS or condition not in CONDITIONS:raise ValueError('unknown_cell')
 old=prior_call(replica);p=copy.deepcopy(old['model_input']);p['assets']={}
 for a in old['asset_audit']:
  data=(Path(__file__).parent/'fixtures'/a['file']).read_bytes();assert hashlib.sha256(data).hexdigest()==a['sha256']
  path=out/a['file'];path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
  p['assets'][a['asset']]={'type':'image','format':'png','data_base64':base64.b64encode(data).decode('ascii')}
 assert hashlib.sha256(json.dumps(p,sort_keys=True).encode()).hexdigest()==old['request_sha256']
 # Preserve explicit references to the unchanged image context after snapshot pruning.
 # This identical manifest is added to BOTH conditions, before the state intervention.
 p['state']['image_asset_manifest']=list(p['assets'])
 keys={q for q,m in old['question_metadata'].items() if m['case']==case}
 p['questions']={q:v for q,v in p['questions'].items() if q in keys};assert len(p['questions'])==2
 meta={q:copy.deepcopy(old['question_metadata'][q]) for q in p['questions']}
 full_state=copy.deepcopy(p['state']);reduced=reduce_state(full_state,p['questions'])
 for m in meta.values():
  objects=reduced['snapshots'][m['snapshot']]['objects']
  for label,w in m['option_witnesses'].items():assert source.check_witness(objects,w,m['schema'],m['query_scope_host'])==m['option_failures'][label]
  assert source.all_bindings(objects,m['schema'],m['query_scope_host'])==m['all_graph_bindings']
 if condition=='relevant_state':p['state']=reduced
 stats={name:{'snapshots':len(state['snapshots']),'objects':sum(len(s['objects']) for s in state['snapshots'].values()),'state_utf8_bytes':len(json.dumps(state,sort_keys=True).encode())} for name,state in (('full_state',full_state),('relevant_state',reduced))}
 historical={q:old['response']['answers'][q] for q in p['questions']}
 return p,meta,old['asset_audit'],stats,historical,old['request_sha256']

def analyze(calls):
 groups={cond:source.analyze([c for c in calls if c['condition']==cond]) for cond in CONDITIONS}
 old_rows={};current={};paired=[]
 for c in calls:
  for q,m in c['question_metadata'].items():
   key=(c['replica'],c['case'],m['schema'])
   historical=c['historical_answers'][q];old_rows[key]=historical['choice']==m['expected_choice']
   answer=c.get('response',{}).get('answers',{}).get(q)
   if answer:current.setdefault(key,{})[c['condition']]={'correct':answer['choice']==m['expected_choice'],'choice':answer['choice'],'expected_choice':m['expected_choice']}
 for key,pair in current.items():
  if set(pair)!=set(CONDITIONS):continue
  paired.append({'replica':key[0],'case':key[1],'schema':key[2],**pair,'historical_correct':old_rows[key]})
 return {'api_calls_attempted':sum('response' in c or 'failure' in c for c in calls),'api_failures':sum('failure' in c for c in calls),'native_answers':sum(g['native_answers'] for g in groups.values()),'by_condition':groups,
         'paired_summary':{'n':len(paired),'both_correct':sum(p['full_state']['correct'] and p['relevant_state']['correct'] for p in paired),'reduced_only_correct':sum(not p['full_state']['correct'] and p['relevant_state']['correct'] for p in paired),'full_only_correct':sum(p['full_state']['correct'] and not p['relevant_state']['correct'] for p in paired),'both_wrong':sum(not p['full_state']['correct'] and not p['relevant_state']['correct'] for p in paired),'fresh_full_vs_historical_choice_changes':sum(p['full_state']['choice']!=prior_call(p['replica'])['response']['answers'][next(q for q,m in prior_call(p['replica'])['question_metadata'].items() if m['case']==p['case'] and m['schema']==p['schema'])]['choice'] for p in paired),'historical_correct':sum(p['historical_correct'] for p in paired)},'matched_observations':paired}

def viewer(out,report):
 e=html.escape;a=report['analysis'];body='<!doctype html><html lang="it"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Binding state completo e incidenze rilevanti</title><style>body{font:16px system-ui;max-width:1200px;margin:2rem auto;padding:1rem;color:#26313d}table{border-collapse:collapse;width:100%;margin:1rem 0}td,th{border:1px solid #ccd;padding:.5rem}pre{white-space:pre-wrap;overflow-wrap:anywhere}details{margin:1rem 0}img{width:230px}</style><h1>Binding degli ID con contesto ridotto</h1><p>Stato: '+e(report['status'])+'. 48 domande totali, due per chiamata. Ogni coppia mantiene domande, contratti, ID, opzioni e immagini identici. Lo state ridotto è la chiusura dei riferimenti di tutte le opzioni, senza risultati del verificatore.</p><table><tr><th>Condizione</th><th>Esatte</th><th>Witness positivi</th><th>None negativi</th></tr>'
 for cond,g in a['by_condition'].items():
  v=g['overall'];body+='<tr><td>'+('State completo' if cond=='full_state' else 'Sole incidenze rilevanti')+'</td><td>'+str(v['correct'])+'/'+str(v['n'])+'</td><td>'+str(v['positive_witnesses_correct'])+'/'+str(v['positive_n'])+'</td><td>'+str(v['negative_none_correct'])+'/'+str(v['negative_n'])+'</td></tr>'
 body+='</table><table><tr><th>Caso</th><th>State completo</th><th>State ridotto</th></tr>'
 labels={'shared':'Caso base','distinct_coincident':'Carrier coincidenti con identità distinte','partial_use':'Uso parziale del carrier','triangle_quadrilateral':'Triangolo e quadrilatero','wrong_host':'Figura ospite diversa','omitted_valid':'Witness valido escluso dalle opzioni'}
 for case in source.CASES:
  body+='<tr><td>'+labels[case]+'</td>'
  for cond in CONDITIONS:
   v=a['by_condition'][cond]['by_case'][case];body+='<td>'+str(v['correct'])+'/'+str(v['n'])+'</td>'
  body+='</tr>'
 body+='</table><p>Il controllo completo è ripetuto con due domande per call, per distinguere la riduzione dello state dal cambio di batch rispetto al precedente esperimento. Sempre none varrebbe 16/24 per condizione.</p>'
 for title,value in [('Confronti appaiati e baseline storica',a['paired_summary']),('Risposte appaiate',a['matched_observations']),('Matrici e witness per condizione',a['by_condition']),('Limiti',report['limits']),('Input e risposte sanitizzate',report['calls'])]:body+='<details><summary>'+title+'</summary><pre>'+e(json.dumps(value,indent=2,ensure_ascii=False))+'</pre></details>'
 shown=set()
 for c in report['calls']:
  if c['replica'] in shown:continue
  shown.add(c['replica']);body+='<h2>Replica '+str(c['replica'])+'</h2>'+''.join('<img src="'+x['file']+'">' for x in c['asset_audit'])
 body+='<p><a href="VERIFIED_RESULTS.md">Interpretazione e audit verificato</a></p></html>';(out/'viewer.html').write_text(body,encoding='utf-8')

def save(out,report):
 report['analysis']=analyze(report['calls']);temp=out/'results.tmp';temp.write_text(json.dumps(report,indent=2),encoding='utf-8');temp.replace(out/'results.json');viewer(out,report)

def transport(payload):
 if os.getenv('GITHUB_ACTIONS')!='true' or not os.getenv('TYPESAFE_API_KEY'):raise RuntimeError('actions_secret_required')
 import requests
 start=time.perf_counter()
 try:
  response=requests.post('https://api.typesafe.ai/v1/systemone',headers={'Authorization':'Bearer '+os.environ['TYPESAFE_API_KEY'],'TypeSafe-Danger-Zone-Images':'true'},json=payload,timeout=180)
  if response.status_code==200:result={'response':source.previous.sanitize(response.json(),payload['questions'])}
  else:
   body=response.text.lower()
   result={'failure':'HTTP_'+str(response.status_code),'validation_flags':{key:key in body for key in ('asset','unused','unreferenced','reference','state','image','token','context','invalid','missing','schema','limit','65536','32768')}}
 except Exception:result={'failure':'transport_or_typed_schema_failure'}
 result['elapsed_seconds']=time.perf_counter()-start
 return result

def diagnose(out):
 if os.getenv('GITHUB_ACTIONS')!='true' or not os.getenv('TYPESAFE_API_KEY'):raise SystemExit('Actions and repository secret required')
 out.mkdir(parents=True,exist_ok=True)
 pairs=[(replica,case) for replica in REPLICAS for case in source.CASES];random.Random(SEED).shuffle(pairs)
 payload,*_=build_payload(out,*pairs[0],'relevant_state');result=transport(payload)
 (out/'diagnostic.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
 print(json.dumps({key:value for key,value in result.items() if key!='response'}),flush=True)

def main(out,live=False):
 if live and (os.getenv('GITHUB_ACTIONS')!='true' or not os.getenv('TYPESAFE_API_KEY')):raise SystemExit('Actions and repository secret required')
 out.mkdir(parents=True,exist_ok=True)
 for name in ('PROTOCOL.md','VERIFIED_RESULTS.md'):
  path=Path(__file__).parent/name
  if path.exists():(out/name).write_text(path.read_text(encoding='utf-8'),encoding='utf-8')
 report={'experiment':'Relevant incidence subgraph versus full state v1','model':'jev-1.14.0','status':'running' if live else 'offline_only','source_commit':os.getenv('GITHUB_SHA'),'run_id':os.getenv('GITHUB_RUN_ID'),'prior_run_id':PRIOR['run_id'],'prior_canonical_json_sha256':hashlib.sha256(json.dumps(PRIOR,sort_keys=True).encode()).hexdigest(),'replicas':REPLICAS,'conditions':CONDITIONS,'limits':LIMITS,'calls':[]}
 pairs=[(replica,case) for replica in REPLICAS for case in source.CASES];random.Random(SEED).shuffle(pairs)
 for index,(replica,case) in enumerate(pairs):
  for condition in CONDITIONS if index%2==0 else tuple(reversed(CONDITIONS)):
   p,meta,audit,stats,old,prior_hash=build_payload(out,replica,case,condition)
   record={'replica':replica,'case':case,'condition':condition,'question_count':2,'question_metadata':meta,'asset_audit':audit,'state_sizes':stats,'historical_answers':old,'prior_request_sha256':prior_hash,'model_input':{k:v for k,v in p.items() if k!='assets'},'request_sha256':hashlib.sha256(json.dumps(p,sort_keys=True).encode()).hexdigest(),'body_bytes':len(json.dumps(p).encode())}
   if live:record.update(transport(p))
   report['calls'].append(record);save(out,report);print('Recorded',len(report['calls']),'/ 24',condition,flush=True)
   if record.get('failure') in ('HTTP_400','HTTP_401','HTTP_403'):
    report['status']='request_rejected';save(out,report);raise SystemExit('Stopped after request rejection; sanitized artifact saved')
 report['status']='completed_with_failures' if any('failure' in c for c in report['calls']) else 'completed' if live else 'offline_only';save(out,report)
 if report['status']=='completed_with_failures':raise SystemExit('Sanitized failures recorded')

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,default=Path('output_relevant_incidence'));ap.add_argument('--live',action='store_true');ap.add_argument('--diagnose',action='store_true');args=ap.parse_args();diagnose(args.out) if args.diagnose else main(args.out,args.live)

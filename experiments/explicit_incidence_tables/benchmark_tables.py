"""Lossless incidence tables versus the same pruned graph, plus literal-ID controls."""
from __future__ import annotations
import argparse,base64,copy,hashlib,html,json,os,random,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'experiments/relevant_incidence_binding'))
import benchmark_reduced as previous
SOURCE_PATH=ROOT/'experiments/relevant_incidence_binding/live_results.json'
PRIOR=json.loads(SOURCE_PATH.read_text(encoding='utf-8'))
CONDITIONS=('graph','incidence_tables')
REPLICAS=(0,3)
SEED=20261026
LIMITS=[
 'Same two replicas, six cases and two contracts as the previous relevant-state experiment. 48 witness judgments plus four literal-ID controls, 52 total answers in 26 two-question calls.',
 'Graph baseline is exactly the archived relevant-state request, including image bytes, ID strings, contracts, options and question order. It is rerun to measure historical drift.',
 'The table state replaces the object dictionary with four typed tables: points, carriers, polygons and boundary uses. Decode must reconstruct every original object and use exactly.',
 'Tables contain raw fields only. No same-ID flags, complete-side flags, precomputed containment, area, validity, gold assignment or missing-premise diagnosis is shown.',
 'Grouping records by table is part of the formatting intervention. Layout, token length and grouping effects are not separately isolated.',
 'Literal-ID probes run separately, with explicit operand strings and no graph or images. They do not reveal their operands or answers inside any witness request.',
 'Passing literal-ID controls does not establish correct graph lookup or integration of all contract constraints. A tiny control set does not show general ID-comparison ability.',
 'The images remain unchanged in both main conditions. A null table effect cannot exclude all representation, visual-context or attention effects.',
 'This selects finite witnesses on supplied structural evidence, not free generation, autonomous visual extraction, theorem proof or internal sequential reasoning.',
 'Native choices are scored before any deterministic rejection. Only Actions may call Jev with the repository secret and required images header. No native Score, retries or long context.'
]

def prior_call(replica,case):
 return next(c for c in PRIOR['calls'] if c['replica']==replica and c['case']==case and c['condition']=='relevant_state')

def encode_objects(objects):
 tables={
  'points':{'columns':['object_id','x','y'],'rows':[]},
  'carriers':{'columns':['object_id','endpoint_0','endpoint_1'],'rows':[]},
  'polygons':{'columns':['object_id','object_type','ordered_vertex_ids'],'rows':[]},
  'boundary_uses':{'columns':['region_id','use_index','carrier_id','use_endpoint_0','use_endpoint_1'],'rows':[]}}
 for key,value in objects.items():
  kind=value['type']
  if kind=='point':
   assert set(value)=={'type','xy'};tables['points']['rows'].append([key,*value['xy']])
  elif kind=='segment':
   assert set(value)=={'type','endpoints'};tables['carriers']['rows'].append([key,*value['endpoints']])
  elif kind in ('region','host'):
   assert set(value)==({'type','vertices','boundary_uses'} if kind=='region' else {'type','vertices'})
   tables['polygons']['rows'].append([key,kind,copy.deepcopy(value['vertices'])])
   for index,use in enumerate(value.get('boundary_uses',[])):
    assert set(use)=={'carrier','endpoints'}
    tables['boundary_uses']['rows'].append([key,index,use['carrier'],*use['endpoints']])
  else:raise ValueError('unknown_object_type')
 return tables

def decode_tables(tables):
 objects={}
 for key,x,y in tables['points']['rows']:objects[key]={'type':'point','xy':[x,y]}
 for key,a,b in tables['carriers']['rows']:objects[key]={'type':'segment','endpoints':[a,b]}
 for key,kind,vertices in tables['polygons']['rows']:
  objects[key]={'type':kind,'vertices':copy.deepcopy(vertices)}
  if kind=='region':objects[key]['boundary_uses']=[]
 for key,index,carrier,a,b in tables['boundary_uses']['rows']:
  assert len(objects[key]['boundary_uses'])==index
  objects[key]['boundary_uses'].append({'carrier':carrier,'endpoints':[a,b]})
 return objects

def table_state(state):
 result=copy.deepcopy(state)
 for snapshot in result['snapshots'].values():
  objects=snapshot.pop('objects');snapshot['tables']=encode_objects(objects)
  assert decode_tables(snapshot['tables'])==objects
 return result

def graph_state(state):
 result=copy.deepcopy(state)
 for snapshot in result['snapshots'].values():
  if 'tables' in snapshot:snapshot['objects']=decode_tables(snapshot.pop('tables'))
 return result

def build_payload(out,replica,case,condition):
 if condition not in CONDITIONS or replica not in REPLICAS:raise ValueError('unknown_cell')
 old=prior_call(replica,case);payload=copy.deepcopy(old['model_input']);payload['assets']={}
 for asset in old['asset_audit']:
  data=(ROOT/'experiments/relevant_incidence_binding/fixtures'/asset['file']).read_bytes()
  assert hashlib.sha256(data).hexdigest()==asset['sha256']
  path=out/asset['file'];path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
  payload['assets'][asset['asset']]={'type':'image','format':'png','data_base64':base64.b64encode(data).decode('ascii')}
 assert hashlib.sha256(json.dumps(payload,sort_keys=True).encode()).hexdigest()==old['request_sha256']
 original=copy.deepcopy(payload['state'])
 if condition=='incidence_tables':payload['state']=table_state(original)
 assert graph_state(payload['state'])==original
 stats={'graph_state_bytes':len(json.dumps(original,sort_keys=True).encode()),'table_state_bytes':len(json.dumps(table_state(original),sort_keys=True).encode())}
 meta=copy.deepcopy(old['question_metadata'])
 for m in meta.values():
  objects=graph_state(payload['state'])['snapshots'][m['snapshot']]['objects']
  for label,w in m['option_witnesses'].items():assert previous.source.check_witness(objects,w,m['schema'],m['query_scope_host'])==m['option_failures'][label]
 return payload,meta,old['asset_audit'],stats,old['response']['answers'],old['request_sha256']

def build_id_control(replica):
 old=prior_call(replica,'shared');aliases=next(iter(old['question_metadata'].values()))['aliases']
 rng=random.Random(SEED+100+replica);refs=['P'+str(v) for v in rng.sample(range(100,999),2)]
 state={'comparisons':{refs[0]:{'left_id':aliases['S'],'right_id':aliases['S']},refs[1]:{'left_id':aliases['S'],'right_id':aliases['T']}}}
 questions={};meta={}
 for index,ref in enumerate(refs):
  labels=['K'+str(v) for v in rng.sample(range(100,999),2)];meanings=dict(zip(labels,('equal','distinct')));order=list(labels);rng.shuffle(order)
  criteria={label:('The two supplied identifier strings are exactly identical.' if meanings[label]=='equal' else 'The two supplied identifier strings are distinct.') for label in order}
  criteria['none']='The shown data is insufficient to compare the identifier strings.'
  q='D'+str(index+1).zfill(3);pair=state['comparisons'][ref]
  questions[q]={'type':'choice','instructions':{'comparison_ref':ref,'task':'Compare the two literal identifier strings in the referenced comparison. Judge exact string identity using only these operands.'},'criteria':criteria}
  expected='equal' if pair['left_id']==pair['right_id'] else 'distinct'
  meta[q]={'expected_choice':next(k for k,v in meanings.items() if v==expected),'expected_relation':expected,'option_meanings':meanings,'operands':pair}
 return {'model':'jev-1.14.0','state':state,'questions':questions},meta

def analyze(calls):
 binding=[c for c in calls if c['kind']=='binding'];groups={condition:previous.source.analyze([c for c in binding if c['condition']==condition]) for condition in CONDITIONS}
 paired={};control_rows=[]
 for c in calls:
  for q,answer in c.get('response',{}).get('answers',{}).items():
   m=c['question_metadata'][q]
   if c['kind']=='id_control':
    control_rows.append({'replica':c['replica'],'question':q,'expected_relation':m['expected_relation'],'predicted_relation':m['option_meanings'].get(answer['choice'],'none'),'correct':answer['choice']==m['expected_choice'],'confidence':answer['confidence']});continue
   key=(c['replica'],c['case'],m['schema'])
   paired.setdefault(key,{})[c['condition']]={'choice':answer['choice'],'correct':answer['choice']==m['expected_choice']}
 matched=[]
 for key,pair in paired.items():
  if set(pair)!=set(CONDITIONS):continue
  old=prior_call(key[0],key[1]);q=next(q for q,m in old['question_metadata'].items() if m['schema']==key[2]);expected=old['question_metadata'][q]['expected_choice'];historical=old['response']['answers'][q]['choice']
  matched.append({'replica':key[0],'case':key[1],'schema':key[2],**pair,'historical_choice':historical,'historical_correct':historical==expected})
 return {'api_calls_attempted':sum('response' in c or 'failure' in c for c in calls),'api_failures':sum('failure' in c for c in calls),'native_answers':sum(g['native_answers'] for g in groups.values())+len(control_rows),'by_condition':groups,
  'paired_summary':{'n':len(matched),'both_correct':sum(p['graph']['correct'] and p['incidence_tables']['correct'] for p in matched),'table_only_correct':sum(not p['graph']['correct'] and p['incidence_tables']['correct'] for p in matched),'graph_only_correct':sum(p['graph']['correct'] and not p['incidence_tables']['correct'] for p in matched),'both_wrong':sum(not p['graph']['correct'] and not p['incidence_tables']['correct'] for p in matched),'historical_correct':sum(p['historical_correct'] for p in matched),'fresh_graph_choice_changes':sum(p['graph']['choice']!=p['historical_choice'] for p in matched)},
  'literal_id_controls':{'n':len(control_rows),'correct':sum(r['correct'] for r in control_rows),'observations':control_rows},'matched_observations':matched}

def viewer(out,report):
 e=html.escape;a=report['analysis'];body='<!doctype html><html lang="it"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Tabella delle incidenze e confronto degli ID</title><style>body{font:16px system-ui;max-width:1200px;margin:2rem auto;padding:1rem;color:#26313d}table{border-collapse:collapse;width:100%;margin:1rem 0}td,th{border:1px solid #ccd;padding:.5rem}pre{white-space:pre-wrap;overflow-wrap:anywhere}details{margin:1rem 0}</style><h1>Grafo ridotto o tabella esplicita delle incidenze?</h1><p>Stato: '+e(report['status'])+'. 48 confronti di witness e quattro controlli letterali degli ID. I fatti, gli ID, i contratti, le immagini e le domande principali restano identici; cambia solo la rappresentazione dello state.</p><table><tr><th>Formato</th><th>Esatte</th><th>Witness positivi</th><th>None negativi</th></tr>'
 for cond,g in a['by_condition'].items():
  v=g['overall'];body+='<tr><td>'+('Grafo ridotto' if cond=='graph' else 'Tabelle esplicite')+'</td><td>'+str(v['correct'])+'/'+str(v['n'])+'</td><td>'+str(v['positive_witnesses_correct'])+'/'+str(v['positive_n'])+'</td><td>'+str(v['negative_none_correct'])+'/'+str(v['negative_n'])+'</td></tr>'
 body+='</table><p>Controlli separati sugli ID letterali: '+str(a['literal_id_controls']['correct'])+'/'+str(a['literal_id_controls']['n'])+'. Questi controlli non includono un grafo e non dimostrano il corretto recupero delle incidenze.</p><table><tr><th>Caso</th><th>Grafo</th><th>Tabelle</th></tr>'
 for case in previous.source.CASES:
  body+='<tr><td>'+case+'</td>'
  for cond in CONDITIONS:
   v=a['by_condition'][cond]['by_case'][case];body+='<td>'+str(v['correct'])+'/'+str(v['n'])+'</td>'
  body+='</tr>'
 body+='</table><p>Sempre none varrebbe 16/24 per condizione. I conteggi sono nativi, senza correzioni del verificatore.</p>'
 example=next((c for c in report['calls'] if c['kind']=='binding' and c['condition']=='incidence_tables'),None)
 if example:
  body+='<h2>Esempio reale delle tabelle inviate</h2>'
  for snapshot in example['model_input']['state']['snapshots'].values():
   for name,t in snapshot['tables'].items():
    body+='<h3>'+name+'</h3><table><tr>'+''.join('<th>'+e(h)+'</th>' for h in t['columns'])+'</tr>'
    for row in t['rows']:body+='<tr>'+''.join('<td>'+e(json.dumps(v) if isinstance(v,list) else str(v))+'</td>' for v in row)+'</tr>'
    body+='</table>'
 for title,value in [('Confronti appaiati e baseline storica',a['paired_summary']),('Controlli degli ID',a['literal_id_controls']),('Matrici complete',a['by_condition']),('Limiti',report['limits']),('Input e risposte sanitizzate',report['calls'])]:body+='<details><summary>'+title+'</summary><pre>'+e(json.dumps(value,indent=2,ensure_ascii=False))+'</pre></details>'
 body+='<p><a href="VERIFIED_RESULTS.md">Interpretazione e audit verificato</a></p></html>';(out/'viewer.html').write_text(body,encoding='utf-8')

def save(out,report):
 report['analysis']=analyze(report['calls']);temp=out/'results.tmp';temp.write_text(json.dumps(report,indent=2),encoding='utf-8');temp.replace(out/'results.json');viewer(out,report)

def main(out,live=False):
 if live and (os.getenv('GITHUB_ACTIONS')!='true' or not os.getenv('TYPESAFE_API_KEY')):raise SystemExit('Actions and repository secret required')
 out.mkdir(parents=True,exist_ok=True)
 for name in ('PROTOCOL.md','VERIFIED_RESULTS.md'):
  p=Path(__file__).parent/name
  if p.exists():(out/name).write_text(p.read_text(encoding='utf-8'),encoding='utf-8')
 report={'experiment':'Lossless explicit incidence tables and literal-ID controls v1','status':'running' if live else 'offline_only','model':'jev-1.14.0','source_commit':os.getenv('GITHUB_SHA'),'run_id':os.getenv('GITHUB_RUN_ID'),'prior_run_id':PRIOR['run_id'],'limits':LIMITS,'calls':[]}
 events=[('pair',r,c) for r in REPLICAS for c in previous.source.CASES]+[('id_control',r,None) for r in REPLICAS];random.Random(SEED).shuffle(events);pair_index=0
 for kind,replica,case in events:
  conditions=(None,) if kind=='id_control' else CONDITIONS if pair_index%2==0 else tuple(reversed(CONDITIONS))
  if kind=='pair':pair_index+=1
  for condition in conditions:
   if kind=='id_control':
    p,meta=build_id_control(replica);audit=[];stats={};historical={};prior_hash=None
   else:p,meta,audit,stats,historical,prior_hash=build_payload(out,replica,case,condition)
   rec={'kind':'id_control' if kind=='id_control' else 'binding','replica':replica,'case':case,'condition':condition,'question_count':len(p['questions']),'question_metadata':meta,'asset_audit':audit,'state_sizes':stats,'historical_answers':historical,'prior_request_sha256':prior_hash,'model_input':{k:v for k,v in p.items() if k!='assets'},'request_sha256':hashlib.sha256(json.dumps(p,sort_keys=True).encode()).hexdigest()}
   if live:rec.update(previous.transport(p))
   report['calls'].append(rec);save(out,report);print('Recorded',len(report['calls']),'/ 26',rec['kind'],condition,flush=True)
   if rec.get('failure') in ('HTTP_400','HTTP_401','HTTP_403'):
    report['status']='request_rejected';save(out,report);raise SystemExit('Stopped after request rejection; sanitized artifact saved')
 report['status']='completed_with_failures' if any('failure' in c for c in report['calls']) else 'completed' if live else 'offline_only';save(out,report)
 if report['status']=='completed_with_failures':raise SystemExit('Sanitized failures recorded')

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,default=Path('output_explicit_tables'));ap.add_argument('--live',action='store_true');args=ap.parse_args();main(args.out,args.live)

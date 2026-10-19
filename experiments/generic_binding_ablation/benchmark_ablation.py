"""Small crossed ablation of historical schema descriptions and ordinal rubrics."""
from __future__ import annotations
import argparse,base64,copy,hashlib,html,json,math,os,random,sys,time
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'experiments/native_score_fanout'))
import benchmark_scores as base

SCHEMAS=('GS_HIST_DOUBLE_TRIANGLE','GS_HIST_MEDIAL_POLYROLE')
CONDITIONS=('compact_generic','explicit_generic','compact_concrete','explicit_concrete')
SOURCE=ROOT/'experiments/native_score_fanout/live_results.json'
PRIOR=json.loads(SOURCE.read_text(encoding='utf-8'))
THRESHOLDS=(.5,.65,.75,.85)
SEED=20261023
EXPLANATIONS={
 SCHEMAS[0]:{
  'variables':{'s':'one material segment','R0':'one closed region','R1':'a distinct closed region'},
  'requirements':['R0 and R1 are both triangles.','The very same segment s is a complete boundary side of both R0 and R1, rather than two different segments of equal length.'],
  'scope':'Structural role binding. No equality of lengths, congruence, bisection or theorem proof is a requirement.'},
 SCHEMAS[1]:{
  'variables':{'s':'one material segment','R0':'one closed region','R1':'a distinct closed region','H':'the host figure'},
  'requirements':['The same material segment s participates as a boundary side of both R0 and R1.','The same segment s also participates as an internal partition of H into R0 and R1. These are distinct participations of one object, not different objects.'],
  'scope':'Structural role binding. The regions need not both be triangles. No equality of lengths, congruence, bisection or theorem proof is a requirement.'}
}
LIMITS=[
 'Four matched workspaces from two geometric templates and two label/order repeats; not 28 independent geometries.',
 'All 28 previously missed positive bindings and 12 negative bindings are included, for two historical schemas only.',
 'State is the shared workspace. The explicit condition adds generic definitions, not candidate-specific bindings or new geometric facts.',
 'The explicit polyrole definition operationalizes the local reference checker; it does not establish the unique philosophical interpretation of the historical schema.',
 'The concrete criteria operationalize the same local target as the prior bridge dimensions. Generic criteria ask more abstractly about roles, relations and certified premises.',
 'Choice reuses identical instructions and four level descriptions, with shuffled neutral labels and an added none outlet; primitive comparisons include this uncertainty-protocol difference.',
 'Modal level and fixed threshold sensitivity are computed from the SAME native Score distribution without extra calls. Threshold sweeps are descriptive, not tuned deployment thresholds.',
 'The small-batch baseline must be compared with the previous 100-question baseline before attributing recovery to either intervention.',
 'Images and code-extracted region geometry remain identical. This is not autonomous visual extraction, proof, free-form discovery, or evidence of internal sequential reasoning.',
 'Only Actions may call Jev, with the repository secret and required images header. No long-context header or automatic retries.'
]

def prior_call(shape,repeat):
 return next(r for r in PRIOR['calls'] if r['kind']=='full' and r['shape']==shape and r['repeat']==repeat)

def build_payload(out,shape,repeat,condition):
 if condition not in CONDITIONS:raise ValueError('unknown_condition')
 prior=prior_call(shape,repeat)
 p=copy.deepcopy(prior['model_input']);mapping=prior['candidate_mapping'];meta=prior['question_metadata'];audit=prior['asset_audit']
 p['assets']={}
 for asset in audit:
  data=(Path(__file__).parent/'fixtures'/asset['file']).read_bytes()
  assert hashlib.sha256(data).hexdigest()==asset['sha256']
  path=out/asset['file'];path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
  p['assets'][asset['asset']]={'type':'image','format':'png','data_base64':base64.b64encode(data).decode('ascii')}
 assert hashlib.sha256(json.dumps(p,sort_keys=True).encode()).hexdigest()==prior['request_sha256']
 targets={q:info for q,info in meta.items() if info['stage']=='generic' and info['schema'] in SCHEMAS}
 questions={};metadata={}
 for q,info in targets.items():
  schema=info['schema'];score=copy.deepcopy(p['questions'][q]);alias=score['instructions']['schema_ref']
  if condition.startswith('explicit'):
   p['state']['schema_hypotheses'][alias]['definition']=copy.deepcopy(EXPLANATIONS[schema])
  if condition.endswith('concrete'):
   score['criteria']=copy.deepcopy(base.PAIR_LEVELS if schema==SCHEMAS[0] else base.POLY_LEVELS)
  method=mapping[info['candidate']];gold=base.binding_check(shape,method,schema)['instantiated']
  old=prior['response']['answers'][q]
  reference=base.bridge_oracle(shape,method)[schema]
  common={**info,'method':method,'reference_binding':gold,'reference_level':reference,'prior_score':old['normalized_score'],'prior_missed_positive':gold and old['normalized_score']<base.GS_MIN,'source_question_id':q}
  questions[q]=score;metadata[q]={**common,'primitive':'score'}
  rng=random.Random(SEED+100*repeat+int(q[1:]));labels=rng.sample(range(100,999),4)
  label_levels={'K'+str(label):i for i,label in enumerate(labels)}
  items=list(label_levels);rng.shuffle(items)
  criteria={label:score['criteria'][label_levels[label]] for label in items}
  criteria['none']='The supplied workspace does not provide enough information to select a described situation.'
  cq='D'+q[1:]
  questions[cq]={'type':'choice','instructions':copy.deepcopy(score['instructions']),'criteria':criteria}
  metadata[cq]={**common,'primitive':'choice','label_levels':label_levels}
 # Every intervention shares one counterbalanced question order within a workspace.
 order=list(questions);random.Random(SEED+repeat+(1000 if shape=='right' else 0)).shuffle(order)
 p['questions']={q:questions[q] for q in order}
 assert len(p['questions'])==20
 return p,mapping,metadata,audit,prior['request_sha256']

def numeric(value):
 return value if isinstance(value,(int,float)) and not isinstance(value,bool) and math.isfinite(value) else None

def sanitize(raw,questions):
 scores={q:v for q,v in questions.items() if v['type']=='score'}
 result=base.sanitize(raw,scores)
 for key,q in questions.items():
  if q['type']!='choice':continue
  a=raw.get('answers',{}).get(key,{})
  if a.get('choice') not in q['criteria']:raise ValueError('invalid_choice')
  probabilities=a.get('probabilities')
  if not isinstance(probabilities,dict) or set(probabilities)!=set(q['criteria']):raise ValueError('invalid_choice_probabilities')
  probs={k:numeric(v) for k,v in probabilities.items()}
  if any(v is None or not 0<=v<=1 for v in probs.values()):raise ValueError('invalid_probability')
  result['answers'][key]={'type':'choice','choice':a['choice'],'probabilities':probs,'confidence':numeric(a.get('confidence')),'reliability':numeric(a.get('reliability'))}
 return result

def transport(payload):
 if os.getenv('GITHUB_ACTIONS')!='true' or not os.getenv('TYPESAFE_API_KEY'):raise RuntimeError('actions_secret_required')
 import requests
 start=time.perf_counter()
 try:
  r=requests.post('https://api.typesafe.ai/v1/systemone',headers={'Authorization':'Bearer '+os.environ['TYPESAFE_API_KEY'],'TypeSafe-Danger-Zone-Images':'true'},json=payload,timeout=180)
  result={'failure':'HTTP_'+str(r.status_code)} if r.status_code!=200 else {'response':sanitize(r.json(),payload['questions'])}
 except Exception:result={'failure':'transport_or_typed_schema_failure'}
 result['elapsed_seconds']=time.perf_counter()-start
 return result

def confusion(rows,key):
 matrix={'supported':{'supported':0,'not_supported':0,'none':0},'not_supported':{'supported':0,'not_supported':0,'none':0}}
 for r in rows:
  value=r[key];pred='none' if value is None else 'supported' if value else 'not_supported'
  matrix['supported' if r['reference_binding'] else 'not_supported'][pred]+=1
 return matrix

def mean(items):
 items=list(items);return sum(items)/len(items) if items else None

def observations(calls):
 rows=[]
 for c in calls:
  for q,a in c.get('response',{}).get('answers',{}).items():
   m=c['question_metadata'][q]
   r={'shape':c['shape'],'repeat':c['repeat'],'condition':c['condition'],'question':q,**m,'confidence':a['confidence'],'reliability':a['reliability']}
   if m['primitive']=='score':
    probs=a['probabilities'];best=max(probs.values());modal=[int(k) for k,v in probs.items() if v==best]
    r.update(normalized_score=a['normalized_score'],top_level_probability=probs['3'],modal_level=modal[0] if len(modal)==1 else None,modal_binding=modal==[3],predicted_binding=a['normalized_score']>=base.GS_MIN)
   else:
    level=m['label_levels'].get(a['choice']);r.update(selected_level=level,predicted_binding=None if a['choice']=='none' else level==3)
   rows.append(r)
 return rows

def analyze(calls):
 rows=observations(calls);summary={};sensitivity={}
 for cond in CONDITIONS:
  summary[cond]={}
  for primitive in ('score','choice'):
   selected=[r for r in rows if r['condition']==cond and r['primitive']==primitive]
   positives=[r for r in selected if r['reference_binding']];negatives=[r for r in selected if not r['reference_binding']]
   value={'n':len(selected),'matrix':confusion(selected,'predicted_binding'),'previously_missed_recovered':sum(r['prior_missed_positive'] and r['predicted_binding'] is True for r in selected),'positive_bindings_recognized':sum(r['predicted_binding'] is True for r in positives),'positive_n':len(positives),'false_positive_n':sum(r['predicted_binding'] is True for r in negatives),'negative_n':len(negatives),'abstentions':sum(r['predicted_binding'] is None for r in selected),'mean_confidence':mean(r['confidence'] for r in selected if r['confidence'] is not None)}
   if primitive=='score':
    value.update(mean_positive_score=mean(r['normalized_score'] for r in positives),mean_negative_score=mean(r['normalized_score'] for r in negatives),modal_level_matrix=confusion(selected,'modal_binding'),mean_absolute_change_from_original_100q=mean(abs(r['normalized_score']-r['prior_score']) for r in selected),by_schema={s:{'mean_positive_score':mean(r['normalized_score'] for r in positives if r['schema']==s),'recognized':sum(r['predicted_binding'] for r in positives if r['schema']==s),'positive_n':sum(r['schema']==s for r in positives)} for s in SCHEMAS})
    sensitivity[cond]={str(t):{'positive_recovered':sum(r['normalized_score']>=t for r in positives),'false_positive_n':sum(r['normalized_score']>=t for r in negatives)} for t in THRESHOLDS}
   summary[cond][primitive]=value
 def effect(before,after):
  a={(r['shape'],r['repeat'],r['candidate'],r['schema']):r for r in rows if r['primitive']=='score' and r['condition']==before}
  b={(r['shape'],r['repeat'],r['candidate'],r['schema']):r for r in rows if r['primitive']=='score' and r['condition']==after}
  keys=a.keys()&b.keys()
  return {'paired_n':len(keys),'positive_n':sum(a[k]['reference_binding'] for k in keys),'mean_positive_score_delta':mean(b[k]['normalized_score']-a[k]['normalized_score'] for k in keys if a[k]['reference_binding']),'mean_negative_score_delta':mean(b[k]['normalized_score']-a[k]['normalized_score'] for k in keys if not a[k]['reference_binding']),'new_positive_recognitions':sum(a[k]['reference_binding'] and not a[k]['predicted_binding'] and b[k]['predicted_binding'] for k in keys),'lost_positive_recognitions':sum(a[k]['reference_binding'] and a[k]['predicted_binding'] and not b[k]['predicted_binding'] for k in keys)}
 effects={a+' -> '+b:effect(a,b) for a,b in (('compact_generic','explicit_generic'),('compact_concrete','explicit_concrete'),('compact_generic','compact_concrete'),('explicit_generic','explicit_concrete'))}
 return {'api_calls_attempted':sum('response' in c or 'failure' in c for c in calls),'api_failures':sum('failure' in c for c in calls),'native_answers':len(rows),'by_condition':summary,'paired_score_effects':effects,'fixed_threshold_sensitivity':sensitivity,'observations':rows}

def viewer(out,report):
 e=html.escape;a=report['analysis'];body='<!doctype html><html lang="it"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Generic Spaces descrizioni e scoring</title><style>body{font:16px system-ui;max-width:1200px;margin:2rem auto;padding:1rem;color:#26313d}table{border-collapse:collapse;width:100%;margin:1rem 0}td,th{border:1px solid #ccd;padding:.5rem;text-align:left}pre{white-space:pre-wrap;overflow-wrap:anywhere}img{width:180px}details{margin:1rem 0}</style><h1>Descrizione del Generic Space o scoring?</h1><p>Stesso workspace, geometria e immagini. Due fattori incrociati: descrizione compatta o esplicita nello state; criteri generici o concreti. Score e Choice usano gli stessi quattro testi dei livelli; Choice aggiunge none.</p><p>Stato: '+e(report['status'])+'. 20 domande per chiamata; due schemi storici. Il riferimento riguarda il binding strutturale locale, non una prova geometrica.</p><table><tr><th>Condizione</th><th>Tipo</th><th>Binding positivi riconosciuti</th><th>Falsi positivi</th><th>None</th><th>Score medio positivi</th></tr>'
 for cond,primitives in a['by_condition'].items():
  for kind,v in primitives.items():
   score=v.get('mean_positive_score');body+='<tr><td>'+e(cond)+'</td><td>'+kind+'</td><td>'+str(v['positive_bindings_recognized'])+'/'+str(v['positive_n'])+'</td><td>'+str(v['false_positive_n'])+'/'+str(v['negative_n'])+'</td><td>'+str(v['abstentions'])+'</td><td>'+('—' if score is None else f'{score:.3f}')+'</td></tr>'
 body+='</table><p>La soglia Score principale rimane 0,75. Le soglie alternative e la classe modale sono diagnostiche calcolate dagli stessi output; non sono ottimizzate come soluzione.</p>'
 for title,value in [('Effetti appaiati dei due fattori',a['paired_score_effects']),('Sensibilità alla soglia senza nuove chiamate',a['fixed_threshold_sensitivity']),('Matrici complete e riferimento al batch precedente',a['by_condition']),('Definizioni aggiunte nello state',EXPLANATIONS),('Limiti',report['limits'])]:
  body+='<details><summary>'+title+'</summary><pre>'+e(json.dumps(value,indent=2,ensure_ascii=False))+'</pre></details>'
 for shape in base.geometry.SHAPES:
  body+='<h2>'+shape+'</h2>'+''.join('<figure style="display:inline-block"><img src="images/'+shape+'/'+('initial' if m=='no_op' else m)+'.png"><figcaption>'+m+'</figcaption></figure>' for m in base.METHODS)
 body+='<details><summary>Risposte native sanitizzate e input ricostruibili</summary><pre>'+e(json.dumps(report['calls'],indent=2))+'</pre></details></html>'
 (out/'viewer.html').write_text(body,encoding='utf-8')

def save(out,report):
 report['analysis']=analyze(report['calls'])
 temp=out/'results.tmp';temp.write_text(json.dumps(report,indent=2),encoding='utf-8');temp.replace(out/'results.json');viewer(out,report)

def main(out,live=False):
 if live and (os.getenv('GITHUB_ACTIONS')!='true' or not os.getenv('TYPESAFE_API_KEY')):raise SystemExit('Actions and repository secret required')
 out.mkdir(parents=True,exist_ok=True)
 source_hash=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
 report={'experiment':'Historical Generic Space description x rubric ablation v1','model':'jev-1.14.0','status':'running' if live else 'offline_only','source_commit':os.getenv('GITHUB_SHA'),'run_id':os.getenv('GITHUB_RUN_ID'),'prior_run_id':PRIOR['run_id'],'prior_results_sha256':source_hash,'conditions':CONDITIONS,'definitions':EXPLANATIONS,'primary_threshold':base.GS_MIN,'fixed_diagnostic_thresholds':THRESHOLDS,'limits':LIMITS,'calls':[]}
 trials=[(shape,repeat,cond) for shape in base.geometry.SHAPES for repeat in range(2) for cond in CONDITIONS]
 random.Random(SEED).shuffle(trials)
 for shape,repeat,cond in trials:
  p,mapping,meta,audit,source=build_payload(out,shape,repeat,cond)
  record={'shape':shape,'repeat':repeat,'condition':cond,'question_count':len(p['questions']),'candidate_mapping':mapping,'question_metadata':meta,'asset_audit':audit,'prior_full_request_sha256':source,'model_input':{k:v for k,v in p.items() if k!='assets'},'body_bytes':len(json.dumps(p).encode()),'request_sha256':hashlib.sha256(json.dumps(p,sort_keys=True).encode()).hexdigest()}
  if live:record.update(transport(p))
  report['calls'].append(record);save(out,report);print('Recorded',len(report['calls']),'/ 16',cond,flush=True)
  if record.get('failure')=='HTTP_400':
   report['status']='request_validation_failed';save(out,report);raise SystemExit('Stopped after request validation failure; sanitized artifact saved')
 report['status']='completed_with_failures' if any('failure' in c for c in report['calls']) else 'completed' if live else 'offline_only'
 save(out,report)
 if report['status']=='completed_with_failures':raise SystemExit('Sanitized failures recorded')

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,default=Path('output_generic_ablation'));ap.add_argument('--live',action='store_true');args=ap.parse_args();main(args.out,args.live)

"""Matched wording/premise-access diagnostic: one native binary judgment per bridge."""
from __future__ import annotations
import argparse,base64,copy,hashlib,html,json,math,os,random,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'experiments/equivalence_class_relevance'))
import benchmark_classes as archive
prior=archive.prior
CONDITIONS=('current','explicit','coverage')
TITLES={'current':'Testo attuale','explicit':'Richiesta esplicita','coverage':'Esplicita + copertura certificata'}
SEED=2026102304
TOL=1e-7
EXPLICIT=('Prepare a later comparison using at least one of the TWO NEW regions induced by the candidate bridge whose OWN boundary contains the COMPLETE designated original reference side, from one original endpoint to the other. Keeping that side in the original host, or covering it only by taking the union of pieces from different regions, does not satisfy this request. The two original endpoints are interchangeable; no endpoint and no size balance is preferred.')
POLICY='All candidates pass both historical local GS contracts. Treat inline code-certified material and metric relations as supplied facts. Independently answer whether each candidate supplies a subfigure meeting the active objective. Several candidates, or none, may satisfy it. No unique winner is required.'
LIMITS=[
 '18 new Noul answers: three original individual bridges, two archived presentations of ONE host, three versions. Six requests of three independent targeted questions; no Score, composite, ranking or extra questions.',
 'Fresh current-text binary baseline. Historical multi-axis Score results are not a contemporaneous control for question-type changes. Only current-to-explicit wording and explicit-to-coverage premise access are matched contrasts.',
 'Images, IDs, candidate order, Mental/Generic Spaces, original material/metric facts and question text are frozen across conditions. Explicit arms change only active_objective.description; coverage adds one uniform per-region/all-original-sides certificate.',
 'Coverage facts deliberately make the needed premises accessible. This tests use of supplied geometric facts, not autonomous image extraction or independent proof. No candidate-level goal verdict is supplied.',
 'Reference labels are observer-only. A complete side must lie on the boundary of one newly induced region. Coverage by the union of distinct regions is insufficient.',
 'Fixed decision p>.5=yes, p<.5=no, p=.5=abstention (counted incorrect in accuracy). Report full matrices, raw probabilities, uncalibrated Brier loss and paired correctness changes. No threshold tuning or repair calls.',
 'Each condition has four positives and two negatives. Always-yes accuracy is 4/6, so accuracy alone cannot establish discrimination. The six cases are correlated views of three cuts, not independent geometric samples.',
 'Noul is a native probability of yes, not a degree-of-relevance score. Separate confidence is normally absent; absent confidence/reliability remain null. No internal sequential reasoning, creativity or general theorem claim.'
]

def projected_coverage(start,end,segments):
 """Union of collinear boundary-use intervals, clipped to a whole original side."""
 dx,dy=end[0]-start[0],end[1]-start[1];norm=dx*dx+dy*dy
 if norm<=TOL*TOL:raise ValueError('degenerate_original_side')
 length=math.sqrt(norm);intervals=[]
 for a,b in segments:
  if math.dist(a,b)<=TOL:continue
  if any(abs(dx*(p[1]-start[1])-dy*(p[0]-start[0]))/length>TOL for p in (a,b)):continue
  ts=[((p[0]-start[0])*dx+(p[1]-start[1])*dy)/norm for p in (a,b)]
  lo,hi=max(0.,min(ts)),min(1.,max(ts))
  if hi-lo>TOL:intervals.append((lo,hi))
 merged=[]
 for lo,hi in sorted(intervals):
  if merged and lo<=merged[-1][1]+TOL:merged[-1][1]=max(hi,merged[-1][1])
  else:merged.append([lo,hi])
 fraction=sum(hi-lo for lo,hi in merged)
 return {'covered_intervals':[list(map(lambda x:round(x,8),v)) for v in merged],
  'covered_fraction':round(fraction,8),'coverage':'complete' if fraction>=1-TOL else 'partial' if fraction>TOL else 'none'}

def coverage_certificate(objects,labels,candidate):
 """No reference side or task label is consulted: certify every side uniformly."""
 prior.certificate(objects)
 vertices=objects['HOST']['vertices'];rows=[]
 for i in range(2):
  region=objects['REGION_'+str(i)]
  segments=[tuple(objects[p]['xy'] for p in use['endpoints']) for use in region['boundary_uses']]
  for j,a in enumerate(vertices):
   b=vertices[(j+1)%len(vertices)]
   rows.append({'region':'R_'+candidate+'_'+str(i+1),'original_side':[labels[a],labels[b]],
    **projected_coverage(objects[a]['xy'],objects[b]['xy'],segments)})
 return {'scope':'Boundary coverage of each original host side by each individual induced region; intervals are measured from the listed first endpoint (0) to the second (1). Code-certified from boundary uses and explicit coordinates, not inferred from pixels.',
  'rows':rows,'geometric_tolerance_pixels':TOL,'interval_merge_tolerance':TOL}

def build_payload(out,replica,condition):
 if replica not in range(2) or condition not in CONDITIONS:raise ValueError('unknown_cell')
 old=archive.archived(replica,'intact_anchor');archive.validate_archive(old)
 p=copy.deepcopy(old['model_input']);p['assets']={};audit=copy.deepcopy(old['asset_audit'])
 for asset in audit:
  data=(Path(archive.__file__).parent/'fixtures'/asset['file']).read_bytes()
  assert hashlib.sha256(data).hexdigest()==asset['sha256']
  path=out/asset['file'];path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
  p['assets'][asset['asset']]={'type':'image','format':'png','data_base64':base64.b64encode(data).decode('ascii')}
 assert prior.base.digest(p)==old['request_sha256']
 p['state']['evidence_policy']=POLICY
 if condition!='current':p['state']['active_objective']['description']=EXPLICIT
 if condition=='coverage':
  p['state']['certified_original_side_coverage']={c:coverage_certificate(prior.objects_for(m,replica),old['point_labels'],c) for c,m in old['candidate_mapping'].items()}
 # Freeze question order within each archived presentation, independently of condition.
 candidates=list(old['candidate_mapping']);random.Random(SEED+replica).shuffle(candidates)
 meta={};questions={};gold={}
 for i,c in enumerate(candidates):
  q='Q'+str(i+1).zfill(3)
  questions[q]={'type':'noul','instructions':{'candidate_ref':c,'objective_ref':'active_objective','question':'Does this candidate supply a subfigure that satisfies the active objective?'}}
  meta[q]={'candidate':c}
  gold[c]=prior.useful(prior.objects_for(old['candidate_mapping'][c],replica),'intact_anchor')
 p['questions']=questions
 observer={'replica':replica,'condition':condition,'candidate_mapping':old['candidate_mapping'],'point_labels':old['point_labels'],
  'question_metadata':meta,'reference':gold,'prior_request_sha256':old['request_sha256']}
 return p,observer,audit

def number(value):return value if isinstance(value,(int,float)) and not isinstance(value,bool) and math.isfinite(value) else None

def sanitize(raw,questions):
 if set(raw.get('answers',{}))!=set(questions):raise ValueError('answer_keys')
 clean={}
 for q in questions:
  answer=raw['answers'][q];p=number(answer.get('noul'))
  if answer.get('type')!='noul' or p is None or not 0<=p<=1:raise ValueError('invalid_noul')
  clean[q]={'type':'noul','noul':p,'confidence':number(answer.get('confidence')),'reliability':number(answer.get('reliability'))}
 usage=raw.get('usage',{})
 return {'answers':clean,'usage':{k:number(usage.get(k)) for k in ('input_tokens','output_tokens','total_tokens')},'reliability':number(raw.get('reliability')),
  'returned_model':raw.get('model') if raw.get('model')=='jev-1.14.0' else None}

def transport(payload):
 if os.getenv('GITHUB_ACTIONS')!='true' or not os.getenv('TYPESAFE_API_KEY'):raise RuntimeError('actions_secret_required')
 import requests
 start=time.perf_counter()
 try:
  res=requests.post('https://api.typesafe.ai/v1/systemone',headers={'Authorization':'Bearer '+os.environ['TYPESAFE_API_KEY'],'TypeSafe-Danger-Zone-Images':'true'},json=payload,timeout=180)
  result={'response':sanitize(res.json(),payload['questions'])} if res.status_code==200 else {'failure':'HTTP_'+str(res.status_code)}
 except Exception:result={'failure':'transport_or_noul_schema_failure'}
 result['elapsed_seconds']=time.perf_counter()-start
 return result

def analyze(calls):
 rows=[]
 for call in calls:
  for q,answer in call.get('response',{}).get('answers',{}).items():
   c=call['question_metadata'][q]['candidate'];gold=call['reference'][c];p=answer['noul'];decision=None if p==.5 else p>.5
   rows.append({'replica':call['replica'],'condition':call['condition'],'candidate':c,'method':call['candidate_mapping'][c],
    'reference':gold,'p_yes':p,'decision':decision,'correct':decision is not None and decision==gold,'brier':(p-int(gold))**2})
 summaries={}
 for condition in CONDITIONS:
  rr=[r for r in rows if r['condition']==condition]
  matrix={k:sum(r['reference']==g and r['decision'] is d for r in rr) for k,g,d in [('tp',True,True),('fn',True,False),('fp',False,True),('tn',False,False),('abstain_positive',True,None),('abstain_negative',False,None)]}
  positives=sum(r['reference'] for r in rr);negatives=len(rr)-positives
  summaries[condition]={'answers':len(rr),'correct':sum(r['correct'] for r in rr),'positive_cases':positives,'negative_cases':negatives,'always_yes_correct':positives,
   'matrix':matrix,'mean_brier':sum(r['brier'] for r in rr)/len(rr) if rr else None}
 paired={}
 for first,second in zip(CONDITIONS,CONDITIONS[1:]):
  aa={(r['replica'],r['method']):r for r in rows if r['condition']==first};bb={(r['replica'],r['method']):r for r in rows if r['condition']==second};keys=aa.keys()&bb.keys()
  paired[first+'_to_'+second]={'paired':len(keys),'improved':sum(not aa[k]['correct'] and bb[k]['correct'] for k in keys),'worsened':sum(aa[k]['correct'] and not bb[k]['correct'] for k in keys),
   'both_correct':sum(aa[k]['correct'] and bb[k]['correct'] for k in keys),'both_incorrect':sum(not aa[k]['correct'] and not bb[k]['correct'] for k in keys)}
 return {'api_calls_attempted':sum('response' in c or 'failure' in c for c in calls),'api_failures':sum('failure' in c for c in calls),'native_noul_answers':len(rows),
  'by_condition':summaries,'paired':paired,'observations':rows,'usage_totals':{k:sum(c['response']['usage'][k] for c in calls if c.get('response',{}).get('usage',{}).get(k) is not None) if any(c.get('response',{}).get('usage',{}).get(k) is not None for c in calls) else None for k in ('input_tokens','output_tokens','total_tokens')}}

def viewer(out,report):
 e=html.escape;a=report['analysis']
 body='<!doctype html><html lang="it"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>JEV — lato intatto</title><style>body{font:16px system-ui;max-width:1150px;margin:2rem auto;padding:1rem;color:#26313d}table{border-collapse:collapse;width:100%;margin:1rem 0}td,th{border:1px solid #ccd;padding:.5rem}pre{white-space:pre-wrap;overflow-wrap:anywhere}img{width:230px;max-width:100%}details{margin:1rem 0}.note{background:#edf3f7;padding:1rem}</style><h1>Lato intatto: formulazione o accesso alle premesse?</h1><p>Stato: '+e(report['status'])+'. Tre versioni, tre bridge, due presentazioni: 18 giudizi binari nativi Noul, nessun composito.</p>'
 if not a['native_noul_answers']:body+='<p class="note">Preparazione offline: nessuna risposta Jev disponibile.</p>'
 else:
  body+='<table><tr><th>Versione</th><th>Corretti</th><th>TP / FN</th><th>TN / FP</th><th>Astensioni</th><th>Brier</th></tr>'
  for c,s in a['by_condition'].items():
   m=s['matrix'];body+='<tr><td>'+TITLES[c]+'</td><td>'+str(s['correct'])+'/'+str(s['answers'])+'</td><td>'+str(m['tp'])+' / '+str(m['fn'])+'</td><td>'+str(m['tn'])+' / '+str(m['fp'])+'</td><td>'+str(m['abstain_positive']+m['abstain_negative'])+'</td><td>'+f"{s['mean_brier']:.4f}"+'</td></tr>'
  body+='</table>'
 body+='<p class="note">Il riferimento richiede un lato originale completo sul bordo di UNA delle due nuove regioni. Due bridge lo conservano; il terzo lo divide fra le regioni. Sempre sì farebbe 4/6. Sono due viste della stessa geometria, non sei geometrie indipendenti. Noul è probabilità di sì, non intensità della pertinenza.</p>'
 for replica in range(2):
  sample=next((c for c in report['calls'] if c['replica']==replica),None)
  if not sample:continue
  body+='<h2>Presentazione '+str(replica)+'</h2><p>Lato designato: '+e('–'.join(sample['model_input']['state']['active_objective']['designated_reference_side']))+'</p>'
  for asset in sample['asset_audit']:body+='<figure style="display:inline-block;margin:.5rem"><img alt="Immagine archivata invariata" src="'+asset['file']+'"><figcaption>'+e(asset['asset'])+'</figcaption></figure>'
  body+='<table><tr><th>Candidato</th><th>Riferimento</th>'+''.join('<th>'+TITLES[c]+' — P(sì)</th>' for c in CONDITIONS)+'</tr>'
  for candidate in sample['candidate_mapping']:
   body+='<tr><td>'+candidate+'</td><td>'+('sì' if sample['reference'][candidate] else 'no')+'</td>'
   for condition in CONDITIONS:
    row=next((r for r in a['observations'] if r['replica']==replica and r['candidate']==candidate and r['condition']==condition),None)
    body+='<td>'+ (f"{row['p_yes']:.4f}"+(' ✓' if row['correct'] else ' ✗') if row else 'non disponibile')+'</td>'
   body+='</tr>'
  body+='</table>'
 for title,value in [('Confronti appaiati e matrici',a),('Limiti',report['limits']),('Richieste e risposte sanitizzate',report['calls'])]:body+='<details><summary>'+title+'</summary><pre>'+e(json.dumps(value,indent=2,ensure_ascii=False))+'</pre></details>'
 body+='<p><a href="VERIFIED_RESULTS.md">Relazione verificata</a> · <a href="PROTOCOL.md">Protocollo</a></p></html>'
 (out/'viewer.html').write_text(body,encoding='utf-8')

def save(out,report):
 report['analysis']=analyze(report['calls']);tmp=out/'results.tmp';tmp.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');tmp.replace(out/'results.json');viewer(out,report)

def main(out,live=False):
 if live and (os.getenv('GITHUB_ACTIONS')!='true' or not os.getenv('TYPESAFE_API_KEY')):raise SystemExit('Actions and repository secret required')
 out.mkdir(parents=True,exist_ok=True)
 for name in ('PROTOCOL.md','VERIFIED_RESULTS.md'):
  source=Path(__file__).parent/name
  if source.exists():(out/name).write_text(source.read_text(encoding='utf-8'),encoding='utf-8')
 report={'experiment':'Intact original side — wording and premise access v1','status':'running' if live else 'offline_only','model':'jev-1.14.0','source_commit':os.getenv('GITHUB_SHA'),'run_id':os.getenv('GITHUB_RUN_ID'),
  'decision_policy':{'threshold':.5,'equal_threshold':'abstain_counted_incorrect'},'limits':LIMITS,
  'provenance':{'prior_run':archive.PRIOR['run_id'],'prior_source_commit':archive.PRIOR['source_commit'],'prior_results_canonical_sha256':prior.base.digest(archive.PRIOR)},'calls':[]}
 events=[(rep,c) for rep in range(2) for c in CONDITIONS];random.Random(SEED).shuffle(events)
 for replica,condition in events:
  p,meta,audit=build_payload(out,replica,condition);rec={**meta,'asset_audit':audit,'model_input':{k:v for k,v in p.items() if k!='assets'},'request_sha256':prior.base.digest(p)}
  if live:rec.update(transport(p))
  report['calls'].append(rec);save(out,report);print('Recorded',len(report['calls']),'/6',flush=True)
  if rec.get('failure') in ('HTTP_400','HTTP_401','HTTP_403'):
   report['status']='request_rejected';save(out,report);raise SystemExit('Request rejected; sanitized artifact saved')
 report['status']='completed_with_failures' if any('failure' in c for c in report['calls']) else 'completed' if live else 'offline_only';save(out,report)
 if report['status']=='completed_with_failures':raise SystemExit('Sanitized failures recorded')

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,default=Path('output_intact_side_diagnostic'));ap.add_argument('--live',action='store_true');args=ap.parse_args();main(args.out,args.live)

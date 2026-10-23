"""Fixed explicit wording on three new triangle geometries and nearby certified cuts."""
from __future__ import annotations
import argparse,base64,copy,hashlib,html,json,math,os,random,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'experiments/intact_side_diagnostic'))
import benchmark_intact as previous
base=previous.prior.base
HERE=Path(__file__).parent
SEED=2026102305
FIGURES={
 'acute_scalene':{'points':{'A':[-120,90],'B':[115,78],'C':[-32,-115]},'epsilon':.12,'rotation':13,'reflection':1,'title':'Scaleno acutangolo'},
 'right_scalene':{'points':{'A':[-110,90],'B':[110,90],'C':[-110,-100]},'epsilon':.10,'rotation':51,'reflection':-1,'title':'Scaleno rettangolo'},
 'obtuse_scalene':{'points':{'A':[-125,70],'B':[120,70],'C':[-65,15]},'epsilon':.14,'rotation':-23,'reflection':1,'title':'Scaleno ottusangolo'}}
METHODS=('A_to_near_C','C_to_near_A','B_to_near_C','C_to_near_B')
PAIRS=(('A_to_near_C','C_to_near_A'),('B_to_near_C','C_to_near_B'))
LIMITS=[
 '12 new native Noul judgments in three requests of four questions: three new triangle hosts, two positive/negative nearby-cut pairs per host. Six positives, six negatives; always-yes and always-no both give 6/12.',
 'Exact previous explicit objective, general evidence policy and per-candidate binary question. No coverage table, complete/partial/none fact or candidate goal verdict enters model-visible state. Observer-only code coverage supplies reference labels.',
 'All four constructions per host satisfy BOTH existing local historical GS contracts before any request: same complete material carrier on two adjacent triangles, disjoint interiors, complete host partition. Negative means misses this objective, not invalid bridge.',
 'Within each pair, one endpoint moves from an original side endpoint into that side while the other moves from a nearby opposite-side point to the opposite original vertex. Cuts lie near the same original boundary; endpoint displacement is at most epsilon times the longest host side (epsilon .10/.12/.14). No zero-area or coincident cuts.',
 'Three metric host types and three fixed orientations/alias layouts, not twelve independent geometries. Shapes are intentionally different and not similar to each other or to the earlier isosceles host. Orientation is not crossed with shape in this low-budget run.',
 'Question order, candidate IDs/order and point/GS aliases randomized before live with seed 2026102305; no retries, follow-ups, threshold fitting, composite or unique-winner policy.',
 'Same fixed p>.5=yes, p<.5=no, p=.5=abstention counted incorrect. Full matrices, raw Noul probabilities, uncalibrated Brier loss, per-host results and paired positive/negative separation. Strict p_positive>p_negative is a diagnostic, not an alternate success threshold.',
 'Images and structured region cycles, material and metric facts remain available. This is generalization of an explicit local predicate, not isolated visual extraction, autonomous binding, proof, open-ended bridge usefulness, or internal sequential reasoning.',
 'Historical explicit 6/6 on the old host is context only; no new old-host control is requested. These new families, constructions and images are synthetic and selected by code, not an independently sampled external test set.'
]

def layout(figure):
 rng=random.Random(SEED+list(FIGURES).index(figure));methods=list(METHODS);rng.shuffle(methods)
 mapping=dict(zip(['C'+str(n) for n in rng.sample(range(100,999),4)],methods))
 labels=dict(zip('ABCDEFG',rng.sample(list('ABCDEFGHJKLMNPQRSTUVWXYZ'),7)))
 gs=dict(zip(base.GS,['H'+str(n) for n in rng.sample(range(100,999),2)]))
 return mapping,labels,gs

def objects_for(figure,method):
 cfg=FIGURES[figure];raw=copy.deepcopy(cfg['points']);eps=cfg['epsilon']
 mix=lambda a,b,t:[(1-t)*a[i]+t*b[i] for i in (0,1)]
 raw.update(D=mix(raw['A'],raw['B'],eps),G=mix(raw['A'],raw['B'],1-eps),E=mix(raw['B'],raw['C'],1-eps),F=mix(raw['A'],raw['C'],1-eps))
 source,contact={'A_to_near_C':('A','E'),'C_to_near_A':('C','D'),'B_to_near_C':('B','F'),'C_to_near_B':('C','G')}[method]
 opposite=[v for v in 'ABC' if v!=source]
 # Explicit consistently ordered face cycles; no reference labels are consulted.
 faces={'A':[['A','B',contact],[contact,'C','A']],'B':[['B','C',contact],[contact,'A','B']],'C':[['C','A',contact],[contact,'B','C']]}[source]
 angle=math.radians(cfg['rotation']);reflection=cfg['reflection']
 def transform(p):
  x,y=p;return [round(160+.85*(reflection*x*math.cos(angle)-y*math.sin(angle)),8),round(160+.85*(reflection*x*math.sin(angle)+y*math.cos(angle)),8)]
 objects={k:{'type':'point','xy':transform(v)} for k,v in raw.items()}
 objects['HOST']={'type':'host','vertices':list('ABC')};objects['BRIDGE']={'type':'segment','endpoints':[source,contact]};boundaries={}
 for i,face in enumerate(faces):
  uses=[]
  for j,a in enumerate(face):
   b=face[(j+1)%len(face)];edge=frozenset((a,b))
   if edge==frozenset((source,contact)):carrier='BRIDGE'
   else:
    if edge not in boundaries:
     boundaries[edge]='BOUNDARY_'+str(len(boundaries)+1);objects[boundaries[edge]]={'type':'segment','endpoints':[a,b]}
    carrier=boundaries[edge]
   uses.append({'carrier':carrier,'endpoints':[a,b]})
  objects['REGION_'+str(i)]={'type':'region','vertices':face,'boundary_uses':uses}
 return objects

def reference(objects):
 cert=previous.coverage_certificate(objects,{v:v for v in 'ABCDEFG'},'observer')
 result=any(r['coverage']=='complete' for r in cert['rows'] if set(r['original_side'])=={'A','B'})
 # Independent fixture-specific endpoint-membership cross-check.
 assert result==any({'A','B'}<=set(objects['REGION_'+str(i)]['vertices']) for i in range(2))
 return result,cert

def nearby_pair(figure,positive,negative):
 a=objects_for(figure,positive);b=objects_for(figure,negative)
 ep=[a[v]['xy'] for v in a['BRIDGE']['endpoints']];en=[b[v]['xy'] for v in b['BRIDGE']['endpoints']]
 distance=min(max(math.dist(ep[0],en[0]),math.dist(ep[1],en[1])),max(math.dist(ep[0],en[1]),math.dist(ep[1],en[0])))
 longest=max(math.dist(a[x]['xy'],a[y]['xy']) for x,y in (('A','B'),('B','C'),('C','A')))
 assert distance<=FIGURES[figure]['epsilon']*longest+1e-7
 assert reference(a)[0] and not reference(b)[0]
 return {'methods':[positive,negative],'max_matched_endpoint_displacement_pixels':distance,'relative_to_longest_host_side':distance/longest}

def freeze_fixtures():
 fixtures=HERE/'fixtures';manifest={'seed':SEED,'figures':{}}
 for figure in FIGURES:
  mapping,labels,_=layout(figure);assets=[]
  for candidate,method in list(mapping.items())+[(None,METHODS[0])]:
   asset='image_'+candidate if candidate else 'initial';relative=Path('images')/figure/(asset+'.png');path=fixtures/relative
   objects=objects_for(figure,method);previous.prior.certificate(objects)
   base.render(objects,labels,path,bridge=candidate is not None)
   assets.append({'asset':asset,'file':relative.as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
  manifest['figures'][figure]={'asset_audit':assets,'objects_sha256':{m:base.digest(objects_for(figure,m)) for m in METHODS},'candidate_mapping':mapping,'point_labels':labels}
 (fixtures/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')

def build_payload(out,figure):
 replica=list(FIGURES).index(figure);mapping,labels,gs=layout(figure)
 frozen=json.loads((HERE/'fixtures/manifest.json').read_text(encoding='utf-8'))['figures'][figure]
 assert frozen['candidate_mapping']==mapping and frozen['point_labels']==labels
 assets={};audit=copy.deepcopy(frozen['asset_audit']);candidates={};gold={};certificates={}
 for asset in audit:
  data=(HERE/'fixtures'/asset['file']).read_bytes();assert hashlib.sha256(data).hexdigest()==asset['sha256']
  path=out/asset['file'];path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
  assets[asset['asset']]={'type':'image','format':'png','data_base64':base64.b64encode(data).decode('ascii')}
 for candidate,method in mapping.items():
  objects=objects_for(figure,method);assert base.digest(objects)==frozen['objects_sha256'][method]
  cert=previous.prior.certificate(objects)
  cert=base.checker.rename(cert,{**labels,**gs,'BRIDGE':'S_'+candidate,'HOST':'host','REGION_0':'R_'+candidate+'_1','REGION_1':'R_'+candidate+'_2'})
  cert['generic_space_bindings']={gs[k]:v for k,v in cert['generic_space_bindings'].items()}
  candidates[candidate]={'image':'image_'+candidate,'verified_certificate':cert,'region_vertex_cycles':[[labels[k] for k in objects['REGION_'+str(i)]['vertices']] for i in range(2)]}
  gold[candidate],certificates[candidate]=reference(objects)
 spaces={}
 for vertex in 'ABC':
  opposite=[v for v in 'ABC' if v!=vertex]
  spaces['fan_'+labels[vertex]]={'kind':'angular_fan','root_vertex':labels[vertex],'incident_original_sides':[[labels[vertex],labels[v]] for v in opposite]}
  spaces['side_'+labels[vertex]]={'kind':'original_side_carrier','endpoints':[labels[v] for v in opposite]}
 objective=previous.prior.objective('intact_anchor',labels);objective['description']=previous.EXPLICIT
 o=objects_for(figure,METHODS[0]);equal=abs(math.dist(o['A']['xy'],o['C']['xy'])-math.dist(o['B']['xy'],o['C']['xy']))<1e-6
 state={'workspace_kind':'prospective constructions, all independently certified admissible','initial_image':'initial','mental_spaces':spaces,
  'generic_spaces':{gs[k]:{'abstract_roles':[{a:b for a,b in r.items() if a in ('role','relation')} for r in base.native.ENTRIES[k]['abstract_roles']],'local_binding_contract':base.checker.CONTRACTS[v]} for k,v in base.GS.items()},
  'admissible_bridges':candidates,'active_objective':objective,'certified_host_facts':{'designated_reference_side':[labels['A'],labels['B']],'other_two_original_sides_have_equal_length':equal,'status':'Verified from explicit coordinates; no metric relation is inferred from the images.'},'evidence_policy':previous.POLICY}
 order=list(mapping);random.Random(SEED+100+replica).shuffle(order);questions={};meta={}
 for i,candidate in enumerate(order):
  q='Q'+str(i+1).zfill(3);questions[q]={'type':'noul','instructions':{'candidate_ref':candidate,'objective_ref':'active_objective','question':'Does this candidate supply a subfigure that satisfies the active objective?'}};meta[q]={'candidate':candidate}
 observer={'figure':figure,'replica':replica,'condition':'explicit','candidate_mapping':mapping,'point_labels':labels,'question_metadata':meta,'reference':gold,'observer_only_coverage':certificates,'nearby_pairs':[nearby_pair(figure,*pair) for pair in PAIRS]}
 return {'model':'jev-1.14.0','assets':assets,'state':state,'questions':questions},observer,audit

def analyze(calls):
 a=previous.analyze(calls);rows=a['observations'];pairs=[]
 for call in calls:
  if not call.get('response'):continue
  rr={r['method']:r for r in rows if r['replica']==call['replica']}
  for positive,negative in PAIRS:
   yes,no=rr[positive],rr[negative];pairs.append({'figure':call['figure'],'methods':[positive,negative],'p_positive':yes['p_yes'],'p_negative':no['p_yes'],'margin':yes['p_yes']-no['p_yes'],'strict_order':yes['p_yes']>no['p_yes'],'both_correct':yes['correct'] and no['correct']})
 return {k:a[k] for k in ('api_calls_attempted','api_failures','native_noul_answers','usage_totals')}|{'overall':a['by_condition']['explicit'],
  'by_figure':{figure:previous.analyze([c for c in calls if c['figure']==figure])['by_condition']['explicit'] for figure in FIGURES},
  'observations':rows,'nearby_pairs':pairs,'pairs_both_correct':sum(p['both_correct'] for p in pairs),'pairs_strict_order':sum(p['strict_order'] for p in pairs),'pair_count':len(pairs)}

def viewer(out,report):
 e=html.escape;a=report['analysis'];s=a['overall'];m=s['matrix']
 body='<!doctype html><html lang="it"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>JEV — lato intatto su nuove figure</title><style>body{font:16px system-ui;max-width:1150px;margin:2rem auto;padding:1rem;color:#26313d}table{border-collapse:collapse;width:100%;margin:1rem 0}td,th{border:1px solid #ccd;padding:.5rem}pre{white-space:pre-wrap;overflow-wrap:anywhere}img{width:210px;max-width:100%}details{margin:1rem 0}.note{background:#edf3f7;padding:1rem}</style><h1>Richiesta esplicita su tre figure nuove</h1><p>Stato: '+e(report['status'])+'. Una domanda Noul per bridge: massimo 12 giudizi, senza tabella di copertura o composito.</p>'
 body+='<p class="note">'+('Risposte corrette: '+str(s['correct'])+'/'+str(s['answers'])+'. TP/FN '+str(m['tp'])+'/'+str(m['fn'])+'; TN/FP '+str(m['tn'])+'/'+str(m['fp'])+'. Astensioni '+str(m['abstain_positive']+m['abstain_negative'])+'.' if s['answers'] else 'Preparazione offline: nessuna risposta Jev disponibile.')+' Sempre sì darebbe 6/12 sul campione completo. Il lato deve appartenere interamente al bordo di UNA nuova regione. Il codice verifica le costruzioni; Jev applica la richiesta ai fatti e alle immagini disponibili.</p>'
 for figure in FIGURES:
  call=next((c for c in report['calls'] if c['figure']==figure),None)
  if not call:continue
  body+='<h2>'+FIGURES[figure]['title']+'</h2><p>Lato designato: '+e('–'.join(call['model_input']['state']['active_objective']['designated_reference_side']))+'</p>'
  for asset in call['asset_audit']:body+='<figure style="display:inline-block;margin:.5rem"><img alt="Figura e bridge con soli ID neutri" src="'+asset['file']+'"><figcaption>'+e(asset['asset'])+'</figcaption></figure>'
  body+='<table><tr><th>Candidato</th><th>Riferimento esterno</th><th>P(sì) nativo</th><th>Esito</th></tr>'
  for candidate in call['candidate_mapping']:
   row=next((r for r in a['observations'] if r['replica']==call['replica'] and r['candidate']==candidate),None)
   body+='<tr><td>'+candidate+'</td><td>'+('sì' if call['reference'][candidate] else 'no')+'</td><td>'+(f"{row['p_yes']:.4f}" if row else 'non disponibile')+'</td><td>'+(('corretto' if row['correct'] else 'astensione' if row['decision'] is None else 'errore') if row else 'non disponibile')+'</td></tr>'
  body+='</table>'
 for title,value in [('Matrici e coppie vicine',a),('Limiti',report['limits']),('Input e risposte sanificate; riferimenti solo osservatore',report['calls'])]:body+='<details><summary>'+title+'</summary><pre>'+e(json.dumps(value,indent=2,ensure_ascii=False))+'</pre></details>'
 body+='<p><a href="PROTOCOL.md">Protocollo</a> · <a href="VERIFIED_RESULTS.md">Relazione verificata</a></p><p>Tre host e sei coppie correlate. Le immagini rappresentano alternative: nessuna prova di ragionamento sequenziale interno.</p></html>';(out/'viewer.html').write_text(body,encoding='utf-8')

def save(out,report):
 report['analysis']=analyze(report['calls']);tmp=out/'results.tmp';tmp.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');tmp.replace(out/'results.json');viewer(out,report)

def main(out,live=False):
 if live and (os.getenv('GITHUB_ACTIONS')!='true' or not os.getenv('TYPESAFE_API_KEY')):raise SystemExit('Actions and repository secret required')
 out.mkdir(parents=True,exist_ok=True)
 for name in ('PROTOCOL.md','VERIFIED_RESULTS.md'):
  source=HERE/name
  if source.exists():(out/name).write_text(source.read_text(encoding='utf-8'),encoding='utf-8')
 report={'experiment':'Explicit intact-side request on new figures v1','status':'running' if live else 'offline_only','model':'jev-1.14.0','source_commit':os.getenv('GITHUB_SHA'),'run_id':os.getenv('GITHUB_RUN_ID'),
  'decision_policy':{'threshold':.5,'equal_threshold':'abstain_counted_incorrect'},'limits':LIMITS,
  'provenance':{'parent_commit':'b3fdbbf1b4985489995bce685958e5eab5aaa714','prior_explicit_run':'39946781738','fixture_manifest_sha256':hashlib.sha256((HERE/'fixtures/manifest.json').read_bytes()).hexdigest()},'calls':[]}
 events=list(FIGURES);random.Random(SEED).shuffle(events)
 for figure in events:
  p,meta,audit=build_payload(out,figure);rec={**meta,'asset_audit':audit,'model_input':{k:v for k,v in p.items() if k!='assets'},'request_sha256':base.digest(p)}
  if live:rec.update(previous.transport(p))
  report['calls'].append(rec);save(out,report);print('Recorded',len(report['calls']),'/3',flush=True)
  if rec.get('failure') in ('HTTP_400','HTTP_401','HTTP_403'):
   report['status']='request_rejected';save(out,report);raise SystemExit('Request rejected; sanitized artifact saved')
 report['status']='completed_with_failures' if any('failure' in c for c in report['calls']) else 'completed' if live else 'offline_only';save(out,report)
 if report['status']=='completed_with_failures':raise SystemExit('Sanitized failures recorded')

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,default=Path('output_intact_side_new_figures'));ap.add_argument('--live',action='store_true');ap.add_argument('--freeze-fixtures',action='store_true');args=ap.parse_args()
 if args.freeze_fixtures:
  if args.live:raise SystemExit('Freeze offline before live evaluation')
  freeze_fixtures()
 else:main(args.out,args.live)

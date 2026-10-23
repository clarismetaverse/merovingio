"""Native relevance scoring on fixed, independently certified isometry classes."""
from __future__ import annotations
import argparse,base64,copy,hashlib,html,itertools,json,os,random,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'experiments/multi_bridge_relevance'))
import benchmark_multi as prior
from audit_multi import same

PRIOR_PATH=ROOT/'experiments/multi_bridge_relevance/live_results.json'
PRIOR=json.loads(PRIOR_PATH.read_text(encoding='utf-8'))
assert PRIOR['run_id']=='39940956209' and PRIOR['status']=='completed'
GOALS=prior.GOALS
AXES=prior.AXES
WEIGHTS=prior.WEIGHTS
DELTA=prior.DELTA
MIN_USEFUL=prior.MIN_USEFUL
SENSITIVITY_DELTAS=prior.SENSITIVITY_DELTAS
SEED=2026102303
LIMITS=[
 '24 new native Score answers in six requests of four questions: two fixed classes, two axes, three unchanged objectives, two archived presentations of ONE isosceles host.',
 'Class construction uses only fixed-host isometries and both checked material contracts, never utility labels or reference tiers. The two base-end cuts form a reflection class; the apex cut is a singleton.',
 'The SAME two classes are shown for all objectives. They are a structural refinement of the broader task equivalence: for the unanchored objective both classes may be equally useful.',
 'All original facts, objectives, candidate aliases/order, images and level descriptions are frozen from the archived individual-bridge experiment. Class membership/certification and class-level instructions are the intervention.',
 'Internal equality of scores after propagation to class members is guaranteed by code. It is not a Jev equivalence-recognition success. Cross-class equality is tested only in the broad objective.',
 'Fixed weights .5/.5, normalized scores, floor 2/3 and band .10 are reused, with all preregistered .05/.10/.15 settings. No forced unique choice, threshold search, repair or retries.',
 'Compare new class scores with both archived raw individual scores and a prespecified arithmetic-mean pooling of those old scores within each class. Pooling consumes no new calls and is not a new Jev output.',
 'The archived comparison is descriptive: no contemporaneous individual-arm rerun or causal estimate. Common state is larger due to class certificates; fewer questions need not mean fewer tokens.',
 'Two correlated axes and repeated presentations of one fixture do not measure general mathematical utility, creativity, autonomous GS discovery, proof or internal sequential reasoning.']

def archived(replica,goal):return next(c for c in PRIOR['calls'] if c['replica']==replica and c['goal']==goal)

def class_partition(replica):
 objects={m:prior.objects_for(m,replica) for m in prior.METHODS}
 for o in objects.values():prior.certificate(o)
 links={m:{m} for m in objects}
 for a,b in itertools.combinations(objects,2):
  if prior.mirror_equivalent(objects[a],objects[b]):links[a].add(b);links[b].add(a)
 components=[];remaining=set(objects)
 while remaining:
  group={min(remaining)}
  while True:
   expanded=group|set().union(*(links[m] for m in group))
   if expanded==group:break
   group=expanded
  for a,b in itertools.combinations(sorted(group),2):
   if not prior.mirror_equivalent(objects[a],objects[b]):raise ValueError('uncertified_isometry_class')
  components.append(sorted(group));remaining-=group
 assert sorted(map(len,components))==[1,2]
 return sorted(components,key=lambda group:(-len(group),group))

def objective_invariant_under_reflection(replica,goal):
 old=archived(replica,goal);labels=old['point_labels'];swap={'A':'B','B':'A','C':'C'}
 rename={prefix+labels[v]:prefix+labels[swap[v]] for prefix in ('fan_','side_') for v in 'ABC'}
 objective=old['model_input']['state']['active_objective']
 refs=objective['mental_space_refs'];side=objective['designated_reference_side']
 return {rename.get(v,v) for v in refs}==set(refs) and {dict((labels[v],labels[swap[v]]) for v in 'ABC').get(v,v) for v in side}==set(side)

def class_layout(replica):
 groups=class_partition(replica)
 if replica%2:groups=[list(reversed(g)) for g in reversed(groups)] # Balance class positions and member order.
 aliases=['E'+str(x) for x in random.Random(SEED+replica).sample(range(100,999),2)]
 return dict(zip(aliases,groups))

def validate_archive(old):
 assert old['model_input']['state']['active_objective']==prior.objective(old['goal'],old['point_labels'])
 for candidate,method in old['candidate_mapping'].items():assert same(old['geometry_certificates'][candidate],prior.certificate(prior.objects_for(method,old['replica'])))
 assert same(old['reference'],prior.reference(old['replica'],old['goal']))
 assert objective_invariant_under_reflection(old['replica'],old['goal'])

def build_payload(out,replica,goal):
 if replica not in range(2) or goal not in GOALS:raise ValueError('unknown_cell')
 old=archived(replica,goal);validate_archive(old);classes=class_layout(replica)
 p=copy.deepcopy(old['model_input']);p['assets']={};audit=copy.deepcopy(old['asset_audit'])
 for asset in audit:
  data=(Path(__file__).parent/'fixtures'/asset['file']).read_bytes();assert hashlib.sha256(data).hexdigest()==asset['sha256']
  path=out/asset['file'];path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
  p['assets'][asset['asset']]={'type':'image','format':'png','data_base64':base64.b64encode(data).decode('ascii')}
 assert prior.base.digest(p)==old['request_sha256']
 inverse={m:c for c,m in old['candidate_mapping'].items()}
 p['state']['certified_equivalence_classes']={code:{'members':[inverse[m] for m in members],
  'certificate':{'valid':True,'relation':'Fixed-host isometry preserving the material participation pattern and the semantics of every supplied objective; identity isometry covers singletons.',
   'identity_policy':'Members are distinct alternative constructions, not merged material objects.'}} for code,members in classes.items()}
 p['state']['class_scoring_policy']='The decision unit is a certified equivalence class. Its members are interchangeable under the supplied objectives. Judge the relevance of any representative; class size is neither a benefit nor a penalty. Several classes may receive the same high score. No unique winner is required.'
 jobs=[(c,a) for c in classes for a in AXES];random.Random(SEED+100+replica).shuffle(jobs)
 questions={};meta={}
 for index,(code,axis) in enumerate(jobs):
  q='R'+str(index+1).zfill(3)
  task='Rate relevance to the active aspects for the current objective.' if axis=='mental_spaces' else 'Rate how useful the certified Generic Space instantiations are for organizing the stated comparison, using the certified material and metric facts. Validity alone is not this score.'
  questions[q]={'type':'score','instructions':{'equivalence_class_ref':code,'dimension':axis,'objective_ref':'active_objective','task':task,
   'unit_policy':'Apply each bridge-level description to any representative of this certified class. Members are equivalent for these objectives. Score the class once; do not score or rank its members, favor cardinality or impose a unique winning class.'},'criteria':copy.deepcopy(prior.LEVELS[axis])}
  meta[q]={'class':code,'axis':axis}
 p['questions']=questions
 observer={'replica':replica,'goal':goal,'class_methods':classes,'candidate_mapping':old['candidate_mapping'],'point_labels':old['point_labels'],'question_metadata':meta,
  'reference':old['reference'],'prior_request_sha256':old['request_sha256'],'historical_answers':old['response']['answers'],'historical_question_metadata':old['question_metadata']}
 return p,observer,audit

def member_assessment(class_scores,classes,reference,delta=DELTA):
 expanded={m:class_scores[c] for c,members in classes.items() for m in members}
 result=prior.assess(expanded,reference,delta)
 expected=set(reference['useful_methods']);selected=set(prior.select_set(class_scores,delta));useful_classes=[];other_classes=[]
 for c,members in classes.items():
  flags=[m in expected for m in members]
  assert all(flags) or not any(flags)
  (useful_classes if all(flags) else other_classes).append(c)
 strict=[{'classes':[a,b],'margin':class_scores[a]-class_scores[b],'win':class_scores[a]>class_scores[b]+1e-9,'separated_by_band':class_scores[a]-class_scores[b]>delta+1e-9} for a in useful_classes for b in other_classes]
 equivalent=[{'classes':[a,b],'gap':abs(class_scores[a]-class_scores[b]),'within_band':abs(class_scores[a]-class_scores[b])<=delta+1e-9} for a,b in itertools.combinations(useful_classes,2)]
 # Internal pair equality is a code invariant, so discard it from the Jev readout.
 result.pop('equivalent_pairs');result.pop('strict_pairs')
 result.update(selected_classes=sorted(selected),expected_classes=sorted(useful_classes),strict_class_pairs=strict,cross_class_equivalent_pairs=equivalent,
  class_matrix={'tp':len(selected&set(useful_classes)),'fp':len(selected-set(useful_classes)),'fn':len(set(useful_classes)-selected)})
 return result

def historical_assessments(call):
 axes={m:{} for m in call['candidate_mapping'].values()}
 for q,a in call['historical_answers'].items():
  meta=call['historical_question_metadata'][q];method=call['candidate_mapping'][meta['candidate']];axes[method][meta['axis']]=a['normalized_score']
 raw={m:prior.base.native.weighted(values,WEIGHTS) for m,values in axes.items()}
 pooled={c:sum(raw[m] for m in members)/len(members) for c,members in call['class_methods'].items()}
 return {'raw':prior.assess(raw,call['reference']),'pooled':member_assessment(pooled,call['class_methods'],call['reference']),'pooled_class_scores':pooled}

def analyze(calls):
 observations=[]
 for call in calls:
  if not call.get('response'):continue
  axes={c:{} for c in call['class_methods']}
  for q,a in call['response']['answers'].items():
   meta=call['question_metadata'][q];axes[meta['class']][meta['axis']]=a['normalized_score']
  scores={c:prior.base.native.weighted(values,WEIGHTS) for c,values in axes.items()}
  historical=historical_assessments(call)
  observations.append({'replica':call['replica'],'goal':call['goal'],
   'classes':[{'class':c,'methods':call['class_methods'][c],'axis_scores':axes[c],'composite':scores[c]} for c in call['class_methods']],
   **member_assessment(scores,call['class_methods'],call['reference']),
   'by_axis':{axis:member_assessment({c:v[axis] for c,v in axes.items()},call['class_methods'],call['reference']) for axis in AXES},
   'sensitivity':{str(d):member_assessment(scores,call['class_methods'],call['reference'],d) for d in SENSITIVITY_DELTAS},
   'historical_raw':historical['raw'],'historical_pooled':historical['pooled'],'historical_pooled_class_scores':historical['pooled_class_scores']})
 strict=[p for g in observations for p in g['strict_class_pairs']];equivalent=[p for g in observations for p in g['cross_class_equivalent_pairs']]
 counts={'api_calls_attempted':sum('response' in c or 'failure' in c for c in calls),'api_failures':sum('failure' in c for c in calls),
  'native_score_answers':sum(len(c.get('response',{}).get('answers',{})) for c in calls),'groups':len(observations),
  'exact_set_matches':sum(g['exact_set_match'] for g in observations),'historical_raw_exact_set_matches':sum(g['historical_raw']['exact_set_match'] for g in observations),
  'historical_pooled_exact_set_matches':sum(g['historical_pooled']['exact_set_match'] for g in observations),
  'strict_class_wins':sum(p['win'] for p in strict),'strict_class_total':len(strict),'strict_class_separated_by_band':sum(p['separated_by_band'] for p in strict),
  'cross_class_equivalent_in_band':sum(p['within_band'] for p in equivalent),'cross_class_equivalent_total':len(equivalent),
  'member_matrix':{k:sum(g[k] for g in observations) for k in ('tp','fp','fn')},'class_matrix':{k:sum(g['class_matrix'][k] for g in observations) for k in ('tp','fp','fn')},
  'spurious_unique_member_sets':sum(g['spurious_unique_set'] for g in observations),'empty_sets':sum(g['empty_set'] for g in observations),
  'paired_vs_historical_raw':{'class_only_correct':sum(g['exact_set_match'] and not g['historical_raw']['exact_set_match'] for g in observations),'raw_only_correct':sum(not g['exact_set_match'] and g['historical_raw']['exact_set_match'] for g in observations)},
  'paired_vs_historical_pooled':{'class_only_correct':sum(g['exact_set_match'] and not g['historical_pooled']['exact_set_match'] for g in observations),'pooled_only_correct':sum(not g['exact_set_match'] and g['historical_pooled']['exact_set_match'] for g in observations)},
  'sensitivity':{str(d):{'exact_set_matches':sum(g['sensitivity'][str(d)]['exact_set_match'] for g in observations),
   'cross_class_equivalent_in_band':sum(p['within_band'] for g in observations for p in g['sensitivity'][str(d)]['cross_class_equivalent_pairs'])} for d in SENSITIVITY_DELTAS},
  'observations':observations,'usage_totals':{k:sum(c['response']['usage'][k] for c in calls if c.get('response',{}).get('usage',{}).get(k) is not None) if any(c.get('response',{}).get('usage',{}).get(k) is not None for c in calls) else None for k in ('input_tokens','output_tokens','total_tokens')}}
 return counts

def viewer(out,report):
 e=html.escape;a=report['analysis'];titles={'intact_anchor':'Lato conservato','unanchored_decomposition':'Decomposizione senza ancoraggio','exchangeable_views':'Sottofigure scambiabili'}
 body='<!doctype html><html lang="it"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>JEV: classi certificate</title><style>body{font:16px system-ui;max-width:1100px;margin:2rem auto;padding:1rem;color:#26313d}table{border-collapse:collapse;width:100%;margin:1rem 0}td,th{border:1px solid #ccd;padding:.5rem}pre{white-space:pre-wrap;overflow-wrap:anywhere}img{width:230px;max-width:100%}details{margin:1rem 0}.note{background:#edf3f7;padding:1rem}</style><h1>Scoring delle classi di equivalenza certificate</h1><p>Stato: '+e(report['status'])+'. Due classi strutturali fisse per gli stessi tre obiettivi. Sei richieste da quattro Score, massimo 24 risposte nuove.</p>'
 if not a['native_score_answers']:body+='<p class="note">Nessun nuovo risultato JEV disponibile: input preparati.</p>'
 else:body+='<p class="note">Insiemi ricostruiti: classi JEV '+str(a['exact_set_matches'])+'/'+str(a['groups'])+'; vecchi Score individuali '+str(a['historical_raw_exact_set_matches'])+'/'+str(a['groups'])+'; loro media per classe '+str(a['historical_pooled_exact_set_matches'])+'/'+str(a['groups'])+'. Preferenze fra classi '+str(a['strict_class_wins'])+'/'+str(a['strict_class_total'])+'; equivalenza fra classi nel caso aperto '+str(a['cross_class_equivalent_in_band'])+'/'+str(a['cross_class_equivalent_total'])+'.</p>'
 body+='<p>L’uguaglianza interna alla classe è imposta dal codice: non è un risultato di riconoscimento JEV. Le classi hanno ID anonimi e non comunicano quale sia utile. Composito 0,5/0,5, minimo 2/3 e fascia 0,10 invariati. Insiemi multipli e vuoti ammessi. Il confronto con il run precedente è storico.</p>'
 for replica in range(2):
  sample=next((c for c in report['calls'] if c['replica']==replica),None)
  if not sample:continue
  body+='<h2>Presentazione '+str(replica)+'</h2>'
  for asset in sample['asset_audit']:body+='<figure style="display:inline-block;margin:.5rem"><img alt="Immagine congelata del benchmark precedente" src="'+asset['file']+'"><figcaption>'+asset['asset']+'</figcaption></figure>'
  for g in [g for g in a['observations'] if g['replica']==replica]:
   body+='<h3>'+titles[g['goal']]+'</h3><p>Classi selezionate: '+(', '.join(g['selected_classes']) or 'nessuna')+'. Classi di riferimento: '+', '.join(g['expected_classes'])+'.</p><table><tr><th>Classe</th><th>Membri</th><th>Mental Spaces</th><th>Generic Spaces</th><th>Composito nuovo</th><th>Media vecchi Score</th></tr>'
   for row in g['classes']:
    members=', '.join(c for c,m in sample['candidate_mapping'].items() if m in row['methods'])
    body+='<tr><td>'+row['class']+'</td><td>'+members+'</td>'+''.join('<td>'+f'{v:.3f}'+'</td>' for v in (row['axis_scores']['mental_spaces'],row['axis_scores']['generic_spaces'],row['composite'],g['historical_pooled_class_scores'][row['class']]))+'</tr>'
   body+='</table>'
 for title,value in [('Analisi, sensibilità e confronti storici',a),('Limiti',report['limits']),('Input e risposte native',report['calls'])]:body+='<details><summary>'+title+'</summary><pre>'+e(json.dumps(value,indent=2,ensure_ascii=False))+'</pre></details>'
 body+='<p><a href="VERIFIED_RESULTS.md">Relazione verificata</a> · <a href="PROTOCOL.md">Protocollo</a></p></html>';(out/'viewer.html').write_text(body,encoding='utf-8')

def save(out,report):
 report['analysis']=analyze(report['calls']);tmp=out/'results.tmp';tmp.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');tmp.replace(out/'results.json');viewer(out,report)

def main(out,live=False):
 if live and (os.getenv('GITHUB_ACTIONS')!='true' or not os.getenv('TYPESAFE_API_KEY')):raise SystemExit('Actions and repository secret required')
 out.mkdir(parents=True,exist_ok=True)
 for name in ('PROTOCOL.md','VERIFIED_RESULTS.md'):
  p=Path(__file__).parent/name
  if p.exists():(out/name).write_text(p.read_text(encoding='utf-8'),encoding='utf-8')
 report={'experiment':'Native scoring of certified isometry classes v1','status':'running' if live else 'offline_only','model':'jev-1.14.0','source_commit':os.getenv('GITHUB_SHA'),'run_id':os.getenv('GITHUB_RUN_ID'),
  'weights':WEIGHTS,'set_policy':{'delta':DELTA,'min_useful':MIN_USEFUL,'sensitivity_deltas':SENSITIVITY_DELTAS},'limits':LIMITS,
  'provenance':{'prior_run':PRIOR['run_id'],'prior_source_commit':PRIOR['source_commit'],'prior_results_canonical_sha256':prior.base.digest(PRIOR),'prior_data_path':PRIOR_PATH.relative_to(ROOT).as_posix()},'calls':[]}
 events=[(r,g) for r in range(2) for g in GOALS];random.Random(SEED).shuffle(events)
 for replica,goal in events:
  p,meta,audit=build_payload(out,replica,goal);rec={**meta,'asset_audit':audit,'model_input':{k:v for k,v in p.items() if k!='assets'},'request_sha256':prior.base.digest(p)}
  if live:rec.update(prior.base.transport(p))
  report['calls'].append(rec);save(out,report);print('Recorded',len(report['calls']),'/6',flush=True)
  if rec.get('failure') in ('HTTP_400','HTTP_401','HTTP_403'):
   report['status']='request_rejected';save(out,report);raise SystemExit('Request rejected; sanitized artifact saved')
 report['status']='completed_with_failures' if any('failure' in c for c in report['calls']) else 'completed' if live else 'offline_only';save(out,report)
 if report['status']=='completed_with_failures':raise SystemExit('Sanitized failures recorded')

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,default=Path('output_equivalence_class_relevance'));ap.add_argument('--live',action='store_true');args=ap.parse_args();main(args.out,args.live)

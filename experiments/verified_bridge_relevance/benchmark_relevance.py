"""Goal-conditioned native Score ranking of independently certified bridges."""
from __future__ import annotations
import argparse,base64,copy,hashlib,html,json,math,os,random,sys,time
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'experiments/native_score_fanout'))
import benchmark_scores as native
sys.path.insert(0,str(ROOT/'experiments/concrete_role_binding'))
import benchmark_binding as checker

METHODS=('from_A','from_B','from_C')
GOALS=('A','B','C')
TRANSFORMS=((0,1),(37,-1))
AXES=('mental_spaces','generic_spaces')
WEIGHTS={'mental_spaces':.5,'generic_spaces':.5}
GS={'GS_HIST_DOUBLE_TRIANGLE':'shared_triangles','GS_HIST_MEDIAL_POLYROLE':'polyrole_partition'}
SEED=20261023
LEVELS={
 'mental_spaces':[
  'The admissible bridge adds no useful coupling of the two active Mental Spaces for the stated objective.',
  'The bridge engages only one active Mental Space directly, or establishes a different coupling that leaves the requested connection absent.',
  'The bridge engages both active Mental Spaces, but their requested coupling remains indirect or incomplete.',
  'The bridge directly couples both active Mental Spaces in the manner required by the current objective.'],
 'generic_spaces':[
  'The certified Generic Space instantiations offer no relevant organization of the comparison requested by the current objective.',
  'The certified patterns organize a different comparison; the requested correspondence between the active roles is absent.',
  'The certified patterns support part of the requested comparison, with an active role only indirectly represented.',
  'The certified shared-carrier and multiple-participation patterns directly organize the requested comparison between the active spaces.']}
LIMITS=[
 '36 native Score answers in six serial requests of six questions: three certified candidates, three objectives, two transformed presentations of ONE host triangle.',
 'Every candidate passes both local historical GS contracts before any model request. Certificates and inline structural relations are supplied intentionally; Jev does not retrieve or validate a binding.',
 'The objective is explicit. Usefulness is operationalized as relevance to a specified angular-fan/opposite-side comparison, not universal mathematical creativity or open-ended discovery.',
 'Within each replica only active_objective changes. Candidate order, aliases, geometry, images, certificates, questions and criteria are identical. Across replicas aliases/order change and the host is rotated/reflected.',
 'Mental and Generic relevance are two correlated semantic views of the same objective, not statistically independent tests. Equal weights are fixed before live evaluation.',
 'All candidates instantiate the same two GS contracts. Validity alone cannot select a candidate. A fixed candidate can match only one of three objectives per replica.',
 'The reference preference is computed from geometric incidence under the declared objective. No gold score, reference winner, rank, weights or missing-premise diagnosis enters the model input.',
 'This small synthetic test has no invalid-candidate negatives, no human usefulness judgments, no uncertified control arm and no causal comparison against earlier Choice experiments.',
 'Score normalization and composite ranking are code; native scores, probabilities and confidence are preserved. No threshold tuning, post-hoc weights, retries or repair calls.',
 'Alternative images are prospective candidates, not a temporal sequence. They do not demonstrate internal sequential reasoning, proof or autonomous visual extraction.']

def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True).encode()).hexdigest()

def objects_for(method,replica):
 g=native.proposal('left',method);points=g['points'];angle,reflection=TRANSFORMS[replica];r=math.radians(angle)
 def transform(p):
  x,y=(p[0]-440)/2.8,(p[1]-310)/2.8
  return [round(160+reflection*x*math.cos(r)-y*math.sin(r),8),round(160+reflection*x*math.sin(r)+y*math.cos(r),8)]
 objects={k:{'type':'point','xy':transform(v)} for k,v in points.items()}
 objects['HOST']={'type':'host','vertices':list('ABC')}
 ends=g['new_segment'];objects['BRIDGE']={'type':'segment','endpoints':ends}
 boundary={}
 for index,face in enumerate(g['regions']):
  uses=[]
  for i,a in enumerate(face):
   b=face[(i+1)%len(face)];edge=frozenset((a,b))
   if edge==frozenset(ends):carrier='BRIDGE'
   else:
    if edge not in boundary:
     carrier='BOUNDARY_'+str(len(boundary)+1);boundary[edge]=carrier;objects[carrier]={'type':'segment','endpoints':[a,b]}
    carrier=boundary[edge]
   uses.append({'carrier':carrier,'endpoints':[a,b]})
  objects['REGION_'+str(index)]={'type':'region','vertices':face,'boundary_uses':uses}
 return objects

def certificate(objects):
 witness={'carrier':'BRIDGE','regions':['REGION_0','REGION_1'],'host':'HOST'}
 checks={gs:checker.check_witness(objects,witness,schema,'HOST') for gs,schema in GS.items()}
 if any(checks.values()):raise ValueError('uncertified_candidate')
 ends=objects['BRIDGE']['endpoints'];vertices=list('ABC');source=[v for v in vertices if v in ends]
 if len(source)!=1:raise ValueError('missing_source_vertex')
 vertex=source[0];other=next(v for v in ends if v!=vertex);opposite=[v for v in vertices if v!=vertex]
 p=lambda v:objects[v]['xy']
 if not native.geometry.interior_between(p(opposite[0]),p(other),p(opposite[1])):raise ValueError('invalid_opposite_contact')
 return {'admissible':True,'generic_space_bindings':{gs:copy.deepcopy(witness) for gs in GS},
  'new_carrier':{'material_id':'BRIDGE','endpoints':ends},
  'direct_structural_relations':{'angular_fan_split_at_vertex':vertex,'interior_contact_on_original_side':opposite,
   'contact_point':other,'closed_regions':['REGION_0','REGION_1'],'partitioned_host':'HOST'},
  'verification_scope':'Local convex-polygon and material boundary-use checks; no metric equality, congruence or theorem conclusion.'}

def reference_method(replica,vertex):
 valid=[]
 for method in METHODS:
  objects=objects_for(method,replica);certificate(objects);ends=objects['BRIDGE']['endpoints'];opposite=[v for v in 'ABC' if v!=vertex]
  p=lambda v:objects[v]['xy']
  if vertex in ends and any(native.geometry.interior_between(p(opposite[0]),p(v),p(opposite[1])) for v in ends if v!=vertex):valid.append(method)
 assert len(valid)==1
 return valid[0]

def render(objects,labels,path,bridge=True):
 im=Image.new('RGB',(320,320),'white');d=ImageDraw.Draw(im);xy=lambda k:tuple(objects[k]['xy'])
 for a,b in (('A','B'),('B','C'),('C','A')):d.line([xy(a),xy(b)],fill='#26313d',width=3)
 names=list('ABC')
 if bridge:
  ends=objects['BRIDGE']['endpoints'];d.line([xy(k) for k in ends],fill='#26313d',width=3);names+= [k for k in ends if k not in names]
 font=ImageFont.load_default(size=15)
 for name in names:
  x,y=xy(name);d.ellipse((x-3,y-3,x+3,y+3),fill='#26313d');d.text((x+5,y+3),labels[name],font=font,fill='#26313d')
 path.parent.mkdir(parents=True,exist_ok=True);im.save(path)

def build_payload(out,replica,goal):
 if replica not in range(2) or goal not in GOALS:raise ValueError('unknown_cell')
 rng=random.Random(SEED+replica);methods=list(METHODS);rng.shuffle(methods)
 mapping=dict(zip(['C'+str(x) for x in rng.sample(range(100,999),3)],methods))
 point_names=list('ABCDEF');rng.shuffle(point_names);labels=dict(zip('ABCDEF',point_names))
 gs_alias=dict(zip(GS,['G'+str(x) for x in rng.sample(range(100,999),2)]))
 asset_files={};candidates={};certificates={}
 for candidate,method in mapping.items():
  objects=objects_for(method,replica);cert=certificate(objects);certificates[candidate]=cert
  cert=checker.rename(cert,{**labels,'BRIDGE':'S_'+candidate,'HOST':'host','REGION_0':'R_'+candidate+'_1','REGION_1':'R_'+candidate+'_2',**gs_alias})
  cert['generic_space_bindings']={gs_alias[k]:v for k,v in cert['generic_space_bindings'].items()}
  # rename() maps values, not dictionary keys. Every certificate is a local inline summary.
  image='image_'+candidate;path=out/'images'/('replica_'+str(replica))/(image+'.png');render(objects,labels,path)
  asset_files[image]=path;candidates[candidate]={'image':image,'verified_certificate':cert,
   'region_vertex_cycles':[[labels[k] for k in objects['REGION_'+str(i)]['vertices']] for i in range(2)]}
 initial=out/'images'/('replica_'+str(replica))/'initial.png';render(objects_for(METHODS[0],replica),labels,initial,False);asset_files['initial']=initial
 spaces={}
 for vertex in GOALS:
  opposite=[v for v in GOALS if v!=vertex]
  spaces['fan_'+labels[vertex]]={'kind':'angular_fan','root_vertex':labels[vertex],'incident_original_sides':[[labels[vertex],labels[v]] for v in opposite]}
  spaces['side_'+labels[vertex]]={'kind':'original_side_carrier','endpoints':[labels[v] for v in opposite]}
 state={'workspace_kind':'prospective constructions, all independently certified admissible',
  'initial_image':'initial','mental_spaces':spaces,'generic_spaces':{gs_alias[gs]:{'abstract_roles':[{k:v for k,v in r.items() if k in ('role','relation')} for r in native.ENTRIES[gs]['abstract_roles']],
    'local_binding_contract':checker.CONTRACTS[contract]} for gs,contract in GS.items()},
  'admissible_bridges':candidates,
  'active_objective':{'mental_space_refs':['fan_'+labels[goal],'side_'+labels[goal]],
   'description':'Compare the two parts of the active angular fan together with the two parts of the opposite original side, using adjacent closed subfigures and their shared new carrier as the common organizing relation.'},
  'evidence_policy':'All three bridges and BOTH GS bindings for each are already checked by code. Use their inline certified relations as supplied facts. Judge relevance to the active objective. Formal admissibility alone does not imply usefulness for that objective. No equality, congruence or proof is asserted.'}
 questions={};meta={};jobs=[(c,a) for c in mapping for a in AXES];rng.shuffle(jobs)
 for index,(c,axis) in enumerate(jobs):
  q='Q'+str(index+1).zfill(3)
  task='Rate how directly this bridge couples the active Mental Spaces for the stated objective.' if axis=='mental_spaces' else 'Rate how useful this bridge\'s certified Generic Space instantiations are for organizing the comparison requested by the active objective. Their formal validity is already established; do not rate validity instead of pertinence.'
  questions[q]={'type':'score','instructions':{'candidate_ref':c,'dimension':axis,'task':task,'objective_ref':'active_objective','policy':'Use the same four levels for every candidate. Scores are independent; there is no requirement to choose exactly one or to distribute a fixed score budget.'},'criteria':LEVELS[axis]}
  meta[q]={'candidate':c,'axis':axis}
 assets={k:{'type':'image','format':'png','data_base64':base64.b64encode(p.read_bytes()).decode('ascii')} for k,p in asset_files.items()}
 audit=[{'asset':k,'file':p.relative_to(out).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for k,p in asset_files.items()]
 payload={'model':'jev-1.14.0','assets':assets,'state':state,'questions':questions}
 observer={'replica':replica,'goal_vertex':goal,'candidate_mapping':mapping,'point_labels':labels,'gs_aliases':gs_alias,'question_metadata':meta,'reference_method':reference_method(replica,goal),'geometry_certificates':certificates}
 return payload,observer,audit

def transport(payload):
 if os.getenv('GITHUB_ACTIONS')!='true' or not os.getenv('TYPESAFE_API_KEY'):raise RuntimeError('actions_secret_required')
 import requests
 start=time.perf_counter()
 try:
  res=requests.post('https://api.typesafe.ai/v1/systemone',headers={'Authorization':'Bearer '+os.environ['TYPESAFE_API_KEY'],'TypeSafe-Danger-Zone-Images':'true'},json=payload,timeout=180)
  if res.status_code!=200:result={'failure':'HTTP_'+str(res.status_code)}
  else:
   raw=res.json()
   if set(raw.get('answers',{}))!=set(payload['questions']):raise ValueError('answer_keys')
   result={'response':native.sanitize(raw,payload['questions'])}
   result['response']['returned_model']=raw.get('model') if raw.get('model')==payload['model'] else None
 except Exception:result={'failure':'transport_or_score_schema_failure'}
 result['elapsed_seconds']=time.perf_counter()-start
 return result

def analyze(calls):
 rankings=[];byrep={}
 for call in calls:
  if not call.get('response'):continue
  axes={c:{} for c in call['candidate_mapping']}
  for q,a in call['response']['answers'].items():
   m=call['question_metadata'][q];axes[m['candidate']][m['axis']]=a['normalized_score']
  rows=[{'candidate':c,'method':m,'axis_scores':axes[c],'composite':native.weighted(axes[c],WEIGHTS)} for c,m in call['candidate_mapping'].items()]
  rows.sort(key=lambda x:-x['composite']);top=[r['method'] for r in rows if abs(r['composite']-rows[0]['composite'])<1e-9]
  target=next(r for r in rows if r['method']==call['reference_method']);distractors=[r for r in rows if r['method']!=call['reference_method']]
  entry={'replica':call['replica'],'goal_vertex':call['goal_vertex'],'ranking':rows,'top_methods':top,'reference_method':call['reference_method'],'unique_reference_top':top==[call['reference_method']],
   'reference_in_top_tie':call['reference_method'] in top,'reference_margin':target['composite']-max(r['composite'] for r in distractors),
   'axis_reference_margins':{a:target['axis_scores'][a]-max(r['axis_scores'][a] for r in distractors) for a in AXES},
   'pairwise_reference_wins':sum(target['composite']>r['composite']+1e-9 for r in distractors),'pairwise_reference_ties':sum(abs(target['composite']-r['composite'])<1e-9 for r in distractors)}
  rankings.append(entry);byrep.setdefault(call['replica'],[]).append(entry)
 changes=[]
 for replica,rows in byrep.items():
  if len(rows)!=3:continue
  for method in METHODS:
   matched=next(r for r in rows if r['reference_method']==method);own=next(c['composite'] for c in matched['ranking'] if c['method']==method)
   others=[next(c['composite'] for c in r['ranking'] if c['method']==method) for r in rows if r is not matched]
   changes.append({'replica':replica,'method':method,'matched_objective_composite':own,'other_objectives_composites':others,'matched_above_both':own>max(others)+1e-9,'margin':own-max(others)})
 return {'api_calls_attempted':sum('response' in c or 'failure' in c for c in calls),'api_failures':sum('failure' in c for c in calls),
  'native_score_answers':sum(len(c.get('response',{}).get('answers',{})) for c in calls),'ranking_groups':len(rankings),'unique_reference_top':sum(r['unique_reference_top'] for r in rankings),
  'reference_in_top_including_ties':sum(r['reference_in_top_tie'] for r in rankings),'pairwise_reference_wins':sum(r['pairwise_reference_wins'] for r in rankings),'pairwise_reference_ties':sum(r['pairwise_reference_ties'] for r in rankings),
  'pairwise_comparisons':2*len(rankings),'goal_sensitive_bridges':sum(c['matched_above_both'] for c in changes),'goal_sensitive_comparisons':len(changes),
  'rankings':rankings,'counterfactual_objective_changes':changes,
  'usage_totals':{k:sum(c['response']['usage'][k] for c in calls if c.get('response',{}).get('usage',{}).get(k) is not None) if any(c.get('response',{}).get('usage',{}).get(k) is not None for c in calls) else None for k in ('input_tokens','output_tokens','total_tokens')}}

def viewer(out,report):
 e=html.escape;a=report['analysis']
 body='<!doctype html><html lang="it"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>JEV: pertinenza dei bridge verificati</title><style>body{font:16px system-ui;max-width:1100px;margin:2rem auto;padding:1rem;color:#26313d}table{border-collapse:collapse;width:100%;margin:1rem 0}td,th{border:1px solid #ccd;padding:.5rem}pre{white-space:pre-wrap;overflow-wrap:anywhere}img{width:230px;max-width:100%}.note{background:#edf3f7;padding:1rem}details{margin:1rem 0}</style><h1>Bridge validi: quali sono pertinenti?</h1><p>Stato: '+e(report['status'])+'. Tre candidati verificati, tre obiettivi e due presentazioni. Sei richieste da sei Score, massimo 36 risposte. Il codice certifica i binding; Jev valuta la pertinenza.</p>'
 if not a['native_score_answers']:body+='<p class="note">Nessuna risposta Jev disponibile: input preparati, nessun risultato sperimentale.</p>'
 else:body+='<p class="note">Primo posto unico coerente con l’obiettivo: <strong>'+str(a['unique_reference_top'])+'/'+str(a['ranking_groups'])+'</strong>. Confronti con alternative: '+str(a['pairwise_reference_wins'])+'/'+str(a['pairwise_comparisons'])+' vinti, '+str(a['pairwise_reference_ties'])+' pari. Sensibilità al cambio di obiettivo per lo stesso bridge: '+str(a['goal_sensitive_bridges'])+'/'+str(a['goal_sensitive_comparisons'])+'. Riferimento limitato alla preferenza strutturale dichiarata.</p>'
 for replica in range(2):
  sample=next((c for c in report['calls'] if c['replica']==replica),None)
  if not sample:continue
  body+='<h2>Presentazione '+str(replica)+'</h2><p>Gli stessi candidati restano visibili quando cambia l’obiettivo.</p>'
  for asset in sample['asset_audit']:body+='<figure style="display:inline-block;margin:.5rem"><img alt="Candidato o stato iniziale senza risposte" src="'+asset['file']+'"><figcaption>'+e(asset['asset'])+'</figcaption></figure>'
  for r in [r for r in a['rankings'] if r['replica']==replica]:
   label=sample['point_labels'][r['goal_vertex']];body+='<h3>Obiettivo: fan al vertice '+label+' e lato opposto</h3><table><tr><th>Candidato</th><th>Mental Spaces</th><th>Generic Spaces</th><th>Composito</th></tr>'
   for row in r['ranking']:body+='<tr><td>'+row['candidate']+'</td>'+''.join('<td>'+f'{v:.3f}'+'</td>' for v in (row['axis_scores']['mental_spaces'],row['axis_scores']['generic_spaces'],row['composite']))+'</tr>'
   body+='</table>'
 for title,value in [('Analisi e cambio di obiettivo',a),('Limiti',report['limits']),('Input, certificati e risposte sanitizzate',report['calls'])]:body+='<details><summary>'+title+'</summary><pre>'+e(json.dumps(value,indent=2,ensure_ascii=False))+'</pre></details>'
 body+='<p>Pesi fissati: 0,5 Mental Spaces e 0,5 Generic Spaces. I due assi sono correlati. Il riferimento non è una misura universale di creatività né una prova geometrica. Le immagini sono alternative, non una sequenza temporale.</p><p><a href="VERIFIED_RESULTS.md">Relazione e interpretazione</a> · <a href="PROTOCOL.md">Protocollo</a></p></html>'
 (out/'viewer.html').write_text(body,encoding='utf-8')

def save(out,report):
 report['analysis']=analyze(report['calls']);tmp=out/'results.tmp';tmp.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');tmp.replace(out/'results.json');viewer(out,report)

def main(out,live=False):
 if live and (os.getenv('GITHUB_ACTIONS')!='true' or not os.getenv('TYPESAFE_API_KEY')):raise SystemExit('Actions and repository secret required')
 out.mkdir(parents=True,exist_ok=True)
 for name in ('PROTOCOL.md','VERIFIED_RESULTS.md'):
  source=Path(__file__).parent/name
  if source.exists():(out/name).write_text(source.read_text(encoding='utf-8'),encoding='utf-8')
 report={'experiment':'Native relevance scoring of preverified bridges v1','status':'running' if live else 'offline_only','model':'jev-1.14.0','source_commit':os.getenv('GITHUB_SHA'),'run_id':os.getenv('GITHUB_RUN_ID'),'weights':WEIGHTS,'limits':LIMITS,
  'provenance':{'memory_path':str(native.MEMORY_PATH.relative_to(ROOT)),'memory_sha256':hashlib.sha256(native.MEMORY_PATH.read_bytes()).hexdigest(),'historical_templates':[native.ENTRIES[gs] for gs in GS]},'calls':[]}
 events=[(replica,goal) for replica in range(2) for goal in GOALS];random.Random(SEED).shuffle(events)
 for replica,goal in events:
  payload,meta,audit=build_payload(out,replica,goal)
  rec={**meta,'asset_audit':audit,'model_input':{k:v for k,v in payload.items() if k!='assets'},'request_sha256':digest(payload)}
  if live:rec.update(transport(payload))
  report['calls'].append(rec);save(out,report);print('Recorded',len(report['calls']),'/6',flush=True)
  if rec.get('failure') in ('HTTP_400','HTTP_401','HTTP_403'):
   report['status']='request_rejected';save(out,report);raise SystemExit('Request rejected; sanitized artifact saved')
 report['status']='completed_with_failures' if any('failure' in c for c in report['calls']) else 'completed' if live else 'offline_only';save(out,report)
 if report['status']=='completed_with_failures':raise SystemExit('Sanitized failures recorded')

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,default=Path('output_verified_bridge_relevance'));ap.add_argument('--live',action='store_true');args=ap.parse_args();main(args.out,args.live)

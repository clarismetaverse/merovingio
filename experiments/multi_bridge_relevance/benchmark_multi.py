"""Independent native scores against objective-dependent sets and partial orders."""
from __future__ import annotations
import argparse,base64,copy,hashlib,html,itertools,json,math,os,random,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'experiments/verified_bridge_relevance'))
import benchmark_relevance as base

METHODS=base.METHODS
AXES=base.AXES
WEIGHTS=base.WEIGHTS
GOALS=('intact_anchor','unanchored_decomposition','exchangeable_views')
DELTA=.10
MIN_USEFUL=2/3
SENSITIVITY_DELTAS=(.05,.10,.15)
SEED=2026102302
RAW_POINTS={'A':[-110,75],'B':[110,75],'C':[0,-65],'D':[0,75],'E':[55,5],'F':[-55,5]}
LEVELS={
 'mental_spaces':[
  'The admissible bridge contributes no relevant organization of the active aspects for this objective.',
  'It supports a general decomposition, but the particular comparison or preserved aspect requested by the objective is absent.',
  'It supports part of the requested comparison or preservation, with a relevant aspect left only indirectly represented.',
  'It fully supports the requested organization of the active aspects. Other candidates may support it equally well.'],
 'generic_spaces':[
  'The certified Generic Space patterns provide no useful organization for the stated comparison.',
  'They organize a valid partition but omit the feature needed for the requested comparison.',
  'They organize part of the requested comparison, leaving another required feature only indirectly supported.',
  'Their certified instantiation organizes the full requested comparison. This level does not require superiority over other candidates.']}
LIMITS=[
 '36 native Score answers: three candidates, two axes, three objectives, two presentations of ONE isosceles host. Six requests of six questions.',
 'Every candidate satisfies both historical local GS contracts. Material checks, metric facts and reflection equivalence are computed before live requests.',
 'The reference is a partial order with useful sets of sizes two, three and one. No unique winner is required and equivalence classes are observer-only.',
 'The intact-anchor and exchange objectives are indirect task descriptions. The broad unanchored objective is an all-useful control, not an open-ended creativity test.',
 'Reference usefulness follows explicit preservation/comparison policies and supplied certified facts. No independent human usefulness ratings or theorem proof are supplied.',
 'Two candidates are related by a certified reflection of the same host. All three are equivalent only under the broad structural objective, which explicitly ignores vertex, side, size and orientation.',
 'Within each presentation only active_objective changes. Across presentations the same host is rotated/reflected and aliases/order change. These are correlated synthetic trials.',
 'The raw scores are unchanged. Equal weights are fixed. Practical equivalence uses a predeclared normalized gap .10; it is an engineering tolerance, not a statistical equivalence test.',
 'The downstream illustrative set policy keeps scores >= 2/3 within .10 of the maximum; empty and multi-element outputs are allowed. It is not calibrated for deployment. Sensitivity .05/.10/.15 is predeclared and all settings are reported.',
 'Two semantic scoring axes are correlated. No post-hoc thresholds, retries, forced choice or repairs. No proof, autonomous visual extraction, free discovery or internal sequential reasoning claim.']

def objects_for(method,replica):
 objects=base.objects_for(method,0);angle,reflection=base.TRANSFORMS[replica];r=math.radians(angle)
 for name,obj in objects.items():
  if obj['type']=='point':
   x,y=RAW_POINTS[name];obj['xy']=[round(160+reflection*x*math.cos(r)-y*math.sin(r),8),round(160+reflection*x*math.sin(r)+y*math.cos(r),8)]
 return objects

def side_profile(objects,region):
 points=base.checker.polygon(objects,region)
 return sorted(math.dist(points[i],points[(i+1)%len(points)]) for i in range(len(points)))

def metric_facts(objects):
 profiles=[side_profile(objects,objects['REGION_'+str(i)]) for i in range(2)]
 return {'region_areas':[base.checker.area(base.checker.polygon(objects,objects['REGION_'+str(i)])) for i in range(2)],
  'region_side_length_profiles':profiles,'region_pair_congruent_by_computed_side_lengths':all(abs(a-b)<1e-6 for a,b in zip(*profiles)),
  'status':'Certified numerical relations of this explicit synthetic coordinate fixture, not a theorem inferred from pixels.'}

def certificate(objects):
 cert=base.certificate(objects);cert['verified_metric_facts']=metric_facts(objects)
 cert['verification_scope']='Local material boundary-use, convex partition and explicit-coordinate metric checks; no general theorem or equality transfer.'
 return cert

def mirror_equivalent(first,second):
 # Reflection about the apex/base-midpoint line, computed in the presented world frame.
 p=first['C']['xy'];a=first['A']['xy'];b=first['B']['xy'];origin=[(a[i]+b[i])/2 for i in (0,1)]
 direction=[p[i]-origin[i] for i in (0,1)];length=math.hypot(*direction);u=[v/length for v in direction]
 mapping={'A':'B','B':'A','C':'C','D':'D','E':'F','F':'E'}
 for name,obj in first.items():
  if obj['type']!='point':continue
  v=[obj['xy'][i]-origin[i] for i in (0,1)];projection=sum(v[i]*u[i] for i in (0,1))
  reflected=[origin[i]+2*u[i]*projection-v[i] for i in (0,1)]
  if mapping[name] not in second or math.dist(reflected,second[mapping[name]]['xy'])>1e-6:return False
 if {mapping[v] for v in first['BRIDGE']['endpoints']}!=set(second['BRIDGE']['endpoints']):return False
 faces=lambda o:{frozenset(o['REGION_'+str(i)]['vertices']) for i in range(2)}
 return {frozenset(mapping[v] for v in f) for f in faces(first)}==faces(second)

def useful(objects,goal):
 certificate(objects)
 if goal=='intact_anchor':return any({'A','B'}<=set(objects['REGION_'+str(i)]['vertices']) for i in range(2))
 if goal=='unanchored_decomposition':return True # Both checked GS contracts exactly supply this objective.
 if goal=='exchangeable_views':return metric_facts(objects)['region_pair_congruent_by_computed_side_lengths'] and mirror_equivalent(objects,objects)
 raise ValueError('unknown_objective')

def reference(replica,goal):
 objects={m:objects_for(m,replica) for m in METHODS}
 if not mirror_equivalent(objects['from_A'],objects['from_B']):raise ValueError('reflection_equivalence_not_certified')
 yes=[m for m,o in objects.items() if useful(o,goal)];no=[m for m in METHODS if m not in yes]
 tiers=[yes]+([no] if no else [])
 if goal=='unanchored_decomposition':
  signatures=[(len([v for v in o.values() if v['type']=='region']),tuple(sorted(len(o['REGION_'+str(i)]['vertices']) for i in range(2))),len(certificate(o)['generic_space_bindings'])) for o in objects.values()]
  assert len(set(signatures))==1
 return {'useful_methods':yes,'tiers':tiers,'equivalent_pairs':[list(p) for tier in tiers for p in itertools.combinations(tier,2)],
  'strict_pairs':[[a,b] for i,tier in enumerate(tiers) for lower in tiers[i+1:] for a in tier for b in lower],
  'equivalence_evidence':'Host reflection certifies the two base-end cuts. The unanchored objective quotients out all original vertex/side and metric distinctions.'}

def objective(goal,labels):
 if goal=='intact_anchor':
  refs=['side_'+labels['C'],'fan_'+labels['A'],'fan_'+labels['B']]
  description='Prepare a later comparison using a subfigure that retains the entire designated reference side as one intact anchor. The two ends of that reference side are interchangeable; no endpoint and no size balance is preferred.'
 elif goal=='unanchored_decomposition':
  refs=list('fan_'+labels[v] for v in 'ABC')
  description='Organize the host as two adjacent triangular views through their common material interface. Leave the choice of original vertex or side open; size balance, angle, orientation and location do not matter for this schematic comparison.'
 elif goal=='exchangeable_views':
  refs=['side_'+labels['C'],'fan_'+labels['C']]
  description='Prepare two subfigure views that can exchange their places under a symmetry of the fixed host without changing their metric shapes. A valid partition alone does not complete this comparison; use the certified metric facts.'
 else:raise ValueError('unknown_objective')
 return {'mental_space_refs':refs,'designated_reference_side':[labels['A'],labels['B']],'description':description}

def build_payload(out,replica,goal):
 if replica not in range(2) or goal not in GOALS:raise ValueError('unknown_cell')
 payload,old,audit=base.build_payload(out,replica,'A');labels=old['point_labels'];gs_alias=old['gs_aliases'];certs={}
 for candidate,method in old['candidate_mapping'].items():
  objects=objects_for(method,replica);cert=certificate(objects);certs[candidate]=cert
  cert=base.checker.rename(cert,{**labels,**gs_alias,'BRIDGE':'S_'+candidate,'HOST':'host','REGION_0':'R_'+candidate+'_1','REGION_1':'R_'+candidate+'_2'})
  cert['generic_space_bindings']={gs_alias[k]:v for k,v in cert['generic_space_bindings'].items()}
  payload['state']['admissible_bridges'][candidate]['verified_certificate']=cert
  image='image_'+candidate;asset=next(a for a in audit if a['asset']==image)
  base.render(objects,labels,out/asset['file'])
 initial=next(a for a in audit if a['asset']=='initial');base.render(objects_for(METHODS[0],replica),labels,out/initial['file'],False)
 for asset in audit:
  data=(out/asset['file']).read_bytes();asset['sha256']=hashlib.sha256(data).hexdigest();payload['assets'][asset['asset']]['data_base64']=base64.b64encode(data).decode('ascii')
 state=payload['state'];state['active_objective']=objective(goal,labels)
 state['certified_host_facts']={'designated_reference_side':[labels['A'],labels['B']],
  'other_two_original_sides_have_equal_length':True,'status':'Verified from explicit coordinates; no metric relation is inferred from the images.'}
 a,b,c=(objects_for(METHODS[0],replica)[v]['xy'] for v in 'ABC')
 assert abs(math.dist(a,c)-math.dist(b,c))<1e-6
 state['evidence_policy']='All candidates pass both historical local GS contracts. Inline material and metric facts are already checked by code. Rate relevance to the objective. Independently high or equal ratings for several candidates are allowed; there is no score budget and no requirement for a unique winner.'
 for q,question in payload['questions'].items():
  axis=old['question_metadata'][q]['axis'];question['criteria']=LEVELS[axis]
  question['instructions']['task']='Rate relevance to the active aspects for the current objective.' if axis=='mental_spaces' else 'Rate how useful the certified Generic Space instantiations are for organizing the stated comparison, using the certified material and metric facts. Validity alone is not this score.'
  question['instructions']['policy']='Score this candidate independently. Several or all candidates may deserve the same high level. Do not break ties for novelty, orientation, labels, position or an unspecified preference.'
 observer={'replica':replica,'goal':goal,'candidate_mapping':old['candidate_mapping'],'point_labels':labels,'gs_aliases':gs_alias,'question_metadata':old['question_metadata'],
  'geometry_certificates':certs,'reference':reference(replica,goal)}
 return payload,observer,audit

def select_set(scores,delta=DELTA):
 if not scores:return []
 maximum=max(scores.values())
 return sorted(m for m,v in scores.items() if v+1e-9>=MIN_USEFUL and maximum-v<=delta+1e-9)

def assess(scores,ref,delta=DELTA):
 expected=set(ref['useful_methods']);selected=set(select_set(scores,delta))
 equivalent=[{'methods':pair,'useful_pair':all(m in expected for m in pair),'gap':abs(scores[pair[0]]-scores[pair[1]]),'within_band':abs(scores[pair[0]]-scores[pair[1]])<=delta+1e-9} for pair in ref['equivalent_pairs']]
 strict=[{'methods':pair,'margin':scores[pair[0]]-scores[pair[1]],'win':scores[pair[0]]>scores[pair[1]]+1e-9,'tie':abs(scores[pair[0]]-scores[pair[1]])<=1e-9,'separated_by_band':scores[pair[0]]-scores[pair[1]]>delta+1e-9} for pair in ref['strict_pairs']]
 return {'delta':delta,'expected_methods':sorted(expected),'selected_methods':sorted(selected),'exact_set_match':selected==expected,
  'tp':len(expected&selected),'fp':len(selected-expected),'fn':len(expected-selected),'empty_set':not selected,
  'spurious_unique_set':len(expected)>1 and len(selected)==1,'equivalent_pairs':equivalent,'strict_pairs':strict,
  'useful_group_spread':max(scores[m] for m in expected)-min(scores[m] for m in expected)}

def analyze(calls):
 groups=[]
 for call in calls:
  if not call.get('response'):continue
  axes={c:{} for c in call['candidate_mapping']}
  for q,answer in call['response']['answers'].items():
   meta=call['question_metadata'][q];axes[meta['candidate']][meta['axis']]=answer['normalized_score']
  rows=[{'candidate':c,'method':m,'axis_scores':axes[c],'composite':base.native.weighted(axes[c],WEIGHTS)} for c,m in call['candidate_mapping'].items()]
  scores={r['method']:r['composite'] for r in rows};maximum=max(scores.values())
  groups.append({'replica':call['replica'],'goal':call['goal'],'ranking':sorted(rows,key=lambda r:-r['composite']),
   'raw_argmax_methods':[m for m,v in scores.items() if abs(v-maximum)<1e-9],
   **assess(scores,call['reference']),
   'by_axis':{a:assess({r['method']:r['axis_scores'][a] for r in rows},call['reference']) for a in AXES},
   'sensitivity':{str(d):assess(scores,call['reference'],d) for d in SENSITIVITY_DELTAS}})
 eq=[p for g in groups for p in g['equivalent_pairs']];strict=[p for g in groups for p in g['strict_pairs']]
 return {'api_calls_attempted':sum('response' in c or 'failure' in c for c in calls),'api_failures':sum('failure' in c for c in calls),
  'native_score_answers':sum(len(c.get('response',{}).get('answers',{})) for c in calls),'groups':len(groups),'exact_set_matches':sum(g['exact_set_match'] for g in groups),
  'equivalent_pairs_in_band':sum(p['within_band'] for p in eq),'equivalent_pairs_total':len(eq),
  'useful_equivalent_pairs_in_band':sum(p['within_band'] for p in eq if p['useful_pair']),'useful_equivalent_pairs_total':sum(p['useful_pair'] for p in eq),
  'strict_preference_wins':sum(p['win'] for p in strict),'strict_preference_ties':sum(p['tie'] for p in strict),
  'strict_preference_total':len(strict),'strict_separated_by_band':sum(p['separated_by_band'] for p in strict),'spurious_unique_sets':sum(g['spurious_unique_set'] for g in groups),
  'empty_sets':sum(g['empty_set'] for g in groups),'set_matrix':{k:sum(g[k] for g in groups) for k in ('tp','fp','fn')},
  'sensitivity':{str(d):{'exact_set_matches':sum(g['sensitivity'][str(d)]['exact_set_match'] for g in groups),
   'equivalent_pairs_in_band':sum(p['within_band'] for g in groups for p in g['sensitivity'][str(d)]['equivalent_pairs']),
   'spurious_unique_sets':sum(g['sensitivity'][str(d)]['spurious_unique_set'] for g in groups)} for d in SENSITIVITY_DELTAS},
  'observations':groups,'usage_totals':{k:sum(c['response']['usage'][k] for c in calls if c.get('response',{}).get('usage',{}).get(k) is not None) if any(c.get('response',{}).get('usage',{}).get(k) is not None for c in calls) else None for k in ('input_tokens','output_tokens','total_tokens')}}

def viewer(out,report):
 e=html.escape;a=report['analysis']
 body='<!doctype html><html lang="it"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Più bridge utili e equivalenze</title><style>body{font:16px system-ui;max-width:1100px;margin:2rem auto;padding:1rem;color:#26313d}table{border-collapse:collapse;width:100%;margin:1rem 0}td,th{border:1px solid #ccd;padding:.5rem}pre{white-space:pre-wrap;overflow-wrap:anywhere}img{width:230px;max-width:100%}details{margin:1rem 0}.note{background:#edf3f7;padding:1rem}</style><h1>Pertinenza senza vincitore unico</h1><p>Stato: '+e(report['status'])+'. Tre bridge verificati, obiettivi con due, tre o un’alternativa utile. Due presentazioni dello stesso triangolo isoscele; 36 Score al massimo.</p>'
 if not a['native_score_answers']:body+='<p class="note">Nessuna risposta JEV: input preparati, nessun risultato da interpretare.</p>'
 else:body+='<p class="note">Insiemi della policy coincidenti col riferimento: '+str(a['exact_set_matches'])+'/'+str(a['groups'])+'. Equivalenze fra bridge utili nella fascia: '+str(a['useful_equivalent_pairs_in_band'])+'/'+str(a['useful_equivalent_pairs_total'])+'; incluse le alternative inferiori: '+str(a['equivalent_pairs_in_band'])+'/'+str(a['equivalent_pairs_total'])+'. Preferenze strette rispettate: '+str(a['strict_preference_wins'])+'/'+str(a['strict_preference_total'])+'. Riduzioni a un solo candidato nei casi multipli: '+str(a['spurious_unique_sets'])+'.</p>'
 body+='<p>Policy fissata prima della prova: composito 0,5/0,5; fascia δ=0,10; livello minimo 2/3. Insiemi vuoti e multipli sono ammessi. La fascia è una tolleranza pratica, non una prova statistica di equivalenza. Nessuno Score nativo viene corretto. Le tabelle sono ordinate per score per facilitarne la lettura: il primo elemento non diventa automaticamente una scelta unica.</p>'
 titles={'intact_anchor':'Un lato conservato come riferimento','unanchored_decomposition':'Decomposizione senza vertice privilegiato','exchangeable_views':'Sottofigure scambiabili nella figura ospite'}
 for replica in range(2):
  sample=next((c for c in report['calls'] if c['replica']==replica),None)
  if not sample:continue
  body+='<h2>Presentazione '+str(replica)+'</h2>'
  for asset in sample['asset_audit']:body+='<figure style="display:inline-block;margin:.5rem"><img alt="Figura o bridge, senza risposte" src="'+asset['file']+'"><figcaption>'+e(asset['asset'])+'</figcaption></figure>'
  inverse={m:c for c,m in sample['candidate_mapping'].items()}
  for g in [g for g in a['observations'] if g['replica']==replica]:
   body+='<h3>'+titles[g['goal']]+'</h3><p>Insieme di riferimento: '+', '.join(inverse[m] for m in g['expected_methods'])+'. Insieme della policy: '+(', '.join(inverse[m] for m in g['selected_methods']) or 'vuoto')+'.</p><table><tr><th>Candidato</th><th>Mental Spaces</th><th>Generic Spaces</th><th>Composito</th></tr>'
   for row in g['ranking']:body+='<tr><td>'+row['candidate']+'</td>'+''.join('<td>'+f'{v:.3f}'+'</td>' for v in (row['axis_scores']['mental_spaces'],row['axis_scores']['generic_spaces'],row['composite']))+'</tr>'
   body+='</table>'
 for title,value in [('Equivalenze, ordini parziali e sensibilità',a),('Limiti',report['limits']),('Input, certificati e risposte native',report['calls'])]:body+='<details><summary>'+title+'</summary><pre>'+e(json.dumps(value,indent=2,ensure_ascii=False))+'</pre></details>'
 body+='<p><a href="VERIFIED_RESULTS.md">Relazione verificata</a> · <a href="PROTOCOL.md">Protocollo</a></p></html>';(out/'viewer.html').write_text(body,encoding='utf-8')

def save(out,report):
 report['analysis']=analyze(report['calls']);tmp=out/'results.tmp';tmp.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');tmp.replace(out/'results.json');viewer(out,report)

def main(out,live=False):
 if live and (os.getenv('GITHUB_ACTIONS')!='true' or not os.getenv('TYPESAFE_API_KEY')):raise SystemExit('Actions and repository secret required')
 out.mkdir(parents=True,exist_ok=True)
 for name in ('PROTOCOL.md','VERIFIED_RESULTS.md'):
  p=Path(__file__).parent/name
  if p.exists():(out/name).write_text(p.read_text(encoding='utf-8'),encoding='utf-8')
 report={'experiment':'Multiple useful bridges and objective-relative equivalence v1','status':'running' if live else 'offline_only','model':'jev-1.14.0','source_commit':os.getenv('GITHUB_SHA'),'run_id':os.getenv('GITHUB_RUN_ID'),
  'weights':WEIGHTS,'set_policy':{'delta':DELTA,'min_useful':MIN_USEFUL,'sensitivity_deltas':SENSITIVITY_DELTAS},'limits':LIMITS,
  'provenance':{'memory_path':base.native.MEMORY_PATH.relative_to(ROOT).as_posix(),'memory_sha256':hashlib.sha256(base.native.MEMORY_PATH.read_bytes()).hexdigest(),'historical_templates':[base.native.ENTRIES[g] for g in base.GS]},'calls':[]}
 events=[(r,g) for r in range(2) for g in GOALS];random.Random(SEED).shuffle(events)
 for replica,goal in events:
  p,meta,audit=build_payload(out,replica,goal);rec={**meta,'asset_audit':audit,'model_input':{k:v for k,v in p.items() if k!='assets'},'request_sha256':base.digest(p)}
  if live:rec.update(base.transport(p))
  report['calls'].append(rec);save(out,report);print('Recorded',len(report['calls']),'/6',flush=True)
  if rec.get('failure') in ('HTTP_400','HTTP_401','HTTP_403'):
   report['status']='request_rejected';save(out,report);raise SystemExit('Rejected request; sanitized artifact saved')
 report['status']='completed_with_failures' if any('failure' in c for c in report['calls']) else 'completed' if live else 'offline_only';save(out,report)
 if report['status']=='completed_with_failures':raise SystemExit('Sanitized failures recorded')

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,default=Path('output_multi_bridge_relevance'));ap.add_argument('--live',action='store_true');args=ap.parse_args();main(args.out,args.live)

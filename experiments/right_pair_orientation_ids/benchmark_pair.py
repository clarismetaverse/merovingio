"""Fresh isolated-pair baseline and crossed orientation/opaque-ID interventions."""
from __future__ import annotations
import argparse,base64,copy,hashlib,html,json,math,os,random,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'experiments/intact_side_new_figures'))
import benchmark_new as prior
native=prior.previous
base=prior.base
HERE=Path(__file__).parent
SOURCE=json.loads((prior.HERE/'live_results.json').read_text(encoding='utf-8'))
assert SOURCE['run_id']=='39994076040' and SOURCE['status']=='completed'
OLD=next(c for c in SOURCE['calls'] if c['figure']=='right_scalene')
METHODS=('B_to_near_C','C_to_near_B')
PAIR={c:m for c,m in OLD['candidate_mapping'].items() if m in METHODS}
assert PAIR=={'C914':METHODS[0],'C850':METHODS[1]}
CELLS={'original':(False,False),'orientation_only':(True,False),'ids_only':(False,True),'orientation_and_ids':(True,True)}
TITLES={'original':'Coppia isolata, originale','orientation_only':'Sola rotazione','ids_only':'Soli ID nuovi','orientation_and_ids':'Rotazione + ID nuovi'}
SEED=2026102306
LIMITS=[
 'Eight new native Noul judgments in four requests of two questions: a fresh isolated-pair baseline and a 2x2 orientation-by-ID design. One positive and one negative per cell; no Score, composite, coverage table, retry or extra question.',
 'Only the previously wrong right-triangle pair C914/C850 is retained. Removing two candidates, their images and their questions is COMMON to all four new cells. The fresh baseline is not an exact repeat of the old four-candidate context.',
 'The original baseline reuses archived PNG bytes and the exact remaining state/certificates/questions. Across orientation only PNG bytes change: undo the 51-degree rotation about (160,160), retaining reflection, scale, center, labels and all structured facts.',
 'The ID intervention is a single fixed bijection of point, candidate, material-carrier, region, Mental/Generic Space and derived candidate-image identifiers. It changes corresponding diagram labels and structured references together. Semantic role/type/predicate names, host context ID, initial-image ID and question IDs are unchanged.',
 'ID changes therefore test displayed and structured naming jointly, not text-only ID comparison. The same bijection is used at both orientations; order and role-to-object incidence never change. Point glyph widths may differ under the same font/size.',
 'All eight candidate instances pass both historical material contracts and the same observer-side preservation predicate. Positive/negative geometry is unchanged up to a rigid rotation; no new bridge, metric premise or coverage fact is introduced.',
 'Fixed p>.5=yes, p<.5=no, p=.5=abstention counted incorrect. Report per-cell matrices, raw probabilities, positive-minus-negative margins and descriptive crossed contrasts. A contrast is a difference between probabilities, not a composite relevance score.',
 'One preselected failed pair, one new orientation and one ID permutation, one response per cell. No replication or statistical causal estimate; context reduction, API variation and selection of a previous failure limit historical comparisons.',
 'Images and structured facts remain together. Rotating an image also changes rasterization and locations of labels; this does not isolate an internal visual algorithm, proof, autonomous binding or sequential reasoning.'
]

def id_bijection():
 rng=random.Random(SEED);old_labels=OLD['point_labels']
 point_map=dict(zip(old_labels.values(),rng.sample([c for c in 'ABCDEFGHJKLMNPQRSTUVWXYZ' if c not in old_labels.values()],7)))
 candidate_map=dict(zip(PAIR,['C'+str(n) for n in rng.sample([n for n in range(100,999) if 'C'+str(n) not in OLD['candidate_mapping']],2)]))
 old_gs=list(OLD['model_input']['state']['generic_spaces'])
 gs_map=dict(zip(old_gs,['H'+str(n) for n in rng.sample([n for n in range(100,999) if 'H'+str(n) not in old_gs],2)]))
 mapping={**point_map,**candidate_map,**gs_map}
 for old,new in candidate_map.items():
  mapping['S_'+old]='S_'+new;mapping['image_'+old]='image_'+new
  for index in (1,2):mapping['R_'+old+'_'+str(index)]='R_'+new+'_'+str(index)
 for old in OLD['model_input']['state']['mental_spaces']:
  prefix,point=old.rsplit('_',1);mapping[old]=prefix+'_'+point_map[point]
 assert len(mapping)==len(set(mapping.values())) and not set(mapping)&set(mapping.values())
 return mapping

ID_MAP=id_bijection()

def rename(value,mapping):
 if isinstance(value,str):return mapping.get(value,value)
 if isinstance(value,list):return [rename(v,mapping) for v in value]
 if isinstance(value,dict):return {mapping.get(k,k):rename(v,mapping) for k,v in value.items()}
 return value

def labels_for(new_ids):return {k:ID_MAP[v] if new_ids else v for k,v in OLD['point_labels'].items()}

def objects_for(method,rotated):
 objects=prior.objects_for('right_scalene',method)
 if rotated:
  angle=math.radians(-51);co,si=math.cos(angle),math.sin(angle)
  for obj in objects.values():
   if obj['type']=='point':
    x,y=[v-160 for v in obj['xy']];obj['xy']=[round(160+x*co-y*si,8),round(160+x*si+y*co,8)]
 return objects

def isolated_input():
 p=copy.deepcopy(OLD['model_input']);p['assets']={}
 for asset in OLD['asset_audit']:
  data=(prior.HERE/'fixtures'/asset['file']).read_bytes();assert hashlib.sha256(data).hexdigest()==asset['sha256']
  p['assets'][asset['asset']]={'type':'image','format':'png','data_base64':base64.b64encode(data).decode('ascii')}
 assert base.digest(p)==OLD['request_sha256'] # Reconstruct the full actual historical request first.
 p['state']['admissible_bridges']={c:v for c,v in p['state']['admissible_bridges'].items() if c in PAIR}
 p['questions']={q:v for q,v in p['questions'].items() if OLD['question_metadata'][q]['candidate'] in PAIR}
 keep={'initial'}|{'image_'+c for c in PAIR}
 p['assets']={k:v for k,v in p['assets'].items() if k in keep}
 return p

def freeze_fixtures():
 manifest={'seed':SEED,'source_request_sha256':OLD['request_sha256'],'id_bijection':ID_MAP,'cells':{}}
 for cell,(rotated,new_ids) in CELLS.items():
  assets=[];labels=labels_for(new_ids)
  for candidate,method in list(PAIR.items())+[(None,METHODS[0])]:
   asset='image_'+(ID_MAP[candidate] if new_ids else candidate) if candidate else 'initial'
   relative=Path('images')/cell/(asset+'.png');path=HERE/'fixtures'/relative;path.parent.mkdir(parents=True,exist_ok=True)
   if not rotated and not new_ids:
    source=next(a for a in OLD['asset_audit'] if a['asset']==('image_'+candidate if candidate else 'initial'))
    path.write_bytes((prior.HERE/'fixtures'/source['file']).read_bytes())
   else:base.render(objects_for(method,rotated),labels,path,bridge=candidate is not None)
   assets.append({'asset':asset,'file':relative.as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
  manifest['cells'][cell]={'asset_audit':assets,'geometry_sha256':{m:base.digest(objects_for(m,rotated)) for m in METHODS}}
 (HERE/'fixtures/manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8',newline='\n')

def fixture_hash():return hashlib.sha256((HERE/'fixtures/manifest.json').read_bytes().replace(b'\r\n',b'\n')).hexdigest()

def historical_probabilities():
 return {OLD['candidate_mapping'][OLD['question_metadata'][q]['candidate']]:answer['noul'] for q,answer in OLD['response']['answers'].items() if OLD['question_metadata'][q]['candidate'] in PAIR}

def build_payload(out,cell):
 rotated,new_ids=CELLS[cell];p=isolated_input();p['assets']={}
 if new_ids:p=rename(p,ID_MAP)
 manifest=json.loads((HERE/'fixtures/manifest.json').read_text(encoding='utf-8'))
 assert manifest['id_bijection']==ID_MAP and manifest['source_request_sha256']==OLD['request_sha256']
 frozen=manifest['cells'][cell];audit=copy.deepcopy(frozen['asset_audit'])
 for asset in audit:
  data=(HERE/'fixtures'/asset['file']).read_bytes();assert hashlib.sha256(data).hexdigest()==asset['sha256']
  path=out/asset['file'];path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
  p['assets'][asset['asset']]={'type':'image','format':'png','data_base64':base64.b64encode(data).decode('ascii')}
 mapping={(ID_MAP[c] if new_ids else c):m for c,m in PAIR.items()};gold={};checks={}
 for candidate,method in mapping.items():
  objects=objects_for(method,rotated);assert base.digest(objects)==frozen['geometry_sha256'][method]
  checks[candidate]=native.prior.certificate(objects);gold[candidate]=prior.reference(objects)[0]
 meta={q:{'candidate':question['instructions']['candidate_ref']} for q,question in p['questions'].items()}
 observer={'cell':cell,'replica':list(CELLS).index(cell),'condition':'explicit','rotated':rotated,'new_ids':new_ids,'candidate_mapping':mapping,'point_labels':labels_for(new_ids),'question_metadata':meta,'reference':gold,'observer_material_certificates':checks}
 return p,observer,audit

def analyze(calls):
 a=native.analyze(calls);rows=a['observations'];cells={}
 for cell in CELLS:
  call=next((c for c in calls if c['cell']==cell and c.get('response')),None)
  if not call:continue
  rr={r['method']:r for r in rows if r['replica']==call['replica']};pos,neg=(rr[m] for m in METHODS)
  cells[cell]={'summary':native.analyze([call])['by_condition']['explicit'],'p_positive':pos['p_yes'],'p_negative':neg['p_yes'],'margin':pos['p_yes']-neg['p_yes'],
   'both_correct':pos['correct'] and neg['correct'],'strict_order':pos['p_yes']>neg['p_yes'],'both_wrong_nonabstaining':all(r['decision'] is not None and not r['correct'] for r in (pos,neg))}
 effects={}
 for name,first,second in [('orientation_at_old_ids','original','orientation_only'),('ids_at_old_orientation','original','ids_only'),('orientation_at_new_ids','ids_only','orientation_and_ids'),('ids_at_new_orientation','orientation_only','orientation_and_ids')]:
  if first in cells and second in cells:effects[name]={key:cells[second][key]-cells[first][key] for key in ('p_positive','p_negative','margin')}
 interaction=cells['orientation_and_ids']['margin']-cells['orientation_only']['margin']-cells['ids_only']['margin']+cells['original']['margin'] if len(cells)==4 else None
 return {k:a[k] for k in ('api_calls_attempted','api_failures','native_noul_answers','usage_totals')}|{'overall':a['by_condition']['explicit'],'cells':cells,'observations':rows,'descriptive_contrasts':effects,'margin_interaction':interaction,
  'historical_two_errors_reproduced_in_isolated_baseline':cells.get('original',{}).get('both_wrong_nonabstaining')}

def viewer(out,r):
 e=html.escape;a=r['analysis'];historical=r['historical_context']['p_yes_by_method']
 body='<!doctype html><html lang="it"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>JEV — coppia rettangolo: orientazione e ID</title><style>body{font:16px system-ui;max-width:1150px;margin:2rem auto;padding:1rem;color:#26313d}table{border-collapse:collapse;width:100%;margin:1rem 0}td,th{border:1px solid #ccd;padding:.5rem}pre{white-space:pre-wrap;overflow-wrap:anywhere}img{width:250px;max-width:100%}details{margin:1rem 0}.note{background:#edf3f7;padding:1rem}</style><h1>Coppia isolata: orientazione × ID</h1><p>Stato: '+e(r['status'])+'. Quattro richieste di due Noul, massimo otto giudizi; nessuna copertura o composito.</p><p class="note">Storico, con quattro candidati: positivo '+str(historical[METHODS[0]])+', negativo '+str(historical[METHODS[1]])+'. Il nuovo baseline ha solo due candidati: deve essere letto prima di attribuire cambiamenti a rotazione o ID. Riflessione, geometria, richiesta esplicita e ordine restano fissi.</p>'
 if not a['native_noul_answers']:body+='<p>Nessun risultato nuovo: preparazione offline.</p>'
 body+='<table><tr><th>Versione</th><th>P(sì) positivo</th><th>P(sì) negativo</th><th>Margine</th><th>Corretti</th></tr>'
 for cell in CELLS:
  row=a['cells'].get(cell);body+='<tr><td>'+TITLES[cell]+'</td>'
  body+=''.join('<td>'+f'{row[k]:.3f}'+'</td>' for k in ('p_positive','p_negative','margin'))+'<td>'+str(row['summary']['correct'])+'/2</td></tr>' if row else '<td colspan="4">non disponibile</td></tr>'
 body+='</table>'
 for cell in CELLS:
  call=next((c for c in r['calls'] if c['cell']==cell),None)
  if not call:continue
  body+='<h2>'+TITLES[cell]+'</h2><p>Lato designato: '+e('–'.join(call['model_input']['state']['active_objective']['designated_reference_side']))+'</p>'
  for asset in call['asset_audit']:
   candidate=asset['asset'][6:] if asset['asset'].startswith('image_') else None
   caption=asset['asset']+(' — riferimento: '+('sì' if call['reference'][candidate] else 'no') if candidate else '')
   body+='<figure style="display:inline-block;margin:.5rem"><img alt="Bridge originale o ruotato, soli ID neutri" src="'+asset['file']+'"><figcaption>'+e(caption)+'</figcaption></figure>'
 for title,value in [('Matrici e contrasti descrittivi',a),('Limiti',r['limits']),('Input, certificati observer e risposte native',r['calls'])]:body+='<details><summary>'+title+'</summary><pre>'+e(json.dumps(value,indent=2,ensure_ascii=False))+'</pre></details>'
 body+='<p><a href="PROTOCOL.md">Protocollo</a> · <a href="VERIFIED_RESULTS.md">Relazione verificata</a></p><p>Una coppia preselezionata, nessuna replicazione: non è una prova geometrica o di ragionamento sequenziale interno.</p></html>';(out/'viewer.html').write_text(body,encoding='utf-8')

def save(out,report):
 report['analysis']=analyze(report['calls']);tmp=out/'results.tmp';tmp.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');tmp.replace(out/'results.json');viewer(out,report)

def main(out,live=False):
 if live and (os.getenv('GITHUB_ACTIONS')!='true' or not os.getenv('TYPESAFE_API_KEY')):raise SystemExit('Actions and repository secret required')
 out.mkdir(parents=True,exist_ok=True)
 for name in ('PROTOCOL.md','VERIFIED_RESULTS.md'):
  source=HERE/name
  if source.exists():(out/name).write_text(source.read_text(encoding='utf-8'),encoding='utf-8')
 report={'experiment':'Right-triangle failed pair: orientation and IDs v1','status':'running' if live else 'offline_only','model':'jev-1.14.0','source_commit':os.getenv('GITHUB_SHA'),'run_id':os.getenv('GITHUB_RUN_ID'),
  'decision_policy':{'threshold':.5,'equal_threshold':'abstain_counted_incorrect'},'limits':LIMITS,'historical_context':{'run_id':SOURCE['run_id'],'source_commit':SOURCE['source_commit'],'candidate_count':4,'p_yes_by_method':historical_probabilities()},
  'provenance':{'parent_commit':'cd751d03a0f416ccd27ec21f6091684b62e0a7f9','archived_results_canonical_sha256':base.digest(SOURCE),'source_request_sha256':OLD['request_sha256'],'fixture_manifest_sha256':fixture_hash()},'calls':[]}
 events=list(CELLS);random.Random(SEED).shuffle(events)
 for cell in events:
  p,meta,audit=build_payload(out,cell);record={**meta,'asset_audit':audit,'model_input':{k:v for k,v in p.items() if k!='assets'},'request_sha256':base.digest(p)}
  if live:record.update(native.transport(p))
  report['calls'].append(record);save(out,report);print('Recorded',len(report['calls']),'/4',flush=True)
  if record.get('failure') in ('HTTP_400','HTTP_401','HTTP_403'):
   report['status']='request_rejected';save(out,report);raise SystemExit('Request rejected; sanitized artifact saved')
 report['status']='completed_with_failures' if any('failure' in c for c in report['calls']) else 'completed' if live else 'offline_only';save(out,report)
 if report['status']=='completed_with_failures':raise SystemExit('Sanitized failures recorded')

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,default=Path('output_right_pair_orientation_ids'));ap.add_argument('--live',action='store_true');ap.add_argument('--freeze-fixtures',action='store_true');args=ap.parse_args()
 if args.freeze_fixtures:
  if args.live:raise SystemExit('Freeze offline before live')
  freeze_fixtures()
 else:main(args.out,args.live)

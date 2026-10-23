"""Same failed pair: unchanged monochrome, color alone, color plus identity legend."""
from __future__ import annotations
import argparse,base64,copy,hashlib,html,json,os,random,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'experiments/right_pair_orientation_ids'))
import benchmark_pair as prior
native=prior.native
base=prior.base
HERE=Path(__file__).parent
SOURCE=json.loads((prior.HERE/'live_results.json').read_text(encoding='utf-8'))
assert SOURCE['run_id']=='39996906771' and SOURCE['status']=='completed'
OLD=next(c for c in SOURCE['calls'] if c['cell']=='original')
ARMS=('monochrome','color','color_legend')
TITLES={'monochrome':'Monocromatico, nuova chiamata','color':'Solo colori','color_legend':'Colori + legenda degli ID'}
SEED=2026102307
DARK='#26313d'
SIDE_COLORS={'AB':{'name':'amber','hex':'#E69F00'},'BC':{'name':'blue','hex':'#0072B2'},'CA':{'name':'teal','hex':'#009E73'}}
POINT_COLORS={'A':{'name':'orange_red','hex':'#D55E00'},'B':{'name':'navy','hex':'#225EA8'},'C':{'name':'dark_teal','hex':'#00796B'}}
CONTACT_COLOR={'name':'magenta','hex':'#C13F8A'}
BRIDGE_COLOR={'name':'purple','hex':'#7A3E9D'}
LIMITS=[
 'Six new native Noul judgments in three requests of two questions: an exact monochrome request replay, color-only PNGs, and those SAME colored PNGs plus an object-identity legend. No coverage table, Score, composite, retries or additional questions.',
 'The two original right-triangle bridges, 51-degree orientation/reflection, IDs, order, explicit objective and all material/metric facts remain fixed. Monochrome reuses actual archived PNG bytes and reconstructs the exact prior isolated-baseline request hash.',
 'Color-only modifies RGB values at existing ink locations. Canvas, coordinates, line width, point radius, label text/font/placement, white region interiors and non-white pixel mask remain unchanged. All original sides have stable distinct colors; the same original vertex retains its color in both diagrams.',
 'Both new carriers share purple; both new contact points share magenta. Colors encode original object identity or drawing kind, never candidate validity, goal satisfaction, positive/negative status or a region coverage verdict. No red/green answer marking or region filling.',
 'The legend lists all three original sides, all five visible point IDs and both new material carriers uniformly. It adds color-to-ID associations only, not side membership, coverage, usefulness or any new geometric premise.',
 'Same fixed p>.5=yes, p<.5=no, p=.5=abstention counted incorrect. Report each raw probability, per-arm matrices/Brier, positive-minus-negative margins and matched probability differences. No post-hoc threshold fitting or unique-winner policy.',
 'One preselected pair, one palette, one response per arm. This is a bounded presentation/binding diagnostic, not three independent geometries, statistical attribution, calibrated deployment, proof or autonomous image extraction.',
 'Historical isolated monochrome .67/.51 is context only; the new same-request replay may differ between calls. Images and structured facts remain together. Multiple images are alternative candidates, not evidence of internal sequential reasoning.'
]

def point_color(name):return POINT_COLORS.get(name,CONTACT_COLOR)

def visual_key():
 labels=OLD['point_labels']
 return {'scope':'Colors distinguish object identity or drawing kind. Shared hues do not merge distinct material IDs across alternative candidates. Colors do not encode validity or goal satisfaction.',
  'original_side_colors':[{'mental_space_ref':'side_'+labels[opposite],'endpoints':[labels[v] for v in edge],**SIDE_COLORS[edge]} for edge,opposite in (('AB','C'),('BC','A'),('CA','B'))],
  'point_colors':[{'point_ref':labels[v],**point_color(v)} for v in 'ABCFG'],
  'new_carrier_colors':[{'candidate_ref':candidate,'material_ref':'S_'+candidate,**BRIDGE_COLOR} for candidate in prior.PAIR]}

def render(objects,labels,path,bridge=True,colored=True):
 im=Image.new('RGB',(320,320),'white');d=ImageDraw.Draw(im);xy=lambda k:tuple(objects[k]['xy'])
 for edge in ('AB','BC','CA'):d.line([xy(v) for v in edge],fill=SIDE_COLORS[edge]['hex'] if colored else DARK,width=3)
 names=list('ABC')
 if bridge:
  ends=objects['BRIDGE']['endpoints'];d.line([xy(v) for v in ends],fill=BRIDGE_COLOR['hex'] if colored else DARK,width=3);names+=[v for v in ends if v not in names]
 font=ImageFont.load_default(size=15)
 for name in names:
  x,y=xy(name);d.ellipse((x-3,y-3,x+3,y+3),fill=point_color(name)['hex'] if colored else DARK)
  d.text((x+5,y+3),labels[name],font=font,fill=DARK)
 path.parent.mkdir(parents=True,exist_ok=True);im.save(path)

def archived_input():
 p=copy.deepcopy(OLD['model_input']);p['assets']={}
 for asset in OLD['asset_audit']:
  data=(prior.HERE/'fixtures'/asset['file']).read_bytes();assert hashlib.sha256(data).hexdigest()==asset['sha256']
  p['assets'][asset['asset']]={'type':'image','format':'png','data_base64':base64.b64encode(data).decode('ascii')}
 assert base.digest(p)==OLD['request_sha256']
 return p

def freeze_fixtures():
 manifest={'seed':SEED,'source_request_sha256':OLD['request_sha256'],'visual_key':visual_key(),'arms':{}}
 for arm in ('monochrome','color'):
  audit=[]
  for source in OLD['asset_audit']:
   asset=source['asset'];relative=Path('images')/arm/(asset+'.png');path=HERE/'fixtures'/relative
   if arm=='monochrome':path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes((prior.HERE/'fixtures'/source['file']).read_bytes())
   else:
    candidate=asset[6:] if asset.startswith('image_') else None;method=prior.PAIR[candidate] if candidate else prior.METHODS[0]
    render(prior.objects_for(method,False),OLD['point_labels'],path,bridge=candidate is not None)
   audit.append({'asset':asset,'file':relative.as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
  manifest['arms'][arm]=audit
 manifest['arms']['color_legend']=copy.deepcopy(manifest['arms']['color'])
 (HERE/'fixtures/manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8',newline='\n')

def fixture_hash():return hashlib.sha256((HERE/'fixtures/manifest.json').read_bytes().replace(b'\r\n',b'\n')).hexdigest()

def build_payload(out,arm):
 if arm not in ARMS:raise ValueError('unknown_arm')
 p=archived_input();p['assets']={}
 if arm=='color_legend':p['state']['visual_object_key']=visual_key()
 manifest=json.loads((HERE/'fixtures/manifest.json').read_text(encoding='utf-8'))
 assert manifest['visual_key']==visual_key() and manifest['source_request_sha256']==OLD['request_sha256']
 audit=copy.deepcopy(manifest['arms'][arm])
 for asset in audit:
  data=(HERE/'fixtures'/asset['file']).read_bytes();assert hashlib.sha256(data).hexdigest()==asset['sha256']
  path=out/asset['file'];path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
  p['assets'][asset['asset']]={'type':'image','format':'png','data_base64':base64.b64encode(data).decode('ascii')}
 if arm=='monochrome':assert base.digest(p)==OLD['request_sha256']
 reference={};certificates={}
 for candidate,method in prior.PAIR.items():
  objects=prior.objects_for(method,False);certificates[candidate]=native.prior.certificate(objects);reference[candidate]=prior.prior.reference(objects)[0]
 observer={'arm':arm,'replica':ARMS.index(arm),'condition':'explicit','candidate_mapping':copy.deepcopy(prior.PAIR),'point_labels':OLD['point_labels'],'question_metadata':OLD['question_metadata'],'reference':reference,'observer_material_certificates':certificates}
 return p,observer,audit

def analyze(calls):
 a=native.analyze(calls);rows=a['observations'];arms={}
 for arm in ARMS:
  call=next((c for c in calls if c['arm']==arm and c.get('response')),None)
  if not call:continue
  rr={r['method']:r for r in rows if r['replica']==call['replica']};positive,negative=(rr[m] for m in prior.METHODS)
  arms[arm]={'summary':native.analyze([call])['by_condition']['explicit'],'p_positive':positive['p_yes'],'p_negative':negative['p_yes'],'margin':positive['p_yes']-negative['p_yes'],
   'both_correct':positive['correct'] and negative['correct'],'strict_order':positive['p_yes']>negative['p_yes']}
 contrasts={}
 for first,second in zip(ARMS,ARMS[1:]):
  if first in arms and second in arms:contrasts[first+'_to_'+second]={key:arms[second][key]-arms[first][key] for key in ('p_positive','p_negative','margin')}
 return {k:a[k] for k in ('api_calls_attempted','api_failures','native_noul_answers','usage_totals')}|{'overall':a['by_condition']['explicit'],'arms':arms,'observations':rows,'descriptive_contrasts':contrasts}

def viewer(out,r):
 e=html.escape;a=r['analysis']
 body='<!doctype html><html lang="it"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>JEV — colori e binding visivo</title><style>body{font:16px system-ui;max-width:1150px;margin:2rem auto;padding:1rem;color:#26313d}table{border-collapse:collapse;width:100%;margin:1rem 0}td,th{border:1px solid #ccd;padding:.5rem}pre{white-space:pre-wrap;overflow-wrap:anywhere}img{width:250px;max-width:100%}details{margin:1rem 0}.note{background:#edf3f7;padding:1rem}</style><h1>Stessi bridge: monocromatico, colori, legenda</h1><p>Stato: '+e(r['status'])+'. Tre richieste di due Noul: massimo sei giudizi, nessuna copertura o composito.</p><p class="note">Il colore indica identità o tipo di oggetto, senza indicare la risposta. Entrambi i nuovi segmenti sono viola ed entrambi i punti di contatto nuovi sono magenta. Geometria, ID, richiesta, linee, punti e testo hanno posizioni e dimensioni fisse.</p>'
 if not a['native_noul_answers']:body+='<p>Preparazione offline: nessun risultato nuovo disponibile.</p>'
 body+='<table><tr><th>Versione</th><th>P(sì), positivo</th><th>P(sì), negativo</th><th>Margine</th><th>Corretti</th></tr>'
 for arm in ARMS:
  row=a['arms'].get(arm);body+='<tr><td>'+TITLES[arm]+'</td>'
  body+=''.join('<td>'+f'{row[k]:.3f}'+'</td>' for k in ('p_positive','p_negative','margin'))+'<td>'+str(row['summary']['correct'])+'/2</td></tr>' if row else '<td colspan="4">non disponibile</td></tr>'
 body+='</table>'
 for arm in ARMS:
  call=next((c for c in r['calls'] if c['arm']==arm),None)
  if not call:continue
  body+='<h2>'+TITLES[arm]+'</h2><p>Lato designato: '+e('–'.join(call['model_input']['state']['active_objective']['designated_reference_side']))+'</p>'
  for asset in call['asset_audit']:
   candidate=asset['asset'][6:] if asset['asset'].startswith('image_') else None
   caption=asset['asset']+(' — riferimento esterno: '+('sì' if call['reference'][candidate] else 'no') if candidate else '')
   body+='<figure style="display:inline-block;margin:.5rem"><img alt="Stessa geometria, colori senza etichette di risposta" src="'+asset['file']+'"><figcaption>'+e(caption)+'</figcaption></figure>'
  if arm=='color_legend':body+='<details><summary>Legenda inviata a Jev</summary><pre>'+e(json.dumps(call['model_input']['state']['visual_object_key'],indent=2))+'</pre></details>'
 for title,value in [('Matrici e differenze descrittive',a),('Limiti',r['limits']),('Input e risposte native sanificate',r['calls'])]:body+='<details><summary>'+title+'</summary><pre>'+e(json.dumps(value,indent=2,ensure_ascii=False))+'</pre></details>'
 body+='<p><a href="PROTOCOL.md">Protocollo</a> · <a href="VERIFIED_RESULTS.md">Relazione verificata</a></p><p>Una coppia e una palette, nessuna replica: non è una prova geometrica né di ragionamento sequenziale interno.</p></html>';(out/'viewer.html').write_text(body,encoding='utf-8')

def save(out,report):
 report['analysis']=analyze(report['calls']);tmp=out/'results.tmp';tmp.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');tmp.replace(out/'results.json');viewer(out,report)

def main(out,live=False):
 if live and (os.getenv('GITHUB_ACTIONS')!='true' or not os.getenv('TYPESAFE_API_KEY')):raise SystemExit('Actions and repository secret required')
 out.mkdir(parents=True,exist_ok=True)
 for name in ('PROTOCOL.md','VERIFIED_RESULTS.md'):
  source=HERE/name
  if source.exists():(out/name).write_text(source.read_text(encoding='utf-8'),encoding='utf-8')
 report={'experiment':'Right pair color and color-to-ID binding v1','status':'running' if live else 'offline_only','model':'jev-1.14.0','source_commit':os.getenv('GITHUB_SHA'),'run_id':os.getenv('GITHUB_RUN_ID'),
  'decision_policy':{'threshold':.5,'equal_threshold':'abstain_counted_incorrect'},'limits':LIMITS,'historical_context':{'run_id':SOURCE['run_id'],'source_commit':SOURCE['source_commit'],'arm':'original','p_yes_by_method':{OLD['candidate_mapping'][OLD['question_metadata'][q]['candidate']]:answer['noul'] for q,answer in OLD['response']['answers'].items()}},
  'provenance':{'parent_commit':'e9ed7abd22bda84bc6d77bd4f2bdf033452fb4b8','source_request_sha256':OLD['request_sha256'],'archived_results_canonical_sha256':base.digest(SOURCE),'fixture_manifest_sha256':fixture_hash()},'calls':[]}
 events=list(ARMS);random.Random(SEED).shuffle(events)
 for arm in events:
  p,meta,audit=build_payload(out,arm);record={**meta,'asset_audit':audit,'model_input':{k:v for k,v in p.items() if k!='assets'},'request_sha256':base.digest(p)}
  if live:record.update(native.transport(p))
  report['calls'].append(record);save(out,report);print('Recorded',len(report['calls']),'/3',flush=True)
  if record.get('failure') in ('HTTP_400','HTTP_401','HTTP_403'):
   report['status']='request_rejected';save(out,report);raise SystemExit('Request rejected; sanitized artifact saved')
 report['status']='completed_with_failures' if any('failure' in c for c in report['calls']) else 'completed' if live else 'offline_only';save(out,report)
 if report['status']=='completed_with_failures':raise SystemExit('Sanitized failures recorded')

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,default=Path('output_right_pair_color_binding'));ap.add_argument('--live',action='store_true');ap.add_argument('--freeze-fixtures',action='store_true');args=ap.parse_args()
 if args.freeze_fixtures:
  if args.live:raise SystemExit('Freeze offline before live')
  freeze_fixtures()
 else:main(args.out,args.live)

"""Concrete role witnesses and near misses; closed-world structural evidence."""
from __future__ import annotations
import argparse,base64,copy,hashlib,html,itertools,json,math,os,random,sys
from pathlib import Path
from PIL import Image,ImageDraw

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'experiments/generic_binding_ablation'))
import benchmark_ablation as previous

SEED=20261024
EPS=1e-4 # Cross-products/areas in pixel coordinates; accommodates rounded rotations.
TRANSFORMS=((0,1),(37,1),(0,-1),(37,-1))
CASES=('shared','distinct_coincident','partial_use','triangle_quadrilateral','wrong_host','omitted_valid')
SCHEMAS=('shared_triangles','polyrole_partition')
CONTRACTS={
 'shared_triangles':{'roles':{'carrier':'segment','regions':'two distinct triangular regions','host':'query scope host'},'requirements':['Both regions lie within the query scope host.','One and the same material segment is a COMPLETE boundary side of each region. Each boundary use must cover both endpoints of that carrier.','The regions have disjoint interiors and are adjacent along that common side.'],'scope':'Host is context containment only. The two triangles need not cover the whole host. No metric equality or congruence is required.'},
 'polyrole_partition':{'roles':{'carrier':'segment','regions':'two distinct closed polygonal regions','host':'query scope host'},'requirements':['Both regions lie within the query scope host.','One and the same material segment is a COMPLETE boundary side of both regions.','The two regions have disjoint interiors and together cover the entire query scope host. The carrier thereby has boundary participations and an internal host-partition participation.'],'scope':'The regions need not both be triangles. No metric equality or congruence is required.'}
}
LIMITS=[
 'Four replicas combine ID/option-order randomization with rotations/reflections. This is a bounded synthetic structural-binding test, not 48 independent geometries.',
 'Coordinates do not merge material identities. The structured workspace declares boundary uses; overlapping images alone cannot resolve coincident material objects.',
 'The same-material counterfactual changes exactly one boundary carrier reference. The base and changed snapshot have pixel-identical images.',
 'Two historical schemas are operationalized by the previous local contracts, extended here with explicit adjacency and complete-side requirements.',
 'Jev selects a supplied finite witness; it does not generate a free-form binding or extract all relations autonomously from pixels.',
 'None means no listed full witness is valid; in omitted_valid a binding exists in the graph but has deliberately been withheld from the options.',
 'The local convex-polygon checker defines this benchmark reference. It is not a theorem prover or validation of the full Merovingio graph engine.',
 'All raw typed choices and invalid-witness reasons are reported before any gate. A downstream rejection does not repair a model answer.',
 'No new native scores are requested. At most four live calls with 12 Choice questions each, through Actions only, images header enabled, long context disabled.',
 'Multiple images do not establish internal sequential reasoning. These snapshots are counterfactual alternatives, not temporal construction frames.'
]

def cross(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def signed_area(p):return sum(p[i][0]*p[(i+1)%len(p)][1]-p[(i+1)%len(p)][0]*p[i][1] for i in range(len(p)))/2
def area(p):return abs(signed_area(p)) if len(p)>=3 else 0
def inside(p,poly):
 sign=1 if signed_area(poly)>0 else -1
 return all(sign*cross(poly[i],poly[(i+1)%len(poly)],p)>=-EPS for i in range(len(poly)))

def intersection(subject,clip):
 """Convex clipping, independently derived from geometry rather than case labels."""
 out=list(subject);sign=1 if signed_area(clip)>0 else -1
 for i,a in enumerate(clip):
  b=clip[(i+1)%len(clip)];source=out;out=[]
  if not source:break
  for j,end in enumerate(source):
   start=source[j-1];ds=sign*cross(a,b,start);de=sign*cross(a,b,end)
   if (ds>=-EPS)!=(de>=-EPS):
    t=ds/(ds-de);out.append([start[k]+t*(end[k]-start[k]) for k in (0,1)])
   if de>=-EPS:out.append(end)
 return out

def canonical(variant,angle,reflection):
 points={'A':[-140,100],'B':[140,100],'C':[0,-130],'D':[-25,100],'E':[-12.5,-15],
         'P':[-63,-26.5],'Q':[70,-15],'U':[-175,-175],'V':[175,-175],'W':[175,175],'X':[-175,175]}
 segs={'AD':['A','D'],'DB':['D','B'],'BC':['B','C'],'CA':['C','A'],'BE':['B','E'],
       'AP':['A','P'],'PC':['P','C'],'BQ':['B','Q'],'QC':['Q','C'],
       'S':['D','C'],'T':['D','C'],'Z':['D','C']}
 def use(carrier,a,b):return {'carrier':carrier,'endpoints':[a,b]}
 left={'type':'region','vertices':['A','D','C'],'boundary_uses':[use('AD','A','D'),use('S','D','C'),use('CA','C','A')]}
 right={'type':'region','vertices':['D','B','C'],'boundary_uses':[use('DB','D','B'),use('BC','B','C'),use('S','C','D')]}
 if variant=='distinct_coincident':right['boundary_uses'][-1]['carrier']='T'
 if variant=='partial_use':
  right={'type':'region','vertices':['D','B','E'],'boundary_uses':[use('DB','D','B'),use('BE','B','E'),use('S','E','D')]}
 if variant=='triangle_quadrilateral':
  for name in ('S','T','Z'):segs[name]=['P','Q']
  left={'type':'region','vertices':['P','Q','C'],'boundary_uses':[use('S','P','Q'),use('QC','Q','C'),use('PC','C','P')]}
  right={'type':'region','vertices':['A','B','Q','P'],'boundary_uses':[use('AD','A','D'),use('DB','D','B'),use('BQ','B','Q'),use('S','Q','P'),use('AP','P','A')]}
 clone=copy.deepcopy(left)
 for u in clone['boundary_uses']:
  if u['carrier']=='S':u['carrier']='Z'
 a=math.radians(angle)
 transform=lambda p:[round(256+reflection*p[0]*math.cos(a)-p[1]*math.sin(a),8),round(256+reflection*p[0]*math.sin(a)+p[1]*math.cos(a),8)]
 objects={k:{'type':'point','xy':transform(p)} for k,p in points.items()}
 objects.update({k:{'type':'segment','endpoints':p} for k,p in segs.items()})
 objects.update({'L':left,'R':right,'CL':clone,'H':{'type':'host','vertices':['A','B','C']},'OUT':{'type':'host','vertices':['U','V','W','X']}})
 return objects

def polygon(objects,item):return [objects[p]['xy'] for p in item['vertices']]

def check_witness(objects,witness,schema,scope_host):
 reasons=[]
 try:
  carrier=objects[witness['carrier']];regions=[objects[k] for k in witness['regions']];host=objects[witness['host']]
  if carrier['type']!='segment' or len(regions)!=2 or any(r['type']!='region' for r in regions) or host['type']!='host':return ['role_types']
  if len(set(witness['regions']))!=2:return ['distinct_regions']
  if witness['host']!=scope_host:reasons.append('wrong_scope_host')
  rp=[polygon(objects,r) for r in regions];hp=polygon(objects,host)
  if any(not inside(p,hp) for poly in rp for p in poly):reasons.append('host_containment')
  if schema=='shared_triangles' and any(len(r['vertices'])!=3 for r in regions):reasons.append('region_types')
  for region in regions:
   uses=[u for u in region['boundary_uses'] if u['carrier']==witness['carrier']]
   if not uses:reasons.append('material_identity')
   elif not any(set(u['endpoints'])==set(carrier['endpoints']) for u in uses):reasons.append('incomplete_side_use')
  if area(intersection(rp[0],rp[1]))>EPS:reasons.append('overlapping_interiors')
  if schema=='polyrole_partition' and abs(sum(area(p) for p in rp)-area(hp))>EPS:reasons.append('incomplete_host_partition')
 except (KeyError,TypeError,IndexError):return ['invalid_object_reference']
 return sorted(set(reasons))

def all_bindings(objects,schema,host):
 regions=[k for k,v in objects.items() if v['type']=='region'];segments=[k for k,v in objects.items() if v['type']=='segment'];found=[]
 for s,pair in itertools.product(segments,itertools.combinations(regions,2)):
  w={'carrier':s,'regions':list(pair),'host':host}
  if not check_witness(objects,w,schema,host):found.append(w)
 return found

def render(objects):
 im=Image.new('RGB',(512,512),'white');d=ImageDraw.Draw(im)
 for v in objects.values():
  if v['type']=='host':d.line(polygon(objects,v)+[polygon(objects,v)[0]],fill='#b6bec8',width=2)
 for v in objects.values():
  if v['type']=='region':
   for u in v['boundary_uses']:d.line([tuple(objects[p]['xy']) for p in u['endpoints']],fill='#26313d',width=3)
 return im

def rename(value,mapping):
 if isinstance(value,dict):return {k:rename(v,mapping) for k,v in value.items()}
 if isinstance(value,list):return [rename(v,mapping) for v in value]
 return mapping.get(value,value) if isinstance(value,str) else value

def build_payload(out,replica):
 angle,reflection=TRANSFORMS[replica];rng=random.Random(SEED+replica)
 base_objects=canonical('shared',angle,reflection)
 aliases={name:'O'+str(v) for name,v in zip(base_objects,rng.sample(range(100,999),len(base_objects)))}
 variants=('shared','distinct_coincident','partial_use','triangle_quadrilateral')
 world_aliases=dict(zip(variants,['V'+str(x) for x in rng.sample(range(100,999),4)]))
 schema_aliases=dict(zip(SCHEMAS,['G'+str(x) for x in rng.sample(range(100,999),2)]))
 state={'workspace_kind':'counterfactual construction snapshots with explicit material objects',
        'identity_policy':'IDs are local to each snapshot. A carrier reference identifies one material object. Equal coordinates, endpoints or lengths do not merge distinct object IDs. Boundary-use endpoints can cover all or part of a carrier.',
        'evidence_policy':'Object types, vertex cycles and boundary uses are supplied facts. Regions are convex closed polygons. Coincident distinct region records can overlap. Do not infer role binding from appearance alone. No metric theorem is certified.',
        'contracts':{schema_aliases[s]:copy.deepcopy(CONTRACTS[s]) for s in SCHEMAS},'snapshots':{}}
 assets={};audit=[];worlds={};image_for={};geometry_images={}
 for variant in variants:
  raw=canonical(variant,angle,reflection);objects={aliases[k]:rename(v,aliases) for k,v in raw.items()}
  order=list(objects);rng.shuffle(order);objects={k:objects[k] for k in order};worlds[variant]=objects
  im=render(raw);key='I'+str(len(assets)+1)
  digest=hashlib.sha256(im.tobytes()).hexdigest()
  if digest in geometry_images:key=geometry_images[digest]
  else:
   geometry_images[digest]=key;path=out/'images'/f'view_{replica}_{len(assets)}.png';path.parent.mkdir(parents=True,exist_ok=True);im.save(path)
   data=path.read_bytes();assets[key]={'type':'image','format':'png','data_base64':base64.b64encode(data).decode('ascii')}
   audit.append({'asset':key,'file':path.relative_to(out).as_posix(),'sha256':hashlib.sha256(data).hexdigest()})
  image_for[variant]=key;state['snapshots'][world_aliases[variant]]={'objects':objects,'image':key}
 assert image_for['shared']==image_for['distinct_coincident']
 questions={};metadata={}
 for case,schema in itertools.product(CASES,SCHEMAS):
  variant=case if case in variants else 'shared';objects=worlds[variant]
  host=aliases['OUT' if case=='wrong_host' else 'H'];other_host=aliases['H' if case=='wrong_host' else 'OUT']
  def witness(carrier,left='L',right='R',h=host):return {'carrier':aliases[carrier],'regions':[aliases[left],aliases[right]],'host':h}
  options=[witness('S'),witness('T'),witness('S','CL'),witness('S','L','CL'),witness('S',h=other_host)]
  if case=='omitted_valid':options[0]=witness('Z')
  assert len({json.dumps(w,sort_keys=True) for w in options})==5
  labels=['K'+str(x) for x in rng.sample(range(100,999),5)];mapping=dict(zip(labels,options));items=list(mapping);rng.shuffle(items)
  criteria={label:mapping[label] for label in items};criteria['none']='No listed role assignment satisfies every requirement for this contract and query scope host.'
  valid=[k for k,w in mapping.items() if not check_witness(objects,w,schema,host)];assert len(valid)<=1
  q='Q'+str(len(questions)+1).zfill(3)
  questions[q]={'type':'choice','instructions':{'snapshot_ref':world_aliases[variant],'contract_ref':schema_aliases[schema],'query_scope_host':host,'task':'Select a listed complete role assignment satisfying the referenced contract in this snapshot. The host field must equal query_scope_host. The region pair is unordered. Material identity and full boundary use must be checked. If no listed assignment is valid, select none; a valid binding may exist outside the offered assignments.'},'criteria':criteria}
  metadata[q]={'case':case,'schema':schema,'snapshot':world_aliases[variant],'query_scope_host':host,'option_witnesses':mapping,'option_failures':{k:check_witness(objects,w,schema,host) for k,w in mapping.items()},'expected_choice':valid[0] if valid else 'none','valid_listed_n':len(valid),'all_graph_bindings':all_bindings(objects,schema,host),'aliases':aliases}
 order=list(questions);rng.shuffle(order)
 payload={'model':'jev-1.14.0','state':state,'assets':assets,'questions':{q:questions[q] for q in order}}
 return payload,metadata,audit

def analyze(calls):
 rows=[]
 for call in calls:
  for q,a in call.get('response',{}).get('answers',{}).items():
   m=call['question_metadata'][q];choice=a['choice'];valid=m['valid_listed_n']>0
   rows.append({'replica':call['replica'],'case':m['case'],'schema':m['schema'],'question':q,'expected_choice':m['expected_choice'],'choice':choice,'correct':choice==m['expected_choice'],'listed_binding_exists':valid,'graph_binding_exists':bool(m['all_graph_bindings']),'selected_witness':m['option_witnesses'].get(choice),'selected_invalid_reasons':m['option_failures'].get(choice,[]),'confidence':a['confidence'],'reliability':a['reliability']})
 def summarize(items):
  matrix={'valid_listed':{'valid_witness':0,'wrong_witness':0,'none':0},'none_valid_listed':{'valid_witness':0,'wrong_witness':0,'none':0}}
  for r in items:
   pred='none' if r['choice']=='none' else 'valid_witness' if r['correct'] else 'wrong_witness'
   matrix['valid_listed' if r['listed_binding_exists'] else 'none_valid_listed'][pred]+=1
  return {'n':len(items),'correct':sum(r['correct'] for r in items),'matrix':matrix,'positive_witnesses_correct':sum(r['listed_binding_exists'] and r['correct'] for r in items),'positive_n':sum(r['listed_binding_exists'] for r in items),'negative_none_correct':sum(not r['listed_binding_exists'] and r['choice']=='none' for r in items),'negative_n':sum(not r['listed_binding_exists'] for r in items),'mean_confidence':previous.mean(r['confidence'] for r in items if r['confidence'] is not None)}
 paired=[]
 for replica,schema in itertools.product(range(4),SCHEMAS):
  a=next((r for r in rows if r['replica']==replica and r['schema']==schema and r['case']=='shared'),None)
  b=next((r for r in rows if r['replica']==replica and r['schema']==schema and r['case']=='distinct_coincident'),None)
  if a and b:paired.append({'replica':replica,'schema':schema,'shared_correct':a['correct'],'changed_identity_correct':b['correct'],'both_correct':a['correct'] and b['correct']})
 return {'api_calls_attempted':sum('response' in c or 'failure' in c for c in calls),'api_failures':sum('failure' in c for c in calls),'native_answers':len(rows),'overall':summarize(rows),'by_case':{case:summarize([r for r in rows if r['case']==case]) for case in CASES},'by_schema':{s:summarize([r for r in rows if r['schema']==s]) for s in SCHEMAS},'identity_counterfactual_pairs':paired,'observations':rows}

def viewer(out,report):
 e=html.escape;a=report['analysis'];body='<!doctype html><html lang="it"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Binding concreto e controesempi</title><style>body{font:16px system-ui;max-width:1200px;margin:2rem auto;padding:1rem;color:#26313d}table{border-collapse:collapse;width:100%}td,th{border:1px solid #ccd;padding:.5rem}pre{white-space:pre-wrap;overflow-wrap:anywhere}img{width:240px}details{margin:1rem 0}</style><h1>Ruoli associati agli oggetti del workspace</h1><p>Stato: '+e(report['status'])+'. Cinque assegnazioni concrete e none. 12 domande per chiamata; quattro repliche con ID e ordine randomizzati, rotazioni e riflessioni. Le immagini dei due casi di identità materiale sono pixel identiche.</p><p>Il modello sceglie un witness fornito: carrier, coppia di regioni e figura ospite. Le relazioni strutturate sono evidenza fornita; nessuna prova geometrica o estrazione visiva autonoma è implicata.</p><pre>'+e(json.dumps(a['overall'],indent=2))+'</pre><table><tr><th>Controllo</th><th>Corretti</th><th>Witness positivi</th><th>None negativi</th></tr>'
 for case,v in a['by_case'].items():body+='<tr><td>'+case+'</td><td>'+str(v['correct'])+'/'+str(v['n'])+'</td><td>'+str(v['positive_witnesses_correct'])+'/'+str(v['positive_n'])+'</td><td>'+str(v['negative_none_correct'])+'/'+str(v['negative_n'])+'</td></tr>'
 body+='</table><p>None significa nessuna assegnazione valida fra le opzioni. Nel controllo omitted_valid il binding esiste nel grafo, ma è escluso dalle opzioni.</p>'
 for call in report['calls']:
  body+='<h2>Replica '+str(call['replica'])+'</h2>'+''.join('<img src="'+asset['file']+'">' for asset in call['asset_audit'])
 for title,value in [('Matrici per schema',a['by_schema']),('Coppie controfattuali di identità',a['identity_counterfactual_pairs']),('Assegnazioni scelte ed errori',a['observations']),('Contratti',report['contracts']),('Limiti',report['limits']),('Input e risposte native sanitizzate',report['calls'])]:body+='<details><summary>'+title+'</summary><pre>'+e(json.dumps(value,indent=2,ensure_ascii=False))+'</pre></details>'
 body+='<p><a href="VERIFIED_RESULTS.md">Risultati verificati e interpretazione</a></p></html>'
 (out/'viewer.html').write_text(body,encoding='utf-8')

def save(out,report):
 report['analysis']=analyze(report['calls']);temp=out/'results.tmp';temp.write_text(json.dumps(report,indent=2),encoding='utf-8');temp.replace(out/'results.json');viewer(out,report)

def main(out,live=False):
 if live and (os.getenv('GITHUB_ACTIONS')!='true' or not os.getenv('TYPESAFE_API_KEY')):raise SystemExit('Actions and repository secret required')
 out.mkdir(parents=True,exist_ok=True)
 for name in ('PROTOCOL.md','VERIFIED_RESULTS.md'):
  path=Path(__file__).parent/name
  if path.exists():(out/name).write_text(path.read_text(encoding='utf-8'),encoding='utf-8')
 report={'experiment':'Concrete role witness and near-miss binding v1','status':'running' if live else 'offline_only','model':'jev-1.14.0','source_commit':os.getenv('GITHUB_SHA'),'run_id':os.getenv('GITHUB_RUN_ID'),'contracts':CONTRACTS,'limits':LIMITS,'transforms':TRANSFORMS,'calls':[]}
 for replica in random.Random(SEED).sample(range(4),4):
  p,meta,audit=build_payload(out,replica)
  record={'replica':replica,'angle':TRANSFORMS[replica][0],'reflection':TRANSFORMS[replica][1],'question_count':len(p['questions']),'question_metadata':meta,'asset_audit':audit,'model_input':{k:v for k,v in p.items() if k!='assets'},'body_bytes':len(json.dumps(p).encode()),'request_sha256':hashlib.sha256(json.dumps(p,sort_keys=True).encode()).hexdigest()}
  if live:record.update(previous.transport(p))
  report['calls'].append(record);save(out,report);print('Recorded',len(report['calls']),'/ 4',flush=True)
  if record.get('failure')=='HTTP_400':
   report['status']='request_validation_failed';save(out,report);raise SystemExit('Stopped after validation rejection; sanitized artifact saved')
 report['status']='completed_with_failures' if any('failure' in c for c in report['calls']) else 'completed' if live else 'offline_only';save(out,report)
 if report['status']=='completed_with_failures':raise SystemExit('Sanitized failures recorded')

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,default=Path('output_concrete_binding'));ap.add_argument('--live',action='store_true');args=ap.parse_args();main(args.out,args.live)

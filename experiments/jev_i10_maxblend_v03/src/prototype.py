"""Merovingio v0.3: constructive grouping without theorem proving.

Only Python stdlib for the symbolic layer; Pillow is used for PNG rendering.
Never concludes the I.10 goal. The image decision model is optional.
"""
from __future__ import annotations
import base64
from dataclasses import dataclass, asdict
import json
import math
import os
from pathlib import Path
import random
import uuid

from PIL import Image, ImageDraw, ImageFont

@dataclass(frozen=True)
class Point:
    x: float
    y: float

A = Point(150, 585)
B = Point(650, 585)
C = Point(400, 585 - 250*math.sqrt(3))
BASE = {"A": A, "B": B, "C": C}

@dataclass(frozen=True)
class Candidate:
    id: str
    family: str
    constructed_point: str | None
    vertex: str | None
    endpoint: str | None
    t: float | None
    description: str

# Deliberately includes geometrically identical operations. Deduplication is mandatory.
RAW = [
    Candidate('raw1','angle_bisector','D','C','AB',None,'Divide the angle at C and extend to AB'),
    Candidate('raw2','perpendicular','D','C','AB',None,'Perpendicular from C to AB'),
    Candidate('raw3','median','D','C','AB',None,'Join C to the midpoint of AB'),
    Candidate('raw4','cevian','D','C','AB',0.31,'Join C to a point in AB (t=0.31)'),
    Candidate('raw5','cevian','D','C','AB',0.69,'Join C to a point in AB (t=0.69)'),
    Candidate('raw6','other_cevian','E','A','BC',0.36,'Join A to a point in BC'),
    Candidate('raw7','parallel',None,'C','AB',None,'Draw a line through C parallel to AB'),
]

def interp(p: Point, q: Point, t: float) -> Point:
    return Point(p.x + (q.x-p.x)*t, p.y + (q.y-p.y)*t)

def mag(v): return math.hypot(*v)
def unit(p:Point,q:Point):
    x,y=q.x-p.x,q.y-p.y
    r=math.hypot(x,y)
    return (x/r,y/r)

def ray_intersection_with_horizontal(p:Point, vx:float, vy:float, y:float):
    u=(y-p.y)/vy
    return Point(p.x+u*vx,y)

def construct(candidate:Candidate):
    p=dict(BASE)
    if candidate.family=='angle_bisector':
        u,v=unit(C,A),unit(C,B)
        p['D']=ray_intersection_with_horizontal(C,u[0]+v[0],u[1]+v[1],A.y)
    elif candidate.family=='perpendicular':
        p['D']=Point(C.x,A.y)
    elif candidate.family=='median':
        p['D']=interp(A,B,0.5)
    elif candidate.family=='cevian':
        p['D']=interp(A,B,candidate.t)
    elif candidate.family=='other_cevian':
        p['E']=interp(B,C,candidate.t)
    return p

def signature(candidate:Candidate):
    p=construct(candidate)
    if candidate.family=='parallel': return ('line', 'horizontal', round(C.y,6))
    if candidate.family in {'angle_bisector','perpendicular','median','cevian'}:
        d=p['D']; return ('segment', 'C', round(d.x,6),round(d.y,6))
    e=p['E']; return ('segment','A',round(e.x,6),round(e.y,6))

def unique_candidates():
    seen={}; out=[]
    for c in RAW:
        sig=signature(c)
        if sig in seen:
            seen[sig]['equivalent_operations'].append(c.family)
            continue
        record={'candidate':c, 'equivalent_operations':[c.family], 'signature':sig}
        seen[sig]=record; out.append(record)
    return out

def angle(p:Point,v:Point,q:Point) -> float:
    a=(p.x-v.x,p.y-v.y); b=(q.x-v.x,q.y-v.y)
    cos=(a[0]*b[0]+a[1]*b[1])/(mag(a)*mag(b))
    return math.degrees(math.acos(min(1,max(-1,cos))))

def explore(entry):
    c=entry['candidate']; p=construct(c)
    spaces=[{'id':'MS_segment_AB', 'members':['A','B','AB'], 'origin':'given'},
            {'id':'MS_angle_ACB','members':['A','C','B','CA','CB','angle_ACB'],'origin':'triangle_vertex'},
            {'id':'MS_equilateral','members':['A','B','C','AB','AC','BC'],'origin':'given_construction'}]
    relations=[]; groups=[]; generic=[]; verified=[]
    if c.family in {'angle_bisector','perpendicular','median','cevian'}:
        d=p['D']; a1=angle(A,C,d); a2=angle(d,C,B)
        mismatch=abs(a1-a2)
        spaces += [
           {'id':'MS_left','members':['A','C','D','AC','CD','AD','angle_ACD'],'origin':'bridge_CD'},
           {'id':'MS_right','members':['B','C','D','BC','CD','DB','angle_DCB'],'origin':'bridge_CD'}]
        groups=[{'id':'left','boundary':['A','C','D'],'generator':'CD','mixed_roles':['outer_side','shared_carrier','included_wedge']},
                {'id':'right','boundary':['B','C','D'],'generator':'CD','mixed_roles':['outer_side','shared_carrier','included_wedge']}]
        verified=[{'predicate':'same_segment','members':['CD','CD'],'status':'structural_identity'},
                  {'predicate':'equal_length','members':['CA','CB'],'status':'given_equilateral'},
                  {'predicate':'betweenness','members':['A','D','B'],'status':'construction'}]
        relations=[{'role':'outer_side_pair','left':'CA','right':'CB','support':'given_equilateral'},
                   {'role':'shared_bridge','left':'CD','right':'CD','support':'identity'},
                   {'role':'included_wedge','left':'angle_ACD','right':'angle_DCB','support':'measured_visual_candidate',
                    'gap_degrees':round(mismatch,4)}]
        generic=[{'id':'GS_paired_mixed_groups','from':['MS_left','MS_right'],
                  'generator':'CD', 'role_alignment':['outer_side_pair','shared_bridge','included_wedge'],
                  'status':'candidate', 'provenance': 'construction_and_angular_measurement'}]
        # Baseline objective deliberately excludes goal, congruence criterion, and equality of base parts.
        angular_alignment=max(0.0,1.0-mismatch/60.0)
        bridge_value=3 # angle domain, segment domain, two resulting triangle groups
        score=0.7 + 0.7*angular_alignment + 0.18*bridge_value - 0.12
        evidence={'paired_mixed_groups':2,'cross_space_roles':3,
                  'angular_alignment':round(angular_alignment,3),
                  'angle_gap_deg':round(mismatch,4),'bridge_spaces':bridge_value}
    elif c.family=='other_cevian':
        e=p['E']; a1=angle(B,A,e); a2=angle(e,A,C); mismatch=abs(a1-a2)
        spaces += [{'id':'MS_base_branch1','members':['A','B','E'],'origin':'bridge_AE'},
                   {'id':'MS_base_branch2','members':['A','E','C'],'origin':'bridge_AE'}]
        groups=[{'id':'branch1','boundary':['A','B','E'],'generator':'AE'},
                {'id':'branch2','boundary':['A','E','C'],'generator':'AE'}]
        relations=[{'role':'shared_bridge','left':'AE','right':'AE','support':'identity'},
                   {'role':'divided_wedge','left':'angle_BAE','right':'angle_EAC',
                    'gap_degrees':round(mismatch,4),'support':'measured_visual_candidate'}]
        generic=[{'id':'GS_branch_pair','from':['MS_base_branch1','MS_base_branch2'],'generator':'AE',
                  'status':'candidate'}]
        # Less alignment to the original mental space *angle at C* and *segment AB*.
        score=0.47+0.22*max(0.0,1-mismatch/60.0)-0.12
        evidence={'paired_mixed_groups':2,'cross_space_roles':1,'angle_gap_deg':round(mismatch,4),
                  'angular_alignment':round(max(0,1-mismatch/60),3),'bridge_spaces':1}
    elif c.family=='parallel':
        spaces += [{'id':'MS_extended_direction','members':['C','line_C_parallel_AB'],'origin':'parallel_through_C'}]
        generic=[{'id':'GS_directional_correspondence','from':['MS_segment_AB','MS_extended_direction'],
                  'generator':'parallel_through_C','status':'candidate'}]
        score=0.32
        evidence={'paired_mixed_groups':0,'cross_space_roles':1,'angular_alignment':None,'bridge_spaces':2}
    else: raise ValueError(c.family)
    multi_roles={
      'AB': [{'role':'given_segment','status':'given','source':'W0'},
             {'role':'equilateral_base','status':'given','source':'W0'}],
      'C': [{'role':'triangle_apex','status':'given','source':'W0'},
            {'role':'angle_vertex','status':'given','source':'W0'}],
    }
    if c.family in {'angle_bisector','perpendicular','median','cevian'}:
        multi_roles['CD']=[{'role':'connection_between_angle_and_base_spaces', 'status':'candidate', 'source':c.id},
                           {'role':'shared_carrier_of_two_groups', 'status':'construction_identity','source':c.id},
                           {'role':'left_right_partition_generator','status':'construction_identity','source':c.id}]
        multi_roles['D']=[{'role':'point_on_base', 'status':'construction_identity','source':c.id},
                          {'role':'bridge_endpoint','status':'construction_identity','source':c.id}]
    if c.family=='other_cevian':
        multi_roles['AE']=[{'role':'group_partition_generator','status':'construction_identity','source':c.id}]
    order=[{'order':0,'event':'given_AB','produces':['AB'],'status':'given'},
           {'order':1,'event':'construct_equilateral_ABC','produces':['AC','BC','C'],'status':'given'}]
    order.append({'order':2,'event':'candidate_construction',
                  'produces':list(p.keys())[3:]+([c.vertex+c.constructed_point] if c.constructed_point else ['line_through_C']),
                  'status':'hypothetical','source':c.id})
    return {'id':c.id, 'operation':c.family,'description':c.description,
            'object_interpretations':multi_roles, 'construction_timeline':order,
            'equivalent_operations':entry['equivalent_operations'],
            'construction_signature':list(entry['signature']),
            'mental_spaces':spaces, 'groups':groups,
            'candidate_generic_spaces':generic, 'correspondences':relations,
            'known_constraints':verified,
            'heuristic_blend_value':round(score,3),
            'heuristic_evidence':evidence,
            'epistemic_status':'geometric simulation / hypothetical, NOT a proof'}

COL_BG='#0C1422'; COL_FG='#EFF2F8'; COL_L='#F0A647'; COL_R='#52B8CB'; COL_B='#BFA1FF'

def font(size=19):
    for f in ['/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf','/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf']:
        if Path(f).exists(): return ImageFont.truetype(f,size)
    return ImageFont.load_default()

def render(path:Path, candidate:Candidate|None, theme='dark', show_legend=True, highlight_groups=True):
    im=Image.new('RGB',(900,800),COL_BG if theme=='dark' else 'white')
    d=ImageDraw.Draw(im)
    points=construct(candidate) if candidate else BASE
    def xy(k): return (int(points[k].x),int(points[k].y))
    def line(x,y,col=COL_FG,w=4): d.line((xy(x),xy(y)),fill=col,width=w)
    line('A','B');line('A','C');line('B','C')
    if candidate is not None:
        if candidate.family in {'angle_bisector','perpendicular','median','cevian'}:
            if highlight_groups:
                d.polygon([xy('A'),xy('C'),xy('D')],fill='#27251F')
                d.polygon([xy('B'),xy('C'),xy('D')],fill='#142E39')
            line('A','B');line('A','C');line('B','C');line('C','D',COL_B,7)
            for k in ['D']:
                q=xy(k);d.ellipse((q[0]-5,q[1]-5,q[0]+5,q[1]+5),fill=COL_B)
        elif candidate.family=='other_cevian':
            if highlight_groups:
                d.polygon([xy('A'),xy('B'),xy('E')],fill='#27251F')
                d.polygon([xy('A'),xy('E'),xy('C')],fill='#142E39')
            line('A','B');line('A','C');line('B','C');line('A','E',COL_B,7)
        elif candidate.family=='parallel':
            d.line((130,int(C.y),670,int(C.y)),fill=COL_B,width=6)
    for name,q in points.items():
        center=xy(name)
        d.ellipse((center[0]-5,center[1]-5,center[0]+5,center[1]+5),fill=COL_FG)
        offsets={'A':(-28,5),'B':(12,5),'C':(-7,-37),'D':(9,8),'E':(12,-18)}
        off=offsets.get(name,(10,10)); d.text((center[0]+off[0],center[1]+off[1]),name,fill=COL_FG,font=font(25))
    title='W0 — prima di qualsiasi bridge' if candidate is None else f'{candidate.id} — workspace dopo la costruzione'
    d.text((40,38),title,fill=COL_FG,font=font(29))
    d.text((40,87),'Mental spaces iniziali: segmento AB · angolo ACB · equilatero ABC',fill='#A9B4C6',font=font(18))
    if show_legend:
        d.text((40,724),'Simulazione della costruzione, non dimostrazione · nessun goal o teorema dato a Jev',fill='#A9B4C6',font=font(17))
        if candidate is not None:
            d.text((40,755),'Arancio / azzurro: raggruppamenti emergenti    Viola: bridge candidato',fill=COL_FG,font=font(16))
    path.parent.mkdir(parents=True,exist_ok=True)
    im.save(path)
    return path

def build_state(results, root:Path, shuffle_seed=19):
    # Important: input to Jev intentionally excludes results and operation names.
    rng=random.Random(shuffle_seed)
    choices=[r['id'] for r in results];rng.shuffle(choices)
    return {
      'task':'exploratory_cross_space_grouping_no_goal',
      'initial_mental_spaces':[
         {'id':'S1','roles':['two endpoints','a continuous carrier','possible interior partitions']},
         {'id':'S2','roles':['apex','two incident rays','angular sectors']},
         {'id':'S3','roles':['closed three-sided structure','three initially equal outer side lengths']}],
      'initial_workspace':'im-w0',
      'candidate_workspaces':[{'id':i, 'after_image':f'im-{i.lower()}'} for i in choices],
      'instructions':'Compare candidate final states, not theorem proofs. Maximize coherent new mixed side-angle groups and cross-space roles. Do not use a proof conclusion; do not equate visual similarity with a certified fact.'}

def jev_payload(results, root:Path, seed=19, model='jev-1.14.0'):
    state=build_state(results,root,seed)
    asset_files={'im-w0':root/'images'/'initial.png'}
    for r in results: asset_files[f"im-{r['id'].lower()}"]=root/'images'/f"{r['id']}.png"
    assets={}
    for key,path in asset_files.items():
        assets[key]={'type':'image','format':'png','data_base64':base64.b64encode(path.read_bytes()).decode('ascii')}
    criteria={r['id']: f"Candidate workspace `{r['id']}` displayed in candidate_workspaces" for r in results}
    criteria['none']='None of the candidates creates a coherent cross-space grouping.'
    questions={'best_bridge':{'type':'choice',
        'instructions':'Which candidate most effectively creates two new structurally aligned mixed groups by connecting the original mental spaces? Prefer alignment of side and angular roles, not visual density alone; do not infer or assume a theorem conclusion.',
        'criteria':criteria}}
    for r in results:
        id=r['id']
        questions[f'alignment_{id}']={'type':'score',
          'instructions':f'How coherent are the new cross-space side-angle correspondences in `{id}`? Do not use unproven metrical equalities or assume a theorem.',
          'criteria':['No meaningful new matching','One shared object without structural alignment',
                      'Some aligned side-angle roles','Multiple coherent aligned roles across groups']}
    return {'model':model,'state':state,'assets':assets,'questions':questions}

def build_all(root:Path):
    (root/'images').mkdir(exist_ok=True,parents=True)
    entries=unique_candidates()
    # rename anonymized IDs AFTER geometric dedup; stable rendering but never reveal method names to Jev
    out=[]
    for i,e in enumerate(entries,1):
        c=e['candidate']
        anon=Candidate(f'C{i:02d}', c.family, c.constructed_point,c.vertex,c.endpoint,c.t,c.description)
        e=dict(e,candidate=anon)
        render(root/'images'/f'{anon.id}.png',anon)
        render(root/'images'/f'{anon.id}_raw.png',anon,highlight_groups=False)
        out.append(explore(e))
    render(root/'images'/'initial.png',None)
    (root/'results.json').write_text(json.dumps({'case':'I.10 geometry-only, goal-hidden','candidates':out},indent=2,ensure_ascii=False))
    return out

def call_jev(payload):
    key=os.getenv('TYPESAFE_API_KEY')
    if not key: raise RuntimeError('TYPESAFE_API_KEY not configured; no live Jev call was made.')
    import requests
    result=requests.post('https://api.typesafe.ai/v1/systemone',
          headers={'Authorization':f'Bearer {key}', 'TypeSafe-Danger-Zone-Images':'true'},
          json=payload,timeout=75)
    result.raise_for_status()
    response=result.json()
    if 'answers' not in response or 'best_bridge' not in response['answers']:
        raise ValueError('Jev response missing best_bridge decision')
    return response

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser()
    ap.add_argument('--out',default='output')
    ap.add_argument('--jev',action='store_true',help='Require a real Jev API call using TYPESAFE_API_KEY')
    ap.add_argument('--seed',type=int,default=19)
    args=ap.parse_args()
    root=Path(args.out).resolve()
    results=build_all(root)
    print('Geometrically distinct candidate states:',len(results),'(from',len(RAW),'raw operations)')
    print('No theorem or proof has been applied. Baseline-only ranking (NOT Jev):')
    for c in sorted(results,key=lambda r:-r['heuristic_blend_value']):
        print(f"{c['id']}: {c['heuristic_blend_value']:.3f} {c['operation']} equivalents={c['equivalent_operations']}")
    if args.jev:
        payload=jev_payload(results,root,args.seed)
        response=call_jev(payload)
        (root/'jev_live_response.json').write_text(json.dumps(response,indent=2),encoding='utf-8')
        print('Jev live choice:',response['answers']['best_bridge'])
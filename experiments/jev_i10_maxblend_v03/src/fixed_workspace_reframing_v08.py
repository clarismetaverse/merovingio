"""Merovingio v0.8 — same geometric construction, different active Mental Spaces.

Four overlays are interpretations of ONE identical A-B-C-D construction, not
different candidate constructions. A/B compares visual regrouping with an
additional structured description of the same Mental Spaces.
"""
from __future__ import annotations

import base64
import hashlib
import json
import math
import os
from pathlib import Path
import sys

from PIL import Image, ImageDraw, ImageFont
from prototype import call_jev

A=(170.0,525.0)
B=(780.0,525.0)
C=(340.0,116.0)
D=(A[0]+0.37*(B[0]-A[0]), A[1])
VERTICES={"A":A,"B":B,"C":C,"D":D}
ROLES=("angular","base","regions","coupling")
FRAMES={
 "angular":"The active interpretation concerns the TWO sectors of the apex angle at C, with CD as their common boundary ray. Which grouping foregrounds those two angular sectors, rather than lengths or area regions?",
 "base":"The active interpretation concerns the ordered subsegments AD and DB of the original carrier AB, meeting at D. Which grouping foregrounds the two subdivisions of this carrier?",
 "regions":"The active interpretation concerns two adjacent CLOSED triangular regions ACD and BCD. Which grouping foregrounds those two regions and their common boundary CD?",
 "coupling":"The active interpretation concerns CD simultaneously as a line leaving the angular workspace at C and reaching the segment workspace AB at D. Which grouping foregrounds this cross-space connection rather than either partition separately?",
}
ROLE_SCHEMAS={
 "angular":{"parts":[["CA","CD"],["CD","CB"]],"shared":["ray_CD"],"anchor":"C","partition":"two neighboring sectors"},
 "base":{"parts":[["A","D"],["D","B"]],"carrier":["A","D","B"],"partition":"linear subdivisions"},
 "regions":{"parts":[["A","C","D"],["B","C","D"]],"shared":["C","D"],"partition":"adjacent closed regions"},
 "coupling":{"source":["CA","CB","C"],"target":["A","D","B"],"bridge":["C","D"],"partition":"inter-space connector"},
}
COLORS={"angular":("#EE9A50","#62BBD3"),"base":("#EE9A50","#62BBD3"),
        "regions":("#EE9A50","#62BBD3"),"coupling":("#9B75DB","#62BBD3")}

def geometry_checks():
    # CD deliberately is NOT an angle-bisector, median or perpendicular.
    def dist(p,q):return math.hypot(p[0]-q[0],p[1]-q[1])
    ratio=dist(A,C)/(dist(A,C)+dist(B,C))
    x=(D[0]-A[0])/(B[0]-A[0])
    assert abs(x-0.5)>0.05
    assert abs(x-ratio)>0.02
    assert abs(D[0]-C[0])>20
    assert abs(D[1]-A[1])<1e-7
    return {"base_fraction":round(x,5),
            "angle_bisector_base_fraction":round(ratio,5),
            "median_base_fraction":0.5,
            "perpendicular_base_fraction":round((C[0]-A[0])/(B[0]-A[0]),5)}

def mapping_for(focus,repeat):
    # Within 8 focus/repeat trials the winning ID occupies K1...K4 twice.
    f=ROLES.index(focus)
    shift=(2*f+repeat)%4
    methods=ROLES[shift:]+ROLES[:shift]
    return {"K"+str(i+1):m for i,m in enumerate(methods)}

def line(d,p,q,fill,width=4):
    d.line([p,q],fill=fill,width=width)

def ellipse(d,p,r,fill):
    d.ellipse((p[0]-r,p[1]-r,p[0]+r,p[1]+r),fill=fill)

def make_image(path,overlay=None):
    canvas=Image.new("RGBA",(970,650),(255,255,255,255))
    bg=Image.new("RGBA",canvas.size,(0,0,0,0))
    d=ImageDraw.Draw(bg)
    orange,teal=COLORS.get(overlay,("#EE9A50","#62BBD3"))
    if overlay=="angular":
        def sector(q):
            n=26
            a=math.atan2(q[1]-C[1],q[0]-C[0])
            return a
        arc1=sector(A);mid=sector(D);arc2=sector(B)
        def wedge(start,end,rgba):
            pts=[C]
            for k in range(33):
                th=start+(end-start)*k/32
                pts.append((C[0]+118*math.cos(th),C[1]+118*math.sin(th)))
            d.polygon(pts,fill=rgba)
        wedge(arc1,mid,(238,154,80,100))
        wedge(mid,arc2,(98,187,211,100))
    elif overlay=="base":
        line(d,A,D,(238,154,80,120),22)
        line(d,D,B,(98,187,211,120),22)
    elif overlay=="regions":
        d.polygon([A,C,D],fill=(238,154,80,70))
        d.polygon([B,C,D],fill=(98,187,211,70))
    elif overlay=="coupling":
        ellipse(d,C,24,(155,117,219,100))
        ellipse(d,D,24,(98,187,211,110))
        line(d,C,D,(155,117,219,95),19)
    canvas=Image.alpha_composite(canvas,bg)
    dr=ImageDraw.Draw(canvas)
    ink="#333B43"
    for p,q in ((A,B),(A,C),(B,C),(C,D)):
        line(dr,p,q,ink,4)
    fp=Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    font=ImageFont.truetype(str(fp),24) if fp.exists() else ImageFont.load_default()
    offset={"A":(-31,10),"B":(14,10),"C":(-4,-38),"D":(-6,16)}
    for name,p in VERTICES.items():
        ellipse(dr,p,5,ink)
        xx,yy=offset[name]
        dr.text((p[0]+xx,p[1]+yy),name,fill=ink,font=font)
    path.parent.mkdir(parents=True,exist_ok=True)
    canvas.convert("RGB").save(path)
    return path

def asset(path):
    return {"type":"image","format":"png",
            "data_base64":base64.b64encode(path.read_bytes()).decode("ascii")}

def trial_payload(out,focus,repeat,condition):
    assert condition in ("visual","structured")
    mapping=mapping_for(focus,repeat)
    folder=out/"images"
    paths={"im-base":make_image(folder/"unannotated.png")}
    for code,role in mapping.items():
        # Same exact geometry and construction in EVERY asset.
        paths["im-"+code.lower()]=make_image(folder/(role+".png"),role)
    state={
        "initial_workspace":"im-base",
        "same_construction_in_every_candidate":True,
        "candidate_views":[{"id":code,"image":"im-"+code.lower()} for code in mapping],
        "original_objects":["A","B","C","D","AB","AC","BC","CD"],
        "construction_facts":["D is interior to AB","C is linked to D"],
        "note":"The candidates depict different conceptual regroupings of the same geometric state, not competing new geometric constructions."
    }
    if condition=="structured":
        state["candidate_mental_spaces"]=[
            {"id":code,"workspace_membership":ROLE_SCHEMAS[role],
             "epistemic_status":"hypothetical conceptual view; no equal measures implied"}
            for code,role in mapping.items()
        ]
    request={
        "model":"jev-1.14.0","state":state,
        "assets":{key:asset(path) for key,path in paths.items()},
        "questions":{"best_bridge":{
            "type":"choice",
            "instructions":FRAMES[focus]+
                " Choose the candidate REPRESENTATION, not a new segment. "
                "Do not infer any angular equality, metric equality, perpendicularity or theorem.",
            "criteria":{code:"Grouping displayed in im-"+code.lower() for code in mapping}
        }}
    }
    return request,mapping

def run(out):
    if not os.getenv("TYPESAFE_API_KEY"):
        raise SystemExit("Missing GitHub Actions TYPESAFE_API_KEY secret")
    checks=geometry_checks()
    out.mkdir(parents=True,exist_ok=True)
    trials=[]
    for focus in ROLES:
        for repeat in (0,1):
            for condition in ("visual","structured"):
                req,mapping=trial_payload(out,focus,repeat,condition)
                resp=call_jev(req)
                choice=resp["answers"]["best_bridge"]
                k=choice.get("choice")
                if k not in mapping:
                    raise ValueError("Unknown candidate ID in Jev response")
                selected=mapping[k]
                entry={
                    "focus":focus,"order_repeat":repeat,"condition":condition,
                    "options_scoring_only":mapping,"selected_id":k,
                    "selected_role":selected,"correct":selected==focus,
                    "confidence":choice.get("confidence"),
                    "probabilities":choice.get("probabilities"),
                    "usage":resp.get("usage"),"model":resp.get("model"),
                }
                trials.append(entry)
                print(f"{focus}/{repeat}/{condition}: chosen={k} matches={entry['correct']}")
    aggregate={}
    for condition in ("visual","structured"):
        group=[x for x in trials if x["condition"]==condition]
        aggregate[condition]={
            "correct":sum(x["correct"] for x in group),"total":len(group),
            "input_tokens":sum((x["usage"] or {}).get("input_tokens",0) for x in group),
            "output_tokens":sum((x["usage"] or {}).get("output_tokens",0) for x in group),
        }
    result={
        "title":"Merovingio Jev v0.8 — fixed construction, variable mental-space focus",
        "model":"jev-1.14.0",
        "same_geometry_across_every_trial":True,
        "verified_geometry":checks,"results":aggregate,"trials":trials,
        "limitations":[
            "This assesses perceptual/conceptual reframing, not finding a new construction.",
            "Each focus has an intentionally authored matching visualization; performance may reflect lexical or visual matching.",
            "The chosen line CD is not a median, perpendicular or angle bisector; no equalities are implied.",
            "Only one fixed construction and 8 focus/order cases per condition: no generalization claim."
        ],
    }
    (out/"reframing_results.json").write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding="utf-8")
    print("Saved sanitized reframing_results.json")
    return result

if __name__=="__main__":
    run(Path(sys.argv[1] if len(sys.argv)>1 else "output_reframing"))

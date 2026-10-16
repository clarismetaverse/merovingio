"""Merovingio v0.7: compare candidate bridge *structures*, not metric angle equality.

No I.10 conclusion, proof, correct candidate mapping, or angular measurement
enters a Jev prompt. Choice labels rotate across frames and shapes.
"""
from __future__ import annotations

import base64
import json
import math
import os
from pathlib import Path
import sys

from PIL import Image, ImageDraw, ImageFont
from prototype import call_jev

A = (140.0, 485.0)
B = (740.0, 485.0)
SHAPES = {"left": (312.0, 126.0), "right": (568.0, 126.0)}
METHODS = ("from_C", "from_A", "from_B", "edge_link")
FRAMES = ("apex_C", "apex_A", "apex_B", "side_pair")
CONDITIONS = ("image", "mental", "generic")
FRAME_DESCRIPTIONS = {
    "apex_C": (
        "The active mental spaces are the angular fan rooted at vertex C and "
        "the opposite original carrier AB. Which construction creates the richest "
        "coupled re-partition of these spaces into two adjacent closed subfigures, "
        "sharing its new connector as a common boundary?"
    ),
    "apex_A": (
        "The active mental spaces are the angular fan rooted at vertex A and "
        "the opposite original carrier BC. Which construction creates the richest "
        "coupled re-partition of these spaces into two adjacent closed subfigures, "
        "sharing its new connector as a common boundary?"
    ),
    "apex_B": (
        "The active mental spaces are the angular fan rooted at vertex B and "
        "the opposite original carrier AC. Which construction creates the richest "
        "coupled re-partition of these spaces into two adjacent closed subfigures, "
        "sharing its new connector as a common boundary?"
    ),
    "side_pair": (
        "The active mental spaces are the two incident sides CA and CB viewed as "
        "carriers with possible interior divisions. Which construction couples "
        "interior points on BOTH carriers, producing a smaller apex-containing "
        "closed region and a complementary lower region retaining the original base?"
    ),
}
# Independent offline topology oracles. These labels and their mappings NEVER
# appear in model-visible assets, state, criteria, or instructions.
TOPOLOGY = {
    "from_C": {
        "endpoints": ("C", "D"), "opposite_carrier": "AB",
        "apex": "C", "interior": ("D",), "side_pair": False,
        "regions": (("A", "C", "D"), ("B", "C", "D")),
        "common_edge": ("C", "D"),
    },
    "from_A": {
        "endpoints": ("A", "E"), "opposite_carrier": "BC",
        "apex": "A", "interior": ("E",), "side_pair": False,
        "regions": (("A", "B", "E"), ("A", "E", "C")),
        "common_edge": ("A", "E"),
    },
    "from_B": {
        "endpoints": ("B", "F"), "opposite_carrier": "AC",
        "apex": "B", "interior": ("F",), "side_pair": False,
        "regions": (("B", "A", "F"), ("B", "F", "C")),
        "common_edge": ("B", "F"),
    },
    "edge_link": {
        "endpoints": ("P", "Q"), "opposite_carrier": None,
        "apex": None, "interior": ("P", "Q"), "side_pair": True,
        "regions": (("C", "P", "Q"), ("A", "B", "Q", "P")),
        "common_edge": ("P", "Q"),
    },
}

def interp(p, q, t):
    return (p[0] * (1.0-t) + q[0]*t, p[1]*(1.0-t)+q[1]*t)

def points(shape):
    C=SHAPES[shape]
    return {"A":A, "B":B, "C":C,
            "D":interp(A,B,0.37), "E":interp(B,C,0.42),
            "F":interp(A,C,0.56),
            "P":interp(A,C,0.43), "Q":interp(B,C,0.43)}

def interior_between(p, x, q):
    # Collinear and strictly between, independent of semantic option labels.
    cross=(x[0]-p[0])*(q[1]-p[1])-(x[1]-p[1])*(q[0]-p[0])
    dot=(x[0]-p[0])*(q[0]-p[0])+(x[1]-p[1])*(q[1]-p[1])
    sq=(q[0]-p[0])**2+(q[1]-p[1])**2
    return abs(cross)<1e-5 and 1e-6<dot<sq-1e-6

def certify_geometry(shape):
    p=points(shape)
    assert interior_between(p["A"],p["D"],p["B"])
    assert interior_between(p["B"],p["E"],p["C"])
    assert interior_between(p["A"],p["F"],p["C"])
    assert interior_between(p["A"],p["P"],p["C"])
    assert interior_between(p["B"],p["Q"],p["C"])
    for method in METHODS:
        region1,region2=TOPOLOGY[method]["regions"]
        # a common new segment must occur in BOTH region boundaries
        common=set(region1) & set(region2)
        assert common==set(TOPOLOGY[method]["common_edge"])
    return True

def expected_method(frame):
    if frame=="side_pair":
        candidates=[k for k,v in TOPOLOGY.items() if v["side_pair"]]
    else:
        vertex=frame.split("_")[-1]
        opposite={"A":"BC","B":"AC","C":"AB"}[vertex]
        candidates=[k for k,v in TOPOLOGY.items()
                    if v["apex"]==vertex and v["opposite_carrier"]==opposite]
    assert len(candidates)==1
    return candidates[0]

def anonymous_mapping(shape, frame):
    # Latin-square-like counterbalancing: across 8 trials, winning label K1..K4
    # occurs exactly twice. No random stochastic variance across conditions.
    i=FRAMES.index(frame)
    s=list(SHAPES).index(shape)
    shift=(2*i+s)%len(METHODS)
    ordered=METHODS[shift:]+METHODS[:shift]
    return {"K"+str(j+1):method for j,method in enumerate(ordered)}

def render(out,shape,method=None):
    p=points(shape)
    im=Image.new("RGB",(860,620),"white")
    draw=ImageDraw.Draw(im)
    ink="#333C47"
    for u,v in (("A","B"),("B","C"),("C","A")):
        draw.line((p[u],p[v]),fill=ink,width=5)
    names=["A","B","C"]
    if method is not None:
        u,v=TOPOLOGY[method]["endpoints"]
        draw.line((p[u],p[v]),fill=ink,width=5)
        names+=list(x for x in (u,v) if x not in names)
    fp=Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    font=ImageFont.truetype(str(fp),23) if fp.exists() else ImageFont.load_default()
    offsets={"A":(-30,13),"B":(14,13),"C":(1,-34),
             "D":(-7,15),"E":(14,-6),"F":(-33,-5),"P":(-29,-10),"Q":(12,-8)}
    for name in names:
        x,y=p[name]
        draw.ellipse((x-5,y-5,x+5,y+5),fill=ink)
        dx,dy=offsets[name]
        draw.text((x+dx,y+dy),name,font=font,fill=ink)
    out.parent.mkdir(exist_ok=True,parents=True)
    im.save(out)
    return out

def asset(path):
    return {"type":"image","format":"png",
            "data_base64":base64.b64encode(path.read_bytes()).decode("ascii")}

def candidate_mental(label,method):
    spec=TOPOLOGY[method]
    region1,region2=spec["regions"]
    return {
        "candidate":label,
        "new_carrier":list(spec["common_edge"]),
        "induced_mental_spaces":[
            {"id":label+"_g1","boundary_nodes":list(region1),
             "provenance":"candidate new carrier"},
            {"id":label+"_g2","boundary_nodes":list(region2),
             "provenance":"candidate new carrier"},
        ],
        "shared_boundary_nodes":list(spec["common_edge"]),
        "status":"hypothetical construction, no metric equalities",
    }

def candidate_generic(label,method):
    spec=TOPOLOGY[method]
    r1,r2=spec["regions"]
    s1=set(r1);s2=set(r2)
    return {
        "candidate":label,
        "generic_space_id":label+"_g",
        "mental_space_pair":[label+"_g1",label+"_g2"],
        "new_shared_boundary":list(spec["common_edge"]),
        "adjacent_group_roles":[
            {"space":label+"_g1","boundary_nodes":list(r1),
             "nonshared_vertices":sorted(s1-s2)},
            {"space":label+"_g2","boundary_nodes":list(r2),
             "nonshared_vertices":sorted(s2-s1)},
        ],
        "common_relation":"constructed incidence and boundary-sharing only",
        "epistemic_status":"candidate alignment; no certified equality or theorem",
    }

def make_payload(out,shape,frame,condition):
    assert condition in CONDITIONS
    certify_geometry(shape)
    mapping=anonymous_mapping(shape,frame)
    imgdir=out/"images"/shape
    assets={"base":asset(render(imgdir/"base.png",shape))}
    for code,method in mapping.items():
        assets["asset-"+code.lower()]=asset(render(imgdir/(method+".png"),shape,method))
    state={
        "workspace":"base",
        "original_mental_spaces":[
            {"id":"W_angle_A","members":["AB","AC","A"]},
            {"id":"W_angle_B","members":["BA","BC","B"]},
            {"id":"W_angle_C","members":["CA","CB","C"]},
            {"id":"W_side_AB","members":["A","AB","B"]},
            {"id":"W_side_BC","members":["B","BC","C"]},
            {"id":"W_side_AC","members":["A","AC","C"]},
        ],
        "candidate_workspace_images":[
            {"id":code,"image":"asset-"+code.lower()} for code in mapping
        ],
    }
    # A: images + common initial context; B: candidate region structures;
    # C: region structures + independently expressible generic relations.
    if condition in ("mental","generic"):
        state["candidate_mental_spaces"]=[
            candidate_mental(code,method) for code,method in mapping.items()
        ]
    if condition=="generic":
        state["candidate_generic_spaces"]=[
            candidate_generic(code,method) for code,method in mapping.items()
        ]
    question={
        "type":"choice",
        "instructions":(
            FRAME_DESCRIPTIONS[frame]+" Consider only the described structural "
            "affordance; do not infer equal lengths, equal angles or proof completion. "
            "Choose the candidate producing the most useful organization."
        ),
        "criteria":{code:"Candidate workspace asset-"+code.lower() for code in mapping},
    }
    return {"model":"jev-1.14.0","state":state,"assets":assets,
            "questions":{"best_bridge":question}},mapping

def run(out):
    if not os.environ.get("TYPESAFE_API_KEY"):
        raise SystemExit("Missing secret TYPESAFE_API_KEY; live calls not attempted")
    out.mkdir(parents=True,exist_ok=True)
    trials=[]
    for shape in SHAPES:
        for frame in FRAMES:
            for condition in CONDITIONS:
                request,mapping=make_payload(out,shape,frame,condition)
                response=call_jev(request)
                decision=response["answers"]["best_bridge"]
                selected=decision.get("choice")
                if selected not in mapping:
                    raise ValueError("Unknown Jev choice identifier")
                chosen=mapping[selected]
                expected=expected_method(frame)
                trial={
                    "shape":shape,"focus":frame,"condition":condition,
                    "mapping_offline_only":mapping,
                    "selected_id":selected,"chosen_operation":chosen,
                    "oracle_expected_operation":expected,"correct":chosen==expected,
                    "confidence":decision.get("confidence"),
                    "probabilities":decision.get("probabilities"),
                    "model":response.get("model"),
                    "usage":response.get("usage"),
                }
                trials.append(trial)
                print(f"{shape}/{frame}/{condition}: {selected}; correct={trial['correct']}")
    aggregate={}
    for condition in CONDITIONS:
        rows=[r for r in trials if r["condition"]==condition]
        aggregate[condition]={
            "correct":sum(r["correct"] for r in rows),"total":len(rows),
            "input_tokens":sum((r["usage"] or {}).get("input_tokens",0) for r in rows),
            "output_tokens":sum((r["usage"] or {}).get("output_tokens",0) for r in rows),
        }
    result={
        "experiment":"Merovingio Jev v0.7 Structural Bridge Selection",
        "meaning":"choosing a structurally fitting bridge between active conceptual spaces",
        "model_requested":"jev-1.14.0",
        "non_proof":"No theorem goal, angular/length equality or proof was supplied",
        "limits":"8 cases per condition, two shapes, three ablations; role-specific choice not automatic theorem discovery",
        "accuracy_by_condition":aggregate,
        "trials":trials,
    }
    (out/"bridge_results.json").write_text(json.dumps(result,indent=2,ensure_ascii=False))
    print("Wrote non-sensitive bridge_results.json")
    return result

if __name__=="__main__":
    run(Path(sys.argv[1] if len(sys.argv)>1 else "output_bridges"))

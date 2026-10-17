"""Merovingio v0.9: SAME geometric construction, two input channels.

A: one unannotated Euclidean diagram only (no colored group overlays).
B: symbolic incidence/betweenness facts only (no image assets).
Eight independent Jev 'noul' hypotheses ask about four possible mental-space
readings and four negative controls; no complete proof is attempted.
"""
from __future__ import annotations

import base64
import json
import math
import os
from pathlib import Path
import sys

from PIL import Image, ImageDraw, ImageFont
import requests

from fixed_workspace_reframing_v08 import A,B,C,D,geometry_checks

MODEL="jev-1.14.0"
REPETITIONS=(0,1,2,3)
CONDITIONS=("diagram","symbolic")
HYPOTHESES={
    "q01":(True,
      "Does CD divide the interior angle ACB into two adjacent angular sectors ACD and DCB?"),
    "q02":(False,
      "Does CD divide the interior angle CAB at A into two adjacent angular sectors at A?"),
    "q03":(True,
      "Does D separate the original base segment AB into two nonempty adjacent parts AD and DB?"),
    "q04":(False,
      "Does D separate segment BC into two nonempty adjacent subsegments BD and DC?"),
    "q05":(True,
      "Can segment CD be the shared boundary of the two adjacent triangular regions ACD and BCD inside ABC?"),
    "q06":(False,
      "Is CD a boundary edge of BOTH the original triangle ABC and the smaller triangle ACD?"),
    "q07":(True,
      "Does CD join the apex C of the angular fan CA and CB to an interior point D on carrier AB?"),
    "q08":(False,
      "Does CD connect a point strictly inside side CA to a point strictly inside side CB?"),
}
POINTS={"A":A,"B":B,"C":C,"D":D}
SEGMENTS=("AB","AC","BC","CD")
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def transform(p, rotation):
    # Rotate a single fixed geometry about its own center; draw labels upright.
    mx,my=485.0,325.0
    x,y=p[0]-mx,p[1]-my
    theta=math.radians(rotation)
    return (450.0+x*math.cos(theta)-y*math.sin(theta),
            450.0+x*math.sin(theta)+y*math.cos(theta))

def render_unannotated(path,rotation):
    im=Image.new("RGB",(900,900),"white")
    draw=ImageDraw.Draw(im)
    pp={name:transform(point,rotation) for name,point in POINTS.items()}
    ink="#303A48"
    # No fill, hatch, caption, angle arcs or interpretive color coding.
    for segment in SEGMENTS:
        draw.line((pp[segment[0]],pp[segment[1]]),fill=ink,width=4)
    fp=Path(FONT)
    font=ImageFont.truetype(str(fp),22) if fp.exists() else ImageFont.load_default()
    for name,(x,y) in pp.items():
        draw.ellipse((x-5,y-5,x+5,y+5),fill=ink)
        draw.text((x+10,y-29),name,font=font,fill=ink)
    path.parent.mkdir(parents=True,exist_ok=True)
    im.save(path)
    return path

def symbolic_workspace(repeat):
    # Same facts, alternate ordering only; no coordinates or given measurements.
    nodes=list(POINTS)
    segments=list(SEGMENTS)
    incidences=[
        {"point":"A","segment":"AB"},{"point":"B","segment":"AB"},
        {"point":"A","segment":"AC"},{"point":"C","segment":"AC"},
        {"point":"B","segment":"BC"},{"point":"C","segment":"BC"},
        {"point":"C","segment":"CD"},{"point":"D","segment":"CD"},
        {"point":"D","segment":"AB"}
    ]
    s=repeat%4
    return {
        "points":nodes[s:]+nodes[:s],
        "segments":segments[s:]+segments[:s],
        "incidence":incidences[s:]+incidences[:s],
        "between":[{"start":"A","middle":"D","end":"B"}],
        "non_collinear":[["A","B","C"]],
        "workspace_status":"one already drawn construction; no proof or metric assertions",
    }

def questions(repeat):
    # Questions are identical across the two conditions; only order changes.
    keys=list(HYPOTHESES)
    s=repeat%len(keys)
    keys=keys[s:]+keys[:s]
    return {
        key:{
            "type":"noul",
            "instructions":HYPOTHESES[key][1],
            "criteria":{
                "true":"This exact structural relation follows from the supplied workspace.",
                "false":"The claimed structural relation does not follow or contradicts the workspace."
            }
        } for key in keys
    }

def build_request(folder,condition,repeat):
    if condition not in CONDITIONS:raise ValueError(condition)
    payload={
      "model":MODEL,
      "state":(
        {"diagram":"workspace-image",
         "context":"One single Euclidean figure with points A, B, C, D. "
                   "Evaluate only structural incidences, partitions and shared boundaries. "
                   "Do not assume any equal lengths or angles."}
         if condition=="diagram" else symbolic_workspace(repeat)
      ),
      "questions":questions(repeat)
    }
    if condition=="diagram":
        png=render_unannotated(folder/"images"/("rotation_"+str(90*repeat)+".png"),90*repeat)
        payload["assets"]={
            "workspace-image":{
                "type":"image","format":"png",
                "data_base64":base64.b64encode(png.read_bytes()).decode("ascii")
            }
        }
    return payload

def call_api(payload):
    secret=os.getenv("TYPESAFE_API_KEY")
    if not secret:
        raise RuntimeError("TYPESAFE_API_KEY missing from Actions secrets")
    headers={"Authorization":"Bearer "+secret}
    if payload.get("assets"):
        headers["TypeSafe-Danger-Zone-Images"]="true"
    response=requests.post(
        "https://api.typesafe.ai/v1/systemone",
        headers=headers,json=payload,timeout=100)
    # Avoid leaking server-provided errors, URLs, or credential fragments.
    if not response.ok:
        raise RuntimeError("Jev API returned HTTP status "+str(response.status_code))
    data=response.json()
    if not isinstance(data.get("answers"),dict):
        raise ValueError("Jev API missing answers")
    return data

def validate_response(response):
    answers=response["answers"]
    record={}
    for ident,(expected,_) in HYPOTHESES.items():
        item=answers.get(ident)
        if not isinstance(item,dict) or item.get("type")!="noul":
            raise ValueError("Missing noul response for "+ident)
        prob=item.get("noul")
        if not isinstance(prob,(int,float)) or not 0<=prob<=1:
            raise ValueError("Invalid noul probability for "+ident)
        record[ident]={
           "p_true":prob,"expected":expected,
           "correct_at_0_5":(prob>=0.5)==expected,
           "confident_at_0_8":(prob>=0.8 if expected else prob<=0.2),
           "uncertain":0.2<prob<0.8
        }
    return record

def main(out):
    if not os.getenv("TYPESAFE_API_KEY"):
        raise SystemExit("GitHub Actions secret missing: no calls attempted")
    geometry_checks()
    out.mkdir(parents=True,exist_ok=True)
    trials=[]
    for repeat in REPETITIONS:
        for condition in CONDITIONS:
            payload=build_request(out,condition,repeat)
            response=call_api(payload)
            evaluations=validate_response(response)
            accuracy=sum(v["correct_at_0_5"] for v in evaluations.values())
            trials.append({
                "condition":condition,"repeat":repeat,
                "visual_rotation_degrees":90*repeat if condition=="diagram" else None,
                "accuracy":accuracy,"total":len(HYPOTHESES),
                "judgments":evaluations,
                "usage":response.get("usage"),
                "model":response.get("model"),
            })
            print(f"{repeat}/{condition}: {accuracy}/{len(HYPOTHESES)}")
    summary={}
    for condition in CONDITIONS:
        cases=[t for t in trials if t["condition"]==condition]
        summary[condition]={
            "correct":sum(t["accuracy"] for t in cases),
            "total":len(cases)*len(HYPOTHESES),
            "true_positive":sum(t["judgments"][k]["correct_at_0_5"] for t in cases
                                for k in HYPOTHESES if HYPOTHESES[k][0]),
            "true_total":len(cases)*sum(x[0] for x in HYPOTHESES.values()),
            "true_negative":sum(t["judgments"][k]["correct_at_0_5"] for t in cases
                                for k in HYPOTHESES if not HYPOTHESES[k][0]),
            "negative_total":len(cases)*sum(not x[0] for x in HYPOTHESES.values()),
            "input_tokens":sum((t["usage"] or {}).get("input_tokens",0) for t in cases),
            "output_tokens":sum((t["usage"] or {}).get("output_tokens",0) for t in cases),
        }
    report={
      "experiment":"Merovingio v0.9 unannotated vs purely symbolic, single workspace",
      "request_structure":"8 independent yes/no candidate propositions per scene, not text generation",
      "note":"No colored annotation or candidate diagrams. Symbolic condition has no image; symbolic facts are unmeasured incidence/betweenness.",
      "epistemic_limit":"This evaluates fixed hypotheses, NOT spontaneous invention of unknown Mental Spaces.",
      "summary":summary,"trials":trials
    }
    (out/"unannotated_symbolic_results.json").write_text(
        json.dumps(report,indent=2,ensure_ascii=False),encoding="utf-8")
    print("Saved sanitized v0.9 benchmark report.")

if __name__=="__main__":
    main(Path(sys.argv[1] if len(sys.argv)>1 else "output_v09"))

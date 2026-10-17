"""Panoptikon v1.4 — emergence of Mental and Generic Spaces across 3 modalities.

Modality: annotated image, unannotated image, or symbolic-only representation.
Same event graph in all modalities, so registration information is controlled.
No answers, oracle labels, proofs, metrical equalities across levels supplied.
"""
from __future__ import annotations
import base64
import json
import math
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import requests
import sys

SHAPES={"iso_low":(5.0,4.0),"iso_high":(5.0,8.0),
        "scalene_left":(3.2,6.4),"scalene_right":(7.1,5.2)}
MODES=("annotated","plain","symbolic")
HISTORIES=("upper_first","lower_first")
STAGES=(0,1,2)
MODEL="jev-1.14.0"
A=(0.0,0.0);B=(10.0,0.0)
QUESTIONS={
 "registered_apex":{
   "type":"noul",
   "instructions":"By this stage of the recorded construction history, has the Mental Space partitioning the apex-angle fan at C been explicitly activated?",
   "criteria":{"true":"The upper angular grouping is registered.","false":"The upper angular grouping has not yet been registered."}
 },
 "registered_base":{
   "type":"noul",
   "instructions":"By this stage of the recorded construction history, has the Mental Space pairing the two right-angle sectors at the foot on AB been explicitly activated?",
   "criteria":{"true":"The base-right-angle grouping is registered.","false":"The base-right-angle grouping has not yet been registered."}
 },
 "joint_abstract":{
   "type":"noul",
   "instructions":"Are BOTH angular Mental Spaces already registered so that a two-pair left/right generic correspondence can now be PROPOSED without claiming metric equality or shared material support?",
   "criteria":{"true":"Both source spaces are registered and permit a candidate role alignment.","false":"At least one source space has not yet been registered."}
 },
 "joint_carrier":{
   "type":"noul",
   "instructions":"Are BOTH upper and lower angular Mental Spaces already registered AND do they use exactly the same physical construction carrier?",
   "criteria":{"true":"Both registered pairs refer to one identical physical segment.","false":"A source space is unregistered or the carriers differ."}
 },
 "cross_metric":{
   "type":"noul",
   "instructions":"Has the construction CERTIFIED that the upper half-angle has equal angular measure to the adjacent base right angle?",
   "criteria":{"true":"The cross-level metric equality has been certified.","false":"No cross-level equality certificate exists."}
 },
 "next_focus":{
   "type":"choice",
   "instructions":"Which already-described conceptual direction would be most useful to inspect next? This is exploratory salience, not a geometrically correct single answer. Distinguish registered interpretations from merely geometrically possible properties.",
   "criteria":{
     "upper":"Inspect the apex-angle Mental Space.",
     "lower":"Inspect the base-right-angle Mental Space.",
     "abstract":"Inspect a possible abstract alignment of two registered left/right angular pairs.",
     "same_carrier":"Inspect a possible joint mapping through one shared material carrier."
   }
 },
}
def dist(p,q):return math.hypot(p[0]-q[0],p[1]-q[1])
def geometry(shape):
    C=SHAPES[shape]
    frac=dist(A,C)/(dist(A,C)+dist(B,C))
    E=(10*frac,0.0)
    H=(C[0],0.0)
    coincides=dist(E,H)<1e-7
    iso=abs(dist(A,C)-dist(B,C))<1e-7
    assert coincides==iso
    if coincides:
        pos={"A":A,"B":B,"C":C,"D":E}
        support={"upper":("C","D"),"lower":("C","D")}
    else:
        pos={"A":A,"B":B,"C":C,"E":E,"H":H}
        support={"upper":("C","E"),"lower":("C","H")}
    return {"points":pos,"supports":support,"same_support":coincides}

def events(history,stage):
    assert history in HISTORIES and stage in STAGES
    sequence=("OP_APEX","OP_FOOT") if history=="upper_first" else ("OP_FOOT","OP_APEX")
    # Always expose only performed events in the recorded history, not the future events.
    return [{"time":i+1,"operator":name,"source_domain":
             ("angle_fan" if name=="OP_APEX" else "base_straight_angle"),
             "result_type":("sector_partition" if name=="OP_APEX" else "right_angle_partition")}
             for i,name in enumerate(sequence[:stage])]

def registered(history,stage):
    observed={e["operator"] for e in events(history,stage)}
    return {"upper":"OP_APEX" in observed,"lower":"OP_FOOT" in observed}

def material_segments(geo,history,stage):
    seg=[("A","B"),("A","C"),("B","C")]
    for e in events(history,stage):
        edge=geo["supports"]["upper" if e["operator"]=="OP_APEX" else "lower"]
        if edge not in seg:seg.append(edge)
    return seg

def rotated_xy(pt,shape):
    # Fixed display scale; no per-stage scaling that could leak the event.
    return (120+pt[0]*62,610-pt[1]*54)

def draw(path,shape,history,stage,annotated):
    g=geometry(shape)
    im=Image.new("RGB",(870,740),"white")
    d=ImageDraw.Draw(im)
    xy={k:rotated_xy(p,shape) for k,p in g["points"].items()}
    drawn=material_segments(g,history,stage)
    active=registered(history,stage)
    # Annotation intentionally shows only registrations, never geometry certificates.
    if annotated:
        if active["upper"]:
            x,y=xy["C"]
            d.ellipse((x-35,y-35,x+35,y+35),outline="#C97028",width=4)
        if active["lower"]:
            f="D" if g["same_support"] else "H"
            x,y=xy[f]
            d.rectangle((x-14,y-14,x+14,y+14),outline="#258B9B",width=4)
    for u,v in drawn:
        d.line((xy[u],xy[v]),fill="#343B44",width=4)
    fp=Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    font=ImageFont.truetype(str(fp),23) if fp.exists() else ImageFont.load_default()
    vertices=set(sum(([a,b] for a,b in drawn),[]))
    for label in sorted(vertices):
        x,y=xy[label]
        d.ellipse((x-5,y-5,x+5,y+5),fill="#343B44")
        d.text((x+8,y-28),label,fill="#343B44",font=font)
    path.parent.mkdir(parents=True,exist_ok=True)
    im.save(path)
    return path

def initial_state(geo,history,stage):
    """Shared across modes; registration trace is not a target label."""
    return {
      "process_clock":{"stage":stage,"completed_events":events(history,stage)},
      "workspace_context":{
         "origin":"initial triangle ABC with straight base AB",
         "operator_legend":{
           "OP_APEX":"create a partition of the angular fan anchored at C",
           "OP_FOOT":"create the right-angle partition at the base contact"
         },
         "epistemic_rule":"geometric possibility, current registration, and certified metric equality are distinct",
      }
    }

def make_request(out,shape,history,stage,mode):
    assert mode in MODES
    geo=geometry(shape)
    state=initial_state(geo,history,stage)
    image_assets={}
    if mode in ("annotated","plain"):
        path=draw(out/"images"/shape/(mode+"_"+history+"_"+str(stage)+".png"),
                  shape,history,stage,annotated=(mode=="annotated"))
        asset_name="w"
        image_assets[asset_name]={
          "type":"image","format":"png",
          "data_base64":base64.b64encode(path.read_bytes()).decode("ascii")
        }
        state["workspace_image"]=asset_name
        state["image_note"]="Image contains one workspace snapshot, not competing answers."
    else:
        # The same material stage, represented ONLY via primitive symbolic objects.
        edges=material_segments(geo,history,stage)
        state["material_graph"]={
           "points":sorted(set(sum(([u,v] for u,v in edges),[]))),
           "carrier_endpoints":[{"a":u,"b":v} for u,v in edges],
           "incidence":[{"point":u,"carrier":u+v} for u,v in edges]+
                       [{"point":v,"carrier":u+v} for u,v in edges],
           "on_AB":[geo["supports"]["upper"][1] if e["operator"]=="OP_APEX"
                    else geo["supports"]["lower"][1]
                    for e in events(history,stage)],
           "remark":"No candidate Generic Space, theorem or metric certificate is supplied.",
        }
    req={"model":MODEL,"state":state,"questions":QUESTIONS}
    if image_assets:req["assets"]=image_assets
    return req

def expected(shape,history,stage):
    geo=geometry(shape);r=registered(history,stage)
    return {
      "registered_apex":r["upper"],
      "registered_base":r["lower"],
      "joint_abstract":r["upper"] and r["lower"],
      "joint_carrier":r["upper"] and r["lower"] and geo["same_support"],
      "cross_metric":False
    }

def api(req):
    secret=os.getenv("TYPESAFE_API_KEY")
    if not secret:raise RuntimeError("TYPESAFE_API_KEY secret is not available")
    headers={"Authorization":"Bearer "+secret}
    if req.get("assets"): headers["TypeSafe-Danger-Zone-Images"]="true"
    response=requests.post("https://api.typesafe.ai/v1/systemone",
                           json=req,headers=headers,timeout=90)
    if response.status_code!=200:
        raise RuntimeError("Jev API status "+str(response.status_code))
    output=response.json()
    if set(QUESTIONS)-set(output.get("answers",{})):
        raise ValueError("Incomplete TypeSafe answers")
    return output

def result_of(reply,truth):
    judgments={}
    for name,target in truth.items():
        q=reply["answers"][name]
        prob=q.get("noul")
        if not isinstance(prob,(float,int)) or not 0<=prob<=1:
            raise ValueError("Expected Noul probability for "+name)
        judgments[name]={"p_true":prob,"truth":target,"correct":(prob>=0.5)==target}
    sel=reply["answers"]["next_focus"]
    if sel.get("choice") not in QUESTIONS["next_focus"]["criteria"]:
        raise ValueError("Invalid salience choice")
    return judgments,{"choice":sel.get("choice"),"probabilities":sel.get("probabilities"),
                      "confidence":sel.get("confidence")}

def run(out):
    if not os.getenv("TYPESAFE_API_KEY"):
        raise SystemExit("Missing GitHub Actions secret; no API calls")
    out.mkdir(parents=True,exist_ok=True)
    rows=[]
    for shape in SHAPES:
        for hist in HISTORIES:
            for stage in STAGES:
                truth=expected(shape,hist,stage)
                for mode in MODES:
                    req=make_request(out,shape,hist,stage,mode)
                    reply=api(req)
                    judgments,focus=result_of(reply,truth)
                    line={"shape":shape,"history":hist,"stage":stage,"mode":mode,
                          "truth_scoring_only":truth,"judgments":judgments,
                          "focus":focus,"usage":reply.get("usage"),
                          "model":reply.get("model")}
                    rows.append(line)
                    print(shape,hist,stage,mode,
                          sum(q["correct"] for q in judgments.values()),"/5",flush=True)
    summary={}
    for mode in MODES:
        sub=[r for r in rows if r["mode"]==mode]
        summary[mode]={
           "correct":sum(q["correct"] for x in sub for q in x["judgments"].values()),
           "total":5*len(sub),
           "by_question":{q:{
             "correct":sum(x["judgments"][q]["correct"] for x in sub),
             "total":len(sub)}
             for q in expected("iso_low","upper_first",0)},
           "input_tokens":sum((x["usage"] or {}).get("input_tokens",0) for x in sub),
           "output_tokens":sum((x["usage"] or {}).get("output_tokens",0) for x in sub),
        }
    report={
       "experiment":"Panoptikon v1.4 emergence across three representations",
       "model":MODEL,"call_count":len(rows),
       "epistemic_note":"Geometric affordance may predate cognitive registration. Stage snapshots explicitly encode observed registrations in typed event history shared by all modalities.",
       "limits":"Typed questions are authored. This tests recognition of registration and proposed correspondences, NOT free discovery of novel spaces.",
       "summary":summary,"trials":rows
    }
    (out/"emergence_v14_results.json").write_text(
        json.dumps(report,indent=2,ensure_ascii=False),encoding="utf-8")
    print("Saved sanitized v1.4 report")
if __name__=="__main__":
    run(Path(sys.argv[1] if len(sys.argv)>1 else "output"))

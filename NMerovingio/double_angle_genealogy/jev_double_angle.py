"""Jev genealogy probe: co-emergence of two angle pairs around one divider.

Compares final-only, historical and reversed event serialization across both
plain images and purely symbolic states. Structural correspondence is distinct
from metric equality. No geometric proof is delegated to Jev.
"""
from __future__ import annotations
import base64
import json
import os
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import requests

from core import GEOMETRIES, HISTORIES, derive, genealogy, benchmark

MODEL="jev-1.14.0"
QUESTIONS={
 "shared": {
  "type":"noul",
  "instructions":(
   "Are the pair of upper apex-angle sectors and the pair of lower right-angle "
   "sectors organized on the SAME physical constructed divider, so their left "
   "and right roles can be aligned without claiming equality of angle measure?"
  ),
  "criteria":{"true":"Both pairs use one common constructed carrier.",
              "false":"They do not share a single constructed carrier."}
 },
 "cross_equal":{
  "type":"noul",
  "instructions":(
    "Does this configuration logically require each upper half-angle to be "
    "equal in angular measure to the corresponding lower right angle?"
  ),
  "criteria":{"true":"Cross-level angle measures must coincide.",
              "false":"No such cross-level equality follows."}
 },
 "focus":{
  "type":"choice",
  "instructions":(
   "Which organization deserves priority for the next exploratory cognitive "
   "step? There is no uniquely correct salience ranking. Use the construction "
   "history only when provided, while distinguishing structural analogy from "
   "equal angular measures."
  ),
  "criteria":{
    "upper":"Explore the two adjoining angular sectors at the apex.",
    "lower":"Explore the two right-angle sectors at the base intersection.",
    "joint":"Explore a coupled left-right role alignment between the two angle pairs.",
    "abstract":"Explore the more abstract analogy between two partitions without assuming one shared carrier."
  }
 }
}

def fig(path,geo):
    p=geo["points"]
    im=Image.new("RGB",(880,720),"white")
    d=ImageDraw.Draw(im)
    col="#353D45"
    def xy(v):
        x,y=p[v]
        return (120+x*62,600-y*55)
    for s in geo["segments"]:
        d.line([xy(s[0]),xy(s[1])],fill=col,width=4)
    font_file=Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    font=ImageFont.truetype(str(font_file),23) if font_file.exists() else ImageFont.load_default()
    offs={"A":(-26,6),"B":(12,6),"C":(6,-31),
          "D":(-7,13),"E":(-17,13),"H":(9,13)}
    for name in p:
        x,y=xy(name)
        d.ellipse([x-5,y-5,x+5,y+5],fill=col)
        dx,dy=offs[name]
        d.text((x+dx,y+dy),name,fill=col,font=font)
    path.parent.mkdir(exist_ok=True,parents=True)
    im.save(path)
    return path

def no_history_state(geo,modality,path):
    # Frozen FINAL STATE input invariant under history choice.
    if modality=="image":
        return ({
           "description":"One Euclidean workspace, unannotated. "
                         "Consider topological angle-pair groupings, not equal-angle proofs.",
           "image":"im-workspace"
         },
         {"im-workspace":{
             "type":"image","format":"png",
             "data_base64":base64.b64encode(fig(path,geo).read_bytes()).decode("ascii")
         }})
    if modality!="symbolic":raise ValueError(modality)
    # Symbolic-only: certified relations but NOT the derived alignment target.
    inc=[{"carrier":s,"endpoints":list(s)} for s in geo["segments"]]
    return ({
       "points":list(geo["points"]),
       "carriers":inc,
       "base":"AB",
       "on_base":["D"] if geo["kind"]=="isosceles" else ["E","H"],
       "angular_partition":{
          "apex":"C","carrier":geo["carriers"]["upper"],
          "two_sectors":[geo["angles"]["upper_left"],geo["angles"]["upper_right"]],
          "relative_measure":"two upper sectors of equal measure"
       },
       "right_angle_pair":{
          "base":"AB","carrier":geo["carriers"]["lower"],
          "two_sectors":[geo["angles"]["lower_left"],geo["angles"]["lower_right"]],
          "individual_measure":"right angles"
       },
       "constraints":"Do not assume an upper sector has the measure of any foot sector.",
    },{})

def payload(shape,history,modality,condition,out):
    if condition not in ("final","chronological","reverse_list"):
        raise ValueError(condition)
    if history not in HISTORIES:raise ValueError(history)
    geo=derive(shape)
    state,assets=no_history_state(geo,modality,out/"images"/(shape+".png"))
    state=dict(state)
    if condition!="final":
        records=genealogy(shape,history)["events"]
        rows=[{"step":e["step"],"operator":e["operator"],
               "source_domain":e["source_domain"],
               "new_roles":e["observed_roles"]} for e in records]
        # Reverse the PRESENTATION order; preserve numerical event steps.
        if condition=="reverse_list":
            rows=list(reversed(rows))
        state["construction_events"]=rows
        state["history_instruction"]="Event step numbers define chronological order."
    request={"model":MODEL,"state":state,"questions":QUESTIONS}
    if assets:
        request["assets"]=assets
    return request

def call(request):
    key=os.environ.get("TYPESAFE_API_KEY")
    if not key:raise RuntimeError("Missing TYPESAFE_API_KEY")
    headers={"Authorization":"Bearer "+key}
    if request.get("assets"):headers["TypeSafe-Danger-Zone-Images"]="true"
    resp=requests.post("https://api.typesafe.ai/v1/systemone",
                       json=request,headers=headers,timeout=90)
    if resp.status_code!=200:
        raise RuntimeError("Jev returned HTTP "+str(resp.status_code))
    body=resp.json()
    answers=body.get("answers",{})
    if not all(key in answers for key in QUESTIONS):
        raise ValueError("Incomplete Jev response")
    ans={}
    for k in ("shared","cross_equal"):
        p=answers[k].get("noul")
        if not isinstance(p,(int,float)) or not 0<=p<=1:
            raise ValueError("Invalid Jev noul")
        ans[k]=float(p)
    chosen=answers["focus"].get("choice")
    if chosen not in QUESTIONS["focus"]["criteria"]:
        raise ValueError("Invalid focus choice")
    ans["focus_choice"]=chosen
    ans["focus_probs"]=answers["focus"].get("probabilities")
    ans["focus_confidence"]=answers["focus"].get("confidence")
    ans["usage"]=body.get("usage")
    ans["model"]=body.get("model")
    return ans

def cases():
    # The two isosceles final-only records repeat identically for both
    # genealogies; a single final-only probe per shape/modality is sufficient.
    entries=[]
    for shape in ("iso_low","iso_high"):
        for modality in ("symbolic","image"):
            entries.append((shape,"apex_first",modality,"final"))
        for history in HISTORIES:
            for modality in ("symbolic","image"):
                entries.append((shape,history,modality,"chronological"))
            entries.append((shape,history,"symbolic","reverse_list"))
    for shape in ("scalene_left","scalene_right"):
        for history in HISTORIES:
            for modality in ("symbolic","image"):
                entries.append((shape,history,modality,"chronological"))
    return entries

def run(out):
    if not os.getenv("TYPESAFE_API_KEY"):
        raise SystemExit("GitHub secret missing; no model call")
    out.mkdir(parents=True,exist_ok=True)
    benchmark_result=benchmark()
    (out/"geometry.json").write_text(json.dumps(benchmark_result,indent=2))
    records=[]
    for shape,history,modality,condition in cases():
        request=payload(shape,history,modality,condition,out)
        result=call(request)
        geo=derive(shape)
        entry={
           "shape":shape,"history":history,"modality":modality,
           "condition":condition,"ground_truth_shared_carrier":geo["certified"]["same_carrier"],
           "ground_truth_cross_level_equality":False,
           **result
        }
        entry["shared_correct"]=(entry["shared"]>=0.5)==entry["ground_truth_shared_carrier"]
        entry["cross_equal_correct"]=entry["cross_equal"]<0.5
        records.append(entry)
        print(shape,history,modality,condition,
              "p_shared=",round(entry["shared"],3),"focus=",entry["focus_choice"])
    aggregate={}
    for modality in ("symbolic","image"):
        rows=[r for r in records if r["modality"]==modality]
        aggregate[modality]={
          "shared_correct":sum(r["shared_correct"] for r in rows),
          "cross_equal_correct":sum(r["cross_equal_correct"] for r in rows),
          "total":len(rows)
        }
    report={
      "experiment":"Panoptikon v1.1 paired angular spaces and genealogy",
      "hypothesis":"relative salience and joint correspondence may vary with space genesis",
      "limitations":"No unique correct focus; paired role alignment is distinct from angular-measure equality. Repeats and mirror-like shapes are not independent evidence.",
      "n_calls":len(records),
      "summary":aggregate,
      "records":records
    }
    (out/"jev_double_angle_results.json").write_text(json.dumps(report,indent=2))
    print("Wrote sanitized report",len(records),"calls")

if __name__=="__main__":
    import sys
    run(Path(sys.argv[1] if len(sys.argv)>1 else "output"))

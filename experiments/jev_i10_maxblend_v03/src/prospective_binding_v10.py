"""Run an authenticated Jev prospective-binding trial, with memory/no-source ablation.

Jev selects a proposed construction, and code independently validates resulting
role bindings. No correct method names or checker results enter Jev state.
"""
from __future__ import annotations
import base64,json,os,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont

from prototype import call_jev
from structural_bridges_v07 import render as render_triangle
from prospective_memory_v10 import (
  read_memory,propose,source_binding,verifier_after_choice,
  rank_candidates_heuristic,memory_priority
)

SCENES=(
 ("triangle","left",0),("triangle","right",1),
 ("triangle","left",2),("triangle","right",3),
 ("circle","standard",0),("circle","standard",1),
 ("circle","standard",2),("circle","standard",3),
 ("negative","left",0),("negative","right",1)
)
MODES=("schema_only","historical_memory")

def render_circle(out,method=None):
 im=Image.new("RGB",(880,730),"white")
 d=ImageDraw.Draw(im);fg="#39434F"
 A=(320,360);B=(520,360);r=200
 d.ellipse((A[0]-r,A[1]-r,A[0]+r,A[1]+r),outline=fg,width=4)
 d.line((A,B),fill=fg,width=4)
 if method in ("circle_opposite_same_radius","circle_opposite_short_radius"):
  rr=r if method=="circle_opposite_same_radius" else 140
  d.ellipse((B[0]-rr,B[1]-rr,B[0]+rr,B[1]+rr),outline=fg,width=4)
 elif method=="circle_same_center":
  d.ellipse((A[0]-r,A[1]-r,A[0]+r,A[1]+r),outline=fg,width=4)
 elif method=="midpoint_line":
  d.line((420,100,420,620),fill=fg,width=4)
 for name,(x,y) in [("A",A),("B",B)]:
  d.ellipse((x-5,y-5,x+5,y+5),fill=fg)
  d.text((x-9,y+16),name,fill=fg)
 out.parent.mkdir(parents=True,exist_ok=True)
 im.save(out)
 return out

def render_scenario(out,case,shape,method=None):
 if case=="circle":return render_circle(out,method)
 return render_triangle(out,shape,method)

def image_asset(path):
 return {"type":"image","format":"png","data_base64":base64.b64encode(path.read_bytes()).decode("ascii")}

def option_mapping(case,shift):
 methods=propose(case)
 sequence=methods[shift:]+methods[:shift]
 return {"K"+str(i+1):method for i,method in enumerate(sequence)}

def build_payload(out,case,shape,shift,mode):
 assert mode in MODES
 item=read_memory(case)
 binding=source_binding(case)
 mapping=option_mapping(case,shift)
 imgdir=out/"images"/case/shape
 assets={"initial":image_asset(render_scenario(imgdir/"initial.png",case,shape))}
 for code,method in mapping.items():
  assets["view-"+code.lower()]=image_asset(render_scenario(imgdir/(method+".png"),case,shape,method))
 missing=list(binding["slots"]["missing"])
 active=list(binding["slots"]["workspace_current"])
 state={
  "current_workspace_image":"initial",
  "active_mental_spaces":active,
  "existing_role_bindings":list(binding["slots"]["already_bound"]),
  "unfilled_generic_roles":missing,
  "candidate_images":[{"id":code,"image":"view-"+code.lower()} for code in mapping],
  "epistemic_status":"prospective only: missing roles are not yet certified",
 }
 if mode=="historical_memory":
  state["retrieved_generic_space"]={
   "memory_id":item["id"],
   "historical_origin":item["provenance"]["workspace_id"] or item["provenance"]["proposition_id"],
   "source_file":item["provenance"]["file"],
   "abstract_relation_roles":[
      {"role":r["role"],"relation":r["relation"]} for r in item["abstract_roles"]
   ],
   "memory_status":"template from an earlier workspace, not a proof",
  }
 if case=="triangle":
  instruction=(
    "We have a triangle with active apex C and opposite base AB. "
    "Find the hypothetical construction that could instantiate the outstanding "
    "roles of a pair of adjacent triangular Mental Spaces having a common new "
    "carrier. Do not assume any equality or congruence. "
    "Choose one candidate workspace; the geometry engine will verify it."
  )
 elif case=="circle":
  instruction=(
    "The current workspace has only segment AB and one circle, centered on A "
    "with radius AB. Which candidate new construction is most likely to complete "
    "the missing linked-radius and shared-intersection roles of the abstract "
    "Generic Space? Prefer preserving a common material radius across "
    "the circle Gestalten. Geometric checks will happen afterward."
  )
 else:
  instruction=(
    "A stored theorem-role template concerns a transfer from established "
    "equal side lengths to corresponding equal angles. No equal side lengths "
    "are certified in the current workspace. Which candidate construction "
    "alone safely COMPLETES the missing certified premise AND the licensed "
    "theorem relation? If none is sufficient, choose none. "
    "Do not mistake adding a segment for proving a metric equality."
  )
 criteria={code:"Hypothetical workspace view-"+code.lower() for code in mapping}
 if case=="negative":
  criteria["none"]="No candidate fills the missing certified roles"
 else:
  instruction+=" Choose only among the four candidate images."
 return {"model":"jev-1.14.0","assets":assets,"state":state,
         "questions":{"best_bridge":{"type":"choice","instructions":instruction,"criteria":criteria}}
        },mapping

def main(out):
 if not os.getenv("TYPESAFE_API_KEY"):
  raise SystemExit("No TYPESAFE_API_KEY configured, no live call made")
 out.mkdir(exist_ok=True,parents=True)
 report=[]
 for case,shape,shift in SCENES:
  for mode in (MODES if case!="negative" else ("historical_memory",)):
   payload,mapping=build_payload(out,case,shape,shift,mode)
   response=call_jev(payload)
   answer=response["answers"]["best_bridge"]
   code=answer.get("choice")
   if code not in mapping and not(case=="negative" and code=="none"):
    raise ValueError("Invalid Jev choice id")
   chosen=mapping.get(code)
   verify=verifier_after_choice(case,shape,chosen)
   scored=rank_candidates_heuristic(case,shape)
   record={
    "case":case,"shape":shape,"shift":shift,"mode":mode,
    "memory_id":read_memory(case)["id"],
    "memory_provenance":read_memory(case)["provenance"],
    "available_preconstruction":list(source_binding(case)["slots"]["already_bound"]),
    "unfilled_preconstruction":list(source_binding(case)["slots"]["missing"]),
    "offline_candidate_mapping":mapping,
    "model_choice":code,"chosen_method":chosen,
    "verifier_after_model_choice":verify,
    "independent_oracle_score_per_method":scored,
    "correct":verify["successful_completion"] if case!="negative" else code=="none",
    "choice_confidence":answer.get("confidence"),
    "probabilities":answer.get("probabilities"),
    "usage":response.get("usage"),
   }
   report.append(record)
   print(f"{case}/{shape}/{shift}/{mode}: choice={code}; independently verified={record['correct']}")
 aggregates={}
 for mode in MODES:
  records=[r for r in report if r["mode"]==mode]
  aggregates[mode]={
   "correct":sum(r["correct"] for r in records),"total":len(records),
   "input_tokens":sum((r["usage"] or {}).get("input_tokens",0) for r in records),
   "output_tokens":sum((r["usage"] or {}).get("output_tokens",0) for r in records)
  }
 overall={
  "experiment":"Merovingio v1.0 Prospective Generic Binding",
  "status":"LIVE_JEV_API",
  "purpose":"memory-guided proposal ranking with independently verified prospective slots",
  "model_requested":"jev-1.14.0",
  "accuracy_by_mode":aggregates,
  "trials":report,
  "limits":[
   "Source memory is previously curated, not autonomously induced.",
   "Candidate construction generation is deterministic, not performed by Jev.",
   "Model receives prospective role schema, never an oracle mapping or metric conclusion.",
   "Historical-memory versus schema-only is not a blind control: role language is shared.",
   "A successful geometric construction does not constitute a theorem proof."
  ]
 }
 (out/"prospective_results.json").write_text(json.dumps(overall,indent=2,ensure_ascii=False),encoding="utf-8")
 print("Saved prospective_results.json, without API credentials")
 return overall

if __name__=="__main__":
 main(Path(sys.argv[1] if len(sys.argv)>1 else "output_prospective"))

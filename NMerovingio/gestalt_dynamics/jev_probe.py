"""Jev exploratory probe: effect of construction genealogy on salience ranking.

No ground-truth 'best' salience exists. This is NOT a proof of discovery.
Authenticated API is only called in the CI stage with the repository secret.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import requests
from core import ROLE_SCHEMA,run_deterministic

CHOICES={
 "base_AD_DB":"Attend to the original segment as two adjacent carriers.",
 "angular_ACD_DCB":"Attend to two sectors adjacent at the apex.",
 "regions_ACD_BCD":"Attend to the two closed triangular regions and their shared boundary.",
 "bridge_angle_base":"Attend to CD as a link between angular and segment domains.",
}
QUESTION={
 "type":"choice",
 "instructions":(
   "Which reading of this one finished workspace deserves the most attention "
   "for further structural exploration? Several readings are valid. When "
   "a construction history is present, consider how the observations arose "
   "without inferring equal measures or a theorem. Select one to explore next."
 ),
 "criteria":{k:v for k,v in CHOICES.items()}
}

def model_payload(history,with_genealogy):
    end=history["final_material"]
    state={
      "material_points":end["points"],
      "material_segments":end["segments"],
      "candidate_readings":[
        {"id":k,"members":ROLE_SCHEMA[k]["members"],
         "domain":ROLE_SCHEMA[k]["domain"],"status":ROLE_SCHEMA[k]["status"]}
        for k in CHOICES
      ],
      "epistemic_note":"all choices are meaningful; no mathematically unique most-salient reading"
    }
    if with_genealogy:
        state["construction_history"]=[
            {"action":event["action"],"genealogy":event["genealogy"]}
            for event in history["events"]
        ]
        state["activation_order"]=[
            {"stage":x["stage"],"new_readings":[k for k in x["first_appearances"]
                                            if k in CHOICES]}
            for x in history["snapshots"]
        ]
    return {"model":"jev-1.14.0","state":state,
            "questions":{"focus":QUESTION}}

def call(payload):
    key=os.getenv("TYPESAFE_API_KEY")
    if not key: raise RuntimeError("Missing GitHub Actions TypeSafe secret")
    result=requests.post(
      "https://api.typesafe.ai/v1/systemone",
      headers={"Authorization":"Bearer "+key},
      json=payload,timeout=90
    )
    if result.status_code!=200:
        raise RuntimeError("Jev API HTTP "+str(result.status_code))
    response=result.json()
    choice=response.get("answers",{}).get("focus",{})
    selected=choice.get("choice")
    if selected not in CHOICES:
        raise ValueError("Jev returned an invalid choice")
    return {
      "selected":selected,
      "confidence":choice.get("confidence"),
      "probabilities":choice.get("probabilities"),
      "usage":response.get("usage"),
      "model":response.get("model")
    }

def main():
    if not os.getenv("TYPESAFE_API_KEY"):
        raise SystemExit("Missing TYPESAFE_API_KEY; no API calls made")
    report=run_deterministic()
    results=[]
    for h in report["histories"]:
        for mode in (False,True):
            payload=model_payload(h,mode)
            response=call(payload)
            results.append({
               "genealogy":h["genealogy"],
               "condition":"history_aware" if mode else "final_only",
               **response
            })
            print(h["genealogy"],"with genealogy:",mode,"choice:",response["selected"])
    out=Path("output/jev_genealogy_probe.json")
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps({
       "experiment":"Exploratory Jev genealogy-sensitive ranking",
       "status":"LIVE_JEV_ONLY_IF_SCRIPT_COMPLETES",
       "note":"No correct target: different probabilities are observations, not verified discovery.",
       "n_calls":len(results),"results":results
    },indent=2,ensure_ascii=False))
    print("Stored sanitized Jev results")

if __name__=="__main__":
    main()

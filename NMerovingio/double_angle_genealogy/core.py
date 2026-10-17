"""Panoptikon v1.1 — double angular-pair genealogy.

One apex-angle partition and one base-right-angle partition may share the
same physical divider. An isosceles triangle makes their carriers coincide;
a scalene control yields distinct carriers. Equality ACROSS the two angle
levels is NEVER claimed. Candidate correspondence is a role analogy only.
"""
from __future__ import annotations
from dataclasses import dataclass
from hashlib import sha256
import json
import math

A=(0.0,0.0); B=(10.0,0.0)
GEOMETRIES={
 "iso_low":(5.0,4.0),
 "iso_high":(5.0,8.0),
 "scalene_left":(3.2,6.4),
 "scalene_right":(7.1,5.2),
}
HISTORIES=("apex_first","base_first")

def dist(p,q): return math.hypot(p[0]-q[0],p[1]-q[1])
def fraction_angle_bisector(c):
    return dist(A,c)/(dist(A,c)+dist(c,B))
def derive(shape):
    c=GEOMETRIES[shape]
    foot=(c[0],0.0)
    apex_end=(10.0*fraction_angle_bisector(c),0.0)
    coincidence=dist(foot,apex_end)<1e-8
    isosceles=abs(dist(A,c)-dist(B,c))<1e-8
    assert coincidence==isosceles
    # Independent exact (coordinate-based) checks of right angle and
    # partition. Neither fact licenses cross-level angle equality.
    def angle(p,v,q):
        u=(p[0]-v[0],p[1]-v[1])
        w=(q[0]-v[0],q[1]-v[1])
        cosine=(u[0]*w[0]+u[1]*w[1])/(math.hypot(*u)*math.hypot(*w))
        return math.degrees(math.acos(max(-1.,min(1.,cosine))))
    half_1=angle(A,c,apex_end)
    half_2=angle(apex_end,c,B)
    base_left=angle(A,foot,c)
    base_right=angle(c,foot,B)
    assert abs(half_1-half_2)<1e-6
    assert abs(base_left-90.)<1e-6
    assert abs(base_right-90.)<1e-6
    assert half_1<90.
    if coincidence:
        points={"A":A,"B":B,"C":c,"D":foot}
        lines=["AB","AC","BC","CD"]
        angles={
          "upper_left":"ACD","upper_right":"DCB",
          "lower_left":"ADC","lower_right":"CDB"}
        carriers={"upper":"CD","lower":"CD"}
    else:
        points={"A":A,"B":B,"C":c,"E":apex_end,"H":foot}
        lines=["AB","AC","BC","CE","CH"]
        angles={
          "upper_left":"ACE","upper_right":"ECB",
          "lower_left":"AHC","lower_right":"CHB"}
        carriers={"upper":"CE","lower":"CH"}
    return {
      "shape":shape,"kind":"isosceles" if coincidence else "scalene",
      "points":points,"segments":lines,
      "angles":angles,"carriers":carriers,
      "carrier_coincidence_verified":coincidence,
      "apex_half_degrees":round(half_1,7),
      "base_right_degrees":90.0,
      "certified":{
        "apex_sectors_equal":True,
        "base_angles_right":True,
        "same_carrier":coincidence,
        "cross_level_angles_equal":False,
      }
    }

def material_fingerprint(g):
    state={"points":g["points"],"segments":g["segments"]}
    return sha256(json.dumps(state,sort_keys=True).encode()).hexdigest()

def event_sequence(g,history):
    if history not in HISTORIES:raise ValueError(history)
    upper={
      "operator":"construct_angle_bisector",
      "produces":["upper_left","upper_right"],
      "observed_roles":["apex_left_sector","apex_right_sector"],
      "source_domain":"apex_angle"
    }
    lower={
      "operator":"construct_apex_to_base_normal",
      "produces":["lower_left","lower_right"],
      "observed_roles":["foot_left_right_angle","foot_right_right_angle"],
      "source_domain":"straight_base_angle"
    }
    first,second=(upper,lower) if history=="apex_first" else (lower,upper)
    return [{**first,"step":1},{**second,"step":2}]

def genealogy(shape,history):
    g=derive(shape)
    events=event_sequence(g,history)
    timelines=[]
    seen=[]
    for e in events:
        seen.extend(e["produces"])
        timelines.append({"step":e["step"],"emerged_spaces":list(e["produces"])})
    if g["carrier_coincidence_verified"]:
        generic={
          "status":"candidate",
          "pair_mapping":{
            "upper_left":"lower_left",
            "upper_right":"lower_right"
          },
          "common_support":g["carriers"]["upper"],
          "cross_level_metric_equality":False,
          "emergence_stage":2,
          "meaning":"two independent pairs of left-right roles share one carrier"
        }
    else:
        generic={
          "status":"candidate_abstract_only",
          "pair_mapping":{
            "upper_left":"lower_left",
            "upper_right":"lower_right"
          },
          "common_support":None,
          "cross_level_metric_equality":False,
          "emergence_stage":2,
          "meaning":"two partition pairs admit an abstract binary analogy, with distinct carriers"
        }
    return {
        "history":history,
        "shape":shape,
        "events":events,
        "snapshots":timelines,
        "first_emergence":{
            name: e["step"] for e in events for name in e["produces"]},
        "candidate_generic_space":generic,
        "final_material_fingerprint":material_fingerprint(g)
    }

def benchmark():
    cases=[]
    for shape in GEOMETRIES:
        g=derive(shape)
        apex=genealogy(shape,"apex_first")
        base=genealogy(shape,"base_first")
        assert apex["final_material_fingerprint"]==base["final_material_fingerprint"]
        assert apex["first_emergence"]!=base["first_emergence"]
        assert not g["certified"]["cross_level_angles_equal"]
        cases.append({
           "shape":shape,
           "geometry":g,
           "histories":[apex,base],
           "epistemic_note":"Corresponding means matching relational roles, not matching angle measure."
        })
    return {
       "experiment":"Panoptikon double angular-pair genealogy v1.1",
       "status":"deterministic geometry + authored candidate frames",
       "cases":cases,
       "conclusion":"Same final figure can bear distinct first-emergence records; structural pair alignment is a candidate, not a theorem."
    }

if __name__=="__main__":
    import sys
    from pathlib import Path
    path=Path(sys.argv[1] if len(sys.argv)>1 else "output/double_angle_geometry.json")
    path.parent.mkdir(parents=True,exist_ok=True)
    payload=benchmark()
    path.write_text(json.dumps(payload,indent=2,ensure_ascii=False))
    print("Independent geometry checks passed:",len(payload["cases"]),"figures")
    for c in payload["cases"]:
        print(c["shape"],"shared carrier:",c["geometry"]["certified"]["same_carrier"])

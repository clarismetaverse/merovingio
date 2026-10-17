"""Panoptikon Gestalt Dynamics v1.0: exact workspace + constructive genealogy.

No theorem proving and no claims of autonomous Gestalt discovery.
The finite role grammar is a deliberately inspectable research fixture.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from hashlib import sha256
import json
from math import isclose
from typing import Optional

@dataclass(frozen=True)
class Point:
    x: float
    y: float

A=Point(0.0,0.0)
B=Point(10.0,0.0)
C=Point(3.3,8.0)
OUTER=("AB","AC","BC")

def lerp(p:Point,q:Point,t:float)->Point:
    return Point(p.x+(q.x-p.x)*t,p.y+(q.y-p.y)*t)

def signed_area(p:Point,q:Point,r:Point)->float:
    return (q.x-p.x)*(r.y-p.y)-(q.y-p.y)*(r.x-p.x)

def interior_of_AB(p:Point)->bool:
    """Certified strict betweenness; endpoint or exterior gives False."""
    return abs(signed_area(A,p,B)) < 1e-9 and A.x+1e-9 < p.x < B.x-1e-9

def interior_wedge_C_through_AB(p:Point)->bool:
    """The direction CP lies inside the convex cone CA/CB iff P strictly between A,B."""
    return signed_area(C,A,p)*signed_area(C,p,B)>0 and interior_of_AB(p)

def stable_json(x)->str:
    return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False)

@dataclass(frozen=True)
class Event:
    action:str
    dependencies:tuple[str,...]
    material_additions:tuple[str,...]
    genealogy:str

ROLE_SCHEMA={
 "outer_triangle":{"members":["A","B","C","AB","AC","BC"],"status":"given","domain":"region"},
 "base_AB":{"members":["A","B","AB"],"status":"given","domain":"side"},
 "angle_ACB":{"members":["CA","CB","C"],"status":"given","domain":"angle"},
 "base_AD_DB":{"members":["A","D","B","AD","DB"],"status":"verified_topology","domain":"side"},
 "ray_from_C":{"members":["C","ray_CD_direction"],"status":"candidate","domain":"angle"},
 "angular_ACD_DCB":{"members":["CA","CD","CB","C"],"status":"verified_topology","domain":"angle"},
 "regions_ACD_BCD":{"members":["A","B","C","D","AC","BC","CD","AD","DB"],"status":"verified_topology","domain":"region"},
 "bridge_angle_base":{"members":["C","CD","D","AB"],"status":"verified_topology","domain":"mixed"},
 "generic_paired_regions":{"members":["ACD","BCD","shared_CD"],"status":"candidate","domain":"generic"},
}
# No equal-length or equal-angle relation is present in this grammar.
assert all("equal" not in stable_json(row).lower() for row in ROLE_SCHEMA.values())

def observe(points:dict[str,Point], segments:set[str],ray:bool)->dict:
    """Finite candidate-generation grammar with deterministic geometric checks."""
    observed={k:dict(v) for k,v in ROLE_SCHEMA.items()
              if k in ("outer_triangle","base_AB","angle_ACB")}
    d=points.get("D")
    within=d is not None and interior_of_AB(d)
    if ray and "CD" not in segments:
        observed["ray_from_C"]=dict(ROLE_SCHEMA["ray_from_C"])
    if within:
        observed["base_AD_DB"]=dict(ROLE_SCHEMA["base_AD_DB"])
    if within and "CD" in segments:
        for key in ("angular_ACD_DCB","regions_ACD_BCD",
                    "bridge_angle_base","generic_paired_regions"):
            observed[key]=dict(ROLE_SCHEMA[key])
    for row in observed.values():
        row["epistemic_status"]=row.pop("status")
    return observed

def object_roles(observations:dict)->dict[str,list[str]]:
    roles={"AB":["outer_side"],"AC":["outer_side"],"BC":["outer_side"],
           "C":["triangle_vertex","angle_vertex"]}
    if "base_AD_DB" in observations:
        roles["AB"].append("carrier_of_adjacent_base_parts")
    if "angular_ACD_DCB" in observations:
        roles["C"].append("vertex_of_adjacent_angular_sectors")
        roles["CD"]=["angular_separator"]
    if "regions_ACD_BCD" in observations:
        roles["AB"].append("outer_boundary_of_paired_regions")
        roles["CD"].append("common_boundary_of_paired_regions")
    if "bridge_angle_base" in observations:
        roles["CD"].append("cross_space_bridge")
    return {key:sorted(set(value)) for key,value in sorted(roles.items())}

def snapshot(points,segments,ray,stage,event,origins):
    groups=observe(points,segments,ray)
    new_groups=sorted(set(groups)-set(origins))
    for key in new_groups:
        origins[key]={"stage":stage,"event":event}
    return {
        "stage":stage,"event":event,
        "material_points":sorted(points),
        "material_segments":sorted(segments),
        "auxiliary_ray_active":ray,
        "candidates":groups,
        "first_appearances":new_groups,
        "roles":object_roles(groups),
    }

def trace_construction(genealogy:str,t:float=0.37)->dict:
    """Two distinct histories converge to precisely the same final material state.

    base-first: choose D as point on AB, then join CD.
    fan-first: choose a ray from C, intersect existing AB at D, then
               realize CD as a finite carrier.
    """
    if genealogy not in ("base_first","fan_first"):
        raise ValueError(genealogy)
    d=lerp(A,B,t)
    points={"A":A,"B":B,"C":C}
    segments=set(OUTER)
    ray=False
    origins={}
    frames=[snapshot(points,segments,ray,0,"given_triangle",origins)]
    events=[]
    if genealogy=="base_first":
        sequence=[
          Event("place_D_on_AB",("AB",),("D",),"segment-driven point selection"),
          Event("join_CD",("C","D"),("CD",),"segment-to-apex connection"),
        ]
    else:
        sequence=[
          Event("open_directional_ray_from_C",("C","AB"),("ray_CD_direction",),
                "apex-driven directional selection"),
          Event("intersect_ray_with_AB",("ray_CD_direction","AB"),("D",),
                "ray-to-base intersection"),
          Event("restrict_ray_to_segment_CD",("C","D"),("CD",),
                "intersection-to-finite-carrier conversion"),
        ]
    for i,event in enumerate(sequence,1):
        if event.action=="place_D_on_AB":
            points["D"]=d
        elif event.action=="open_directional_ray_from_C":
            ray=True
        elif event.action=="intersect_ray_with_AB":
            # A line from C through D meets AB at exactly this point.
            if abs(signed_area(A,d,B))>1e-9:raise ValueError("No ray/base intersection")
            points["D"]=d
        elif event.action in ("join_CD","restrict_ray_to_segment_CD"):
            if "D" not in points:raise ValueError("Cannot make CD without D")
            segments.add("CD");ray=False
        events.append(asdict(event))
        frames.append(snapshot(points,segments,ray,i,event.action,origins))
    final=frames[-1]
    material={
       "points":{key:[round(p.x,9),round(p.y,9)] for key,p in sorted(points.items())},
       "segments":sorted(segments)
    }
    final_signature=sha256(stable_json(material).encode()).hexdigest()
    return {
       "genealogy":genealogy,"parameter_t":t,
       "events":events,"snapshots":frames,"first_appearance_provenance":origins,
       "final_material":material,"final_material_sha256":final_signature,
       "final_candidates":sorted(final["candidates"]),
       "final_roles":final["roles"],
    }

def backpropagation(trace)->list[dict]:
    """Log newly enabled interpretations of already existing objects."""
    frames=trace["snapshots"]
    changes=[]
    for before,after in zip(frames[:-1],frames[1:]):
        for obj,new_roles in after["roles"].items():
            if obj not in before["roles"]:continue
            delta=sorted(set(new_roles)-set(before["roles"][obj]))
            if delta:
                changes.append({
                   "object":obj,"event":after["event"],"stage":after["stage"],
                   "new_interpretive_roles":delta,"epistemic_status":"topological_or_candidate",
                })
    return changes

def deformation_series(values=(0.37,1.0,1.15))->list[dict]:
    rows=[]
    for t in values:
        trace=trace_construction("base_first",t)
        active=trace["final_candidates"]
        d=lerp(A,B,t)
        rows.append({"t":t,"D":[d.x,d.y],"strictly_within_AB":interior_of_AB(d),
                     "active_mental_spaces":active})
    return rows

def run_deterministic()->dict:
    g1=trace_construction("base_first")
    g2=trace_construction("fan_first")
    if g1["final_material_sha256"]!=g2["final_material_sha256"]:
        raise AssertionError("Different final geometry")
    if g1["final_candidates"]!=g2["final_candidates"]:
        raise AssertionError("Different final candidate vocabulary")
    if g1["events"]==g2["events"]:
        raise AssertionError("Histories are not distinct")
    return {
        "experiment":"Panoptikon Gestalt Dynamics v1.0",
        "status":"DETERMINISTIC_FIXTURE_NOT_LEARNED_DISCOVERY",
        "same_final_material":True,
        "same_final_candidates":True,
        "semantic_warning":"Present heuristic role grammar is hand-authored, not inferred by Jev.",
        "histories":[
          {**g1,"backpropagation":backpropagation(g1)},
          {**g2,"backpropagation":backpropagation(g2)}
        ],
        "deformation":deformation_series(),
        "conclusions":[
            "Final geometry and candidates are identical for these paths.",
            "Construction genealogies, intermediate candidate activation, and provenance differ.",
            "No equality, congruence, or theorem proof is asserted."
        ],
    }

if __name__=="__main__":
    from pathlib import Path
    import sys
    target=Path(sys.argv[1] if len(sys.argv)>1 else "output/gestalt_dynamics.json")
    target.parent.mkdir(parents=True,exist_ok=True)
    report=run_deterministic()
    target.write_text(json.dumps(report,indent=2,ensure_ascii=False))
    print("Same final geometry:",report["same_final_material"])
    for h in report["histories"]:
        print(h["genealogy"],"events:",len(h["events"]),
              "backpropagated roles:",len(h["backpropagation"]))
    print("Report:",target)

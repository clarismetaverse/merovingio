"""Prospective Generic Space binding: source memory -> missing roles -> proposals.

This oracle and candidate generator are deterministic. Selection is delegated to
Jev only after candidate images are generated. No proof facts are transferred.
"""
from __future__ import annotations
import json, math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
MEMORY_PATH=ROOT/"NMerovingio/graph/generic_space_memory_v0_9.json"
MEMORY={e["id"]:e for e in json.loads(MEMORY_PATH.read_text(encoding="utf-8"))["entries"]}

TRIANGLE_METHODS=("from_C","from_A","from_B","edge_link")
CIRCLE_METHODS=("circle_opposite_same_radius","circle_opposite_short_radius","circle_same_center","midpoint_line")
SOURCE_CASES={
 "triangle": "GS_HIST_DOUBLE_TRIANGLE",
 "circle": "GS_HIST_RADIUS_TRIANGLE",
 "negative": "GS_PROP_I_5",
}
TRIANGLE_SHAPES=("left","right")
TRIANGLE_ROLES={
 "workspace_current":("triangle_ABC","angular_fan_C","base_AB"),
 "already_bound":("triangle_ABC","angular_fan_C","base_AB"),
 "missing":("new_shared_carrier","two_adjacent_triangle_regions","base_contact_D"),
 "description":"The current angular fan at C and opposite base AB should acquire two adjacent closed triangular regions that share one new material carrier."
}
CIRCLE_ROLES={
 "workspace_current":("segment_AB","circle_center_A_radius_AB"),
 "already_bound":("segment_AB","first_circle","radius_reference_AB"),
 "missing":("second_circle_with_same_radius_reference","common_intersection_C","two_radius_sides_from_C"),
 "description":"A single circle has been drawn with A as center and AB as its radius. Retrieve the pattern of two circle Gestalten linked by a common radius packet and a shared intersection vertex."
}

def read_memory(case):
 entry=MEMORY[SOURCE_CASES[case]]
 assert entry["memory_status"]=="retrievable_template"
 assert entry["provenance"]["file"].startswith("NMerovingio/")
 assert entry["metric_status"]!="proven"
 return entry

def memory_priority(case):
 """Small source-grounded preference without treating recall as proof."""
 features={
  "triangle":{"triangle","medial_carrier","shared_side","partition_two_regions"},
  "circle":{"circle","radius","common_reference","intersection"},
  "negative":{"isosceles","side_equality","opposite_angle"},
 }[case]
 ranked=sorted(((len(features.intersection(e["tags"])),e["id"]) for e in MEMORY.values()),reverse=True)
 correct=SOURCE_CASES[case]
 assert correct in {entry_id for count,entry_id in ranked if count>0}
 return ranked

def propose(case):
 if case in ("triangle","negative"): return TRIANGLE_METHODS
 if case=="circle": return CIRCLE_METHODS
 raise ValueError(case)

def source_binding(case):
 item=read_memory(case)
 if case=="triangle": slots=TRIANGLE_ROLES
 elif case=="circle": slots=CIRCLE_ROLES
 else:
  slots={
    "workspace_current":("triangle_ABC","no_certified_equal_sides"),
    "already_bound":("triangle_ABC",),
    "missing":("certified_equal_outer_sides","licensed_angle_relation"),
    "description":"An earlier theorem pattern transfers equality of two sides into equality of corresponding angles. In the current workspace no equal-side premise is certified. No decorative line is a theorem proof."
  }
 return {"memory_id":item["id"],"source_path":item["provenance"]["file"],
         "source_workspace_id":item["provenance"]["workspace_id"],
         "source_node_ids":item["provenance"]["node_ids"],
         "slots":slots}

def geometric_oracle(case,shape,method):
 """Compute correct role completion from independently checked geometry."""
 if case=="triangle":
  from structural_bridges_v07 import TOPOLOGY,certify_geometry
  certify_geometry(shape)
  v=TOPOLOGY[method]
  return {
   "new_shared_carrier": v["apex"]=="C" and v["opposite_carrier"]=="AB",
   "two_adjacent_triangle_regions": len(v["regions"])==2 and all(len(r)==3 for r in v["regions"]),
   "base_contact_D": "D" in v["interior"] and v["apex"]=="C",
   "completed":method=="from_C"
  }
 if case=="negative":
  return {"certified_equal_outer_sides":False,"licensed_angle_relation":False,"completed":False}
 if case=="circle":
  # Coordinate source: AB=200, initial circle centered A, radius 200.
  A=(320.0,360.0);B=(520.0,360.0)
  r=math.dist(A,B)
  distinct_second_center=(method in ("circle_opposite_same_radius","circle_opposite_short_radius"))
  second_radius=r if method in ("circle_opposite_same_radius","circle_same_center") else 0.7*r
  same_reference=distinct_second_center and abs(second_radius-r)<1e-8
  # Strict two-circle intersection: |r1-r2| < d < r1+r2.
  intersects=distinct_second_center and abs(r-second_radius)<r<r+second_radius
  return {"second_circle_with_same_radius_reference":same_reference,
          "common_intersection_C":intersects,
          "two_radius_sides_from_C":same_reference and intersects,
          "completed":same_reference and intersects}
 raise ValueError(case)

def rank_candidates_heuristic(case,shape):
 """Independent symbolic baseline: number of completed missing roles."""
 missing=source_binding(case)["slots"]["missing"]
 scores={}
 for method in propose(case):
  cert=geometric_oracle(case,shape,method)
  scores[method]=sum(bool(cert.get(role,False)) for role in missing)
 return scores

def verifier_after_choice(case,shape,chosen):
 slots=source_binding(case)["slots"]
 before={role:"missing" for role in slots["missing"]}
 after_raw=geometric_oracle(case,shape,chosen) if chosen else {}
 after={role:("verified_structural" if after_raw.get(role,False) else "missing")
        for role in slots["missing"]}
 return {"before":before,"after":after,"successful_completion":bool(after_raw.get("completed",False)),
         "epistemic_limit":"constructed geometry / structural roles only; no theorem proven"}

#!/usr/bin/env python3
"""Merovingio v10 — Cognitive closure through proof-agnostic binding memory.

The purpose of this experiment is NOT to run or simulate a geometric proof.
It records a causal cognitive history:
  prior triangle/category and initial equality perception;
  prospective two-role blend (W0); material bisector and new faces (W1);
  cognitive role bindings (outer legs, common side, included angles);
  frame-completion event (LAL);
  cognitive projection of the *corresponding opposite side relationship*;
  MEDIAN frame activation and LLL reinterpretation.

The last two are changes in the cognitive workspace, not proof certificates.
The same resulting side relation may be mathematically demonstrable, but
that is a separate task for a future geometric verifier. The source of the
new relation is a completed LAL conceptual mapping, with explicit parents.

No cognitive event silently upgrades a conjecture to a certified theorem.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import random
import sys
from pathlib import Path
from statistics import mean

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/"congruence_frame_v9"))
from frame_competition import (
    make_workspace, role_schema, preconstruction_evidence,
    check_witnesses, score_frames, FRAMES
)
sys.path.insert(0,str(HERE.parent/"prospective_blending_v8"))
from prospective import (
    division_goal, prospective_blend, candidate_constructions,
    construct, bind_prospective
)

CONDITIONS=("normal","LLL_initially_favored","without_prospection",
            "angle_witness_masked","counterfactual_base_given")
SHAPES=("equilateral","isosceles","scalene")
GOALS=("A","B","C")


def stable_id(kind,payload):
    raw=json.dumps([kind,payload],sort_keys=True,ensure_ascii=False,default=str)
    return "C:"+hashlib.sha256(raw.encode()).hexdigest()[:13]


class CognitiveWorkspace:
    """Append-only, lineage-traceable representations and attention events."""
    def __init__(self):
        self.entries=[]
        self.by_id={}
        self.links=[]
        self.clock=0

    def record(self,kind,meaning,*,status,parents=(),payload=None,frame=None):
        payload={} if payload is None else payload
        for parent in parents:
            if parent not in self.by_id:
                raise ValueError("Unrecognized mental parent: "+str(parent))
        self.clock+=1
        key=stable_id(kind,{"seq":self.clock,"meaning":meaning,
                            "parents":list(parents),"payload":payload})
        node={"id":key,"tick":self.clock,"kind":kind,"meaning":meaning,
              "status":status,"parents":list(parents),
              "payload":payload,"frame":frame}
        self.entries.append(node)
        self.by_id[key]=node
        self.links.extend({"from":parent,"to":key,"type":"cognitive_enables"}
                          for parent in parents)
        return node

    def paths(self,node_id):
        seen=set();order=[]
        def go(id):
            if id in seen:return
            seen.add(id)
            for p in self.by_id[id]["parents"]:go(p)
            order.append(id)
        go(node_id)
        return [self.by_id[x] for x in order]

    def check(self):
        prior=set()
        for node in self.entries:
            if not all(p in prior for p in node["parents"]):
                raise AssertionError("Cognitive dependency not ordered")
            prior.add(node["id"])
            if node["kind"]=="PROJECT_RELATION":
                if node["status"]!="cognitive_inference_not_proven":
                    raise AssertionError("Cognitive projection must not be proof")
                if not node["parents"]:
                    raise AssertionError("Unmotivated projected consequence")
        return True

    def export(self):
        self.check()
        return {"entries":self.entries,"edges":self.links,
                "acyclic":True,
                "proven_metric_equalities":[],
                "projected_relations":[x for x in self.entries
                                       if x["kind"]=="PROJECT_RELATION"]}


def initial_sources(ws,goal):
    e=preconstruction_evidence(ws,goal)
    return e["equal_outer_legs"]


def run(shape="equilateral",goal="C",condition="normal",seed=0):
    if shape not in SHAPES or goal not in GOALS or condition not in CONDITIONS:
        raise ValueError("Unknown condition/geometry")
    if shape=="scalene" and condition=="counterfactual_base_given":
        raise ValueError("Counterfactual base equality incompatible with scalene fixture")

    before=make_workspace(shape)
    task=division_goal(before,goal)
    prospective=None if condition=="without_prospection" else prospective_blend(before,task)
    initial=initial_sources(before,goal)
    memory=CognitiveWorkspace()

    root=memory.record(
        "ACTIVATE_FRAMES","TRIANGLE × DIVISION",
        status="conceptual_primitive",frame="TRIANGLE/DIVISION",
        payload={"goal":task,
                 "original_material_points":sorted(before["points"]),
                 "material_faces":before["faces"]})
    given=memory.record(
        "PERCEIVE_INITIAL_RELATION","Original external sides",
        status="given_available" if initial["status"]=="verified" else "not_available",
        parents=[root["id"]],frame="TRIANGLE",
        payload={"role":"equal_outer_legs","witness":initial})
    prospective_node=None
    if prospective:
        prospective_node=memory.record(
            "FORM_PROSPECTIVE_BLEND","Two future angle↔side role pairs",
            status="prospective_only",parents=[root["id"]],
            frame="TRIANGLE × DIVISION",
            payload={"latent_role_pairs":prospective["blended_space"]["correspondence_pairs"],
                     "material_points_unchanged":sorted(before["points"])})

    # The material event is independent of the mental frame chosen.
    op=next(x for x in candidate_constructions(before) if x["origin_vertex"]==goal)
    after=construct(before,op)
    roles=role_schema(before,after,task)
    prospective_binding=bind_prospective(prospective,before,after,task)
    built=memory.record(
        "CONSTRUCT_DIVIDER","Bisector meets the opposite side",
        status="constructed_material",parents=[root["id"]],
        frame="CONSTRUCTION",
        payload={"operation":op,
                 "new_point":after["construction_events"][-1]["contact_point"],
                 "new_faces":after["construction_events"][-1]["new_faces"]})
    matched=memory.record(
        "RECOGNIZE_FRAME_ROLES","Two triangle-shaped readings of the construction",
        status="structurally_bound",
        parents=[built["id"]]+([prospective_node["id"]] if prospective_node else []),
        frame="TWO_PARTITIONED_TRIANGLES",
        payload={"role_mapping":roles,
                 "prospective_roles_matched":prospective_binding["matched"] if prospective else False})

    full=check_witnesses(before,after,roles,condition)
    # This is inspection of the cognitive evidence, not a proof tactic.
    order=["equal_shared_side","equal_included_angles"]
    random.Random(seed*1009+31).shuffle(order)
    role_nodes={"equal_outer_legs":given["id"]}
    activation=[{"stage":"BEFORE_CONSTRUCTION",
                 "available_roles":["equal_outer_legs"] if initial["status"]=="verified" else [],
                 "LAL_attraction":score_frames(preconstruction_evidence(before,goal),
                    "LLL_initially_favored" if condition=="LLL_initially_favored" else "balanced",
                    prospective is not None)["LAL"]["attraction_probability"]}]
    observed={"equal_outer_legs":initial}
    for slot in order:
        witness=full[slot]
        node=memory.record(
            "BIND_ROLE",slot,
            status="cognitive_witness_confirmed" if witness["status"]=="verified"
                   else "unavailable_or_masked",
            parents=[matched["id"]],
            frame="LAL/LLL",
            payload={"slot":slot,"witness":witness})
        role_nodes[slot]=node["id"]
        observed[slot]=witness
        stage={k:dict(v) for k,v in preconstruction_evidence(before,goal).items()}
        for k in order[:len(activation)]:
            if k in observed:stage[k]=observed[k]
        scores=score_frames(stage,
            "LLL_initially_favored" if condition=="LLL_initially_favored" else "balanced",
            prospective is not None)
        activation.append({"stage":"AFTER_ROLE_BINDING","new_role":slot,
                           "available_roles":[k for k,v in observed.items() if v["status"]=="verified"],
                           "LAL_attraction":scores["LAL"]["attraction_probability"]})

    observed.update({"equal_base_halves":full["equal_base_halves"]})
    lal_complete=all(observed[k]["status"]=="verified" for k in FRAMES["LAL"]["slots"])
    lhs=roles["role_pairs"]["equal_base_halves"]
    side_relation={"predicate":"cognitive_equal_segments_candidate",
                   "objects":lhs,"origin":"LAL frame corresponding opposite sides"}
    frame_node=None
    projected=None
    median=None
    secondary=None
    if lal_complete:
        frame_node=memory.record(
            "COMPLETE_FRAME","LAL binding of corresponding subtriangle roles",
            status="fully_bound_cognitive_frame",
            parents=[matched["id"],*(role_nodes[k] for k in FRAMES["LAL"]["slots"])],
            frame="LAL",
            payload={"filled_roles":{k:observed[k] for k in FRAMES["LAL"]["slots"]},
                     "role_correspondence":roles["role_pairs"],
                     "frame_ready":True})
        projected=memory.record(
            "PROJECT_RELATION","Corresponding base-side roles may have equal lengths",
            status="cognitive_inference_not_proven",
            parents=[frame_node["id"]],
            frame="LAL → OPPOSITE SIDE PAIR",
            payload={"proposed_relation":side_relation,
                     "epistemic_qualification":"not independently geometrically verified",
                     "not_input_to_same_inference":True})
        median=memory.record(
            "ACTIVATE_ALTERNATIVE_FRAME","MEDIAN frame becomes salient",
            status="hypothetical_frame_attraction",
            parents=[built["id"],projected["id"]],
            frame="MEDIAN",
            payload={"carrier":after["construction_events"][-1]["contact_point"],
                     "candidate_midpoint_side":op["destination_edge"],
                     "required_relation":side_relation,
                     "median_not_certified":True})
        secondary=memory.record(
            "REBASE_FRAME","LLL reconsidered using new cognitive projection",
            status="prospective_reading_not_independent_premise",
            parents=[frame_node["id"],projected["id"]],
            frame="LLL",
            payload={"LLL_slots":{"original_leg_equality":"given",
                                  "shared_side":"material_identity",
                                  "base_halves":"cognitively_projected_NOT_in_initial_premises"},
                     "do_not_reuse_projection_as_proof_of_itself":True})

    # Independently available target-side equality is a *control only*.
    externally_given=None
    if condition=="counterfactual_base_given":
        externally_given=memory.record(
            "RECALL_EXTRA_GIVEN","Target base equality independently supplied",
            status="independently_given_in_counterfactual",
            parents=[built["id"]],frame="LLL",
            payload={"roles":lhs,"source":"COUNTERFACTUAL_EXTRA_GIVEN"})
    # In this scenario we NEVER produce a verified equality from the LAL
    # binding. We register the phenomenology of the cognitive transition.
    memory.check()
    return {
        "shape":shape,"goal":goal,"condition":condition,"seed":seed,
        "preconstruction":before,"postconstruction":after,
        "prospective":prospective,"prospective_binding":prospective_binding,
        "role_schema":roles,"original_premise":initial,
        "role_witnesses":full,"binding_order":order,
        "cognitive_memory":memory.export(),
        "attraction_timeline":activation,
        "cognitive_projection":projected,
        "new_median_reading":median,
        "new_LLL_reading":secondary,
        "extra_given_control":externally_given,
        "projection_ancestry":memory.paths(projected["id"]) if projected else [],
        "metrics":{
            "LAL_cognitive_frame_completed":bool(frame_node),
            "new_side_relation_projected":bool(projected),
            "median_frame_activated":bool(median),
            "LLL_rereading_from_new_binding":bool(secondary),
            "prospective_blend_matched":bool(prospective_binding["matched"]),
            "original_equal_legs_available":initial["status"]=="verified",
            "projected_equalities_marked_proven":0,
            "lineage_acyclic":True,
            "projection_preexists_binding":False,
            "circular_premises_used":0}
    }


def experiment(seeds=range(48)):
    designs={"equilateral":GOALS,"isosceles":("C",),"scalene":("C",)}
    runs=[run(shape,goal,condition,seed)
          for shape,goals in designs.items() for goal in goals
          for condition in CONDITIONS
          if not(shape=="scalene" and condition=="counterfactual_base_given")
          for seed in seeds]
    agg={}
    for shape,goals in designs.items():
        agg[shape]={}
        for goal in goals:
            agg[shape][goal]={}
            for condition in CONDITIONS:
                rr=[r for r in runs if r["shape"]==shape and
                    r["goal"]==goal and r["condition"]==condition]
                if not rr:continue
                avg=lambda k:mean(r["metrics"][k] for r in rr)
                agg[shape][goal][condition]={
                    "n":len(rr),
                    "frame_completion_rate":round(avg("LAL_cognitive_frame_completed"),4),
                    "relation_projection_rate":round(avg("new_side_relation_projected"),4),
                    "median_attraction_rate":round(avg("median_frame_activated"),4),
                    "new_LLL_reading_rate":round(avg("LLL_rereading_from_new_binding"),4),
                    "false_proof_promotions":sum(r["metrics"]["projected_equalities_marked_proven"] for r in rr),
                    "circular_premises_used":sum(r["metrics"]["circular_premises_used"] for r in rr)}
    return {"schema":"merovingio.cognitive_binding_consequences.v10",
            "epistemology":"Cognitive frame consequence memory only. No geometric inference/proof engine.",
            "conditions":CONDITIONS,"shapes":SHAPES,"designs":designs,
            "seeds":list(seeds),"aggregates":agg,"runs":runs}


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--seeds",type=int,default=48)
    p.add_argument("--output",default=str(HERE/"results"))
    args=p.parse_args()
    out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    result=experiment(range(args.seeds))
    (out/"traces.json").write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
    (out/"aggregates.json").write_text(json.dumps(result["aggregates"],ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(result["aggregates"],indent=2))
    print("Created",out/"traces.json")


if __name__=="__main__":main()

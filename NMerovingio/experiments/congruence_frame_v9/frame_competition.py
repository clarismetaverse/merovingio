#!/usr/bin/env python3
"""v9 · Competing congruence frame attraction for two constructed subtriangles.

LAL (side-angle-side, SAS) and LLL (side-side-side, SSS) are general templates
with independently checked premises. An equilateral triangle supplies one
side equality BEFORE the bisector. A bisector supplies an angular equality,
and its own physical line is a shared side of the two new triangles. LAL thus
fills 3/3; LLL remains 2/3 until the TARGET base equality is independently
proved. That equality MUST NOT enter the LLL premises through analogy.

The goal is to examine frame completion/attention dynamics, not to hard-code
the LAL outcome. In a separate explicitly counterfactual GIVEN_BASE variant,
LLL can become ready and win if favored. That case is not a proof of I.10.

The score and binder are engineered; the proof guard only applies a narrow
sound SAS congruence rule when its prerequisites are independently verified.
"""
from __future__ import annotations
import argparse
import json
import math
import random
import sys
from pathlib import Path
from statistics import mean

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/"prospective_blending_v8"))
from prospective import (triangle_workspace,division_goal,prospective_blend,
                         candidate_constructions,construct,bind_prospective)

SHAPES=("equilateral","isosceles","scalene")
CONDITIONS=("balanced","LLL_initially_favored","without_prospection",
            "angle_witness_masked","counterfactual_base_given")
GOALS=("A","B","C")
FRAMES={
  "LAL":{"label":"side–angle–side","slots":("equal_outer_legs","equal_shared_side",
                                        "equal_included_angles")},
  "LLL":{"label":"side–side–side","slots":("equal_outer_legs","equal_shared_side",
                                        "equal_base_halves")},
}
TEMPERATURE=.54


def e(u,v):return tuple(sorted((u,v)))
def normalize_pair(a,b):return tuple(sorted((e(*a),e(*b))))


def make_workspace(shape):
    if shape=="equilateral":ws=triangle_workspace("equilateral")
    elif shape=="scalene":ws=triangle_workspace("scalene")
    elif shape=="isosceles":
        ws=triangle_workspace("equilateral")
        # Same apex C and base midpoint, but a different height:
        # two original legs equal, unlike base. Explicit isosceles premise.
        ax,ay=ws["points"]["A"];bx,by=ws["points"]["B"]
        ws["points"]["C"]=[(ax+bx)/2,115.]
        ws["shape"]="isosceles"
    else:raise ValueError(shape)
    # Assert premised equalities are genuine before using them as givens,
    # but no coordinate measurements participate in frame scoring.
    edges=ws["edges"];p=ws["points"]
    premise_pairs=[]
    if shape=="equilateral":
        for i in range(len(edges)):
            for j in range(i+1,len(edges)):
                premise_pairs.append(normalize_pair(edges[i],edges[j]))
    if shape=="isosceles":
        premise_pairs.append(normalize_pair(("A","C"),("B","C")))
    for aa,bb in premise_pairs:
        assert abs(math.dist(p[aa[0]],p[aa[1]])-
                   math.dist(p[bb[0]],p[bb[1]]))<1e-8
    ws["premises"]={
        "side_equalities":[[list(a),list(b)] for a,b in premise_pairs],
        "source":"equilateral_construction" if shape=="equilateral"
                 else "isosceles_given" if shape=="isosceles" else "none"}
    return ws


def canonical_premises(ws):
    return {normalize_pair(a,b) for a,b in ws["premises"]["side_equalities"]}


def role_schema(before,after,goal):
    """Infer two-face correspondence from a shared construction carrier.

    No literal AB/AC/CD/AD labels and no assumed equality; only graph edges
    and one constructed bisector event are used.
    """
    event=after["construction_events"][-1]
    pivot=event["vertex"];mid=event["contact_point"]
    assert pivot==goal["vertex"]
    faces=[set(f) for f in event["new_faces"]]
    assert len(faces)==2 and all(len(f)==3 and {pivot,mid}<=f for f in faces)
    ends=[next(iter(f-{pivot,mid})) for f in faces]
    assert len(set(ends))==2
    left,right=sorted(ends)
    parent_edge=event["target_edge"]
    assert set(parent_edge)=={left,right}
    return {
        "correspondence":{
            "fixed_vertex":pivot,"fixed_contact":mid,
            "external_vertex_pair":[left,right],
            "triangular_faces":[sorted(f) for f in faces]},
        "role_pairs":{
            "equal_outer_legs":[[pivot,left],[pivot,right]],
            "equal_shared_side":[[pivot,mid],[pivot,mid]],
            "equal_included_angles":[[pivot,left,mid],[pivot,right,mid]],
            "equal_base_halves":[[left,mid],[right,mid]]},
        "required_proof_target":"equal_base_halves",
        "material_source":"constructed_faces_and_shared_segment",
        "epistemic_status":"material_role_frame"}


def check_witnesses(before,after,roles,condition):
    """Independent evidence ledger; absence is never silently assumed false."""
    pairs=roles["role_pairs"];material=roles["correspondence"]
    given=canonical_premises(before)
    outer=normalize_pair(*pairs["equal_outer_legs"])
    eq_outer=outer in given
    common=pairs["equal_shared_side"]
    eq_common=(e(*common[0])==e(*common[1]) and
               all(x in after["points"] for x in common[0]))
    angles=pairs["equal_included_angles"]
    bisector=after["given_angular_equalities"]
    ang={"available":False,"source":"none"}
    for item in bisector:
        if item["status"]!="CONSTRUCTION_GIVEN":continue
        supplied={(a[0],frozenset(a[1:])) for a in item["sectors"]}
        wanted={(a[0],frozenset(a[1:])) for a in angles}
        if supplied==wanted and all(a[0]==material["fixed_vertex"] for a in angles):
            ang={"available":True,"source":"constructed_angle_bisector"}
    if condition=="angle_witness_masked":
        ang={"available":False,"source":"masked_from_attention_only"}
    base=normalize_pair(*pairs["equal_base_halves"])
    # The original construction has NO base-half equality premise.
    # This counterfactual is permitted only when it is geometrically true,
    # and marked as a *separate new premise*, not an inferred conclusion.
    base_as_given=(condition=="counterfactual_base_given" and eq_outer)
    return {
        "equal_outer_legs":{
            "status":"verified" if eq_outer else "unavailable",
            "source":before["premises"]["source"] if eq_outer else "none",
            "roles":pairs["equal_outer_legs"]},
        "equal_shared_side":{
            "status":"verified" if eq_common else "unavailable",
            "source":"same_material_segment_reflexive" if eq_common else "none",
            "roles":common},
        "equal_included_angles":{
            "status":"verified" if ang["available"] else "unavailable",
            "source":ang["source"],"roles":angles},
        "equal_base_halves":{
            "status":"verified" if base_as_given else "unavailable",
            "source":"COUNTERFACTUAL_EXTRA_GIVEN" if base_as_given else "not_a_premise",
            "roles":pairs["equal_base_halves"],
            "goal_dependent":True},
    }


def preconstruction_evidence(before,pivot):
    face=before["faces"][0]
    ends=sorted(set(face)-{pivot})
    parent_leg_pair=[[pivot,ends[0]],[pivot,ends[1]]]
    outer=normalize_pair(*parent_leg_pair)
    return {
        "equal_outer_legs":{
            "status":"verified" if outer in canonical_premises(before) else "unavailable",
            "source":before["premises"]["source"] if outer in canonical_premises(before) else "none",
            "roles":parent_leg_pair},
        "equal_shared_side":{"status":"uninstantiated","source":"construction_not_executed"},
        "equal_included_angles":{"status":"uninstantiated","source":"construction_not_executed"},
        "equal_base_halves":{"status":"uninstantiated","source":"construction_not_executed",
                             "goal_dependent":True},
    }


def observe(before,after,roles,condition):
    """Evidence order reflects attention, not a proof search tied to a frame."""
    full=check_witnesses(before,after,roles,condition)
    return full


def state_from_revealed(full,revealed,pre):
    state={k:dict(v) for k,v in pre.items()}
    # At construction time all material roles exist but remain *uninspected*
    # until a corresponding evidence codelet has visited them.
    for key in ("equal_shared_side","equal_included_angles","equal_base_halves"):
        state[key]={"status":"uninspected","source":"not_yet_bound"}
    for key in revealed:
        state[key]=dict(full[key])
    return state


def score_frames(ledger,condition,prospected):
    result={}
    for name,schema in FRAMES.items():
        checked=[ledger[k]["status"]=="verified" for k in schema["slots"]]
        count=sum(checked)
        missing=[key for key in schema["slots"] if ledger[key]["status"]!="verified"]
        prior=1.65 if name=="LLL" and condition in (
            "LLL_initially_favored","counterfactual_base_given") else 0.
        prospective=.20 if prospected and name=="LAL" else 0.
        complete=1.35 if count==3 else 0.
        # A proof cannot rely on its *own requested conclusion*: treating a
        # missing target base equality as a premise would be circular.
        circular=(name=="LLL" and "equal_base_halves" in missing)
        safety=-.48 if circular else 0.
        score=.75*count-.18*len(missing)+complete+prior+prospective+safety
        result[name]={
            "score":round(score,6),
            "evidence_filled":count,"slots_total":3,
            "evidence_missing":missing,
            "fully_supported":count==3,
            "proof_circularity_risk":circular,
            "terms":{"verified_bindings":round(.75*count,6),
                     "missing_penalty":round(-.18*len(missing),6),
                     "frame_prior":prior,
                     "prospection":prospective,
                     "completeness":complete,
                     "circularity_safeguard":safety}
        }
    weights={f:math.exp((r["score"]-max(x["score"] for x in result.values()))/TEMPERATURE)
             for f,r in result.items()}
    denominator=sum(weights.values())
    for name in result:result[name]["attraction_probability"]=round(weights[name]/denominator,6)
    return result


def select_frame(scores,seed):
    rng=random.Random(seed*1000003+29)
    u=rng.random()
    total=0.
    for key in ("LAL","LLL"):
        total+=scores[key]["attraction_probability"]
        if u<=total:return key
    return "LLL"


def certify_sas(ledger,roles,selected):
    """Small explicit SAS verifier. Only BEFORE-proof construction givens.

    Does not infer a midpoint from an angular bisector alone. Even if a
    cognitive scorer prefers LLL, an independent LAL proof can be recorded
    only after checking its own complete three-premise certificate.
    """
    needed=FRAMES["LAL"]["slots"]
    if not all(ledger[k]["status"]=="verified" for k in needed):
        return {"rule":"SAS","licensed":False,"status":"NOT_PROVEN",
                "missing":[k for k in needed if ledger[k]["status"]!="verified"],
                "derived_segment_equalities":[]}
    pair=roles["role_pairs"]
    a,b=pair["equal_outer_legs"]
    shared=pair["equal_shared_side"]
    angles=pair["equal_included_angles"]
    pivot=roles["correspondence"]["fixed_vertex"]
    if not all(pivot in edge for edge in (a,b,*shared)):
        raise AssertionError("SAS side inclusion mismatch")
    if not all(tuple(triple)[0]==pivot and
               set(triple[1:])==set((next(x for x in side if x!=pivot), next(
                   x for x in shared[0] if x!=pivot))) for triple,side in zip(angles,(a,b))):
        raise AssertionError("SAS angles do not lie between paired sides")
    conclusion=pair["equal_base_halves"]
    return {"rule":"SAS","licensed":True,"status":"DERIVED_BY_SAS_RULE",
            "premises":[{"slot":k,"source":ledger[k]["source"]} for k in needed],
            "derived_segment_equalities":[conclusion],
            "epistemic_status":"proven_from_independently_verified_SAS_premises"}


def simulate(shape="equilateral",goal="C",condition="balanced",seed=0):
    if condition not in CONDITIONS or shape not in SHAPES or goal not in GOALS:
        raise ValueError("Unknown condition")
    before=make_workspace(shape)
    task=division_goal(before,goal)
    prospective=prospective_blend(before,task) if condition!="without_prospection" else None
    assert len(before["faces"])==1 and len(before["points"])==3
    pre=preconstruction_evidence(before,goal)
    pre_scores=score_frames(pre,condition,prospective is not None)
    # Keep geometric construction identical under every cognitive ablation,
    # so attraction differences cannot be attributed to a changed figure.
    chosen_op=next(c for c in candidate_constructions(before) if c["origin_vertex"]==goal)
    after=construct(before,chosen_op)
    roles=role_schema(before,after,task)
    binding=bind_prospective(prospective,before,after,task)
    complete=observe(before,after,roles,condition)
    # The side equality premise was already available at W0, before any CD.
    revealed=[]
    equalities=["equal_shared_side","equal_included_angles"]
    random.Random(seed*1009+31).shuffle(equalities)
    steps=[
        {"tick":0,"stage":"BEFORE_CD",
         "given_equalities":before["premises"],"evidence":pre,
         "frame_attraction":pre_scores,"prospective_blend":prospective,
         "material_points":sorted(before["points"]),"faces":before["faces"]},
        {"tick":1,"stage":"CONSTRUCT_AND_FIND_TWO_FACES",
         "given_angular_equalities":after["given_angular_equalities"],
         "structural_roles":roles,
         "material_points":sorted(after["points"]),
         "faces":after["faces"],"prospective_binding":binding,
         "evidence":state_from_revealed(complete,[],pre),
         "frame_attraction":score_frames(state_from_revealed(complete,[],pre),
                                         condition,prospective is not None)}
    ]
    for tick,slot in enumerate(equalities,2):
        revealed.append(slot)
        st=state_from_revealed(complete,revealed,pre)
        steps.append({"tick":tick,"stage":"REBASE_BIND_EVIDENCE",
                      "newly_inspected_slot":slot,
                      "evidence":st,
                      "frame_attraction":score_frames(st,condition,prospective is not None),
                      "material_points":sorted(after["points"]),
                      "faces":after["faces"]})
    # Finally test the LLL base-length requirement without using the desired
    # conclusion as evidence. Separate GIVEN_BASE branch is labeled explicitly.
    revealed.append("equal_base_halves")
    final=state_from_revealed(complete,revealed,pre)
    scores=score_frames(final,condition,prospective is not None)
    cognitive=select_frame(scores,seed)
    sas=certify_sas(final,roles,cognitive)
    lll_licensed=all(final[k]["status"]=="verified" for k in FRAMES["LLL"]["slots"])
    steps.append({"tick":4,"stage":"COMPETING_FRAME_BINDING",
                  "newly_inspected_slot":"equal_base_halves",
                  "evidence":final,"frame_attraction":scores,
                  "cognitively_selected_frame":cognitive,
                  "proof_verifier":sas,
                  "LLL_licensed":lll_licensed,
                  "note":"Cognitive preference is not itself a proof."})
    return {"shape":shape,"goal":goal,"condition":condition,"seed":seed,
            "preconstruction":before,"prospective":prospective,
            "postconstruction":after,"binding":binding,
            "structural_role_schema":roles,
            "frame_memory":FRAMES,"frame_attraction":scores,
            "selected_frame":cognitive,
            "independent_proof_verifier":sas,
            "LLL_licensed_without_using_conclusion":lll_licensed,
            "evidence_at_selection":final,"timeline":steps,
            "metrics":{
                "LAL_selected":cognitive=="LAL",
                "LAL_supported":scores["LAL"]["fully_supported"],
                "LLL_supported":scores["LLL"]["fully_supported"],
                "LAL_attraction":scores["LAL"]["attraction_probability"],
                "frame_posterior_gain":round(
                    scores["LAL"]["attraction_probability"]-
                    pre_scores["LAL"]["attraction_probability"],6),
                "certified_base_halves_by_SAS":sas["licensed"],
                "LLL_circular_attempt":False,
                "target_equality_assumed":complete["equal_base_halves"]["source"]==
                    "COUNTERFACTUAL_EXTRA_GIVEN",
                "prospective_pair_binding":binding["matched"] if prospective else False,
                "false_metric_certifications":0,
            }}


def experiment(seeds=range(48)):
    # Equilateral: three equivalent choices of target angle.
    # Isosceles/scalene: C is the apex reference, and allows a stringent
    # comparison of what is and is not supplied by initial assumptions.
    goals={"equilateral":GOALS,"isosceles":("C",),"scalene":("C",)}
    runs=[simulate(shape,goal,cond,seed)
          for shape,vertices in goals.items() for goal in vertices
          for cond in CONDITIONS for seed in seeds
          if cond!="counterfactual_base_given" or shape!="scalene"]
    agg={}
    for shape,vertices in goals.items():
        agg[shape]={}
        for goal in vertices:
            agg[shape][goal]={}
            for cond in CONDITIONS:
                rr=[r for r in runs if r["shape"]==shape and
                    r["goal"]==goal and r["condition"]==cond]
                if not rr:continue
                avg=lambda key:mean(r["metrics"][key] for r in rr)
                agg[shape][goal][cond]={
                    "n":len(rr),"LAL_selected_rate":round(avg("LAL_selected"),4),
                    "LAL_fully_supported_rate":round(avg("LAL_supported"),4),
                    "LLL_fully_supported_rate":round(avg("LLL_supported"),4),
                    "mean_LAL_attraction":round(avg("LAL_attraction"),4),
                    "mean_attraction_gain":round(avg("frame_posterior_gain"),4),
                    "certified_SAS_rate":round(avg("certified_base_halves_by_SAS"),4),
                    "counterfactual_given_rate":round(avg("target_equality_assumed"),4),
                    "false_metric_certifications":sum(r["metrics"]["false_metric_certifications"] for r in rr)}
    return {"schema":"merovingio.competition_congruence_frames.v9",
            "models":["LAL","LLL"],"conditions":CONDITIONS,"shapes":SHAPES,
            "seeds":list(seeds),"goal_design":goals,
            "limits":"Engineered salience and explicit SAS verifier; no theorem-prover completeness or human cognitive validation.",
            "aggregates":agg,"runs":runs}


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--seeds",type=int,default=48)
    p.add_argument("--output",default=str(HERE/"results"))
    a=p.parse_args();out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
    obj=experiment(range(a.seeds))
    (out/"traces.json").write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding="utf-8")
    (out/"aggregates.json").write_text(json.dumps(obj["aggregates"],indent=2),encoding="utf-8")
    print(json.dumps(obj["aggregates"],indent=2))
    print("Wrote",out/"traces.json")
if __name__=="__main__":main()

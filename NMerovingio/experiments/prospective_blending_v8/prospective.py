#!/usr/bin/env python3
"""Merovingio v8 · Prospective double-scope blending BEFORE construction.

Inputs: ONLY a material triangle, a target angle to divide, and the memory
grammars TRIANGLE (angle opposite non-incident edge) and DIVISION (whole→parts).
NO D / CD / AD / DB / left/right subtriangles are in the initial material.

The prospective blend is derived by transporting binary PARTITION from ANGLE
through an instantiated TRIANGLE OPPOSITION relation to an opposite SIDE,
then by a general polygon face-splitting grammar. A codelet chooses among
all three eligible vertex→opposite-edge bisector constructions. Only AFTER
selection are incidence, new triangle faces and role bindings materialized.

This is explicitly HAND-CODED cognitive simulation, not historical evidence,
neural learning, an autonomous theorem prover, or a proof of AD=DB.
"""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
import math
import random
from pathlib import Path
from statistics import mean

HERE=Path(__file__).resolve().parent
SHAPES=("equilateral","scalene","obtuse")
CONDITIONS=("full_blend","no_opposition","no_transport",
            "post_construct_only","goal_only")
GOALS=("A","B","C")
BUDGET=1
TEMPERATURE=.48

# Encoded as *general* reusable frame grammars, not target-specific slots.
MEMORY={
    "TRIANGLE":{
        "type":"relational_frame",
        "roles":["vertex","opposite_nonincident_edge","triangular_face"],
        "rule":"opposite_angle_edge_in_triangular_face",
        "metric_implications":[]},
    "DIVISION":{
        "type":"relational_frame",
        "roles":["whole","two_parts","divider"],
        "rule":"binary_partition_with_common_divider",
        "metric_implications":[]},
}
PRIOR={"goal_fit":.84,"triangle_role":.28,"prospective_completion":1.00}


def polygon_faces_after_split(face,vertex,edge,mid):
    """Pure combinatorial face split, for ANY n-gon.

    A split from a polygon vertex to an interior point of a *nonincident*
    boundary edge creates two new face cycles. This operator knows nothing
    about triangle pairs or the proposition being sought.
    """
    if vertex not in face or len(face)<3 or mid in face:
        raise ValueError("Invalid face or split vertex")
    vertices=list(face)
    matches=[i for i in range(len(vertices)) if
        {vertices[i],vertices[(i+1)%len(vertices)]}==set(edge)]
    if len(matches)!=1 or vertex in edge:
        raise ValueError("Only a nonincident boundary edge may be split")
    i=matches[0]
    path=vertices[i+1:]+vertices[:i+1]
    path.insert(0,vertices[i])
    if vertex not in path:raise ValueError("Missing pivot")
    v=path.index(vertex)
    # Insert mid between the edge endpoints at the beginning of the path.
    path.insert(1,mid)
    v=path.index(vertex)
    # Two cycles start at pivot, walk along different sides of boundary.
    first=path[1:v+1][::-1]+[mid] if False else [vertex]+path[v+1:]+path[:2][::-1][1:]
    # Robust generic construction uses explicit cyclic walks after insertion.
    old=vertices[:i+1]+[mid]+vertices[i+1:]
    m=old.index(mid);p=old.index(vertex);n=len(old)
    cw=[old[p]];j=p
    while j!=m:
        j=(j+1)%n;cw.append(old[j])
    ccw=[old[p]];j=p
    while j!=m:
        j=(j-1)%n;ccw.append(old[j])
    assert len(cw)>=3 and len(ccw)>=3
    assert len(set(cw))==len(cw) and len(set(ccw))==len(ccw)
    return [cw,ccw]


def triangle_workspace(shape):
    if shape=="equilateral":
        h=math.sqrt(3)*120.
        p={"A":(65.,280.),"B":(305.,280.),"C":(185.,280.-h)}
    elif shape=="scalene":
        p={"A":(65.,280.),"B":(335.,280.),"C":(144.,72.)}
    elif shape=="obtuse":
        p={"A":(65.,280.),"B":(335.,280.),"C":(155.,238.)}
    else:raise ValueError(shape)
    face=["A","B","C"]
    edges=[tuple(sorted((face[i],face[(i+1)%3]))) for i in range(3)]
    return {"shape":shape,"points":{k:list(v) for k,v in p.items()},
            "faces":[face],"edges":sorted(edges),
            "angles":[{"vertex":v,"arms":sorted(x for x in face if x!=v)}
                      for v in face],
            "construction_events":[],
            "given_angular_equalities":[],
            "certified_segment_equalities":[]}


def role_oppositions(ws,active=True):
    """Instantiate TRIANGLE's generic opposite relation in material 3-cycles."""
    if not active:return []
    facts=[]
    for face in ws["faces"]:
        if len(face)!=3:continue
        for pivot in face:
            others=tuple(sorted(x for x in face if x!=pivot))
            if others not in ws["edges"]:continue
            facts.append({"angle_vertex":pivot,
                          "opposite_edge":list(others),
                          "source_face":sorted(face),
                          "origin":"TRIANGLE.opposite_angle_edge",
                          "epistemic_status":"structural"})
    return sorted(facts,key=lambda x:x["angle_vertex"])


def division_goal(ws,pivot):
    if pivot not in ws["points"]:raise ValueError(pivot)
    return {"target_kind":"angle","vertex":pivot,"parts":2,
            "equal_angular_sectors_requested":True,
            "status":"unrealized_goal"}


def prospective_blend(ws,goal,opp_memory=True,transport=True):
    """Do not insert geometric names/points. Derive roles from two frame grammars."""
    roles=role_oppositions(ws,opp_memory)
    match=next((r for r in roles if r["angle_vertex"]==goal["vertex"]),None)
    if not match or not transport:return None
    face=match["source_face"]
    edge=match["opposite_edge"]
    # A fresh placeholder is private to the prospective mental space and
    # does not appear in the material graph.
    slot="X:unbound"
    simulated=polygon_faces_after_split(face,goal["vertex"],edge,slot)
    # The exact two triangle subframes arise from the generic n-gon splitting
    # rule applied to a 3-cycle: they are not retrieved as a pre-stored frame.
    triangles=[sorted(f) for f in simulated if len(f)==3]
    latent_parts=[
        {"frame":i,
         "angle_role":{"center":goal["vertex"],"sector_slot":i},
         "opposite_side_role":{"parent_edge":edge,"side_slot":i},
         "prospective_face":part,
         "epistemic_status":"PROSPECTIVE_ONLY"}
        for i,part in enumerate(simulated)
    ]
    return {"input_frames":["TRIANGLE","DIVISION"],
            "source_opposition":match,
            "generic_space":{"parent_triangle_face":face,
                             "angle_whole":goal["vertex"],
                             "side_whole":edge,
                             "constraint":"binary partition of opposed roles"},
            "blended_space":{
                "latent_intersection":slot,
                "correspondence_pairs":latent_parts,
                "prospective_face_cycles":simulated,
                "triangular_face_slots":len(triangles),
                "construction_required":"join active vertex to an interior point of the nonincident edge",
                "metric_equality_of_side_parts":"NOT_ASSERTED"},
            "process":["composition: triangle opposition + angle division",
                       "completion: inherit generic polygon split roles",
                       "elaboration: anticipate new face cycles and missing bindings"],
            "status":"HYPOTHESIS_ONLY_PRECONSTRUCTION"}


def candidate_constructions(ws):
    """Same candidate operator vocabulary for every experimental condition."""
    candidates=[]
    for face in ws["faces"]:
        if len(face)!=3:continue
        for vertex in face:
            edge=sorted(v for v in face if v!=vertex)
            candidates.append({
                "kind":"BISECT_ANGLE_TO_OPPOSITE_EDGE",
                "origin_vertex":vertex,
                "destination_edge":edge,
                "source_face":sorted(face),
                "epistemic_status":"possible_unexecuted_construction"})
    return sorted(candidates,key=lambda x:x["origin_vertex"])


def score_candidate(candidate,goal,blend,condition,opposition):
    is_goal=candidate["origin_vertex"]==goal["vertex"]
    goalfit=PRIOR["goal_fit"] if is_goal else 0.
    rolefit=0.
    if condition in ("full_blend","no_transport") and opposition and is_goal:
        rolefit=PRIOR["triangle_role"]
    forward=0.
    if blend is not None and is_goal and set(candidate["destination_edge"])==set(
            blend["source_opposition"]["opposite_edge"]):
        forward=PRIOR["prospective_completion"]
    if condition=="post_construct_only":
        rolefit=0.;forward=0.
    return {"score":round(.25+goalfit+rolefit+forward,6),
            "goal_fit":goalfit,"role_fit":rolefit,
            "prospective_analogy":forward}


def choose(candidates,scores,seed):
    rng=random.Random(seed*104729+17)
    values=[]
    for c in candidates:
        key=c["origin_vertex"]
        u=max(1e-12,min(1-1e-12,rng.random()))
        g=-math.log(-math.log(u))
        values.append((scores[key]["score"]/TEMPERATURE+g,c))
    return max(values,key=lambda x:x[0])[1]


def length(v):return math.hypot(*v)
def cross(u,v):return u[0]*v[1]-u[1]*v[0]
def sub(p,q):return (p[0]-q[0],p[1]-q[1])
def add(p,q):return (p[0]+q[0],p[1]+q[1])
def scale(v,t):return (v[0]*t,v[1]*t)


def construct(ws,candidate):
    """Execute only *after* the plan has been selected.

    Direction is the sum of two unit rays at the chosen vertex.
    Intersection solved with the opposite edge; no angle-bisector theorem
    or equality of split edge lengths is used to locate the new point.
    """
    pre_points=set(ws["points"])
    mid=next(x for x in "DEFGHIJKLMNOPQRSTUVWXYZ" if x not in pre_points)
    pivot=candidate["origin_vertex"]
    u,v=candidate["destination_edge"]
    p,pu,pv=[tuple(ws["points"][n]) for n in (pivot,u,v)]
    a,b=sub(pu,p),sub(pv,p)
    ray=add(scale(a,1/length(a)),scale(b,1/length(b)))
    segment=sub(pv,pu)
    den=cross(ray,segment)
    if abs(den)<1e-10:raise ValueError("Degenerate geometry")
    t=cross(sub(pu,p),segment)/den
    z=cross(sub(pu,p),ray)/den
    if not (t>0 and 0<z<1):raise ValueError("Bisector must meet opposite side interior")
    point=add(p,scale(ray,t))
    after=json.loads(json.dumps(ws))
    after["points"][mid]=list(point)
    # Point-on-side incidence replaces one edge by two; full original
    # edge remains as a parent SEGMENT but is no longer the boundary edge.
    old_edge=tuple(sorted((u,v)))
    after["edges"]=[e for e in after["edges"] if tuple(e)!=old_edge]
    after["edges"] += [tuple(sorted((u,mid))),tuple(sorted((mid,v))),
                       tuple(sorted((pivot,mid)))]
    after["edges"]=sorted({tuple(x) for x in after["edges"]})
    parent_face=next(f for f in after["faces"] if set(f)==set(candidate["source_face"]))
    after["faces"].remove(parent_face)
    newfaces=polygon_faces_after_split(parent_face,pivot,(u,v),mid)
    after["faces"]+=newfaces
    after["construction_events"].append({
        "kind":"BISECTOR_RAY_INTERSECTS_OPPOSITE_SIDE",
        "vertex":pivot,"contact_point":mid,"target_edge":[u,v],
        "new_faces":newfaces,
        "epistemic_status":"CONSTRUCTED"})
    after["given_angular_equalities"].append({
        "vertex":pivot,"sectors":sorted([(pivot,u,mid),(pivot,mid,v)]),
        "reason":"constructed_angle_bisector","status":"CONSTRUCTION_GIVEN"})
    # only material coordinate diagnostics; do not certify AD=DB.
    after["observations"]={
        "split_base_parts_equal_by_coordinates":
            abs(math.dist(pu,point)-math.dist(pv,point))<1e-8,
        "new_triangle_faces":sum(len(f)==3 for f in newfaces),
        "bisected_vertex":pivot}
    after["certified_segment_equalities"]=[]
    return after


def bind_prospective(blend,before,after,goal):
    if blend is None:
        return {"state":"no_prospective_blend","matched":False,"bindings":[]}
    newpts=set(after["points"])-set(before["points"])
    if len(newpts)!=1:return {"state":"no_new_point","matched":False,"bindings":[]}
    middle=next(iter(newpts))
    parent=blend["generic_space"]["side_whole"]
    pivot=goal["vertex"]
    target_faces=[f for f in after["faces"] if
                  pivot in f and middle in f and len(f)==3]
    source_faces=blend["blended_space"]["prospective_face_cycles"]
    matches={}
    for old in source_faces:
        actual=sorted(middle if x=="X:unbound" else x for x in old)
        for f in target_faces:
            if sorted(f)==actual:
                matches[tuple(actual)]=f
    bindings=[]
    for face in target_faces:
        ends=[x for x in face if x not in (pivot,middle)]
        if len(ends)!=1:continue
        endpoint=ends[0]
        bindings.append({
            "angle_sector":{"vertex":pivot,"arms":sorted((endpoint,middle))},
            "opposite_segment":sorted((endpoint,middle)),
            "face":sorted(face),
            "parent_side":parent,
            "epistemic_status":"STRUCTURALLY_BOUND_NOT_METRIC_PROOF"})
    matched=(len(matches)==len(source_faces)==len(bindings)==2 and
             set(parent)==set(x for b in bindings for x in b["face"] if x not in (pivot,middle)))
    return {"state":"BOUND" if matched else "PARTIAL_OR_MISMATCH",
            "matched":matched,"bindings":bindings,
            "latent_to_material":{"X:unbound":middle} if matched else {},
            "certified_segment_equalities":[]}


def postconstruction_reading(after,goal):
    """Read the actual material; separate from prospective anticipation."""
    ev=after["construction_events"][-1]
    subfaces=ev["new_faces"]
    roles=[]
    for face in subfaces:
        if len(face)!=3:continue
        p=ev["vertex"];q=ev["contact_point"]
        ends=[x for x in face if x not in (p,q)]
        if len(ends)!=1:continue
        roles.append({"angle_vertex":p,"side_opposite":sorted([ends[0],q]),
                      "source_face":sorted(face)})
    return {"material_subfaces":[sorted(f) for f in subfaces],
            "observed_angle_side_oppositions":roles,
            "goal_vertex_bisected":ev["vertex"]==goal["vertex"],
            "epistemic_status":"CONSTRUCTED_STRUCTURAL"}


def simulate(condition="full_blend",shape="equilateral",goal_vertex="C",seed=0):
    if condition not in CONDITIONS or shape not in SHAPES or goal_vertex not in GOALS:
        raise ValueError("Invalid condition, shape or target")
    ws=triangle_workspace(shape)
    goal=division_goal(ws,goal_vertex)
    available=role_oppositions(ws,condition!="no_opposition")
    blend=prospective_blend(
        ws,goal,opp_memory=(condition!="no_opposition"),
        transport=(condition not in ("no_transport","post_construct_only","goal_only")))
    assert "D" not in ws["points"] and all(len(f)==3 for f in ws["faces"])
    assert len(ws["faces"])==1
    constructions=candidate_constructions(ws)
    scores={c["origin_vertex"]:score_candidate(
        c,goal,blend,condition,
        next((a for a in available if a["angle_vertex"]==c["origin_vertex"]),None))
        for c in constructions}
    choice=choose(constructions,scores,seed)
    after=construct(ws,choice)
    binding=bind_prospective(blend,ws,after,goal)
    observed=postconstruction_reading(after,goal)
    # Distinguish a successful construction from the prospective ability.
    # No binding is counted if construction was aimed at another vertex.
    valid_construct=observed["goal_vertex_bisected"]
    if not valid_construct:
        binding={"state":"CONSTRUCTION_NOT_TARGETED_AT_GOAL",
                 "matched":False,"bindings":[],
                 "certified_segment_equalities":[]}
    return {
        "condition":condition,"shape":shape,"goal_vertex":goal_vertex,"seed":seed,
        "memory":MEMORY,"goal":goal,
        "preconstruction_material":ws,
        "preconstruction_oppositions":available,
        "preconstruction_blend":blend,
        "construction_candidates":constructions,
        "candidate_scores":scores,"chosen_operation":choice,
        "postconstruction_material":after,
        "postconstruction_reading":observed,
        "prospective_binding":binding,
        "timeline":[
            {"tick":0,"stage":"MATERIAL_INITIAL","points":sorted(ws["points"]),
             "faces":ws["faces"],"goal":goal,
             "note":"No midpoint, bisector, subtriangles, or side-part equality exists"},
            {"tick":1,"stage":"FRAME_COMPOSITION_AND_PROSPECTION",
             "triangle_frame_oppositions":available,
             "prospective_blend":blend,"material_still_unchanged":ws["points"],
             "epistemic_status":"PROSPECTIVE_ONLY" if blend else "NO_PROSPECTIVE_BINDING"},
            {"tick":2,"stage":"ELABORATE_AND_SELECT_CONSTRUCTION",
             "available":constructions,"candidate_scores":scores,
             "chosen":choice,"was_guided_by_blend":bool(scores[choice["origin_vertex"]]["prospective_analogy"])},
            {"tick":3,"stage":"MATERIAL_CONSTRUCTION",
             "points":sorted(after["points"]),"faces":after["faces"],
             "given_angular_equalities":after["given_angular_equalities"],
             "certified_segment_equalities":[]},
            {"tick":4,"stage":"BOTTOM_UP_RECOGNITION_AND_BINDING",
             "observed":observed,"binding":binding,
             "mismatch_detected":not binding["matched"],
             "certified_segment_equalities":[]},
        ],
        "metrics":{
            "prospective_blend_before_construction":blend is not None,
            "preconstruction_two_triangle_roles":(blend is not None and
              blend["blended_space"]["triangular_face_slots"]==2),
            "correct_goal_construction":valid_construct,
            "two_material_subtriangles_detected":len(observed["material_subfaces"])==2,
            "prospective_roles_bound":bool(binding["matched"]),
            "false_segment_equalities":len(after["certified_segment_equalities"]),
            "unused_prospective_material_points":len(set(ws["points"])-{"A","B","C"}),
            "preconstruction_false_subtriangles":max(0,len(ws["faces"])-1),
        }
    }


def experiment(seeds=range(48)):
    runs=[simulate(c,s,v,seed) for s in SHAPES for v in GOALS
          for c in CONDITIONS for seed in seeds]
    agg={}
    for s in SHAPES:
        agg[s]={}
        for v in GOALS:
            agg[s][v]={}
            for c in CONDITIONS:
                rr=[r for r in runs if r["shape"]==s and
                    r["goal_vertex"]==v and r["condition"]==c]
                avg=lambda k:mean(r["metrics"][k] for r in rr)
                agg[s][v][c]={
                    "n":len(rr),
                    "prospective_rate":round(avg("prospective_blend_before_construction"),4),
                    "two_role_anticipation_rate":round(avg("preconstruction_two_triangle_roles"),4),
                    "goal_construction_rate":round(avg("correct_goal_construction"),4),
                    "successful_material_binding_rate":round(avg("prospective_roles_bound"),4),
                    "false_metric_assertions":sum(r["metrics"]["false_segment_equalities"] for r in rr),
                    "false_pre_material_subtriangles":sum(r["metrics"]["preconstruction_false_subtriangles"] for r in rr)}
    return {"schema":"merovingio.prospective_double_scope_blend.v8",
            "epistemic_note":"General polygon split + frame transport engineering simulation, not spontaneous human cognition or geometric proof.",
            "shapes":SHAPES,"goals":GOALS,"conditions":CONDITIONS,
            "seeds":list(seeds),"memory":MEMORY,
            "no_historical_claim":True,"no_jev":True,"no_proof":True,
            "aggregates":agg,"runs":runs}


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--seeds",type=int,default=48)
    p.add_argument("--output",default=str(HERE/"results"))
    a=p.parse_args()
    out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
    e=experiment(range(a.seeds))
    (out/"traces.json").write_text(json.dumps(e,ensure_ascii=False,indent=2),encoding="utf-8")
    (out/"aggregates.json").write_text(json.dumps(e["aggregates"],ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(e["aggregates"],indent=2))
    print("Wrote",out/"traces.json")
if __name__=="__main__":main()

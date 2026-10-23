#!/usr/bin/env python3
"""Merovingio v4: recursive REBASE *only* over angular/segment oppositions.

At every turn the same pair of opposition edges is re-read from the other
domain. Its material carrier and construction event are fixed; a new
graph-grounded relational witness must be incorporated on each rebase.
Already inspected mappings are preserved. An exhausted reading cannot be
revisited: this is a bounded cumulative loop, not a vacuous A/B toggle.

This is an engineered exploration model, NOT Copycat itself or a theorem prover.
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
sys.path.insert(0,str(HERE.parent/"gestalt_heat_v3"))
from poristic import build_material, co_generations

MODES=("isosceles","scalene","ordinary_cevian")
CONDITIONS=("no_pressure","macro_only","genealogy_only","recursive_coupled",
            "recursive_genealogy_blind","one_way")
CONCEPTS=("angles","sides","opposition","coorigin")
START={"angles":.72,"sides":.55,"opposition":.75,"coorigin":.80}
FAMILIES=("ANGLE","SIDE")


def _matching_edges(graph,kind,objects):
    wanted=set(objects)
    out=[]
    for eid,e in graph["edges"].items():
        if e["kind"]==kind and set(e["nodes"])==wanted:
            out.append(eid)
    return sorted(out)


def role_witnesses(graph,packet):
    """Build evidence sets from actual edges, without target group labels."""
    a=packet["angular_partition"]
    s=packet["segment_partition"]
    carrier=packet["mediator"]["carrier"]
    contact="P:"+packet["mediator"]["contact"]
    angles=a["children"]
    sides=s["children"]
    shared_ray=[]
    for angle_id in angles:
        shared_ray.extend(_matching_edges(graph,"bounds_angle",(angle_id,carrier)))
    contacts=[]
    for side_id in sides:
        contacts.extend(_matching_edges(graph,"endpoint",(contact,side_id)))
    opp_edges=[pair["edge_id"] for pair in packet["oppositions"]]
    assert len(opp_edges)==2 and len(shared_ray)==2 and len(contacts)==2
    witnessed={
        "ANGLE":[
            {"name":"angle_partition","edges":a["edge_ids"]},
            {"name":"common_bisecting_ray","edges":shared_ray},
        ],
        "SIDE":[
            {"name":"side_partition","edges":s["edge_ids"]},
            {"name":"common_incidence_point","edges":contacts},
        ]
    }
    if packet["angle_equality_evidence"]:
        witnessed["ANGLE"].append({
            "name":"angular_equality_given",
            "edges":packet["angle_equality_evidence"]
        })
    for domain,items in witnessed.items():
        for item in items:
            assert all(eid in graph["edges"] for eid in item["edges"])
            item["id"]=domain+":"+item["name"]
            item["domain"]=domain
    return witnessed,opp_edges


def retrieve_opposition_pair(graph):
    """Select one co-generated packet by shared mediator, not by AD=DB goal."""
    candidates=co_generations(graph)
    # Stable geometrically defined selection; generalization to simultaneous
    # concurrent packets is left for a future test.
    candidates=sorted(candidates,key=lambda p:(-len(p["oppositions"]),
        p["mediator"]["carrier"]))
    for p in candidates:
        if len(p["oppositions"])==2 and len(p["regions"])==2:
            angles={x["angle"] for x in p["oppositions"]}
            sides={x["side"] for x in p["oppositions"]}
            if len(angles)==len(sides)==2:return p
    raise ValueError("No paired opposition mapping derived from construction")


def _activation(condition):
    if condition=="no_pressure":return dict.fromkeys(CONCEPTS,0.)
    if condition=="genealogy_only":
        return {"angles":0.,"sides":0.,"opposition":0.,"coorigin":START["coorigin"]}
    a=START.copy()
    if condition in ("macro_only","recursive_genealogy_blind"):a["coorigin"]=0.
    return a


def _probability(condition,activation,temperature,witness_count,roundtrip):
    # Similar grammar, choice stochastic; gradients represent engineered
    # salience and must NOT be mistaken for empirical psychological effects.
    coherence=.22+min(witness_count,4)*.045
    pressure=.23*activation["angles"]+.23*activation["sides"]+.36*activation["opposition"]
    genealogy=.95*activation["coorigin"]
    score=coherence+pressure+genealogy+(.09 if roundtrip else 0.)
    # Comparable against a "rest" alternative; heat is independent of
    # conceptual activation, and only regulates selection stochasticity.
    rest=.92
    p=1./(1.+math.exp(-((score-rest)/temperature)))
    return round(p,7),round(score,6),round(rest,6)


def _feedback(act,focus,condition):
    if condition!="recursive_coupled" and condition!="recursive_genealogy_blind":
        return act.copy(),{}
    a={k:round(v*.990,6) for k,v in act.items()}
    delta={focus.lower():.11,"opposition":.085}
    if condition=="recursive_coupled":delta["coorigin"]=.06
    for k,v in delta.items():
        a[k]=round(min(1.,a[k]+v),6)
    if condition=="recursive_genealogy_blind":a["coorigin"]=0.
    return a,delta


def run(condition="recursive_coupled",mode="isosceles",seed=0,budget=8):
    if condition not in CONDITIONS or mode not in MODES:raise ValueError("Invalid condition/mode")
    if budget<1:raise ValueError("budget must be >= 1")
    graph=build_material(mode)
    packet=retrieve_opposition_pair(graph)
    witnesses,opposition_edges=role_witnesses(graph,packet)
    mapping={
        "paired_opposition_edges":opposition_edges,
        "angle_side_correspondences":packet["oppositions"],
        "material_mediator":packet["mediator"]["carrier"],
        "construction_event":packet["material_event"],
        "angle_pair":packet["angular_partition"]["children"],
        "side_pair":packet["segment_partition"]["children"],
        "source_angular_equality":packet["angle_equality_evidence"],
    }
    # Readings are directed perspectives on a shared mapping. The source of
    # metric equality is a given on ANGLE only; there is no reverse implication.
    focus="ANGLE"
    active=_activation(condition)
    source_given=bool(packet["angle_equality_evidence"])
    # Initial cognitive noticing: angular equality (if given), otherwise
    # angular partition. The angle graph is not "created" by this noticing.
    first=(witnesses["ANGLE"][-1] if source_given else witnesses["ANGLE"][0])
    acquired={first["id"]}
    interpretations=[{
        "focus":"ANGLE","origin_domain":None,"direction":"START",
        "new_witness":first,"witnesses":sorted(acquired),
        "epistemic_status":"given_angle_equality" if source_given else "structural_partition",
        "coorigin_event":packet["material_event"]
    }]
    timeline=[{
        "tick":0,"event":"CONSTRUCTION_AND_INITIAL_ATTENTION","focus":"ANGLE",
        "new_witness":first,"activation_before":active.copy(),
        "activation_after":active.copy(),"mapping":mapping,
        "acquired_witnesses":sorted(acquired),"generated_generic_spaces":[],
        "temperature":None,"status":"no metric transfer licensed"}]
    generics=[];questions=[];revisits=0;previous_targets={"ANGLE"}
    for tick in range(1,budget+1):
        target="SIDE" if focus=="ANGLE" else "ANGLE"
        if condition=="one_way" and target=="ANGLE":break
        remaining=[w for w in witnesses[target] if w["id"] not in acquired]
        if not remaining:break
        # Stable ordering of novelty witnesses is purposeful: once we reach
        # a perspective, first perceive its partition, then its carrier
        # boundary/contact. New role evidence supports a *new* reading.
        chosen=remaining[0]
        temperature=round(max(.37,.62-.032*(len(acquired)-1)),4)
        p,proposal_score,rest_score=_probability(
            condition,active,temperature,len(acquired),target in previous_targets)
        draw=random.Random(seed*100003+tick*353+17).random()
        if draw>p:
            timeline.append({
                "tick":tick,"event":"ATTENTION_STABILIZES",
                "focus":focus,"proposed_direction":focus+"→"+target,
                "candidate_witness":chosen["id"],"sample":round(draw,7),
                "rebase_probability":p,"proposal_score":proposal_score,
                "rest_score":rest_score,"temperature":temperature,
                "activation_before":active.copy(),"activation_after":active.copy(),
                "acquired_witnesses":sorted(acquired),
                "status":"stopped_without_new_rebase"
            })
            break
        before=active.copy()
        known_before=sorted(acquired)
        acquired.add(chosen["id"])
        reversed_into_known=target in previous_targets
        if reversed_into_known:revisits+=1
        previous_targets.add(target)
        focus=target
        active,delta=_feedback(active,focus,condition)
        # Every step can produce a richer perspective without duplicating
        # the already stored material graph. Only distinct graph-grounded
        # witnesses are counted; role alternation alone scores zero novelty.
        interp={
            "focus":focus,"origin_domain":"ANGLE" if focus=="SIDE" else "SIDE",
            "direction":"ANGLE→SIDE" if focus=="SIDE" else "SIDE→ANGLE",
            "new_witness":chosen,
            "witnesses":sorted(acquired),
            "reverse_revisitation":reversed_into_known,
            "coorigin_event":packet["material_event"],
            "relation_projection":"unknown" if focus=="SIDE" else
                                  ("given_angular_equality" if source_given else "unknown"),
            "epistemic_status":"structural_interpretation_not_proof"
        }
        interpretations.append(interp)
        new_generic={
            "id":"GS:opposition-perspective:"+str(len(generics)+1),
            "relation":"opposition_side_angle_pair",
            "origin_event":packet["material_event"],
            "carrier":packet["mediator"]["carrier"],
            "roles":packet["oppositions"],
            "direction":interp["direction"],
            "supports":sorted(acquired),
            "new_support":chosen["id"],
            "status":"candidate_abstract_reading_not_metric_proof"}
        generics.append(new_generic)
        question=None
        # Source equality is a property of actual given relations, not a
        # numerical coincidence; never create a side equality fact.
        if focus=="SIDE" and source_given:
            question={
                "source":{"domain":"ANGLE","objects":mapping["angle_pair"],
                          "relation":"equal_given",
                          "support":packet["angle_equality_evidence"]},
                "destination":{"domain":"SIDE","objects":mapping["side_pair"],
                               "relation":"equal?"},
                "mediator":mapping["material_mediator"],
                "through":opposition_edges,
                "epistemic_status":"HYPOTHESIS_ONLY",
                "licensed":False
            }
            questions.append(question)
        timeline.append({
            "tick":tick,"event":"REBASE_OPPOSITION","source_focus":interp["origin_domain"],
            "focus":focus,"direction":interp["direction"],
            "new_witness":chosen,"previously_known":known_before,
            "acquired_witnesses":sorted(acquired),
            "return_to_prior_focus":reversed_into_known,
            "temperature":temperature,"proposal_score":proposal_score,
            "rest_score":rest_score,"rebase_probability":p,
            "sample":round(draw,7),"feedback":delta,
            "activation_before":before,"activation_after":active.copy(),
            "generated_generic_spaces":[new_generic],
            "analogical_question":question,
            "provenance_chain":["CONSTRUCT:"+mapping["material_mediator"],
               "OPPOSITION_PAIR","REBASE:"+interp["direction"],
               chosen["id"]],
            "certified_metric_equalities":[],
            "status":"hypothesis_only" if question else "structural_candidate"
        })
    rebase_events=[e for e in timeline if e["event"]=="REBASE_OPPOSITION"]
    trace={
        "condition":condition,"mode":mode,"seed":seed,"budget":budget,
        "graph":{"nodes":graph["nodes"],"edges":graph["edges"]},
        "geometry":graph["geometry"],"mapping":mapping,
        "evidence_pool":witnesses,"source_equality_given":source_given,
        "initial_activation":_activation(condition),
        "timeline":timeline,"interpretations":interpretations,
        "generic_spaces":generics,"analogical_questions":questions,
        "metrics":{
            "rebase_count":len(rebase_events),
            "angle_to_side_count":sum(e["direction"]=="ANGLE→SIDE" for e in rebase_events),
            "side_to_angle_count":sum(e["direction"]=="SIDE→ANGLE" for e in rebase_events),
            "recursive_loop":any(e.get("return_to_prior_focus") for e in rebase_events),
            "return_visits_with_novelty":revisits,
            "distinct_witness_count":len(acquired),
            "new_role_supports":len(acquired)-1,
            "questions_raised":len(questions),
            "feedback_events":sum(bool(e.get("feedback")) for e in rebase_events),
            "redundant_rebases":sum(
                e["new_witness"]["id"] in e["previously_known"] for e in rebase_events),
            "false_metric_assertions":0
        }}
    assert trace["metrics"]["redundant_rebases"]==0
    assert all(e.get("certified_metric_equalities",[])==[] for e in timeline)
    return trace


def experiment(seeds=range(48),budget=8):
    runs=[run(c,m,s,budget) for m in MODES for c in CONDITIONS for s in seeds]
    agg={}
    for mode in MODES:
        agg[mode]={}
        for c in CONDITIONS:
            rr=[x for x in runs if x["condition"]==c and x["mode"]==mode]
            metric=lambda name:mean(x["metrics"][name] for x in rr)
            agg[mode][c]={
                "n":len(rr),
                "loop_rate":round(metric("recursive_loop"),4),
                "mean_rebases":round(metric("rebase_count"),3),
                "mean_novel_supports":round(metric("new_role_supports"),3),
                "mean_side_to_angle":round(metric("side_to_angle_count"),3),
                "mean_questions":round(metric("questions_raised"),3),
                "redundant_rebases":sum(x["metrics"]["redundant_rebases"] for x in rr),
                "false_metric_assertions":sum(x["metrics"]["false_metric_assertions"] for x in rr)
            }
    return {"schema":"merovingio.opposition_rebase_loop.v4",
            "description":"Recursive cognitive re-reading of opposing angle-side pairs only.",
            "non_empirical":True,"no_jev":True,"no_proof":True,
            "conditions":CONDITIONS,"modes":MODES,"seeds":list(seeds),"budget":budget,
            "aggregates":agg,"runs":runs}


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--seeds",type=int,default=48)
    p.add_argument("--budget",type=int,default=8)
    p.add_argument("--output",default=str(HERE/"results"))
    a=p.parse_args()
    out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
    r=experiment(range(a.seeds),a.budget)
    (out/"traces.json").write_text(json.dumps(r,indent=2,ensure_ascii=False),encoding="utf-8")
    (out/"aggregates.json").write_text(json.dumps(r["aggregates"],indent=2),encoding="utf-8")
    print(json.dumps(r["aggregates"],indent=2))
    print("Saved",out/"traces.json")


if __name__=="__main__":main()

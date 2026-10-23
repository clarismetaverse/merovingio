#!/usr/bin/env python3
"""Merovingio v6: productivity-driven recursive REBASE, ANGLE↔SIDE only.

Each selected opposition (angle, opposite side) updates a partial Generic Space
induced from the *construction's co-generated roles*. An incomplete GS can
favor its missing opposition. Completing it supplies a new relational reading
without asserting equal sides. Productive discoveries, rather than all merely
nearby nodes, provide the feedback signal.

The schema grammar, weights and ground-truth graph are hand-designed. This is
an engineering ablation, not a psychological test, human discovery or proof.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import random
import sys
from collections import defaultdict
from pathlib import Path
from statistics import mean

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/"gestalt_heat_v5"))
from dynamic import (
    build_material,coorigin_ledger,opposite_roles,initialize,
    candidate_score as v5_candidate_score,propagate,question_if_given,
    pair_generic
)

CONDITIONS=("fixed_initial","topology_only","predictive_only",
            "productivity_feedback","feedback_genealogy_blind")
MODES=("isosceles","scalene","ordinary_cevian")
ATTENTION=("clean","competing_oppositions")
MACROS=("angles","sides","opposition","coorigin")
T=0.59
BUDGET=4


def packet_schema(graph,packets):
    """Derive paired opposition slots from actual material partition packets."""
    found={}
    for packet in packets:
        pairs=packet["oppositions"]
        if len(pairs)!=2 or len(set(p["angle"] for p in pairs))!=2 or len(set(p["side"] for p in pairs))!=2:
            continue
        key="PS:"+hashlib.sha256("|".join(sorted(p["edge_id"] for p in pairs)).encode()).hexdigest()[:10]
        found[key]={
            "id":key,"slots":sorted(p["edge_id"] for p in pairs),
            "source_event":packet["material_event"],
            "medial_carrier":packet["mediator"]["carrier"],
            "angel_roles":sorted(p["angle"] for p in pairs),
            "side_roles":sorted(p["side"] for p in pairs),
            "given_angle_equality":bool(packet["angle_equality_evidence"]),
            "epistemic_status":"structural_template_not_proof"
        }
    return found


def initial_field(graph,packets,condition,attention):
    act,macro,sources=initialize(graph,packets,
        "macro_no_genealogy" if condition=="feedback_genealogy_blind" else "coupled")
    if attention=="competing_oppositions":
        # Introduce an attention challenge derived from the graph, not from a
        # hard-coded target answer: prime the two graph-grounded oppositions
        # with no participation in the CD co-generation packet.
        members={x["edge_id"] for p in packets for x in p["oppositions"]}
        distractors=[m for m in opposite_roles(graph) if m["id"] not in members]
        distractors=sorted(distractors,key=lambda x:x["id"])[:2]
        for m in distractors:
            act[m["angle"]]=1.0
            act[m["side"]]=max(.85,act[m["side"]])
    return act,macro,sources


def generic_increment(mapping,selected,schemas):
    """Prospective productivity of selecting this opposition, not a proof target.

    A co-generated partial role packet gives a first partial binding;
    filling its *unoccupied* second role is a stronger structural event.
    """
    effects=[]
    for schema in schemas.values():
        if mapping["id"] not in schema["slots"]:continue
        used=set(schema["slots"]) & selected
        if len(used)==0:
            effects.append({"type":"partial","schema":schema["id"],
                            "gain":.19, "new_slot":mapping["id"],
                            "origin":schema["source_event"]})
        elif len(used)==1:
            effects.append({"type":"completion","schema":schema["id"],
                            "gain":1.08,"new_slot":mapping["id"],
                            "origin":schema["source_event"]})
    return effects


def rank(graph,mappings,selected,focus,activation,macro,ledger,schemas,
         condition,boost):
    scored={}
    cond="macro_no_genealogy" if condition=="feedback_genealogy_blind" else "coupled"
    for mapping in mappings:
        if mapping["id"] in selected:continue
        base=v5_candidate_score(mapping,focus,activation,macro,ledger,cond,selected)
        predicted=generic_increment(mapping,selected,schemas)
        expected=(sum(x["gain"] for x in predicted)
                  if condition in ("predictive_only","productivity_feedback","feedback_genealogy_blind")
                  else 0.)
        if condition=="feedback_genealogy_blind":
            # A structural completion remains imaginable even if its common
            # construction source is hidden, but loses genealogical coherence.
            expected*=.42
        reward_boost=boost.get(mapping["id"],0.) if condition=="productivity_feedback" else 0.
        if condition=="feedback_genealogy_blind":
            reward_boost=boost.get(mapping["id"],0.)*.42
        scored[mapping["id"]]={
            "id":mapping["id"],"score":round(base["score"]+expected+reward_boost,6),
            "topological":base["score"],
            "prospective_productivity":round(expected,6),
            "realized_feedback":round(reward_boost,6),
            "predicted_events":predicted,"macro_support":base["macro_support"],
            "coorigin_support":base["coorigin_support"]}
    return scored


def choose(scores,seed,tick,condition,initial_rank):
    if condition=="fixed_initial":return next(id for id in initial_rank if id in scores)
    rng=random.Random(seed*1000003+tick*7919)
    winning,maximum=None,-1e30
    for key in sorted(scores):
        u=max(1e-12,min(1-1e-12,rng.random()))
        g=-math.log(-math.log(u))
        value=scores[key]["score"]/T+g
        if value>maximum: winning,maximum=key,value
    return winning


def realize(mapping,selected,schemas,graph):
    """Register partial and completed Generic Spaces from co-generated roles."""
    realized=[]
    for schema in schemas.values():
        if mapping["id"] not in schema["slots"]:continue
        occupied=sorted(set(schema["slots"]) & selected)
        if len(occupied)==1:
            realized.append({
                "id":"GS:partial:"+schema["id"],
                "kind":"INCOMPLETE_GENERIC",
                "origin":schema["source_event"],
                "carrier":schema["medial_carrier"],
                "occupied_roles":occupied,
                "missing_roles":sorted(set(schema["slots"])-set(occupied)),
                "supporting_angle_roles":[m for m in schema["angel_roles"]],
                "epistemic_status":"prospective_structural_candidate"
            })
        elif len(occupied)==2:
            realized.append({
                "id":"GS:complete:"+schema["id"],
                "kind":"COMPLETED_GENERIC",
                "origin":schema["source_event"],
                "carrier":schema["medial_carrier"],
                "occupied_roles":occupied,
                "missing_roles":[],
                "side_roles":schema["side_roles"],
                "angle_roles":schema["angel_roles"],
                "epistemic_status":"structural_analogy_not_metric_equality"
            })
    return realized


def feedback_signal(graph,selected_mapping,realized,schemas,boost,act,macro,
                    condition,allowed_candidates):
    """Only an actual partial/complete role binding may send feedback.

    The signal points to still-missing slots, not to the target equality
    label. Completed GS can strengthen the conceptual macro-opposition.
    """
    if condition not in ("productivity_feedback","feedback_genealogy_blind"):
        return boost.copy(),act.copy(),macro.copy(),[]
    nxt={k:round(v*.94,6) for k,v in boost.items()}
    new_act=act.copy()
    new_macro=macro.copy()
    causal=[]
    for event in realized:
        if event["kind"]=="INCOMPLETE_GENERIC":
            for missing in event["missing_roles"]:
                if missing not in allowed_candidates:continue
                gain=.73 if condition=="productivity_feedback" else .25
                nxt[missing]=round(min(2.,nxt.get(missing,0.)+gain),6)
                remaining=allowed_candidates[missing]
                for object_id in (remaining["angle"],remaining["side"]):
                    new_act[object_id]=round(min(1.,new_act[object_id]+gain*.18),6)
                causal.append({"from":event["id"],"to":missing,
                               "mechanism":"missing_opposition_role_salience",
                               "gain":gain})
        elif event["kind"]=="COMPLETED_GENERIC":
            gain=.19 if condition=="productivity_feedback" else .08
            new_macro["opposition"]=round(min(1.,new_macro["opposition"]+gain),6)
            if condition=="productivity_feedback":
                new_macro["coorigin"]=round(min(1.,new_macro["coorigin"]+.08),6)
            causal.append({"from":event["id"],"to":"macro.opposition",
                           "mechanism":"completed_generic_feedback",
                           "gain":gain})
    return nxt,new_act,new_macro,causal


def simulate(condition="productivity_feedback",mode="isosceles",seed=0,
             budget=BUDGET,attention="competing_oppositions"):
    if condition not in CONDITIONS or mode not in MODES or attention not in ATTENTION:
        raise ValueError("Unknown mode, condition or attention")
    if budget<1:raise ValueError("budget must be positive")
    graph=build_material(mode)
    packets,ledger=coorigin_ledger(graph)
    mappings=opposite_roles(graph)
    lookup={m["id"]:m for m in mappings}
    schemas=packet_schema(graph,packets)
    if not schemas: raise ValueError("No grounded co-generation schema")
    activation,macro,sources=initial_field(graph,packets,condition,attention)
    selected=set()
    memory={}
    boost={}
    generic_history=[]
    questions=[]
    start_rank=rank(graph,mappings,selected,"ANGLE",activation,macro,ledger,schemas,
                    "fixed_initial",boost)
    initial_order=sorted(start_rank,key=lambda k:(-start_rank[k]["score"],k))
    timeline=[{"tick":0,"operation":"CONSTRUCT_CD",
               "attention":attention,"source_angles":sources,
               "initial_ranking":initial_order,"macro_after":macro.copy(),
               "node_activation_after":activation.copy(),
               "status":"construction_facts_not_metric_conclusion"}]
    focus="ANGLE"
    seen_pair_keys=set()
    for tick in range(1,budget+1):
        scores=rank(graph,mappings,selected,focus,activation,macro,ledger,schemas,
                    condition,boost)
        if not scores:break
        candidate=choose(scores,seed,tick,condition,initial_order)
        prior_focus=focus
        focus="SIDE" if focus=="ANGLE" else "ANGLE"
        before=macro.copy()
        selected.add(candidate)
        chosen=lookup[candidate]
        realized=realize(chosen,selected,schemas,graph)
        delta=[x for x in realized if x["id"] not in memory]
        for x in delta:
            memory[x["id"]]=x
        # Distinct instances may be structurally analogous without a shared
        # construction; report them but never reward them as co-origin GS.
        alternate_structural=0
        for previous in selected-{candidate}:
            try_g=pair_generic(graph,{},lookup[previous],chosen,packets)
            if try_g and not try_g["genealogical_source"]:
                key=tuple(sorted((previous,candidate)))
                if key not in seen_pair_keys:
                    seen_pair_keys.add(key)
                    alternate_structural+=1
        fresh_questions=[]
        for x in delta:
            if x["kind"]!="COMPLETED_GENERIC":continue
            g={"angle_roles":x["angle_roles"],"side_roles":x["side_roles"],
               "edges":x["occupied_roles"]}
            q=question_if_given(graph,g)
            if q:
                fresh_questions.append(q)
                questions.append(q)
        # All active-search regimes preserve v5 structural propagation,
        # but ONLY the productivity variant also feeds novel Generic roles back.
        if condition!="fixed_initial":
            activation,changes=propagate(graph,activation,chosen,ledger,
                use_origin=condition!="feedback_genealogy_blind")
        else:changes=[]
        allowed={m["id"]:m for m in mappings if m["id"] not in selected}
        boost,activation,macro,causal=feedback_signal(
            graph,chosen,delta,schemas,boost,activation,macro,condition,allowed)
        # Compare counterfactual ranking within the *same* next focus to
        # avoid treating obligatory ANGLE/SIDE switching as a ranking change.
        remaining=rank(graph,mappings,selected,focus,activation,macro,ledger,schemas,
                       condition,boost)
        before_scores=rank(graph,mappings,selected,focus,
                           timeline[-1].get("node_activation_after",activation),
                           before,ledger,schemas,condition,{})
        relative_before=sorted(before_scores,key=lambda k:(-before_scores[k]["score"],k))
        relative_after=sorted(remaining,key=lambda k:(-remaining[k]["score"],k))
        timeline.append({
            "tick":tick,"operation":"REBASE_OPPOSITE_PAIR",
            "from":prior_focus,"to":focus,
            "selected_opposition":chosen,
            "chosen_score":scores[candidate],
            "score_candidates_before":scores,
            "new_generic_events":delta,
            "non_cogenerative_generic_pairs":alternate_structural,
            "new_questions":fresh_questions,
            "feedback_causes":causal,
            "macro_before":before,"macro_after":macro.copy(),
            "node_activation_changes":changes,
            "node_activation_after":activation.copy(),
            "relative_ranking_before_new_group":relative_before,
            "relative_ranking_after_new_group":relative_after,
            "ranking_changed_by_feedback":relative_before!=relative_after,
            "acquired_oppositions":sorted(selected),
            "certified_metric_equalities":[],
            "epistemic_status":"analogy_not_proof"})
    events=timeline[1:]
    return {
        "condition":condition,"mode":mode,"seed":seed,"budget":budget,"attention":attention,
        "material":{"nodes":graph["nodes"],"edges":graph["edges"]},
        "geometry":graph["geometry"],"source_given_angles":graph["given_equal_angles"],
        "oppositions":mappings,"construction_schemas":list(schemas.values()),
        "timeline":timeline,"generic_spaces":list(memory.values()),
        "analogical_questions":questions,
        "metrics":{
            "selected_oppositions":len(selected),
            "partial_generic_count":sum(x["kind"]=="INCOMPLETE_GENERIC" for x in memory.values()),
            "complete_generic_count":sum(x["kind"]=="COMPLETED_GENERIC" for x in memory.values()),
            "question_found":bool(questions),
            "first_completion_tick":next((e["tick"] for e in events if any(
                x["kind"]=="COMPLETED_GENERIC" for x in e["new_generic_events"])),None),
            "feedback_signal_count":sum(len(e["feedback_causes"]) for e in events),
            "relative_rerankings":sum(e["ranking_changed_by_feedback"] for e in events),
            "false_metric_certifications":0,
            "duplicate_mapping_rebases":sum(1 for e in events if
                e["selected_opposition"]["id"] not in e["acquired_oppositions"])
        }
    }


def experiment(seeds=range(32),budget=BUDGET):
    results=[simulate(c,m,s,budget,a) for a in ATTENTION
            for m in MODES for c in CONDITIONS for s in seeds]
    agg={}
    for a in ATTENTION:
        agg[a]={}
        for m in MODES:
            agg[a][m]={}
            for c in CONDITIONS:
                rr=[r for r in results if r["attention"]==a and
                    r["mode"]==m and r["condition"]==c]
                n=lambda key:mean(r["metrics"][key] for r in rr)
                agg[a][m][c]={
                    "trials":len(rr),
                    "complete_rate":round(n("complete_generic_count"),4),
                    "question_rate":round(n("question_found"),4),
                    "mean_first_completion_tick_if_found":(
                        round(mean(r["metrics"]["first_completion_tick"] for r in rr
                         if r["metrics"]["first_completion_tick"] is not None),3)
                        if any(r["metrics"]["complete_generic_count"] for r in rr) else None),
                    "mean_feedback_signals":round(n("feedback_signal_count"),4),
                    "mean_relative_rerankings":round(n("relative_rerankings"),4),
                    "false_metric_certifications":sum(r["metrics"]["false_metric_certifications"] for r in rr)}
    return {"schema":"merovingio.productivity_driven_rebase.v6",
            "explanation":"Predicted vs actually realized GS completion, controlled causal salience propagation.",
            "limits":"Engineered rule/weight simulation, not human psychology or a proof system.",
            "conditions":CONDITIONS,"modes":MODES,"attentions":ATTENTION,
            "seeds":list(seeds),"budget":budget,"no_proof":True,"no_jev":True,
            "aggregates":agg,"runs":results}


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--seeds",type=int,default=32)
    p.add_argument("--budget",type=int,default=BUDGET)
    p.add_argument("--output",default=str(HERE/"results"))
    args=p.parse_args()
    out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    data=experiment(range(args.seeds),args.budget)
    (out/"traces.json").write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
    (out/"aggregates.json").write_text(json.dumps(data["aggregates"],indent=2),encoding="utf-8")
    print(json.dumps(data["aggregates"],indent=2))
    print("Saved",out/"traces.json")


if __name__=="__main__":main()

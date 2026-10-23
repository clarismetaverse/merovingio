#!/usr/bin/env python3
"""Merovingio v5: dynamic graph-guided REBASE of angle↔side opposition mappings.

The next mapping is NOT read from a fixed ordered witness list: after each
rebase, newly selected role pairs spread activation to connected objects,
candidate opposite relations are re-scored, and a fresh codelet is sampled.
Every hypothesis is non-certifying. Codelets never rebase triangles.
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
sys.path.insert(0,str(HERE.parent/"gestalt_heat_v3"))
from poristic import build_material, co_generations

CONDITIONS=("fixed_order","local_only","macro_no_feedback",
            "macro_no_genealogy","coupled")
MODES=("isosceles","scalene","ordinary_cevian")
MACROS=("angles","sides","opposition","coorigin")
PRIOR={"angles":.72,"sides":.55,"opposition":.76,"coorigin":.82}
BRIDGE_KIND={"opposite","bounds_angle","part_of","endpoint","boundary","angle_in_region"}
SCORED_NEIGHBORS={"part_of":.75,"bounds_angle":.65,"endpoint":.64,
                  "opposite":.82,"boundary":.31,"angle_in_region":.26}


def opposite_roles(graph):
    """Enumerate all possible *single* opposite angle-side mappings from facts."""
    out=[]
    for eid,e in graph["edges"].items():
        if e["kind"]!="opposite":continue
        a=[n for n in e["nodes"] if graph["nodes"][n]["kind"]=="angle"]
        s=[n for n in e["nodes"] if graph["nodes"][n]["kind"]=="side"]
        if len(a)==1 and len(s)==1:
            out.append({"id":eid,"angle":a[0],"side":s[0],
                        "triangle":e.get("triangle"),"relation":"opposite",
                        "epistemic_status":"graph_derived_structural"})
    return sorted(out,key=lambda x:x["id"])


def coorigin_ledger(graph):
    packets=co_generations(graph)
    # Each packet exists before exploration, but is not an inferential proof.
    ledger={}
    for p in packets:
        for pair in p["oppositions"]:
            ledger.setdefault(pair["edge_id"],[]).append({
                "event":p["material_event"],
                "carrier":p["mediator"]["carrier"],
                "co_generated_angle_partition":p["angular_partition"]["edge_ids"],
                "co_generated_side_partition":p["segment_partition"]["edge_ids"]})
    return packets,ledger


def graph_adjacency(graph):
    neighbors=defaultdict(list)
    for eid,e in graph["edges"].items():
        if e["kind"] not in BRIDGE_KIND:continue
        a,b=e["nodes"]
        strength=SCORED_NEIGHBORS[e["kind"]]
        neighbors[a].append((b,eid,strength))
        neighbors[b].append((a,eid,strength))
    return neighbors


def given_sources(graph,packets):
    """Focus on constructed angular partitions; never presume equal sides."""
    sources=set(graph["given_equal_angles"])
    if sources:return sorted(sources)
    # For a generic cevian there are angular parts but no equality.
    for packet in packets:
        sources.update(packet["angular_partition"]["children"])
    return sorted(sources)


def initialize(graph,packets,condition):
    sources=given_sources(graph,packets)
    act={n:0. for n in graph["nodes"]}
    # Preliminary angular Gestalt is present from construction.
    for n in sources:act[n]=.87
    for packet in packets:
        carrier=packet["mediator"]["carrier"]
        act[carrier]=max(act.get(carrier,0),.30)
        for seg in packet["segment_partition"]["children"]:
            act[seg]=max(act.get(seg,0),.12)
    macro=dict.fromkeys(MACROS,0.) if condition=="local_only" else PRIOR.copy()
    if condition=="macro_no_genealogy":macro["coorigin"]=0.
    return act,macro,sources


def candidate_score(mapping,focus,node_act,macro,ledger,condition,chosen_ids):
    """Re-evaluate each unseen opposition using current *local* salience."""
    source=mapping["angle"] if focus=="ANGLE" else mapping["side"]
    target=mapping["side"] if focus=="ANGLE" else mapping["angle"]
    local=.95*node_act[source]+.32*node_act[target]
    inherited=.30*macro["opposition"]+.25*macro["angles" if focus=="ANGLE" else "sides"]
    provenance=.72*macro["coorigin"] if mapping["id"] in ledger else 0.
    if condition in ("macro_no_genealogy","local_only"):provenance=0.
    novelty=0.0
    if mapping["id"] in chosen_ids:novelty=-100.
    # A motif is particularly promising if one of its roles is already
    # activated by the most recent grouping, not if it has a target label.
    raw=.16+local+inherited+provenance+novelty
    return {"id":mapping["id"],"score":round(raw,6),
            "current_source":source,"target":target,
            "local_support":round(local,6),
            "macro_support":round(inherited,6),
            "coorigin_support":round(provenance,6),
            "novelty_penalty":novelty}


def propagate(graph,node_act,mapping,ledger,use_origin=True):
    """Spread newly acquired oppositional grouping to graph neighbors.

    Importantly, this changes relative candidate salience. No relation is
    added to the material graph, and no metric fact is inferred.
    """
    neighbors=graph_adjacency(graph)
    before=node_act.copy()
    additions=defaultdict(float)
    touched=(mapping["angle"],mapping["side"])
    for src in touched:
        additions[src]+=.30
        for dst,eid,strength in neighbors[src]:
            additions[dst]+=.23*strength
            # Next halo allows a side partition at D to prime the *other*
            # base segment and its opposite angular role.
            for nxt,_,s2 in neighbors[dst]:
                if nxt!=src:additions[nxt]+=.085*strength*s2
    if use_origin and mapping["id"] in ledger:
        for relation in ledger[mapping["id"]]:
            for eid in relation["co_generated_angle_partition"]+relation["co_generated_side_partition"]:
                for n in graph["edges"][eid]["nodes"]:
                    additions[n]+=.065
    after={}
    for n,old in node_act.items():
        # Small decay keeps fixed early nodes from dominating indefinitely.
        after[n]=round(min(1.,old*.955+additions[n]),6)
    changed=[{"node":n,"before":round(before[n],4),"after":after[n],
              "delta":round(after[n]-before[n],4)}
             for n in after if abs(after[n]-before[n])>=.002]
    changed.sort(key=lambda d:-abs(d["delta"]))
    return after,changed[:20]


def macro_feedback(macro,mapping,focus,ledger,condition):
    if condition not in ("coupled","macro_no_genealogy"):return macro.copy(),{}
    updated={k:round(v*.988,6) for k,v in macro.items()}
    gains={"opposition":.085,"sides" if focus=="SIDE" else "angles":.11}
    if mapping["id"] in ledger and condition=="coupled":
        gains["coorigin"]=.055
    for k,v in gains.items():updated[k]=round(min(1.,updated[k]+v),6)
    if condition=="macro_no_genealogy":updated["coorigin"]=0.
    return updated,gains


def choose(frontier,seed,tick,condition,baseline_order):
    if condition=="fixed_order":
        # One static ranking computed BEFORE any grouping; unchanged by new
        # evidence. No role-specific re-ranking after a move.
        return next(eid for eid in baseline_order if eid in frontier),{"strategy":"static_initial_ranking"}
    rng=random.Random(seed*1000003+tick*7919)
    temp=max(.38,.68-.03*tick)
    best,maxval=None,-float("inf")
    for key in sorted(frontier):
        u=max(1e-12,min(1-1e-12,rng.random()))
        z=frontier[key]["score"]/temp-math.log(-math.log(u))
        if z>maxval:best,maxval=key,z
    return best,{"strategy":"dynamic_gumbel_softmax","temperature":round(temp,4)}


def pair_generic(graph,discovered,first,second,packets):
    """Induce a generic if two actual opposition relations share a context.

    The paired is a new abstract *candidate*, not a metric conclusion.
    """
    if first["id"]==second["id"]:return None
    angles={first["angle"],second["angle"]}
    sides={first["side"],second["side"]}
    if len(angles)!=2 or len(sides)!=2:return None
    origins=sorted({p["material_event"] for p in packets if
                    {first["id"],second["id"]}<=
                    {q["edge_id"] for q in p["oppositions"]}})
    sharing=bool(origins)
    if not sharing:
        # Alternate reading may align around a shared vertex or side contact.
        a=graph["nodes"][first["angle"]]
        b=graph["nodes"][second["angle"]]
        sharing=(a["vertex"]==b["vertex"] or
            bool(set(graph["nodes"][first["side"]]["vertices"]) &
                 set(graph["nodes"][second["side"]]["vertices"])))
    if not sharing:return None
    k="GS:"+hashlib.sha256(("|".join(sorted((first["id"],second["id"])))).encode()).hexdigest()[:10]
    if k in discovered:return None
    return {"id":k,"relation":"aligned_angular_segment_oppositions",
            "edges":sorted((first["id"],second["id"])),
            "angle_roles":sorted(angles),"side_roles":sorted(sides),
            "genealogical_source":origins,
            "status":"candidate_GS_no_metric_certification"}


def question_if_given(graph,generic):
    if not generic:return None
    if set(generic["angle_roles"])!=set(graph["given_equal_angles"]):return None
    return {"source":{"objects":generic["angle_roles"],"relation":"equal_given"},
            "target":{"objects":generic["side_roles"],"relation":"equal?"},
            "through":generic["edges"],"direction":"angular_to_segmental",
            "epistemic_status":"HYPOTHESIS_ONLY","proven":False}


def simulate(condition="coupled",mode="isosceles",seed=0,budget=8):
    if condition not in CONDITIONS or mode not in MODES:raise ValueError("bad condition/mode")
    if budget<1:raise ValueError("budget>=1 required")
    graph=build_material(mode)
    packets,ledger=coorigin_ledger(graph)
    candidates=opposite_roles(graph)
    assert len(candidates)>=5
    node_act,macro,sources=initialize(graph,packets,condition)
    # Baseline rank computed at t=0, frozen even if attention would change.
    fixed_initial={m["id"]:candidate_score(
        m,"ANGLE",node_act,macro,ledger,condition,set()) for m in candidates}
    baseline_order=sorted(fixed_initial,key=lambda k:(-fixed_initial[k]["score"],k))
    chosen=set()
    history=[]
    generics={}
    questions=[]
    timeline=[{"tick":0,"operation":"CONSTRUCTION_CD_AND_SOURCE_FOCUS",
               "focus":"ANGLE","initial_sources":sources,"macro_after":macro.copy(),
               "node_activation_after":node_act.copy(),
               "available_mapping_count":len(candidates),"selected":None,
               "new_generic_spaces":[],"epistemic_status":"constructed_not_proven"}]
    focus="ANGLE"
    for tick in range(1,budget+1):
        available=[m for m in candidates if m["id"] not in chosen]
        if not available:break
        # A REBASE alternates domains; *which* angle-side opposition it binds
        # is determined by dynamically ranking all remaining material edges.
        scores={m["id"]:candidate_score(m,focus,node_act,macro,ledger,condition,chosen)
                for m in available}
        choice,choice_info=choose(scores,seed,tick,condition,baseline_order)
        selected=next(m for m in available if m["id"]==choice)
        old_rank=[x["id"] for x in sorted(scores.values(),key=lambda z:(-z["score"],z["id"]))]
        before=macro.copy()
        before_nodes=node_act.copy()
        chosen.add(choice)
        target="SIDE" if focus=="ANGLE" else "ANGLE"
        reading={"id":"READ:"+str(tick),"from":focus,"to":target,
                 "new_opposition_edge":choice,"carrier_source_event":ledger.get(choice,[]),
                 "epistemic_status":"structural_role_rebase"}
        new_generics=[]
        for previous in history:
            generic=pair_generic(graph,generics,previous["new_opposition_edge"],selected,packets)
            if generic:
                generics[generic["id"]]=generic
                new_generics.append(generic)
                q=question_if_given(graph,generic)
                if q:questions.append(q)
        history.append(reading)
        # Dynamic reranking: a group changes the graph-object activation halo.
        if condition!="fixed_order":
            node_act,node_change=propagate(graph,node_act,selected,ledger,
                use_origin=condition!="macro_no_genealogy")
        else:node_change=[]
        if condition=="local_only":
            macro=dict.fromkeys(MACROS,0.)
        else:macro,_=macro_feedback(macro,selected,target,ledger,condition)
        # Experimentally observable counterfactual: rank remaining candidates
        # before vs after the new group. Static baseline keeps ranking frozen.
        remaining=[m for m in candidates if m["id"] not in chosen]
        after_scores={m["id"]:candidate_score(m,target,node_act,macro,ledger,condition,chosen)
                      for m in remaining}
        next_ranking=sorted(after_scores,key=lambda k:(-after_scores[k]["score"],k))
        # Controlled within-focus comparison: isolate the effect of new
        # salience from the mandatory change of perspective.
        pre_same={m["id"]:candidate_score(m,target,before_nodes,before,ledger,condition,chosen)
                  for m in remaining}
        prior_ranking=sorted(pre_same,key=lambda k:(-pre_same[k]["score"],k))
        changed_order=prior_ranking!=next_ranking
        timeline.append({
            "tick":tick,"operation":"OPPOSITION_REBASE",
            "from":focus,"to":target,
            "selected":reading,
            "selected_score":scores[choice],
            "candidate_scores_before":scores,
            "ranking_before_selection":old_rank,
            "next_ranking":next_ranking,
            "within_target_ranking_before_propagation":prior_ranking,
            "relative_rank_changed_by_new_group":changed_order if condition!="fixed_order" else False,
            "new_generics":new_generics,
            "new_questions":[q for q in questions if q["through"] in [g["edges"] for g in new_generics]],
            "macro_before":before,"macro_after":macro.copy(),
            "changed_node_activation":node_change,
            "node_activation_after":node_act.copy(),
            "choice_info":choice_info,
            "epistemic_status":"mapping_candidate_not_proof",
            "certified_metric_equalities":[]})
        focus=target
    rebase_events=timeline[1:]
    data={
        "condition":condition,"mode":mode,"seed":seed,"budget":budget,
        "graph":{"nodes":graph["nodes"],"edges":graph["edges"]},
        "geometry":graph["geometry"],"packets":packets,
        "opposition_mappings":candidates,
        "construction_ledger":ledger,
        "source_given_angles":graph["given_equal_angles"],
        "timeline":timeline,"selected_readings":history,
        "generic_spaces":list(generics.values()),
        "analogical_questions":questions,
        "metrics":{
            "rebases":len(rebase_events),
            "distinct_opposition_edges":len(chosen),
            "induced_generic_spaces":len(generics),
            "target_transfer_question_found":bool(questions),
            "first_question_tick":next((e["tick"] for e in rebase_events if e["new_questions"]),None),
            "dynamic_rank_reorderings":sum(e["relative_rank_changed_by_new_group"] for e in rebase_events),
            "feedback_events":sum(e["macro_after"]!=e["macro_before"] for e in rebase_events),
            "false_metric_assertions":0,
            "duplicate_mapping_rebases":len(history)-len(chosen),
        }}
    assert data["metrics"]["duplicate_mapping_rebases"]==0
    assert all(not e.get("certified_metric_equalities") for e in timeline)
    return data


def experiment(seeds=range(32),budget=8):
    runs=[simulate(c,m,s,budget) for m in MODES for c in CONDITIONS for s in seeds]
    agg={}
    for mode in MODES:
        agg[mode]={}
        for cond in CONDITIONS:
            rr=[r for r in runs if r["mode"]==mode and r["condition"]==cond]
            avg=lambda field:mean(r["metrics"][field] for r in rr)
            agg[mode][cond]={
                "n":len(rr),
                "transfer_question_rate":round(avg("target_transfer_question_found"),4),
                "mean_induced_generics":round(avg("induced_generic_spaces"),4),
                "mean_rank_reorderings":round(avg("dynamic_rank_reorderings"),4),
                "mean_distinct_oppositions":round(avg("distinct_opposition_edges"),4),
                "mean_first_question_tick_if_found":(
                   round(mean(r["metrics"]["first_question_tick"] for r in rr
                              if r["metrics"]["first_question_tick"] is not None),3)
                   if any(r["metrics"]["target_transfer_question_found"] for r in rr) else None),
                "false_metric_assertions":sum(r["metrics"]["false_metric_assertions"] for r in rr)
            }
    return {"schema":"merovingio.dynamic_opposition_rebase.v5",
            "definition":"Graph-derived opposition edge REBASE, online salience reranking, memory of structural role pairings.",
            "conditions":CONDITIONS,"modes":MODES,"seeds":list(seeds),"budget":budget,
            "non_empirical":True,"no_proof":True,"no_jev":True,
            "aggregates":agg,"runs":runs}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--seeds",type=int,default=32)
    ap.add_argument("--budget",type=int,default=8)
    ap.add_argument("--output",default=str(HERE/"results"))
    a=ap.parse_args()
    out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
    data=experiment(range(a.seeds),a.budget)
    (out/"traces.json").write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
    (out/"aggregates.json").write_text(json.dumps(data["aggregates"],indent=2),encoding="utf-8")
    print(json.dumps(data["aggregates"],indent=2))
    print("Saved",out/"traces.json")

if __name__=="__main__":main()

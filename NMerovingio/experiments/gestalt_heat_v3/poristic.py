#!/usr/bin/env python3
"""Merovingio v3: a construction is a polysemic generator of relational readings.

The *same material event* creates angle and side partitions plus adjacent
triangle roles. Co-origin may spread activation, directing subsequent
angle→side analogical binding. No metric equality is concluded by analogy.

Candidate Gestalten remain graph-generated; operator grammar and priors are
explicitly engineered, not learned or evidence for Euclid's psychology.
"""
from __future__ import annotations
import argparse
import itertools
import json
import math
import random
import sys
from collections import defaultdict
from pathlib import Path
from statistics import mean

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/"gestalt_heat_v2"))
from endogenous import (
    make_graph, side, group_from_edges, proposals as graph_proposals,
    candidate_score as graph_candidate_score, select_softmax,
    relation_signature, equal_angle_witness, fixture_contract
)

CONDITIONS=("no_macro","macro_only","cogeneration_only","coupled","genealogy_blinded")
MODES=("isosceles","scalene","ordinary_cevian")
MACROS=("angles","sides","opposition","partition","shared","genealogy","transfer")
INIT={"angles":.64,"sides":.64,"opposition":.78,"partition":.58,
      "shared":.38,"genealogy":.84,"transfer":.30}


def build_material(mode):
    """An arbitrary interior transversal has dual partitions even without equality."""
    if mode not in MODES: raise ValueError(mode)
    graph=make_graph("scalene" if mode=="ordinary_cevian" else mode)
    if mode=="ordinary_cevian":
        # Replace the bisector intersection by an arbitrary interior point,
        # keep incidence topology; remove the bisector's *metric* given.
        points=graph["geometry"]["points"]
        a,b=points["A"],points["B"]
        d=[a[i]+.38*(b[i]-a[i]) for i in range(2)]
        points["D"]=d
        graph["geometry"]["observations"]["AD"]=math.dist(a,d)
        graph["geometry"]["observations"]["DB"]=math.dist(d,b)
        graph["geometry"]["observations"]["base_halves_equal_by_coordinates"]=False
        graph["geometry"]["construction_given"]=[]
        graph["geometry"]["hypotheses_only"]=[
            "No equality of angular sectors or base segments follows from an arbitrary cevian"]
        graph["given_equal_angles"]=[]
        graph["edges"]={eid:e for eid,e in graph["edges"].items()
                        if e["kind"]!="equal_given"}
    graph["geometry"]["mode"]=mode
    graph["certified_metric_equalities"]=[]
    return graph


def partition_families(graph):
    """Derive child-pairs from PART_OF edges, grouped by parent/type."""
    buckets=defaultdict(list)
    for eid,e in graph["edges"].items():
        if e["kind"]!="part_of":continue
        x,y=e["nodes"]
        if graph["nodes"][x]["kind"]!=graph["nodes"][y]["kind"]:continue
        # Parent carries both child segments/angles in the same relation.
        for candidate_parent in (x,y):
            candidate_child=y if candidate_parent==x else x
            buckets[candidate_parent].append((candidate_child,eid))
    families=[]
    for parent,pairs in buckets.items():
        # Choose parents that have >=2 distinct *proper* child objects.
        # Topology: parent is longer (endpoints of both child sides) or
        # has both child angular rays (outside endpoints).
        n=graph["nodes"][parent]
        if n["kind"]=="side":
            pv=set(n["vertices"])
            children=[(x,eid) for x,eid in pairs if
                      len(pv.intersection(graph["nodes"][x]["vertices"]))==1]
        elif n["kind"]=="angle":
            children=[(x,eid) for x,eid in pairs if
                      graph["nodes"][x]["vertex"]==n["vertex"]]
        else:continue
        if len(children)<2:continue
        # Group exactly two for a binary split; arbitrary larger sets may
        # generate multiple hypotheses in later generalized partitions.
        for x,y in itertools.combinations(children,2):
            families.append({
                "domain":n["kind"],"parent":parent,
                "children":sorted([x[0],y[0]]),
                "edge_ids":sorted([x[1],y[1]]),
                "origins":sorted({graph["edges"][x[1]]["origin"],
                                  graph["edges"][y[1]]["origin"]})
            })
    return families


def common_term(graph, angular, segmental):
    """Discover a physical C-D mediator from shared angular ray and contact D.

    Neither C nor D is identified by a pre-written answer group.
    """
    nodes=graph["nodes"]
    ans=[nodes[n] for n in angular["children"]]
    sn=[nodes[n] for n in segmental["children"]]
    vertices={x["vertex"] for x in ans}
    if len(vertices)!=1: return None
    vertex=next(iter(vertices))
    common_arms=set(ans[0]["arms"]) & set(ans[1]["arms"])
    contact=set(sn[0]["vertices"]) & set(sn[1]["vertices"])
    for d in sorted(contact & common_arms):
        if side(vertex,d) in nodes:
            return {"vertex":vertex,"contact":d,"carrier":side(vertex,d),
                    "incidence":"CARRIER_ENDPOINT_AND_SEGMENT_SPLIT_CONTACT"}
    return None


def opposite_correspondences(graph,angular,segmental):
    """Derive role-opposition candidates by traversing actual opposite edges."""
    a=set(angular["children"]);s=set(segmental["children"])
    pairs=[]
    for eid,e in graph["edges"].items():
        if e["kind"]=="opposite":
            hit_a=next((x for x in e["nodes"] if x in a),None)
            hit_s=next((x for x in e["nodes"] if x in s),None)
            if hit_a and hit_s:pairs.append({"angle":hit_a,"side":hit_s,"edge_id":eid})
    return sorted(pairs,key=lambda x:x["edge_id"])


def co_generations(graph):
    """One event -> simultaneously available groupings in multiple domains.

    The event ledger and the geometric packet are SEPARATE: a provenance
    ablation hides genealogical identity, but never deletes the geometry.
    """
    families=partition_families(graph)
    packets=[]
    for angular in (f for f in families if f["domain"]=="angle"):
        for segmental in (f for f in families if f["domain"]=="side"):
            mediator=common_term(graph,angular,segmental)
            if not mediator:continue
            if set(angular["children"]) & set(segmental["children"]):continue
            opposite=opposite_correspondences(graph,angular,segmental)
            triangles=sorted(t for t in graph["triangles"] if
                  graph["nodes"][t]["kind"]=="region" and
                  mediator["carrier"] in [s for s in [
                      "S:"+"".join(sorted(ab)) for ab in
                      itertools.combinations(graph["nodes"][t]["vertices"],2)]])
            # The shared material carrier must participate in two regions;
            # it is an interpretive hub, not a theorem proof.
            if len(triangles)<2:continue
            match={}
            equal_edges=[eid for eid,e in graph["edges"].items()
                         if e["kind"]=="equal_given" and
                         set(e["nodes"])==set(angular["children"])]
            identity="CONSTRUCT:"+mediator["carrier"]
            packets.append({
                "id":"PACKET:"+mediator["carrier"],
                "material_event":identity,
                "ledger_source":"v2 construction / contacts",
                "co_origin_claim":"both angular and segment splits arise from one constructed carrier",
                "angular_partition":angular,
                "segment_partition":segmental,
                "mediator":mediator,
                "regions":triangles,
                "oppositions":opposite,
                "angle_equality_evidence":equal_edges,
                "structural_status":"co_generated_role_packet",
                "equality_status":"given_only_for_angles" if equal_edges else "no_equalities_given",
            })
    return packets


def packet_groups(graph, packets, selected, done):
    """Grammar expansion of co-created readings: coframe, then opposition rebasing.

    Preconditions for REBASE are formed *Gestalten*, not merely graph existence.
    This keeps the direction/origination of analogical transfer traceable.
    """
    result={}
    for packet in packets:
        eids=sorted(packet["angular_partition"]["edge_ids"]+
                    packet["segment_partition"]["edge_ids"])
        co=group_from_edges(graph,eids,"COFRAME")
        co.update({"packet_id":packet["id"],"mediator":packet["mediator"]["carrier"],
                   "role_families":["angle_split","side_split","shared_carrier"],
                   "regions":packet["regions"],"parents":[],
                   "provenance_event":packet["material_event"]})
        if co["id"] not in done:result[co["id"]]=co
        if co["id"] not in selected or len(packet["oppositions"])<2:continue
        for pair in itertools.combinations(packet["oppositions"],2):
            if pair[0]["angle"]==pair[1]["angle"] or pair[0]["side"]==pair[1]["side"]:continue
            rel=[pair[0]["edge_id"],pair[1]["edge_id"]]
            # A known equal-angle pair may be a SOURCE of transfer but is
            # never assumed in arbitrary-transversal negative control.
            rel+=packet["angle_equality_evidence"]
            g=group_from_edges(graph,rel,"REBASE",(co["id"],))
            g.update({"packet_id":packet["id"],"mediator":packet["mediator"]["carrier"],
                      "opposition_roles":sorted([pair[0],pair[1]],key=lambda x:x["angle"]),
                      "has_angular_equality":bool(packet["angle_equality_evidence"]),
                      "direction":"angles→sides" if packet["angle_equality_evidence"]
                                  else "undirected_structural_analogy",
                      "provenance_event":packet["material_event"]})
            if g["id"] not in done:result[g["id"]]=g
    return result


def activation_init(condition):
    if condition=="no_macro": return dict.fromkeys(MACROS,0.)
    act=INIT.copy()
    if condition=="macro_only":act["genealogy"]=0.
    if condition=="cogeneration_only":
        act={k:0. for k in MACROS}
        act["genealogy"]=INIT["genealogy"]
    if condition=="genealogy_blinded": act["genealogy"]=0.
    return act


def score(graph,g,activation,condition,packet):
    """Pressure biases attention, never truth; ledger blinding is independent."""
    if g["operator"] not in ("COFRAME","REBASE"):
        # All original v2 graph-generated SEED/EXTEND/ALIGN remain present.
        score_,inherited,sources=graph_candidate_score(graph,g,activation)
        return score_,inherited,sources
    base=.61 if g["operator"]=="COFRAME" else .79
    analog=(.20*activation["angles"]+.20*activation["sides"]+
            .32*activation["opposition"]+.24*activation["partition"])
    # Source and target may be empty until an equal-angle witness exists.
    origin_visible=condition in ("cogeneration_only","coupled")
    geo_bonus=(2.45*activation["genealogy"] if origin_visible else 0.)
    shared=.20*activation["shared"]
    if g["operator"]=="REBASE":
        analog += .80*activation["opposition"]+.38*activation["transfer"]
        if g["has_angular_equality"]: analog+=.27*activation["angles"]
    bias=geo_bonus+analog+shared
    score_=round(base+bias+.045*len(g["relations"]),6)
    source={"macro_cross_domain":round(analog,5),
            "shared_carrier":round(shared,5),
            "construction_genealogy":round(geo_bonus,5)}
    return score_,round(bias,6),source


def update_activation(act,g,condition,packet):
    before=act.copy()
    if condition not in ("coupled","genealogy_blinded"):
        return before,{},None
    new={k:round(v*.985,6) for k,v in act.items()}
    update={}
    kinds=set(g["kinds"]);rel=set(g["relation_types"])
    for k,key in (("angle","angles"),("side","sides")):
        if k in kinds:update[key]=.045
    if "opposite" in rel and g["cross_domain"]:update["opposition"]=.08
    if "part_of" in rel:update["partition"]=.06
    if g["operator"] in ("COFRAME","REBASE"):
        update["shared"]=.10
        if condition=="coupled":
            update["genealogy"]=.085
        if g["operator"]=="REBASE" and g.get("has_angular_equality"):
            update["transfer"]=.17
    for k,v in update.items():new[k]=round(min(1.,new[k]+v),6)
    if condition=="genealogy_blinded":new["genealogy"]=0.
    return new,update,"micro_group→macro_activations"


def run(condition="coupled",mode="isosceles",seed=0,budget=18):
    if condition not in CONDITIONS or mode not in MODES:raise ValueError("Invalid ablation")
    if budget<1: raise ValueError("budget must be positive")
    graph=build_material(mode)
    packets=co_generations(graph)
    before=make_graph("scalene" if mode=="ordinary_cevian" else mode,include_bridge=False)
    act=activation_init(condition)
    trace=[{"tick":0,"operation":"CONSTRUCT_TRANSVERSAL","new_group":None,
            "macro_before":act.copy(),"macro_after":act.copy(),
            "event":"construction creates multiple readings",
            "co_generated_packets":packets,
            "material_delta":{"new_objects":len(graph["nodes"])-len(before["nodes"]),
                              "new_relations":len(graph["edges"])-len(before["edges"])},
            "epistemic_status":"material_event_only; angle equality only if separately given"}]
    selected={};done=set();hypotheses=[];generic_spaces=[]
    for t in range(1,budget+1):
        frontier=graph_proposals(graph,selected,done)
        frontier.update(packet_groups(graph,packets,selected,done))
        if not frontier:break
        # Every condition sees exactly the same mathematical graph and
        # candidate grammar. Only conceptual activation and genealogy differ.
        scores={key:score(graph,g,act,condition,packets[0] if packets else None)
                for key,g in frontier.items()}
        temperature=round(max(.43,.71-.010*t),3)
        key=select_softmax(frontier,scores,random.Random((seed+1)*104729+t),temperature)
        g=frontier[key]
        chosen_score,bias,sources=scores[key]
        macro_before=act.copy()
        selected[key]=g
        done.add(key)
        new_generic=None;hypothesis=None
        if g["operator"] in ("REBASE","ALIGN"):
            # Generic induction by *instantiated* structural matching.
            if len(g["relations"])>=2:
                opposites=[eid for eid in g["relations"] if graph["edges"][eid]["kind"]=="opposite"]
                if len(opposites)>=2:
                    new_generic={
                        "id":"GS:"+":".join(sorted(g["operator"] for _ in (0,)))+":"+g["id"][2:],
                        "kind":"paired_opposition_role_mapping",
                        "carrier":g.get("mediator"),
                        "source_event":g.get("provenance_event"),
                        "relations":opposites,
                        "epistemic_status":"structural_candidate_not_metric_proof",
                        "parent_groups":g["parents"]}
                    generic_spaces.append(new_generic)
        if g["operator"]=="REBASE" and g["has_angular_equality"]:
            # Discover which segments the opposition edges actually target.
            opp=g["opposition_roles"]
            targets=sorted({o["side"] for o in opp})
            if len(targets)==2 and packets:
                hypothesis={"id":"H:"+g["id"],"source":"equal angular sectors from construction",
                            "destination":{"relation":"candidate_equal_segments",
                                           "objects":targets},
                            "through":[o["edge_id"] for o in opp],
                            "originating_group":g["parents"],
                            "medial_term":g["mediator"],
                            "direction":"angular_equality→segment_equality?",
                            "epistemic_status":"HYPOTHESIS_ONLY",
                            "licensed_by_theorem":False}
                hypotheses.append(hypothesis)
        act,feedback,reverse=update_activation(act,g,condition,packets[0] if packets else None)
        trace.append({"tick":t,"operation":g["operator"],"new_group":g,
                      "new_generic":new_generic,"new_analogical_hypothesis":hypothesis,
                      "frontier_size":len(frontier),"score":chosen_score,
                      "macro_inherited":bias,"score_sources":sources,
                      "temperature":temperature,"macro_before":macro_before,
                      "macro_after":act.copy(),"feedback_delta":feedback,
                      "cause":["material_relations",
                               "coorigin→group" if sources.get("construction_genealogy",0)>0 else
                               "macro→group" if bias>0 else "bottom_up",
                               g["id"],reverse or "no_reverse_feedback"],
                      "epistemic_status":"hypothesis_only" if hypothesis else "structural_candidate",
                      "certified_metric_equalities":[]})
    coframe=[x for x in selected.values() if x["operator"]=="COFRAME"]
    rebase=[x for x in selected.values() if x["operator"]=="REBASE"]
    return {"condition":condition,"mode":mode,"seed":seed,"budget":budget,
            "geometry":graph["geometry"],
            "construction_packets":packets,
            "graph":{"nodes":graph["nodes"],"edges":graph["edges"]},
            "timeline":trace,"analogical_hypotheses":hypotheses,
            "induced_generic_spaces":generic_spaces,
            "metrics":{
                "cogeneration_detected":len(packets),
                "coframe_found":bool(coframe),
                "rebasing_found":bool(rebase),
                "transfer_question_found":bool(hypotheses),
                "coframe_tick":next((x["tick"] for x in trace if x["operation"]=="COFRAME"),None),
                "transfer_tick":next((x["tick"] for x in trace if x.get("new_analogical_hypothesis")),None),
                "cross_domain_selected":sum(x["cross_domain"] for x in selected.values()),
                "induced_generic_spaces":len(generic_spaces),
                "feedback_events":sum(bool(x.get("feedback_delta")) for x in trace),
                "coorigin_influenced_selected":sum(
                    x.get("score_sources",{}).get("construction_genealogy",0)>0 for x in trace),
                "false_metric_certifications":0}}


def experiment(seeds=range(32),budget=18):
    runs=[run(cond,mode,seed,budget) for mode in MODES for cond in CONDITIONS for seed in seeds]
    result={}
    for mode in MODES:
        result[mode]={}
        for cond in CONDITIONS:
            arr=[r for r in runs if r["mode"]==mode and r["condition"]==cond]
            metric=lambda key:mean(r["metrics"][key] for r in arr)
            result[mode][cond]={
                "n":len(arr),
                "cogeneration_detected_rate":round(metric("cogeneration_detected"),4),
                "coframe_rate":round(metric("coframe_found"),4),
                "rebasing_rate":round(metric("rebasing_found"),4),
                "transfer_question_rate":round(metric("transfer_question_found"),4),
                "mean_cross_domain_groups":round(metric("cross_domain_selected"),4),
                "mean_generic_spaces":round(metric("induced_generic_spaces"),4),
                "first_coframe_tick_if_found":(
                    round(mean(r["metrics"]["coframe_tick"] for r in arr
                               if r["metrics"]["coframe_tick"] is not None),3)
                    if any(r["metrics"]["coframe_found"] for r in arr) else None),
                "false_metric_certifications":sum(r["metrics"]["false_metric_certifications"] for r in arr)}
    return {"schema":"merovingio.co_generated_gestalten.v3","conditions":CONDITIONS,
            "modes":MODES,"seeds":list(seeds),"budget":budget,
            "source":{"parent_experiment":"gestalt_heat_v2",
                      "memory_contract":fixture_contract()},
            "epistemic_note":"Seeded engineered cognitive simulation, not psychometry, Euclid's discovery history, or a theorem prover.",
            "no_jev":True,"no_proof":True,
            "aggregates":result,"runs":runs}


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--seeds",type=int,default=32)
    p.add_argument("--budget",type=int,default=18)
    p.add_argument("--output",default=str(HERE/"results"))
    a=p.parse_args()
    out=Path(a.output)
    out.mkdir(parents=True,exist_ok=True)
    r=experiment(range(a.seeds),a.budget)
    (out/"traces.json").write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding="utf-8")
    (out/"aggregates.json").write_text(json.dumps(r["aggregates"],ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(r["aggregates"],indent=2))
    print("Saved",out/"traces.json")

if __name__=="__main__":
    main()

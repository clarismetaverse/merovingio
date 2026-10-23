#!/usr/bin/env python3
"""Emergent Gestalt grouping from a geometric incidence/role graph.

v2 differs from v1: no named list of target Gestalten/codelets. Search proposals
are compiled at runtime from relation edges, expansions and motif alignments.
The graph grammar and scoring priors are still manually engineered. Neither
structural analogy nor coordinate equality licenses a mathematical theorem.
"""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
import math
import random
from collections import defaultdict
from pathlib import Path
from statistics import mean

import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent / "gestalt_heat_v1"))
from engine import geometry, fixture_contract
CONDITIONS=("bottom_up","feedforward","reciprocal","reciprocal_without_opposition")
MODES=("isosceles","scalene")
MACROS=("angles","sides","opposition","partition","shared")
INIT={"angles":0.64,"sides":0.64,"opposition":0.84,"partition":0.55,"shared":0.35}


def stable_noise(s: str) -> float:
    return int(hashlib.sha256(s.encode("utf-8")).hexdigest()[:8],16)/0xffffffff


def side(u,v):
    return "S:"+"".join(sorted((u,v)))


def angle(u,v,w):
    return "A:"+min(u,w)+v+max(u,w)


def tri(vertices):
    return "T:"+"".join(sorted(vertices))


def make_graph(mode: str, include_bridge=True):
    """Create objects and relations from segment incidence and triangle cycles.

    Oppositions are derived from opposite vertex in each recovered triangular
    3-cycle, not manually listed angle/side pairs.
    """
    geom=geometry(mode)
    coords=geom["points"]
    segments=[("A","B"),("A","C"),("B","C")]
    if include_bridge:
        segments += [("A","D"),("D","B"),("C","D")]
    nodes={}
    edges={}
    def node(key,kind,**kw):
        nodes[key]={"id":key,"kind":kind,**kw}
    def edge(kind,a,b,origin,**kw):
        if a==b: return
        eid="E:"+kind+":"+":".join(sorted((a,b)))
        if eid not in edges:
            edges[eid]={"id":eid,"kind":kind,"nodes":sorted([a,b]),
                        "origin":origin,"epistemic_status":"structural",**kw}
    for p in ("A","B","C","D") if include_bridge else ("A","B","C"):
        node("P:"+p,"point",label=p)
    for u,v in segments:
        s=side(u,v)
        node(s,"side",label=u+v,vertices=[u,v])
        edge("endpoint","P:"+u,s,"material_incidence")
        edge("endpoint","P:"+v,s,"material_incidence")
    possible=sorted(set(itertools.chain.from_iterable(segments)))
    found_triangles=[]
    for vs in itertools.combinations(possible,3):
        if all(side(u,v) in nodes for u,v in itertools.combinations(vs,2)):
            p,q,r=(coords[x] for x in vs)
            area=abs((q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0]))
            if area<1e-7: continue
            t=tri(vs)
            node(t,"region",label="".join(vs),vertices=list(vs))
            found_triangles.append((t,vs))
            for u,v in itertools.combinations(vs,2):
                edge("boundary",t,side(u,v),"triangular_3_cycle")
            for pivot in vs:
                outside=sorted(x for x in vs if x!=pivot)
                a=angle(outside[0],pivot,outside[1])
                node(a,"angle",label="∠"+outside[0]+pivot+outside[1],
                     vertex=pivot,arms=outside)
                edge("angle_in_region",a,t,"triangular_3_cycle")
                edge("opposite",a,side(*outside),"opposite_vertex_in_triangle",
                     triangle=t)
                for end in outside:
                    edge("bounds_angle",a,side(pivot,end),"angle_ray_incidence")
    if include_bridge:
        # These partition facts arise from given construction + contact.
        edge("part_of",side("A","D"),side("A","B"),"D_between_A_B")
        edge("part_of",side("B","D"),side("A","B"),"D_between_A_B")
        aa=angle("A","C","D");ab=angle("B","C","D")
        full=angle("A","C","B")
        edge("part_of",aa,full,"CD_inside_angle_ACB")
        edge("part_of",ab,full,"CD_inside_angle_ACB")
        edge("equal_given",aa,ab,"CD_is_constructed_angle_bisector",
             epistemic_status="construction_given")
        for (t1,v1),(t2,v2) in itertools.combinations(found_triangles,2):
            shared=set(side(*v) for v in itertools.combinations(v1,2)) & set(
                side(*v) for v in itertools.combinations(v2,2))
            for s in shared:
                edge("share_material_side",t1,t2,"common_material_segment",carrier=s)
    return {"geometry":geom,"nodes":nodes,"edges":edges,"triangles":[t for t,_ in found_triangles],
            "given_equal_angles": [angle("A","C","D"),angle("B","C","D")] if include_bridge else [],
            "certified_metric_equalities": []}


def relation_signature(graph, eid):
    e=graph["edges"][eid]
    x,y=e["nodes"]
    return (e["kind"], *sorted((graph["nodes"][x]["kind"],graph["nodes"][y]["kind"])))


def group_from_edges(graph, eids, operator, parents=()):
    nodes=sorted(set(n for eid in eids for n in graph["edges"][eid]["nodes"]))
    kinds={graph["nodes"][n]["kind"] for n in nodes}
    rels=[graph["edges"][eid]["kind"] for eid in eids]
    key="G:"+hashlib.sha256(("|".join(sorted(eids))+":"+operator).encode()).hexdigest()[:12]
    cross="angle" in kinds and "side" in kinds
    opp=sum(r=="opposite" for r in rels)
    return {"id":key,"operator":operator,"relations":sorted(eids),"objects":nodes,
            "kinds":sorted(kinds),"relation_types":sorted(rels),"parents":list(parents),
            "cross_domain":cross,"oppositions":opp,
            "epistemic_status":"candidate_structural_group",
            "genealogy":["material_graph"]+list(parents)}


def equal_angle_witness(graph, g):
    equal=graph["given_equal_angles"]
    if len(equal)!=2: return False
    endpoints=[graph["edges"][eid] for eid in g["relations"]
               if graph["edges"][eid]["kind"]=="opposite"]
    if len(endpoints)<2: return False
    pairs=[]
    for e in endpoints:
        angle_ids=[n for n in e["nodes"] if graph["nodes"][n]["kind"]=="angle"]
        side_ids=[n for n in e["nodes"] if graph["nodes"][n]["kind"]=="side"]
        if angle_ids and side_ids: pairs.append((angle_ids[0],side_ids[0]))
    return all(any(a==x for a,s in pairs) for x in equal) and len({s for a,s in pairs if a in equal})==2


def proposals(graph, selected, generated):
    """Generate new GROUPS by the graph grammar rather than a target group list."""
    available={}
    def add(g):
        if g["id"] not in generated:available[g["id"]]=g
    # SEED: any grounded binary relation can become a group.
    for eid in graph["edges"]:
        add(group_from_edges(graph,(eid,),"SEED"))
    adjacency=defaultdict(set)
    for eid,e in graph["edges"].items():
        for n in e["nodes"]: adjacency[n].add(eid)
    # EXTEND: attach any incident relation to an actually selected group.
    for chosen in selected.values():
        if chosen["operator"]=="ALIGN": continue
        if len(chosen["objects"])>=5 or len(chosen["relations"])>=4:continue
        new_edges=set()
        for node_id in chosen["objects"]:
            new_edges.update(adjacency[node_id])
        for eid in sorted(new_edges-set(chosen["relations"])):
            eids=tuple(sorted(set(chosen["relations"])|{eid}))
            g=group_from_edges(graph,eids,"EXTEND",(chosen["id"],))
            if len(g["objects"])<=5:add(g)
    # ALIGN: once a relation is perceived, its generic relational motif can be
    # applied to all independently graph-derived peers of the same signature.
    # This code DOES NOT enumerate which opposite-angle pairs should match.
    seen=set()
    for chosen in selected.values():
        if len(chosen["relations"])!=1:continue
        first=chosen["relations"][0]
        sign=relation_signature(graph,first)
        for second in graph["edges"]:
            if second==first or relation_signature(graph,second)!=sign:continue
            pair=tuple(sorted((first,second)))
            if pair in seen:continue
            seen.add(pair)
            # Ignore trivial self-alignment on the exact same material instance.
            if set(graph["edges"][first]["nodes"])==set(graph["edges"][second]["nodes"]):continue
            g=group_from_edges(graph,pair,"ALIGN",(chosen["id"],))
            add(g)
    return available


def inherited_score(graph, group, activation):
    if not activation:return 0., {}
    kinds=set(group["kinds"])
    rels=set(group["relation_types"])
    sources={}
    if "angle" in kinds: sources["angles"]=0.19*activation["angles"]
    if "side" in kinds: sources["sides"]=0.19*activation["sides"]
    if "opposite" in rels and {"angle","side"}<=kinds:
        sources["opposition"]=1.55*activation["opposition"]
    if "part_of" in rels:sources["partition"]=0.43*activation["partition"]
    if "share_material_side" in rels:sources["shared"]=0.38*activation["shared"]
    if group["operator"]=="ALIGN" and group["cross_domain"]:
        sources["analogy_binding"]=0.22*(activation["angles"]+activation["sides"])
    return sum(sources.values()),{k:round(v,5) for k,v in sources.items()}


def candidate_score(graph,group,activation):
    base={"SEED":0.38,"EXTEND":0.38,"ALIGN":0.49}[group["operator"]]
    bonus=min(len(group["objects"]),5)*0.028
    bonus+=min(len(group["relations"]),4)*0.038
    if group["operator"]=="ALIGN" and equal_angle_witness(graph,group):
        # A structural equality witness from the graph *guides attention*;
        # it does not justify equality of the two opposite sides.
        bonus+=0.45
    macro,sources=inherited_score(graph,group,activation)
    # Stable low-amplitude geometric diversity prevents lexical-order shortcuts.
    jitter=0.075*(stable_noise(group["id"])-.5)
    return round(base+bonus+macro+jitter,6),round(macro,6),sources


def select_softmax(frontier, scores, rng, temperature=0.48):
    # Gumbel-max: sampling without depending on generator iteration order.
    winner=None;maxvalue=-1e100
    for k in sorted(frontier):
        u=max(1e-12,min(1-1e-12,rng.random()))
        gumbel=-math.log(-math.log(u))
        v=scores[k][0]/temperature+gumbel
        if v>maxvalue:
            winner,maxvalue=k,v
    return winner


def feedback(activation,group):
    new=activation.copy()
    evidence={}
    for kind,macro in (("angle","angles"),("side","sides")):
        if kind in group["kinds"]:
            evidence[macro]=0.065
    if "opposite" in group["relation_types"] and group["cross_domain"]:
        evidence["opposition"]=0.13
    if "part_of" in group["relation_types"]:evidence["partition"]=0.075
    if "share_material_side" in group["relation_types"]:evidence["shared"]=0.080
    if group["operator"]=="ALIGN" and group["cross_domain"]:
        evidence["opposition"]=evidence.get("opposition",0)+0.07
    for k in MACROS:
        new[k]=round(min(1.,new[k]*.988+evidence.get(k,0)),6)
    return new,evidence


def run(condition="reciprocal",mode="isosceles",seed=0,budget=16):
    if condition not in CONDITIONS or mode not in MODES:raise ValueError("Unknown condition/mode")
    if budget<1: raise ValueError("Budget must be positive")
    graph=make_graph(mode)
    act={k:0. for k in MACROS} if condition=="bottom_up" else INIT.copy()
    if condition=="reciprocal_without_opposition":act["opposition"]=0.
    before_graph=make_graph(mode,include_bridge=False)
    timeline=[{"tick":0,"operation":"CONSTRUCT_CD","activation_before":act.copy(),
               "activation_after":act.copy(),"top_down_heritage":{},
               "groups_now":[],"generated_candidates":0,
               "material_delta":{"nodes":len(graph["nodes"])-len(before_graph["nodes"]),
                                 "relations":len(graph["edges"])-len(before_graph["edges"])},
               "epistemic_status":"constructed_angle_equality; no segment equality certified"}]
    selected={};generated=set();discovered_generics={};hypotheses=[];score_accum=0
    for tick in range(1,budget+1):
        frontier=proposals(graph,selected,generated)
        if not frontier:break
        scores={id:candidate_score(graph,g,act if condition!="bottom_up" else {}) for id,g in frontier.items()}
        chosen_id=select_softmax(frontier,scores,random.Random((seed+1)*1000003+tick),0.43)
        g=frontier[chosen_id]
        score,heritage,sources=scores[chosen_id]
        before=act.copy()
        generated.add(chosen_id)
        selected[chosen_id]=g
        # Generic Spaces are induced from two independently discovered relation
        # instances with the same relational signature; never listed by name.
        new_generic=None
        new_hypothesis=None
        if g["operator"]=="ALIGN":
            rs=[graph["edges"][e] for e in g["relations"]]
            if len(rs)==2 and relation_signature(graph,rs[0]["id"])==relation_signature(graph,rs[1]["id"]):
                new_generic={
                    "id":"GS:"+":".join(relation_signature(graph,rs[0]["id"])),
                    "relations":g["relations"],"objects":g["objects"],
                    "role_schema":list(relation_signature(graph,rs[0]["id"])),
                    "genealogy":g["genealogy"],
                    "metric_status":"not_certified",
                    "epistemic_status":"induced_structural_analogy"}
                discovered_generics.setdefault(new_generic["id"],[]).append(new_generic)
            if equal_angle_witness(graph,g):
                # Derive the missing segment relation from the graph pairing as a
                # directional analogical question, never certify it as equality.
                opposites=[graph["edges"][eid] for eid in g["relations"] if graph["edges"][eid]["kind"]=="opposite"]
                sides=sorted({n for e in opposites for n in e["nodes"] if graph["nodes"][n]["kind"]=="side"})
                new_hypothesis={"from_equal_angles":graph["given_equal_angles"],
                                "to_candidate_equal_sides":sides,
                                "path":g["relations"],"direction":"angle_to_side",
                                "epistemic_status":"HYPOTHESIS_ONLY",
                                "license":"none"}
                hypotheses.append(new_hypothesis)
        if condition=="reciprocal" or condition=="reciprocal_without_opposition":
            act,delta=feedback(act,g)
            if condition=="reciprocal_without_opposition":act["opposition"]=0.
        else:delta={}
        score_accum+=heritage
        timeline.append({"tick":tick,"operation":g["operator"],"codelet":"GRAPH_"+g["operator"],
                         "new_group":g, "new_generic":new_generic,"new_analogical_hypothesis":new_hypothesis,
                         "activation_before":before,"activation_after":act.copy(),"feedback":delta,
                         "score":score,"macro_inherited":heritage,"top_down_heritage":sources,
                         "temperature":0.43,"frontier_size":len(frontier),
                         "candidate_ids_sample":sorted(frontier)[:8],
                         "provenance_chain":["CONSTRUCT_CD","GRAPH_RELATIONS",g["operator"],
                                             "MACRO→MICRO" if heritage>0 else "BOTTOM_UP",
                                             "MICRO→MACRO" if delta else "NO_FEEDBACK"],
                         "epistemic_status":"hypothesis_only" if new_hypothesis else "structural_candidate",
                         "certified_metric_equalities":[]})
    motifs=[g for g in selected.values() if g["cross_domain"]]
    alignments=[g for g in selected.values() if g["operator"]=="ALIGN"]
    opposite_align=[g for g in alignments if "opposite" in g["relation_types"]]
    return {
        "condition":condition,"mode":mode,"seed":seed,"budget":budget,
        "graph":{"nodes":graph["nodes"],"edges":graph["edges"]},
        "material":graph["geometry"],"initial_macros":INIT,
        "timeline":timeline,
        "generic_spaces":discovered_generics,
        "analogical_hypotheses":hypotheses,
        "metrics":{
            "generated_group_count":len(selected),"cross_domain_count":len(motifs),
            "alignment_count":len(alignments),"opposition_alignment_count":len(opposite_align),
            "induced_generic_count":sum(len(a) for a in discovered_generics.values()),
            "angle_to_side_hypothesis_found":bool(hypotheses),
            "time_to_hypothesis":next((e["tick"] for e in timeline if e.get("new_analogical_hypothesis")),None),
            "macro_inheritance_total":round(score_accum,4),
            "feedback_events":sum(bool(e.get("feedback")) for e in timeline),
            "false_certified_metric_equalities":0,
            "runtime_relation_count":len(graph["edges"])
        }
    }


def experiment(seeds=range(32),budget=16):
    contract=fixture_contract()
    runs=[run(c,m,seed,budget) for m in MODES for c in CONDITIONS for seed in seeds]
    aggregate={}
    for mode in MODES:
        aggregate[mode]={}
        for condition in CONDITIONS:
            rr=[r for r in runs if r["mode"]==mode and r["condition"]==condition]
            aggregate[mode][condition]={
                "n":len(rr),
                "hypothesis_rate":round(mean(r["metrics"]["angle_to_side_hypothesis_found"] for r in rr),4),
                "mean_cross_domain_count":round(mean(r["metrics"]["cross_domain_count"] for r in rr),3),
                "mean_alignment_count":round(mean(r["metrics"]["alignment_count"] for r in rr),3),
                "mean_opposition_alignments":round(mean(r["metrics"]["opposition_alignment_count"] for r in rr),3),
                "mean_first_hypothesis_tick_if_found":(
                    round(mean(r["metrics"]["time_to_hypothesis"] for r in rr if r["metrics"]["time_to_hypothesis"] is not None),3)
                    if any(r["metrics"]["angle_to_side_hypothesis_found"] for r in rr) else None),
                "false_metric_assertions":sum(r["metrics"]["false_certified_metric_equalities"] for r in rr)
            }
    return {
        "schema":"merovingio.gestalt_endogenous_v2",
        "kind":"seeded_graph_grammar_simulation_not_human_cognition",
        "source":{"v1":"NMerovingio/experiments/gestalt_heat_v1",
                  "fixtures":contract,
                  "constraint":"Graph-generated groups; operator vocabulary and scores remain hand-designed"},
        "conditions":CONDITIONS,"modes":MODES,"seeds":list(seeds),"budget":budget,
        "no_proof":True,"no_llm_or_jev":True,
        "aggregate":aggregate,"runs":runs
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--seeds",type=int,default=32)
    p.add_argument("--budget",type=int,default=16)
    p.add_argument("--output",default=str(HERE/"results"))
    a=p.parse_args()
    output=Path(a.output);output.mkdir(parents=True,exist_ok=True)
    data=experiment(range(a.seeds),a.budget)
    (output/"traces.json").write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
    (output/"aggregate.json").write_text(json.dumps(data["aggregate"],ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(data["aggregate"],indent=2))
    print("Saved",output/"traces.json")

if __name__=="__main__":
    main()

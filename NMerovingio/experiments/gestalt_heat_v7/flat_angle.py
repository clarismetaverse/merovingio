#!/usr/bin/env python3
"""Merovingio v7: constructively grounded flat-angle / segment medial regrouping.

Generalizes v6's productivity-driven REBASE without using triangle opposition
relations at all: angle sectors and segment halves are both derived as binary
PART_OF families, optionally sharing a causal construction event and contact.

Important: no implicit angle equality, no segment equality, and vertical
opposition is structural, not a metric certificate.
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

HERE=Path(__file__).resolve().parent
SCENARIOS=("flat_ray","crossed_lines","independent_partitions")
CONDITIONS=("fixed_initial","topology_only","predictive_only",
            "productivity_feedback","genealogy_blind")
ATTENTION=("clean","competing")
# Freeze v6 numerical priors/productivity rewards. They have not been tuned to v7.
PRIOR={"angles":.72,"sides":.55,"opposition":.76,"coorigin":.82}
PARTIAL_GAIN=.19
COMPLETION_GAIN=1.08
MISSING_ROLE_FEEDBACK=.73
COORIGIN_BASE=.72
TEMPERATURE=.59


def pair_id(prefix,u,v):
    return prefix+":"+"".join(sorted((u,v)))


def generate_material(scenario):
    if scenario not in SCENARIOS:raise ValueError(scenario)
    # Event identity and geometry are recorded separately. Nothing in the
    # scoring function refers to the desired segment labels.
    points={
        "A":(60.,150.),"O":(180.,150.),"B":(300.,150.),"C":(230.,62.),
        "D":(130.,238.),"E":(385.,150.),"P":(465.,150.),"F":(545.,150.),
        "G":(350.,302.),"Q":(435.,302.),"H":(520.,302.),"I":(478.,233.),
        "J":(555.,302.),"R":(623.,302.),"K":(690.,302.),
    }
    nodes={};edges={};events={}
    def node(key,kind,**kw):
        if key in nodes:
            assert nodes[key]["kind"]==kind
            return
        nodes[key]={"id":key,"kind":kind,**kw}
    def edge(kind,u,v,event,**kw):
        assert u in nodes and v in nodes
        key="E:"+kind+":"+":".join(sorted((u,v)))
        if key not in edges:
            edges[key]={"id":key,"kind":kind,"nodes":sorted((u,v)),
                        "source_event":event,"epistemic_status":"material_structural",**kw}
        return key
    def point(p):
        node("P:"+p,"point",label=p,position=points[p])
    def ray(p,q,event):
        point(p);point(q)
        key="R:"+p+q
        node(key,"ray",label=p+"→"+q,root=p,target=q)
        edge("ray_endpoint","P:"+p,key,event)
        return key
    def seg(p,q,event):
        point(p);point(q)
        key=pair_id("S",p,q)
        node(key,"side",label=p+q,vertices=[p,q])
        for w in (p,q):edge("endpoint","P:"+w,key,event)
        return key
    def angle(p,v,q,event):
        ray(v,p,event);ray(v,q,event)
        key="A:"+p+v+q
        node(key,"angle",label="∠"+p+v+q,vertex=v,arms=[p,q])
        for x in (p,q):edge("bounds_angle",key,"R:"+v+x,event)
        return key
    def angle_split(l,v,r,t,event,root,phase,domain_label):
        # A ray inserted into a straight angle creates two sectors.
        events[event]={"id":event,"root":root,"phase":phase,"construction":"insert_or_extend_ray",
                       "medial_contact":v,"carrier":"R:"+v+t}
        full="FLAT:"+l+v+r+":"+domain_label
        node(full,"straight_angle",label="straight ∠"+l+v+r+" "+domain_label,
             vertex=v,arms=[l,r])
        a=angle(l,v,t,event);b=angle(t,v,r,event)
        for child in (a,b):
            edge("part_of",child,full,event,
                 child=child,parent=full,root_event=root,construction_phase=phase)
        return a,b
    def side_split(l,v,r,event,root,phase):
        events[event]={"id":event,"root":root,"phase":phase,"construction":"divide_segment",
                       "medial_contact":v,"carrier":"P:"+v}
        full=seg(l,r,event);a=seg(l,v,event);b=seg(v,r,event)
        for child in (a,b):
            edge("part_of",child,full,event,
                 child=child,parent=full,root_event=root,construction_phase=phase)
        return a,b
    # The baseline of O is initially a *line*, hence independent_partitions
    # does not clandestinely create AO/OB as a finite segment partition.
    events["EV:O:INCIDENCE"]={"id":"EV:O:INCIDENCE","root":"EV:O:INCIDENCE",
        "phase":"W1","construction":"ray_meets_supporting_line","medial_contact":"O","carrier":"R:OC"}
    angle_split("A","O","B","C","EV:O:UPPER","EV:O:INCIDENCE","W1","upper")
    if scenario in ("flat_ray","crossed_lines"):
        side_split("A","O","B","EV:O:SPLIT","EV:O:INCIDENCE","W1")
    if scenario=="crossed_lines":
        ray("O","D","EV:O:EXTENSION")
        # A new partition arises on extension; common causal ancestry does not
        # imply equal parts.
        lower=angle_split("B","O","A","D","EV:O:LOWER","EV:O:INCIDENCE","W2","lower")
        upper=[n for n in nodes if n.startswith("A:") and n in ("A:AOC","A:COB")]
        for u,v in (("A:AOC","A:BOD"),("A:COB","A:DOA")):
            if u in nodes and v in nodes:
                edge("vertical_opposite",u,v,"EV:O:EXTENSION",
                     epistemic_status="structural_opposition_not_equality")
    # Structural distractors with no common root. A full straight angle
    # partition at Q competes with the one born at O.
    angle_split("G","Q","H","I","EV:Q:RAY","EV:Q:RAY","W1","upper")
    side_split("E","P","F","EV:P:SPLIT","EV:P:SPLIT","W1")
    if scenario=="independent_partitions":
        # A second independent split helps keep a genuine choice in SIDE.
        side_split("J","R","K","EV:R:SPLIT","EV:R:SPLIT","W1")
    stages=["W0","W1"]+(["W2"] if scenario=="crossed_lines" else [])
    return {"scenario":scenario,"nodes":nodes,"edges":edges,"events":events,
            "geometry":{"points":points,"stages":stages},
            "given_metric_equalities":[],"certified_metric_equalities":[]}


def partition_families(graph):
    """Read binary partition schemas directly from oriented PART_OF graph edges."""
    buckets=defaultdict(list)
    for e in graph["edges"].values():
        if e["kind"]!="part_of":continue
        buckets[e["parent"]].append(e)
    families=[]
    for parent,rels in sorted(buckets.items()):
        if len(rels)!=2:continue
        a,b=rels
        children=sorted((a["child"],b["child"]))
        kind=graph["nodes"][children[0]]["kind"]
        if kind!=graph["nodes"][children[1]]["kind"]:continue
        if kind not in ("angle","side"):continue
        if kind=="angle":
            if graph["nodes"][parent]["kind"]!="straight_angle":continue
            anchors={graph["nodes"][x]["vertex"] for x in children}
        else:
            if graph["nodes"][parent]["kind"]!="side":continue
            anchors=set(graph["nodes"][children[0]]["vertices"]) & set(
                graph["nodes"][children[1]]["vertices"])
        if len(anchors)!=1:continue
        family={
            "id":"G:"+hashlib.sha256("|".join(children).encode()).hexdigest()[:10],
            "kind":"ANGLE" if kind=="angle" else "SIDE",
            "parent":parent,"children":children,"anchor":next(iter(anchors)),
            "relation_ids":sorted((a["id"],b["id"])),
            "root_event":a["root_event"],
            "direct_event":a["source_event"],
            "phase":a["construction_phase"],
            "epistemic_status":"graph_generated_partition"}
        assert b["root_event"]==a["root_event"]
        families.append(family)
    return sorted(families,key=lambda x:x["id"])


def prospective_schemata(families):
    """Only a shared genealogical root + physical medial anchor licenses pairing."""
    results={}
    for a,b in itertools.combinations(families,2):
        if a["kind"]==b["kind"]:continue
        if a["root_event"]!=b["root_event"] or a["anchor"]!=b["anchor"]:continue
        key="GS:"+hashlib.sha256("|".join(sorted((a["id"],b["id"]))).encode()).hexdigest()[:10]
        results[key]={"id":key,"slots":sorted((a["id"],b["id"])),
                     "anchor":a["anchor"],"root_event":a["root_event"],
                     "relation":"paired_partitions_different_domains",
                     "epistemic_status":"prospective_structural_template"}
    return results


def graph_neighbors(families):
    """Alternative purely topological accessibility from shared objects/anchor."""
    nb={}
    for a in families:
        for b in families:
            if a["id"]==b["id"]:continue
            same_anchor=a["anchor"]==b["anchor"]
            object_overlap=bool(set(a["children"])&set(b["children"]))
            # No implicit correspondence between independent split events:
            # topological grouping sees material contact, not causal ancestry.
            nb[(a["id"],b["id"])]=.17*same_anchor+.28*object_overlap
    return nb


def case_initial_focus(families):
    # The W1 ray construction creates an angle partition in the primary
    # workspace. Choose through event/phase, not inferred metric goal.
    options=[f for f in families if f["kind"]=="ANGLE" and
             f["phase"]=="W1" and f["anchor"]=="O"]
    assert len(options)==1
    return options[0]


def anticipated(candidate,selected,templates):
    records=[]
    for schema in templates.values():
        if candidate["id"] not in schema["slots"]:continue
        occupied=set(schema["slots"]) & selected
        if not occupied:
            records.append({"generic":schema["id"],"kind":"partial",
                            "gain":PARTIAL_GAIN})
        elif len(occupied)==1:
            records.append({"generic":schema["id"],"kind":"complete",
                            "gain":COMPLETION_GAIN})
    return records


def activated_macro(condition):
    result=PRIOR.copy()
    if condition=="genealogy_blind":result["coorigin"]=0.
    if condition=="topology_only":result={k:0. for k in PRIOR}
    return result


def candidate_scores(families,selected,focus,active,macro,templates,
                     reward,condition,neighbors):
    out={}
    target="SIDE" if focus=="ANGLE" else "ANGLE"
    for c in families:
        if c["id"] in selected or c["kind"]!=target:continue
        # v6 coefficients .95 local, .32 secondary, .30 opposition and .25
        # domain macro; no response-specific answer reward.
        adjacency=max((neighbors[(x,c["id"])] for x in selected),default=0.)
        local=.95*active[c["id"]]+.32*adjacency
        topological=.16+local+.30*macro["opposition"]+.25*macro[
            "angles" if c["kind"]=="ANGLE" else "sides"]
        paired=anticipated(c,selected,templates)
        genealogy=COORIGIN_BASE*macro["coorigin"] if paired else 0.
        if condition in ("genealogy_blind","topology_only"):genealogy=0.
        predictive=sum(x["gain"] for x in paired) if condition in (
            "predictive_only","productivity_feedback","genealogy_blind") else 0.
        if condition=="genealogy_blind":predictive*=.42
        feedback=reward.get(c["id"],0.) if condition=="productivity_feedback" else 0.
        if condition=="genealogy_blind":feedback=reward.get(c["id"],0.)*.42
        out[c["id"]]={
            "id":c["id"],
            "score":round(topological+genealogy+predictive+feedback,6),
            "topological":round(topological,6),
            "genealogy":round(genealogy,6),
            "prospective":round(predictive,6),
            "feedback":round(feedback,6),
            "anticipated":paired}
    return out


def update_structural_activation(selected_family,active,families,neighbors):
    new={x:round(v*.955,6) for x,v in active.items()}
    for c in families:
        if c["id"]==selected_family["id"]:
            new[c["id"]]=round(min(1.,new[c["id"]]+.30),6)
        else:
            link=neighbors[(selected_family["id"],c["id"])]
            new[c["id"]]=round(min(1.,new[c["id"]]+.23*link),6)
    return new


def choose(scores,seed,tick,condition,fixed_order):
    if condition=="fixed_initial":
        return next(i for i in fixed_order if i in scores)
    r=random.Random(seed*1000003+tick*7919)
    best=None;greatest=-1e30
    for key in sorted(scores):
        u=min(1.-1e-12,max(1e-12,r.random()))
        value=scores[key]["score"]/TEMPERATURE-math.log(-math.log(u))
        if value>greatest:best,greatest=key,value
    return best


def new_generic_events(selected,templates,memory):
    proposed=[]
    for s in templates.values():
        bound=sorted(set(s["slots"]) & selected)
        key=s["id"]+":"+str(len(bound))
        if not bound or key in memory:continue
        event={"id":key,"template":s["id"],"kind":
               "COMPLETED_GENERIC" if len(bound)==2 else "INCOMPLETE_GENERIC",
               "root_event":s["root_event"],"anchor":s["anchor"],
               "acquired_roles":bound,
               "missing_roles":sorted(set(s["slots"])-set(bound)),
               "epistemic_status":"structural_mapping_not_metric_proof"}
        proposed.append(event)
    return proposed


def productivity_feedback(events,templates,reward,macro,condition):
    out={k:round(v*.94,6) for k,v in reward.items()}
    newmacro=macro.copy()
    caused=[]
    if condition not in ("productivity_feedback","genealogy_blind"):
        return out,newmacro,caused
    for event in events:
        if event["kind"]=="INCOMPLETE_GENERIC":
            for role in event["missing_roles"]:
                gain=MISSING_ROLE_FEEDBACK if condition=="productivity_feedback" else .25
                out[role]=round(out.get(role,0.)+gain,6)
                caused.append({"source":event["id"],"target":role,"gain":gain,
                               "kind":"new_generic_primes_missing_role"})
        if event["kind"]=="COMPLETED_GENERIC":
            gain=.19 if condition=="productivity_feedback" else .08
            newmacro["opposition"]=round(min(1.,newmacro["opposition"]+gain),6)
            if condition=="productivity_feedback":
                newmacro["coorigin"]=round(min(1.,newmacro["coorigin"]+.08),6)
            caused.append({"source":event["id"],"target":"macro.opposition",
                           "gain":gain,"kind":"completion_primes_new_reading"})
    return out,newmacro,caused


def simulate(condition="productivity_feedback",scenario="flat_ray",seed=0,
             budget=3,attention="competing"):
    if condition not in CONDITIONS or scenario not in SCENARIOS or attention not in ATTENTION:
        raise ValueError("Unknown experimental condition")
    g=generate_material(scenario)
    families=partition_families(g)
    mapping={f["id"]:f for f in families}
    templates=prospective_schemata(families)
    neighbors=graph_neighbors(families)
    initial=case_initial_focus(families)
    selected={initial["id"]}
    memory={}
    macro=activated_macro(condition)
    activation={f["id"]:.10 for f in families}
    activation[initial["id"]]=.87
    if attention=="competing":
        # Prime unrelated SIDE families based on *different event*, not label.
        for f in families:
            if f["kind"]=="SIDE" and f["root_event"]!=initial["root_event"]:
                activation[f["id"]]=1.
    reward={}
    start_events=new_generic_events(selected,templates,memory)
    for e in start_events:memory[e["id"]]=e
    # Initial observation is an actual cognitive grouping; its feedback can
    # prime the missing SIDE slot before the first REBASE.
    reward,macro,first_causes=productivity_feedback(start_events,templates,reward,
                                                    macro,condition)
    # A static baseline has a frozen initial order PER DOMAIN.
    # It must remain valid when focus returns to ANGLE after a SIDE step.
    fixed_order={}
    for domain in ("ANGLE","SIDE"):
        initial_scores=candidate_scores(
            families,set(),"SIDE" if domain=="ANGLE" else "ANGLE",
            activation,macro,templates,{},"fixed_initial",neighbors)
        fixed_order[domain]=sorted(initial_scores,
            key=lambda k:(-initial_scores[k]["score"],k))
    timeline=[{"tick":0,"operation":"CONSTRUCT_AND_SEED_ANGLE",
               "focus":"ANGLE","selected_family":initial,
               "new_generic_events":start_events,"feedback_causes":first_causes,
               "current_activation":activation.copy(),"macro_after":macro.copy(),
               "epistemic_status":"structural_partition_not_metric_proof"}]
    focus="ANGLE"
    for tick in range(1,budget+1):
        scores=candidate_scores(families,selected,focus,activation,macro,
                                templates,reward,condition,neighbors)
        if not scores:break
        chosen=choose(scores,seed,tick,condition,
                      fixed_order["SIDE" if focus=="ANGLE" else "ANGLE"])
        f=mapping[chosen]
        before_act=activation.copy()
        before_macro=macro.copy()
        selected.add(chosen)
        events=new_generic_events(selected,templates,memory)
        for event in events:memory[event["id"]]=event
        if condition!="fixed_initial":
            activation=update_structural_activation(f,activation,families,neighbors)
        reward,macro,causes=productivity_feedback(events,templates,reward,macro,condition)
        candidate_next=candidate_scores(families,selected,f["kind"],activation,
                                        macro,templates,reward,condition,neighbors)
        counterfactual=candidate_scores(families,selected,f["kind"],before_act,
                                        before_macro,templates,{},condition,neighbors)
        old_rank=sorted(counterfactual,key=lambda k:(-counterfactual[k]["score"],k))
        new_rank=sorted(candidate_next,key=lambda k:(-candidate_next[k]["score"],k))
        timeline.append({"tick":tick,"operation":"REBASE_PARTITION",
            "from":focus,"to":f["kind"],"selected_family":f,
            "score_at_choice":scores[chosen],"available_scores":scores,
            "new_generic_events":events,"feedback_causes":causes,
            "ranking_before_new_group":old_rank,"ranking_after_new_group":new_rank,
            "relative_ranking_changed":old_rank!=new_rank,
            "current_activation":activation.copy(),"macro_after":macro.copy(),
            "acquired_families":sorted(selected),"certified_metric_equalities":[],
            "epistemic_status":"structural_generic_not_metric_proof"})
        focus=f["kind"]
    all_events=list(memory.values())
    complete=[e for e in all_events if e["kind"]=="COMPLETED_GENERIC"]
    return {"scenario":scenario,"condition":condition,"seed":seed,"attention":attention,
        "geometry":g["geometry"],"nodes":g["nodes"],"edges":g["edges"],
        "events":g["events"],"families":families,
        "templates":list(templates.values()),
        "timeline":timeline,"generic_spaces":all_events,
        "metrics":{
            "medial_generic_complete":bool(complete),
            "completed_count":len(complete),
            "partial_count":sum(x["kind"]=="INCOMPLETE_GENERIC" for x in all_events),
            "first_completion_tick":next((e["tick"] for e in timeline if any(
                x["kind"]=="COMPLETED_GENERIC" for x in e["new_generic_events"])),None),
            "feedback_causes":sum(len(e.get("feedback_causes",[])) for e in timeline),
            "reorderings":sum(e.get("relative_ranking_changed",False) for e in timeline),
            "selected_rebases":len(timeline)-1,
            "false_metric_certifications":0,
            "false_genealogy_pairings":sum(
                mapping[x["acquired_roles"][0]]["root_event"]!=
                mapping[x["acquired_roles"][1]]["root_event"] for x in complete)
        }}


def experiment(seeds=range(32),budget=3):
    runs=[simulate(c,s,seed,budget,a) for a in ATTENTION for s in SCENARIOS
          for c in CONDITIONS for seed in seeds]
    agg={}
    for a in ATTENTION:
        agg[a]={}
        for s in SCENARIOS:
            agg[a][s]={}
            for c in CONDITIONS:
                rr=[r for r in runs if r["attention"]==a and
                    r["scenario"]==s and r["condition"]==c]
                metric=lambda key:mean(r["metrics"][key] for r in rr)
                agg[a][s][c]={
                    "n":len(rr),
                    "completion_rate":round(metric("medial_generic_complete"),4),
                    "mean_completed_generic":round(metric("completed_count"),3),
                    "first_completion_tick_if_found":(
                        round(mean(r["metrics"]["first_completion_tick"] for r in rr
                                   if r["metrics"]["first_completion_tick"] is not None),3)
                        if any(r["metrics"]["medial_generic_complete"] for r in rr) else None),
                    "mean_feedback_events":round(metric("feedback_causes"),3),
                    "mean_reorderings":round(metric("reorderings"),3),
                    "false_metric_certifications":sum(r["metrics"]["false_metric_certifications"] for r in rr),
                    "false_genealogy_pairings":sum(r["metrics"]["false_genealogy_pairings"] for r in rr)}
    return {"schema":"merovingio.flat_angle_medial_regrouping.v7",
            "kind":"engineered_relational_analogy_simulation_not_proof",
            "conditions":CONDITIONS,"scenarios":SCENARIOS,"attentions":ATTENTION,
            "seeds":list(seeds),"budget":budget,
            "no_jev":True,"no_proof":True,"parameters_frozen_from_v6":True,
            "aggregates":agg,"runs":runs}


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--seeds",type=int,default=32)
    p.add_argument("--budget",type=int,default=3)
    p.add_argument("--output",default=str(HERE/"results"))
    a=p.parse_args()
    out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
    data=experiment(range(a.seeds),a.budget)
    (out/"traces.json").write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding="utf-8")
    (out/"aggregates.json").write_text(json.dumps(data["aggregates"],indent=2,ensure_ascii=False),encoding="utf-8")
    print(json.dumps(data["aggregates"],indent=2))
    print("Wrote",out/"traces.json")


if __name__=="__main__":main()

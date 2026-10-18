"""Order-sensitive support binding with identical frame multisets."""
from __future__ import annotations
import argparse,base64,hashlib,html,importlib.util,itertools,json,math,os,random
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
from PIL import Image,ImageDraw

SPEC=importlib.util.spec_from_file_location("order_ablation",Path(__file__).parents[1]/"temporal_genealogy_order/benchmark_order.py")
previous=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(previous)
pilot=previous.pilot
TRANSFORMS=previous.TRANSFORMS
REPEATS=2
SEED=20261020
CONDITIONS=("ordered_images","reverse_images","unordered_images","single_event","final_only","ordered_spaces","spaces_only")
IDENTIFIABLE=frozenset(("ordered_images","reverse_images","ordered_spaces","spaces_only"))
EVENTS=("idle","circle","vector","final")
TASK=("A session contains two activation events, one for each support family, exactly once. "
      "The first activation binds the initial-support role; the later activation supplies an independent secondary support. "
      "All scaffold objects are already drawn and remain present. Magenta/darker accent strokes indicate the currently active support; "
      "the final dark triangle only indicates selection. Use the declared ordering convention; a single event without its temporal position, "
      "an unordered collection, or the final state cannot establish which family was first. Infer only from supplied evidence.")
QUESTION="Which support family was activated before the other and thus bound to the initial-support role? Choose none if the supplied evidence does not identify a unique order. This is an order-of-support task, not a geometric proof."
DESCRIPTIONS={"circle":"The two-circle/common-radius support was activated before the equal-vector/translation support.","vector":"The equal-vector/translation support was activated before the two-circle/common-radius support.","none":"The supplied evidence does not identify which support family was activated first."}
LIMITS=[
 "SAME_FINAL_STATE != SAME_GENEALOGY. Both histories contain the exact same frames, differing only in middle-event order.",
 "This is a staged activation and role-binding session over a pre-drawn scaffold, not an ex-nihilo Euclidean construction.",
 "Initial support and later corroboration are protocol-defined roles; highlighting is supplied event evidence, not proof certification.",
 "Temporal labels and causal dependencies are not autonomously extracted. A correct answer may use simple ordered-list comparison.",
 "Structured conditions deliberately supply equivalent textual evidence and do not demonstrate autonomous visual grounding.",
 "Unordered, unpositioned single-event and final-only controls have no unique order target; accuracy is null.",
 "Eight transforms and two repetitions of two templates are dependent observations, not independent geometric problems.",
 "Multiple images and behavioral order sensitivity do not demonstrate internal sequential reasoning or geometric proof."]

def render(event,angle,reflection):
    assert event in EVENTS
    im=Image.new("RGB",(512,512),"white");d=ImageDraw.Draw(im)
    A,B,C=pilot.points(angle,reflection)
    D=(B[0]+C[0]-A[0],B[1]+C[1]-A[1])
    inactive="#B9C1CA";active="#A63570";dark="#26313D"
    def line(a,b,color,width=2):d.line((a,b),fill=color,width=width)
    def arrow(a,b,color,width=2):
        line(a,b,color,width);t=math.atan2(b[1]-a[1],b[0]-a[0])
        for delta in (-.45,.45):line(b,(b[0]-12*math.cos(t+delta),b[1]-12*math.sin(t+delta)),color,width)
    def circles(color,width):
        for x,y in (A,B):d.ellipse((x-160,y-160,x+160,y+160),outline=color,width=width)
    def vectors(color,width):
        for p,q in ((A,B),(A,C),(B,D),(C,D)):arrow(p,q,color,width)
        for P in (B,C):
            m=((A[0]+P[0])/2,(A[1]+P[1])/2);v=(P[0]-A[0],P[1]-A[1]);length=math.hypot(*v)
            line((m[0]-5*v[1]/length,m[1]+5*v[0]/length),(m[0]+5*v[1]/length,m[1]-5*v[0]/length),color,width)
        u=math.atan2(B[1]-A[1],B[0]-A[0]);v=math.atan2(C[1]-A[1],C[0]-A[0]);diff=(v-u+math.pi)%(2*math.pi)-math.pi
        d.line([(A[0]+24*math.cos(u+diff*i/20),A[1]+24*math.sin(u+diff*i/20)) for i in range(21)],fill=color,width=width)
    # Exactly the same primitives are present in every frame.
    circles(inactive,2);vectors(inactive,2)
    for p,q in ((A,B),(A,C),(B,C)):line(p,q,inactive,2)
    if event=="circle":circles(active,4)
    if event=="vector":vectors(active,4)
    if event=="final":
        for p,q in ((A,B),(A,C),(B,C)):line(p,q,dark,4)
    for x,y in (A,B,C,D):d.ellipse((x-3,y-3,x+3,y+3),fill=dark if event=="final" else inactive)
    return im

def timeline(history):
    return ("idle","circle","vector","final") if history=="circle" else ("idle","vector","circle","final")

def role_trace(events):
    # Observer-only role state machine. It never certifies geometric truths.
    origin=None;secondary=[];trace=[]
    carriers={"circle":"M_RADIUS_PACKET","vector":"M_TRANSLATION_PACKET"}
    seen=set()
    for event in events:
        change=[]
        if event in carriers:
            if event in seen:raise ValueError("Repeated support activation")
            seen.add(event)
            if origin is None:
                origin=event;role="initial_support"
            else:
                secondary.append(event);role="secondary_support"
            change=[{"carrier":carriers[event],"from":"available_scaffold","to":role}]
        trace.append({"event":event,"initial_support":origin,"secondary_supports":list(secondary),"triangle_selected":event=="final","role_changes":change})
    return trace

def manifest():
    trials=[]
    for transform,(angle,reflection) in enumerate(TRANSFORMS):
        for repeat in range(REPEATS):
            cell=transform*REPEATS+repeat
            for history in ("circle","vector"):
                for condition in CONDITIONS:
                    trials.append(dict(case=f"t{transform:02d}",angle=angle,reflection=reflection,repeat=repeat,history=history,condition=condition,option_seed=SEED+cell,single_event="circle" if cell%2==0 else "vector"))
    random.Random(SEED).shuffle(trials)
    return [dict(t,trial=i) for i,t in enumerate(trials)]

def presented_events(trial):
    c=trial["condition"]
    if c in ("ordered_images","ordered_spaces"):return timeline(trial["history"])
    if c=="reverse_images":return tuple(reversed(timeline(trial["history"])))
    if c=="unordered_images":
        values=list(EVENTS);random.Random(trial["option_seed"]+444).shuffle(values);return tuple(values)
    if c=="single_event":return (trial["single_event"],)
    if c=="final_only":return ("final",)
    return ()

def structures(history):
    # These records describe observations, never temporal rank or the correct answer.
    library={
     "idle":{"active_carriers":[],"triangle_role":"candidate"},
     "circle":{"active_carriers":[{"relation":"center to boundary at common distance","objects":["p","q","r"]}],"mental_spaces":["two equal-distance loci"],"generic_space":{"shared_role":"common radial carrier"}},
     "vector":{"active_carriers":[{"relation":"equal displacement norms at included angle pi/3","objects":["p","q","r"]}],"mental_spaces":["two translation generators and translated copies"],"generic_space":{"shared_role":"displacement-preserving carrier"}},
     "final":{"active_carriers":[],"triangle_role":"selected"}}
    return [library[event] for event in timeline(history)]

def build_payload(out,trial):
    rng=random.Random(trial["option_seed"])
    codes=["K"+str(n) for n in rng.sample(range(100000,999999),2)]
    mapping=dict(zip(codes,("circle","vector")))
    options=[(code,DESCRIPTIONS[h]) for code,h in mapping.items()]+[("none",DESCRIPTIONS["none"])];rng.shuffle(options)
    assets={};views=[];audit=[]
    for index,event in enumerate(presented_events(trial)):
        key=f"view{index+1}"
        path=out/"images"/f"{event}_{trial['angle']}_{trial['reflection']}.png"
        path.parent.mkdir(parents=True,exist_ok=True);render(event,trial["angle"],trial["reflection"]).save(path)
        data=path.read_bytes()
        assets[key]={"type":"image","format":"png","data_base64":base64.b64encode(data).decode("ascii")}
        views.append(key);audit.append({"asset":key,"event":event,"file":path.relative_to(out).as_posix(),"sha256":hashlib.sha256(data).hexdigest()})
    c=trial["condition"]
    direction="earliest to latest"
    if c=="reverse_images":direction="latest to earliest"
    if c=="unordered_images":direction="unordered collection; listed position has no temporal meaning"
    if c=="single_event":direction="one isolated activation; its temporal position is not supplied"
    if c=="final_only":direction="final state only; no activation order is supplied"
    state={"views":views,"ordering_convention":direction,"task":TASK}
    if c in ("ordered_spaces","spaces_only"):state["structural_observations"]=structures(trial["history"])
    payload={"model":"jev-1.14.0","state":state,"questions":{"origin":{"type":"choice","instructions":QUESTION,"criteria":dict(options)}}}
    if assets:payload["assets"]=assets
    return payload,mapping,audit

def summarize(records):
    result={}
    for c in CONDITIONS:
        rows=[r for r in records if r["condition"]==c];attempted=[r for r in rows if r["predicted"]!="not_run"]
        matrix={}
        for r in attempted:
            gold=r["history"] if c in IDENTIFIABLE else "non_identifiable"
            matrix.setdefault(gold,{})[r["predicted"]]=matrix.setdefault(gold,{}).get(r["predicted"],0)+1
        confidence=[r["response"]["answer"]["confidence"] for r in attempted if isinstance(r.get("response",{}).get("answer",{}).get("confidence"),(int,float))]
        result[c]={"planned_n":len(rows),"attempted_n":len(attempted),"failure_n":sum(r["predicted"]=="failure" for r in attempted),"order_accuracy":previous.mean([r["correct"] is True for r in attempted]) if c in IDENTIFIABLE else None,"none_rate":previous.mean([r["predicted"]=="none" for r in attempted]),"mean_confidence":previous.mean(confidence),"confidence_n":len(confidence),"confusion_matrix":matrix,"usage":{k:sum(((r.get("response",{}).get("usage") or {}).get(k) or 0) for r in attempted) for k in ("input_tokens","output_tokens")}}
    return result

def contrasts(records):
    result={};pairs={};cells={}
    for r in records:
        if r["predicted"]=="not_run":continue
        cells.setdefault((r["case"],r["repeat"],r["history"]),{})[r["condition"]]=r
        pairs.setdefault((r["case"],r["repeat"],r["condition"]),{})[r["history"]]=r
    for c in CONDITIONS:
        rows=[v for (case,repeat,condition),v in pairs.items() if condition==c and "circle" in v and "vector" in v]
        result[c]={"history_pairs":len(rows),"both_correct":sum(v["circle"]["correct"] is True and v["vector"]["correct"] is True for v in rows) if c in IDENTIFIABLE else None,"opposite_named_choices":sum({v["circle"]["predicted"],v["vector"]["predicted"]}=={"circle","vector"} for v in rows),"both_abstain":sum(v["circle"]["predicted"]==v["vector"]["predicted"]=="none" for v in rows),"failure_pairs":sum(any(r["predicted"]=="failure" for r in v.values()) for v in rows)}
    for left,right in (("ordered_images","reverse_images"),("ordered_spaces","ordered_images"),("ordered_spaces","spaces_only")):
        rows=[(v[left],v[right]) for v in cells.values() if left in v and right in v]
        result[left+"_vs_"+right]={"paired_n":len(rows),"both_correct":sum(a["correct"] is True and b["correct"] is True for a,b in rows),"left_only_correct":sum(a["correct"] is True and b["correct"] is not True for a,b in rows),"right_only_correct":sum(a["correct"] is not True and b["correct"] is True for a,b in rows),"neither_correct":sum(a["correct"] is not True and b["correct"] is not True for a,b in rows)}
    return result

def viewer(out,report):
    e=html.escape;table=[]
    for condition,r in report["by_condition"].items():
        accuracy="not identifiable" if r["order_accuracy"] is None else f"{r['order_accuracy']:.1%}"
        table.append(f"<tr><td>{condition}</td><td>{r['attempted_n']}/{r['planned_n']}</td><td>{accuracy}</td><td>{r['none_rate']}</td><td>{r['failure_n']}</td></tr>")
    examples=[]
    for angle,reflection in TRANSFORMS:
        part=[f"<details><summary>Rotation {angle}, reflection {reflection}</summary>"]
        for history in ("circle","vector"):
            part.append(f"<h3>{history} activated first</h3><div class=frames>"+"".join(f'<figure><img src="images/{event}_{angle}_{reflection}.png"><figcaption>{event}</figcaption></figure>' for event in timeline(history))+"</div>")
        examples.append("".join(part)+"</details>")
    content='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Temporal Role Binding</title><style>body{font:16px system-ui;max-width:1180px;margin:2em auto;padding:0 1em;color:#26313d}td,th{border:1px solid #ccd;padding:.5em}table{border-collapse:collapse;width:100%}.frames{display:flex;flex-wrap:wrap}figure{margin:.3em}img{width:230px;border:1px solid #ccd}details{margin:1em 0}summary{font-weight:600;cursor:pointer}pre{white-space:pre-wrap;overflow-wrap:anywhere}</style><h1>Same frames, different first-support role</h1><p>Status: '+e(report["status"])+'. All geometric objects are pre-drawn. Accent strokes indicate activation. These are support-binding sessions, not geometric proofs. The two chronological histories have identical image multisets and final images.</p><table><tr><th>Condition</th><th>Attempted / planned</th><th>Order accuracy</th><th>None rate</th><th>Failures</th></tr>'+"".join(table)+'</table><p>Unordered, isolated-event and final-only inputs have no unique order target. Correct chronological classification may use simple list comparison and does not establish internal sequential reasoning.</p><details><summary>Counterfactual and direction checks</summary><pre>'+e(json.dumps(report["paired_contrasts"],indent=2))+'</pre></details>'+"".join(examples)+'<details><summary>Full input and sanitized response audit</summary><pre>'+e(json.dumps(report["trials"],indent=2))+'</pre></details></html>'
    (out/"viewer.html").write_text(content,encoding="utf-8")

def save(out,report):
    report["by_condition"]=summarize(report["trials"]);report["paired_contrasts"]=contrasts(report["trials"])
    temp=out/"results.tmp";temp.write_text(json.dumps(report,indent=2),encoding="utf-8");temp.replace(out/"results.json")

def main(out,live=False,workers=3):
    if live and (os.getenv("GITHUB_ACTIONS")!="true" or not os.getenv("TYPESAFE_API_KEY")):
        raise SystemExit("Live calls require GitHub Actions and repository secret; no request made")
    out.mkdir(parents=True,exist_ok=True)
    report={"experiment":"Temporal Role Binding v3","status":"running" if live else "offline_only","model":"jev-1.14.0","seed":SEED,"repeats":REPEATS,"source_commit":os.getenv("GITHUB_SHA"),"run_id":os.getenv("GITHUB_RUN_ID"),"source_provenance":pilot.provenance(),"limits":LIMITS,"trials":[]}
    prepared=[]
    for t in manifest():
        p,m,audit=build_payload(out,t)
        record=dict(t,offline_role_trace=role_trace(timeline(t["history"])),offline_mapping=m,asset_audit=audit,model_input={k:v for k,v in p.items() if k!="assets"},request_sha256=hashlib.sha256(json.dumps(p,sort_keys=True).encode()).hexdigest(),predicted="not_run",correct=None)
        report["trials"].append(record);prepared.append((record,p))
    save(out,report);viewer(out,report)
    if live:
        with ThreadPoolExecutor(max_workers=workers) as pool:
            futures={pool.submit(previous.transport,p):record for record,p in prepared}
            for future in as_completed(futures):
                r=futures[future];answer=future.result();r.update(answer)
                r["predicted"]="failure" if "failure" in answer else r["offline_mapping"].get(answer["response"]["answer"]["choice"],"none")
                r["correct"]=r["predicted"]==r["history"] if r["condition"] in IDENTIFIABLE else None
                save(out,report);print("Completed",sum(t["predicted"]!="not_run" for t in report["trials"]),"/",len(prepared),flush=True)
        report["status"]="completed_with_failures" if any(r["predicted"]=="failure" for r in report["trials"]) else "completed"
    save(out,report);viewer(out,report)
    if report["status"]=="completed_with_failures":raise SystemExit("Failures retained in sanitized report")

if __name__=="__main__":
    ap=argparse.ArgumentParser();ap.add_argument("--out",type=Path,default=Path("output_temporal_binding"));ap.add_argument("--live",action="store_true");ap.add_argument("--workers",type=int,choices=range(1,5),default=3);args=ap.parse_args();main(args.out,args.live,args.workers)

"""Paired image-order ablations. Live transport is restricted to GitHub Actions."""
from __future__ import annotations
import argparse,base64,hashlib,html,importlib.util,itertools,json,math,os,random
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path

SPEC=importlib.util.spec_from_file_location("temporal_pilot",Path(__file__).parents[1]/"temporal_genealogy/benchmark.py")
pilot=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(pilot)
CONDITIONS=("final_only","ordered","middle_only","shuffled","ordered_spaces","spaces_only")
TRANSFORMS=tuple(itertools.product((0,37,83,151),(1,-1)))
PERMUTATIONS=tuple(p for p in itertools.permutations(range(3)) if p!=(0,1,2))
SEED=20261019
REPEATS=2
QUESTION="Which construction origin is supported by the supplied evidence? Choose none when the evidence does not identify a unique origin. This is an evidence-classification question, not a geometric proof."
TASK="Inspect the supplied views in their listed presentation order, if any, and the supplied structural observations, if any. No timestamps are available."
DESCRIPTIONS={"circle":"Intersection of two circles with common radius equal to the base.","translation":"Equal vector basis at pi/3 and translated copies.","none":"The supplied evidence does not identify a unique construction history."}
LIMITS=[
 "SAME_FINAL_STATE != SAME_GENEALOGY. Final-only has no unique historical target; origin accuracy is null.",
 "Chronological, shuffled and middle-only comparisons test order contribution versus diagnostic snapshot evidence.",
 "Asset IDs and structures carry no hidden original time index in shuffled input.",
 "Structured observations are curated explicit evidence; spaces-only is a textual cue control, not autonomous discovery.",
 "Both origins are visually diagnostic in the middle; no order effect would not show an inability to reason temporally in other tasks.",
 "Repeated requests and transformed versions of two templates are not independent geometrical problems.",
 "More than one image does not demonstrate internal sequential reasoning. Recognition is not geometric proof.",
 "This is descriptive paired evidence; no significance or causal mechanism claim is made."]

def manifest():
    trials=[]
    for transform,(angle,reflection) in enumerate(TRANSFORMS):
        for repeat in range(REPEATS):
            cell=transform*REPEATS+repeat
            permutation=PERMUTATIONS[cell%len(PERMUTATIONS)]
            for history in ("circle","translation"):
                for condition in CONDITIONS:
                    trials.append(dict(case=f"t{transform:02d}",angle=angle,reflection=reflection,repeat=repeat,history=history,condition=condition,option_seed=SEED+cell,permutation=permutation))
    random.Random(SEED).shuffle(trials)
    return [dict(t,trial=i) for i,t in enumerate(trials)]

def frame_order(trial):
    c=trial["condition"]
    return {"final_only":(2,),"ordered":(0,1,2),"middle_only":(1,),"shuffled":tuple(trial["permutation"]),"ordered_spaces":(0,1,2),"spaces_only":()}[c]

def build_payload(out,trial):
    rng=random.Random(trial["option_seed"])
    codes=["K"+str(n) for n in rng.sample(range(100000,999999),2)]
    mapping=dict(zip(codes,("circle","translation")))
    options=[(code,DESCRIPTIONS[h]) for code,h in mapping.items()]+[("none",DESCRIPTIONS["none"])];rng.shuffle(options)
    assets={};views=[];audit=[]
    for index,original in enumerate(frame_order(trial)):
        name=f"view{index+1}"
        image=pilot.render(trial["history"],original,trial["angle"],trial["reflection"])
        path=out/"images"/f"{trial['history']}_{trial['angle']}_{trial['reflection']}_{original}.png"
        path.parent.mkdir(parents=True,exist_ok=True);image.save(path)
        data=path.read_bytes()
        assets[name]={"type":"image","format":"png","data_base64":base64.b64encode(data).decode("ascii")}
        views.append(name)
        audit.append({"asset":name,"file":path.relative_to(out).as_posix(),"sha256":hashlib.sha256(data).hexdigest(),"original_frame":original})
    state={"views":views,"task":TASK}
    if trial["condition"] in ("ordered_spaces","spaces_only"):
        # The same structured text is supplied with and without images.
        structures=[]
        for index,frame in enumerate(pilot.spaces(trial["history"])):
            structures.append(dict(observation=index+1,**{k:v for k,v in frame.items() if k!="frame"}))
        state["structural_observations"]=structures
    request={"model":"jev-1.14.0","state":state,"questions":{"origin":{"type":"choice","instructions":QUESTION,"criteria":dict(options)}}}
    if assets:request["assets"]=assets
    return request,mapping,audit

def transport(payload):
    # No live request can escape Actions through a helper call.
    if os.getenv("GITHUB_ACTIONS")!="true" or not os.getenv("TYPESAFE_API_KEY"):
        raise RuntimeError("actions_secret_required")
    import requests
    try:
        res=requests.post("https://api.typesafe.ai/v1/systemone",headers={"Authorization":"Bearer "+os.environ["TYPESAFE_API_KEY"],"TypeSafe-Danger-Zone-Images":"true"},json=payload,timeout=90)
        if res.status_code!=200:return {"failure":f"HTTP_{res.status_code}"}
        raw=res.json();clean=pilot.sanitize(raw)
        choice=clean["answer"].get("choice")
        if choice not in payload["questions"]["origin"]["criteria"]:return {"failure":"invalid_typed_choice"}
        return {"response":clean}
    except Exception:
        return {"failure":"transport_or_schema_failure"}

def mean(values):return sum(values)/len(values) if values else None

def summarize(records):
    summary={}
    for condition in CONDITIONS:
        rows=[r for r in records if r["condition"]==condition]
        attempted=[r for r in rows if r["predicted"]!="not_run"]
        matrix={}
        for row in attempted:
            target="non_identifiable" if condition=="final_only" else row["history"]
            matrix.setdefault(target,{})[row["predicted"]]=matrix.setdefault(target,{}).get(row["predicted"],0)+1
        confidence=[r["response"]["answer"]["confidence"] for r in attempted if isinstance(r.get("response",{}).get("answer",{}).get("confidence"),(float,int))]
        summary[condition]={"planned_n":len(rows),"attempted_n":len(attempted),"failure_n":sum(r["predicted"]=="failure" for r in attempted),"confusion_matrix":matrix,"origin_accuracy":None if condition=="final_only" or not attempted else sum(r["correct"] is True for r in attempted)/len(attempted),"none_rate":mean([r["predicted"]=="none" for r in attempted]),"mean_confidence":mean(confidence),"confidence_n":len(confidence),"usage":{k:sum((r.get("response",{}).get("usage") or {}).get(k,0) or 0 for r in attempted) for k in ("input_tokens","output_tokens")}}
    return summary

def comparisons(records):
    output={}
    for left,right in (("ordered","middle_only"),("ordered","shuffled"),("ordered_spaces","ordered"),("ordered_spaces","spaces_only")):
        cells={}
        for r in records:
            if r["predicted"]=="not_run":continue
            cells.setdefault((r["case"],r["repeat"],r["history"]),{})[r["condition"]]=r
        pairs=[(c[left],c[right]) for c in cells.values() if left in c and right in c]
        output[left+"_vs_"+right]={"paired_n":len(pairs),"both_correct":sum(a["correct"] is True and b["correct"] is True for a,b in pairs),"left_only_correct":sum(a["correct"] is True and b["correct"] is not True for a,b in pairs),"right_only_correct":sum(a["correct"] is not True and b["correct"] is True for a,b in pairs),"neither_correct":sum(a["correct"] is not True and b["correct"] is not True for a,b in pairs),"failure_pairs":sum(a["predicted"]=="failure" or b["predicted"]=="failure" for a,b in pairs)}
    repeats={}
    for r in records:
        if r["predicted"] in ("not_run","failure"):continue
        repeats.setdefault((r["case"],r["history"],r["condition"]),[]).append(r["predicted"])
    output["repeat_agreement"]={c:{"pairs":sum(len(v)==REPEATS for k,v in repeats.items() if k[2]==c),"agreement":mean([len(set(v))==1 for k,v in repeats.items() if k[2]==c and len(v)==REPEATS])} for c in CONDITIONS}
    return output

def viewer(out,report):
    e=html.escape
    rows=[]
    for condition,s in report["by_condition"].items():
        acc="not defined" if s["origin_accuracy"] is None else f"{100*s['origin_accuracy']:.1f}%"
        rows.append(f"<tr><td>{condition}</td><td>{s['attempted_n']}/{s['planned_n']}</td><td>{acc}</td><td>{s['none_rate']}</td><td>{s['failure_n']}</td></tr>")
    sections=[]
    for angle,reflection in TRANSFORMS:
        section=[f"<details><summary>Rotation {angle}, reflection {reflection}</summary>"]
        for history in ("circle","translation"):
            section.append(f"<h3>{history}</h3><div class=frames>"+"".join(f'<figure><img src="images/{history}_{angle}_{reflection}_{f}.png"><figcaption>State {f}</figcaption></figure>' for f in range(3))+"</div>")
        sections.append("".join(section)+"</details>")
    audit="<details><summary>Paired contrasts and repeat agreement</summary><pre>"+e(json.dumps(report["paired_comparisons"],indent=2))+"</pre></details>"
    trials="<details><summary>Trials, model-visible input audit, responses</summary><pre>"+e(json.dumps(report["trials"],indent=2))+"</pre></details>"
    text='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Temporal Genealogy Order Ablation</title><style>body{font:16px system-ui;max-width:1100px;margin:2em auto;padding:0 1em;color:#26313d}table{border-collapse:collapse;width:100%}td,th{padding:.6em;border:1px solid #ccd}details{margin:1.2em 0}summary{cursor:pointer;font-weight:600}.frames{display:flex;flex-wrap:wrap}figure{margin:.4em}img{width:220px;border:1px solid #ddd}pre{white-space:pre-wrap;overflow-wrap:anywhere}</style><h1>SAME_FINAL_STATE != SAME_GENEALOGY</h1><p>Order ablation; observer labels never enter model-visible images. Status: '+e(report["status"])+'.</p><table><tr><th>Condition</th><th>Attempted / planned</th><th>Origin accuracy</th><th>None rate</th><th>Failures</th></tr>'+''.join(rows)+'</table><p>Final-only has no unique history target. Middle-only versus ordered versus shuffled tests whether diagnostic snapshots suffice. Structured input supplies textual evidence. Multiple images do not establish internal sequential reasoning.</p>'+audit+''.join(sections)+trials+'</html>'
    (out/"viewer.html").write_text(text,encoding="utf-8")

def save(out,report):
    report["by_condition"]=summarize(report["trials"])
    report["paired_comparisons"]=comparisons(report["trials"])
    path=out/"results.tmp"
    path.write_text(json.dumps(report,indent=2),encoding="utf-8");path.replace(out/"results.json")

def main(out,live=False,workers=3):
    if live and (os.getenv("GITHUB_ACTIONS")!="true" or not os.getenv("TYPESAFE_API_KEY")):
        raise SystemExit("Live calls require GitHub Actions and TYPESAFE_API_KEY; no request made")
    out.mkdir(parents=True,exist_ok=True)
    report={"experiment":"Temporal Genealogy order ablation v2","status":"running" if live else "offline_only","model":"jev-1.14.0","seed":SEED,"repeats":REPEATS,"source_commit":os.getenv("GITHUB_SHA"),"run_id":os.getenv("GITHUB_RUN_ID"),"source_provenance":pilot.provenance(),"limits":LIMITS,"trials":[]}
    prepared=[]
    for trial in manifest():
        payload,mapping,audit=build_payload(out,trial)
        # No base64 duplication in the observer audit; PNGs plus hashes reconstruct inputs.
        observer={k:v for k,v in payload.items() if k!="assets"}
        record=dict(trial,offline_mapping=mapping,asset_audit=audit,model_input=observer,request_sha256=hashlib.sha256(json.dumps(payload,sort_keys=True).encode()).hexdigest(),predicted="not_run",correct=None)
        report["trials"].append(record);prepared.append((record,payload))
    save(out,report);viewer(out,report)
    if live:
        with ThreadPoolExecutor(max_workers=workers) as pool:
            futures={pool.submit(transport,payload):record for record,payload in prepared}
            for future in as_completed(futures):
                record=futures[future];result=future.result();record.update(result)
                record["predicted"]="failure" if "failure" in result else record["offline_mapping"].get(result["response"]["answer"]["choice"],"none")
                record["correct"]=None if record["condition"]=="final_only" else record["predicted"]==record["history"]
                save(out,report)
                completed=sum(r["predicted"]!="not_run" for r in report["trials"])
                print(f"Completed {completed}/{len(prepared)}",flush=True)
        report["status"]="completed_with_failures" if any(r["predicted"]=="failure" for r in report["trials"]) else "completed"
    save(out,report);viewer(out,report)
    if report["status"]=="completed_with_failures":raise SystemExit("Jev failures saved in sanitized report")

if __name__=="__main__":
    ap=argparse.ArgumentParser();ap.add_argument("--out",type=Path,default=Path("output_temporal_order"));ap.add_argument("--live",action="store_true");ap.add_argument("--workers",type=int,choices=range(1,5),default=3);args=ap.parse_args();main(args.out,args.live,args.workers)

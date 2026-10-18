"""Matched 3 modalities x 2 presentation directions, reusing v3 stimuli."""
from __future__ import annotations
import argparse,hashlib,html,importlib.util,json,os,random
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
SPEC=importlib.util.spec_from_file_location("role_binding",Path(__file__).parents[1]/"temporal_role_binding/benchmark_binding.py")
base=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(base)
MODALITIES=("images","text","combined")
DIRECTIONS=("forward","reverse")
CONDITIONS=tuple(m+"_"+d for m in MODALITIES for d in DIRECTIONS)
SEED=20261021
ALIASES={"images_forward":"ordered_images","images_reverse":"reverse_images","text_forward":"spaces_only","text_reverse":"spaces_only","combined_forward":"ordered_spaces","combined_reverse":"reverse_images"}
LIMITS=[
 "Authored support-binding sessions over pre-drawn geometry; not construction from nothing or geometric proof.",
 "Current task, criteria, direction wording, images, structural records and label seeds are inherited from v3 without prompt strengthening.",
 "The new manipulation reverses the SAME textual records, with latest-to-earliest declared. No timestamps or first-support answer fields are added.",
 "Both modalities are reversed together in combined_reverse. Text-only removes image assets, not structural observations.",
 "Text success with image failure would implicate modality/presentation integration in these inputs, not establish a visual architectural cause.",
 "Failure across modalities would show a broader behavioral direction problem under this encoding, not prove an internal algorithm.",
 "Whole-list reversal also reverses idle/final boundaries; boundary versus activation-only reversal remains unisolated.",
 "Eight transforms and two repetitions of two templates are dependent observations; text-only geometry tags alter no textual content except label remapping.",
 "Separate API requests have no conversational carryover. Repeated calls can vary; do not pool directly with v3 or claim significance.",
 "Simple ordered-list comparison suffices; no result establishes internal sequential reasoning or autonomous induction of roles."]

def manifest():
    trials=[]
    for i,(angle,reflection) in enumerate(base.TRANSFORMS):
        for repeat in range(base.REPEATS):
            for history in ("circle","vector"):
                for modality in MODALITIES:
                    for direction in DIRECTIONS:
                        trials.append(dict(case=f"t{i:02d}",angle=angle,reflection=reflection,repeat=repeat,history=history,modality=modality,direction=direction,condition=modality+"_"+direction,option_seed=base.SEED+i*base.REPEATS+repeat))
    random.Random(SEED).shuffle(trials)
    return [dict(t,trial=i) for i,t in enumerate(trials)]

def build_payload(out,trial):
    alias=ALIASES[trial["condition"]]
    payload,mapping,audit=base.build_payload(out,dict(trial,condition=alias))
    if trial["condition"] in ("text_reverse","combined_reverse"):
        payload["state"]["ordering_convention"]="latest to earliest"
        payload["state"]["structural_observations"]=list(reversed(base.structures(trial["history"])))
    return payload,mapping,audit

def summarize(records):
    result={}
    for c in CONDITIONS:
        rows=[r for r in records if r["condition"]==c];done=[r for r in rows if r["predicted"]!="not_run"]
        matrix={}
        for r in done:matrix.setdefault(r["history"],{})[r["predicted"]]=matrix.setdefault(r["history"],{}).get(r["predicted"],0)+1
        confidence=[r["response"]["answer"]["confidence"] for r in done if isinstance(r.get("response",{}).get("answer",{}).get("confidence"),(int,float))]
        result[c]={"planned_n":len(rows),"attempted_n":len(done),"correct_n":sum(r["correct"] is True for r in done),"order_accuracy":base.previous.mean([r["correct"] is True for r in done]),"none_n":sum(r["predicted"]=="none" for r in done),"opposite_order_n":sum(r["predicted"] in ("circle","vector") and r["predicted"]!=r["history"] for r in done),"failure_n":sum(r["predicted"]=="failure" for r in done),"mean_confidence":base.previous.mean(confidence),"confidence_n":len(confidence),"confusion_matrix":matrix,"usage":{k:sum(((r.get("response",{}).get("usage") or {}).get(k) or 0) for r in done) for k in ("input_tokens","output_tokens")}}
    return result

def paired(records,left,right):
    cells={}
    for r in records:
        if r["predicted"]!="not_run":cells.setdefault((r["case"],r["repeat"],r["history"]),{})[r["condition"]]=r
    pairs=[(v[left],v[right]) for v in cells.values() if left in v and right in v]
    return {"paired_n":len(pairs),"both_correct":sum(a["correct"] is True and b["correct"] is True for a,b in pairs),"left_only_correct":sum(a["correct"] is True and b["correct"] is not True for a,b in pairs),"right_only_correct":sum(a["correct"] is not True and b["correct"] is True for a,b in pairs),"neither_correct":sum(a["correct"] is not True and b["correct"] is not True for a,b in pairs),"failure_pairs":sum(a["predicted"]=="failure" or b["predicted"]=="failure" for a,b in pairs)}

def contrasts(records):
    result={m+"_forward_vs_reverse":paired(records,m+"_forward",m+"_reverse") for m in MODALITIES}
    result.update({a+"_vs_"+b:paired(records,a,b) for a,b in (("text_reverse","images_reverse"),("combined_reverse","images_reverse"),("combined_reverse","text_reverse"))})
    for c in CONDITIONS:
        cells={}
        for r in records:
            if r["condition"]==c and r["predicted"]!="not_run":cells.setdefault((r["case"],r["repeat"]),{})[r["history"]]=r
        pairs=[v for v in cells.values() if "circle" in v and "vector" in v]
        result[c+"_history_pairs"]={"pairs":len(pairs),"both_correct":sum(v["circle"]["correct"] is True and v["vector"]["correct"] is True for v in pairs),"opposite_named_choices":sum({v["circle"]["predicted"],v["vector"]["predicted"]}=={"circle","vector"} for v in pairs)}
    return result

def viewer(out,report):
    e=html.escape;rows=[]
    for m in MODALITIES:
        values=[]
        for d in DIRECTIONS:
            s=report["by_condition"][m+"_"+d]
            values.append("not run" if not s["attempted_n"] else f"{s['correct_n']}/{s['attempted_n']} ({s['order_accuracy']:.1%}); none={s['none_n']}; opposite={s['opposite_order_n']}; failure={s['failure_n']}")
        rows.append(f"<tr><th>{m}</th><td>{values[0]}</td><td>{values[1]}</td></tr>")
    example=[]
    for h in ("circle","vector"):
        example.append(f"<h2>{h} activated first</h2>")
        for d in DIRECTIONS:
            events=base.timeline(h) if d=="forward" else tuple(reversed(base.timeline(h)))
            records=base.structures(h) if d=="forward" else list(reversed(base.structures(h)))
            example.append(f"<h3>{d}</h3><div class=frames>"+"".join(f'<figure><img src="images/{event}_0_1.png"><figcaption>{event}</figcaption></figure>' for event in events)+"</div><details><summary>Equivalent textual observations</summary><pre>"+e(json.dumps(records,indent=2))+"</pre></details>")
    content='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Temporal Direction Across Modalities</title><style>body{font:16px system-ui;max-width:1180px;margin:2em auto;padding:0 1em;color:#26313d}table{border-collapse:collapse;width:100%}th,td{border:1px solid #ccd;padding:.6em}.frames{display:flex;flex-wrap:wrap}figure{margin:.3em}img{width:230px;border:1px solid #ccd}pre{white-space:pre-wrap;overflow-wrap:anywhere}details{margin:1em 0}summary{cursor:pointer;font-weight:600}</style><h1>Temporal direction across images and text</h1><p>Status: '+e(report["status"])+'. Matched 3 modalities × 2 directions. Reverse presentation is explicitly latest to earliest. Same underlying session and same target in both directions.</p><table><tr><th>Evidence</th><th>Earliest to latest</th><th>Latest to earliest</th></tr>'+"".join(rows)+'</table><p>This compares supplied event-order evidence. It does not establish internal sequential reasoning, causal understanding or geometric proof. Repeated two-template cases are dependent.</p><details><summary>Matched contrasts</summary><pre>'+e(json.dumps(report["paired_contrasts"],indent=2))+'</pre></details>'+"".join(example)+'<details><summary>All trials and input audit</summary><pre>'+e(json.dumps(report["trials"],indent=2))+'</pre></details></html>'
    (out/"viewer.html").write_text(content,encoding="utf-8")

def save(out,report):
    report["by_condition"]=summarize(report["trials"]);report["paired_contrasts"]=contrasts(report["trials"])
    temp=out/"results.tmp";temp.write_text(json.dumps(report,indent=2),encoding="utf-8");temp.replace(out/"results.json")

def main(out,live=False,workers=3):
    if live and (os.getenv("GITHUB_ACTIONS")!="true" or not os.getenv("TYPESAFE_API_KEY")):
        raise SystemExit("Live requests require Actions and repository secret; no request made")
    out.mkdir(parents=True,exist_ok=True)
    report={"experiment":"Temporal Direction Across Modalities v4","status":"running" if live else "offline_only","model":"jev-1.14.0","seed":SEED,"label_seed_base":base.SEED,"repeats":base.REPEATS,"source_commit":os.getenv("GITHUB_SHA"),"run_id":os.getenv("GITHUB_RUN_ID"),"source_provenance":base.pilot.provenance(),"limits":LIMITS,"trials":[]}
    prepared=[]
    for t in manifest():
        p,m,audit=build_payload(out,t)
        r=dict(t,offline_mapping=m,asset_audit=audit,offline_role_trace=base.role_trace(base.timeline(t["history"])),model_input={k:v for k,v in p.items() if k!="assets"},request_sha256=hashlib.sha256(json.dumps(p,sort_keys=True).encode()).hexdigest(),predicted="not_run",correct=None)
        report["trials"].append(r);prepared.append((r,p))
    save(out,report);viewer(out,report)
    if live:
        with ThreadPoolExecutor(max_workers=workers) as pool:
            futures={pool.submit(base.previous.transport,p):r for r,p in prepared}
            for f in as_completed(futures):
                r=futures[f];answer=f.result();r.update(answer)
                r["predicted"]="failure" if "failure" in answer else r["offline_mapping"].get(answer["response"]["answer"]["choice"],"none")
                r["correct"]=r["predicted"]==r["history"]
                save(out,report);print("Completed",sum(t["predicted"]!="not_run" for t in report["trials"]),"/",len(prepared),flush=True)
        report["status"]="completed_with_failures" if any(r["predicted"]=="failure" for r in report["trials"]) else "completed"
    save(out,report);viewer(out,report)
    if report["status"]=="completed_with_failures":raise SystemExit("Failures retained in sanitized report")

if __name__=="__main__":
    ap=argparse.ArgumentParser();ap.add_argument("--out",type=Path,default=Path("output_temporal_direction"));ap.add_argument("--live",action="store_true");ap.add_argument("--workers",type=int,choices=range(1,5),default=3);args=ap.parse_args();main(args.out,args.live,args.workers)

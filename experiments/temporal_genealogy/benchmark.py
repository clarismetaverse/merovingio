"""Temporal genealogy: controlled visual histories, not geometric proof."""
import argparse, base64, hashlib, json, math, os, random
from pathlib import Path
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[2]
SOURCES=["workspace_equilateral_same_state_different_genealogy_v0_4_1.json","workspace_two_circles_triangle_v0_4_1.json"]
CONDITIONS=("final_only","sequence","sequence_spaces")

def provenance():
    result=[]
    for name in SOURCES:
        path=ROOT/"NMerovingio/graph/examples"/name
        data=json.loads(path.read_text(encoding="utf-8"))
        result.append({"file":str(path.relative_to(ROOT)),"sha256":hashlib.sha256(path.read_bytes()).hexdigest(),"workspace":data["workspace"],"nodes":data["nodes"],"edges":data["edges"]})
    return result

def points(angle,reflection):
    raw=[(-80,46.188021535),(80,46.188021535),(0,-92.37604307)]
    a=math.radians(angle)
    return [(256+reflection*x*math.cos(a)-y*math.sin(a),256+reflection*x*math.sin(a)+y*math.cos(a)) for x,y in raw]

def render(history,frame,angle=0,reflection=1):
    im=Image.new("RGB",(512,512),"white");d=ImageDraw.Draw(im)
    A,B,C=points(angle,reflection);fg="#26313d"
    def line(a,b):d.line((a,b),fill=fg,width=3)
    def arrow(a,b):
        line(a,b);t=math.atan2(b[1]-a[1],b[0]-a[0])
        for delta in (-.45,.45):line(b,(b[0]-12*math.cos(t+delta),b[1]-12*math.sin(t+delta)))
    line(A,B)
    if frame==1:
        if history=="circle":
            for x,y in (A,B):d.ellipse((x-160,y-160,x+160,y+160),outline=fg,width=3)
        else:
            arrow(A,B);arrow(A,C)
            D=(B[0]+C[0]-A[0],B[1]+C[1]-A[1])
            arrow(B,D);arrow(C,D)
            # Equal-length ticks and an unlabelled 60 degree sector.
            for P in (B,C):
                m=((A[0]+P[0])/2,(A[1]+P[1])/2);v=(P[0]-A[0],P[1]-A[1]);l=math.hypot(*v)
                line((m[0]-5*v[1]/l,m[1]+5*v[0]/l),(m[0]+5*v[1]/l,m[1]-5*v[0]/l))
            u=math.atan2(B[1]-A[1],B[0]-A[0]);v=math.atan2(C[1]-A[1],C[0]-A[0]);diff=(v-u+math.pi)%(2*math.pi)-math.pi
            arc=[(A[0]+24*math.cos(u+diff*i/20),A[1]+24*math.sin(u+diff*i/20)) for i in range(21)]
            d.line(arc,fill=fg,width=2)
    if frame==2:
        # Identical code and coordinates for both histories. No construction residue.
        line(A,C);line(B,C)
    for x,y in ([A,B,C] if frame==2 else [A,B]):d.ellipse((x-3,y-3,x+3,y+3),fill=fg)
    return im

def spaces(history):
    # Structural evidence is the experimental manipulation, not a hidden answer key.
    if history=="circle":
        middle={"mental_spaces":[{"objects":["p","q"],"relation":"center to boundary","carrier":"s0"},{"objects":["q","p"],"relation":"center to boundary","carrier":"s0"}],"generic_space":{"shared_carrier":"s0","relation":"equal distance"},"role_changes":{"s0":["base","radial carrier"],"r":["unbound","shared boundary point"]}}
    else:
        middle={"mental_spaces":[{"objects":["p","q"],"relation":"directed displacement","carrier":"s0"},{"objects":["p","r"],"relation":"directed displacement","carrier":"s1"}],"generic_space":{"relations":["equal displacement norms","included angle pi/3","translated copies preserve displacement"]},"role_changes":{"s0":["base","translation generator"],"s1":["unbound","translation generator"]}}
    return [{"frame":0,"mental_spaces":[{"objects":["p","q"],"carrier":"s0","relation":"segment"}],"roles":{"s0":"base"}},dict(frame=1,**middle),{"frame":2,"mental_spaces":[{"objects":["p","q","r"],"relation":"closed triangle"}],"roles":{"s0":"side","s1":"side","s2":"side"}}]

def payload(out,history,condition,angle,reflection,seed):
    rng=random.Random(seed)
    labels=["K"+str(x) for x in rng.sample(range(100,999),2)]
    mapping=dict(zip(labels,("circle","translation")))
    descriptions={"circle":"Intersection of two circles with common radius equal to the base.","translation":"Equal vector basis at pi/3 and translated copies."}
    items=list(mapping);rng.shuffle(items)
    criteria={k:descriptions[mapping[k]] for k in items}
    criteria["none"]="The supplied evidence does not identify a unique construction history."
    assets={};frames=[]
    for f in ([2] if condition=="final_only" else [0,1,2]):
        image=render(history,f,angle,reflection)
        path=out/"images"/f"{history}_{angle}_{reflection}_{f}.png";path.parent.mkdir(parents=True,exist_ok=True);image.save(path)
        key=f"frame{f}";assets[key]={"type":"image","format":"png","data_base64":base64.b64encode(path.read_bytes()).decode()};frames.append(key)
    state={"ordered_frames":frames,"task":"Infer the construction origin from the available evidence. The final geometry alone can have multiple origins."}
    if condition=="sequence_spaces":state["frame_structures"]=spaces(history)
    return {"model":"jev-1.14.0","assets":assets,"state":state,"questions":{"origin":{"type":"choice","instructions":"Which construction origin is supported? Choose none when the evidence cannot distinguish the histories. This asks about construction evidence, not a geometric proof.","criteria":criteria}}},mapping

def sanitize(response):
    # Explicit schema allowlist: no free-form server text or credentials.
    def number(x):return x if isinstance(x,(int,float)) and not isinstance(x,bool) and math.isfinite(x) else None
    a=response.get("answers",{}).get("origin",{})
    answer={"choice":a.get("choice")}
    for key in ("confidence","reliability"):
        answer[key]=number(a.get(key))
    if isinstance(a.get("probabilities"),dict):
        answer["probabilities"]={k:number(v) for k,v in a["probabilities"].items() if k=="none" or (k.startswith("K") and k[1:].isdigit())}
    usage=response.get("usage")
    return {"answer":answer,"usage":{k:number(v) for k,v in usage.items() if k in ("input_tokens","output_tokens","total_tokens","cached_tokens","reasoning_tokens")} if isinstance(usage,dict) else None,"reliability":number(response.get("reliability"))}

def summarize(records):
    result={}
    for condition in CONDITIONS:
        rows=[r for r in records if r["condition"]==condition];matrix={}
        for r in rows:
            key=r["history"] if condition!="final_only" else "non_identifiable"
            matrix.setdefault(key,{})[r["predicted"]]=matrix.setdefault(key,{}).get(r["predicted"],0)+1
        confidence=[r["response"]["answer"]["confidence"] for r in rows if isinstance(r.get("response",{}).get("answer",{}).get("confidence"),(float,int))]
        result[condition]={"n":len(rows),"failures":sum(r["predicted"]=="failure" for r in rows),"confusion_matrix":matrix,"genealogy_accuracy":None if condition=="final_only" else sum(r["correct"] is True for r in rows)/len(rows) if rows else None,"abstention_rate":sum(r["predicted"]=="none" for r in rows)/len(rows) if rows else None,"mean_confidence":sum(confidence)/len(confidence) if confidence else None,"confidence_n":len(confidence)}
    return result

def viewer(out):
    groups=[]
    for a,r in ((0,1),(37,1),(0,-1),(37,-1)):
        groups.append(f"<h2>Rotation {a}, reflection {r}</h2>")
        for h in ("circle","translation"):
            groups.append(f"<h3>{h}</h3>"+"".join(f'<img width="220" src="images/{h}_{a}_{r}_{f}.png">' for f in range(3)))
    (out/"viewer.html").write_text('<!doctype html><meta charset="utf-8"><title>Temporal Genealogy</title><style>body{font:16px system-ui;max-width:1000px;margin:2em auto}img{border:1px solid #ccc}</style><h1>SAME_FINAL_STATE != SAME_GENEALOGY</h1><p>Observer viewer; labels here never enter model-visible images. Multiple images do not establish internal sequential reasoning. See results.json for outcomes.</p>'+''.join(groups),encoding="utf-8")

def main(out,live=False):
    out.mkdir(parents=True,exist_ok=True)
    if live and (os.getenv("GITHUB_ACTIONS")!="true" or not os.getenv("TYPESAFE_API_KEY")):raise SystemExit("Live calls require GitHub Actions and TYPESAFE_API_KEY")
    trials=[(h,c,a,r) for a,r in ((0,1),(37,1),(0,-1),(37,-1)) for h in ("circle","translation") for c in CONDITIONS]
    random.Random(114).shuffle(trials);records=[]
    report={"status":"running" if live else "offline_only","seed":114,"model":"jev-1.14.0","source_provenance":provenance(),"trials":records,"limits":["Final-only has no unique genealogy ground truth: 50% forced-choice accuracy is not success.","Structured relations are supplied evidence, not autonomous extraction; improvement can be textual cue use.","Multiple-image input does not demonstrate internal sequential reasoning.","Distinguishability is not geometric proof; small controlled pilot, not generalization.","Role structures are curated reconstructions of historical workspaces, not historical animation logs."]}
    for i,(h,c,a,r) in enumerate(trials):
        p,m=payload(out,h,c,a,r,114+((0 if a==0 else 2)+(0 if r==1 else 1)))
        rec={"trial":i,"history":h,"condition":c,"angle":a,"reflection":r,"offline_mapping":m,"predicted":"not_run","correct":None,"request_sha256":hashlib.sha256(json.dumps(p,sort_keys=True).encode()).hexdigest()}
        if live:
            import requests
            try:
                res=requests.post("https://api.typesafe.ai/v1/systemone",headers={"Authorization":"Bearer "+os.environ["TYPESAFE_API_KEY"],"TypeSafe-Danger-Zone-Images":"true"},json=p,timeout=90)
                if res.status_code!=200:raise RuntimeError("HTTP_"+str(res.status_code))
                raw=res.json();s=sanitize(raw);choice=s["answer"].get("choice")
                if choice not in {*m,"none"}:raise ValueError("invalid_typed_choice")
                rec.update(response=s,predicted=m.get(choice,"none"))
                rec["correct"]=None if c=="final_only" else rec["predicted"]==h
            except Exception as e:rec.update(predicted="failure",failure=type(e).__name__+":"+(str(e) if isinstance(e,RuntimeError) else "request_or_schema_failure"))
        records.append(rec);report["by_condition"]=summarize(records)
        (out/"results.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
    report["status"]="completed_with_failures" if live and any(r["predicted"]=="failure" for r in records) else "completed" if live else "offline_only"
    (out/"results.json").write_text(json.dumps(report,indent=2),encoding="utf-8");viewer(out)
    if live and any(r["predicted"]=="failure" for r in records):raise SystemExit("One or more Jev calls failed; see sanitized report")

if __name__=="__main__":
    ap=argparse.ArgumentParser();ap.add_argument("--out",type=Path,default=Path("output_temporal"));ap.add_argument("--live",action="store_true");args=ap.parse_args();main(args.out,args.live)

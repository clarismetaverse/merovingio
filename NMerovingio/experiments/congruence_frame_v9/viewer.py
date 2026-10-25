#!/usr/bin/env python3
"""Standalone offline viewer for actual v9 frame competition traces."""
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
OUT=HERE/"results"
HTML=r"""<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Merovingio v9 · LAL versus LLL</title><style>
:root{color-scheme:dark;font-family:Inter,ui-sans-serif,system-ui,sans-serif}
*{box-sizing:border-box}body{background:#12131d;color:#f1edfa;margin:0}
header{padding:24px max(18px,calc((100vw - 1220px)/2));background:#1d1c2b;border-bottom:1px solid #403b54}
h1{margin:4px 0 7px;font-size:26px}.eyebrow{letter-spacing:1.7px;text-transform:uppercase;color:#c2a3e6;font-size:11px;font-weight:700}
p{font-size:12px;color:#bfb8d1;line-height:1.55}h2{font-size:16px;margin:0 0 13px}h3{font-size:13px;margin:12px 0}
main{max-width:1220px;margin:auto;display:grid;gap:14px;padding:17px}
.panel{background:#1f2031;border:1px solid #454056;border-radius:13px;padding:15px;min-width:0}
.controls{display:flex;gap:13px;flex-wrap:wrap;align-items:end}
label{color:#c6bdd1;font-size:12px;display:flex;flex-direction:column;gap:6px}
select,input{background:#141727;border:1px solid #665d79;border-radius:7px;font:inherit;color:#eee9fa;padding:9px}
input[type=range]{padding:0;accent-color:#a897ed;width:170px}
.columns{display:grid;grid-template-columns:1fr 1fr;gap:14px}
svg{background:#171925;border-radius:9px;width:100%}
.frames{display:grid;gap:11px}.frame{border:1px solid #524d65;border-radius:10px;padding:11px;background:#2b293e}
.frame.active{border-color:#b6a0e9}.bar{height:10px;background:#373648;border-radius:10px;overflow:hidden}
.fill{height:100%;background:linear-gradient(90deg,#5a92bc,#caa1ed)}
.frame h3{display:flex;justify-content:space-between;margin:0 0 7px}
.slots{font-size:12px;line-height:1.8}.slot{display:inline-flex;margin:3px 5px 3px 0;border:1px solid #746e88;padding:5px 8px;border-radius:7px;font-size:11px}
.slot.yes{color:#bde4c7;border-color:#639d7c}.slot.no{color:#e7bd9a;border-color:#936d55}
.story{font-size:12px;background:#302b45;border-left:3px solid #c0a6ea;padding:11px;border-radius:7px;line-height:1.55}
.note{font-size:12px;line-height:1.5;padding:11px;background:#332b21;border:1px solid #8c7049;border-radius:9px;color:#e8d1a8}
.kpis{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
.kpi{background:#28273b;padding:12px;border-radius:9px}.kpi small{color:#a9a4be;font-size:10px}.kpi b{font-size:22px;color:#e6cfff;display:block}
table{border-collapse:collapse;font-size:11px;width:100%}td,th{text-align:left;padding:9px;border-bottom:1px solid #443e54}
th{color:#d0bfdc}.timeline{display:flex;gap:6px;flex-wrap:wrap}.step{background:#333044;color:#d2c8df;border:1px solid #665878;border-radius:8px;padding:7px 9px;font-size:11px}
.step.current{border-color:#bca6f0;color:white}
@media(max-width:850px){.columns{grid-template-columns:1fr}.kpis{grid-template-columns:1fr}}
</style></head><body><header><div class="eyebrow">Merovingio · Panoptikon · v9</div>
<h1>Come viene attratto un frame di congruenza?</h1>
<p>Due frame in competizione, LAL e LLL. Le evidenze iniziali, la bisettrice e il lato condiviso riempiono progressivamente i loro ruoli. Il sistema distingue la salienza di un frame dalla sua effettiva applicabilità.</p></header>
<main>
<div class="panel controls">
<label>Figura<select id="shape"><option value="equilateral">Equilatero di Euclide I.10</option><option value="isosceles">Isoscele non equilatero</option><option value="scalene">Scaleno · controllo negativo</option></select></label>
<label>Angolo obiettivo<select id="goal"><option value="C">C</option><option value="A">A</option><option value="B">B</option></select></label>
<label>Condizione<select id="condition"><option value="balanced">Frame con prior uguali</option><option value="LLL_initially_favored">LLL favorito inizialmente</option><option value="without_prospection">Senza frame prospettico</option><option value="angle_witness_masked">Uguaglianza angolare oscurata</option><option value="counterfactual_base_given">Controfattuale: uguaglianza base aggiunta come premessa</option></select></label>
<label>Seed<select id="seed"></select></label>
<label>Fase <span id="phase"></span><input id="tick" type="range" min="0" max="4" value="3"></label>
</div>
<div class="kpis">
<div class="kpi"><small>Frame favorito al termine</small><b id="k1">—</b></div>
<div class="kpi"><small>LAL rigorosamente applicabile?</small><b id="k2">—</b></div>
<div class="kpi"><small>LLL ha tutte le premesse?</small><b id="k3">—</b></div>
</div>
<div class="columns">
<div class="panel"><h2>Costruzione e binding</h2><svg id="figure" viewBox="0 0 395 330"></svg>
<h3>Ruoli delle due sottofigure</h3><div id="bindings" class="slots"></div>
<div class="note">LLL non può assumere AD = DB per dimostrare AD = DB. LAL può invece dedurre questa uguaglianza dall'equivalenza dei due lati corrispondenti e dell'angolo compreso, quando tali premesse sono effettivamente date.</div></div>
<div class="panel"><h2>Competizione fra frame</h2><div id="frames" class="frames"></div><h3>Evento corrente</h3><div id="story" class="story"></div>
<h3>Sequenza</h3><div class="timeline" id="steps"></div></div>
</div>
<div class="panel"><h2>Statistiche sperimentali (48 seed)</h2>
<table><thead><tr><th>Condizione</th><th>LAL scelto</th><th>LAL completamente supportato</th><th>LLL completamente supportato</th><th>Uguaglianza dedotta da SAS</th></tr></thead><tbody id="summary"></tbody></table>
<p>La preferenza è campionata da un punteggio ingegnerizzato. La correttezza della deduzione è verificata separatamente, sulla base di premesse strutturali esplicite. Non è una simulazione empiricamente validata di cognizione umana.</p></div>
</main><script id="data" type="application/json">__DATA__</script><script>
"use strict";
const D=JSON.parse(document.getElementById("data").textContent),$=id=>document.getElementById(id);
D.seeds.forEach(n=>{let o=document.createElement("option");o.value=n;o.textContent="Seed "+n;$("seed").append(o)});
const active=()=>D.runs.find(x=>x.shape===$("shape").value&&x.goal===$("goal").value&&x.condition===$("condition").value&&x.seed===Number($("seed").value));
function line(a,b,c,w=3){return '<line x1="'+a[0]+'" y1="'+a[1]+'" x2="'+b[0]+'" y2="'+b[1]+'" stroke="'+c+'" stroke-width="'+w+'" stroke-linecap="round"/>'}
function draw(r,t){
const ws=t===0?r.preconstruction:r.postconstruction,p=ws.points;
let svg="";
if(t>0){ws.faces.forEach((f,i)=>{svg+='<polygon points="'+f.map(v=>p[v].join(",")).join(" ")+'" fill="'+(i===0?"#5979a2":"#b0a06b")+'" opacity=".18"/>'})}
const outline=r.preconstruction.faces[0];for(let i=0;i<outline.length;i++)svg+=line(p[outline[i]],p[outline[(i+1)%outline.length]],"#eae5f3",3);
if(t>0){const ev=ws.construction_events[0];svg+=line(p[ev.vertex],p[ev.contact_point],"#bea0f0",4)}
else if(r.prospective){let v=r.goal,oth=outline.filter(x=>x!==v),pt=p[v];let mid=[(p[oth[0]][0]+p[oth[1]][0])/2,(p[oth[0]][1]+p[oth[1]][1])/2];svg+='<line x1="'+pt[0]+'" y1="'+pt[1]+'" x2="'+(pt[0]+.53*(mid[0]-pt[0]))+'" y2="'+(pt[1]+.53*(mid[1]-pt[1]))+'" stroke="#b69ee8" stroke-width="2" stroke-dasharray="7 5"/>'}
for(const [key,pt] of Object.entries(p)){svg+='<circle cx="'+pt[0]+'" cy="'+pt[1]+'" r="4.3" fill="white"/><text x="'+(pt[0]+9)+'" y="'+(pt[1]-8)+'" fill="#fff" font-size="15">'+key+'</text>'}
$("figure").innerHTML=svg;
$("bindings").innerHTML=t===0?'<span class="slot">CD non esiste ancora</span>':Object.entries(r.structural_role_schema.role_pairs).map(([name,pair])=>'<span class="slot">'+name.replaceAll("_"," ")+'</span>').join("");
}
function render(){
let r=active();
if(!r){$("condition").value="balanced";$("goal").value="C";r=active()}
if(!r)return;
let ix=Math.min(Number($("tick").value),r.timeline.length-1);$("tick").value=ix;$("phase").textContent=ix+"/4";
let e=r.timeline[ix],scores=e.frame_attraction;draw(r,ix);
$("k1").textContent=r.selected_frame;
$("k2").textContent=r.independent_proof_verifier.licensed?"Sì":"No";
$("k3").textContent=r.LLL_licensed_without_using_conclusion?"Sì":"No";
$("frames").innerHTML=["LAL","LLL"].map(name=>{
let s=scores[name],slots=r.frame_memory[name].slots;
let captions={equal_outer_legs:"Lati esterni uguali",equal_shared_side:"Lato comune",equal_included_angles:"Angolo compreso uguale",equal_base_halves:"Metà della base uguali"};
return '<div class="frame '+(scores[name].score>=scores[name==="LAL"?"LLL":"LAL"].score?"active":"")+'"><h3><span>'+name+' · '+r.frame_memory[name].label+'</span><span>'+Math.round(100*s.attraction_probability)+'%</span></h3><div class="bar"><div class="fill" style="width:'+(100*s.attraction_probability)+'%"></div></div><div class="slots">'+slots.map(k=>'<span class="slot '+(e.evidence[k].status==="verified"?"yes":"no")+'">'+captions[k]+': '+e.evidence[k].status+'</span>').join("")+'</div></div>';
}).join("");
const descriptions={
BEFORE_CD:"Prima della bisettrice: le uguaglianze esterne provengono dall'assunzione geometrica, mentre i ruoli della futura costruzione sono incompleti.",
CONSTRUCT_AND_FIND_TWO_FACES:"La bisettrice viene costruita, i due sottotriangoli diventano materiali e i ruoli LAL/LLL sono riconosciuti, ma i witness devono ancora essere ispezionati.",
REBASE_BIND_EVIDENCE:"Nuovo witness ispezionato: "+(e.newly_inspected_slot||"")+". I punteggi di entrambi i frame vengono ricalcolati.",
COMPETING_FRAME_BINDING:"Valutazione finale. Frame attratto: "+r.selected_frame+". Regola SAS verificata indipendentemente: "+(r.independent_proof_verifier.licensed?"applicabile":"non applicabile")+"."
};
$("story").textContent=descriptions[e.stage];
$("steps").innerHTML=r.timeline.map((z,i)=>'<span class="step '+(i===ix?"current":"")+'">'+i+' · '+z.stage+'</span>').join("");
let stats=D.aggregates[r.shape][r.goal];
$("summary").innerHTML=Object.entries(stats).map(([name,a])=>'<tr><td>'+name+'</td><td>'+Math.round(100*a.LAL_selected_rate)+'%</td><td>'+Math.round(100*a.LAL_fully_supported_rate)+'%</td><td>'+Math.round(100*a.LLL_fully_supported_rate)+'%</td><td>'+Math.round(100*a.certified_SAS_rate)+'%</td></tr>').join("");
}
["shape","goal","condition","seed"].forEach(id=>$(id).addEventListener("change",render));
$("tick").addEventListener("input",render);render();
</script></body></html>"""


def main():
    data=json.loads((OUT/"traces.json").read_text(encoding="utf-8"))
    tiny={k:data[k] for k in ("schema","conditions","shapes","aggregates")}
    tiny["seeds"]=data["seeds"][:12]
    tiny["runs"]=[r for r in data["runs"] if r["seed"] in tiny["seeds"]]
    embedded=json.dumps(tiny,separators=(",",":"),ensure_ascii=False).replace("</","<\\/")
    (OUT/"viewer.html").write_text(HTML.replace("__DATA__",embedded),encoding="utf-8")
    lines=["# Merovingio v9 — Frame attraction: LAL versus LLL",
           "", "A competing frame is *attracted* by observed role equalities; it is NOT a proof.",
           "", "| Shape | Goal | Regime | N | LAL selected | LAL supported | LLL supported | SAS conclusion licensed | Mean LAL attraction |",
           "|---|---|---|---:|---:|---:|---:|---:|---:|"]
    for shape,goals in data["aggregates"].items():
        for goal,conditions in goals.items():
            for cond,v in conditions.items():
                lines.append("| "+" | ".join((shape,goal,cond,str(v["n"]),
                  str(v["LAL_selected_rate"]),str(v["LAL_fully_supported_rate"]),
                  str(v["LLL_fully_supported_rate"]),str(v["certified_SAS_rate"]),
                  str(v["mean_LAL_attraction"]) ))+" |")
    lines+=["", "## Assumptions and circularity",
            "The equilateral initial construction licenses equality of the triangle's three original sides.",
            "After constructing the bisector, the two emerging triangles have a COMMON side and EQUAL INCLUDED apex angles.",
            "LAL therefore has all three evidence slots. LLL lacks the equality of the two base parts AD=DB, which is the conclusion.",
            "The separate COUNTERFACTUAL_EXTRA_GIVEN condition supplies that equality as an explicit additional premise so LLL can genuinely become applicable. It is NOT a proof of midpoint.",
            "An independent narrow SAS rule checker may derive equality of the base portions only when all of its separately grounded prerequisites are verified.",
            "A merely attractive or prospective LLL cannot back-propagate its own desired conclusion into the premises.",
            "Weights, choice stochasticity and frame templates are engineered and do not establish an empirically validated cognitive mechanism.",
            ""]
    (OUT/"REPORT.md").write_text("\n".join(lines),encoding="utf-8")
    print("Generated",OUT/"viewer.html",OUT/"REPORT.md")
if __name__=="__main__":main()

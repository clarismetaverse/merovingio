#!/usr/bin/env python3
"""Build a standalone read-only timeline explorer from actually executed traces."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "results"
HTML = r"""<!doctype html>
<html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Merovingio · Gestalt Propagation</title>
<style>
:root{font-family:Inter,ui-sans-serif,system-ui,sans-serif;color:#eee7fb;background:#11131d}
*{box-sizing:border-box}body{margin:0}header{padding:25px max(18px,calc((100vw - 1260px)/2));border-bottom:1px solid #373446;background:#171924}
h1{font-size:24px;margin:0 0 7px}p{color:#aba9c1;line-height:1.55;margin:5px 0}.eyebrow{font-size:11px;font-weight:700;letter-spacing:2px;color:#c6a0ff;text-transform:uppercase}
main{max-width:1260px;margin:auto;padding:20px;display:grid;gap:16px}
.controls{display:flex;flex-wrap:wrap;gap:14px;align-items:end;padding:14px;background:#1b1c29;border:1px solid #373446;border-radius:14px}
label{font-size:12px;font-weight:600;color:#bbb8d0;display:flex;flex-direction:column;gap:6px}
select,input{background:#11141f;border:1px solid #514f60;border-radius:8px;color:#f7f0ff;padding:8px 11px;font:inherit}
input[type=range]{padding:0;width:200px;accent-color:#bc94ed}
.columns{display:grid;grid-template-columns:minmax(300px,.93fr) minmax(400px,1.07fr);gap:16px}
.panel{border:1px solid #383747;border-radius:14px;background:#1b1d29;padding:18px;min-width:0}
h2{font-size:16px;margin:0 0 14px;color:#f6ecff}h3{font-size:13px;margin:14px 0 9px;color:#dacdf0}
svg{width:100%;height:auto;background:#151925;border-radius:12px}
.meter{display:grid;grid-template-columns:100px 1fr 43px;align-items:center;gap:8px;margin:9px 0;font-size:12px}
.track{height:9px;border-radius:99px;overflow:hidden;background:#303346}
.fill{height:100%;background:linear-gradient(90deg,#8479f8,#ca9ee7)}
.group{display:inline-flex;margin:4px 5px 4px 0;padding:7px 9px;border:1px solid #585174;background:#29253b;border-radius:9px;font-size:11px;color:#ede2ff}
.group.analogy{border-color:#d1a360;background:#393127}
#event{padding:12px;background:#24283a;border-left:3px solid #a98ee3;min-height:88px;border-radius:7px;font-size:13px;line-height:1.6}
#trace{max-height:390px;overflow:auto;display:grid;gap:6px}
.trace-row{font-size:12px;line-height:1.4;padding:9px;border-radius:7px;background:#272736;color:#c5c2d1}
.trace-row.active{outline:1px solid #b599e9;color:#fff}
.summary{display:grid;grid-template-columns:repeat(4,minmax(90px,1fr));gap:10px}
.metric{padding:13px;background:#232333;border-radius:10px}
.metric strong{display:block;font-size:21px;color:#dec5ff}.metric small{font-size:11px;color:#a9a6bd}
.note{font-size:12px;color:#dbc4a5;border:1px solid #705e46;border-radius:10px;padding:12px;background:#31291f}
@media(max-width:900px){.columns{grid-template-columns:1fr}.summary{grid-template-columns:repeat(2,minmax(90px,1fr))}}
</style></head><body>
<header><div class="eyebrow">Merovingio / Panoptikon · Cognitive experiment v1</div>
<h1>Macro ↔ Micro Gestalt Propagation</h1>
<p>La tensione analogica angoli ↔ lati orienta la nascita dei sottogruppi. Ogni raggruppamento può riattivare i macroconcetti.</p></header>
<main>
<section class="controls">
<label>Condizione<select id="condition"><option value="bottom_up">A · Solo bottom-up</option><option value="top_down">B · Macro → micro</option><option value="reciprocal" selected>C · Macro ↔ micro</option></select></label>
<label>Geometria<select id="mode"><option value="isosceles">Isoscele · I.10</option><option value="scalene">Scaleno · controllo negativo</option></select></label>
<label>Random seed<select id="seed"></select></label>
<label>Evento <span id="ticklabel"></span><input type="range" id="tick" min="0" max="12" value="8" step="1"></label>
</section>
<div class="summary">
<div class="metric"><small>Opposizioni emerse</small><strong id="m-op">—</strong></div>
<div class="metric"><small>Triplette SAS</small><strong id="m-sas">—</strong></div>
<div class="metric"><small>Generic candidates</small><strong id="m-gs">—</strong></div>
<div class="metric"><small>Certificazioni metriche false</small><strong id="m-false">0</strong></div>
</div>
<div class="columns">
<div class="panel"><h2>Workspace geometrico</h2><svg id="geom" viewBox="0 0 610 400"></svg>
<h3>Raggruppamenti costituiti finora</h3><div id="groups"></div>
<div class="note">∠ACD = ∠DCB è dato dalla costruzione. AD = DB? è una destinazione analogica ipotetica; in uno scaleno NON segue dalla bisettrice.</div></div>
<div class="panel"><h2>Slipnet · propagazione dell'attivazione</h2><div id="meters"></div>
<h3>Codelet ed evidenze al tick corrente</h3><div id="event"></div>
<h3>Genealogia degli eventi</h3><div id="trace"></div></div>
</div>
<div class="panel"><h2>Confronto fra le ablazioni · risultati dei seed eseguiti</h2><div id="compare"></div>
<p>La simulazione ha priors e codelets manuali: queste differenze, se presenti, illustrano un meccanismo ingegneristico, non provano un modello cognitivo umano. Nessun modello Jev/LLM invocato.</p></div>
</main>
<script type="application/json" id="results-data">__EMBED__</script>
<script>
"use strict";
const DATA=JSON.parse(document.getElementById("results-data").textContent);
const byId=x=>document.getElementById(x);
const seedSel=byId("seed");
DATA.seeds.forEach(s=>{let o=document.createElement("option");o.value=s;o.textContent="Seed "+s;seedSel.appendChild(o)});
function current(){return DATA.runs.find(r=>r.mode===byId("mode").value&&r.condition===byId("condition").value&&r.seed===Number(seedSel.value))}
function segment(a,b,color,width,dash){
return '<line x1="'+a[0]+'" y1="'+a[1]+'" x2="'+b[0]+'" y2="'+b[1]+'" stroke="'+color+'" stroke-width="'+width+'"'+(dash?' stroke-dasharray="8 5"':'')+' stroke-linecap="round"/>'}
function polygon(a,b,c,fill){return '<polygon points="'+[a,b,c].map(p=>p.join(",")).join(" ")+'" fill="'+fill+'" opacity=".16"/>'}
function dot(p,name){return '<circle cx="'+p[0]+'" cy="'+p[1]+'" r="5" fill="#eee7fb"/><text x="'+(p[0]+9)+'" y="'+(p[1]-10)+'" fill="#eee7fb" font-size="18">'+name+'</text>'}
function renderGeom(run,selected){
let P=run.construction.points, A=P.A,B=P.B,C=P.C,D=P.D, z='';
if(selected.includes("LEFT_TRIANGLE"))z+=polygon(A,C,D,"#deaf64");
if(selected.includes("RIGHT_TRIANGLE"))z+=polygon(B,C,D,"#6bc4d0");
z+=segment(A,B,"#dedbea",3)+segment(A,C,"#dedbea",3)+segment(B,C,"#dedbea",3)+segment(C,D,"#ae8aee",5);
if(selected.includes("BASE_PAIR"))z+=segment(A,D,"#e0ab61",6)+segment(D,B,"#6bc4d0",6);
if(selected.includes("OPPOSITION_PAIR")){z+=segment([C[0]-20,C[1]+32],[D[0]-20,D[1]-17],"#dda65d",2,true);z+=segment([C[0]+20,C[1]+32],[D[0]+20,D[1]-17],"#65c0ce",2,true)}
z+=dot(A,"A")+dot(B,"B")+dot(C,"C")+dot(D,"D");
byId("geom").innerHTML=z;
}
function render(){
const r=current();if(!r)return;
let slider=byId("tick");slider.max=r.timeline.length-1;slider.value=Math.min(Number(slider.value),r.timeline.length-1);
const t=Number(slider.value),ev=r.timeline[t],selected=r.timeline.slice(0,t+1).map(x=>x.codelet).filter(Boolean);
byId("ticklabel").textContent=t+" / "+(r.timeline.length-1);
renderGeom(r,selected);
byId("groups").innerHTML=selected.map(s=>'<span class="group '+(["OPPOSITION_PAIR","SAS_TRIPLETS","HIGHER_GENERIC","TRANSFER_TENSION"].includes(s)?"analogy":"")+'">'+s.replaceAll("_"," ")+'</span>').join("")||'<small>Solo la costruzione CD; i codelets non hanno ancora selezionato gruppi.</small>';
const a=ev.macro_after;
byId("meters").innerHTML=Object.keys(a).map(key=>'<div class="meter"><span>'+key+'</span><div class="track"><div class="fill" style="width:'+(100*a[key]).toFixed(1)+'%"></div></div><span>'+(100*a[key]).toFixed(0)+'%</span></div>').join("");
byId("event").innerHTML= ev.codelet?
'<strong>'+ev.codelet+'</strong> · '+ev.description+'<br>Score '+ev.chosen_score.score+' · inherited '+ev.chosen_score.macro_inherited+' · temperature '+ev.temperature+'<br><small>'+ev.causal_chain.join(" → ")+'</small><br><small>Stato epistemico: '+ev.status+'</small>':
'<strong>CONSTRUCTION_CD</strong> · partizione angolare e incidenza sulla base; non è dimostrata alcuna uguaglianza dei segmenti.';
byId("trace").innerHTML=r.timeline.slice(0,t+1).map((e,i)=>'<div class="trace-row '+(i===t?"active":"")+'">'+i+'. '+(e.codelet||e.event)+(e.codelet?' · heat '+e.temperature+' · eredità '+e.chosen_score.macro_inherited:'')+'</div>').join("");
byId("m-op").textContent=selected.includes("OPPOSITION_PAIR")?"Sì":"No";
byId("m-sas").textContent=selected.includes("SAS_TRIPLETS")?"Sì":"No";
byId("m-gs").textContent=selected.filter(x=>["OPPOSITION_PAIR","DIVIDER_GENERIC","MULTIROLE_GENERIC","HIGHER_GENERIC"].includes(x)).length;
byId("m-false").textContent=r.metrics.false_certified_metric_equalities;
let mode=byId("mode").value;
byId("compare").innerHTML='<div class="summary">'+["bottom_up","top_down","reciprocal"].map(cond=>{
let a=DATA.aggregates[mode][cond];return '<div class="metric"><small>'+cond.replaceAll("_"," → ")+' ('+a.trials+' seed)</small><strong>'+Math.round(a.opposition_rate*100)+'%</strong><small>opposition · '+a.mean_cross_domain_groups.toFixed(2)+' cross-domain medi</small></div>'}).join("")+'</div>';
}
function updateRun(){byId("tick").value=8;render()}
["mode","condition","seed"].forEach(id=>byId(id).addEventListener("change",updateRun));
byId("tick").addEventListener("input",render);
render();
</script></body></html>"""


def main():
    traces = OUT / "traces.json"
    data = json.loads(traces.read_text(encoding="utf-8"))
    embedded = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    viewer = HTML.replace("__EMBED__", embedded)
    (OUT / "viewer.html").write_text(viewer, encoding="utf-8")
    lines = [
        "# Merovingio — Gestalt Heat v1: risultati eseguiti",
        "",
        "Simulazione con codelets manuali; no Jev, no training; non prova I.10.",
        "",
        "48 seed per condizione e per geometria; budget identico: " + str(data["budget"]) + " codelet ticks.",
        "",
        "| Geometria | Condizione | Opposizioni | Triplette SAS | Ipotesi transfer | Media gruppi cross-domain | Primo opposition tick (se trovato) |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for mode, conditions in data["aggregates"].items():
        for name, a in conditions.items():
            lines.append("| " + " | ".join([
                mode, name, str(a["opposition_rate"]), str(a["sas_rate"]),
                str(a["transfer_hypothesis_rate"]),
                str(a["mean_cross_domain_groups"]),
                str(a["mean_first_opposition_tick_given_found"])]) + " |")
    lines += ["", "## Epistemic boundary",
              "La costruzione garantisce la bisettrice; il target AD=DB? rimane HYPOTHESIS_ONLY.",
              "Il controllo scaleno testa che la bisettrice non autorizzi automaticamente la mediana.",
              "Zero certificazioni metriche effettuate dal motore.",
              "",
              "## Interpretazione corretta",
              "Le differenze misurano l'effetto *interno* di bias macro e feedback progettati nei codelets.",
              "Non sono evidenza che esseri umani o Euclide abbiano ragionato così.",
              "Vedere traces.json e viewer.html per score, stati, attivazioni e genealogie di ogni selezione.",
              ""]
    (OUT / "REPORT.md").write_text("\n".join(lines), encoding="utf-8")
    print("Generated", OUT / "viewer.html", "and", OUT / "REPORT.md")

if __name__ == "__main__":
    main()

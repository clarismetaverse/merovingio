#!/usr/bin/env python3
"""Standalone offline viewer for executed flat-angle regrouping v7 traces."""
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
OUT=HERE/"results"

PAGE=r"""<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Merovingio v7 · Flat-angle construction</title><style>
:root{font-family:Inter,ui-sans-serif,system-ui,sans-serif;color-scheme:dark}
*{box-sizing:border-box}body{margin:0;background:#11121c;color:#f3eefa}
header{background:#1d1c2c;padding:24px max(16px,calc((100vw - 1250px)/2));border-bottom:1px solid #443c58}
h1{font-size:25px;margin:6px 0 10px;letter-spacing:-.5px}h2{font-size:16px;margin:0 0 12px}h3{font-size:13px;margin:17px 0 7px}
.eyebrow{font-size:11px;font-weight:700;letter-spacing:1.5px;color:#b99bde}
p{font-size:12px;color:#b8b0c6;line-height:1.58}main{max-width:1250px;padding:16px;margin:auto;display:grid;gap:14px}
.panel{background:#1d1e2d;border:1px solid #424054;border-radius:13px;padding:15px;min-width:0}
.controls{display:flex;flex-wrap:wrap;gap:13px;align-items:end}
label{font-size:12px;color:#bcb4ce;display:flex;flex-direction:column;gap:6px}
select,input{background:#141625;border:1px solid #655e75;border-radius:7px;color:#f6f0fe;padding:8px;font:inherit}
input[type=range]{padding:0;width:170px;accent-color:#b8a0f0}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:15px}
svg{background:#151825;border-radius:9px;width:100%;display:block}
.metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}
.metric{background:#292739;border-radius:10px;padding:12px}
.metric small{font-size:10px;color:#b7aec8}.metric b{font-size:23px;color:#dec3ff;display:block}
.pill{padding:6px 8px;display:inline-block;border-radius:8px;font-size:11px;border:1px solid #77708e;margin:3px}
.pill.angle{border-color:#659fcd;color:#acd2f3}.pill.side{border-color:#d1a36d;color:#f0d4a4}.pill.gs{border-color:#86a88f;color:#b7dbbb}
.info{padding:12px;background:#2c2843;border-left:3px solid #b29bea;border-radius:8px;font-size:12px;line-height:1.6;min-height:88px}
.note{border:1px solid #8c7049;background:#322a24;color:#f0d6ae;border-radius:9px;font-size:12px;padding:11px;line-height:1.5}
.steps{max-height:270px;overflow:auto;display:grid;gap:6px}
.step{border:1px solid #484359;border-radius:8px;padding:8px;font-size:11px;color:#c6c0d4}
.step.now{border-color:#b9a0e9;background:#3c3152}
table{width:100%;border-collapse:collapse;font-size:11px}
th,td{text-align:left;padding:9px 8px;border-bottom:1px solid #484257}th{color:#d0c1e2}
@media(max-width:840px){.grid{grid-template-columns:1fr}.metrics{grid-template-columns:repeat(2,1fr)}}
</style></head><body><header><div class="eyebrow">MEROVINGIO · PANOPTIKON · EXPERIMENT V7</div>
<h1>Angolo piatto e REBASE della doppia partizione</h1>
<p>Un raggio incontra una retta: i settori angolari e le porzioni del segmento possono essere prodotti dallo stesso gesto. Esplora l'emergere dei Generic Spaces e confronta un'unica genealogia con due costruzioni indipendenti.</p></header>
<main><div class="panel controls">
<label>Figura<select id="scenario">
<option value="flat_ray">W1 · Angolo piatto + raggio</option>
<option value="crossed_lines">W2 · Retta completa + angoli opposti</option>
<option value="independent_partitions">Controllo · partizioni indipendenti</option>
</select></label>
<label>Strategia<select id="condition">
<option value="fixed_initial">Priorità statica</option>
<option value="topology_only">Solo topologia</option>
<option value="predictive_only">Produttività prevista</option>
<option value="productivity_feedback" selected>Produttività + feedback</option>
<option value="genealogy_blind">Genealogia attenuata</option>
</select></label>
<label>Attenzione<select id="attention">
<option value="clean">Lettura pulita</option>
<option value="competing" selected>Gruppi concorrenti</option>
</select></label>
<label>Seed<select id="seed"></select></label>
<label>Passaggio <span id="tick_label"></span><input id="tick" type="range" min="0" max="3" value="2"></label>
</div>
<div class="metrics">
<div class="metric"><small>Partizioni selezionate</small><b id="m1">0</b></div>
<div class="metric"><small>Generic incompleti</small><b id="m2">0</b></div>
<div class="metric"><small>Generic completati</small><b id="m3">0</b></div>
<div class="metric"><small>False uguaglianze</small><b id="m4">0</b></div>
</div>
<div class="grid"><div class="panel"><h2>Workspace materiale</h2><svg id="fig" viewBox="0 0 760 360"></svg>
<div id="family"></div><h3>Generic Spaces attivati</h3><div id="generics"></div>
<div class="note">Il completamento di un Generic Space indica una corrispondenza strutturale, NON una congruenza. Gli angoli opposti al vertice sono marcati come opposizioni materiali; nessuna uguaglianza metrica di segmenti viene certificata.</div></div>
<div class="panel"><h2>REBASE e feedback</h2><div class="info" id="event"></div>
<h3>Alternative disponibili prima del passaggio</h3>
<table><thead><tr><th>Partizione</th><th>Score</th><th>Prospettiva</th><th>Feedback</th></tr></thead><tbody id="options"></tbody></table>
<h3>Traccia delle riletture</h3><div class="steps" id="trace"></div>
</div></div>
<div class="panel"><h2>Confronto delle ablazioni eseguite</h2>
<table><thead><tr><th>Condizione</th><th>Completamento</th><th>Tick medio di completamento</th><th>Feedback medi</th><th>Riorganizzazioni</th></tr></thead><tbody id="summary"></tbody></table>
<p>La geometria resta costante fra strategie della stessa figura. La suite misura un motore con pesi progettati manualmente e riusati dalla v6; non dimostra una legge psicologica né un ragionamento storico di Euclide.</p></div></main>
<script type="application/json" id="data">__DATA__</script><script>
"use strict";
const DATA=JSON.parse(document.getElementById("data").textContent),$=id=>document.getElementById(id);
DATA.seeds.forEach(s=>{const o=document.createElement("option");o.value=s;o.textContent="Seed "+s;$("seed").appendChild(o)});
const current=()=>DATA.runs.find(x=>x.condition===$("condition").value&&x.scenario===$("scenario").value&&x.attention===$("attention").value&&x.seed===Number($("seed").value));
function seg(a,b,color="#bcb9cf",width=2.6,dash=false){return '<line x1="'+a[0]+'" y1="'+a[1]+'" x2="'+b[0]+'" y2="'+b[1]+'" stroke="'+color+'" stroke-width="'+width+'" stroke-linecap="round"'+(dash?' stroke-dasharray="6 6"':'')+'/>'}
function draw(x,e){
const p=x.geometry.points;
let paths=[["A","O"],["O","B"],["O","C"],["E","P"],["P","F"],["G","Q"],["Q","H"],["Q","I"]];
if(x.scenario==="crossed_lines")paths.push(["O","D"]);
if(x.scenario==="independent_partitions")paths.push(["J","R"],["R","K"]);
let out=paths.map(([u,v])=>seg(p[u],p[v],u==="O"||v==="O"?"#ad9fe2":"#767992",3)).join("");
const fam=e.selected_family;if(fam){
const hi=fam.kind==="ANGLE"?"#68b8d9":"#e2b878";
if(fam.kind==="SIDE"){for(let child of fam.children){const f=x.nodes[child];out+=seg(p[f.vertices[0]],p[f.vertices[1]],hi,7)}}
else{out+='<circle cx="'+p[fam.anchor][0]+'" cy="'+p[fam.anchor][1]+'" r="26" fill="none" stroke="'+hi+'" stroke-width="3"/>'}
}
let names=new Set(paths.flat());
for(const n of names){let v=p[n];out+='<circle cx="'+v[0]+'" cy="'+v[1]+'" r="4.2" fill="#eae7f1"/><text x="'+(v[0]+6)+'" y="'+(v[1]-9)+'" font-size="13" fill="#e8e4f0">'+n+'</text>'}
$("fig").innerHTML=out;
$("family").innerHTML=fam?'<span class="pill '+(fam.kind==="ANGLE"?"angle":"side")+'">'+fam.kind+' · '+fam.children.map(n=>x.nodes[n].label).join(" + ")+'</span>':'';
}
function render(){
const x=current();if(!x)return;
const slider=$("tick");slider.max=x.timeline.length-1;slider.value=Math.min(+slider.value,x.timeline.length-1);
const index=+slider.value,e=x.timeline[index],past=x.timeline.slice(0,index+1);
$("tick_label").textContent=index+"/"+(x.timeline.length-1);draw(x,e);
let gen=past.flatMap(y=>y.new_generic_events||[]);
$("m1").textContent=past.length;$("m2").textContent=gen.filter(y=>y.kind==="INCOMPLETE_GENERIC").length;
$("m3").textContent=gen.filter(y=>y.kind==="COMPLETED_GENERIC").length;$("m4").textContent=x.metrics.false_metric_certifications;
$("generics").innerHTML=gen.map(y=>'<span class="pill gs">'+y.kind+' · '+y.anchor+'</span>').join("")||'<span class="pill">Nessuno</span>';
$("event").innerHTML=e.operation==="REBASE_PARTITION"?
'<b>'+e.from+' → '+e.to+'</b>, partizione acquisita: '+e.selected_family.parent+'<br>Attenzione locale + genealogia: '+e.score_at_choice.topological+' + '+e.score_at_choice.genealogy+'<br>Produttività prevista: '+e.score_at_choice.prospective+'; feedback: '+e.score_at_choice.feedback+'<br>Nuovi Generic Spaces: '+e.new_generic_events.length+' · Riorganizzazione alternative: '+(e.relative_ranking_changed?"Sì":"No"):
'Costruzione iniziale: lettura angolare in O. Le due partizioni diventano candidati non equivalenze metriche.';
$("options").innerHTML=(e.available_scores?Object.values(e.available_scores):[]).sort((a,b)=>b.score-a.score).map(q=>{
let f=x.families.find(y=>y.id===q.id);return '<tr><td>'+f.kind+' · '+f.anchor+'</td><td>'+q.score+'</td><td>'+q.prospective+'</td><td>'+q.feedback+'</td></tr>'}).join("")||'<tr><td colspan="4">Primo raggruppamento in O</td></tr>';
$("trace").innerHTML=past.map((z,i)=>'<div class="step '+(i===index?"now":"")+'">'+i+'. '+z.operation+' · '+(z.selected_family?.kind||"")+" "+(z.selected_family?.anchor||"")+'</div>').join("");
$("summary").innerHTML=DATA.conditions.map(c=>{let a=DATA.aggregates[x.attention][x.scenario][c];return '<tr><td>'+c+'</td><td>'+Math.round(100*a.completion_rate)+'%</td><td>'+(a.first_completion_tick_if_found??'—')+'</td><td>'+a.mean_feedback_events+'</td><td>'+a.mean_reorderings+'</td></tr>'}).join("");
}
["condition","scenario","attention","seed"].forEach(id=>$(id).addEventListener("change",()=>{$("tick").value=2;render()}));
$("tick").addEventListener("input",render);render();
</script></body></html>"""


def main():
    data=json.loads((OUT/"traces.json").read_text(encoding="utf-8"))
    short={k:data[k] for k in ("schema","scenarios","conditions","attentions","aggregates")}
    short["seeds"]=data["seeds"][:10]
    short["runs"]=[r for r in data["runs"] if r["seed"] in short["seeds"]]
    embedded=json.dumps(short,ensure_ascii=False,separators=(",",":")).replace("</","<\\/")
    (OUT/"viewer.html").write_text(PAGE.replace("__DATA__",embedded),encoding="utf-8")
    lines=[
        "# Merovingio v7 — Flat-Angle & Medial Regrouping",
        "",
        "Generalization out of triangles: angle sector partitions and segment subdivisions are independently derived from oriented PART_OF graph relations.",
        "No shape-specific metric inference is authorized. Experimental salience uses frozen coefficients from v6.",
        "",
        "| Attention | Scenario | Strategy | n | Completion rate | First completion tick | Mean feedback events | False metric certificates | False genealogy pairings |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for attention,scenarios in data["aggregates"].items():
        for scenario,conditions in scenarios.items():
            for condition,a in conditions.items():
                lines.append("| "+" | ".join([
                    attention,scenario,condition,str(a["n"]),str(a["completion_rate"]),
                    str(a["first_completion_tick_if_found"]),str(a["mean_feedback_events"]),
                    str(a["false_metric_certifications"]),str(a["false_genealogy_pairings"])])+" |")
    lines+=["",
        "## Interpretation",
        "A completed Generic Space means a matched ANGLE and SIDE partition with identical causal root and material anchor.",
        "The independent control contains structurally similar angle/segment partitions at different points without that common genealogical root.",
        "Crossed lines add a second angular partition and two structural pairs of vertical opposite sectors. Their equality is not certified here.",
        "The model is an explicit cognitive *simulation* with hand-coded rules, not a demonstration of historical Euclidean discovery or human cognition.",
        "Do not interpret increases in completion rate as mathematical correctness: mathematical equality remains unasserted.",
        ""]
    (OUT/"REPORT.md").write_text("\n".join(lines),encoding="utf-8")
    print("Created",OUT/"viewer.html",OUT/"REPORT.md")


if __name__=="__main__":main()

#!/usr/bin/env python3
"""Build standalone interactive v3 timeline from executed, sanitized trace JSON."""
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
OUT=HERE/"results"
HTML=r"""<!doctype html><html lang="it"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Merovingio · Costruzione polisemica v3</title>
<style>
:root{color-scheme:dark;font-family:Inter,ui-sans-serif,system-ui,sans-serif;font-size:14px}
*{box-sizing:border-box}body{background:#12131d;color:#efecf7;margin:0}
header{padding:25px max(18px,calc((100vw - 1260px)/2));background:#1b1d2b;border-bottom:1px solid #3d3953}
h1{font-size:26px;letter-spacing:-.7px;margin:3px 0 6px}h2{font-size:16px;margin:0 0 14px}
p{color:#b0aabe;font-size:13px;line-height:1.6}.eyebrow{letter-spacing:1.8px;text-transform:uppercase;font-weight:700;font-size:11px;color:#bc9fee}
main{max-width:1260px;margin:auto;padding:16px;display:grid;gap:15px}
.panel{border:1px solid #414051;border-radius:14px;background:#1d1e2d;padding:16px;min-width:0}
.controls{display:flex;gap:13px;flex-wrap:wrap;align-items:end}
label{font-size:12px;display:flex;flex-direction:column;gap:6px;color:#b9b3ca}
select,input{font:inherit;color:#ece9fa;background:#121524;border:1px solid #625e73;padding:8px;border-radius:7px;max-width:230px}
input[type=range]{padding:0;width:190px;accent-color:#a991e2}
.columns{display:grid;grid-template-columns:1fr 1fr;gap:15px}
svg{display:block;width:100%;background:#151928;border-radius:11px}
.meter{display:grid;grid-template-columns:92px 1fr 45px;align-items:center;gap:10px;margin:12px 0;font-size:12px}
.bar{background:#313345;height:10px;overflow:hidden;border-radius:20px}.inner{background:linear-gradient(90deg,#777ce7,#cc93eb);height:100%}
.pill{padding:6px 9px;font-size:11px;background:#29273d;border:1px solid #615277;color:#e3d8f0;display:inline-flex;border-radius:9px;margin:4px}
.readings{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.reading{padding:12px;border-radius:11px;border:1px solid #45455b;background:#242739}
.reading.a{border-color:#598aae}.reading.s{border-color:#bb9766}
.reading b{display:block;font-size:12px;margin:0 0 6px}.reading span{font-size:12px;color:#b6b3c8}
.arrows{color:#af91dd;text-align:center;font-weight:700;padding:5px}
.event{padding:12px;background:#2b2840;border-left:3px solid #b59beb;min-height:100px;line-height:1.6;font-size:13px;border-radius:7px}
.trace{max-height:280px;overflow:auto;display:grid;gap:6px}
.step{border:1px solid #3c3850;border-radius:8px;padding:9px;color:#bcb5d0;font-size:11px}
.step.active{background:#3b3150;border-color:#c59aec;color:#fff}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}
.kpi{padding:13px;background:#272537;border-radius:12px}.kpi b{font-size:23px;color:#e0c4ff;display:block}.kpi small{font-size:11px;color:#a9a5b8}
table{border-collapse:collapse;width:100%;font-size:11px}td,th{text-align:left;padding:10px 8px;border-bottom:1px solid #494659}
th{color:#c5badb}.note{padding:12px;border-radius:10px;background:#312922;border:1px solid #8a714c;color:#e7cfae;font-size:12px;line-height:1.45}
@media(max-width:900px){.columns{grid-template-columns:1fr}.kpis{grid-template-columns:repeat(2,1fr)}.readings{grid-template-columns:1fr}}
</style></head>
<body><header><div class="eyebrow">Merovingio · Panoptikon · Gestalt Propagation v3</div>
<h1>La costruzione come dispositivo polisemico</h1>
<p>Un medesimo termine medio CD produce simultaneamente partizioni angolari, segmentali, sottoregioni e opposizioni. La Slipnet può seguire la loro genealogia comune e propagare la tensione analogica.</p></header>
<main><div class="panel controls">
<label>Condizione<select id="condition">
<option value="no_macro">A · Solo grafo</option>
<option value="macro_only">B · Macro senza genealogia</option>
<option value="cogeneration_only">C · Solo co-origine</option>
<option value="coupled" selected>D · Macro + co-origine + feedback</option>
<option value="genealogy_blinded">E · Genealogia cieca, feedback attivo</option>
</select></label>
<label>Figura<select id="mode"><option value="isosceles">Isoscele</option><option value="scalene">Scaleno con bisettrice</option><option value="ordinary_cevian">Trasversale senza bisettrice</option></select></label>
<label>Seed<select id="seed"></select></label>
<label>Passaggio <span id="tick-label"></span><input type="range" min="0" max="18" value="8" id="tick"></label>
</div>
<div class="kpis">
<div class="kpi"><small>Termine medio</small><b>CD</b></div>
<div class="kpi"><small>Co-frame emerso</small><b id="k-co">—</b></div>
<div class="kpi"><small>Rebase opposizioni</small><b id="k-re">—</b></div>
<div class="kpi"><small>Ipotesi angoli → lati</small><b id="k-hy">—</b></div>
</div>
<div class="columns">
<div class="panel"><h2>Un evento, molte letture</h2>
<svg viewBox="0 0 610 405" id="diagram"></svg>
<div class="arrows">↕ C / CD / D : lo stesso termine medio</div>
<div class="readings"><div class="reading a"><b>ANGLE SPACE</b><span id="angle-read"></span></div>
<div class="reading s"><b>SIDE SPACE</b><span id="side-read"></span></div></div>
<h2 style="margin-top:17px">Interpretazione attiva</h2><div id="group"></div>
<div class="note">Partizione e co-origine non implicano uguaglianza delle parti. ∠ACD = ∠DCB è dato soltanto quando CD è una bisettrice. AD = DB rimane una domanda analogica, non una conclusione.</div>
</div>
<div class="panel"><h2>Attivazione Slipnet</h2><div id="meters"></div>
<h2 style="margin-top:18px">Codelet ed effetto cognitivo</h2><div id="event" class="event"></div>
<h2 style="margin-top:18px">Traccia della co-generazione</h2><div id="trace" class="trace"></div>
</div></div>
<div class="panel"><h2>Ablazioni · statistiche realmente eseguite</h2><table><thead><tr><th>Condizione</th><th>Co-frame</th><th>Rebase</th><th>Domanda angoli → lati</th><th>Gruppi cross-domain</th></tr></thead><tbody id="aggregates"></tbody></table>
<p>Le differenze rappresentano gli effetti di incentivi codificati a mano, non osservazioni cognitive umane né risultati di Jev. Il controllo con trasversale generica deve impedire un trasferimento che richieda uguaglianza angolare non data.</p></div>
</main><script id="data" type="application/json">__DATA__</script><script>
"use strict";
const data=JSON.parse(document.getElementById("data").textContent);
const $=id=>document.getElementById(id);
for(const n of data.seeds){const el=document.createElement("option");el.value=n;el.textContent="Seed "+n;$("seed").append(el)}
function getRun(){return data.runs.find(r=>r.condition===$("condition").value&&r.mode===$("mode").value&&r.seed===Number($("seed").value))}
function segment(a,b,color,w=3,dash=false){return '<line x1="'+a[0]+'" y1="'+a[1]+'" x2="'+b[0]+'" y2="'+b[1]+'" stroke="'+color+'" stroke-width="'+w+'"'+(dash?' stroke-dasharray="6 4"':'')+' stroke-linecap="round"/>'}
function text(x,y,s,color="#e9e6f5"){return '<text x="'+x+'" y="'+y+'" font-size="16" fill="'+color+'">'+s+'</text>'}
function draw(r,step){const p=r.geometry.points;let a=p.A,b=p.B,c=p.C,d=p.D;
let svg='<polygon points="'+[a,c,d].map(x=>x.join(",")).join(" ")+'" fill="#547999" opacity=".12"/><polygon points="'+[b,c,d].map(x=>x.join(",")).join(" ")+'" fill="#d5a160" opacity=".12"/>';
svg+=segment(a,b,"#d9d4ee",3)+segment(a,c,"#d9d4ee")+segment(b,c,"#d9d4ee")+segment(c,d,"#bd99ed",5);
if(step.new_group){let g=step.new_group;if(["COFRAME","REBASE"].includes(g.operator)){svg+=segment(a,d,"#e2b375",6)+segment(b,d,"#5eafc7",6)}}
for(const [n,q] of Object.entries(p)){svg+='<circle cx="'+q[0]+'" cy="'+q[1]+'" r="5" fill="#eeeaf5"/>'+text(q[0]+8,q[1]-10,n)}
$("diagram").innerHTML=svg}
function render(){const r=getRun();if(!r)return;const control=$("tick");control.max=r.timeline.length-1;control.value=Math.min(+control.value,r.timeline.length-1);let tick=+control.value,ev=r.timeline[tick];
$("tick-label").textContent=tick+" / "+(r.timeline.length-1);
draw(r,ev);
const packet=r.construction_packets[0];
$("angle-read").textContent=packet?packet.angular_partition.children.map(x=>r.graph.nodes[x].label).join(" ↔ "):"Nessun gruppo";
$("side-read").textContent=packet?packet.segment_partition.children.map(x=>r.graph.nodes[x].label).join(" ↔ "):"Nessun gruppo";
const past=r.timeline.slice(0,tick+1);
$("k-co").textContent=past.some(x=>x.operation==="COFRAME")?"Sì":"No";
$("k-re").textContent=past.some(x=>x.operation==="REBASE")?"Sì":"No";
$("k-hy").textContent=past.some(x=>x.new_analogical_hypothesis)?"Sì":"No";
$("meters").innerHTML=Object.entries(ev.macro_after).map(([name,val])=>'<div class="meter"><span>'+name+'</span><div class="bar"><div class="inner" style="width:'+(val*100).toFixed(1)+'%"></div></div><span>'+Math.round(val*100)+'%</span></div>').join("");
const g=ev.new_group;
$("group").innerHTML=g?g.objects.map(x=>'<span class="pill">'+(r.graph.nodes[x]?.label??x)+'</span>').join(""):'<span class="pill">Prima della selezione: co-generazione disponibile</span>';
$("event").innerHTML=g?'<b>'+ev.operation+'</b> · '+g.relation_types.join(", ")+'<br><small>Score '+ev.score+' · eredità macro '+ev.macro_inherited+' · frontiera '+ev.frontier_size+'</small><br><small>'+ev.cause.join(" → ")+'</small>'+(ev.new_analogical_hypothesis?'<br><b>Ipotesi: trasferimento dall’uguaglianza angolare ai lati opposti · NON DIMOSTRATO</b>':''):
'<b>COSTRUZIONE</b> · '+ev.material_delta.new_objects+' nuovi oggetti; '+ev.material_delta.new_relations+' relazioni. Due partizioni con la stessa origine, prima di ogni raggruppamento.';
$("trace").innerHTML=past.map((e,i)=>'<div class="step '+(i===tick?'active':'')+'">'+i+'. '+e.operation+(e.new_group?' · '+e.new_group.relation_types.join(", "):'')+(e.score_sources?' · co-origine '+e.score_sources.construction_genealogy:'')+'</div>').join("");
const agg=data.aggregates[r.mode];$("aggregates").innerHTML=data.conditions.map(c=>{let a=agg[c];return '<tr><td>'+c+'</td><td>'+Math.round(a.coframe_rate*100)+'%</td><td>'+Math.round(a.rebasing_rate*100)+'%</td><td>'+Math.round(a.transfer_question_rate*100)+'%</td><td>'+a.mean_cross_domain_groups+'</td></tr>'}).join("");
}
for(const id of ["condition","mode","seed"]){$(id).addEventListener("change",()=>{$("tick").value=8;render()})}
$("tick").addEventListener("input",render);render();
</script></body></html>"""


def main():
    data=json.loads((OUT/"traces.json").read_text(encoding="utf-8"))
    small={k:data[k] for k in ("schema","conditions","modes","aggregates")}
    small["seeds"]=data["seeds"][:8]
    small["runs"]=[r for r in data["runs"] if r["seed"] in small["seeds"]]
    embedded=json.dumps(small,ensure_ascii=False,separators=(",",":")).replace("</","<\\/")
    (OUT/"viewer.html").write_text(HTML.replace("__DATA__",embedded),encoding="utf-8")
    lines=[
      "# Merovingio · v3 · co-generazione porismatica",
      "",
      "Esperimento eseguito sulla grammatica del grafo. Non una ricostruzione storica di Euclide, non una prova, non Jev.",
      "",
      "| Geometria | Condizione | Seed | Co-frame | Rebase | Domanda trasferimento | Cross-domain medi |",
      "|---|---|---:|---:|---:|---:|---:|"]
    for mode,cond in data["aggregates"].items():
        for name,a in cond.items():
            lines.append("| "+" | ".join([mode,name,str(a["n"]),str(a["coframe_rate"]),
                str(a["rebasing_rate"]),str(a["transfer_question_rate"]),
                str(a["mean_cross_domain_groups"])])+" |")
    lines+=["",
      "## Cosa misura",
      "L'evento costruttivo può generare due partizioni con un carrier materiale e un punto d'incidenza comuni.",
      "Un COFRAME stabilizzato può in seguito rendere disponibile un REBASE fra opposizioni lato-angolo.",
      "La genealogia della costruzione fornisce un ulteriore canale di propagazione salienziale, separato dalla metrica.",
      "Il numero di candidati co-generati è lo stesso nelle ablazioni; cambia la probabilità che vengano esplorati.",
      "",
      "## Limiti",
      "Gli operatori COFRAME/REBASE e i loro punteggi sono progettati. Il vantaggio atteso non è apprendimento emergente spontaneo.",
      "Un accordo della simulazione con l'intuizione è supporto ingegneristico, non validazione cognitiva o storica.",
      "La relazione AD = DB non è mai certificata dal motore; in scaleno resta in generale falsa.",
      "La trasversale generica senza dato di uguaglianza angolare può co-generare ma non autorizza la stessa domanda orientata.",
      ""]
    (OUT/"REPORT.md").write_text("\n".join(lines),encoding="utf-8")
    print("Created",OUT/"viewer.html",OUT/"REPORT.md")
if __name__=="__main__": main()

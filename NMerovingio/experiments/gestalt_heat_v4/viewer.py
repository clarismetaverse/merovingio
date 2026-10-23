#!/usr/bin/env python3
"""Standalone v4 trace explorer. All data derives from executed Python runs."""
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
OUT=HERE/"results"
HTML=r"""<!doctype html><html lang="it"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Merovingio v4 · Recursive Opposition REBASE</title>
<style>
:root{font-family:Inter,ui-sans-serif,system-ui,sans-serif;color-scheme:dark}
*{box-sizing:border-box}body{background:#11131d;color:#f2edf8;margin:0}
header{padding:25px max(18px,calc((100vw - 1200px)/2));background:#1a1b2b;border-bottom:1px solid #403a50}
.eyebrow{color:#bba1ed;letter-spacing:1.6px;text-transform:uppercase;font-size:11px;font-weight:700}
h1{font-size:27px;margin:5px 0 10px}h2{font-size:16px;margin:0 0 15px}h3{font-size:13px;margin:13px 0 6px}
p{font-size:13px;color:#b4aec5;line-height:1.6}main{padding:17px;max-width:1200px;margin:0 auto;display:grid;gap:16px}
.panel{background:#1d1f2e;border:1px solid #424056;border-radius:13px;padding:16px;min-width:0}
.controls{display:flex;flex-wrap:wrap;gap:15px;align-items:end}label{font-size:12px;color:#c2bacf;display:flex;flex-direction:column;gap:6px}
select,input{background:#121626;border:1px solid #656078;border-radius:8px;color:#f2ecfa;padding:9px;font:inherit}
input[type=range]{width:170px;accent-color:#b29cfa;padding:0}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:14px}
svg{width:100%;background:#131928;border-radius:10px}
.anchor{display:flex;gap:8px;flex-wrap:wrap}.pill{border-radius:8px;border:1px solid #666076;padding:7px 9px;font-size:11px;background:#2b293d;margin:3px 0}
.pill.a{border-color:#5485b2;color:#b1d9fd}.pill.s{border-color:#ad8554;color:#ffe0ad}
.timeline{max-height:360px;overflow:auto;display:grid;gap:6px}
.event{border-radius:8px;border:1px solid #3a3951;padding:9px;color:#c5bdd5;font-size:11px}
.event.focus{border-color:#bd9bea;background:#342d48;color:#fff}
.info{padding:12px;border-left:3px solid #b8a0ed;border-radius:7px;background:#292640;font-size:12px;line-height:1.65;min-height:95px}
.meter{display:grid;grid-template-columns:85px 1fr 35px;gap:10px;align-items:center;font-size:11px;margin:9px 0}
.track{height:8px;border-radius:12px;background:#333345;overflow:hidden}.fill{height:100%;background:linear-gradient(90deg,#638ab9,#c89bdd)}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}
.kpi{background:#242536;border-radius:10px;padding:13px}.kpi small{font-size:10px;color:#b4aac7}.kpi b{display:block;font-size:22px;color:#e1c8ff}
.witness{font-size:12px;padding:7px 8px;border-radius:7px;margin:4px 4px 4px 0;display:inline-flex;border:1px solid #525773;background:#2b2c41}
.question{color:#f0d6b0;background:#342c25;border:1px solid #735e44;border-radius:9px;padding:12px;font-size:12px;line-height:1.5}
table{border-collapse:collapse;width:100%;font-size:11px}
td,th{text-align:left;padding:10px 7px;border-bottom:1px solid #45445b}th{color:#d3c6e5}
@media(max-width:850px){.grid{grid-template-columns:1fr}.kpis{grid-template-columns:repeat(2,1fr)}}
</style></head><body><header><div class="eyebrow">Panoptikon / Merovingio · Cognitive Experiment v4</div>
<h1>REBASE ricorsivo delle opposizioni angolo–lato</h1>
<p>Ogni passaggio cambia il dominio in primo piano, preserva il mapping e incorpora una nuova evidenza del grafo. Il ritorno non cancella la lettura precedente: accumula supporti interpretativi.</p>
</header><main>
<div class="panel controls">
<label>Condizione<select id="condition">
<option value="no_pressure">Solo opportunità strutturali</option>
<option value="macro_only">Solo tensione macro</option>
<option value="genealogy_only">Solo co-origine</option>
<option value="recursive_coupled" selected>Macro + genealogia + feedback</option>
<option value="recursive_genealogy_blind">Feedback, genealogia oscurata</option>
<option value="one_way">Solo angoli → lati, no ritorno</option>
</select></label>
<label>Costruzione<select id="mode"><option value="isosceles">Isoscele + bisettrice</option><option value="scalene">Scaleno + bisettrice</option><option value="ordinary_cevian">Trasversale generica</option></select></label>
<label>Seed<select id="seed"></select></label>
<label>Passaggio <span id="step"></span><input type="range" id="tick" min="0" value="3"></label>
</div>
<div class="kpis">
<div class="kpi"><small>REBASE effettuati</small><b id="k1">—</b></div>
<div class="kpi"><small>Ritorni che aggiungono evidenza</small><b id="k2">—</b></div>
<div class="kpi"><small>Supporti distinti acquisiti</small><b id="k3">—</b></div>
<div class="kpi"><small>Ipotesi uguaglianza lati?</small><b id="k4">—</b></div>
</div>
<div class="grid">
<div class="panel"><h2>Uno stesso CD, letture alternate</h2>
<svg id="fig" viewBox="0 0 610 398"></svg>
<div class="anchor"><span class="pill a">ANGLE: <span id="angs"></span></span><span class="pill s">SIDE: <span id="sides"></span></span></div>
<h3>Evidenze incorporate fino a questo momento</h3><div id="evidence"></div>
<div class="question">La relazione angolare nota può originare una <b>domanda</b> sul lato opposto, non una sua certificazione. L'eguaglianza AD = DB non viene mai assunta in uno scaleno e nessun REBASE usa il criterio di congruenza dei triangoli.</div>
</div>
<div class="panel"><h2>Pressione e feedback</h2><div id="meters"></div>
<h3>Evento corrente</h3><div id="detail" class="info"></div>
<h3>Storia interpretativa</h3><div id="events" class="timeline"></div>
</div>
</div>
<div class="panel"><h2>Risultati delle ablazioni su tutti i seed</h2>
<table><thead><tr><th>Condizione</th><th>Loop ricorsivi</th><th>REBASE medi</th><th>Nuovi supporti</th><th>Domande medie sui lati</th></tr></thead><tbody id="stats"></tbody></table>
<p>Questo esperimento misura un sistema artificiale di riletture. I concetti, il punteggio di salienza e la probabilità di interrompere la ricerca sono programmati, non appresi da osservazioni umane.</p></div>
</main>
<script type="application/json" id="data">__DATA__</script><script>
"use strict";
const data=JSON.parse(document.getElementById("data").textContent),$=id=>document.getElementById(id);
data.seeds.forEach(s=>{let o=document.createElement("option");o.textContent="Seed "+s;o.value=s;$("seed").appendChild(o)});
function selection(){return data.runs.find(r=>r.mode===$("mode").value&&r.condition===$("condition").value&&r.seed===Number($("seed").value))}
function line(a,b,c,w=3){return '<line x1="'+a[0]+'" y1="'+a[1]+'" x2="'+b[0]+'" y2="'+b[1]+'" stroke="'+c+'" stroke-width="'+w+'" stroke-linecap="round"/>'}
function circle(p,l){return '<circle cx="'+p[0]+'" cy="'+p[1]+'" r="4" fill="#f8efff"/><text x="'+(p[0]+9)+'" y="'+(p[1]-9)+'" fill="#f0e8fc" font-size="16">'+l+'</text>'}
function diagram(run,ev){let p=run.geometry.points,a=p.A,b=p.B,c=p.C,d=p.D;
let s='<polygon points="'+[a,c,d].map(x=>x.join(",")).join(" ")+'" fill="#539aba" fill-opacity=".12"/><polygon points="'+[b,c,d].map(x=>x.join(",")).join(" ")+'" fill="#cca05a" fill-opacity=".12"/>';
s+=line(a,c,"#d9d6ed")+line(b,c,"#d9d6ed")+line(a,b,"#d9d6ed")+line(c,d,"#bb99ea",5);
if(ev.focus==="SIDE"){s+=line(a,d,"#e5b471",6)+line(d,b,"#60b6c3",6)}
else{s+='<circle cx="'+c[0]+'" cy="'+c[1]+'" r="27" stroke="#6bb8d5" stroke-width="4" fill="none" opacity=".7"/>'}
for(let [n,q] of Object.entries(p))s+=circle(q,n);
$("fig").innerHTML=s;
}
function render(){let r=selection();if(!r)return;let ctl=$("tick");ctl.max=r.timeline.length-1;ctl.value=Math.min(Number(ctl.value),r.timeline.length-1);
let index=Number(ctl.value),e=r.timeline[index];$("step").textContent=index+"/"+(r.timeline.length-1);diagram(r,e);
$("angs").textContent=r.mapping.angle_pair.map(x=>r.graph.nodes[x].label).join(" / ");
$("sides").textContent=r.mapping.side_pair.map(x=>r.graph.nodes[x].label).join(" / ");
let hist=r.timeline.slice(0,index+1);
$("k1").textContent=hist.filter(x=>x.event==="REBASE_OPPOSITION").length;
$("k2").textContent=hist.filter(x=>x.return_to_prior_focus).length;
$("k3").textContent=e.acquired_witnesses.length;
$("k4").textContent=hist.some(x=>x.analogical_question)?"Formulata":"No";
$("evidence").innerHTML=e.acquired_witnesses.map(w=>'<span class="witness">'+w.replaceAll("_"," ").replaceAll(":"," · ")+'</span>').join("");
$("meters").innerHTML=Object.entries(e.activation_after).map(([k,v])=>'<div class="meter"><span>'+k+'</span><div class="track"><div class="fill" style="width:'+(100*v)+'%"></div></div><span>'+Math.round(v*100)+'%</span></div>').join("");
$("detail").innerHTML=e.event==="REBASE_OPPOSITION"?
'<b>'+e.direction+'</b> · nuovo supporto: '+e.new_witness.name+'<br>Probabilità selezione '+e.rebase_probability+' · temperatura '+e.temperature+'<br>Origine: '+e.provenance_chain.join(" → ")+(e.analogical_question?'<br><b>Proiezione di uguaglianza = sola ipotesi!</b>':''):
e.event==="ATTENTION_STABILIZES"?'La ricerca si arresta prima del REBASE '+e.proposed_direction+'. Possibile supporto: '+e.candidate_witness+'.':
'Costruzione CD, lettura angolare iniziale e mapping di opposizioni dalla figura.';
$("events").innerHTML=hist.map((x,i)=>'<div class="event '+(i===index?'focus':'')+'">'+i+'. '+x.event+(x.direction?' · '+x.direction:'')+(x.new_witness?' · '+x.new_witness.name:'')+'</div>').join("");
let a=data.aggregates[r.mode];$("stats").innerHTML=data.conditions.map(c=>{let z=a[c];return '<tr><td>'+c+'</td><td>'+Math.round(100*z.loop_rate)+'%</td><td>'+z.mean_rebases+'</td><td>'+z.mean_novel_supports+'</td><td>'+z.mean_questions+'</td></tr>'}).join("");
}
for(let id of ["mode","condition","seed"])$(id).addEventListener("change",()=>{$("tick").value=3;render()});
$("tick").addEventListener("input",render);render();
</script></body></html>"""


def main():
    data=json.loads((OUT/"traces.json").read_text(encoding="utf-8"))
    short={k:data[k] for k in ("schema","modes","conditions","aggregates")}
    short["seeds"]=data["seeds"][:16]
    short["runs"]=[r for r in data["runs"] if r["seed"] in short["seeds"]]
    raw=json.dumps(short,ensure_ascii=False,separators=(",",":")).replace("</","<\\/")
    (OUT/"viewer.html").write_text(HTML.replace("__DATA__",raw),encoding="utf-8")
    lines=["# Merovingio v4 · REBASE ricorsivo delle opposizioni angolo–lato","",
        "Il REBASE può alternare le interpretazioni del medesimo mapping mantenendo le relazioni precedenti. Ogni REBASE incorpora almeno un nuovo witness strutturale dal grafo; quando le novità finiscono il ciclo si arresta.","",
        "Non è una dimostrazione geometrica né un esperimento su soggetti umani.","",
        "| Geometria | Condizione | Seed | Loop (%) | REBASE medi | Nuovi supporti | Domande medie |",
        "|---|---|---:|---:|---:|---:|---:|"]
    for m,cs in data["aggregates"].items():
        for c,a in cs.items():
            lines.append("| "+" | ".join((m,c,str(a["n"]),str(round(a["loop_rate"]*100,2)),
                str(a["mean_rebases"]),str(a["mean_novel_supports"]),str(a["mean_questions"])))+" |")
    lines+=["","## Confini epistemici","Il trasferimento di uguaglianza angolare verso i segmenti resta sempre una domanda, mai un teorema.",
        "Nel caso della trasversale generica non vi è relazione angolare di uguaglianza di partenza.",
        "I supporti vengono letti da relazioni materialmente presenti e da una sola genealogia di costruzione.",
        "Non esistono REBASE di triangoli in questa versione: tutti i passaggi attraversano opposizioni lato-angolo.",
        "Le probabilità di continuazione e le attivazioni sono stati progettati manualmente, non appresi.",
        ""]
    (OUT/"REPORT.md").write_text("\n".join(lines),encoding="utf-8")
    print("Created",OUT/"viewer.html",OUT/"REPORT.md")

if __name__=="__main__":main()

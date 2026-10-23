#!/usr/bin/env python3
"""Build offline v5 explorer from actually executed graph-rebase simulations."""
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
OUT=HERE/"results"
PAGE=r"""<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Merovingio — Dynamic Opposition REBASE v5</title>
<style>
:root{font-family:Inter,ui-sans-serif,system-ui,sans-serif;color-scheme:dark}
*{box-sizing:border-box}body{margin:0;background:#10131c;color:#eeeaf6}
header{padding:24px max(18px,calc((100vw - 1250px)/2));background:#191b29;border-bottom:1px solid #3a3853}
h1{font-size:26px;letter-spacing:-.5px;margin:5px 0}h2{font-size:16px;margin:0 0 12px}
p{font-size:13px;color:#b4b1c7;line-height:1.55}.eyebrow{font-size:11px;letter-spacing:1.7px;color:#c5aced;font-weight:700}
main{display:grid;gap:15px;max-width:1250px;margin:auto;padding:18px}
.panel{border:1px solid #403c54;background:#1b1e2d;border-radius:13px;padding:16px;min-width:0}
.controls{display:flex;flex-wrap:wrap;gap:14px;align-items:end}
label{font-size:12px;color:#c5bdd3;display:flex;flex-direction:column;gap:6px}
select,input{background:#121624;border:1px solid #696379;color:#f4edfc;border-radius:8px;padding:9px;font:inherit}
input[type=range]{width:170px;accent-color:#ad92f4;padding:0}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:15px}
svg{width:100%;background:#141728;border-radius:11px;display:block}
.metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}
.metric{border-radius:10px;background:#282738;padding:12px}.metric b{font-size:22px;display:block;color:#e4caff}
.metric small{font-size:11px;color:#b7b2ca}
.pill{padding:7px 9px;border:1px solid #65597e;background:#312b43;border-radius:9px;font-size:11px;display:inline-block;margin:3px}
.pill.a{border-color:#6088b9}.pill.s{border-color:#d0a562}
.meter{display:grid;grid-template-columns:91px 1fr 40px;align-items:center;gap:9px;font-size:11px;margin:9px 0}
.track{height:9px;background:#343646;border-radius:20px;overflow:hidden}
.fill{height:100%;background:linear-gradient(90deg,#7791cb,#ba92e3)}
.event{padding:12px;background:#262944;border-left:3px solid #b89cef;border-radius:8px;font-size:12px;line-height:1.6}
table{border-collapse:collapse;width:100%;font-size:11px}th,td{text-align:left;padding:8px;border-bottom:1px solid #444153}
th{color:#c5bade}
.notes{background:#322922;border:1px solid #766048;color:#edd1ac;border-radius:9px;font-size:12px;line-height:1.5;padding:12px}
.trace{max-height:240px;overflow:auto;display:grid;gap:5px}
.entry{background:#28283b;border:1px solid #3d3c55;border-radius:6px;padding:8px;font-size:11px}
.entry.now{border-color:#b9a2ee;color:white}
@media(max-width:850px){.grid{grid-template-columns:1fr}.metrics{grid-template-columns:repeat(2,1fr)}}
</style></head><body><header><div class="eyebrow">PANOPTIKON · MEROVINGIO · V5</div>
<h1>REBASE dinamico: quali opposizioni diventano salienti?</h1>
<p>Il dominio angoli/lati cambia ad ogni passaggio, ma la prossima opposizione viene selezionata fra tutte quelle ancora disponibili. Ogni nuova lettura può riordinare le alternative.</p></header>
<main>
<div class="panel controls">
<label>Condizione<select id="condition">
<option value="fixed_order">A · Ranking fisso</option>
<option value="local_only">B · Diffusione locale</option>
<option value="macro_no_feedback">C · Macro + genealogia, senza feedback</option>
<option value="macro_no_genealogy">D · Macro + feedback, senza genealogia</option>
<option value="coupled" selected>E · Macro + genealogia + feedback</option>
</select></label>
<label>Geometria<select id="mode"><option value="isosceles">Isoscele con bisettrice</option><option value="scalene">Scaleno con bisettrice</option><option value="ordinary_cevian">Trasversale generica</option></select></label>
<label>Seed<select id="seed"></select></label>
<label>Passaggio <span id="step"></span><input type="range" id="tick" min="0" value="4"></label>
</div>
<div class="metrics">
<div class="metric"><small>Opposizioni lette</small><b id="k1">—</b></div>
<div class="metric"><small>Generic Spaces candidati</small><b id="k2">—</b></div>
<div class="metric"><small>Riorganizzazioni ranking</small><b id="k3">—</b></div>
<div class="metric"><small>Ipotesi angoli → lati?</small><b id="k4">—</b></div>
</div>
<div class="grid">
<div class="panel"><h2>Figura e opposizione selezionata</h2>
<svg id="figure" viewBox="0 0 610 400"></svg>
<div id="role"></div>
<h2 style="margin-top:20px">Attivazioni dei macroconcetti</h2><div id="macro"></div>
<div class="notes">Il REBASE non autorizza la congruenza AD = DB. La bisettrice certifica solo l'uguaglianza angolare; l'eventuale trasferimento resta HYPOTHESIS_ONLY. La trasversale arbitraria non offre neppure questa sorgente.</div>
</div>
<div class="panel"><h2>Ricalcolo dinamico</h2><div class="event" id="detail"></div>
<h2 style="margin-top:18px">Alternative al prossimo passaggio</h2>
<table><thead><tr><th>Opposizione candidata</th><th>Score</th><th>Attivazione locale</th><th>Genealogia</th></tr></thead><tbody id="candidates"></tbody></table>
<h2 style="margin-top:18px">Sequenza delle riletture</h2><div class="trace" id="trace"></div>
</div>
</div>
<div class="panel"><h2>Statistiche delle ablazioni</h2><table><thead><tr><th>Condizione</th><th>Ipotesi trovata</th><th>Generic Spaces medi</th><th>Riorganizzazioni medie</th><th>Opposizioni lette</th></tr></thead><tbody id="summary"></tbody></table>
<p>I candidati sono derivati dal grafo, ma la diffusione e i pesi sono progettati, non addestrati. Le percentuali descrivono la simulazione, non la cognizione umana o il ragionamento storico di Euclide.</p></div>
</main><script type="application/json" id="data">__DATA__</script><script>
"use strict";
const D=JSON.parse(document.getElementById("data").textContent),$=id=>document.getElementById(id);
D.seeds.forEach(s=>{let o=document.createElement("option");o.value=s;o.textContent="Seed "+s;$("seed").append(o)});
function cur(){return D.runs.find(r=>r.condition===$("condition").value&&r.mode===$("mode").value&&r.seed===Number($("seed").value))}
function line(a,b,color,w=3){return '<line x1="'+a[0]+'" y1="'+a[1]+'" x2="'+b[0]+'" y2="'+b[1]+'" stroke="'+color+'" stroke-width="'+w+'" stroke-linecap="round"/>'}
function dot(p,name){return '<circle cx="'+p[0]+'" cy="'+p[1]+'" r="4.5" fill="#f1eff7"/><text x="'+(p[0]+9)+'" y="'+(p[1]-10)+'" fill="#f3efff" font-size="16">'+name+'</text>'}
function geometry(r,e){
let p=r.geometry.points,a=p.A,b=p.B,c=p.C,d=p.D;
let out='<polygon points="'+[a,c,d].map(x=>x.join(",")).join(" ")+'" fill="#4e91b0" opacity=".12"/><polygon points="'+[b,c,d].map(x=>x.join(",")).join(" ")+'" fill="#cf9a54" opacity=".12"/>';
out+=line(a,b,"#ddd7ef")+line(a,c,"#ddd7ef")+line(b,c,"#ddd7ef")+line(c,d,"#bb9ce8",4);
let obj=e.selected?.new_opposition_edge;
if(obj){let s=r.graph.nodes[obj.side],an=r.graph.nodes[obj.angle];
out+=line(p[s.vertices[0]],p[s.vertices[1]],"#dda968",6);
let q=p[an.vertex];out+='<circle cx="'+q[0]+'" cy="'+q[1]+'" r="23" fill="none" stroke="#69bbd1" stroke-width="3"/>';
}
for(const [n,q]of Object.entries(p))out+=dot(q,n);
$("figure").innerHTML=out;
$("role").innerHTML=obj?'<span class="pill a">'+r.graph.nodes[obj.angle].label+'</span> ↔ <span class="pill s">'+r.graph.nodes[obj.side].label+'</span>':'<span class="pill">Costruzione e attenzione angolare iniziale</span>'}
function render(){
let r=cur();if(!r)return;let ctl=$("tick");ctl.max=r.timeline.length-1;ctl.value=Math.min(+ctl.value,r.timeline.length-1);
let tick=+ctl.value,e=r.timeline[tick],steps=r.timeline.slice(1,tick+1);
$("step").textContent=tick+"/"+(r.timeline.length-1);geometry(r,e);
$("k1").textContent=steps.length;
let gens=steps.flatMap(x=>x.new_generics||[]);
$("k2").textContent=gens.length;
$("k3").textContent=steps.filter(x=>x.relative_rank_changed_by_new_group).length;
$("k4").textContent=steps.some(x=>(x.new_questions||[]).length)?"Sì":"No";
$("macro").innerHTML=Object.entries(e.macro_after).map(([key,value])=>'<div class="meter"><span>'+key+'</span><div class="track"><div class="fill" style="width:'+(100*value).toFixed(1)+'%"></div></div><span>'+Math.round(100*value)+'%</span></div>').join("");
$("detail").innerHTML=e.operation==="OPPOSITION_REBASE"?
'<strong>'+e.from+' → '+e.to+'</strong>, nuova opposizione: '+r.graph.nodes[e.selected.new_opposition_edge.angle].label+' ↔ '+r.graph.nodes[e.selected.new_opposition_edge.side].label+'<br>Score '+e.selected_score.score+'; locale '+e.selected_score.local_support+'; macro '+e.selected_score.macro_support+'; genealogia '+e.selected_score.coorigin_support+'<br><b>Le nuove attivazioni hanno cambiato l’ordine dei candidati? '+(e.relative_rank_changed_by_new_group?"Sì":"No")+'</b><br>Nuovi Generic Spaces: '+e.new_generics.length+'; domande di trasferimento: '+e.new_questions.length:
'CONSTRUCTION: i due angoli e i termini medi sono disponibili. La ricerca parte senza alcun teorema metrico sul lato.';
$("candidates").innerHTML= e.candidate_scores_before?Object.values(e.candidate_scores_before).sort((a,b)=>b.score-a.score).slice(0,7).map(s=>'<tr><td>'+r.graph.nodes[r.opposition_mappings.find(x=>x.id===s.id).angle].label+' ↔ '+r.graph.nodes[r.opposition_mappings.find(x=>x.id===s.id).side].label+'</td><td>'+s.score+'</td><td>'+s.local_support+'</td><td>'+s.coorigin_support+'</td></tr>').join(""):'<tr><td colspan="4">Seleziona un REBASE</td></tr>';
$("trace").innerHTML=r.timeline.slice(0,tick+1).map((ev,i)=>'<div class="entry '+(i===tick?"now":"")+'">'+i+'. '+(ev.selected?ev.from+'→'+ev.to+' · '+r.graph.nodes[ev.selected.new_opposition_edge.angle].label+' ↔ '+r.graph.nodes[ev.selected.new_opposition_edge.side].label:ev.operation)+'</div>').join("");
const all=D.aggregates[r.mode];
$("summary").innerHTML=D.conditions.map(c=>{let a=all[c];return '<tr><td>'+c+'</td><td>'+Math.round(a.transfer_question_rate*100)+'%</td><td>'+a.mean_induced_generics+'</td><td>'+a.mean_rank_reorderings+'</td><td>'+a.mean_distinct_oppositions+'</td></tr>'}).join("");
}
["condition","mode","seed"].forEach(id=>$(id).addEventListener("change",()=>{$("tick").value=4;render()}));
$("tick").addEventListener("input",render);render();
</script></body></html>"""


def main():
    data=json.loads((OUT/"traces.json").read_text(encoding="utf-8"))
    small={k:data[k] for k in ("schema","modes","conditions","aggregates")}
    small["seeds"]=data["seeds"][:10]
    small["runs"]=[r for r in data["runs"] if r["seed"] in small["seeds"]]
    raw=json.dumps(small,ensure_ascii=False,separators=(",",":")).replace("</","<\\/")
    (OUT/"viewer.html").write_text(PAGE.replace("__DATA__",raw),encoding="utf-8")
    lines=["# Merovingio v5 — Dynamic Opposition REBASE", "",
           "Rebase delle sole opposizioni angolo–lato, con nuova scelta dinamica dell'opposizione dopo ogni gruppo.",
           "Simulazione progettata; nessun modello vision/LLM, nessuna prova geometrica.","",
           "| Geometria | Condizione | N | Ipotesi trovato | Generic medi | Riorganizzazioni ranking | Opposizioni esplorate |",
           "|---|---|---:|---:|---:|---:|---:|"]
    for m,cs in data["aggregates"].items():
        for c,a in cs.items():
            lines.append("| "+" | ".join([m,c,str(a["n"]),str(a["transfer_question_rate"]),
            str(a["mean_induced_generics"]),str(a["mean_rank_reorderings"]),
            str(a["mean_distinct_oppositions"])])+" |")
    lines+=["","## Come leggerlo",
           "La v4 rileggeva una coppia di opposizioni già selezionata; la v5 sceglie online quale opposizione esplorare fra tutte quelle disponibili nel grafo.",
           "Ogni selezione genera un campo di attivazione locale che modifica la rilevanza delle altre opposizioni.",
           "I Generic Spaces candidati sono indotti da coppie strutturalmente associate di opposizioni già esplorate.",
           "Il trasferimento AD=DB? è una domanda prodotta solo quando vengono individuate entrambe le opposizioni degli angoli dati uguali.",
           "Il controllo senza bisettrice può trovare analogie strutturali, ma non questa domanda metrica.",
           "I parametri salienza/feedback sono fissati manualmente: non si può interpretare il confronto come validazione psicologica.",
           ""]
    (OUT/"REPORT.md").write_text("\n".join(lines),encoding="utf-8")
    print("Created",OUT/"viewer.html",OUT/"REPORT.md")

if __name__=="__main__":main()

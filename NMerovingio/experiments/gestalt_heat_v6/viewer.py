#!/usr/bin/env python3
"""Offline v6 explorer: productive analogical loops, actual trace provenance."""
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
OUT=HERE/"results"
PAGE=r"""<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Merovingio v6 — Productivity Driven REBASE</title>
<style>
:root{color-scheme:dark;font-family:Inter,ui-sans-serif,system-ui,sans-serif}
*{box-sizing:border-box}body{background:#10121c;color:#f2ecfa;margin:0}
header{background:#1b1c2b;border-bottom:1px solid #3b3850;padding:25px max(18px,calc((100vw - 1250px)/2))}
.eyebrow{font-size:11px;font-weight:700;color:#c9abe9;letter-spacing:2px}
h1{font-size:26px;margin:5px 0 9px}h2{font-size:16px;margin:0 0 12px}h3{font-size:13px;margin:14px 0 7px}
p{font-size:12px;color:#bdb6ca;line-height:1.55}
main{max-width:1250px;padding:18px;margin:auto;display:grid;gap:14px}
.panel{background:#1e1f2d;border:1px solid #403d56;border-radius:13px;padding:15px;min-width:0}
.controls{display:flex;gap:14px;align-items:end;flex-wrap:wrap}
label{font-size:12px;color:#bdb5cd;display:flex;flex-direction:column;gap:6px}
select,input{background:#111527;border:1px solid #656077;color:#f5effb;border-radius:8px;font:inherit;padding:8px}
input[type=range]{width:165px;padding:0;accent-color:#b29af0}
.columns{display:grid;grid-template-columns:1fr 1fr;gap:14px}
svg{width:100%;background:#141827;border-radius:10px}
.metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}
.metric{background:#2a2738;border-radius:10px;padding:12px}.metric small{font-size:10px;color:#a9a6b8}.metric b{font-size:23px;display:block;color:#e2c8fb}
.pill{padding:7px 9px;display:inline-flex;font-size:11px;border-radius:8px;background:#303047;border:1px solid #655977;margin:3px}
.pill.active{border-color:#b995f2;color:#e7d5fa}.pill.gs{border-color:#7ba79a;color:#b0e0cd}
.event{padding:12px;background:#2b2943;border-left:3px solid #b399e8;line-height:1.55;font-size:12px;border-radius:8px}
.evidence{padding:10px;background:#24283b;border-radius:8px;font-size:12px}
.trace{max-height:250px;overflow:auto;display:grid;gap:5px}
.step{padding:8px 10px;border:1px solid #444054;border-radius:7px;font-size:11px;color:#c5bfd0}
.step.now{border-color:#b89bef;background:#362c48;color:#fff}
table{width:100%;border-collapse:collapse;font-size:11px}
td,th{padding:9px;text-align:left;border-bottom:1px solid #403d50}
th{color:#cfbfe3}
.warning{border-radius:9px;border:1px solid #8e714c;padding:11px;color:#e8cda6;font-size:12px;background:#332c25}
@media(max-width:850px){.columns{grid-template-columns:1fr}.metrics{grid-template-columns:repeat(2,1fr)}}
</style></head><body><header><div class="eyebrow">MEROVINGIO / PANOPTIKON — EXPERIMENT V6</div>
<h1>REBASE delle opposizioni guidato dalla produttività</h1>
<p>Ogni opposizione angolo–lato può avviare un Generic Space incompleto. La seconda opposizione può completarlo, generando un feedback capace di cambiare ciò che verrà esplorato dopo.</p></header>
<main><div class="panel controls">
<label>Regime<select id="condition">
<option value="fixed_initial">A · Priorità iniziale fissa</option>
<option value="topology_only">B · Propagazione topologica</option>
<option value="predictive_only">C · Produttività prevista</option>
<option value="productivity_feedback" selected>D · Produttività + feedback</option>
<option value="feedback_genealogy_blind">E · Feedback senza genealogia</option>
</select></label>
<label>Figura<select id="mode"><option value="isosceles">Isoscele + bisettrice</option><option value="scalene">Scaleno + bisettrice</option><option value="ordinary_cevian">Trasversale non bisettrice</option></select></label>
<label>Attenzione iniziale<select id="attention"><option value="clean">Pulita</option><option selected value="competing_oppositions">Opposizioni distraenti</option></select></label>
<label>Seed<select id="seed"></select></label>
<label>Passaggio <span id="tickLabel"></span><input id="tick" type="range" min="0" max="4" value="3"></label></div>
<div class="metrics">
<div class="metric"><small>Opposizioni lette</small><b id="k1">0</b></div>
<div class="metric"><small>Generic incompleti</small><b id="k2">0</b></div>
<div class="metric"><small>Generic completati</small><b id="k3">0</b></div>
<div class="metric"><small>Ipotesi lati uguali?</small><b id="k4">No</b></div>
</div>
<div class="columns">
<div class="panel"><h2>Geometria e origine del trasferimento</h2><svg id="figure" viewBox="0 0 610 405"></svg>
<div id="selected"></div><h3>Generic Spaces emergenti</h3><div id="generics"></div>
<div class="warning">Il REBASE non dimostra AD=DB. Nel triangolo scaleno una bisettrice può generare la domanda, ma l'uguaglianza dei due segmenti è generalmente falsa. Una trasversale generica non dà l'uguaglianza angolare di partenza.</div></div>
<div class="panel"><h2>Feedback generativo</h2><div id="event" class="event"></div>
<h3>Candidati prima del REBASE</h3><table><thead><tr><th>Opposizione</th><th>Score</th><th>Produttività prevista</th><th>Feedback</th></tr></thead><tbody id="candidates"></tbody></table>
<h3>Genealogia del loop</h3><div class="trace" id="trace"></div>
</div></div>
<div class="panel"><h2>Confronto delle ablazioni · risultati del benchmark</h2><table><thead><tr><th>Condizione</th><th>Completamenti (%)</th><th>Ipotesi (%)</th><th>Prima chiusura (tick)</th><th>Feedback medi</th></tr></thead><tbody id="summary"></tbody></table>
<p>Tutte le condizioni vedono la stessa geometria. Cambiano le priorità e l'effetto delle analogie effettivamente generate. Sono dinamiche progettate manualmente, non una verifica psicologica.</p></div>
</main><script type="application/json" id="dataset">__DATA__</script>
<script>
"use strict";
const DB=JSON.parse(document.getElementById("dataset").textContent);const $=id=>document.getElementById(id);
DB.seeds.forEach(s=>{let o=document.createElement("option");o.textContent="Seed "+s;o.value=s;$("seed").appendChild(o)});
const get=()=>DB.runs.find(r=>r.seed===Number($("seed").value)&&r.condition===$("condition").value&&r.mode===$("mode").value&&r.attention===$("attention").value);
function line(a,b,c,w=3){return '<line x1="'+a[0]+'" y1="'+a[1]+'" x2="'+b[0]+'" y2="'+b[1]+'" stroke="'+c+'" stroke-width="'+w+'" stroke-linecap="round"/>'}
function figure(r,ev){
const p=r.geometry.points,a=p.A,b=p.B,c=p.C,d=p.D;
let s='<polygon points="'+[a,c,d].map(x=>x.join(",")).join(" ")+'" fill="#589abe" opacity=".12"/><polygon points="'+[b,c,d].map(x=>x.join(",")).join(" ")+'" fill="#dbad5d" opacity=".12"/>';
s+=line(a,c,"#ddd9ed")+line(b,c,"#ddd9ed")+line(a,b,"#ddd9ed")+line(c,d,"#ba98f1",5);
let chosen=ev.selected_opposition;
if(chosen){let n=r.material.nodes[chosen.side];s+=line(p[n.vertices[0]],p[n.vertices[1]],"#ecc075",7);let center=p[r.material.nodes[chosen.angle].vertex];s+='<circle cx="'+center[0]+'" cy="'+center[1]+'" r="25" fill="none" stroke="#78cad5" stroke-width="3"/>'}
for(const [name,v] of Object.entries(p)){s+='<circle cx="'+v[0]+'" cy="'+v[1]+'" r="5" fill="white"/><text x="'+(v[0]+8)+'" y="'+(v[1]-9)+'" fill="#e9e6f0" font-size="17">'+name+'</text>'}
$("figure").innerHTML=s;$("selected").innerHTML=chosen?'<span class="pill active">'+r.material.nodes[chosen.angle].label+'</span> ↔ <span class="pill active">'+r.material.nodes[chosen.side].label+'</span>':'<span class="pill">Costruzione, prima dell’esplorazione</span>';
}
function render(){
let r=get();if(!r)return;let input=$("tick");input.max=r.timeline.length-1;input.value=Math.min(Number(input.value),r.timeline.length-1);
let t=Number(input.value),e=r.timeline[t],hist=r.timeline.slice(1,t+1),gs=hist.flatMap(x=>x.new_generic_events||[]);
$("tickLabel").textContent=t+"/"+(r.timeline.length-1);
figure(r,e);
$("k1").textContent=hist.length;$("k2").textContent=gs.filter(x=>x.kind==="INCOMPLETE_GENERIC").length;
$("k3").textContent=gs.filter(x=>x.kind==="COMPLETED_GENERIC").length;
$("k4").textContent=hist.some(x=>(x.new_questions||[]).length)?"Formulata":"No";
$("generics").innerHTML=gs.map(x=>'<span class="pill gs">'+x.kind.replaceAll("_"," ")+' · '+x.carrier+'</span>').join("")||'<span class="pill">Ancora nessuno</span>';
$("event").innerHTML=e.operation==="CONSTRUCT_CD"?'Costruzione CD. La partizione angolare e quella della base sono disponibili. Nessun risultato metrico trasferito.':
'<b>'+e.from+' → '+e.to+'</b><br>Opposizione selezionata: '+r.material.nodes[e.selected_opposition.angle].label+' ↔ '+r.material.nodes[e.selected_opposition.side].label+
'<br>Produttività prevista: '+e.chosen_score.prospective_productivity+' · Feedback disponibile: '+e.chosen_score.realized_feedback+
'<br>Nuovi Generic Spaces: '+e.new_generic_events.length+' · Cause di feedback: '+e.feedback_causes.length+' · Ranking riordinato: '+(e.ranking_changed_by_feedback?"Sì":"No")+
(e.new_questions.length?'<br><b>Domanda di uguaglianza generata — NON PROVATA.</b>':'');
$("candidates").innerHTML=e.score_candidates_before?Object.values(e.score_candidates_before).sort((a,b)=>b.score-a.score).slice(0,6).map(x=>{let m=r.oppositions.find(z=>z.id===x.id);return '<tr><td>'+r.material.nodes[m.angle].label+' ↔ '+r.material.nodes[m.side].label+'</td><td>'+x.score+'</td><td>'+x.prospective_productivity+'</td><td>'+x.realized_feedback+'</td></tr>'}).join(""):'<tr><td colspan="4">Nessun REBASE selezionato</td></tr>';
$("trace").innerHTML=r.timeline.slice(0,t+1).map((x,i)=>'<div class="step '+(i===t?'now':'')+'">'+i+' · '+x.operation+(x.selected_opposition?' · '+r.material.nodes[x.selected_opposition.angle].label+' ↔ '+r.material.nodes[x.selected_opposition.side].label:'')+'</div>').join("");
$("summary").innerHTML=DB.conditions.map(c=>{const a=DB.aggregates[r.attention][r.mode][c];return '<tr><td>'+c+'</td><td>'+Math.round(100*a.complete_rate)+'%</td><td>'+Math.round(100*a.question_rate)+'%</td><td>'+(a.mean_first_completion_tick_if_found??'—')+'</td><td>'+a.mean_feedback_signals+'</td></tr>'}).join("");
}
["mode","condition","attention","seed"].forEach(id=>$(id).addEventListener("change",()=>{$("tick").value=3;render()}));
$("tick").addEventListener("input",render);render();
</script></body></html>"""


def main():
    data=json.loads((OUT/"traces.json").read_text(encoding="utf-8"))
    tiny={k:data[k] for k in ("schema","modes","conditions","attentions","aggregates")}
    tiny["seeds"]=data["seeds"][:10]
    tiny["runs"]=[r for r in data["runs"] if r["seed"] in tiny["seeds"]]
    embedded=json.dumps(tiny,ensure_ascii=False,separators=(",",":")).replace("</","<\\/")
    (OUT/"viewer.html").write_text(PAGE.replace("__DATA__",embedded),encoding="utf-8")
    lines=["# Merovingio v6 — Productivity-Driven Opposition REBASE",
        "", "Simulazione comparativa, NON prova euclidea, NON osservazione psicologica.",
        "",
        "| Attenzione | Geometria | Condizione | Seed | Completamenti | Domanda lato | Primo completamento | Feedback medi |",
        "|---|---|---|---:|---:|---:|---:|---:|"]
    for att,modes in data["aggregates"].items():
        for mode,cs in modes.items():
            for cond,a in cs.items():
                lines.append("| "+" | ".join([att,mode,cond,str(a["trials"]),
                  str(a["complete_rate"]),str(a["question_rate"]),
                  str(a["mean_first_completion_tick_if_found"]),
                  str(a["mean_feedback_signals"])])+" |")
    lines+=["", "## Lettura dei risultati",
        "Un Generic Space COMPLETED richiede due reali relazioni di opposizione co-generate dal medesimo divisore.",
        "La competizione delle altre opposizioni costituisce il controllo sull'esplorazione locale.",
        "PREDICTIVE_ONLY può anticipare il valore di completamento; PRODUCTIVITY_FEEDBACK aggiunge attivazione in seguito alla creazione effettiva di un nuovo GS.",
        "Una domanda AD=DB? è ammissibile solo quando la coppia di opposizioni include i due angoli con uguaglianza data; non si certifica mai la proposizione.",
        "Una performance di FIXED_INITIAL migliore dei metodi dinamici è un risultato da riportare, non da correggere a posteriori.",
        "Tutti i pesi della Slipnet e gli operatori di produttività sono programmati manualmente.",
        ""]
    (OUT/"REPORT.md").write_text("\n".join(lines),encoding="utf-8")
    print("Created",OUT/"viewer.html",OUT/"REPORT.md")
if __name__=="__main__":main()

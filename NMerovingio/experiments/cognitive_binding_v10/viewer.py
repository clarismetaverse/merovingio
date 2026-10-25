#!/usr/bin/env python3
"""Render v10 offline viewer from completed cognitive simulation traces."""
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
OUT=HERE/"results"
HTML=r"""<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Merovingio v10 · Cognitive Binding Memory</title>
<style>
:root{color-scheme:dark;font-family:Inter,ui-sans-serif,system-ui,sans-serif}
*{box-sizing:border-box}body{margin:0;background:#11131d;color:#f0edf9}
header{padding:24px max(15px,calc((100vw - 1210px)/2));background:#1c1d2c;border-bottom:1px solid #4d4459}
h1{font-size:26px;margin:5px 0 8px;letter-spacing:-.5px}h2{font-size:16px;margin:0 0 11px}
h3{font-size:13px;margin:14px 0 8px}p{font-size:12px;color:#b9b2ca;line-height:1.6}
.eyebrow{color:#c2a0e4;font-weight:700;letter-spacing:1.6px;font-size:11px}
main{max-width:1210px;margin:0 auto;padding:17px;display:grid;gap:14px}
.panel{background:#1f2030;border:1px solid #49435c;border-radius:13px;padding:15px;min-width:0}
.controls{display:flex;flex-wrap:wrap;gap:13px;align-items:end}
label{font-size:12px;color:#c2bbd2;display:flex;flex-direction:column;gap:6px}
select,input{background:#151827;color:#f3eefb;border:1px solid #665f7b;border-radius:8px;padding:9px;font:inherit}
input[type=range]{width:150px;accent-color:#b39deb;padding:0}
.grid{display:grid;grid-template-columns:.95fr 1.05fr;gap:14px}
svg{width:100%;background:#161a29;border-radius:10px}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:9px}
.kpi{background:#2a283b;padding:12px;border-radius:10px}.kpi small{font-size:10px;color:#bcb2c7}.kpi b{display:block;font-size:19px;color:#dcc8f9}
.pill{display:inline-flex;border:1px solid #6a5b82;background:#302b45;font-size:11px;border-radius:8px;padding:7px 9px;margin:3px}
.pill.new{border-color:#73a88a;color:#b9e6cc}
.story{background:#2f2944;border-left:3px solid #bfa2ec;border-radius:8px;padding:12px;font-size:13px;line-height:1.55}
.trace{display:grid;gap:5px;max-height:440px;overflow:auto}
.event{font-size:11px;border:1px solid #4c4661;padding:9px;border-radius:7px;background:#252638;color:#c4bcda}
.event.now{border-color:#baa2ec;background:#362e4d;color:#fff}
.parents{font-size:10px;color:#9c93b2;margin-top:4px}
.note{background:#362b25;border:1px solid #886946;color:#f0d6ab;font-size:12px;padding:11px;border-radius:8px;line-height:1.55}
table{border-collapse:collapse;width:100%;font-size:11px}
th,td{text-align:left;border-bottom:1px solid #4b465e;padding:10px 7px}
th{color:#d2bfdc}
@media(max-width:850px){.grid{grid-template-columns:1fr}.kpis{grid-template-columns:repeat(2,1fr)}}
</style></head><body><header><div class="eyebrow">MEROVINGIO · PANOPTIKON · V10</div>
<h1>Memoria delle conseguenze cognitive dei binding</h1>
<p>Non dimostriamo un nuovo teorema: seguiamo il movimento cognitivo dai ruoli prospettici al frame LAL completato, alla relazione segmentale proiettata, fino all'attivazione dei frame MEDIANA e LLL.</p></header>
<main><div class="panel controls">
<label>Figura<select id="shape"><option value="equilateral">Equilatero</option><option value="isosceles">Isoscele</option><option value="scalene">Scaleno</option></select></label>
<label>Angolo<select id="goal"><option value="C">C</option><option value="A">A</option><option value="B">B</option></select></label>
<label>Condizione<select id="condition"><option value="normal">Binding normale</option><option value="LLL_initially_favored">LLL inizialmente favorito</option><option value="without_prospection">Senza anticipazione v8</option><option value="angle_witness_masked">Angolo compreso oscurato</option><option value="counterfactual_base_given">Controfattuale: base già data uguale</option></select></label>
<label>Seed<select id="seed"></select></label>
<label>Evento <span id="ticktxt"></span><input id="tick" type="range" min="0" value="5"/></label></div>
<div class="kpis">
<div class="kpi"><small>LAL cognitivamente completo</small><b id="k1">—</b></div>
<div class="kpi"><small>Nuova relazione proiettata</small><b id="k2">—</b></div>
<div class="kpi"><small>Frame MEDIANA attivato</small><b id="k3">—</b></div>
<div class="kpi"><small>Nuova lettura LLL</small><b id="k4">—</b></div></div>
<div class="grid">
<div class="panel"><h2>Figura materiale invariata durante la rilettura</h2><svg id="fig" viewBox="0 0 410 338"></svg>
<h3>Ultima relazione attivata</h3><div id="current" class="story"></div>
<h3>Catena delle dipendenze</h3><div id="ancestry"></div>
<div class="note">La relazione fra le due metà della base è marcata come <b>conseguenza cognitiva proiettata</b>. Non è promossa automaticamente a teorema verificato. Se manca AC = BC o l'uguaglianza degli angoli compresi, il frame LAL non si completa e non produce alcuna proiezione.</div>
</div>
<div class="panel"><h2>Cosa è cambiato nel workspace mentale?</h2><div class="trace" id="trace"></div></div>
</div>
<div class="panel"><h2>Confronto fra le condizioni · 48 seed</h2><table><thead><tr><th>Condizione</th><th>Completamenti LAL</th><th>Relazioni proiettate</th><th>Mediana attivata</th><th>False promozioni a prova</th></tr></thead><tbody id="summary"></tbody></table>
<p>Le attività sono tracciate con riferimenti ai binding che le hanno rese possibili. L'architettura è una simulazione cognitiva con operatori ideati manualmente, non una ricostruzione storica o un verificatore di teoremi.</p></div>
</main>
<script type="application/json" id="data">__DATA__</script>
<script>
"use strict";
const DATA=JSON.parse(document.getElementById("data").textContent);const $=id=>document.getElementById(id);
DATA.seeds.forEach(n=>{const o=document.createElement("option");o.value=n;o.textContent="Seed "+n;$("seed").append(o)});
function run(){return DATA.runs.find(r=>r.seed===Number($("seed").value)&&r.shape===$("shape").value&&r.goal===$("goal").value&&r.condition===$("condition").value)}
function line(a,b,color,w=3){return '<line x1="'+a[0]+'" y1="'+a[1]+'" x2="'+b[0]+'" y2="'+b[1]+'" stroke="'+color+'" stroke-width="'+w+'" stroke-linecap="round"/>'}
function draw(r,item){
let newMaterial=item.kind==="CONSTRUCT_DIVIDER"||item.tick>=(r.cognitive_memory.entries.find(x=>x.kind==="CONSTRUCT_DIVIDER")||{tick:999}).tick;
const p=newMaterial?r.postconstruction.points:r.preconstruction.points;
const face=r.preconstruction.faces[0];
let out="";
if(newMaterial)for(let f of r.postconstruction.faces){out+='<polygon points="'+f.map(x=>p[x].join(",")).join(" ")+'" fill="#7287b9" opacity=".13"/>'}
for(let i=0;i<3;i++)out+=line(p[face[i]],p[face[(i+1)%3]],"#ece8f5",3);
if(newMaterial){let ev=r.postconstruction.construction_events[0];out+=line(p[ev.vertex],p[ev.contact_point],"#b89cec",5)}
for(const [name,pt] of Object.entries(p)){out+='<circle cx="'+pt[0]+'" cy="'+pt[1]+'" r="4" fill="#fff"/><text x="'+(pt[0]+8)+'" y="'+(pt[1]-8)+'" font-size="15" fill="white">'+name+'</text>'}
$("fig").innerHTML=out;
}
function render(){
let r=run();if(!r){$("goal").value="C";$("condition").value="normal";r=run()}
if(!r)return;
let entries=r.cognitive_memory.entries,slider=$("tick");
slider.max=entries.length-1;slider.value=Math.min(Number(slider.value),entries.length-1);
let idx=Number(slider.value),e=entries[idx],prior=entries.slice(0,idx+1);
$("ticktxt").textContent=(idx+1)+"/"+entries.length;draw(r,e);
$("k1").textContent=prior.some(x=>x.kind==="COMPLETE_FRAME")?"Sì":"No";
$("k2").textContent=prior.some(x=>x.kind==="PROJECT_RELATION")?"Sì":"No";
$("k3").textContent=prior.some(x=>x.kind==="ACTIVATE_ALTERNATIVE_FRAME")?"Sì":"No";
$("k4").textContent=prior.some(x=>x.kind==="REBASE_FRAME")?"Sì":"No";
$("current").innerHTML='<b>'+e.kind.replaceAll("_"," ")+'</b><br>'+e.meaning+'<br><small>Stato: '+e.status+' · Frame: '+e.frame+'</small>';
$("ancestry").innerHTML=e.parents.map(id=>{let p=r.cognitive_memory.entries.find(y=>y.id===id);return '<span class="pill">'+p?.kind.replaceAll("_"," ")+'</span>'}).join("")||'<span class="pill">Evento iniziale</span>';
$("trace").innerHTML=entries.map((x,i)=>'<div class="event '+(idx===i?"now":"")+'">'+(i+1)+'. '+x.kind.replaceAll("_"," ")+'<br>'+x.meaning+'<div class="parents">'+x.status+' · '+x.parents.length+' dipendenze</div></div>').join("");
let aggregate=DATA.aggregates[r.shape][r.goal];
$("summary").innerHTML=Object.entries(aggregate).map(([c,a])=>'<tr><td>'+c+'</td><td>'+Math.round(100*a.frame_completion_rate)+'%</td><td>'+Math.round(100*a.relation_projection_rate)+'%</td><td>'+Math.round(100*a.median_attraction_rate)+'%</td><td>'+a.false_proof_promotions+'</td></tr>').join("");
}
["shape","goal","condition","seed"].forEach(id=>$(id).addEventListener("change",()=>{$("tick").value=5;render()}));
$("tick").addEventListener("input",render);render();
</script></body></html>"""


def main():
    d=json.loads((OUT/"traces.json").read_text(encoding="utf-8"))
    small={k:d[k] for k in ("schema","shapes","conditions","aggregates")}
    small["seeds"]=d["seeds"][:10]
    small["runs"]=[r for r in d["runs"] if r["seed"] in small["seeds"]]
    inline=json.dumps(small,ensure_ascii=False,separators=(",",":")).replace("</","<\\/")
    (OUT/"viewer.html").write_text(HTML.replace("__DATA__",inline),encoding="utf-8")
    lines=["# Merovingio v10 — Cognitive Binding Consequence Memory",
      "", "NOT a geometric proof attempt. Records causally attributed cognitive acts that emerge AFTER successful frame binding.",
      "",
      "| Shape | Goal | Condition | N | LAL mental completion | Projected relation | Median frame activation | New LLL reading | False proof upgrades |",
      "|---|---|---|---:|---:|---:|---:|---:|---:|"]
    for shape,goals in d["aggregates"].items():
        for goal,conds in goals.items():
            for condition,a in conds.items():
                lines.append("| "+" | ".join([shape,goal,condition,str(a["n"]),
                    str(a["frame_completion_rate"]),str(a["relation_projection_rate"]),
                    str(a["median_attraction_rate"]),str(a["new_LLL_reading_rate"]),
                    str(a["false_proof_promotions"])])+" |")
    lines+=["",
      "## Epistemic sequence",
      "1. Original initial side relation is AVAILABLE as a given, or NOT AVAILABLE.",
      "2. The prospective dual-angle/side blend may exist in mental space without new material points.",
      "3. The bisector is constructed and subfaces are recognized bottom-up.",
      "4. Cognitive role bindings attach original side equality, shared segment and included angle equality to the LAL frame.",
      "5. Only after the LAL frame is cognitively complete can a relationship between the two opposite base portions be PROJECTED AS COGNITIVE CONSEQUENCE.",
      "6. The projected relation activates a MEDIAN reading and a new LLL reinterpretation with an explicit provenance chain.",
      "7. No projected relation is automatically a formal theorem or an independent premise available to prove itself.",
      "",
      "## Negative controls",
      "Scalene: no original pair of equal external sides, so no LAL cognitive completion or new base relation.",
      "Masked included angle: no complete LAL, therefore no projected base relation.",
      "Counterfactual extra given: an independently supplied equality is marked separately, never confused with a projected relation.",
      "",
      "This remains a hand-engineered cognitive process model, not an empirical human-cognition model.",
      ""]
    (OUT/"REPORT.md").write_text("\n".join(lines),encoding="utf-8")
    print("Created",OUT/"viewer.html",OUT/"REPORT.md")

if __name__=="__main__":main()

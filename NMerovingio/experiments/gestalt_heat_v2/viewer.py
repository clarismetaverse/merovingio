#!/usr/bin/env python3
"""Standalone viewer for actual graph-grammar v2 timelines (no external JS)."""
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
OUT=HERE/"results"
TEMPLATE=r"""<!doctype html><html lang="it"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Merovingio · Endogenous Gestalt v2</title>
<style>
*{box-sizing:border-box}body{background:#12121b;color:#eeeaf4;margin:0;font-family:Inter,ui-sans-serif,system-ui}
header{padding:25px max(18px,calc((100vw - 1260px)/2));border-bottom:1px solid #373343;background:#1b1925}
h1{font-size:26px;margin:4px 0 8px}h2{font-size:16px;margin:0 0 15px;color:#f3e7fa}
p{font-size:13px;line-height:1.55;color:#aca6bd}.subtitle{font-size:12px;letter-spacing:2px;text-transform:uppercase;color:#c1a5e8}
main{max-width:1260px;margin:auto;padding:18px;display:grid;gap:14px}
.controls{display:flex;gap:14px;flex-wrap:wrap;align-items:end;background:#1e1c2b;border:1px solid #414054;border-radius:13px;padding:13px}
label{display:flex;flex-direction:column;gap:5px;font-size:12px;color:#bdb6ce;font-weight:600}
select,input{background:#171923;color:#f7f3fc;padding:8px;border:1px solid #65607b;border-radius:8px;font:inherit}
input[type=range]{accent-color:#a99cf0;width:180px;padding:0}
.grid{display:grid;grid-template-columns:minmax(330px,1fr) minmax(350px,1fr);gap:14px}
.panel{background:#1c1d2b;border:1px solid #3c3b50;border-radius:13px;padding:16px;min-width:0}
svg{background:#141726;width:100%;border-radius:12px}
.meter{display:grid;grid-template-columns:87px 1fr 38px;align-items:center;gap:8px;margin:10px 0;font-size:12px}
.track{background:#343245;height:9px;border-radius:20px;overflow:hidden}.fill{height:100%;background:linear-gradient(90deg,#746fea,#bda0f1)}
.badge{font-size:11px;color:#ddcaef;background:#393047;border:1px solid #716087;border-radius:8px;padding:7px;display:inline-block;margin:4px 5px 3px 0}
.event{padding:11px;background:#28263a;border-left:3px solid #b499ea;font-size:13px;line-height:1.6;border-radius:8px;min-height:92px}
.trace{max-height:290px;overflow:auto;display:grid;gap:6px}.step{padding:8px;border:1px solid #353044;border-radius:7px;font-size:11px;color:#c9bddc}
.step.active{background:#332b49;border-color:#bfa5ed}
.kpis{display:grid;grid-template-columns:repeat(4,minmax(100px,1fr));gap:9px}
.kpi{background:#292438;padding:12px;border-radius:10px}.kpi b{font-size:22px;display:block;color:#ddc6fb}.kpi small{font-size:10px;color:#b8abc8}
table{width:100%;border-collapse:collapse;font-size:12px}td,th{padding:9px;text-align:left;border-bottom:1px solid #454052}th{font-weight:600;color:#c9bde0}
small,code{color:#d2c5e6}code{font-size:11px;word-break:break-word}
.warning{padding:12px;border:1px solid #80684b;background:#382e28;border-radius:10px;color:#e4c9a9;font-size:12px}
@media(max-width:900px){.grid{grid-template-columns:1fr}.kpis{grid-template-columns:repeat(2,minmax(100px,1fr))}}
</style></head><body><header>
<div class="subtitle">Merovingio · Panoptikon · Graph Grammar Experiment</div>
<h1>Gestalt Propagation v2</h1>
<p>Il punto non è trovare un gruppo già elencato: la grammatica del grafo genera raggruppamenti, la tensione angoli ↔ lati orienta la ricerca e il raggruppamento retroagisce sulla Slipnet.</p>
</header><main><div class="controls">
<label>Condizione<select id="condition"><option value="bottom_up">A · Bottom-up</option><option value="feedforward">B · Macro → micro</option><option selected value="reciprocal">C · Macro ↔ micro</option><option value="reciprocal_without_opposition">D · Feedback senza opposizione</option></select></label>
<label>Geometria<select id="mode"><option value="isosceles">Isoscele</option><option value="scalene">Scaleno</option></select></label>
<label>Seed<select id="seed"></select></label>
<label>Evento <span id="tickcount"></span><input type="range" min="0" max="16" value="9" id="tick"></label>
</div><div class="kpis">
<div class="kpi"><small>Gruppi generati</small><b id="groups-kpi">—</b></div>
<div class="kpi"><small>Allineamenti</small><b id="align-kpi">—</b></div>
<div class="kpi"><small>Generic Spaces indotti</small><b id="generics-kpi">—</b></div>
<div class="kpi"><small>Tensione → ipotesi segmentale</small><b id="hyp-kpi">—</b></div>
</div><div class="grid">
<div class="panel"><h2>Figura e generazione delle Gestalten</h2>
<svg id="figure" viewBox="0 0 610 400"></svg>
<h2 style="margin-top:18px">Oggetti del gruppo appena generato</h2><div id="selected-objects"></div>
<h2 style="margin-top:18px">Nuove astrazioni</h2><div id="abstract"></div>
<div class="warning">La congruenza ∠ACD = ∠DCB è data. L'eventuale uguaglianza AD = DB resta un'ipotesi analogica, mai un'asserzione verificata dal motore.</div>
</div><div class="panel"><h2>Slipnet: attivazione macro</h2><div id="meters"></div>
<h2 style="margin-top:19px">Evento corrente</h2><div id="event" class="event"></div>
<h2 style="margin-top:18px">Genealogia operativa</h2><div id="trace" class="trace"></div></div>
</div><div class="panel"><h2>Confronto delle quattro condizioni</h2><table><thead><tr><th>Condizione</th><th>Ipotesi (%)</th><th>Gruppi cross-domain</th><th>Allineamenti</th><th>Opposition align</th></tr></thead><tbody id="table"></tbody></table><p>Statistica completa su tutti i seed. Il viewer visualizza una selezione di seed, senza alterare gli aggregati.</p></div>
<p>**Limite sperimentale:** la grammatica e gli incentivi sono costruiti manualmente; i sottogruppi e i Generic Spaces non sono elencati in anticipo. Non è una misura empirica della cognizione umana.</p>
</main><script type="application/json" id="dataset">__DATA__</script><script>
"use strict";
const d=JSON.parse(document.getElementById("dataset").textContent),el=x=>document.getElementById(x);
for(const s of d.seeds){const o=document.createElement("option");o.value=s;o.textContent="Seed "+s;el("seed").appendChild(o)}
function run(){return d.runs.find(x=>x.seed===Number(el("seed").value)&&x.mode===el("mode").value&&x.condition===el("condition").value)}
function lin(a,b,color,width,dashed=false){return '<line x1="'+a[0]+'" y1="'+a[1]+'" x2="'+b[0]+'" y2="'+b[1]+'" stroke="'+color+'" stroke-width="'+width+'"'+(dashed?' stroke-dasharray="6 5"':'')+'/>'}
function dot(p,n){return '<circle cx="'+p[0]+'" cy="'+p[1]+'" r="5" fill="#eee7fa"/><text x="'+(p[0]+9)+'" y="'+(p[1]-10)+'" font-size="17" fill="#eee7fa">'+n+'</text>'}
function draw(r,e){
const p=r.material.points,A=p.A,B=p.B,C=p.C,D=p.D;
let s=lin(A,B,"#ded8ed",3)+lin(A,C,"#ded8ed",3)+lin(B,C,"#ded8ed",3)+lin(C,D,"#a994ea",4);
s+=dot(A,"A")+dot(B,"B")+dot(C,"C")+dot(D,"D");
if(e.new_group){let g=e.new_group;
for(const id of g.objects){let n=r.graph.nodes[id];
if(n.kind==="side"){let xy=n.vertices.map(x=>p[x]);s+=lin(xy[0],xy[1],"#edba6b",7)}
if(n.kind==="angle"&&n.vertex==="C")s+='<circle cx="'+C[0]+'" cy="'+C[1]+'" r="28" fill="none" stroke="#71c1ce" stroke-width="4" opacity=".8"/>';
if(n.kind==="region"){let xy=n.vertices.map(x=>p[x]);s+='<polygon points="'+xy.map(t=>t.join(",")).join(" ")+'" fill="#aa90e5" opacity=".15"/>'}
}}
el("figure").innerHTML=s;
}
function render(){
const r=run();if(!r)return;const tick=el("tick");tick.max=r.timeline.length-1;tick.value=Math.min(Number(tick.value),r.timeline.length-1);
const t=+tick.value,e=r.timeline[t];
el("tickcount").textContent=t+" / "+(r.timeline.length-1);draw(r,e);
const chosen=r.timeline.slice(1,t+1).filter(x=>x.new_group);
const aligned=chosen.filter(x=>x.operation==="ALIGN");
el("groups-kpi").textContent=chosen.length;
el("align-kpi").textContent=aligned.length;
el("generics-kpi").textContent=chosen.filter(x=>x.new_generic).length;
el("hyp-kpi").textContent=chosen.some(x=>x.new_analogical_hypothesis)?"Sì":"No";
el("selected-objects").innerHTML=e.new_group?e.new_group.objects.map(x=>'<span class="badge">'+r.graph.nodes[x].label+'</span>').join(""):'<span class="badge">Solo costruzione CD</span>';
const gs=chosen.filter(x=>x.new_generic).map(x=>x.new_generic);
el("abstract").innerHTML=gs.length?gs.map(g=>'<span class="badge">'+g.role_schema.join(" / ")+'</span>').join(""):'<small>Nessun Generic Space allineato a questo tick.</small>';
el("meters").innerHTML=Object.entries(e.activation_after).map(([key,value])=>'<div class="meter"><span>'+key+'</span><div class="track"><div class="fill" style="width:'+(100*value).toFixed(1)+'%"></div></div><span>'+Math.round(value*100)+'%</span></div>').join("");
el("event").innerHTML=e.new_group?
'<b>'+e.operation+'</b> · '+e.new_group.relation_types.join(", ")+'<br><small>Score '+e.score+', contributo macro '+e.macro_inherited+'; frontiera '+e.frontier_size+' gruppi.</small><br><code>'+e.provenance_chain.join(" → ")+'</code>'+(e.new_analogical_hypothesis?'<br><b>Trasferimento ipotizzato, NON PROVATO</b>':''):
'<b>CONSTRUCT_CD</b> · +'+e.material_delta.nodes+' oggetti; +'+e.material_delta.relations+' relazioni. La prima partizione è disponibile prima della scelta dei gruppi.';
el("trace").innerHTML=r.timeline.slice(0,t+1).map((x,i)=>'<div class="step '+(i===t?"active":"")+'">'+i+'. '+x.operation+(x.new_group?' → '+x.new_group.relation_types.join(", ")+' · macro '+x.macro_inherited:'')+'</div>').join("");
const ag=d.aggregate[r.mode];el("table").innerHTML=d.conditions.map(c=>{const a=ag[c];return '<tr><td>'+c+'</td><td>'+Math.round(a.hypothesis_rate*100)+'%</td><td>'+a.mean_cross_domain_count+'</td><td>'+a.mean_alignment_count+'</td><td>'+a.mean_opposition_alignments+'</td></tr>'}).join("");
}
for(const k of ["condition","mode","seed"]){el(k).addEventListener("change",()=>{el("tick").value=9;render()})}
el("tick").addEventListener("input",render);render();
</script></body></html>"""


def main():
    data=json.loads((OUT/"traces.json").read_text(encoding="utf-8"))
    small={k:data[k] for k in ("schema","seeds","modes","conditions","aggregate")}
    small["seeds"]=data["seeds"][:8]
    small["runs"]=[r for r in data["runs"] if r["seed"] in small["seeds"]]
    encoded=json.dumps(small,ensure_ascii=False,separators=(",",":")).replace("</","<\\/")
    (OUT/"viewer.html").write_text(TEMPLATE.replace("__DATA__",encoded),encoding="utf-8")
    lines=[
    "# Merovingio · Endogenous Gestalt v2 · risultati",
    "",
    "Simulazione di grammatica sul grafo, senza Jev e senza prova geometrica.",
    "",
    "| Geometria | Condizione | N | Ipotesi (%) | Media gruppi cross-domain | Media allineamenti | Media allineamenti opposite |",
    "|---|---|---:|---:|---:|---:|---:|"]
    for m,cc in data["aggregate"].items():
        for c,a in cc.items():
            lines.append("| "+" | ".join([m,c,str(a["n"]),str(round(a["hypothesis_rate"]*100,2)),
            str(a["mean_cross_domain_count"]),str(a["mean_alignment_count"]),str(a["mean_opposition_alignments"])])+" |")
    lines+=["",
    "## Interpretazione",
    "I gruppi non sono enumerati: emergono da SEED / EXTEND / ALIGN su relazioni derivate.",
    "Il lessico dei tipi e operatori è invece fissato a priori: questa non è ancora induzione libera di categorie.",
    "La strategia reciproca rinforza gli stessi concetti che favoriscono i gruppi.",
    "I differenziali descrivono un sistema progettato; non dimostrano effetti cognitivi umani.",
    "La relazione AD = DB non viene mai certificata a partire dalla sola bisettrice.",
    "Il caso scaleno ne impedisce l'interpretazione come identità metrica universale.",
    "",
    "## Artefatti", "traces.json: eventi e provenienza per tutti i seed; aggregate.json: statistiche; viewer.html: esplorazione con slider.",
    ""]
    (OUT/"REPORT.md").write_text("\n".join(lines),encoding="utf-8")
    print("Created",OUT/"viewer.html","and",OUT/"REPORT.md")


if __name__=="__main__":main()

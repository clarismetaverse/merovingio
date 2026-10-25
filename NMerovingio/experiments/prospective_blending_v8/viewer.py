#!/usr/bin/env python3
"""Merovingio v8: offline stepwise explorer of a prospective double-scope blend."""
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
OUT=HERE/"results"
HTML=r"""<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Merovingio v8 — Prospective Double-Scope Blending</title>
<style>
:root{font-family:Inter,system-ui,ui-sans-serif,sans-serif;color-scheme:dark}
*{box-sizing:border-box}body{margin:0;background:#11121d;color:#f1ecfa}
header{padding:25px max(16px,calc((100vw - 1240px)/2));background:#1b1c2c;border-bottom:1px solid #403950}
h1{font-size:25px;letter-spacing:-.45px;margin:4px 0 8px}
h2{font-size:16px;margin:0 0 11px}h3{font-size:13px;margin:14px 0 8px}
p{color:#b8b2c8;font-size:12px;line-height:1.55}
.eyebrow{font-size:11px;letter-spacing:1.6px;color:#c6a9ea;font-weight:700}
main{max-width:1240px;margin:auto;padding:18px;display:grid;gap:14px}
.panel{background:#1e1e2f;border:1px solid #45415a;border-radius:13px;padding:15px;min-width:0}
.controls{display:flex;gap:13px;flex-wrap:wrap;align-items:end}
label{display:flex;flex-direction:column;gap:6px;font-size:12px;color:#c9c1d3}
select,input{font:inherit;background:#141728;border:1px solid #68637e;border-radius:7px;padding:9px;color:#f6f1fd}
input[type=range]{padding:0;width:170px;accent-color:#bba2ed}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:14px}
svg{width:100%;border-radius:10px;background:#151727;display:block}
.mets{display:grid;grid-template-columns:repeat(4,1fr);gap:9px}
.met{background:#292637;padding:12px;border-radius:9px}.met b{color:#e0c6fb;font-size:22px;display:block}
.met small{font-size:10px;color:#b5adc7}
.pill{display:inline-flex;border:1px solid #6a587d;background:#302c43;padding:7px 9px;border-radius:8px;font-size:11px;margin:3px}
.pill.good{border-color:#73a68d;color:#b2ddc2}
.story{padding:12px;border-left:3px solid #b398e9;border-radius:7px;background:#2c2b42;font-size:12px;line-height:1.65}
.note{font-size:12px;padding:12px;border:1px solid #896c49;background:#312921;color:#e9d2b3;border-radius:8px;line-height:1.5}
.timeline{display:grid;gap:6px}
.step{border:1px solid #555065;border-radius:7px;padding:9px;font-size:11px;color:#c1b9d0}
.step.selected{border-color:#c0a2ef;background:#3b3050;color:#fff}
table{border-collapse:collapse;width:100%;font-size:11px}
td,th{padding:9px 8px;text-align:left;border-bottom:1px solid #48455e}
th{color:#c9badd}
@media(max-width:850px){.grid{grid-template-columns:1fr}.mets{grid-template-columns:repeat(2,1fr)}}
</style></head><body>
<header><div class="eyebrow">PANOPTIKON / MEROVINGIO · V8</div><h1>Blending prospettico: prima della bisettrice</h1>
<p>Il triangolo e l'obiettivo di dividere un angolo sono dati. Il sistema richiama TRIANGLE e DIVISION, anticipa possibili corrispondenze a coppie, sceglie una costruzione, e soltanto dopo verifica quali ruoli si materializzano.</p></header>
<main>
<div class="panel controls">
<label>Triangolo<select id="shape"><option value="equilateral">Equilatero</option><option value="scalene">Scaleno</option><option value="obtuse">Ottusangolo</option></select></label>
<label>Angolo da dividere<select id="goal"><option value="C">C</option><option value="A">A</option><option value="B">B</option></select></label>
<label>Strategia<select id="condition"><option value="full_blend" selected>Blending prospettico completo</option><option value="no_opposition">Senza memoria di opposizione</option><option value="no_transport">Senza trasporto di DIVISION</option><option value="post_construct_only">Solo lettura dopo costruzione</option><option value="goal_only">Solo obiettivo angolare</option></select></label>
<label>Seed<select id="seed"></select></label>
<label>Fase <span id="phase_label"></span><input id="stage" type="range" min="0" max="4" value="1" step="1"></label>
</div>
<div class="mets">
<div class="met"><small>Blend prima di CD</small><b id="k1">—</b></div>
<div class="met"><small>Triangoli anticipati</small><b id="k2">—</b></div>
<div class="met"><small>Costruzione sul vertice giusto</small><b id="k3">—</b></div>
<div class="met"><small>Ruoli poi istanziati</small><b id="k4">—</b></div>
</div>
<div class="grid">
<div class="panel"><h2>Prima e dopo la costruzione</h2>
<svg id="diagram" viewBox="0 0 400 335"></svg>
<div id="caption"></div>
<h3>Ruoli prospettici / relazioni costruite</h3><div id="roles"></div>
<div class="note">Le due sottofigure possono essere anticipate strutturalmente. Il loro riconoscimento NON dimostra che la bisettrice divida il lato opposto in due segmenti uguali. Nel caso scaleno questo è generalmente falso.</div>
</div>
<div class="panel"><h2>Operazione cognitiva in primo piano</h2><div class="story" id="story"></div>
<h3>Costruzioni candidate e loro punteggi</h3>
<table><thead><tr><th>Vertice</th><th>Lato raggiunto</th><th>Obiettivo</th><th>Ruolo TRIANGLE</th><th>Blend</th></tr></thead><tbody id="candidates"></tbody></table>
<h3>Sequenza di pensiero e costruzione</h3><div class="timeline" id="timeline"></div>
</div>
</div>
<div class="panel"><h2>Ablazioni eseguite: stesso triangolo e stesso obiettivo</h2>
<table><thead><tr><th>Condizione</th><th>Blend anticipato</th><th>Costruzione corretta</th><th>Binding prospettico</th></tr></thead><tbody id="summary"></tbody></table>
<p>Risultati su tutti i seed disponibili. Questa è una simulazione con una grammatica esplicitamente programmata; non misura ragionamento spontaneo umano né dimostra un teorema.</p></div>
</main>
<script id="data" type="application/json">__DATA__</script>
<script>
"use strict";
const data=JSON.parse(document.getElementById("data").textContent),$=id=>document.getElementById(id);
data.seeds.forEach(n=>{let el=document.createElement("option");el.value=n;el.textContent="Seed "+n;$("seed").append(el)});
function current(){return data.runs.find(x=>x.condition===$("condition").value&&x.shape===$("shape").value&&x.goal_vertex===$("goal").value&&x.seed===Number($("seed").value))}
function lin(a,b,color,w=3,dashed=false){return '<line x1="'+a[0]+'" y1="'+a[1]+'" x2="'+b[0]+'" y2="'+b[1]+'" stroke="'+color+'" stroke-width="'+w+'" stroke-linecap="round"'+(dashed?' stroke-dasharray="7 5"':'')+'/>'}
function render(){
const r=current();if(!r)return;
const stage=Number($("stage").value),initial=r.preconstruction_material,post=r.postconstruction_material,material=stage>=3?post:initial,p=material.points;
$("phase_label").textContent=stage+"/4";
const f=initial.faces[0];
let svg="",faces=material.faces;
if(stage>=3){for(const face of faces){let poly=face.map(x=>p[x].join(",")).join(" ");svg+='<polygon points="'+poly+'" fill="#6c789c" fill-opacity=".13"/>'}}
for(let i=0;i<f.length;i++)svg+=lin(p[f[i]],p[f[(i+1)%f.length]],"#ece7f5",3);
if(stage>=3){let event=post.construction_events[0];svg+=lin(p[event.vertex],p[event.contact_point],"#a896e6",4)}
else if(stage===1&&r.preconstruction_blend){
const edge=r.preconstruction_blend.source_opposition.opposite_edge;
let a=p[edge[0]],b=p[edge[1]],c=p[r.goal_vertex],sideCenter=[(a[0]+b[0])/2,(a[1]+b[1])/2];
let abstract=[c[0]+.57*(sideCenter[0]-c[0]),c[1]+.57*(sideCenter[1]-c[1])];
svg+=lin(c,abstract,"#b19cea",2,true);
svg+='<text x="'+(abstract[0]+8)+'" y="'+(abstract[1]-4)+'" font-size="18" fill="#cdb3f2">?</text>';
}
for(let [name,pt] of Object.entries(p)){svg+='<circle cx="'+pt[0]+'" cy="'+pt[1]+'" r="4.6" fill="white"/><text x="'+(pt[0]+9)+'" y="'+(pt[1]-10)+'" fill="#f2ebf9" font-size="14">'+name+'</text>'}
$("diagram").innerHTML=svg;
$("k1").textContent=r.metrics.prospective_blend_before_construction?"Sì":"No";
$("k2").textContent=r.preconstruction_blend?r.preconstruction_blend.blended_space.triangular_face_slots:0;
$("k3").textContent=r.metrics.correct_goal_construction?"Sì":"No";
$("k4").textContent=r.metrics.prospective_roles_bound?"Sì":"No";
const active=r.timeline[stage];
const headings=[
"TRIANGLE: la figura materiale e l'angolo da dividere sono disponibili. Nessun CD, D o sottotriangolo esiste ancora.",
"COMPOSITION → COMPLETION: il frame di opposizione angolo/base e DIVISION si integrano. Il blend può anticipare due coppie prospettiche senza crearle.",
"ELABORATION: una costruzione viene selezionata fra tre bisettrici possibili; il punteggio del blend può orientare la scelta.",
"COSTRUZIONE: il raggio bisettore interseca il lato non incidente; il punto nuovo e le due facce triangolari vengono realmente aggiunti.",
"BOTTOM-UP: riconoscimento delle opposizioni nelle sottofigure; binding con i ruoli previsti oppure registrazione del disallineamento."];
$("story").textContent=headings[stage];
$("caption").innerHTML='<span class="pill">Goal: bisecare ∠'+r.goal_vertex+'</span>'+(stage>=3?'<span class="pill good">Punto nuovo creato dopo scelta</span>':'<span class="pill">Nessun nuovo punto materiale</span>');
if(stage===1&&r.preconstruction_blend){$("roles").innerHTML=r.preconstruction_blend.blended_space.correspondence_pairs.map((z,i)=>'<span class="pill">Coppia prospettica '+(i+1)+': settore '+z.angle_role.sector_slot+' ↔ porzione base '+z.opposite_side_role.side_slot+'</span>').join("")}
else if(stage>=3){$("roles").innerHTML=r.postconstruction_reading.observed_angle_side_oppositions.map(x=>'<span class="pill good">Angolo in '+x.angle_vertex+' ↔ lato '+x.side_opposite.join("")+'</span>').join("")}
else $("roles").innerHTML='<span class="pill">Nessun binding ancora istanziato</span>';
$("candidates").innerHTML=r.construction_candidates.map(x=>{let s=r.candidate_scores[x.origin_vertex];return '<tr><td>'+x.origin_vertex+(x.origin_vertex===r.chosen_operation.origin_vertex?' ✓':'')+'</td><td>'+x.destination_edge.join("")+'</td><td>'+s.goal_fit+'</td><td>'+s.role_fit+'</td><td>'+s.prospective_analogy+'</td></tr>'}).join("");
$("timeline").innerHTML=r.timeline.map((x,i)=>'<div class="step '+(i===stage?"selected":"")+'">'+i+'. '+x.stage+'</div>').join("");
$("summary").innerHTML=data.conditions.map(c=>{let a=data.aggregates[r.shape][r.goal_vertex][c];return '<tr><td>'+c+'</td><td>'+Math.round(100*a.prospective_rate)+'%</td><td>'+Math.round(100*a.goal_construction_rate)+'%</td><td>'+Math.round(100*a.successful_material_binding_rate)+'%</td></tr>'}).join("");
}
["shape","goal","condition","seed"].forEach(x=>$(x).addEventListener("change",render));
$("stage").addEventListener("input",render);render();
</script></body></html>"""


def main():
    data=json.loads((OUT/"traces.json").read_text(encoding="utf-8"))
    small={k:data[k] for k in ("schema","shapes","goals","conditions","aggregates")}
    small["seeds"]=data["seeds"][:10]
    small["runs"]=[r for r in data["runs"] if r["seed"] in small["seeds"]]
    payload=json.dumps(small,ensure_ascii=False,separators=(",",":")).replace("</","<\\/")
    (OUT/"viewer.html").write_text(HTML.replace("__DATA__",payload),encoding="utf-8")
    lines=["# Merovingio v8 — Prospective Double-Scope Blending",
         "",
         "Engineering test starting BEFORE the angle-bisector construction.",
         "The only frame primitives are TRIANGLE (opposite angle and nonincident side) and DIVISION (binary partition).",
         "A GENERAL polygon-face split rule predicts new cycles, not a stored TWO TRIANGLES frame.",
         "",
         "| Shape | Goal vertex | Condition | Seed count | Prospective blend | Correct construction | Bound after construction | False side equalities |",
         "|---|---|---|---:|---:|---:|---:|---:|"]
    for shape,goals in data["aggregates"].items():
        for goal,conds in goals.items():
            for condition,v in conds.items():
                lines.append("| "+" | ".join([
                    shape,goal,condition,str(v["n"]),str(v["prospective_rate"]),
                    str(v["goal_construction_rate"]),
                    str(v["successful_material_binding_rate"]),
                    str(v["false_metric_assertions"])])+" |")
    lines.extend([
        "",
        "## Limits and interpretation",
        "PROSPECTIVE means frame slots exist in a mental representation but their material objects are absent.",
        "CONSTRUCTED means the bisector operation was executed; the resulting two faces and opposite roles can be observed.",
        "PROVEN is NOT produced: in scalene triangles the bisector generally does not bisect the opposite segment.",
        "The proposed construction is a programmed geometry operator in a finite catalogue, not a free discovery from scratch.",
        "The simulated double-scope integration is hand-designed and cannot independently validate cognition or the historical process.",
        "No Jev/Vision calls were made.",
        ""])
    (OUT/"REPORT.md").write_text("\n".join(lines),encoding="utf-8")
    print("Created",OUT/"viewer.html",OUT/"REPORT.md")

if __name__=="__main__":main()

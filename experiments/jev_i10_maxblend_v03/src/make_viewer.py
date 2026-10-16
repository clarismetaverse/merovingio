"""Creates a self-contained offline interface; candidate figures remain local PNG assets."""
import json
from pathlib import Path

PAGE_HEAD=r'''<!doctype html><html lang="it"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Merovingio · I.10 | Max-Blend Lab</title>
<style>
:root{color-scheme:dark;font-family:Inter,system-ui,-apple-system,Segoe UI,sans-serif;background:#0b1422;color:#e9eff7}
*{box-sizing:border-box}body{margin:0}header{padding:34px max(5vw,20px) 26px;background:linear-gradient(120deg,#13243a,#0e1726);border-bottom:1px solid #293649}
.eyebrow{font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:#8fbecf}h1{font-size:clamp(24px,4vw,38px);margin:10px 0 10px;letter-spacing:-.04em}
p{color:#afbece;line-height:1.55;font-size:14px;max-width:900px;margin:10px 0}main{margin:22px auto;max-width:1280px;padding:0 22px}
.layout{display:grid;grid-template-columns:minmax(0,1.45fr) minmax(280px,.8fr);gap:20px}.panel{border:1px solid #334256;background:#101b2c;border-radius:15px;overflow:hidden}
.pan{padding:20px}.muted{color:#9aaec5}.meta{font-size:12px;color:#aebbd0}.title{font-size:15px;font-weight:700;margin:0 0 14px}
.screen{display:block;width:100%;height:auto;max-height:510px;object-fit:contain;background:#0c1422}
.options{display:grid;grid-template-columns:repeat(5,minmax(100px,1fr));gap:10px;margin:18px 0}
.option{cursor:pointer;border:1px solid #34465b;background:#142338;padding:8px;border-radius:10px;text-align:left;color:#dbe4f0}
.option.sel{border-color:#a38aff;background:#222646;box-shadow:0 0 0 1px #a38aff4b}.option img{width:100%;aspect-ratio:1.12;object-fit:cover;border-radius:5px}
.tag{font-size:10px;letter-spacing:.04em;text-transform:uppercase;color:#a9bed1}.score{font-size:30px;font-weight:700;letter-spacing:-.04em;margin-top:6px}
small{color:#97a9bb}.pill{font-size:11px;border:1px solid #41607a;border-radius:999px;padding:4px 8px;margin:3px;display:inline-block;color:#bdcee0}
.dash{border-top:1px solid #2c3b4f;margin:14px 0}.row{display:flex;justify-content:space-between;align-items:center;gap:12px}
.details{font-size:13px;line-height:1.55;color:#c2d0e1}code{font-family:ui-monospace,Menlo,Consolas,monospace;color:#ae9bff}
.stage{display:flex;gap:5px;flex-wrap:wrap;margin:12px 0}.stage button{border:1px solid #34465b;background:#15253a;color:#e9eff7;padding:8px 13px;border-radius:8px;cursor:pointer}.stage button.active{border-color:#9e85ee;background:#28254d}
.note{font-size:12px;padding:11px 13px;border-radius:9px;background:#15273a;border:1px solid #29435a;margin-top:16px;color:#c2d0e1}
footer{padding:10px 22px 32px;color:#8d9bae;font-size:12px}
@media(max-width:900px){.layout{grid-template-columns:1fr}.options{grid-template-columns:repeat(3,1fr)}}
@media(max-width:480px){.options{grid-template-columns:repeat(2,1fr)}}
</style></head><body>
<header><div class="eyebrow">Merovingio · Panoptikon / visual construction search</div>
<h1>Euclide I.10 — Max-Blend, non dimostrazione</h1>
<p>Tre mental spaces iniziali: segmento, angolo al vertice, triangolo equilatero. Proponiamo costruzioni geometriche, osserviamo quali nuovi gruppi misti producono e confrontiamo la loro compatibilità strutturale. Non viene fornito alcun obiettivo di prova.</p></header>
<main><div class="layout">
<section class="panel"><div class="pan"><div class="row"><span class="title">Workspace ipotetico</span><span class="meta" id="selected">C01</span></div>
<div class="stage"><button data-stage="initial" onclick="stageSelect('initial')">1 · Figura iniziale</button><button data-stage="bridge" onclick="stageSelect('bridge')">2 · Costruzione</button><button data-stage="groups" onclick="stageSelect('groups')">3 · Regrouping</button></div><img class="screen" id="scene" alt="Diagramma geometrico" src="images/C01.png"/>
<div class="options" id="options"></div>
<div class="note">Le figure sono disegni esatti nella simulazione, ma l'allineamento visivo o numerico <b>non equivale a una dimostrazione</b>. Non viene applicato alcun criterio di congruenza.</div>
</div></section>
<aside class="panel"><div class="pan">
<div class="eyebrow">Baseline esplicita — non Jev</div>
<div class="title" style="margin-top:8px">Valore del blending strutturale</div>
<div class="score" id="score"></div><small id="rank"></small><div class="dash"></div>
<div class="title">Partizioni e generatori</div><div class="details" id="groups"></div><div class="dash"></div>
<div class="title">Corrispondenze candidate</div><div class="details" id="rels"></div><div class="dash"></div>
<div class="title">Generic Spaces possibili</div><div class="details" id="generic"></div><div class="dash"></div>
<div class="title">Ruoli multipli</div><div class="details" id="roles"></div><div class="dash"></div>
<div class="title">Provenienza costruttiva</div><div class="details" id="history"></div>
</div></aside>
</div></main><footer>Output sperimentale locale · Nessuna chiamata Jev eseguita · Nessun goal fornito al ranking</footer>
<script>const RESULTS='''
PAGE_TAIL=r''';
let selected=RESULTS[0].id; let stage='groups';
const ranked=[...RESULTS].sort((a,b)=>b.heuristic_blend_value-a.heuristic_blend_value);
function esc(v){return String(v).replaceAll('&','&amp;').replaceAll('<','&lt;')}
function line(s){return `<div style="margin:6px 0">${esc(s)}</div>`}
function stageSelect(v){stage=v;select(selected);}
function select(id){
 selected=id;const r=RESULTS.find(x=>x.id===id);
 document.querySelector('#scene').src=stage==='initial'?'images/initial.png':(stage==='bridge'?`images/${id}_raw.png`:`images/${id}.png`);
 document.querySelectorAll('.stage button').forEach(x=>x.classList.toggle('active',x.dataset.stage===stage));
 document.querySelector('#selected').textContent=id;
 document.querySelector('#score').textContent=r.heuristic_blend_value.toFixed(3);
 document.querySelector('#rank').textContent=`Posizione baseline: ${ranked.findIndex(x=>x.id===id)+1}/${RESULTS.length}. Punteggio euristico, non probabilità.`;
 document.querySelector('#groups').innerHTML=r.groups.length?r.groups.map(x=>line(`${x.id} — confini: ${(x.boundary||[]).join('–')} · generatore: ${x.generator}`)).join(''):'Nessuna coppia triangolare interna generata.';
 document.querySelector('#rels').innerHTML=r.correspondences.length?r.correspondences.map(x=>line(`${x.role}: ${x.left} ↔ ${x.right} · ${x.support}${x.gap_degrees!==undefined?` (gap ${x.gap_degrees}°)`:''}`)).join(''):'Nessuna corrispondenza triangolare diretta.';
 document.querySelector('#generic').innerHTML=r.candidate_generic_spaces.map(x=>line(`${x.id} [${x.status}] · indotto da ${x.generator}`)).join('');
 document.querySelector('#roles').innerHTML=Object.entries(r.object_interpretations).map(([k,v])=>line(`${k}: ${v.map(x=>x.role).join(' · ')}`)).join('');
 document.querySelector('#history').innerHTML=r.construction_timeline.map(x=>line(`${x.order}. ${x.event} [${x.status}]`)).join('');
 document.querySelectorAll('.option').forEach(x=>x.classList.toggle('sel',x.dataset.id===id));
}
document.querySelector('#options').innerHTML=RESULTS.map(x=>`<button class="option" data-id="${x.id}" onclick="select('${x.id}')"><img src="images/${x.id}.png" alt="${x.id}"/><div class="row"><b>${x.id}</b><span class="tag">${x.heuristic_blend_value.toFixed(2)}</span></div></button>`).join('');select(selected);
</script></body></html>'''

def main(out:Path):
    results=json.loads((out/'results.json').read_text())['candidates']
    html=PAGE_HEAD+json.dumps(results,ensure_ascii=False).replace('</','<\\/')+PAGE_TAIL
    (out/'index.html').write_text(html,encoding='utf-8')
    print('Created viewer:',out/'index.html')
if __name__=='__main__':
    import sys
    main(Path(sys.argv[1]) if len(sys.argv)>1 else Path('output'))
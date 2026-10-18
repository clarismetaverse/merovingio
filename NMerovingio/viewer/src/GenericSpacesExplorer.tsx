import { useMemo, useState } from 'react'
import sample from '../../graph/examples/generic_spaces_v0_8.json'

type PointName = 'A' | 'B' | 'C' | 'D'
type Stage = 0 | 1 | 2
type Origin = 'memory' | 'induced' | 'blend'
type Role = {
  id: string
  label: string
  left: string
  right: string
  left_object: string | null
  right_object: string | null
  available_at: number
}
type Gap = {
  id: string
  title: string
  resolved_at: number | null
  proposal: string
  evidence: string
}
type GS = {
  id: string
  name: string
  source: Origin
  family: string
  activation_stage: number
  statuses: [string, string, string]
  mental_spaces: string[]
  description: string
  roles: Role[]
  missing: Gap[]
  salience: { context: [number, number, number]; generative: [number, number, number] }
  genealogical_sources: string[]
  epistemic_status: string
}
type Fixture = {
  meta: { project: string; version: string; purpose: string; epistemic_note: string; provenance: string }
  points: Record<PointName, [number, number]>
  stages: { id: string; label: string; description: string }[]
  mental_spaces: { id: string; label: string; objects: string[]; origin: string; available_at?: number }[]
  generic_spaces: GS[]
}
const model = sample as unknown as Fixture
type Ranking = 'context' | 'generative'

const ORIGIN: Record<Origin, string> = {
  memory: 'Richiamato',
  induced: 'Indotto',
  blend: 'Emergente dal blend',
}

const { A, B, C, D } = model.points

function score(space: GS, stage: Stage, ranking: Ranking): number {
  return space.salience[ranking][stage]
}

function segmentsOf(id: string): [PointName, PointName][] {
  const byId: Record<string, [PointName, PointName][]> = {
    AB: [['A', 'B']], AD: [['A', 'D']], DB: [['D', 'B']],
    CA: [['C', 'A']], CB: [['C', 'B']], CD: [['C', 'D']],
    C: [], D: [], A: [], B: [],
    angleACD: [['C', 'A'], ['C', 'D']],
    angleDCB: [['C', 'D'], ['C', 'B']],
    angleACB: [['C', 'A'], ['C', 'B']],
  }
  return byId[id] || []
}
function keyPair(a: PointName, b: PointName): string {
  return [a, b].sort().join('-')
}
const baseEdges: [PointName, PointName][] = [['A', 'B'], ['A', 'C'], ['B', 'C']]

function GeometryPanel({ stage, selected, focusedRole, preview }: {
  stage: Stage; selected: GS; focusedRole: Role | null; preview: boolean
}) {
  const color = { left: '#E9AF64', right: '#5EC7C0' }
  const highlighted = new Map<string, string>()
  const hotPoints = new Set<string>()

  if (focusedRole && focusedRole.available_at <= stage) {
    for (const [objectId, tint] of [
      [focusedRole.left_object, color.left],
      [focusedRole.right_object, color.right],
    ] as [string | null, string][]) {
      if (!objectId) continue
      if (objectId.length === 1) hotPoints.add(objectId)
      for (const [a, b] of segmentsOf(objectId)) {
        highlighted.set(keyPair(a, b), highlighted.has(keyPair(a, b)) ? '#BDA4FF' : tint)
      }
    }
  }

  const selectedPair = selected.id === 'GS_PAIR_ADJACENT' || selected.id === 'GS_SIDE_ANGLE'
  const hasRegions = stage >= 1 && (selectedPair || selected.id === 'GS_MULTIPLE_ROLE')
  const isGhost = preview && selected.id === 'GS_PARALLEL_TRANSPORT'

  const pointAt = (name: PointName) => model.points[name]
  return (
    <section className="gv-panel gv-workspace" aria-label="Workspace geometrico">
      <div className="gv-panelheading">
        <div>
          <span className="gv-kicker">01 · ISTANZIAZIONE</span>
          <h2>Workspace geometrico</h2>
        </div>
        <span className="gv-smalltag">identità preservata</span>
      </div>
      <svg viewBox="0 0 600 460" role="img" aria-label="Triangolo ABC e, dopo la costruzione, segmento CD con due Mental Spaces adiacenti">
        <defs>
          <linearGradient id="workspace-light" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stopColor="#131D2B" />
            <stop offset="100%" stopColor="#0C1220" />
          </linearGradient>
        </defs>
        <rect x="0" y="0" width="600" height="460" rx="16" fill="url(#workspace-light)"/>
        {hasRegions && (
          <>
            <polygon points="95,355 300,44 300,355" fill="#E9AF64" fillOpacity=".12" />
            <polygon points="300,44 505,355 300,355" fill="#5EC7C0" fillOpacity=".12" />
          </>
        )}
        {(stage >= 1 ? [...baseEdges, ['C','D'] as [PointName,PointName]] : baseEdges).map(([a,b]) => {
          const tint=highlighted.get(keyPair(a,b))
          return (
            <line key={a+b} x1={pointAt(a)[0]} y1={pointAt(a)[1]}
              x2={pointAt(b)[0]} y2={pointAt(b)[1]}
              stroke={tint || (a==='C' && b==='D' ? '#BDA4FF' : '#D5DFEE')}
              strokeWidth={tint ? 7 : a==='C' && b==='D' ? 4.5 : 3}
              strokeLinecap="round" />
          )
        })}
        {stage >= 1 && focusedRole && (
          <>
            {focusedRole.left_object==='AD' && <line x1={A[0]} y1={A[1]} x2={D[0]} y2={D[1]} stroke={color.left} strokeWidth={7}/>}
            {focusedRole.right_object==='DB' && <line x1={D[0]} y1={D[1]} x2={B[0]} y2={B[1]} stroke={color.right} strokeWidth={7}/>}
            {(focusedRole.left_object==='angleACD' || focusedRole.left_object==='angleACB') &&
              <path d="M 279 76 Q 295 100 300 101" stroke={color.left} strokeWidth="4" fill="none"/>}
            {focusedRole.right_object==='angleDCB' &&
              <path d="M 300 101 Q 315 100 321 76" stroke={color.right} strokeWidth="4" fill="none"/>}
          </>
        )}
        {isGhost && (
          <>
            <line x1="76" y1={C[1]} x2="524" y2={C[1]} stroke="#E9AF64" strokeWidth="3" strokeDasharray="9 8" opacity=".95"/>
            <text x="352" y="33" fill="#E9AF64" fontSize="12">proposta · NON costruita</text>
          </>
        )}
        {hasRegions && <><text x="185" y="270" className="gv-regionlabel" fill={color.left}>MS SINISTRO</text><text x="348" y="270" className="gv-regionlabel" fill={color.right}>MS DESTRO</text></>}
        {(['A','B','C',...(stage >=1 ? ['D'] : [])] as PointName[]).map(name => {
          const [x,y] = pointAt(name)
          const displacements: Record<PointName,[number,number]> = {
            A: [-26,18], B: [14,18], C: [-6,-18], D: [10,18]
          }
          const [dx,dy] = displacements[name]
          return (
            <g key={name}>
              <circle cx={x} cy={y} r={hotPoints.has(name) ? 7 : 5}
                fill={hotPoints.has(name) ? '#E9AF64' : '#EEF4FA'}/>
              <text x={x+dx} y={y+dy} className="gv-pointlabel">{name}</text>
            </g>
          )
        })}
        {stage===0 && <text x="300" y="422" fill="#8190A4" fontSize="13" textAnchor="middle">Il ponte CD non esiste ancora</text>}
        {stage>=1 && <text x="300" y="422" fill="#8190A4" fontSize="13" textAnchor="middle">CD è un unico carrier materiale con più interpretazioni</text>}
      </svg>
      <div className="gv-legend">
        <span><i className="gv-dot gv-amber"/>Mental Space L</span>
        <span><i className="gv-dot gv-cyan"/>Mental Space R</span>
        <span><i className="gv-dot gv-purple"/>Carrier mediale</span>
        <span><i className="gv-dash"/>Costruzione ipotetica</span>
      </div>
    </section>
  )
}

function AbstractPanel({selected,stage,focus,onFocus}:{
 selected:GS;stage:Stage;focus:string|null;onFocus:(next:string|null)=>void
}) {
 const inactive=selected.activation_stage>stage
 return (
  <section className="gv-panel gv-generic" aria-label="Generic Space astratto">
    <div className="gv-panelheading">
      <div><span className="gv-kicker">02 · ASTRAZIONE</span><h2>Generic Space</h2></div>
      <span className={'gv-origin gv-' + selected.source}>{ORIGIN[selected.source]}</span>
    </div>
    <div className="gv-generic-header">
      <strong>{selected.name}</strong>
      <small>{selected.family}</small>
    </div>
    <div className={'gv-abstract ' + (inactive ? 'gv-unborn' : '')}>
      <div className="gv-abstract-head">
        <span>Ruoli nel dominio L</span>
        <span>Allineamento</span>
        <span>Ruoli nel dominio R</span>
      </div>
      {selected.roles.map(role=>{
        const unresolved=role.available_at>stage
        const active=focus===role.id
        return (
          <button key={role.id}
            className={'gv-role-row ' + (unresolved?'gv-role-missing ':'') + (active?'gv-role-active':'')}
            onMouseEnter={()=>onFocus(role.id)}
            onMouseLeave={()=>onFocus(null)}
            onFocus={()=>onFocus(role.id)}
            onBlur={()=>onFocus(null)}
            onClick={()=>onFocus(active?null:role.id)}
            aria-label={'Evidenzia ruolo '+role.label}
            title={role.label + (unresolved?' — non ancora istanziato':' — corrispondenza candidata')}>
            <div className="gv-role-side"><b>{role.left}</b><small>{unresolved?'slot atteso':role.left_object||'ruolo non materializzato'}</small></div>
            <div className="gv-role-middle"><span>{role.label}</span><div className={unresolved?'gv-bridge-line gv-bridge-empty':'gv-bridge-line'}/></div>
            <div className="gv-role-side gv-role-right"><b>{role.right}</b><small>{unresolved?'slot atteso':role.right_object||'ruolo non materializzato'}</small></div>
          </button>
        )
      })}
      {inactive && <div className="gv-pending">Questa astrazione non è ancora emersa nel workspace</div>}
    </div>
    <p className="gv-epistemic">Le linee fra ruoli rappresentano analogie proposte, non uguaglianze di lunghezze o angoli.</p>
    <div className="gv-missing">
      <h3>Ruoli ancora mancanti</h3>
      {selected.missing.length===0
        ? <p>Nessun ruolo costruttivo mancante nel modello attuale. La validità metrica rimane aperta.</p>
        : selected.missing.map(gap=>(
          <div key={gap.id} className={gap.resolved_at!==null && gap.resolved_at<=stage?'gv-gap gv-resolved':'gv-gap'}>
            <span>{gap.resolved_at!==null && gap.resolved_at<=stage?'✓ realizzato':'◇ ancora aperto'}</span>
            <strong>{gap.title}</strong>
            <small>{gap.proposal}</small>
          </div>
        ))
      }
    </div>
  </section>
 )
}

export default function GenericSpacesExplorer(){
  const [stage,setStage] = useState<Stage>(0)
  const [selectedId,setSelectedId] = useState('GS_PAIR_ADJACENT')
  const [ranking,setRanking] = useState<Ranking>('context')
  const [focusedRoleId,setFocusedRoleId] = useState<string|null>(null)
  const [preview,setPreview] = useState(false)

  const sorted=useMemo(()=>[...model.generic_spaces].sort((a,b)=>score(b,stage,ranking)-score(a,stage,ranking)),[stage,ranking])
  const selected=model.generic_spaces.find(x=>x.id===selectedId) || model.generic_spaces[0]
  const focused=selected.roles.find(x=>x.id===focusedRoleId) || null
  const pending=selected.missing.some(x=>x.resolved_at===null || x.resolved_at>stage)
  return (
    <main className="gv-app">
      <header className="gv-topbar">
        <div>
          <div className="gv-kicker">MEROVINGIO / PANOPTIKON · v0.8</div>
          <h1>Generic Space Explorer</h1>
          <p>Tra figura concreta, astrazione richiamata e blending emergente.</p>
        </div>
        <div className="gv-links"><a href="./workspace.html">Workspace Atlas ↗</a><a href="./index.html">Grafo cognitivo ↗</a></div>
      </header>
      <nav className="gv-timeline" aria-label="Sequenza costruttiva">
        {model.stages.map((item,index)=>(
          <button type="button" key={item.id} className={stage===index?'gv-stage-active':''}
            onClick={()=>{setStage(index as Stage);setFocusedRoleId(null);setPreview(false)}}>
            <span className="gv-stagecircle">{index+1}</span>{item.label}
          </button>
        ))}
        <p>{model.stages[stage].description}</p>
      </nav>
      <div className="gv-grid">
        <aside className="gv-sidebar" aria-label="Generic Spaces e ranking">
          <div className="gv-asideheading"><span className="gv-kicker">REPERTORIO ATTIVO</span><strong>Generic Spaces <small>{model.generic_spaces.length}</small></strong></div>
          <div className="gv-segment" role="group" aria-label="Modalità di ranking">
            <button className={ranking==='context'?'active':''} onClick={()=>setRanking('context')}>Rilevanza</button>
            <button className={ranking==='generative'?'active':''} onClick={()=>setRanking('generative')}>Potenziale</button>
          </div>
          <p className="gv-asidenote">Salienza dimostrativa: pesi di esempio, non punteggi Jev.</p>
          <div className="gv-space-list">
            {sorted.map((space,index)=>(
              <button type="button" key={space.id} className={'gv-space-card '+(selected.id===space.id?'active ':'')+(stage<space.activation_stage?'latent':'')}
                onClick={()=>{setSelectedId(space.id);setFocusedRoleId(null);setPreview(false)}}>
                <div className="gv-space-top"><span>#{index+1}</span><span className={'gv-source gv-'+space.source}>{ORIGIN[space.source]}</span></div>
                <strong>{space.name}</strong>
                <small>{space.statuses[stage]}</small>
                <div className="gv-score-line"><span style={{width:(score(space,stage,ranking)*100)+'%'}}/></div>
                <em>{Math.round(score(space,stage,ranking)*100)}/100</em>
              </button>
            ))}
          </div>
          <div className="gv-asidenote gv-footer-note">Un Generic Space può essere recuperato prima che esistano gli oggetti necessari a istanziarlo.</div>
        </aside>
        <div className="gv-canvas">
          <GeometryPanel stage={stage} selected={selected} focusedRole={focused} preview={preview}/>
          <AbstractPanel selected={selected} stage={stage} focus={focusedRoleId} onFocus={setFocusedRoleId}/>
        </div>
        <aside className="gv-inspector">
          <span className="gv-kicker">03 · GENEALOGIA</span>
          <h2>{selected.name}</h2>
          <span className={'gv-origin gv-'+selected.source}>{ORIGIN[selected.source]}</span>
          <p>{selected.description}</p>
          <section>
            <h3>Stato al tempo {stage+1}</h3>
            <div className="gv-status">{selected.statuses[stage]}</div>
            <p>{selected.epistemic_status}</p>
          </section>
          <section>
            <h3>Mental Spaces coinvolti</h3>
            {selected.mental_spaces.map(id=>{
              const space=model.mental_spaces.find(x=>x.id===id)
              return <div key={id} className="gv-concept-tag">{space?.label||id} <span>{space?.available_at!==undefined && space.available_at>stage?'futuro':'attivo'}</span></div>
            })}
          </section>
          <section>
            <h3>Provenienza concettuale</h3>
            <ol>{selected.genealogical_sources.map(s=><li key={s}>{s}</li>)}</ol>
          </section>
          {pending && <section className="gv-proposal">
            <h3>Prospective blending</h3>
            <p>La struttura nota suggerisce quali ruoli mancano e come potrebbe essere trasformato il workspace.</p>
            {selected.missing.filter(x=>x.resolved_at===null||x.resolved_at>stage).map(x=>(
              <p key={x.id}><strong>{x.title}:</strong> {x.proposal}</p>
            ))}
            {selected.id==='GS_PARALLEL_TRANSPORT' &&
              <button type="button" onClick={()=>setPreview(!preview)} aria-pressed={preview}>
                {preview?'Nascondi proposta':'Mostra costruzione fantasma'}
              </button>
            }
          </section>}
          <section className="gv-safety"><h3>Stato epistemico</h3>
            <p>Fixture concettuale illustrativa. Nessuna uguaglianza geometrica è dimostrata, nessun ranking è una risposta live di Jev e le costruzioni fantasma non sono applicate al workspace.</p>
          </section>
        </aside>
      </div>
    </main>
  )
}

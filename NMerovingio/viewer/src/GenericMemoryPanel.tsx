import { useMemo, useState } from 'react'
import { contexts, memoryEntries, recall, families, type ContextKey, type RecallResult } from './generic-memory'

type Stage = 0 | 1 | 2
const TIME_CONTEXT: ContextKey[] = ['initial','partition','reinterpretation']
const historicalContextOptions: ContextKey[] = ['circle','side_transfer']

export default function GenericMemoryPanel({ stage }: {stage:Stage}){
  const [override,setOverride] = useState<ContextKey | 'stage'>('stage')
  const [selection,setSelection] = useState<string|null>(null)
  const [filter,setFilter] = useState<'all'|'workspace_abstraction'|'proposition_catalog_pattern'>('all')
  const key:ContextKey=override==='stage' ? TIME_CONTEXT[stage] : override
  const matches=useMemo(()=>recall(contexts[key].features).filter(x=>filter==='all'||x.item.kind===filter),[key,filter])
  const selected=(matches.find(x=>x.item.id===selection)||matches[0]) as RecallResult|undefined
  const familys=useMemo(()=>families(),[])
  return (
    <section className="gm-panel" id="historical-generic-memory">
      <div className="gm-heading">
        <div><span className="gv-kicker">04 · MEMORIA INTER-WORKSPACE</span><h3>Generic Spaces ricordati</h3></div>
        <strong>{memoryEntries.length} schemi</strong>
      </div>
      <p className="gm-explain">Recupero deterministico basato su ruoli e strutture di workspace documentati.
        Non è ancora un ranking Jev né prova di trasferimento geometrico.</p>
      <label className="gm-label" htmlFor="gm-context">Workspace o focus da confrontare</label>
      <select id="gm-context" value={override} onChange={event=>{setOverride(event.target.value as ContextKey|'stage');setSelection(null)}}>
        <option value="stage">Segui lo stadio corrente · {contexts[TIME_CONTEXT[stage]].title}</option>
        {historicalContextOptions.map(id=><option key={id} value={id}>{contexts[id].title}</option>)}
      </select>
      <div className="gm-features" aria-label="Ruoli disponibili nel workspace">
        {contexts[key].features.map(tag=><span key={tag}>{tag.replaceAll('_',' ')}</span>)}
      </div>
      <div className="gm-switch" role="group" aria-label="Tipo della fonte">
        <button className={filter==='all'?'active':''} onClick={()=>{setFilter('all');setSelection(null)}}>Tutti</button>
        <button className={filter==='workspace_abstraction'?'active':''} onClick={()=>{setFilter('workspace_abstraction');setSelection(null)}}>Workspace</button>
        <button className={filter==='proposition_catalog_pattern'?'active':''} onClick={()=>{setFilter('proposition_catalog_pattern');setSelection(null)}}>Teoremi</button>
      </div>
      <div className="gm-list">
        {matches.length === 0 ? <p>Nessuna corrispondenza. Il motore non inventa nuovi teoremi.</p> : matches.map((r,index)=>
          <button key={r.item.id} className={'gm-match '+(selected?.item.id===r.item.id?'selected':'')}
            onClick={()=>setSelection(r.item.id)}>
            <span className="gm-rank">#{index+1} · {Math.round(r.score*100)} / 100</span>
            <strong>{r.item.name}</strong>
            <small>{r.item.provenance.proposition_id || r.item.provenance.workspace_id}</small>
            <div className="gm-track"><i style={{width:(r.score*100)+'%'}}/></div>
          </button>
        )}
      </div>
      {selected && <div className="gm-details">
        <div className="gm-status">
          <span>{selected.status==='structural_match'?'Firma completa':'Firma parziale'}</span>
          <span>{selected.item.kind==='workspace_abstraction'?'Da workspace':'Da proposizione catalogata'}</span>
        </div>
        <h4>{selected.item.name}</h4>
        <p>{selected.item.genealogical_note}</p>
        <div className="gm-compare">
          <div><strong>Ruoli corrispondenti</strong>{selected.overlap.map(x=><span className="gm-hit" key={x}>✓ {x.replaceAll('_',' ')}</span>)}</div>
          <div><strong>Ruoli assenti / prospettici</strong>{selected.missing.length?selected.missing.map(x=><span className="gm-miss" key={x}>◇ {x.replaceAll('_',' ')}</span>):<span className="gm-muted">Nessuno nella firma; le relazioni metriche restano da verificare</span>}</div>
        </div>
        <h4>Generic Space astratto dal precedente</h4>
        <div className="gm-roles">
          {selected.item.abstract_roles.map(role=>
            <div className="gm-role" key={role.role}>
              <span>{role.role.replaceAll('_',' ')}</span>
              <strong>{role.relation.replaceAll('_',' ')}</strong>
              <small>{role.source_objects.join(' · ')}</small>
            </div>
          )}
        </div>
        <h4>Genealogia / fonte verificabile</h4>
        <code>{selected.item.provenance.file}</code>
        <div className="gm-source">
          <span>{selected.item.provenance.workspace_id||selected.item.provenance.proposition_id}</span>
          <a href={'https://github.com/clarismetaverse/merovingio/blob/experiment/generic-space-memory-v0.9/'+selected.item.provenance.file}
            target="_blank" rel="noopener noreferrer">Apri fonte GitHub ↗</a>
        </div>
        <p className="gm-warning">{selected.explanation}. {selected.item.metric_status.replaceAll('_',' ')}.</p>
        <small className="gm-muted">Famiglie distinte per firma: {familys.length}. Identità materiale e genealogie NON collassate.</small>
      </div>}
    </section>
  )
}

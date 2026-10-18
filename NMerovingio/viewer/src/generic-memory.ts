/** Generic Space memory: deterministic, non-proof graph/relation recall.
 * Source signatures are explicit abstractions from repository fixtures and
 * proposition catalogue. Never interpret retrieval as geometric certification.
 */
import memoryJson from '../../graph/generic_space_memory_v0_9.json'

export type MemoryItem = {
  id: string
  name: string
  kind: 'workspace_abstraction' | 'proposition_catalog_pattern'
  provenance: {
    file: string
    workspace_id: string | null
    proposition_id: string | null
    node_ids: string[]
    source_kind: string
    status: string
  }
  tags: string[]
  goal_tags: string[]
  abstract_roles: {role:string;source_objects:string[];relation:string}[]
  genealogical_note: string
  interpretation: string
  metric_status: string
  memory_status: string
  conservation: string
}
export const memoryEntries = (memoryJson.entries as MemoryItem[])

export type ContextKey = 'initial' | 'partition' | 'reinterpretation' | 'circle' | 'side_transfer'

/** Feature observations are tagged with their origin, not logical truths. */
export const contexts: Record<ContextKey, {title:string;features:string[];motivation:string}> = {
  initial: {
    title:'ABC — figura iniziale',
    features:['triangle','angle_sector','base_segment'],
    motivation:'Riconoscere schemi recuperabili prima di costruire CD'
  },
  partition: {
    title:'CD — partizione in due regioni',
    features:['triangle','medial_carrier','shared_side','partition_two_regions','paired_triangles'],
    motivation:'Richiamo per analogia topologica a ponte condiviso'
  },
  reinterpretation: {
    title:'CD — reinterpretazione multi-ruolo',
    features:['triangle','medial_carrier','shared_side','partition_two_regions','multi_role_carrier','co_constitution','provenance_reinterpretation','role_alignment'],
    motivation:'Richiamo genealogico e pluralità dei ruoli del carrier'
  },
  circle: {
    title:'Due circonferenze — workspace storico',
    features:['circle','two_circles','radius','triangle','common_reference','intersection','equilateral'],
    motivation:'Test di recupero cross-workspace'
  },
  side_transfer: {
    title:'I.5 — rapporto lato / angolo',
    features:['isosceles','side_equality','opposite_angle','relation_transfer'],
    motivation:'Pattern di proposizione catalogata, non dimostrazione importata'
  }
}
export type RecallResult = {
  item: MemoryItem
  score: number
  overlap: string[]
  missing: string[]
  status: 'partial_match' | 'structural_match'
  explanation: string
}

/** Role matching + bounded salience proxy; no Jev predictions. */
export function recall(features: string[], pool: MemoryItem[] = memoryEntries): RecallResult[] {
  const have = new Set(features)
  return pool.map(item => {
    const required = [...new Set(item.tags)]
    const overlap = required.filter(k => have.has(k))
    const missing = required.filter(k => !have.has(k))
    const goal = [...new Set(item.goal_tags)]
    const relevantGoals = goal.filter(k => have.has(k)).length
    const matchCoverage = overlap.length / Math.max(1, required.length)
    const relevance = relevantGoals / Math.max(1, goal.length)
    // Mild reward for actionable *partial* templates, not for proof.
    const prospective = missing.length > 0 && overlap.length > 0 ? 0.05 : 0
    const score = Math.min(1, +(0.7*matchCoverage+0.25*relevance+prospective).toFixed(3))
    return {
      item,score,overlap,missing,
      status: missing.length ? 'partial_match' as const : 'structural_match' as const,
      explanation: missing.length ? 'Schema richiamato: ruoli mancanti non certificati' : 'Match della firma concettuale: non è una prova'
    }
  }).filter(x => x.overlap.length > 0)
    .sort((a,b)=>b.score-a.score || a.item.id.localeCompare(b.item.id))
}
/** Group by structural tag signature but never merge source identities or genealogies. */
export function families(pool:MemoryItem[]=memoryEntries) {
  const grouped = new Map<string,MemoryItem[]>()
  for(const x of pool){
    const signature=[...new Set(x.tags)].sort().join('|')
    grouped.set(signature,[...(grouped.get(signature)||[]),x])
  }
  return [...grouped].map(([signature,members])=>({
    signature, members:members.map(x=>x.id),
    provenances: members.map(x=>x.provenance.file),
    genealogy_collapsed:false
  }))
}

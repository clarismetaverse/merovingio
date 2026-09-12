import { useEffect, useMemo, useRef, useState } from 'react'
import cytoscape, { type Core, type ElementDefinition } from 'cytoscape'

import entitiesJson from '../../graph/entities_v1.json'
import edgesJson from '../../graph/edges_v1.json'
import genealogyJson from '../../graph/genealogy_v1.json'
import snapshotsJson from '../../graph/snapshots_v1.json'

type AnyRecord = Record<string, any>

type Entity = AnyRecord & {
  id: string
  type: string
  name: string
  level?: string
  evidence?: { status?: string; source_files?: string[]; notes?: string }
}

type GraphEdge = AnyRecord & {
  id: string
  source: string
  target: string
  type: string
  run_introduced?: string
  evidence?: { status?: string }
}

type Snapshot = AnyRecord & {
  id: string
  after_run?: string | null
  active_entities?: string[]
  active_families?: string[]
  active_invariants?: string[]
  open_questions?: string[]
  notes?: string
}

const entities = (entitiesJson as AnyRecord).entities as Entity[]
const edges = (edgesJson as AnyRecord).edges as GraphEdge[]
const genealogies = (genealogyJson as AnyRecord).genealogies as AnyRecord[]
const snapshots = (snapshotsJson as AnyRecord).snapshots as Snapshot[]

const entityById = new Map(entities.map((entity) => [entity.id, entity]))

const epistemicColor: Record<string, string> = {
  SEED: '#7e8a9a',
  PROP_LICENSED: '#39c987',
  VALIDATED_COGNITIVE: '#69a7ff',
  COMPILED_COGNITIVE: '#8a7dff',
  CONDITIONALLY_VALIDATED: '#e9b949',
  COGNITIVE_CANDIDATE: '#f59f59',
  PROPOSAL: '#f59f59',
  OPEN: '#767b87',
}

const typeOrder = [
  'WORKSPACE',
  'GESTALT',
  'FAMILY',
  'ZERO_LOCUS',
  'REGISTER',
  'PROPOSITION',
  'OPERATOR',
  'AGENT',
  'IMPETUS',
]

function shortLabel(entity: Entity) {
  return entity.name || entity.id
}

function evidenceStatus(entity: Entity) {
  return entity.evidence?.status || 'OPEN'
}

function makeElements(): ElementDefinition[] {
  const validIds = new Set(entities.map((entity) => entity.id))

  const nodes: ElementDefinition[] = entities.map((entity) => ({
    data: {
      id: entity.id,
      label: shortLabel(entity),
      type: entity.type,
      level: entity.level || '',
      status: evidenceStatus(entity),
      color: epistemicColor[evidenceStatus(entity)] || '#767b87',
    },
  }))

  const graphEdges: ElementDefinition[] = edges
    .filter((edge) => validIds.has(edge.source) && validIds.has(edge.target))
    .map((edge) => ({
      data: {
        id: edge.id,
        source: edge.source,
        target: edge.target,
        label: edge.type,
        edgeType: edge.type,
        status: edge.evidence?.status || 'OPEN',
        run: edge.run_introduced || '',
      },
    }))

  return [...nodes, ...graphEdges]
}

function styleSheet(): any[] {
  return [
    {
      selector: 'node',
      style: {
        'background-color': 'data(color)',
        'border-width': 1.5,
        'border-color': '#d9e0ea',
        label: 'data(label)',
        color: '#f5f7fb',
        'font-size': 10,
        'font-family': 'Inter, ui-sans-serif, system-ui, sans-serif',
        'text-wrap': 'wrap',
        'text-max-width': 118,
        'text-valign': 'bottom',
        'text-margin-y': 7,
        width: 34,
        height: 34,
        'overlay-opacity': 0,
      },
    },
    { selector: 'node[type = "WORKSPACE"]', style: { shape: 'ellipse', width: 45, height: 45 } },
    { selector: 'node[type = "GESTALT"]', style: { shape: 'round-rectangle', width: 52, height: 38 } },
    { selector: 'node[type = "FAMILY"]', style: { shape: 'hexagon', width: 50, height: 50 } },
    { selector: 'node[type = "ZERO_LOCUS"]', style: { shape: 'diamond', width: 42, height: 42 } },
    { selector: 'node[type = "REGISTER"]', style: { shape: 'barrel', width: 40, height: 34 } },
    { selector: 'node[type = "PROPOSITION"]', style: { shape: 'rectangle', width: 35, height: 28 } },
    { selector: 'node[type = "OPERATOR"]', style: { shape: 'tag', width: 40, height: 32 } },
    { selector: 'node[type = "AGENT"]', style: { shape: 'round-diamond', width: 42, height: 42 } },
    { selector: 'node[type = "IMPETUS"]', style: { shape: 'vee', width: 42, height: 42 } },
    {
      selector: 'edge',
      style: {
        width: 1.2,
        'line-color': '#566070',
        'target-arrow-color': '#566070',
        'target-arrow-shape': 'triangle',
        'curve-style': 'bezier',
        label: 'data(label)',
        color: '#778091',
        'font-size': 7,
        'text-background-color': '#0b0d12',
        'text-background-opacity': 0.82,
        'text-background-padding': 2,
        'text-rotation': 'autorotate',
        'arrow-scale': 0.7,
      },
    },
    {
      selector: '.dimmed',
      style: {
        opacity: 0.09,
        'text-opacity': 0.05,
      },
    },
    {
      selector: '.active-snapshot',
      style: {
        opacity: 1,
        'text-opacity': 1,
        'border-width': 2.5,
        'border-color': '#ffffff',
      },
    },
    {
      selector: '.search-hit',
      style: {
        'border-width': 4,
        'border-color': '#ffe39a',
        'z-index': 999,
      },
    },
    {
      selector: ':selected',
      style: {
        'border-width': 4,
        'border-color': '#ffffff',
        'line-color': '#a9caff',
        'target-arrow-color': '#a9caff',
      },
    },
  ]
}

export default function App() {
  const containerRef = useRef<HTMLDivElement | null>(null)
  const cyRef = useRef<Core | null>(null)
  const [selectedId, setSelectedId] = useState<string | null>('G_TRIANGLE_ZERO')
  const [snapshotId, setSnapshotId] = useState<string>('ALL')
  const [query, setQuery] = useState('')
  const [visibleTypes, setVisibleTypes] = useState<Set<string>>(
    () => new Set(typeOrder.filter((type) => entities.some((entity) => entity.type === type))),
  )

  const elements = useMemo(() => makeElements(), [])
  const selectedEntity = selectedId ? entityById.get(selectedId) : undefined
  const selectedGenealogies = useMemo(
    () => genealogies.filter((genealogy) => genealogy.target === selectedId),
    [selectedId],
  )
  const selectedSnapshot = snapshots.find((snapshot) => snapshot.id === snapshotId)

  const incidentEdges = useMemo(() => {
    if (!selectedId) return []
    return edges.filter((edge) => edge.source === selectedId || edge.target === selectedId)
  }, [selectedId])

  useEffect(() => {
    if (!containerRef.current || cyRef.current) return

    const cy = cytoscape({
      container: containerRef.current,
      elements,
      style: styleSheet(),
      wheelSensitivity: 0.18,
      minZoom: 0.16,
      maxZoom: 3.2,
      layout: {
        name: 'cose',
        animate: false,
        fit: true,
        padding: 54,
        nodeRepulsion: 620000,
        idealEdgeLength: 115,
        edgeElasticity: 90,
        gravity: 0.28,
        numIter: 1200,
      } as any,
    })

    cy.on('tap', 'node', (event) => {
      setSelectedId(event.target.id())
    })

    cy.on('tap', (event) => {
      if (event.target === cy) setSelectedId(null)
    })

    cyRef.current = cy

    return () => {
      cy.destroy()
      cyRef.current = null
    }
  }, [elements])

  useEffect(() => {
    const cy = cyRef.current
    if (!cy) return

    cy.batch(() => {
      cy.nodes().forEach((node) => {
        const visible = visibleTypes.has(node.data('type'))
        node.style('display', visible ? 'element' : 'none')
      })
      cy.edges().forEach((edge) => {
        const sourceVisible = visibleTypes.has(edge.source().data('type'))
        const targetVisible = visibleTypes.has(edge.target().data('type'))
        edge.style('display', sourceVisible && targetVisible ? 'element' : 'none')
      })
    })
  }, [visibleTypes])

  useEffect(() => {
    const cy = cyRef.current
    if (!cy) return

    cy.elements().removeClass('dimmed active-snapshot')
    if (!selectedSnapshot) return

    const activeIds = new Set([
      ...(selectedSnapshot.active_entities || []),
      ...(selectedSnapshot.active_families || []),
    ])

    cy.nodes().forEach((node) => {
      if (activeIds.has(node.id())) node.addClass('active-snapshot')
      else node.addClass('dimmed')
    })

    cy.edges().forEach((edge) => {
      if (activeIds.has(edge.source().id()) && activeIds.has(edge.target().id())) {
        edge.addClass('active-snapshot')
      } else {
        edge.addClass('dimmed')
      }
    })
  }, [selectedSnapshot])

  useEffect(() => {
    const cy = cyRef.current
    if (!cy) return
    const normalized = query.trim().toLowerCase()
    cy.nodes().removeClass('search-hit')
    if (!normalized) return

    cy.nodes().forEach((node) => {
      const entity = entityById.get(node.id())
      const haystack = `${node.id()} ${entity?.name || ''} ${(entity?.semantic_aliases || []).join(' ')}`.toLowerCase()
      if (haystack.includes(normalized)) node.addClass('search-hit')
    })
  }, [query])

  function relayout() {
    cyRef.current?.layout({
      name: 'cose',
      animate: true,
      animationDuration: 650,
      fit: true,
      padding: 46,
      nodeRepulsion: 620000,
      idealEdgeLength: 115,
      edgeElasticity: 90,
      gravity: 0.28,
      numIter: 1000,
    } as any).run()
  }

  function fit() {
    cyRef.current?.fit(undefined, 42)
  }

  function toggleType(type: string) {
    setVisibleTypes((previous) => {
      const next = new Set(previous)
      if (next.has(type)) next.delete(type)
      else next.add(type)
      return next
    })
  }

  function focusNode(id: string) {
    const cy = cyRef.current
    if (!cy) return
    const node = cy.getElementById(id)
    if (!node.length) return
    node.select()
    setSelectedId(id)
    cy.animate({ center: { eles: node }, zoom: Math.max(cy.zoom(), 1.15) }, { duration: 320 })
  }

  return (
    <div className="app-shell">
      <header className="topbar">
        <div>
          <div className="eyebrow">MEROVINGIO / N9</div>
          <h1>Cognitive Graph Explorer</h1>
        </div>
        <div className="topbar-actions">
          <input
            className="search"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Search gestalt, family, zero…"
          />
          <button onClick={fit}>Fit</button>
          <button onClick={relayout}>Relayout</button>
        </div>
      </header>

      <div className="workspace-grid">
        <aside className="timeline-panel panel">
          <div className="panel-heading">
            <span>Evolution</span>
            <small>dry-run snapshots</small>
          </div>

          <button
            className={`timeline-item ${snapshotId === 'ALL' ? 'is-active' : ''}`}
            onClick={() => setSnapshotId('ALL')}
          >
            <span className="timeline-dot" />
            <span><strong>All</strong><small>full N9 graph</small></span>
          </button>

          {snapshots.map((snapshot) => (
            <button
              key={snapshot.id}
              className={`timeline-item ${snapshotId === snapshot.id ? 'is-active' : ''}`}
              onClick={() => setSnapshotId(snapshot.id)}
            >
              <span className="timeline-dot" />
              <span>
                <strong>{snapshot.id}</strong>
                <small>{snapshot.after_run || 'baseline'}</small>
              </span>
            </button>
          ))}

          <div className="divider" />
          <div className="filter-title">Entity layers</div>
          <div className="type-filters">
            {typeOrder.filter((type) => entities.some((entity) => entity.type === type)).map((type) => (
              <button
                key={type}
                className={`filter-chip ${visibleTypes.has(type) ? 'on' : ''}`}
                onClick={() => toggleType(type)}
              >
                {type.replace('_', ' ')}
              </button>
            ))}
          </div>

          <div className="divider" />
          <div className="legend">
            <div className="filter-title">Epistemic status</div>
            {Object.entries(epistemicColor).slice(0, 7).map(([status, color]) => (
              <div className="legend-row" key={status}>
                <span style={{ background: color }} />
                <small>{status}</small>
              </div>
            ))}
          </div>
        </aside>

        <main className="graph-panel panel">
          <div ref={containerRef} className="cytoscape-canvas" />
          {selectedSnapshot && (
            <div className="snapshot-card">
              <div className="snapshot-title">{selectedSnapshot.id}</div>
              <div>{selectedSnapshot.notes}</div>
              {!!selectedSnapshot.active_invariants?.length && (
                <div className="snapshot-meta">
                  {selectedSnapshot.active_invariants.slice(0, 2).map((item) => <span key={item}>{item}</span>)}
                </div>
              )}
            </div>
          )}
        </main>

        <aside className="inspector-panel panel">
          <div className="panel-heading">
            <span>Inspector</span>
            <small>{selectedEntity?.type || 'select a node'}</small>
          </div>

          {!selectedEntity ? (
            <div className="empty-state">
              Select a node to inspect its roles, evidence, genealogy and local connections.
            </div>
          ) : (
            <div className="inspector-content">
              <div className="entity-badge-row">
                <span className="entity-type">{selectedEntity.type}</span>
                <span
                  className="evidence-badge"
                  style={{ borderColor: epistemicColor[evidenceStatus(selectedEntity)] || '#767b87' }}
                >
                  {evidenceStatus(selectedEntity)}
                </span>
              </div>
              <h2>{selectedEntity.name}</h2>
              <code className="entity-id">{selectedEntity.id}</code>

              {!!selectedEntity.semantic_aliases?.length && (
                <section>
                  <h3>Semantic aliases</h3>
                  <div className="tag-row">
                    {selectedEntity.semantic_aliases.map((alias: string) => <span key={alias}>{alias}</span>)}
                  </div>
                </section>
              )}

              <section>
                <h3>Structure</h3>
                <pre>{JSON.stringify({
                  level: selectedEntity.level,
                  workspace_id: selectedEntity.workspace_id,
                  registers: selectedEntity.registers,
                  state: selectedEntity.state,
                  properties: selectedEntity.properties,
                  stable_region: selectedEntity.stable_region,
                  variation_axes: selectedEntity.variation_axes,
                }, null, 2)}</pre>
              </section>

              <section>
                <h3>Local connections <span className="count">{incidentEdges.length}</span></h3>
                <div className="connection-list">
                  {incidentEdges.slice(0, 16).map((edge) => {
                    const otherId = edge.source === selectedId ? edge.target : edge.source
                    return (
                      <button key={edge.id} onClick={() => focusNode(otherId)}>
                        <span>{edge.type}</span>
                        <strong>{entityById.get(otherId)?.name || otherId}</strong>
                      </button>
                    )
                  })}
                </div>
              </section>

              <section>
                <h3>Genealogy <span className="count">{selectedGenealogies.length}</span></h3>
                {selectedGenealogies.length === 0 ? (
                  <div className="muted">No explicit genealogy record for this entity yet.</div>
                ) : (
                  selectedGenealogies.map((genealogy) => (
                    <div className="genealogy" key={genealogy.id}>
                      <div className="genealogy-key">{genealogy.genetic_identity_key}</div>
                      {genealogy.paths?.map((path: AnyRecord) => (
                        <div className="genealogy-path" key={path.id}>
                          <div className="origin">{path.origin}</div>
                          {path.steps?.map((step: AnyRecord) => (
                            <div className="genealogy-step" key={`${path.id}-${step.index}`}>
                              <span>{step.index}</span>
                              <div>{step.event}</div>
                            </div>
                          ))}
                        </div>
                      ))}
                    </div>
                  ))
                )}
              </section>

              {!!selectedEntity.evidence?.source_files?.length && (
                <section>
                  <h3>Provenance</h3>
                  <div className="source-files">
                    {selectedEntity.evidence.source_files.map((source: string) => <code key={source}>{source}</code>)}
                  </div>
                </section>
              )}
            </div>
          )}
        </aside>
      </div>
    </div>
  )
}

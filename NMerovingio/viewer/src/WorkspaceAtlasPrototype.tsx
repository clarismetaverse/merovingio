import { useEffect, useMemo, useRef, useState } from 'react'
import cytoscape, { type Core, type ElementDefinition } from 'cytoscape'

import exampleJson from '../../graph/examples/workspace_quadrilateral_diagonal_v0_4_1.json'

type AnyRecord = Record<string, any>
type Perspective = 'MATERIAL' | 'CO_CONSTITUTION' | 'ATLAS' | 'ALL'

const example = exampleJson as AnyRecord
const nodeById = new Map<string, AnyRecord>(example.nodes.map((node: AnyRecord) => [node.id, node]))
const perspectiveOrder: Perspective[] = ['MATERIAL', 'CO_CONSTITUTION', 'ATLAS', 'ALL']

function makeElements(): ElementDefinition[] {
  const nodes: ElementDefinition[] = example.nodes.map((node: AnyRecord) => ({
    data: {
      id: node.id,
      label: node.label,
      type: node.type,
      materialIdentity: node.material_identity || '',
    },
    position: node.position,
  }))

  const edges: ElementDefinition[] = example.edges.map((edge: AnyRecord) => ({
    data: {
      id: edge.id,
      source: edge.source,
      target: edge.target,
      type: edge.type,
      label: edge.role ? `${edge.type} · ${edge.role}` : edge.type,
      role: edge.role || '',
    },
  }))

  return [...nodes, ...edges]
}

function graphStyle(): any[] {
  return [
    {
      selector: 'node',
      style: {
        label: 'data(label)',
        color: '#e9eef7',
        'font-family': 'Inter, ui-sans-serif, system-ui, sans-serif',
        'font-size': 11,
        'text-wrap': 'wrap',
        'text-max-width': 120,
        'text-valign': 'bottom',
        'text-margin-y': 8,
        'background-color': '#243046',
        'border-width': 1.5,
        'border-color': '#53647e',
        width: 52,
        height: 42,
        'overlay-opacity': 0,
      },
    },
    {
      selector: 'node[type = "WORKSPACE"]',
      style: {
        shape: 'round-rectangle',
        width: 122,
        height: 58,
        'background-color': '#18202e',
        'border-width': 2.5,
        'border-color': '#8191a9',
      },
    },
    {
      selector: 'node[type = "GESTALT"]',
      style: {
        shape: 'round-rectangle',
        width: 96,
        height: 50,
        'background-color': '#263650',
        'border-color': '#647b9e',
      },
    },
    {
      selector: 'node[type = "MEDIAL_CARRIER"]',
      style: {
        shape: 'diamond',
        width: 70,
        height: 70,
        'background-color': '#d9ad45',
        'border-color': '#ffe19a',
        'border-width': 3,
        color: '#fff7df',
        'font-size': 14,
        'font-weight': 800,
      },
    },
    {
      selector: 'node[type = "CO_CONSTITUTION"]',
      style: {
        shape: 'octagon',
        width: 78,
        height: 58,
        'background-color': '#774f8f',
        'border-color': '#ae82c5',
      },
    },
    {
      selector: 'node[type = "FAMILY"]',
      style: {
        shape: 'hexagon',
        width: 82,
        height: 70,
        'background-color': '#315f59',
        'border-color': '#6d9d92',
      },
    },
    {
      selector: 'edge',
      style: {
        width: 1.5,
        'curve-style': 'bezier',
        'line-color': '#48566a',
        'target-arrow-shape': 'triangle',
        'target-arrow-color': '#48566a',
        'arrow-scale': 0.75,
        label: 'data(label)',
        color: '#75849a',
        'font-size': 7,
        'text-background-color': '#0b0f16',
        'text-background-opacity': 0.9,
        'text-background-padding': 2,
        'text-rotation': 'autorotate',
      },
    },
    {
      selector: 'edge[type = "PARTICIPATES_IN"]',
      style: {
        width: 3.2,
        'line-color': '#c99f45',
        'target-arrow-color': '#c99f45',
      },
    },
    {
      selector: 'edge[type = "CO_CONSTITUTES"], edge[type = "SEEDS_CO_CONSTITUTION"]',
      style: {
        width: 2.5,
        'line-style': 'dashed',
        'line-color': '#956cad',
        'target-arrow-color': '#956cad',
      },
    },
    {
      selector: 'edge[type = "REALIZES"]',
      style: {
        'line-color': '#4b8179',
        'target-arrow-color': '#4b8179',
      },
    },
    {
      selector: '.dimmed',
      style: {
        opacity: 0.1,
        'text-opacity': 0.06,
      },
    },
    {
      selector: '.focused',
      style: {
        opacity: 1,
        'text-opacity': 1,
        'border-width': 4,
        'border-color': '#ffffff',
        'z-index': 999,
      },
    },
    {
      selector: '.neighbor',
      style: {
        opacity: 1,
        'text-opacity': 1,
      },
    },
  ]
}

export default function WorkspaceAtlasPrototype() {
  const graphRef = useRef<HTMLDivElement | null>(null)
  const cyRef = useRef<Core | null>(null)
  const [perspective, setPerspective] = useState<Perspective>('CO_CONSTITUTION')
  const [selectedId, setSelectedId] = useState<string>('M_AC')

  const elements = useMemo(() => makeElements(), [])
  const selected = nodeById.get(selectedId)

  useEffect(() => {
    if (!graphRef.current || cyRef.current) return

    const cy = cytoscape({
      container: graphRef.current,
      elements,
      style: graphStyle(),
      layout: { name: 'preset', fit: true, padding: 65 },
      wheelSensitivity: 0.18,
      minZoom: 0.45,
      maxZoom: 2.8,
    })

    cy.on('tap', 'node', (event) => {
      setSelectedId(event.target.id())
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

    const focusIds = new Set<string>(example.perspectives[perspective] || [])
    cy.elements().removeClass('dimmed')

    if (perspective !== 'ALL') {
      cy.nodes().forEach((node) => {
        if (!focusIds.has(node.id())) node.addClass('dimmed')
      })
      cy.edges().forEach((edge) => {
        if (!focusIds.has(edge.source().id()) || !focusIds.has(edge.target().id())) {
          edge.addClass('dimmed')
        }
      })
    }
  }, [perspective])

  useEffect(() => {
    const cy = cyRef.current
    if (!cy) return

    cy.elements().removeClass('focused neighbor')
    const node = cy.getElementById(selectedId)
    if (!node.length) return
    node.addClass('focused')
    node.neighborhood().addClass('neighbor')
  }, [selectedId])

  const incidentEdges = example.edges.filter(
    (edge: AnyRecord) => edge.source === selectedId || edge.target === selectedId,
  )

  return (
    <div className="atlas-app">
      <header className="atlas-topbar">
        <div>
          <div className="atlas-eyebrow">MEROVINGIO / WORKSPACE v0.4.1</div>
          <h1>Workspace Co-Constitution Atlas</h1>
          <p>One material carrier, many Gestalt participations, one derivational environment.</p>
        </div>
        <a href="/" className="back-link">Cognitive graph ↗</a>
      </header>

      <section className="perspective-bar">
        <span>Perspective</span>
        {perspectiveOrder.map((item) => (
          <button
            key={item}
            className={perspective === item ? 'active' : ''}
            onClick={() => setPerspective(item)}
          >
            {item.replace('_', ' ')}
          </button>
        ))}
      </section>

      <div className="atlas-layout">
        <aside className="concept-panel">
          <div className="concept-kicker">Example 01</div>
          <h2>Quadrilateral + diagonal AC</h2>
          <p>
            AC is not copied across views. It is one material segment co-participating as side,
            diagonal, transversal and identity bridge.
          </p>

          <div className="equation-card">
            <span>Workspace</span>
            <strong>genetic field</strong>
            <i>:</i>
            <span>Atlas</span>
            <strong>conceptual organization</strong>
          </div>

          <div className="legend-stack">
            <div><b className="dot workspace" />Workspace</div>
            <div><b className="dot gestalt" />Gestalt</div>
            <div><b className="dot carrier" />Medial carrier</div>
            <div><b className="dot coconst" />Co-constitution</div>
            <div><b className="dot family" />Family chart</div>
          </div>
        </aside>

        <main className="atlas-graph">
          <div ref={graphRef} className="atlas-canvas" />
          <div className="floating-note">
            <strong>{perspective.replace('_', ' ')}</strong>
            <span>
              {perspective === 'MATERIAL' && 'Keep material identity foregrounded.'}
              {perspective === 'CO_CONSTITUTION' && 'See how one carrier binds several Gestalten.'}
              {perspective === 'ATLAS' && 'See the same Gestalten distributed across family charts.'}
              {perspective === 'ALL' && 'Full derivational environment.'}
            </span>
          </div>
        </main>

        <aside className="atlas-inspector">
          <div className="concept-kicker">{selected?.type || 'NODE'}</div>
          <h2>{selected?.label || selectedId}</h2>
          <code>{selectedId}</code>

          {selected?.material_identity && (
            <section>
              <h3>Material identity</h3>
              <div className="identity-pill">{selected.material_identity}</div>
            </section>
          )}

          {!!selected?.participations?.length && (
            <section>
              <h3>Participations</h3>
              <div className="participation-list">
                {selected.participations.map((item: AnyRecord) => (
                  <button key={`${item.gestalt}-${item.role}`} onClick={() => setSelectedId(item.gestalt)}>
                    <span>{item.role}</span>
                    <strong>{nodeById.get(item.gestalt)?.label || item.gestalt}</strong>
                  </button>
                ))}
              </div>
            </section>
          )}

          <section>
            <h3>Local structure</h3>
            <div className="relation-list">
              {incidentEdges.map((edge: AnyRecord) => {
                const otherId = edge.source === selectedId ? edge.target : edge.source
                return (
                  <button key={edge.id} onClick={() => setSelectedId(otherId)}>
                    <span>{edge.role || edge.type}</span>
                    <strong>{nodeById.get(otherId)?.label || otherId}</strong>
                  </button>
                )
              })}
            </div>
          </section>

          {selectedId === 'M_AC' && (
            <section className="insight-card">
              <h3>Why AC matters</h3>
              <p>
                The same material segment participates in five Gestalten. Its identity is stable;
                its relational role changes. That shared participation is what makes cross-Gestalt
                derivation visible without duplicating the object.
              </p>
            </section>
          )}
        </aside>
      </div>
    </div>
  )
}

import { useEffect, useMemo, useRef, useState } from 'react'
import cytoscape, { type Core, type ElementDefinition } from 'cytoscape'

import quadJson from '../../graph/examples/workspace_quadrilateral_diagonal_v0_4_1.json'
import circlesJson from '../../graph/examples/workspace_two_circles_triangle_v0_4_1.json'
import compareJson from '../../graph/examples/workspace_triangle_genealogy_comparison_v0_4_1.json'
import sameStateJson from '../../graph/examples/workspace_equilateral_same_state_different_genealogy_v0_4_1.json'

type AnyRecord = Record<string, any>
type Perspective = 'MATERIAL' | 'CO_CONSTITUTION' | 'ATLAS' | 'ALL'
type ExampleKey = 'QUADRILATERAL' | 'CIRCLES' | 'COMPARE' | 'SAME_STATE'

const perspectiveOrder: Perspective[] = ['MATERIAL', 'CO_CONSTITUTION', 'ATLAS', 'ALL']

const examples: Record<ExampleKey, AnyRecord> = {
  QUADRILATERAL: quadJson as AnyRecord,
  CIRCLES: circlesJson as AnyRecord,
  COMPARE: compareJson as AnyRecord,
  SAME_STATE: sameStateJson as AnyRecord,
}

function makeElements(example: AnyRecord): ElementDefinition[] {
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
      selector: 'node[type = "GENEALOGY"]',
      style: {
        shape: 'round-rectangle',
        width: 116,
        height: 52,
        'background-color': '#684c38',
        'border-color': '#9d7657',
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
      selector: 'edge[type = "REALIZES"], edge[type = "REALIZES_AS"], edge[type = "HAS_REGION"], edge[type = "OCCUPIES_REGION"]',
      style: {
        'line-color': '#4b8179',
        'target-arrow-color': '#4b8179',
      },
    },
    {
      selector: 'edge[type = "GENETIC_SOURCE"], edge[type = "GENETIC_RESULT"], edge[type = "CARRIES_GENEALOGY"]',
      style: {
        width: 2.2,
        'line-style': 'dashed',
        'line-color': '#9d7657',
        'target-arrow-color': '#9d7657',
      },
    },
    {
      selector: 'edge[type = "STABILIZES"]',
      style: {
        width: 2.3,
        'line-color': '#6f86c7',
        'target-arrow-color': '#6f86c7',
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
  const [exampleKey, setExampleKey] = useState<ExampleKey>('QUADRILATERAL')
  const [perspective, setPerspective] = useState<Perspective>('CO_CONSTITUTION')

  const example = examples[exampleKey]
  const nodeById = useMemo(
    () => new Map<string, AnyRecord>(example.nodes.map((node: AnyRecord) => [node.id, node] as [string, AnyRecord])),
    [example],
  )
  const defaultSelected = example.metadata?.default_selected
    || example.nodes.find((node: AnyRecord) => node.type === 'MEDIAL_CARRIER')?.id
    || example.nodes[0]?.id
  const [selectedId, setSelectedId] = useState<string>(defaultSelected)

  const elements = useMemo(() => makeElements(example), [example])
  const selected = nodeById.get(selectedId)

  useEffect(() => {
    setSelectedId(defaultSelected)
    setPerspective(exampleKey === 'COMPARE' || exampleKey === 'SAME_STATE' ? 'ATLAS' : 'CO_CONSTITUTION')
  }, [exampleKey, defaultSelected])

  useEffect(() => {
    if (!graphRef.current) return

    cyRef.current?.destroy()

    const cy = cytoscape({
      container: graphRef.current,
      elements,
      style: graphStyle(),
      layout: { name: 'preset', fit: true, padding: 65 },
      wheelSensitivity: 0.18,
      minZoom: 0.42,
      maxZoom: 2.8,
    })

    cy.on('tap', 'node', (event) => {
      setSelectedId(event.target.id())
    })

    cyRef.current = cy

    return () => {
      cy.destroy()
      if (cyRef.current === cy) cyRef.current = null
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
  }, [perspective, example])

  useEffect(() => {
    const cy = cyRef.current
    if (!cy) return

    cy.elements().removeClass('focused neighbor')
    const node = cy.getElementById(selectedId)
    if (!node.length) return
    node.addClass('focused')
    node.neighborhood().addClass('neighbor')
  }, [selectedId, elements])

  const incidentEdges = example.edges.filter(
    (edge: AnyRecord) => edge.source === selectedId || edge.target === selectedId,
  )

  const exampleNumber = exampleKey === 'QUADRILATERAL' ? '01' : exampleKey === 'CIRCLES' ? '02' : exampleKey === 'COMPARE' ? '03' : '04'
  const exampleTitle = example.metadata?.title
    || (exampleKey === 'QUADRILATERAL'
      ? 'Quadrilateral + diagonal AC'
      : exampleKey === 'CIRCLES'
        ? 'Two circles → equilateral triangle'
        : exampleKey === 'COMPARE'
          ? 'Same triangle medium, different genealogies'
          : 'Same equilateral state, different genealogies')

  const selectedInsight = example.insight && (
    selectedId === defaultSelected
    || selected?.type === 'FAMILY'
    || selected?.type === 'GENEALOGY'
  ) ? example.insight : null

  return (
    <div className="atlas-app">
      <header className="atlas-topbar">
        <div>
          <div className="atlas-eyebrow">MEROVINGIO / WORKSPACE v0.4.1</div>
          <h1>Workspace Co-Constitution Atlas</h1>
          <p>Material identity stays fixed while Gestalt participation and family organization change.</p>
        </div>
        <a href="/" className="back-link">Cognitive graph ↗</a>
      </header>

      <section className="perspective-bar">
        <span>Example</span>
        <button
          className={exampleKey === 'QUADRILATERAL' ? 'active' : ''}
          onClick={() => setExampleKey('QUADRILATERAL')}
        >
          Quadrilateral
        </button>
        <button
          className={exampleKey === 'CIRCLES' ? 'active' : ''}
          onClick={() => setExampleKey('CIRCLES')}
        >
          Circles → triangle
        </button>
        <button
          className={exampleKey === 'COMPARE' ? 'active' : ''}
          onClick={() => setExampleKey('COMPARE')}
        >
          Compare genesis
        </button>
        <button
          className={exampleKey === 'SAME_STATE' ? 'active' : ''}
          onClick={() => setExampleKey('SAME_STATE')}
        >
          Same state ≠ genesis
        </button>

        <div className="bar-divider" />

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
          <div className="concept-kicker">Example {exampleNumber}</div>
          <h2>{exampleTitle}</h2>
          <p>{example.workspace?.description}</p>

          {exampleKey === 'QUADRILATERAL' && (
            <p>
              AC is one material segment co-participating as side, diagonal, transversal and identity bridge.
            </p>
          )}

          {exampleKey === 'CIRCLES' && (
            <p>
              AB, AC, BC and the shared intersection C are fused across the two circle Gestalten and the derived triangle.
              The triangle is a rebase of the circular workspace, not an unrelated figure added afterwards.
            </p>
          )}

          {exampleKey === 'COMPARE' && (
            <>
              <p>
                The two branches do not share material support. They converge only at the level of the triangle relational medium.
              </p>
              <div className="comparison-principle">
                <strong>SAME MEDIUM</strong>
                <span>≠</span>
                <strong>SAME GENEALOGY</strong>
              </div>
            </>
          )}

          {exampleKey === 'SAME_STATE' && (
            <>
              <p>
                Here even the final triangle state is identical: both branches occupy the equilateral zero of the same triangle medium.
                Only the genetic constitution remains different.
              </p>
              <div className="comparison-principle triple">
                <strong>SAME MEDIUM + STATE</strong>
                <span>≠</span>
                <strong>SAME GENEALOGY</strong>
              </div>
            </>
          )}

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
            <div><b className="dot genealogy" />Genealogy</div>
            <div><b className="dot coconst" />Co-constitution</div>
            <div><b className="dot family" />Family chart</div>
          </div>
        </aside>

        <main className="atlas-graph">
          <div ref={graphRef} className="atlas-canvas" />
          <div className="floating-note">
            <strong>{perspective.replace('_', ' ')}</strong>
            <span>
              {perspective === 'MATERIAL' && 'Keep material identity and workspace separation foregrounded.'}
              {perspective === 'CO_CONSTITUTION' && 'See how shared carriers fuse Gestalten inside each derivational environment.'}
              {perspective === 'ATLAS' && (
                exampleKey === 'COMPARE'
                  ? 'See different genealogies converge on one triangle medium without collapsing their origins.'
                  : exampleKey === 'SAME_STATE'
                    ? 'See medium identity and state identity coincide while genealogy remains split.'
                    : 'See the same Gestalten distributed across family charts.'
              )}
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

          {(exampleKey === 'COMPARE' || exampleKey === 'SAME_STATE') && example.comparison && (
            <section className="comparison-card">
              <h3>Genealogy comparison</h3>
              <div className="compare-row">
                <span>Invariant</span>
                <strong>{example.comparison.invariant}</strong>
              </div>
              <div className="compare-row">
                <span>Non-identity</span>
                <strong>{example.comparison.non_identity}</strong>
              </div>
              <div className="compare-row">
                <span>Principle</span>
                <strong>{example.comparison.principle}</strong>
              </div>
            </section>
          )}

          {selectedInsight && (
            <section className="insight-card">
              <h3>{selectedInsight.title}</h3>
              <p>{selectedInsight.body}</p>
            </section>
          )}

          {exampleKey === 'QUADRILATERAL' && selectedId === 'M_AC' && (
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

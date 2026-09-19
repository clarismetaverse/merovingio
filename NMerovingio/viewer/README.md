# Merovingio Cognitive Graph Explorer

React + Cytoscape viewers for the machine-readable Merovingio graph and the v0.4.1 workspace / family-atlas model.

## Run locally

```bash
cd NMerovingio/viewer
npm install
npm run dev
```

Open:

- `/` — canonical cognitive graph explorer
- `/workspace.html` — workspace co-constitution / family-atlas prototype

Build:

```bash
npm run build
npm run preview
```

## Workspace Atlas prototype

The first v0.4.1 visual example uses one quadrilateral workspace with diagonal `AC`.

The prototype makes the architectural distinction visible:

```text
WORKSPACE = genetic / derivational field
ATLAS     = multiperspectival conceptual organization
```

It renders:

- the material workspace;
- co-participating Gestalten;
- `AC` as one **MedialCarrier** rather than duplicated edges;
- the different local roles of `AC` (side, diagonal, transversal, identity bridge);
- an explicit co-constitution hub;
- family charts realized by the Gestalten.

Perspective controls let the same graph be read as:

- **Material** — foreground material identity;
- **Co constitution** — foreground carrier participation and blending;
- **Atlas** — foreground family memberships;
- **All** — full derivational environment.

Selecting the medial carrier exposes every role it occupies without creating copies of the underlying segment.

The data is in:

`../graph/examples/workspace_quadrilateral_diagonal_v0_4_1.json`

## Cognitive graph view

The original graph explorer provides:

- canonical snapshot timeline;
- entity-layer filters;
- inspector;
- genealogy;
- graph search.

## Design principle

The UI intentionally does **not** present one graph layout as the unique representation of Merovingio. Perspective switching should preserve material identity while changing role, family, and Gestalt foregrounding.

The workspace prototype is the first step toward synchronized views for:

1. material support;
2. medial carriers and co-constitution;
3. family atlas / strata / fibers;
4. hierarchical multi-parent organization;
5. genealogy and deformation animation.

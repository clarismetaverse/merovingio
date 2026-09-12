# Merovingio Cognitive Graph Explorer

Small React + Cytoscape viewer for the machine-readable graph in `../graph/`.

## Run locally

```bash
cd NMerovingio/viewer
npm install
npm run dev
```

Build:

```bash
npm run build
npm run preview
```

## Current views

- **Full N9 graph** with ontology encoded by node shape and epistemic status by color.
- **N0–N9 timeline**: selecting a snapshot keeps the whole graph visible but dims entities outside that snapshot's active cognitive foreground.
- **Entity-layer filters** for workspaces, Gestalten, families, zero loci, registers, propositions, operators, agents and impetus nodes.
- **Inspector** with raw structure, local graph connections, evidence provenance, and explicit genealogy paths.
- **Search** across IDs, names and semantic aliases.

## Visual grammar

Node shape encodes ontology:

- ellipse — workspace
- rounded rectangle — Gestalt
- hexagon — family
- diamond — zero locus
- barrel — register
- rectangle — proposition
- tag — operator
- round diamond — agent
- vee — impetus

Node color encodes epistemic status (`SEED`, `PROP_LICENSED`, `VALIDATED_COGNITIVE`, `COGNITIVE_CANDIDATE`, etc.).

## Design principle

The UI intentionally does **not** present one graph layout as the unique representation of Merovingio. Snapshot selection, type filters and entity inspection are themselves partializations of the underlying cognitive network.

Next useful views:

1. dedicated genealogy-only mode;
2. graph-delta animation between snapshots;
3. workspace/Gestalt partialization view;
4. explicit impetus field / agent proposal overlay;
5. Somaschini Graph mode for user-selected subgraphs.

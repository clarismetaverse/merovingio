# Merovingio machine-readable cognitive graph

This directory materializes the conceptual network developed in the controlled dry-runs into explicit machine-readable data.

## Status

The data here is **not the output of an autonomous multi-agent execution**. It is the formal extraction of the manually simulated/controlled runs documented in the `NMerovingio/*.md` files. Every run record therefore carries `execution_mode = CONTROLLED_DRY_RUN`.

The goal is to make the next implementation phase possible without asking an LLM to reinterpret prose Markdown on every run.

## Files

- `schema_v1.json` — JSON Schema for graph entities, edges, run deltas, snapshots, genealogies, and evidence status.
- `entities_v1.json` — canonical node registry: workspaces, Gestalten, families, registers, zero loci, operators, agents, impetus types, propositions/capabilities.
- `edges_v1.json` — current accepted cognitive-graph relations through N9.
- `genealogy_v1.json` — multiple generative paths for important states/Gestalten; preserves `STATE_IDENTITY != GENETIC_IDENTITY`.
- `runs_v1.json` — formal deltas for Runs 01–09.
- `snapshots_v1.json` — compact snapshots N0–N9 showing the progressive reorganization of the network.
- `merovingio_n9.dot` — Graphviz view of the main N9 families and transformations.

## Core invariants

```text
REACHABILITY != ANALOGICAL_STRENGTH
STATE_IDENTITY != GENETIC_IDENTITY
CENTRALITY != ACTUALITY
ROLE_ALIGNMENT != RELATION_EQUALITY != COMPLETION_READOUT
COGNITIVE_CYCLE != LOGICAL_CIRCULARITY
```

## Three graph layers

The formalization keeps three layers distinct:

1. **Material / constructive layer** — workspaces, carriers, points, segments, rays, intersections, constructions.
2. **Cognitive layer** — Gestalt partializations, families, zero loci, genealogies, rebase/host/completion relations, agent proposals.
3. **Proof layer** — proposition-licensed or validator-certified relations. The cognitive graph may contain cycles; proof certificates may not.

## Gestalt definition used by the data

A Gestalt is modeled as a partialization of a constructive workspace:

```text
Gestalt = Partialize(
    workspace,
    selected elements,
    role assignment,
    privileged relations,
    completion mode,
    active ground
)
```

Thus two Gestalten may partially organize the same material construction without being separate mathematical universes.

## Snapshot convention

`N0` is the deliberately banalized triangle network before Run 01.

Each subsequent state is the accepted conceptual delta of one controlled run:

```text
N0 --Run01--> N1  triangle relation family / isosceles zero
N1 --Run02--> N2  internal/external correspondence completion
N2 --Run03--> N3  transversal injection / role topology / relation transducers
N3 --Run04--> N4  parallel certification / closure topology
N4 --Run05--> N5  I.29 completion cycle / generative parallel host
N5 --Run06--> N6  parallelogram product family / composite zero
N6 --Run07--> N7  square diagonal projection / inherited zero
N7 --Run08--> N8  zero recomposition with extra angular condition
N8 --Run09--> N9  one-zero family / free angular register / centrality != actuality
```

## Intended software usage

The next Merovingio implementation should load these files into an in-memory graph and let specialized agents propose `NetworkDelta` objects rather than editing state directly.

```text
CoreGraph
  -> events/tensions
  -> ImpetusRouter
  -> Completion / Expansion / Genealogy / Reorganization / Compiler agents
  -> ProposalBlackboard
  -> Validator
  -> accepted NetworkDelta
  -> next snapshot
```

These files are the seed dataset and regression benchmark for that implementation.
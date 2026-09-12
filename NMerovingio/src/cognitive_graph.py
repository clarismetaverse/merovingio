from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable
import argparse
import json


@dataclass(frozen=True)
class Entity:
    id: str
    type: str
    name: str
    raw: dict[str, Any]


@dataclass(frozen=True)
class Edge:
    id: str
    source: str
    target: str
    type: str
    raw: dict[str, Any]


@dataclass(frozen=True)
class Genealogy:
    id: str
    target: str
    raw: dict[str, Any]


@dataclass(frozen=True)
class RunRecord:
    id: str
    input_snapshot: str
    output_snapshot: str
    raw: dict[str, Any]


@dataclass(frozen=True)
class Snapshot:
    id: str
    raw: dict[str, Any]


class CognitiveGraph:
    """Machine-readable Merovingio cognitive graph.

    This class intentionally does not implement the future multi-agent reasoner.
    It provides the deterministic substrate the agents will operate on:

    - canonical entity/edge registry
    - explicit genealogies
    - run deltas
    - N0..N9 snapshots
    - reference validation
    - basic graph queries

    The current dataset is extracted from CONTROLLED_DRY_RUN records. It must not
    be represented as autonomous experimental output.
    """

    def __init__(
        self,
        entities: Iterable[Entity],
        edges: Iterable[Edge],
        genealogies: Iterable[Genealogy],
        runs: Iterable[RunRecord],
        snapshots: Iterable[Snapshot],
    ) -> None:
        self.entities = {e.id: e for e in entities}
        self.edges = {e.id: e for e in edges}
        self.genealogies = {g.id: g for g in genealogies}
        self.runs = {r.id: r for r in runs}
        self.snapshots = {s.id: s for s in snapshots}

        self._outgoing: dict[str, list[Edge]] = {}
        self._incoming: dict[str, list[Edge]] = {}
        for edge in self.edges.values():
            self._outgoing.setdefault(edge.source, []).append(edge)
            self._incoming.setdefault(edge.target, []).append(edge)

    @classmethod
    def from_directory(cls, graph_dir: str | Path) -> "CognitiveGraph":
        graph_dir = Path(graph_dir)

        entities_raw = _load_json(graph_dir / "entities_v1.json")["entities"]
        edges_raw = _load_json(graph_dir / "edges_v1.json")["edges"]
        genealogies_raw = _load_json(graph_dir / "genealogy_v1.json")["genealogies"]
        runs_raw = _load_json(graph_dir / "runs_v1.json")["runs"]
        snapshots_raw = _load_json(graph_dir / "snapshots_v1.json")["snapshots"]

        return cls(
            entities=(Entity(x["id"], x["type"], x["name"], x) for x in entities_raw),
            edges=(Edge(x["id"], x["source"], x["target"], x["type"], x) for x in edges_raw),
            genealogies=(Genealogy(x["id"], x["target"], x) for x in genealogies_raw),
            runs=(RunRecord(x["id"], x["input_snapshot"], x["output_snapshot"], x) for x in runs_raw),
            snapshots=(Snapshot(x["id"], x) for x in snapshots_raw),
        )

    @classmethod
    def load_default(cls) -> "CognitiveGraph":
        graph_dir = Path(__file__).resolve().parents[1] / "graph"
        return cls.from_directory(graph_dir)

    def validate(self) -> list[str]:
        """Return structural validation errors; empty list means references cohere."""
        errors: list[str] = []

        for edge in self.edges.values():
            if edge.source not in self.entities:
                errors.append(f"edge {edge.id}: unknown source {edge.source}")
            if edge.target not in self.entities:
                errors.append(f"edge {edge.id}: unknown target {edge.target}")

        for genealogy in self.genealogies.values():
            if genealogy.target not in self.entities:
                errors.append(f"genealogy {genealogy.id}: unknown target {genealogy.target}")
            for path in genealogy.raw.get("paths", []):
                for step in path.get("steps", []):
                    for key in ("input_entities", "output_entities"):
                        for entity_id in step.get(key, []):
                            if entity_id not in self.entities:
                                errors.append(
                                    f"genealogy {genealogy.id}/{path.get('id')}: "
                                    f"unknown {key} reference {entity_id}"
                                )

        for run in self.runs.values():
            if run.input_snapshot not in self.snapshots:
                errors.append(f"run {run.id}: unknown input snapshot {run.input_snapshot}")
            if run.output_snapshot not in self.snapshots:
                errors.append(f"run {run.id}: unknown output snapshot {run.output_snapshot}")

            delta = run.raw.get("delta", {})
            for entity_id in delta.get("add_entities", []):
                if entity_id not in self.entities:
                    errors.append(f"run {run.id}: unknown added entity {entity_id}")
            for edge_id in delta.get("add_edges", []):
                if edge_id not in self.edges:
                    errors.append(f"run {run.id}: unknown added edge {edge_id}")
            for entity_id in delta.get("enrich_entities", []):
                if entity_id not in self.entities:
                    errors.append(f"run {run.id}: unknown enriched entity {entity_id}")

        for snapshot in self.snapshots.values():
            for entity_id in snapshot.raw.get("active_entities", []):
                if entity_id not in self.entities:
                    errors.append(f"snapshot {snapshot.id}: unknown active entity {entity_id}")
            for family_id in snapshot.raw.get("active_families", []):
                entity = self.entities.get(family_id)
                if entity is None:
                    errors.append(f"snapshot {snapshot.id}: unknown active family {family_id}")
                elif entity.type != "FAMILY":
                    errors.append(f"snapshot {snapshot.id}: {family_id} is not a FAMILY")

        return errors

    def entity(self, entity_id: str) -> Entity:
        return self.entities[entity_id]

    def snapshot(self, snapshot_id: str) -> Snapshot:
        return self.snapshots[snapshot_id]

    def run(self, run_id: str) -> RunRecord:
        return self.runs[run_id]

    def outgoing(self, entity_id: str, edge_type: str | None = None) -> list[Edge]:
        edges = self._outgoing.get(entity_id, [])
        if edge_type is None:
            return list(edges)
        return [edge for edge in edges if edge.type == edge_type]

    def incoming(self, entity_id: str, edge_type: str | None = None) -> list[Edge]:
        edges = self._incoming.get(entity_id, [])
        if edge_type is None:
            return list(edges)
        return [edge for edge in edges if edge.type == edge_type]

    def genealogies_for(self, target_id: str) -> list[Genealogy]:
        return [g for g in self.genealogies.values() if g.target == target_id]

    def entities_of_type(self, entity_type: str) -> list[Entity]:
        return [e for e in self.entities.values() if e.type == entity_type]

    def introduced_in_run(self, run_id: str) -> tuple[list[Entity], list[Edge]]:
        run = self.run(run_id)
        delta = run.raw.get("delta", {})
        entities = [self.entities[x] for x in delta.get("add_entities", [])]
        edges = [self.edges[x] for x in delta.get("add_edges", [])]
        return entities, edges

    def neighbors(self, entity_id: str) -> set[str]:
        result = {edge.target for edge in self.outgoing(entity_id)}
        result.update(edge.source for edge in self.incoming(entity_id))
        return result

    def reachable(
        self,
        source_id: str,
        *,
        edge_types: set[str] | None = None,
        max_depth: int = 4,
    ) -> dict[str, int]:
        """Breadth-first cognitive reachability.

        Important: this computes reachability only. It intentionally does NOT score
        analogical strength; the architecture explicitly requires
        REACHABILITY != ANALOGICAL_STRENGTH.
        """
        seen = {source_id: 0}
        frontier = [source_id]

        while frontier:
            current = frontier.pop(0)
            depth = seen[current]
            if depth >= max_depth:
                continue

            for edge in self.outgoing(current):
                if edge_types is not None and edge.type not in edge_types:
                    continue
                if edge.target not in seen:
                    seen[edge.target] = depth + 1
                    frontier.append(edge.target)

        return seen

    def summary(self) -> dict[str, Any]:
        return {
            "entities": len(self.entities),
            "edges": len(self.edges),
            "genealogies": len(self.genealogies),
            "runs": len(self.runs),
            "snapshots": len(self.snapshots),
            "entity_types": {
                entity_type: len(self.entities_of_type(entity_type))
                for entity_type in sorted({e.type for e in self.entities.values()})
            },
        }


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _cmd_validate(graph: CognitiveGraph) -> int:
    errors = graph.validate()
    if errors:
        print("INVALID")
        for error in errors:
            print(f"- {error}")
        return 1
    print("VALID")
    print(json.dumps(graph.summary(), indent=2))
    return 0


def _cmd_show(graph: CognitiveGraph, entity_id: str) -> int:
    entity = graph.entity(entity_id)
    print(json.dumps(entity.raw, indent=2))
    print("\nOUTGOING")
    for edge in graph.outgoing(entity_id):
        print(f"  {edge.id}: {edge.type} -> {edge.target}")
    print("\nINCOMING")
    for edge in graph.incoming(entity_id):
        print(f"  {edge.id}: {edge.source} -> {edge.type}")
    print("\nGENEALOGIES")
    for genealogy in graph.genealogies_for(entity_id):
        print(f"  {genealogy.id}: {len(genealogy.raw.get('paths', []))} path(s)")
    return 0


def _cmd_run(graph: CognitiveGraph, run_id: str) -> int:
    run = graph.run(run_id)
    print(json.dumps(run.raw, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect the Merovingio cognitive graph")
    parser.add_argument("--graph-dir", type=Path, default=None)
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("validate")

    show = sub.add_parser("show")
    show.add_argument("entity_id")

    run = sub.add_parser("run")
    run.add_argument("run_id")

    args = parser.parse_args()
    graph = CognitiveGraph.from_directory(args.graph_dir) if args.graph_dir else CognitiveGraph.load_default()

    if args.command == "validate":
        return _cmd_validate(graph)
    if args.command == "show":
        return _cmd_show(graph, args.entity_id)
    if args.command == "run":
        return _cmd_run(graph, args.run_id)
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())

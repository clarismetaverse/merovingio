from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Iterable
import json


class Relation(str, Enum):
    EQ = "="
    GT = ">"
    LT = "<"
    UNKNOWN = "?"


@dataclass(frozen=True)
class GestaltState:
    side_relation: Relation = Relation.EQ
    angle_relation: Relation = Relation.EQ
    provenance: tuple[str, ...] = ("ISOSCELES_BASE",)
    eliminated: tuple[str, ...] = ()


@dataclass(frozen=True)
class Counterfactual:
    source: GestaltState
    target: GestaltState
    break_kind: str
    impetus: str
    preserved_contacts: tuple[str, ...]


@dataclass(frozen=True)
class PropositionPattern:
    proposition_id: str
    role: str
    direction: str
    preconditions: tuple[str, ...]
    effect: tuple[str, ...]
    counterfactual_signature: tuple[str, ...]
    visual_operations: tuple[str, ...]
    forbidden_shortcuts: tuple[str, ...]


@dataclass
class Trace:
    events: list[str] = field(default_factory=list)

    def add(self, message: str) -> None:
        self.events.append(message)

    def __str__(self) -> str:
        return "\n".join(f"{i + 1}. {event}" for i, event in enumerate(self.events))


class NMerovingio:
    """Tiny role-analogical reasoner for the isosceles workspace.

    It deliberately does not perform general theorem proving. It creates one-break
    counterfactuals, detects the active inferential tension, and retrieves proposition
    patterns by inferential role.
    """

    def __init__(self, patterns: Iterable[PropositionPattern]):
        self.patterns = tuple(patterns)
        self.base = GestaltState()

    @classmethod
    def from_json(cls, path: str | Path) -> "NMerovingio":
        raw = json.loads(Path(path).read_text(encoding="utf-8"))
        patterns = [
            PropositionPattern(
                proposition_id=item["id"],
                role=item["role"],
                direction=item["direction"],
                preconditions=tuple(item["preconditions"]),
                effect=tuple(item["effect"]),
                counterfactual_signature=tuple(item["counterfactual_signature"]),
                visual_operations=tuple(item["visual_operations"]),
                forbidden_shortcuts=tuple(item["forbidden_shortcuts"]),
            )
            for item in raw
        ]
        return cls(patterns)

    def break_side_equality(self, direction: Relation = Relation.GT) -> Counterfactual:
        if direction not in {Relation.GT, Relation.LT}:
            raise ValueError("A side break must be GT or LT")
        target = GestaltState(
            side_relation=direction,
            angle_relation=Relation.UNKNOWN,
            provenance=self.base.provenance + (f"BREAK_SIDE_EQUALITY({direction.value})",),
        )
        return Counterfactual(
            source=self.base,
            target=target,
            break_kind="side",
            impetus="Which angle relation can remain coherent after side equality is broken?",
            preserved_contacts=("same triangle correspondence", "opposition side<->angle"),
        )

    def break_angle_equality(self, direction: Relation = Relation.GT) -> Counterfactual:
        if direction not in {Relation.GT, Relation.LT}:
            raise ValueError("An angle break must be GT or LT")
        target = GestaltState(
            side_relation=Relation.UNKNOWN,
            angle_relation=direction,
            provenance=self.base.provenance + (f"BREAK_ANGLE_EQUALITY({direction.value})",),
        )
        return Counterfactual(
            source=self.base,
            target=target,
            break_kind="angle",
            impetus="Which side relation can remain coherent after angle equality is broken?",
            preserved_contacts=("same triangle correspondence", "opposition side<->angle"),
        )

    def inferential_role(self, cf: Counterfactual) -> str:
        if cf.break_kind == "side":
            return "propagate_side_disanalogy_to_opposite_angle"
        if cf.break_kind == "angle":
            return "propagate_angle_disanalogy_to_opposite_side"
        raise ValueError(f"Unknown break kind: {cf.break_kind}")

    def retrieve_by_role(self, cf: Counterfactual, *, exclude: set[str] | None = None) -> list[PropositionPattern]:
        exclude = exclude or set()
        desired = self.inferential_role(cf)
        exact = [p for p in self.patterns if p.role == desired and p.proposition_id not in exclude]
        if exact:
            return exact

        # Fallback: retrieve structurally adjacent patterns without target leakage.
        adjacent_roles = {
            "side": {
                "propagate_equality_side_to_angle",
                "reject_side_disanalogy_under_equal_angles",
                "reject_second_compatible_closure",
            },
            "angle": {
                "reject_side_disanalogy_under_equal_angles",
                "propagate_equality_side_to_angle",
                "reject_second_compatible_closure",
            },
        }[cf.break_kind]
        return [p for p in self.patterns if p.role in adjacent_roles and p.proposition_id not in exclude]

    def candidate_states(self, cf: Counterfactual) -> tuple[GestaltState, ...]:
        if cf.break_kind == "side":
            return tuple(
                GestaltState(
                    side_relation=cf.target.side_relation,
                    angle_relation=r,
                    provenance=cf.target.provenance + (f"TEST_ANGLE({r.value})",),
                )
                for r in (Relation.EQ, Relation.GT, Relation.LT)
            )
        return tuple(
            GestaltState(
                side_relation=r,
                angle_relation=cf.target.angle_relation,
                provenance=cf.target.provenance + (f"TEST_SIDE({r.value})",),
            )
            for r in (Relation.EQ, Relation.GT, Relation.LT)
        )

    def eliminate_with_base(self, state: GestaltState, trace: Trace) -> bool:
        """Use the stabilized equality Gestalt as a constraint bridge.

        This is intentionally tiny: equality on one member plus inequality on the
        corresponding member is marked as an incompatible overlay.
        """
        if state.side_relation == Relation.EQ and state.angle_relation in {Relation.GT, Relation.LT}:
            trace.add("Base contact rejects side '=' with angle inequality: isosceles equality cannot close.")
            return True
        if state.angle_relation == Relation.EQ and state.side_relation in {Relation.GT, Relation.LT}:
            trace.add("Base contact rejects angle '=' with side inequality: isosceles equality cannot close.")
            return True
        return False

    def run_counterfactual(self, cf: Counterfactual, *, hide_target: bool = True) -> Trace:
        trace = Trace()
        trace.add(f"Load base Gestalt: sides '=', base angles '='.")
        trace.add(f"Apply minimal {cf.break_kind} break: {cf.target.provenance[-1]}.")
        trace.add("Preserve contacts: " + ", ".join(cf.preserved_contacts) + ".")
        trace.add("Generate three candidate relations for the still-open correspondence.")

        survivors: list[GestaltState] = []
        for state in self.candidate_states(cf):
            if self.eliminate_with_base(state, trace):
                continue
            survivors.append(state)

        target_ids = {"I.18"} if cf.break_kind == "side" else {"I.19"}
        exclude = target_ids if hide_target else set()
        retrieved = self.retrieve_by_role(cf, exclude=exclude)
        if retrieved:
            trace.add(
                "Retrieve prior patterns by inferential role (not diagram similarity): "
                + ", ".join(p.proposition_id for p in retrieved)
                + "."
            )
        else:
            trace.add("No prior role-analogous pattern resolves the remaining orientation yet.")

        if survivors:
            readable = ", ".join(
                f"(side {s.side_relation.value}, angle {s.angle_relation.value})" for s in survivors
            )
            trace.add("Surviving counterfactual regions: " + readable + ".")
        trace.add("Stop before target leakage: unresolved regions are research space for RUN/LLM construction.")
        return trace


def demo() -> None:
    here = Path(__file__).resolve().parents[1]
    reasoner = NMerovingio.from_json(here / "data" / "propositions.json")
    print("=== SIDE BREAK: search toward I.18 without I.18 ===")
    print(reasoner.run_counterfactual(reasoner.break_side_equality(Relation.GT), hide_target=True))
    print()
    print("=== ANGLE BREAK: search toward I.19 without I.19 ===")
    print(reasoner.run_counterfactual(reasoner.break_angle_equality(Relation.GT), hide_target=True))


if __name__ == "__main__":
    demo()

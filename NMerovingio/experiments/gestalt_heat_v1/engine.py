#!/usr/bin/env python3
"""Merovingio: macro-to-micro Gestalt activation / codelet experiment.

This is an executable *cognitive simulation*, not a Euclidean proof or a
reimplementation of Copycat. It preserves the epistemic boundary between
observed incidences, constructed angle equality, and analogical goals.
"""
from __future__ import annotations

import argparse
import json
import math
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from statistics import mean

HERE = Path(__file__).resolve().parent
NMEROVINGIO = HERE.parents[1]
FIXTURE = NMEROVINGIO / "graph/examples/generic_spaces_v0_8.json"
MEMORY = NMEROVINGIO / "graph/generic_space_memory_v0_9.json"

CONDITIONS = ("bottom_up", "top_down", "reciprocal")
MODES = ("isosceles", "scalene")
MACRO_CONCEPTS = ("angles", "sides", "opposition", "divider", "sas", "carrier")

@dataclass(frozen=True)
class Codelet:
    id: str
    prerequisites: tuple[str, ...]
    tags: tuple[str, ...]
    base: float
    description: str
    kind: str = "structural_candidate"

CODELETS = (
    Codelet("ANGLE_PAIR", (), ("angles", "divider"), 0.50, "Two angular sectors at C"),
    Codelet("BASE_PAIR", (), ("sides", "divider"), 0.50, "Two base segments AD and DB"),
    Codelet("LEFT_TRIANGLE", (), ("angles", "sides"), 0.60, "Left region ACD"),
    Codelet("RIGHT_TRIANGLE", (), ("angles", "sides"), 0.60, "Right region BCD"),
    Codelet("VERTEX_PARTITION", ("ANGLE_PAIR",), ("angles", "divider"), 0.45, "Vertex angle partition"),
    Codelet("BASE_PARTITION", ("BASE_PAIR",), ("sides", "divider"), 0.45, "Base segment partition (not equal-halves)"),
    Codelet("SHARED_CARRIER", ("LEFT_TRIANGLE", "RIGHT_TRIANGLE"), ("carrier",), 0.55, "One material CD, two triangle side roles"),
    Codelet("OPPOSITION_PAIR", ("ANGLE_PAIR", "BASE_PAIR"), ("angles", "sides", "opposition"), 0.35,
            "Opposite pairs angle ACD : AD, angle DCB : DB"),
    Codelet("DIVIDER_GENERIC", ("VERTEX_PARTITION", "BASE_PARTITION"), ("angles", "sides", "divider"), 0.33,
            "Analogous division in angular and segment domains"),
    Codelet("SAS_TRIPLETS", ("ANGLE_PAIR", "SHARED_CARRIER"), ("angles", "sides", "sas"), 0.37,
            "AC-angleACD-CD and BC-angleDCB-CD role triplets"),
    Codelet("MULTIROLE_GENERIC", ("SHARED_CARRIER", "DIVIDER_GENERIC"), ("carrier", "divider"), 0.30,
            "CD as carrier, angular divisor, and base-incidence bridge"),
    Codelet("HIGHER_GENERIC", ("OPPOSITION_PAIR", "DIVIDER_GENERIC"), ("opposition", "angles", "sides"), 0.30,
            "Meta-grouping of opposed angular / segment partitions"),
    Codelet("TRANSFER_TENSION", ("OPPOSITION_PAIR", "SAS_TRIPLETS"), ("opposition", "angles", "sides", "sas"), 0.26,
            "Project angle equality toward possible base equality AD=DB?", "hypothesis_only"),
    Codelet("PERIMETER_READING", (), ("sides",), 0.55, "Alternative perimeter reading"),
    Codelet("CORNER_ANGLE_READING", (), ("angles",), 0.55, "Alternative base-corner angle grouping"),
    Codelet("GLOBAL_OUTLINE", (), ("carrier",), 0.60, "Alternative outline-only reading"),
)

STRUCTURAL_GENERIC_IDS = ("OPPOSITION_PAIR", "DIVIDER_GENERIC", "MULTIROLE_GENERIC", "HIGHER_GENERIC")
ANGLE_TO_SIDE = ("OPPOSITION_PAIR", "SAS_TRIPLETS", "TRANSFER_TENSION", "HIGHER_GENERIC")


def fixture_contract() -> dict:
    f = json.loads(FIXTURE.read_text(encoding="utf-8"))
    spaces = {s["id"] for s in f["mental_spaces"]}
    names = {g["id"] for g in f["generic_spaces"]}
    assert {"MS_INITIAL_SIDE", "MS_INITIAL_ANGLE", "MS_LEFT", "MS_RIGHT"} <= spaces
    assert {"GS_SIDE_ANGLE", "GS_MULTIPLE_ROLE", "GS_PAIR_ADJACENT"} <= names
    m = json.loads(MEMORY.read_text(encoding="utf-8"))
    ids = {g["id"] for g in m["entries"]}
    assert "GS_HIST_DOUBLE_TRIANGLE" in ids
    return {"fixture": str(FIXTURE.relative_to(NMEROVINGIO)),
            "memory": str(MEMORY.relative_to(NMEROVINGIO)),
            "historical_generic": "GS_HIST_DOUBLE_TRIANGLE",
            "workspace_mental_spaces": sorted(spaces)}


def geometry(mode: str) -> dict:
    if mode not in MODES:
        raise ValueError(mode)
    f = json.loads(FIXTURE.read_text(encoding="utf-8"))
    a = tuple(f["points"]["A"])
    b = tuple(f["points"]["B"])
    c = (float(f["points"]["C"][0]), float(f["points"]["C"][1]))
    if mode == "scalene":
        c = (c[0] - 55.0, c[1])
    distance = lambda p, q: math.dist(p, q)
    ac, bc, ab = distance(a, c), distance(b, c), distance(a, b)
    t = ac / (ac + bc)  # angle-bisector intersection on AB
    d = (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]))
    ad, db = distance(a, d), distance(d, b)
    def cosine(u, v):
        return sum(x*y for x,y in zip(u,v)) / math.hypot(*u) / math.hypot(*v)
    u = (a[0]-c[0],a[1]-c[1])
    v = (b[0]-c[0],b[1]-c[1])
    w = (d[0]-c[0],d[1]-c[1])
    equal_sectors = abs(cosine(u,w) - cosine(w,v)) < 1e-10
    assert equal_sectors, "The constructed CD must bisect the angle."
    return {
        "mode": mode,
        "points": {"A": list(a), "B": list(b), "C": list(c), "D": list(d)},
        "observations": {"AC": ac, "BC": bc, "AD": ad, "DB": db,
                         "is_symmetric_by_coordinates": abs(ac-bc)<1e-8,
                         "base_halves_equal_by_coordinates": abs(ad-db)<1e-8},
        "verified_material": ["D lies strictly between A and B", "CD joins C and D",
                              "ACD and BCD are material triangle subspaces",
                              "CD is the same carrier in both triangles"],
        "construction_given": ["angle(ACD) = angle(DCB) by angle-bisector construction"],
        "hypotheses_only": ["AD = DB ? (analogical destination, never a verified fact)"]
    }


def softmax_choose(options: list[dict], temperature: float, rng: random.Random) -> dict:
    top = max(x["score"] for x in options)
    weights = [math.exp((x["score"]-top)/temperature) for x in options]
    r = rng.random() * sum(weights)
    for option, weight in zip(options, weights):
        r -= weight
        if r <= 0:
            return option
    return options[-1]


def candidate_score(c: Codelet, active: dict, condition: str, chosen: set) -> dict:
    # Layer-specific inherited activation, not the heat/temperature itself.
    supports = {tag: round(active[tag], 4) for tag in c.tags if tag in active}
    # Opposition between the macrodomains strengthens candidates that *bridge*
    # the two; do not transfer this bias to every generic triangle grouping.
    crosses_domains = "angles" in c.tags and "sides" in c.tags
    inherited = 0.0
    if condition != "bottom_up":
        inherited += sum(0.20 * active[tag] for tag in c.tags if tag in ("angles", "sides"))
        inherited += 0.68 * active["opposition"] if crosses_domains else 0.0
        inherited += 0.12 * active["divider"] if "divider" in c.tags else 0.0
        inherited += 0.14 * active["sas"] if "sas" in c.tags else 0.0
        inherited += 0.10 * active["carrier"] if "carrier" in c.tags else 0.0
    structural_affordance = 0.10 * len(c.prerequisites)
    return {"id": c.id, "score": round(c.base + inherited + structural_affordance, 5),
            "bottom_up_base": c.base, "macro_inherited": round(inherited, 5),
            "inherited_from": supports if condition != "bottom_up" else {},
            "ready_because": list(c.prerequisites), "kind": c.kind}


def run(condition: str, mode: str, seed: int, budget: int = 12) -> dict:
    if condition not in CONDITIONS:
        raise ValueError(condition)
    if budget < 1:
        raise ValueError("budget must be positive")
    rng = random.Random(seed)
    geom = geometry(mode)
    selected = set()
    active = dict.fromkeys(MACRO_CONCEPTS, 0.0)
    if condition != "bottom_up":
        active.update({"angles": .64, "sides": .64, "opposition": .79,
                       "divider": .52, "sas": .31, "carrier": .41})
    timeline = [{"tick": 0, "event": "CONSTRUCTION_CD", "provenance": "material construction",
                 "geometry_stage": "after bisector", "macro_before": active.copy(),
                 "macro_after": active.copy(), "temperature": None,
                 "status": "constructed; no side equality is certified",
                 "note": "Angle split and base incidence create available microgroups, not an automatic median."}]
    first_opposition = None
    for tick in range(1, budget+1):
        available = [c for c in CODELETS if c.id not in selected and set(c.prerequisites) <= selected]
        if not available:
            break
        options = [candidate_score(c, active, condition, selected) for c in available]
        # Heat is sampling freedom; conceptual activation is the propagated signal.
        coherence = len(selected.intersection(STRUCTURAL_GENERIC_IDS)) / len(STRUCTURAL_GENERIC_IDS)
        temperature = round(max(.52, 1.19-.41*coherence), 4)
        choice = softmax_choose(options, temperature, rng)
        codelet = next(c for c in available if c.id == choice["id"])
        before = active.copy()
        selected.add(codelet.id)
        if first_opposition is None and codelet.id == "OPPOSITION_PAIR":
            first_opposition = tick
        feedback = {}
        if condition == "reciprocal":
            # The microgroup re-excites the macrodomain(s) that helped generate it.
            # A cross-domain match strengthens *opposition pressure* preferentially.
            for tag in codelet.tags:
                if tag in active:
                    gain = .08 if tag in ("angles", "sides") else .055
                    active[tag] = min(1., active[tag] + gain)
                    feedback[tag] = round(gain, 3)
            if "angles" in codelet.tags and "sides" in codelet.tags:
                active["opposition"] = min(1., active["opposition"]+.12)
                feedback["opposition"] = round(feedback.get("opposition",0)+.12, 3)
        if condition == "reciprocal":
            for key in active:
                active[key] = round(active[key]*.994, 6)
        # Feedforward mode keeps the initial macro tension fixed by design.
        timeline.append({
            "tick": tick,
            "event": "CODELET_SELECT_AND_GROUP",
            "codelet": codelet.id,
            "description": codelet.description,
            "causal_chain": [
                "CONSTRUCTION_CD",
                "macroopposition→microcandidate" if choice["macro_inherited"]>0 else "bottomup→microcandidate",
                codelet.id,
                "microgroup→macrofeedback" if feedback else "no_feedback"
            ],
            "available_candidate_count": len(options),
            "chosen_score": choice,
            "candidate_scores": options,
            "temperature": temperature,
            "macro_before": before,
            "macro_after": active.copy(),
            "feedback_delta": feedback,
            "new_mental_spaces": ["MS_LEFT", "MS_RIGHT"] if codelet.id in ("LEFT_TRIANGLE","RIGHT_TRIANGLE") else [],
            "status": "hypothesis_not_proof" if codelet.kind == "hypothesis_only" else "structural_candidate",
            "metric_assertions_certified": [],
        })
    formed = [e["codelet"] for e in timeline if e.get("codelet")]
    assert not any(e.get("metric_assertions_certified") for e in timeline)
    return {
        "condition": condition, "mode": mode, "seed": seed, "budget": budget,
        "construction": geom,
        "macro_tension": {
            "source": "angle(ACD)=angle(DCB)",
            "destination": "AD=DB?",
            "through": ["angle(ACD) opposite AD", "angle(DCB) opposite DB"],
            "direction": "angular_equality→candidate_segment_equality",
            "epistemic_status": "hypothesis_only"
        },
        "timeline": timeline,
        "formed_groups": formed,
        "metrics": {
            "selected_codelets": len(formed),
            "first_opposition_tick": first_opposition,
            "opposition_found": "OPPOSITION_PAIR" in selected,
            "sas_triple_found": "SAS_TRIPLETS" in selected,
            "prospective_transfer_found": "TRANSFER_TENSION" in selected,
            "grounded_generic_candidates": len(selected.intersection(STRUCTURAL_GENERIC_IDS)),
            "cross_domain_groups": len(selected.intersection(ANGLE_TO_SIDE)),
            "macro_inherited_selections": sum(e.get("chosen_score", {}).get("macro_inherited",0)>0 for e in timeline),
            "feedback_events": sum(bool(e.get("feedback_delta")) for e in timeline),
            "false_certified_metric_equalities": 0,
        }
    }


def experiment(seeds=range(24), budget=12) -> dict:
    contract = fixture_contract()
    runs = [run(condition, mode, seed, budget) for mode in MODES
            for condition in CONDITIONS for seed in seeds]
    aggregates = {}
    for mode in MODES:
        aggregates[mode] = {}
        for condition in CONDITIONS:
            trials = [r for r in runs if r["mode"] == mode and r["condition"] == condition]
            aggregates[mode][condition] = {
                "trials": len(trials),
                "opposition_rate": round(mean(r["metrics"]["opposition_found"] for r in trials),4),
                "sas_rate": round(mean(r["metrics"]["sas_triple_found"] for r in trials),4),
                "transfer_hypothesis_rate": round(mean(r["metrics"]["prospective_transfer_found"] for r in trials),4),
                "mean_cross_domain_groups": round(mean(r["metrics"]["cross_domain_groups"] for r in trials),4),
                "mean_grounded_generics": round(mean(r["metrics"]["grounded_generic_candidates"] for r in trials),4),
                "mean_first_opposition_tick_given_found": (round(mean(r["metrics"]["first_opposition_tick"] for r in trials
                    if r["metrics"]["first_opposition_tick"] is not None),3)
                    if any(r["metrics"]["opposition_found"] for r in trials) else None),
                "false_certified_metric_equalities": sum(r["metrics"]["false_certified_metric_equalities"] for r in trials)
            }
    return {
        "schema": "merovingio.gestalt_macro_micro_heat.v1",
        "kind": "seeded_cognitive_simulation_not_observed_human_data",
        "purpose": "Does macro-level angle↔side analogical pressure co-determine which micro-Gestalts emerge after CD?",
        "conceptual_limit": "Activation scores and codelet incentives are designed hypotheses, not learned cognition.",
        "no_proof": True, "no_jev": True,
        "fixture_contract": contract, "budget": budget, "seeds": list(seeds),
        "definitions": {
            "bottom_up": "materially available codelets compete without inherited macro-tension",
            "top_down": "initial angle/side/opposition conceptual activation biases micro-codelets; no feedback",
            "reciprocal": "same initial macro bias plus microgroup→macro activation feedback",
            "heat": "stochastic codelet choice temperature; distinct from spreading conceptual activation"
        },
        "aggregates": aggregates, "runs": runs
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--output", default=str(HERE/"results"))
    p.add_argument("--seeds", type=int, default=24)
    p.add_argument("--budget", type=int, default=12)
    args = p.parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    data = experiment(range(args.seeds), args.budget)
    (out/"traces.json").write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(data["aggregates"], indent=2))
    print("Saved", out/"traces.json")

if __name__ == "__main__":
    main()

"""Panoptikon v1.2: graph-encoded constructive genealogy, not free-form narrative.

Jev evaluates correspondence and salience. A deterministic oracle owns geometry.
The ordering of JSON arrays is manipulated independently of graph time order.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import random
from pathlib import Path
import sys

import requests

MODEL = "jev-1.14.0"
A = (0.0, 0.0)
B = (10.0, 0.0)
SHAPES = {
    "iso_low": (5.0, 4.0),
    "iso_high": (5.0, 8.0),
    "scalene_left": (3.2, 6.4),
    "scalene_right": (7.1, 5.2),
}
HISTORIES = ("upper_first", "lower_first")
PRESENTATIONS = ("canonical", "reversed", "shuffled")
MODES = ("no_history", "history")


def distance(p, q):
    return math.hypot(p[0] - q[0], p[1] - q[1])


def geometry(shape):
    """Simple independent certification of same- vs separate-divider contexts."""
    c = SHAPES[shape]
    t = distance(A, c) / (distance(A, c) + distance(c, B))
    upper_foot = (10 * t, 0.0)   # Angle bisector theorem, used by the oracle.
    lower_foot = (c[0], 0.0)    # Perpendicular onto horizontal base.
    iso = abs(distance(A, c) - distance(B, c)) < 1e-10
    shared = distance(upper_foot, lower_foot) < 1e-10
    assert shared == iso
    upper_carrier = "CD" if shared else "CE"
    lower_carrier = "CD" if shared else "CH"
    carriers = {
        "upper": {"id": upper_carrier, "endpoints": ["C", "D" if shared else "E"]},
        "lower": {"id": lower_carrier, "endpoints": ["C", "D" if shared else "H"]},
    }
    return {
        "shape": shape,
        "point_set": {"A": A, "B": B, "C": c,
                      **({"D": lower_foot} if shared else {"E": upper_foot, "H": lower_foot})},
        "carriers": carriers,
        "shared_carrier": shared,
        "upper_half_angle_equal_within_pair": True,
        "lower_angles_both_right": True,
        "cross_level_angle_equal": False,
    }


def final_workspace(shape):
    g = geometry(shape)
    return {
        "vertices": sorted(g["point_set"]),
        "carriers": [g["carriers"]["upper"], g["carriers"]["lower"]],
        "base": {"id": "AB", "endpoints": ["A", "B"]},
        "angle_spaces": {
            "upper": {"vertex": "C", "opposite_carrier": "AB",
                      "role": "pair of adjoining sectors at the apex",
                      "pair_internal_status": "the two sectors have equal measure"},
            "lower": {"vertex": "D" if g["shared_carrier"] else "H",
                      "role": "two adjoining right-angle sectors at the base",
                      "pair_internal_status": "both are right angles"},
        },
        "metrology_note": "Apex sectors and base right angles are not generally equal across pairs",
    }


def graph(shape, history):
    assert history in HISTORIES
    base = {
        "id": "O0", "type": "existing_workspace", "produces": ["AB", "AC", "BC"],
        "time": 0,
    }
    # Event ids and contents are fixed across genealogies. Only the causal/temporal
    # precedence and timestamps differ. Operators are typed, not English narrative.
    up = {
        "id": "O1", "type": "construct_apex_partition",
        "uses": ["C", "AB"], "produces_space": "upper",
        "support": geometry(shape)["carriers"]["upper"]["id"],
        "time": 1 if history == "upper_first" else 2,
    }
    low = {
        "id": "O2", "type": "construct_base_orthogonal_partition",
        "uses": ["C", "AB"], "produces_space": "lower",
        "support": geometry(shape)["carriers"]["lower"]["id"],
        "time": 2 if history == "upper_first" else 1,
    }
    join = {"id": "O3", "type": "final_material_snapshot", "time": 3}
    temporal_from, temporal_to = (("O1", "O2") if history == "upper_first"
                                  else ("O2", "O1"))
    edges = [
        {"from": "O0", "to": "O1", "relation": "requires_material"},
        {"from": "O0", "to": "O2", "relation": "requires_material"},
        {"from": "O1", "to": "O3", "relation": "contributes_to_final"},
        {"from": "O2", "to": "O3", "relation": "contributes_to_final"},
        {"from": temporal_from, "to": temporal_to, "relation": "precedes"},
    ]
    return {"nodes": [base, up, low, join], "edges": edges,
            "semantics": "time and typed edges define order, not array position"}


def ordered_graph(shape, history, presentation):
    g = graph(shape, history)
    if presentation == "reversed":
        g["nodes"].reverse()
        g["edges"].reverse()
    elif presentation == "shuffled":
        # Separate seeded permutations for nodes and edges. Stable across runs.
        rng = random.Random(20261017 + list(SHAPES).index(shape) * 19
                            + list(HISTORIES).index(history) * 101)
        rng.shuffle(g["nodes"])
        rng.shuffle(g["edges"])
    elif presentation != "canonical":
        raise ValueError(presentation)
    return g


def graph_signature(g):
    """Invariant to serialization, sensitive to actual timestamps and edges."""
    canonical = {
        "nodes": sorted(g["nodes"], key=lambda v: v["id"]),
        "edges": sorted(g["edges"], key=lambda v: (v["from"], v["to"], v["relation"])),
    }
    return hashlib.sha256(json.dumps(canonical, sort_keys=True).encode()).hexdigest()


def construct_payload(shape, history=None, presentation=None):
    state = {"workspace": final_workspace(shape),
             "epistemic_scope": "Two pairs of angles, structural mapping distinct from equality of measure"}
    if history is not None:
        state["construction_graph"] = ordered_graph(shape, history, presentation)
    questions = {
        "same_support": {
            "type": "noul",
            "instructions": "Do the two angular pairs share exactly the same physical construction carrier?",
            "criteria": {"true": "One identical segment is used for both pairs",
                         "false": "Different physical carrier segments"},
        },
        "cross_measure": {
            "type": "noul",
            "instructions": "Does the workspace force the apex half-angles to have the same measure as the base right angles?",
            "criteria": {"true": "The cross-level angle measures are necessarily equal",
                         "false": "No cross-level metrical equality follows"},
        },
        "next_focus": {
            "type": "choice",
            "instructions": "Select which structural relation to explore next in this workspace. All options may be useful; this is an attention preference, not a proof. Consider construction genealogy only if available. Treat role analogy and angular equality as distinct.",
            "criteria": {
                "upper": "Inspect the pair of angular sectors at the apex",
                "lower": "Inspect the pair of right-angle sectors at the base",
                "joint": "Explore the correspondence between upper and lower pairs via shared roles",
                "separate": "Explore two independently arising angular partitions",
            },
        },
    }
    if history is not None:
        # This is a *control*: the model must recover event order from graph, not
        # lexical placement of the nodes. No answer labels are included.
        questions["last_event"] = {
            "type": "choice",
            "instructions": "Based only on causal timestamps/precedence in construction_graph, which angular space was introduced later? Ignore the order in which graph nodes are serialized.",
            "criteria": {"upper": "The apex-angle partition appeared later",
                         "lower": "The base right-angle partition appeared later"},
        }
    return {"model": MODEL, "state": state, "questions": questions}


def run_schedule():
    result = []
    for shape in SHAPES:
        # Same static facts as v1.1; two baseline repeats estimate model noise.
        for repeat in (0, 1):
            result.append({"shape": shape, "condition": "final_only", "repeat": repeat})
        for history in HISTORIES:
            for presentation in PRESENTATIONS:
                result.append({"shape": shape, "condition": "causal_graph",
                               "history": history, "presentation": presentation})
    return result


def call_jev(payload):
    key = os.environ.get("TYPESAFE_API_KEY")
    if not key:
        raise RuntimeError("TYPESAFE_API_KEY secret unavailable")
    r = requests.post("https://api.typesafe.ai/v1/systemone",
                      json=payload, headers={"Authorization": "Bearer " + key}, timeout=90)
    if not r.ok:
        raise RuntimeError("Jev responded HTTP " + str(r.status_code))
    body = r.json()
    answers = body.get("answers", {})
    if not all(q in answers for q in payload["questions"]):
        raise RuntimeError("Incomplete Jev answers")
    out = {}
    for name in ("same_support", "cross_measure"):
        value = answers[name].get("noul")
        if not isinstance(value, (float, int)) or not 0 <= value <= 1:
            raise RuntimeError("Unexpected noul response")
        out[name] = value
    for name in ("next_focus", "last_event"):
        if name not in answers:
            continue
        a = answers[name]
        possible = set(payload["questions"][name]["criteria"])
        if a.get("choice") not in possible:
            raise RuntimeError("Unexpected choice response")
        out[name] = {"choice": a.get("choice"),
                     "probabilities": a.get("probabilities"),
                     "confidence": a.get("confidence")}
    out["usage"] = body.get("usage")
    out["model"] = body.get("model")
    return out


def probabilities_of_focus(answer):
    prob = answer.get("probabilities") or {}
    if not isinstance(prob, dict):
        raise RuntimeError("Malformed focus probabilities")
    return prob


def produce_report(out: Path):
    if not os.environ.get("TYPESAFE_API_KEY"):
        raise SystemExit("Missing GitHub Actions secret; no calls attempted")
    out.mkdir(parents=True, exist_ok=True)
    results = []
    for record in run_schedule():
        shape = record["shape"]
        if record["condition"] == "final_only":
            payload = construct_payload(shape)
        else:
            payload = construct_payload(shape, record["history"], record["presentation"])
        response = call_jev(payload)
        g = geometry(shape)
        item = {
            **record,
            "independent_geometry_oracle": {"carrier_shared": g["shared_carrier"],
                                             "cross_level_equal": False},
            "response": response,
            "carrier_verdict_correct": (response["same_support"] >= 0.5) == g["shared_carrier"],
            "cross_level_verdict_correct": response["cross_measure"] < 0.5,
        }
        if item["condition"] == "causal_graph":
            expected = "lower" if item["history"] == "upper_first" else "upper"
            item["expected_last_event_offline"] = expected
            item["temporal_order_correct"] = response["last_event"]["choice"] == expected
            item["graph_signature"] = graph_signature(graph(shape, item["history"]))
        results.append(item)
        message = f'{shape} {item["condition"]}'
        if item["condition"] == "causal_graph":
            message += f' {item["history"]}/{item["presentation"]}: time_ok={item["temporal_order_correct"]}'
        print(message + f' joint_p={probabilities_of_focus(response["next_focus"]).get("joint")}', flush=True)
    summary = {"n_calls": len(results),
               "shared_correct": sum(r["carrier_verdict_correct"] for r in results),
               "cross_measure_correct": sum(r["cross_level_verdict_correct"] for r in results),
               "time_correct": sum(r.get("temporal_order_correct", False) for r in results),
               "time_tested": sum("temporal_order_correct" in r for r in results),
               "total_input_tokens": sum((r["response"]["usage"] or {}).get("input_tokens",0) for r in results),
               "total_output_tokens": sum((r["response"]["usage"] or {}).get("output_tokens",0) for r in results)}
    report = {"experiment": "Panoptikon v1.2 causal graph, chronology vs serialization",
              "model": MODEL,
              "caution": "No single correct salience choice; independent samples and richer geometries required.",
              "definitions": {"history": "timestamps and causal precedes edge, not array order",
                              "presentation": "different serialization of identical typed graph"},
              "summary": summary, "trials": results}
    (out / "jev_causal_graph_v12.json").write_text(json.dumps(report, indent=2, ensure_ascii=False))
    print("Saved sanitized report", summary)
    return report


if __name__ == "__main__":
    destination = Path(sys.argv[1] if len(sys.argv) > 1 else "output_v12")
    produce_report(destination)
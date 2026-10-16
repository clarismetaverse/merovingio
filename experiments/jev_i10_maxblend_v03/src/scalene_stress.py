"""Live Jev Vision runner. The model never receives method names or proof labels."""
from __future__ import annotations

import base64
import json
import os
from pathlib import Path
import sys

from prototype import call_jev
from scalene_visuals import SHAPES, METHODS, MODES, fractions, label_order, render

EXPECTED = {"angle": "angle", "segment": "segment", "orthogonal": "orthogonal"}
PROMPTS = {
    "free": (
        "Compare the candidate new workspaces without a theorem goal. "
        "Which connector produces coherent, non-redundant mixed side-angle regroupings "
        "across the two resulting regions? Assess relations, not visual centeredness. "
        "Different choices may be defensible."
    ),
    "angle": (
        "The active conceptual partition is of the apex angle into two equal angular sectors. "
        "Which connector would generate this partition and two adjacent mixed side-angle groups?"
    ),
    "segment": (
        "The active conceptual partition is of the base segment into two equal subsegments. "
        "Which connector from the apex realizes this while creating two adjacent mixed groups?"
    ),
    "orthogonal": (
        "The active conceptual partition divides a straight angle at the base into "
        "two adjacent right angles. Which connector from the apex realizes it?"
    ),
}


def encode_png(path):
    return {"type": "image", "format": "png",
            "data_base64": base64.b64encode(path.read_bytes()).decode("ascii")}


def make_trial(out, shape, mode):
    mapping, seed = label_order(shape, mode)
    folder = out / "images" / shape
    assets = {"initial": encode_png(render(folder / "initial.png", shape))}
    for label, method in mapping.items():
        assets["img-" + label.lower()] = encode_png(
            render(folder / (method + ".png"), shape, method)
        )
    state = {
        "initial_workspace": "initial",
        "mental_spaces": [
            "a base carrier with two endpoints and possible subdivisions",
            "two rays forming an angle at an apex",
            "a triangular configuration that can be regrouped into two adjacent subconfigurations"
        ],
        "candidate_workspaces": [
            {"id": label, "image": "img-" + label.lower()} for label in mapping
        ],
        "epistemic_note": "These are hypothetical constructions, not proven equalities."
    }
    choices = {label: "Workspace shown by img-" + label.lower() for label in mapping}
    choices["none"] = "None of the candidate drawings realizes the requested grouping"
    payload = {
        "model": "jev-1.14.0",
        "state": state,
        "assets": assets,
        "questions": {"best_bridge": {
            "type": "choice",
            "instructions": PROMPTS[mode],
            "criteria": choices
        }}
    }
    return payload, mapping, seed


def main():
    destination = Path(sys.argv[1] if len(sys.argv) > 1 else "output_scalene")
    if not os.environ.get("TYPESAFE_API_KEY"):
        raise SystemExit("Missing TYPESAFE_API_KEY secret: no API call attempted.")
    destination.mkdir(parents=True, exist_ok=True)
    trials = []
    for shape in SHAPES:
        for mode in MODES:
            payload, mapping, seed = make_trial(destination, shape, mode)
            response = call_jev(payload)
            answer = response["answers"]["best_bridge"]
            code = answer.get("choice")
            if code not in mapping and code != "none":
                raise ValueError("Unknown option identifier from Jev")
            selected = mapping.get(code)
            expected = EXPECTED.get(mode)
            result = {
                "shape": shape, "mode": mode, "randomization_seed": seed,
                "candidate_mapping": mapping, "choice_id": code,
                "choice_method": selected,
                "ground_truth_method": expected,
                "matches_target": (selected == expected) if expected else None,
                "confidence": answer.get("confidence"),
                "probabilities": answer.get("probabilities"),
                "usage": response.get("usage")
            }
            trials.append(result)
            print(shape, mode, "selected:", code, "target_match:", result["matches_target"])
    report = {
        "experiment": "Scalene role-selection anti-symmetry v0.4",
        "model": "jev-1.14.0",
        "note": "Free exploration has no objectively unique winning construction.",
        "conditioned_accuracy": {
            "correct": sum(x["matches_target"] is True for x in trials),
            "total": sum(x["matches_target"] is not None for x in trials)
        },
        "geometric_oracle": {s: fractions(s) for s in SHAPES},
        "trials": trials
    }
    (destination / "scalene_results.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("Sanitized results written; no key was recorded.")


if __name__ == "__main__":
    main()

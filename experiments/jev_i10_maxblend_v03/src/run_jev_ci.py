"""Safe, single-call live Jev evaluation for I.10 exploratory grouping.

No I.10 goal or proof is sent. The API key is read only from the environment
and is never written to reports or printed.
"""
from __future__ import annotations
import json
import os
from pathlib import Path
import sys

from prototype import build_all, jev_payload, call_jev


def run(out: Path, seed: int = 19) -> dict:
    if not os.environ.get("TYPESAFE_API_KEY"):
        raise SystemExit("Missing TYPESAFE_API_KEY Actions secret; live request NOT attempted.")
    results = build_all(out)
    request = jev_payload(results, out, seed=seed, model="jev-1.14.0")
    # Use raw candidate diagrams: the model must identify groups itself,
    # rather than rely on deliberately colored, post-hoc annotations.
    for candidate in results:
        img_key = f"im-{candidate['id'].lower()}"
        png = out / "images" / f"{candidate['id']}_raw.png"
        import base64
        request["assets"][img_key]["data_base64"] = base64.b64encode(png.read_bytes()).decode("ascii")

    response = call_jev(request)
    answers = response["answers"]
    choice = answers["best_bridge"]
    selected = choice.get("choice")
    allowed = {row["id"] for row in results} | {"none"}
    if selected not in allowed:
        raise ValueError("Unexpected choice id in API response")
    scores = {}
    for row in results:
        aid = f"alignment_{row['id']}"
        ans = answers.get(aid, {})
        scores[row["id"]] = {
            "score": ans.get("score"),
            "confidence": ans.get("confidence"),
            "probabilities": ans.get("probabilities"),
        }
    report = {
        "experiment": "I.10 exploratory mixed side-angle grouping (no goal, no proof)",
        "mode": "LIVE_JEV_API",
        "model": response.get("model"),
        "candidate_count": len(results),
        "randomized_candidate_order_seed": seed,
        "chosen_candidate": selected,
        "choice_confidence": choice.get("confidence"),
        "choice_probabilities": choice.get("probabilities"),
        "per_candidate_alignment": scores,
        "baseline_only_ranking": [
            {"id": r["id"], "heuristic_score": r["heuristic_blend_value"]}
            for r in sorted(results, key=lambda v: -v["heuristic_blend_value"])
        ],
        "usage": response.get("usage"),
        "limitations": [
            "A choice is not a geometric proof.",
            "A single symmetric example cannot establish generalization.",
            "Anonymous candidate ids are stable across renderings; future tests must randomize ids and geometry."
        ],
    }
    out.mkdir(parents=True,exist_ok=True)
    (out / "jev_summary.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
    print("Jev model:",report["model"])
    print("Chosen anonymized candidate:",selected)
    print("Confidence:",report["choice_confidence"])
    print("Report: output/jev_summary.json (no secrets, no request body)")
    return report

if __name__ == "__main__":
    out = Path(sys.argv[1] if len(sys.argv)>1 else "output")
    run(out)
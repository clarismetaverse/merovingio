#!/usr/bin/env python3
"""Compare selection at one step to short recursive horizon, with frozen priors."""
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
OUT=HERE/"results"
a=json.loads((OUT/"one_step"/"aggregates.json").read_text(encoding="utf-8"))
b=json.loads((OUT/"aggregates.json").read_text(encoding="utf-8"))
lines=[
"# Merovingio v7 — One-step selectivity vs three-REBASE accumulation",
"",
"Frozen parameters and identical seed set. The first horizon isolates whether",
"the agent chooses the correctly co-generated partition immediately;",
"the second allows a short cumulative REBASE loop.",
"",
"| Attention | Scenario | Strategy | One step completion | Three steps completion | Mean first completion tick (three) |",
"|---|---|---|---:|---:|---:|",
]
for attention in a:
    for scenario in a[attention]:
        for cond,item in a[attention][scenario].items():
            three=b[attention][scenario][cond]
            lines.append("| "+" | ".join([
                attention,scenario,cond,
                str(item["completion_rate"]),str(three["completion_rate"]),
                str(three["first_completion_tick_if_found"])])+" |")
lines.extend([
    "",
    "## Reading",
    "A completion in this test means a cognitive pairing of two partitions",
    "with the same material anchor and rooted construction genealogy;",
    "it never proves equality of angles or lengths.",
    "The independent control has no matching genealogical root and should",
    "not generate a mediated double-partition GS.",
    "A high three-step rate can be saturation rather than intelligent choice;",
    "the one-step benchmark isolates early selectivity.",
    "All priors are hand-chosen and frozen from v6; this is a software",
    "simulation, not evidence about historical Euclid or human psychology.",
    "",
])
(OUT/"HORIZON_COMPARISON.md").write_text("\n".join(lines),encoding="utf-8")
print("Wrote",OUT/"HORIZON_COMPARISON.md")

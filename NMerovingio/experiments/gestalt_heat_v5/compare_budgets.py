"""Compare genuinely selective search against the high-coverage saturation control."""
import json
from pathlib import Path
OUT=Path(__file__).resolve().parent/"results"
primary=json.loads((OUT/"aggregates.json").read_text(encoding="utf-8"))
saturation=json.loads((OUT/"saturation"/"aggregates.json").read_text(encoding="utf-8"))
lines=[
"# Merovingio v5 — Selective vs Saturated Search",
"",
"Two horizons are evaluated on the **same** graph, seed set, and scoring system.",
"",
"- **Four steps**: selective benchmark; only a minority of opposition edges are explored.",
"- **Eight steps**: saturation control, close to exhausting the available opposition edges.",
"",
"| Geometry | Condition | 4-step question rate | 8-step question rate | 4-step mean Generic Spaces | 4-step mean rank changes |",
"|---|---|---:|---:|---:|---:|",
]
for mode,cases in primary.items():
    for cond,x in cases.items():
        y=saturation[mode][cond]
        lines.append("| "+" | ".join([
            mode,cond,str(x["transfer_question_rate"]),str(y["transfer_question_rate"]),
            str(x["mean_induced_generics"]),str(x["mean_rank_reorderings"])])+" |")
lines+=["",
"**Interpretation:** More rank changes measure real reordering by graph propagation,",
"not necessarily more useful inferences. A fixed ranking that already prioritizes",
"the target may outperform dynamic search under a small budget. The model is",
"hand-engineered and is not validated cognitive science.",
"",
"Both conditions preserve the distinction between analogical questions and",
"formally verified equalities; **no** metric assertions are certified.",
""]
(OUT/"SATURATION_COMPARISON.md").write_text("\n".join(lines),encoding="utf-8")
print("Created",OUT/"SATURATION_COMPARISON.md")

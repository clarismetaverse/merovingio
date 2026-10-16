# Merovingio — Jev v0.7 Structural Bridge Selection (live run 01)

**Status:** 24 authenticated Jev 1.14 calls completed; GitHub Actions succeeded.  
**Source branch:** `experiment/jev-structural-bridges-v0.7` (no merge into main).  
**Workflow:** https://github.com/clarismetaverse/merovingio/actions/runs/38983318251  
**Artifact:** `jev-structural-bridges-v07`; normalized JSON in `/Merovingio/Results/jev-structural-bridges-v07-summary.json` (ChatGPT Library).

## Question

Select a construction creating the most useful **structural cross-space re-partition**, conditional on two salient Mental Spaces. Unlike v0.5 and v0.6, do **not** ask Jev to detect exact equality of angles or lengths by inspecting pixels.

## Fixed inputs

- Two scalene triangle configurations, apex displaced left/right.
- Four construction families with distinctly different structural consequences: vertex-to-opposite-side from C, from A, from B, and between interior points on CA and CB.
- Four focus frames: wedge C + AB; wedge A + BC; wedge B + AC; side-pair CA + CB.
- Conditions: A images with original-space context; B plus candidate Mental Spaces; C plus candidate Generic Spaces.
- The same candidate images and anonymous option IDs within each shape/focus across all three conditions.
- Counterbalance: each correct option falls twice into K1, K2, K3 and K4 (per condition).
- Deterministic geometric/topological oracle validates strict betweenness and shared boundary between new regions. No metric equality and no theorem proof.

## Real results

| Condition | Correct | Mean reported confidence | API input tokens | API output tokens |
| --- | ---: | ---: | ---: | ---: |
| A images + original focus | 8 / 8 | 0.884 | 111,376 | 408 |
| B + induced Mental Spaces | 8 / 8 | 0.916 | 116,608 | 408 |
| C + candidate Generic Spaces | 8 / 8 | 0.897 | 122,880 | 408 |
| **Total** | **24 / 24** | | **350,864** | **1,224** |

Every frame was selected correctly for both shapes across all three conditions. Under the defined task, there was no gain in accuracy from providing candidate structural data because the image+focus baseline was already at ceiling. The modest difference in confidence is not proof of better calibration or accuracy.

## Interpretation and limitations

**What it supports:** Jev is capable of reliably choosing the relevant *type of constructive bridge* from visual alternatives when the focal conceptual spaces are explicitly identified, on these 8 paired cases. Crucially, an operation can be useful for one focus and inappropriate for another; this is not merely selecting an intrinsically symmetric axis.

**What it does NOT support:** general-purpose discovery of Generic Spaces, geometric theorem proving, inference of angle equality, a causal advantage from the Mental Space representations, or statistical generalization. The visual condition already includes original-space descriptions and fairly explicit task wording; this is not blind open-ended invention. The symbolic structures are generated and validated by deterministic code rather than inferred by Jev.

Confidence: mean A 0.884, B 0.916, C 0.897; N=8 per condition is too small for reliable differences. All outcomes were correct in this restricted test. The two shapes are near-mirror configurations; external validity is not established.

## Next tests

1. Add less explicit focus statements and distractor bridges that partially satisfy the goal; avoid trivially obvious endpoint matching.
2. Evaluate **held-out workspace families** (quadrilaterals, two intersecting lines, angle and circle frames).
3. Introduce negative/unanswerable frames with an abstention option and assess confidence calibration.
4. Model constructive **sequences** with multiple steps, emergence of Generic Spaces, and delayed back-propagation. Compare against a graph-matching baseline and human-chosen partitions.
5. Reconcile the dashboard token counter with confirmed Jev API response `usage`: the zero displayed in TypeSafe UI is inconsistent with 350,864 + 1,224 reported tokens on this run (not yet diagnosed).

### Reproducibility

Code: `experiments/jev_i10_maxblend_v03/src/structural_bridges_v07.py`  
Tests: `experiments/jev_i10_maxblend_v03/tests/test_structural_bridges_v07.py`  
Action: `.github/workflows/jev-structural-bridges-v07.yml`  
Artifacts contain diagrams and per-trial distributions. No API credentials are stored in repository outputs.

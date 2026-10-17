# Panoptikon v1.3 — Results: material state, support graph, and temporal precedence

**Controlled run:** https://github.com/clarismetaverse/merovingio/actions/runs/39020639934  
**Pilot run (different question batches; not used for primary comparison):** https://github.com/clarismetaverse/merovingio/actions/runs/39020407546  
**Branch:** `experiment/panoptikon-causal-ablation-v1.3`  
**Model:** `jev-1.14.0`  
**Status:** 56 successful authenticated API calls, six local geometry/request tests passing, source saved on a research branch; `main` untouched.

## Experimental question

Can the temporal ordering of two angular Mental Spaces alter the model's exploratory preference for their shared Generic Space **after controlling for final geometric state and structural support relations**?

The two spaces in question are (i) the two equal sectors induced at the apex by an angle bisector; (ii) two right-angle sectors induced at the base by an altitude. These spaces may have the **same physical carrier** in an isosceles triangle or **different carriers** in a scalene triangle. *Corresponding roles are not corresponding metrical angles*. This study never asks Jev to prove a theorem.

## Controls

- **F — final state:** only the final workspace, angle-pair descriptions, and carrier identities. Each of four figures repeated twice to estimate noise.
- **S — structural supports:** same F facts plus a typed non-temporal dependency DAG for the two partitions. Neither steps nor chronology appear in S. History names appear in offline scoring only. The **actual API payload is identical** for both histories at matched figure/serialization.
- **T — temporal order:** exactly the S data and the **same three typed questions**, with only `step` and one `happens_before` edge added. Compare `upper_first` and `lower_first`; identical typed support facts.

Four geometries (two isosceles, two scalene), three node/edge serializations (canonical, reversed, shuffled), two genealogical orders. Tests certify support-only payload identity between histories, canonical signature invariance under JSON reordering, and no oracle/secret leakage.

## Primary result

| Condition | Jev calls | Mean P(choose joint correspondence) | Shared-carrier judgment correct | Cross-level false equality rejected | Input tokens | Output tokens |
|---|---:|---:|---:|---:|---:|---:|
| F: final only | 8 | 29.75% | 8/8 | 8/8 | 5,880 | 704 |
| S: + support DAG | 24 | 40.67% | 18/24 | 24/24 | 25,416 | 2,098 |
| T: + chronology | 24 | 39.17% | 23/24 | 24/24 | 26,664 | 2,100 |
| **TOTAL** | **56** | — | **49/56** | **56/56** | **57,960** | **4,902** |

Adding explicit support structure is associated with an increase of **+10.92 percentage points** in average joint-space prioritization. Adding chronology beyond S changes that figure by **-1.50 pp**; there is no positive general chronology lift here.

## Focused test of direction of genealogy

For each figure and JSON presentation we compute:

`ΔT = P(joint | T, upper-first) − P(joint | T, lower-first)`  
`ΔS = P(joint | S, replicate A) − P(joint | S, replicate B)`  
`Contrast = ΔT − ΔS`

Across the 12 matched contrasts:

- Mean `ΔT` = **+1.00 pp** (different time direction).
- Mean `ΔS` = **-0.33 pp** (same input, independent noisy responses).
- Mean contrast = **+1.33 pp**.
- Mean absolute support-only repeat difference = **2.00 pp**.
- Mean absolute chronology-direction difference = **3.50 pp**.
- Individual matched contrasts range from **-7.00 to +7.00 pp**.

A 1.33 pp directional difference is comparable to the uncontrolled fluctuations of identical support-only inputs. These observations **do not provide convincing evidence for genealogy-direction-dependent salience** in the model. This is a descriptive matched subtraction, not randomized causal inference or statistical proof.

## Negative controls and diagnostic surprise

The model correctly rejected false equality of apex half-angles and lower right angles **56/56 times**. It correctly identified shared support **8/8** in F, **18/24** in S, and **23/24** in T. Specifically in **scalene** geometries, S produced only **6/12** correct separate-carrier judgments, despite the same distinct `CE` vs `CH` IDs appearing in final facts. T scored **11/12** in those cases. The extra temporal context may change how the model attends to support identity, but these are limited, correlated trials and not proof that chronological reasoning is responsible.

The original pilot run asked an additional temporal-comprehension question only in T. Jev answered that diagnostic **24/24** correctly, but that experiment had unequal question batches. Its results are retained for provenance and not compared as the primary isolated treatment. The updated controlled run sends the **same three questions** in F/S/T, avoiding that confound.

## Architectural consequence

Preserve distinct layers:

1. `material_state` — verified points, carrier identity, measured geometric constraints.
2. `support_graph` — event-independent dependencies and conceptual participation in carriers.
3. `temporal_genealogy` — precedence edges, first appearance, producer events.
4. `candidate_generic_space` — hypothetical role alignments, scored probabilistically by Jev, never treated as geometric truth.

For now, evidence favors support-structure awareness over temporal ordering as a determinant of this narrowly defined exploratory prioritization. True prospective blending and spontaneous new Mental Space generation remain untested.

## Next rigorous experiment

Randomize **different support topologies while holding time fixed**, then apply contradictory or permuted event histories (always with explicit contradiction checks and an abstention class). Use more diverse geometries and a held-out group; reduce lexical hints. This could help separate meaningful causal mediation from incidental prompt sensitivity.

## Files

- `NMerovingio/causal_ablation_v13/causal_ablation_v13.py`
- `NMerovingio/causal_ablation_v13/tests/test_causal_ablation_v13.py`
- `.github/workflows/panoptikon-causal-ablation-v13.yml`
- Artifact ZIP `panoptikon-v13-controlled-results.zip` containing per-response distributions and token usage, with no secrets.
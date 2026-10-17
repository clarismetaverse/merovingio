# Panoptikon v1.2 — Causal Graph Genealogy (live run 01)

**Code branch:** `experiment/panoptikon-causal-graph-v1.2`  
**GitHub Actions:** https://github.com/clarismetaverse/merovingio/actions/runs/39019742795  
**Model:** Jev `jev-1.14.0`, 32 successfully completed calls.  
**Artifact:** `panoptikon-causal-graph-v12`, JSON `jev_causal_graph_v12.json`.  
**Security:** the existing `TYPESAFE_API_KEY` GitHub Actions secret was used without being included in logs, source code or reports.

## Design and controls

Same physical final workspace within each of four geometries: two isosceles (`iso_low`, `iso_high`, where angle-bisector and base perpendicular coincide), two scalene (`scalene_left`, `scalene_right`, where they differ). Angle equality *within* each pair is distinguished from unlicensed equality *across* apex and right-angle pairs.

Causal-graph genealogies `upper_first` and `lower_first` contain the same typed nodes and material dependencies; only causal precedence and event times differ. Each graph is serialized **canonical / reversed / shuffled**, with exact canonical-signature invariance verified locally. Two history-blind repeats per shape give an estimate of baseline response variability.

Questions in each call: two factual `noul` judgments about physical common support and cross-level equality, plus a goal-free `choice` of what to explore next. Graph trials additionally ask which Mental Space was instantiated last; this is a validation that the model read the chronology, not an inferential proof.

## Live quantitative outcomes

| Check | Correct / trials | Interpretation |
| --- | ---: | --- |
| Later-created space, when graph supplied | **24/24** | Reads timestamp/precedence irrespective of node-array ordering |
| Common physical carrier | **28/32** | Four mistakes all on history-blind isosceles cases |
| No cross-level angular equality | **32/32** | Avoids converting role analogy into a metric identity |

The **history-blind isosceles** cases returned `P(shared) = 0.23–0.26` despite matching carrier identifiers in the static description (0/4 correct). Adding the graph increased this to `0.82–0.88` in the isosceles trials (12/12 correct). The added graph includes explicit support attributes; this improvement therefore **cannot be attributed specifically to construction order**. Both scalene shapes were correctly identified as not sharing a physical carrier in all representations.

## Salience of the joint upper/lower correspondence

| Condition | Mean Jev P(joint) |
| --- | ---: |
| Final state only, two repeats per shape | **0.603** |
| Graph, apex first | **0.623** |
| Graph, base first | **0.593** |
| Graph with canonical node order | **0.585** |
| Graph with reversed node order | **0.629** |
| Graph with shuffled node order | **0.611** |

`upper_first` minus `lower_first` = approximately **+0.030** pooled over the four shapes. `reversed` minus `canonical` display = approximately **+0.044** pooled over both histories. Within the same shape and same causal history, P(joint) varied by **0.01–0.10** across array serialization orders that preserve the exact same graph.

The four shape-specific upper-minus-lower differences were: `iso_low +0.063`, `iso_high +0.040`, `scalene_left +0.027`, `scalene_right -0.010`. The small genealogy-dependent signal is thus **not separable from presentation sensitivity or model response noise** in this benchmark.

**Reported API usage:** 35,960 input tokens and 3,320 output tokens across 32 calls. This counts API-reported usage, not externally verified billing.

## Scientific interpretation

1. **Supported:** the typed graph retains constructive genealogy independent of JSON presentation order; Jev can identify temporal precedence and avoid confusing structural role correspondences with angular-measure equality.
2. **Suggested but unresolved:** explicit generative-support relationships help Jev recognize the common physical carrier more reliably than the final-only structural description, but this is **an input-information effect**, not necessarily cognitive genealogy.
3. **Not demonstrated:** a genuine causal influence of *which pair was constructed first* on the priority of an emergent Generic Space. Narrative/event priming and serialization effects remain confounders.
4. **Not attempted:** autonomous discovery of new Mental Spaces, invention of a construction, theorem proving, or free-form explanation from Jev's typed outputs.

## Next controlled comparison

Factor the input explicitly into `(final geometry)`, `(support/provenance graph without order)`, `(same graph with chronological precedence)` and `(same ordered graph with shuffled serialization)`. Use several independent candidate constructions and hold-out shape families. This 4-condition ablation would isolate **support information** from **temporal genealogy** more cleanly. Repeat each identical payload several times to estimate model variance.

Reproduction: `NMerovingio/causal_graph_v12/graph_genealogy_v12.py`, `tests/test_graph_genealogy_v12.py`, `.github/workflows/panoptikon-causal-graph-v12.yml`.
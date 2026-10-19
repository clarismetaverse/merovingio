# Explicit incidence tables and literal identifier comparisons

Parent 46309be, branch codex/explicit-incidence-tables. Main, v0.9/v1.0 and all previous experiments remain preserved. Jev 1.14.0; live only through Actions with the repository secret and required images header.

## Small matched experiment

Reuse replicas 0 and 3 and all six counterexamples from run 39236636905. The baseline is that experiment's relevant_state condition, reconstructed exactly from stored input and frozen PNGs. Each block has the identical two witness questions. Compare the same block in graph and incidence_tables conditions: two replicas x six cases x two formats x two questions = 48 primary judgments in 24 calls. A fresh graph baseline exposes run-to-run drift. Format order is counterbalanced six graph-first/six table-first, with shuffled block order.

Add four separate literal-ID controls in two additional calls, for 52 total judgments in 26 calls. For each replica, use actual carrier IDs from the source workspace as one equal pair S/S and one distinct pair S/T. State exposes only these operand strings. Native Choice options distinguish literal identity, distinct strings and insufficient evidence, under neutral shuffled labels. These requests contain neither graph nor images and are not batched with witness questions. Their operands or answers cannot become hints in the primary state.

## Lossless table format

Only representation of the same reduced object set changes. Remove the objects dictionary and replace it with four explicit column/row tables:

| Table | Columns |
| --- | --- |
| points | object_id, x, y |
| carriers | object_id, endpoint_0, endpoint_1 |
| polygons | object_id, object_type, ordered_vertex_ids |
| boundary_uses | region_id, use_index, carrier_id, use_endpoint_0, use_endpoint_1 |

Every object, material ID, polygon cycle, endpoint coordinate, boundary use and within-object order is preserved exactly. Object types are carried by the typed table or polygon type column. The use_index serializes the pre-existing boundary-use array order; it is not a computed property of a binding. Relative row order within each table follows source-object iteration order. Grouping object types into separate tables is part of the formatting intervention.

No equality or full-side flags, candidate validity, areas, containment results, missing-premise analysis, selected binding or gold label is supplied. The encode/decode roundtrip must reproduce the source object dictionary. Every proposed witness has the same independent failure reasons and every graph binding remains unchanged. Unknown source fields fail rather than being silently discarded. Contracts, identity/evidence policies, schema and snapshot aliases, original image manifest, all image bytes, instructions, question order and options remain exactly identical within every format pair.

## Readout and interpretation

Each primary condition has 24 questions, eight valid-listed positives and sixteen none-required negatives. Report both classes, matrices by case/schema, invalid-witness choices, identity-counterfactual pair success and exact paired changes. Always none gives 16/24 and is not a working binding policy. Retain the previous graph responses separately, and report historical drift without conflating it with the current paired effect.

Literal controls directly test comparison of shown strings. Passing them while failing witness selection would locate the observed difficulty beyond a bare literal equality operation: it could concern retrieving carrier references, integrating constraints, representation, context or finite-option selection. It would not identify an internal mechanism. Table improvement would support sensitivity to this concrete formatting intervention; a null effect would not rule out every possible table format. Layout, grouping and token-length changes are not separately isolated, and the image context stays present in the main task.

All results concern two transformed synthetic replicas with supplied structural facts and finite witness options. They do not establish general ID-comparison ability, autonomous visual extraction, proof, free-form binding discovery or internal sequential reasoning. Raw native answers are reported before any deterministic rejection. Confidence is not treated as correctness and no threshold is tuned.

## Execution and artifacts

Only Actions may call Jev with TYPESAFE_API_KEY secret and TypeSafe-Danger-Zone-Images: true. Text-only literal controls also use the same guarded transport, omitting image assets. No new Score requests, automatic retries or long-context header. Checkpoint every request and stop on HTTP 400/401/403, retaining sanitized failures. Offline mode has no model scores or invented results.

Save native Choice/probabilities/confidence, numeric reliability or null, usage, matrices, exact source/request hashes, images and the reversible table state. Download and independently verify every request, table roundtrip and witness reference, then save a comparative offline viewer, report and complete artifact in outputs and the existing Library page.

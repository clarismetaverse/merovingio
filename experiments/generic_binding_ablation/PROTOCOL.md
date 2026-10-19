# Historical Generic Space descriptions and scoring ablation

Parent: 021d2ed. Branch: codex/generic-binding-description-scoring. Earlier studies and main are preserved. Jev is pinned to jev-1.14.0. This pilot tests why the two historical Generic Space schemas missed 28 structural bindings in run 39216941401, without repeating the 100-question catalogue search.

## Fixed evidence and local reference

Use the exact four earlier workspaces: two triangle layouts and two anonymous-label/order repetitions. There are five candidate transformations, including no change. The only targeted schemas are GS_HIST_DOUBLE_TRIANGLE and GS_HIST_MEDIAL_POLYROLE. Each workspace has seven positive bindings and three negatives: double-triangle binds three vertex connectors, not the triangle-plus-quadrilateral connector or no-change; polyrole binds all four actual partitions, not no-change. Total 28 positive bindings previously below 0.75, plus 12 negatives. They are repeated instances of two geometric templates, not 28 independent geometries.

All original state fields, including the other ten library hypotheses and existing MS/GS, remain in the common workspace. Only the two target definitions vary in the state-description intervention. Source requests are reconstructed from stored model input and frozen PNG assets from the earlier artifact, with exact source-request and asset hashes checked before subsetting. The fixtures avoid operating-system font differences. No historical file or previous result is changed. Images contain no answer or schema labels.

The reference is explicitly the previous local structural gate, not theorem validity. The polyrole description operationalizes boundary roles and host-partition roles of one segment. This is a permissible local interpretation to test, not a claim that every historical use of polyrole has exactly this meaning. The experiment can expose a mismatch between an underspecified template and this checker; it cannot prove that the original wording had a unique intended interpretation.

## Crossed interventions

Four conditions, each on the same four workspaces:

| Condition | Schema description in state | Score criteria |
| --- | --- | --- |
| compact_generic | Exact previous abstract role/relation fields | Exact previous broad four-level rubric |
| explicit_generic | Same fields plus generic object variables, structural requirements and no-metric-premise scope | Same broad rubric |
| compact_concrete | Exact previous fields | Exact concrete PAIR_LEVELS / POLY_LEVELS used in the earlier bridge dimensions |
| explicit_concrete | Explicit definitions | Concrete criteria |

The question instructions remain byte-for-byte equal across conditions. The explicit definitions contain no candidate-specific assignment, score, gold label, new geometry or claim that a particular binding exists. Criterion changes do not change state or assets. All conditions share the same candidate aliases, schema aliases, assets and question ordering within a workspace. Call order is deterministically shuffled across all 16 calls.

For each of ten candidate-schema pairs, ask one native Score and one Choice: 20 questions per call, 16 calls, 320 total answers, comprising 160 Score and 160 Choice. This is fewer question evaluations than the previous 432, and no question addresses the other ten schemas. Shared-workspace repetition means token usage must still be measured.

Choice has identical instructions and the same four level texts, mapped to shuffled neutral labels, plus a none option for insufficient information. Labels are never quoted in instructions as desired answers. Only selection of the complete-binding level is a recognized binding. Partial support is distinct from a complete binding. Choice adds an uncertainty outlet, so this contrast is not solely a change in the internal primitive. The two concrete rubrics also provide a check on whether the supplied geometry can support a local complete-binding judgment.

## Separate arithmetic from interpretation

Primary Score screening keeps the earlier normalized threshold 0.75. Retain probabilities, confidence, native score, normalization and optional numeric reliability. Compute the unique modal level from the same Score distribution, and descriptive fixed thresholds 0.50, 0.65, 0.75 and 0.85 without additional calls. Do not tune a threshold on these fixtures or treat a high confidence as correctness.

Compare compact_generic in the small mixed batch with its original 100-question Score outputs before attributing changes to descriptions or rubrics. Report both positive recovery and false positives, none, per-schema score means, matched score changes and native Score-versus-Choice disagreements. A lower threshold that also accepts the partial triangle/quadrilateral negative is not an unqualified improvement.

Reading the contrasts: improvement from explicit versus compact state under a fixed rubric indicates sensitivity to description/operationalization; improvement from concrete versus generic criteria at fixed state indicates rubric sensitivity. Differences between threshold and modal projection on the same native distribution isolate post-processing. Choice comparison tests an alternate typed judgment protocol, not a theorem verifier or proof of which internal component caused an error. A batch-baseline shift or poor negative controls limits causal interpretation. No significance or broad generalization claim is predeclared for four workspaces.

## Execution and artifacts

Only GitHub Actions may issue live calls with TYPESAFE_API_KEY secret and TypeSafe-Danger-Zone-Images: true. No local API execution, raw server body, long-context header or automatic retry. Checkpoint after each call, stop repeated HTTP 400 validation, sanitize through an explicit typed allowlist, and upload artifacts even on failure. Offline mode has no scores or fabricated metrics.

Save results, usage, confidence, optional reliability, all condition matrices, threshold diagnostics, exact input and asset hashes, failures, frozen images and an offline comparison viewer. Download and independently audit artifacts, publish the verified report and retain them in the existing Library page. Native Score semantics follow [TypeSafe Score](https://docs.typesafe.ai/primitives/score); Choice follows [TypeSafe Choice](https://docs.typesafe.ai/primitives/choice). Multiple images do not demonstrate internal sequential reasoning; structured geometry is supplied evidence.

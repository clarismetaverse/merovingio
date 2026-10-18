# Verified Temporal Genealogy pilot

Live GitHub Actions run: https://github.com/clarismetaverse/merovingio/actions/runs/39172253094
Evaluated commit: f5be5ef. Base: e1277e3 (v1.0, includes v0.9). main unchanged.

24 successful Jev 1.14 calls; no request or schema failures. Build and four original offline tests passed in Actions. Six tests pass after adding explicit offline-null and sanitization checks. Subsequent viewer/report-only improvements do not alter stimuli or live requests.

| Condition | n | Result | Mean reported confidence |
| --- | ---: | --- | ---: |
| Final image only | 8 | none 8/8; origin accuracy undefined | 0.480 |
| Three chronological frames | 8 | origin correct 6/8; none 2/8 | 0.394 |
| Frames plus Mental and Generic Spaces | 8 | origin correct 8/8 | 0.535 |

Sequence errors were abstentions on two translation-origin trials; circle origin was recognized 4/4. Structured trials recognized both origins 4/4. These are small paired pilot observations across four transforms, not independent evidence of broad generalization or a significance claim. The final-only control is non-identifiable: no unique historical target and no interpretation of 50% binary choice as success.

Usage: 53,072 input tokens and 1,098 output tokens. Confidence and option probabilities are API reported. Reliability was not supplied as a numeric field and is preserved as null; no reliability estimate is invented. Empirical correctness and abstention are reported separately. No response rationale/free text, credentials or raw HTTP body is retained.

SAME_FINAL_STATE != SAME_GENEALOGY. Pixel identity was rechecked on all four final-image pairs from the downloaded artifact. Initial states match as well; intermediate construction evidence differs. Mental Space and Generic Space relations are curated structural input, so their benefit can include textual cue use. Multiple images do not establish internal sequential reasoning. Origin distinguishability is not geometric proof.

The report retains all source nodes, edges and hashes from the two historical workspaces. Structural role transitions are newly reconstructed, not claimed as recovered historical animation logs.

Files: results.json is the unchanged sanitized live report from Actions. viewer.html adds offline presentation of its matrices, image sequences and frame structures. run-metadata.json identifies the evaluated commit. Library holds this package and report. Re-run live only via workflow_dispatch with live=true; pushes perform offline checks and build.

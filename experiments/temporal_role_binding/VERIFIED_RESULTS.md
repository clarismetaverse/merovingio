# Temporal Role Binding verified results

Live run: https://github.com/clarismetaverse/merovingio/actions/runs/39174531307
Evaluated commit: 8c6e5e1bddf02857bbb0b21501b3915fdaf56bb3.
Branch: codex/temporal-role-order-binding. Parent: 2d6d74a. Both prior pilots and v0.9/v1.0 are preserved. Main remains 7ec0c2b8e7a4f0e0cac82a1265a53e3fb5a98475.

224/224 Jev 1.14 requests completed, no transport/schema failures. All 27 offline tests and the existing viewer build passed in GitHub Actions. All 224 request fingerprints reconstruct exactly from the downloaded audit and image files. All 48 opposite-history control pairs have identical requests. All 16 ordered-image opposite-history pairs have identical image multisets and initial/final PNGs, differing only in the order of the two activation frames. Observer role traces are consistent with the initial-support binding rule.

## Construct boundary

This study tests which support family was activated first in an authored support-binding session over pre-drawn geometry. It does not recover an actual construction from a blank workspace or prove the triangle. Both circle and vector scaffolds are always present. Accent strokes are explicit activation evidence. The first activation binds the initial-support role, the other adds a secondary support; these are protocol-defined roles. Geometry and source carrier identities are grounded in the historical workspaces, while the activation sessions are newly authored.

## Results

| Condition | Correct first-support order | None | Mean reported confidence |
| --- | --- | --- | --- |
| Images, earliest to latest | 27/32 (84.4%) | 5/32 | 0.422 |
| Same images, latest to earliest, direction explicit | 2/32 (6.3%) | 14/32 | 0.163 |
| Unordered image collection | Undefined | 28/32 | 0.295 |
| Single activation without temporal position | Undefined | 32/32 | 0.674 |
| Common final state only | Undefined | 32/32 | 0.507 |
| Ordered images plus structures | 29/32 (90.6%) | 3/32 | 0.397 |
| Ordered structures only, no images | 32/32 (100%) | 0/32 | 0.761 |

The chronological image condition correctly follows BOTH opposite histories in 11/16 matched pairs. Its five errors are vector-first abstentions; circle-first is 16/16. The image-plus-structures condition gets both histories right in 13/16 pairs. Structures-only gets both right in 16/16 pairs.

In the reverse presentation, 16/32 answers name the support that was activated LATER in real chronology (the first displayed activation); 14/32 abstain and two correctly identify the earlier support. No opposite-history pair is fully correct in reverse presentation. In the chronological-versus-reverse comparison, both are correct in two cases, only chronological is correct in 25, only reverse in zero, and neither in five. This is strong descriptive presentation-direction sensitivity in these stimuli. It is consistent with a first-displayed-event heuristic on some trials, but does not identify an internal algorithm. The reversed condition also places the common final state first and the scaffold last; the contribution of boundary reversal versus the direction annotation is not isolated.

The image-plus-structures advantage over images alone is small and mixed: 26 shared successes, three successes only with structures, one only without, and two joint failures. The textual structures alone are sufficient in every tested case, so success with supplied Mental/Generic Spaces is not evidence of autonomous visual role extraction. Reverse-ordered text-only structures were NOT tested, so the reversal deficit cannot be attributed specifically to vision rather than direction interpretation.

Unordered input has four unsupported named-order decisions (three circle-first, one vector-first), alongside 28 abstentions. Single-event and final-only inputs always elicit none in this run. These controls have no unique order target; order accuracy and per-trial correct remain null. Never treat 50% binary order guesses as success. The two histories have identical image content and differ only in supplied chronology when chronology is available.

## Interpretation and limits

Jev can use the ordinary presentation order to discriminate these matched support histories in many cases. It does not robustly recover that same ordering under an explicitly reversed presentation. The result establishes limited behavioral use of ordering information, not internal sequential reasoning, causal understanding, general genealogy reconstruction or geometric proof. Simple ordered-list comparison can solve the task. The initial-support role itself is supplied by the protocol, not autonomously induced.

Eight transforms and two repetitions of two templates are dependent observations, not 224 distinct geometric problems. No significance claim is made. This task and prompt differ from both prior pilots; percentages must not be pooled directly or treated as a longitudinal model improvement.

## Response handling and artifacts

554,592 input tokens; 11,860 output tokens. Confidence and option probabilities are API-reported. No numerical reliability field was supplied; it remains null. No local Jev calls, no automatic retries, and no raw server body or key retained. Actions used TYPESAFE_API_KEY and TypeSafe-Danger-Zone-Images: true. results.json is the unchanged sanitized Actions report, including model-visible input audit, image references, source nodes/edges/hashes and observer-only role transitions. run-metadata.json identifies the live commit; artifact-verification.json records integrity checks. Viewer runs offline.

The next discriminating control would separate direction interpretation from visual ordering: reverse the textual observations as well, and compare activation-order reversal with and without reversing the idle/final boundary frames. Those controls have not been executed here.

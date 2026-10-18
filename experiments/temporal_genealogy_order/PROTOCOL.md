# Temporal Genealogy order and snapshot ablation

This follow-up preserves the initial pilot and v0.9/v1.0 work. Parent: 2068472. Dedicated branch: codex/temporal-genealogy-order-ablation. Main is unchanged. Model: jev-1.14.0.

## Fixed plan before live evaluation

192 calls: six conditions x two construction origins x eight rigid transforms x two repetitions. Angles: 0, 37, 83, 151 degrees; reflection +1/-1. Repetitions change opaque option codes and option order; one cell's mapping is shared across conditions and histories. Trials are shuffled with seed 20261019; requests are independent, without conversational carryover. Three bounded concurrent HTTP workers in Actions; no automatic retries, including on failure.

Conditions: final_only, ordered, middle_only, shuffled, ordered_spaces, spaces_only. Each request has exactly one typed choice with two described origins and none. Text and options match across conditions, except for the deliberately supplied structures. No condition name, source file, correct code, hidden history ID, or original temporal index is transmitted. Images have no text, labels or PNG metadata. All final image pairs are identical bytes. This is a new matched run, not pooled with the original pilot.

The chronological sequence is [initial, diagnostic intermediate, final]. The middle-only condition uses exactly that intermediate PNG. Shuffled uses the same three PNGs in a guaranteed nonidentity permutation. The five nonidentity permutations are distributed cyclically across transform/repetition cells (four occurrences of the first, three of each other); both histories share a cell's permutation. Every transmitted asset is renamed view1/view2/view3 by PRESENTATION position. Reusing original frame0/frame1/frame2 IDs would reveal the ordering and is prohibited. Prompt wording makes no claim that supplied order certifies chronology; it is identical in all conditions.

Ordered_spaces includes the pilot's curated per-frame Mental Spaces, Generic Spaces and role transitions. Spaces_only supplies exactly the same structures without image assets. This isolates the sufficiency of explicit textual evidence; it does not test autonomous discovery of those structures.

## Targets and analysis

Final-only has no identifiable origin and no unique genealogy target. Correct is null, origin accuracy is null; summarize none rate and response distribution. Never interpret 50% forced choice as genealogy success. All other conditions have the actual construction-origin target because the diagnostic carrier evidence is supplied, even if presentation order is permuted. Shuffling does not erase circle or translation evidence.

Report condition confusion matrices including none/failure, accuracy with failures in the denominator, confidence, option probabilities, numeric reliability if returned, token usage, and per-trial inputs without duplicated base64. Compare matched case/repetition/history cells: ordered vs middle_only; ordered vs shuffled; ordered_spaces vs ordered; ordered_spaces vs spaces_only. Report repeat agreement under changed option labels, not as an independent reliability certificate. No significance claims: transformed and repeated two-template observations are dependent.

If middle-only and shuffled match ordered, the data support sufficient diagnostic snapshot evidence within these stimuli; they do not support a special chronology advantage. If structured-only matches image-plus-structures, textual observations may account for that condition's performance. Even an ordered advantage is behavioral evidence of presentation sensitivity, not proof of internal sequential reasoning. No outcome here is a geometric proof. SAME_FINAL_STATE != SAME_GENEALOGY remains the geometric control, not a claim about model architecture.

## Provenance and artifacts

Reuse the first pilot's deterministic renderer, geometry and curated structural observations unchanged. Results contain full nodes, edges and hashes from workspace_equilateral_same_state_different_genealogy_v0_4_1.json and workspace_two_circles_triangle_v0_4_1.json, never as model input. The animations are reconstructed interventions, not historical recordings.

Run offline: python -m unittest discover -s experiments/temporal_genealogy_order -v; python experiments/temporal_genealogy_order/benchmark_order.py --out output_temporal_order.

Live runs require GitHub Actions and the TYPESAFE_API_KEY repository secret. TypeSafe-Danger-Zone-Images: true is always sent. Transport checks the guard itself. Checkpoint sanitized JSON after each completed request; no raw response text, headers, credentials or response bodies are logged. Offline accuracy and none rates are null until attempted. Workflow uploads results and images even after failure. Viewer is fully offline and includes contrasts, all transformed image pairs, per-trial model input and sanitized responses.

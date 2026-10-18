# Temporal Role Binding with identical frame multisets

## Question and construct boundary

Follow-up to the two completed Temporal Genealogy pilots. Parent: 2d6d74a. Branch: codex/temporal-role-order-binding. Main, v0.9/v1.0, and both earlier experiments are preserved. Model: jev-1.14.0.

The first two pilots can be solved from circle-versus-vector contents of one diagnostic snapshot. This study instead presents BOTH support families in BOTH histories, using identical frame multisets. The target is the support family activated BEFORE the other and consequently occupying the session's initial-support role. This is staged support activation over pre-drawn geometric scaffolding, not recovery of an actual Euclidean construction from nothing. All points, circles, vector copies and the candidate triangle are already visible. The first highlighted activation binds an initial-support role; the second adds an independent corroborating support under an explicitly supplied protocol. These roles are experiment-defined; no proof is certified.

SAME_FINAL_STATE != SAME_GENEALOGY. History A: inactive scaffold, circle activation, vector activation, common final selection. History B: inactive scaffold, vector activation, circle activation, same final selection. Each event image is generated once by event type and rigid transform, with no history or temporal-position argument. All geometric primitives persist. Accent color marks active support; no text, option label, timestamp or correct answer is drawn. Initial and final images and the entire multiset are byte-identical across histories. Only ordering can distinguish the first-support role in the ordered evidence. An observer-only state machine records the carrier transition from available scaffold to initial support, then the alternative carrier to secondary support; it never overwrites the initial binding. The shared final state here means visible geometric state, not equality of the hidden role history.

## Fixed plan before live evaluation

224 independent API requests: seven conditions x eight rigid transforms x two role histories x two option-label repetitions. Transforms: angles 0, 37, 83 and 151 degrees, reflected and unreflected. Cases/repetitions use shared random option mappings across conditions and histories; trial order shuffled with seed 20261020. Three bounded concurrent HTTP workers in Actions, no automatic retries. Repeated/transformed templates are dependent scientific observations despite independent API contexts.

| Condition | Evidence | Identifiable first support |
| --- | --- | --- |
| ordered_images | Four frames, explicitly earliest to latest | Yes |
| reverse_images | Same frames in reverse, explicitly latest to earliest | Yes, requires respecting direction |
| unordered_images | Same multiset in a cell-shared random order, explicitly no temporal meaning | No |
| single_event | One activation chosen independently of history, no temporal position | No |
| final_only | Common final selection | No |
| ordered_spaces | Ordered images plus corresponding structural observations | Yes |
| spaces_only | Same ordered structural observations, no images | Yes |

Every request has one typed choice question with two described relative-order alternatives and none. The task and alternatives are identical across conditions; the declared ordering convention and supplied evidence are intentional experimental inputs. Neutral view1/view2/etc IDs indicate presentation position only. No original event names, source filenames, original temporal indices, history labels or answer keys enter image metadata or asset IDs. The structured records describe active carriers, Mental Spaces and Generic Space relations; the records themselves carry no temporal ranks or initial-support answer. Their list order supplies the temporal evidence deliberately.

For unordered_images the permutation is generated from the canonical event library, independent of the hidden history. For single_event the chosen family is balanced by repetition/cell, independent of history. Thus these controls, and final_only, have exactly identical model requests for the opposite-history pair. They cannot identify a unique initial-support role. Permuting frames while continuing to score a hidden historical order would be invalid; this protocol instead removes the unique target explicitly. Reverse_images retains the true order via an explicit shared direction annotation, so a first-displayed-event heuristic gives the wrong relation there.

## Analysis

For identifiable conditions: first-support order accuracy, confusion matrices, failures in denominator, response confidence and probabilities, token usage and any numerical reliability returned. For the three non-identifiable controls: order accuracy and per-trial correct are null; report none rate and non-identifiable response distribution. A 50% forced-choice result is not success. Failures stay visible, no outcome is invented for offline/unattempted requests.

Pair opposite histories at fixed case/repetition. Report both-correct history pairs separately from merely opposite named choices: choosing opposite but reversed answers is sensitivity without correct interpretation. Compare chronological versus reverse-chronological views on the same cases, and image-plus-structures versus image-only and structures-only. Do not infer statistical significance from transformed/repeated two-template examples. Successful behavior demonstrates use of supplied ordering information at most; simple list comparison suffices. It does not establish internal sequential reasoning, autonomous induction of roles, causal reasoning, geometric proof, or general genealogy recovery.

The geometry and carrier interpretation are grounded in the two historical workspaces used by the prior pilots. Full node/role/edge records and source hashes remain observer-only in results.json. Temporal activation sessions are newly authored interventions; no claim is made that these are historical animation logs.

## Execution and artifacts

Offline: python -m unittest discover -s experiments/temporal_role_binding -v; python experiments/temporal_role_binding/benchmark_binding.py --out output_temporal_binding.

Live: only through GitHub Actions, using TYPESAFE_API_KEY secret and TypeSafe-Danger-Zone-Images: true. Both main() and the shared transport enforce the Actions/secret guard. A [jev-live] commit marker starts the initial authorized branch run; later ordinary pushes are offline. workflow_dispatch live=true is also supported where available. Source commit and run ID are recorded. JSON is checkpointed after every completed call; sanitized numerical/categorical response fields only, no raw body or key. Upload on failure. Fully offline viewer includes both chronological histories, matrices, paired checks and reconstructable model inputs.

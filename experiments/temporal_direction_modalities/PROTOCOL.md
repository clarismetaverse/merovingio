# Temporal direction across textual and visual observations

## Purpose and fixed design

Follow-up explicitly requested to test reversed textual structures after the v3 image reversal deficit. Parent: 922e67e. Dedicated branch: codex/temporal-direction-modalities. All previous pilots and v0.9/v1.0 remain preserved; main unchanged. Model: jev-1.14.0.

192 API calls in a complete matched 3 x 2 design: images, text, combined; forward and reverse presentation. Each of six conditions has 32 calls: two first-support histories x eight rigid transforms x two option remappings. New trial-order seed 20261021, existing option seed base 20261020. Same cell's option mapping is shared across directions, modalities and histories. Three bounded concurrent HTTP workers, no automatic retries, independent API contexts.

Every request inherits the exact v3 task, typed choice question, descriptions, image renderer and structural records. No stronger wording, explicit timestamp, original event index or answer key is added. Four existing conditions (images forward/reverse, text forward, combined forward) reproduce v3 payloads exactly for the same case/repetition/history. They are rerun concurrently with the two new reversed textual conditions; outcomes are not pooled across runs.

| Condition | Images | Structural observations | Direction declaration |
| --- | --- | --- | --- |
| images_forward | Original event order | None | earliest to latest |
| images_reverse | Exact reverse | None | latest to earliest |
| text_forward | No assets | Original record order | earliest to latest |
| text_reverse | No assets | Exact reverse of SAME records | latest to earliest |
| combined_forward | Original event order | Original record order | earliest to latest |
| combined_reverse | Exact reverse | Exact reverse of SAME records | latest to earliest |

The combined and text-only conditions have identical textual states after removing images and emptying the views list. Combined and image-only differ solely by supplied structural observations. Image asset IDs are neutral presentation positions; textual records have no temporal-rank or initial-support answer field. Chronology reversal changes list position and direction declaration, not the target: which support was activated first in the underlying session. This must require reading the last presented activation in reverse conditions.

## Stimuli, gold and construct boundary

Use v3's two authored sessions over a pre-drawn scaffold. Both contain the exact same four event frames and the exact same structural-record multiset: idle, one circle-support activation, one vector-support activation, common final triangle selection. Only the middle-event chronological order distinguishes histories. All final geometry is identical. SAME_FINAL_STATE != SAME_GENEALOGY refers to visible geometric state. The initial-support role and subsequent secondary-support transition are protocol-defined and observer-traced; no proof or construction from blank is performed.

All six present sufficient ordered evidence and therefore have unique first-support gold labels. None remains available as a typed choice and counts as an abstention error here; failures stay in the denominator. Previous non-identifiable controls remain preserved in v3 and are not rerun in this focused study. No 50% success claim is made for those controls.

## Analysis and interpretation boundary

Report condition accuracy, confusion matrices, none, opposite-order choices, transport/schema failures, confidence, probabilities, numerical reliability if supplied and token usage. Pair forward/reverse within each modality and compare modalities within reverse presentation. Also require both opposite histories correct in matched cell pairs rather than just aggregate accuracy. Preserve reconstructable request hashes and source commit/run identity.

If textual reversal remains strong while images fail, the deficit is associated with visual/presentation integration under this encoding. It would not establish a specific architectural cause or prove imagery is inherently incapable of reversal. Text explicitly names relations and candidate/selected roles; it is curated semantic evidence, not information extracted by Jev from pixels. If text reversal also fails relative to text forward, the observed limitation spans modalities and is consistent with a broader problem interpreting the declared direction in this task. Either case is behavioral evidence, not internal process identification.

Whole-list reversal also reverses the idle/final boundary records and frames. Reversing only activation order versus full boundaries is NOT isolated here. Simple list comparison suffices. Transformations of two templates and repeated option remappings are dependent observations, not independent geometry problems; text-only transforms are pairing metadata and not added textual geometric variation. No significance or general reasoning claim. No internal sequential reasoning, causal reasoning, autonomous role induction or geometric proof is established.

## Execution

Offline: python -m unittest discover -s experiments/temporal_direction_modalities -v; python experiments/temporal_direction_modalities/benchmark_direction.py --out output_temporal_direction.

Only Actions may call Jev, using TYPESAFE_API_KEY repository secret and TypeSafe-Danger-Zone-Images: true. Main and shared transport both guard this. Initial [jev-live] push is authorized by the user request; ordinary later pushes only test/build/generate offline. workflow_dispatch live=true is supported where available. JSON checkpointed after each call; upload even on failure. Only sanitized typed/numeric fields survive, no credentials/raw body. Source nodes/edges/hashes and role traces remain observer-only. Offline viewer compares the modality-by-direction matrix, paired outcomes, exact input records and sample image/text sequences.

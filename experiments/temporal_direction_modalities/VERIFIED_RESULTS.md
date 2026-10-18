# Reversed textual structures and modality comparison verified results

Live run: https://github.com/clarismetaverse/merovingio/actions/runs/39175172222
Evaluated commit: 0d8e99092c322df3188b245bc523f60f27a096c1.
Branch: codex/temporal-direction-modalities; parent 922e67e. Main and all earlier pilots/v0.9/v1.0 are preserved.

192/192 Jev 1.14 requests completed without transport/schema failures. All 39 offline tests and the existing viewer build passed in Actions. All 192 request fingerprints reconstruct exactly. The 128 overlapping requests match the v3 artifact byte-for-byte at the request-fingerprint level. All 32 reversed text pairs and all 64 image/text alignments were verified. No stronger temporal wording or explicit time indices were introduced.

## Matched modality-by-direction results

| Evidence | Earliest to latest | Latest to earliest, explicitly declared |
| --- | --- | --- |
| Images only | 29/32 (90.625%) | 4/32 (12.5%) |
| Textual structures only | 32/32 (100%) | 32/32 (100%) |
| Images plus identical textual structures | 29/32 (90.625%) | 7/32 (21.875%) |

Forward and reverse conditions have the same underlying first-support target. Text reverse is exactly the reverse of the same four structural records, with no images or original temporal indices. Combined reverse has both the images and records reversed together. The question, criteria, task and direction phrases are inherited unchanged from v3. Thus the difference cannot be credited to a strengthened text-only instruction in this run.

## What the comparison supports

Within these authored support-binding sessions, Jev handles the declared temporal reversal correctly when the evidence is entirely textual: both opposite histories are correct in all 16 matched pairs, in both directions. It does not fail on the phrase latest to earliest in every modality. A modality-independent inability to interpret that direction is therefore not supported by this sample.

The deficit appears in the conditions containing images. Images reverse has four correct, 15 abstentions and 13 opposite-order decisions. Combined reverse has seven correct, 21 abstentions and four opposite-order decisions. Supplying the correct reversed text alongside images does not restore the text-only performance. Compared with reverse images, the combination helps four matched cases, harms one, and leaves 24 jointly incorrect; three are jointly correct. Compared with reverse text, adding images loses correctness in 25 matched cases and gains none.

This is evidence of a modality/presentation-integration limitation under this exact input encoding. It is not a diagnosis of model architecture, a proof that visual reasoning is absent, or a general claim that images impair Jev. Text explicitly names carriers, relations and boundary roles; it is curated semantic evidence rather than autonomously extracted geometry. Adding images also changes context size and invokes a multimodal input path. Request traces verify what was submitted, not server-internal image ordering or processing. These possible contributors are not isolated here.

The image-containing reverse conditions correctly follow BOTH opposite histories in zero of 16 pairs, despite some individual correct answers. Forward images and combined have 13/16 fully correct pairs. Text has 16/16 in both directions. This avoids treating a one-history preference as reliable genealogy discrimination.

## Detailed counts and confidence

| Condition | Correct | None | Opposite order | Failures | Mean reported confidence |
| --- | --- | --- | --- | --- | --- |
| images_forward | 29 | 3 | 0 | 0 | 0.431 |
| images_reverse | 4 | 15 | 13 | 0 | 0.175 |
| text_forward | 32 | 0 | 0 | 0 | 0.776 |
| text_reverse | 32 | 0 | 0 | 0 | 0.545 |
| combined_forward | 29 | 3 | 0 | 0 | 0.407 |
| combined_reverse | 7 | 21 | 4 | 0 | 0.183 |

Text-only confidence falls under reversal although choices remain correct. These are API-reported confidence values, not calibration or reliability certificates. Numerical reliability was not supplied and remains null. Usage: 503,584 input tokens and 10,500 output tokens.

## Scope and integrity

All six conditions have uniquely identifiable order targets, so abstentions count against order accuracy. Earlier final-only/unordered/isolated-event controls remain preserved and unscored for unique-history accuracy; they were not rerun here. No 50% forced-choice result is treated as success in a non-identifiable control.

This is an authored sequence over pre-drawn scaffold with an explicitly supplied first-support binding rule, not construction from blank, autonomous role induction or geometric proof. Whole-list reversal also reverses idle/final boundary observations. Text-only transformed cases are pairing metadata, not added geometric variation. Transforms and repeated labels of two templates are dependent observations; no significance claim or inference of internal sequential reasoning is made. Separate contexts and matched requests do not make the model deterministic: image counts differ slightly from v3 despite identical overlapping requests. Runs are documented separately rather than pooled.

results.json remains unchanged from the Actions artifact, with typed/numeric sanitized responses, usage, per-condition matrices, input audit, source records/hashes and observer role traces. run-metadata.json and artifact-verification.json identify execution and integrity. Live calls only used GitHub Actions with TYPESAFE_API_KEY secret and TypeSafe-Danger-Zone-Images: true; no key or raw server body is retained. Viewer is offline.

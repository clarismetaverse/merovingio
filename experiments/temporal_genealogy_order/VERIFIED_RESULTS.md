# Temporal Genealogy order ablation verified results

Live run: https://github.com/clarismetaverse/merovingio/actions/runs/39173673410
Evaluated commit: 13e46dc26c5054eb13423579e40bc2d3e0bebb23.
Branch: codex/temporal-genealogy-order-ablation. Base: 2068472; first pilot and all ancestral v0.9/v1.0 work preserved. Main remains at 7ec0c2b8e7a4f0e0cac82a1265a53e3fb5a98475.

192/192 requests completed; zero transport or schema failures. Both offline suites (16 tests) and the existing viewer build passed in Actions. The downloaded artifact reconstructs all 192 request fingerprints exactly. All eight transformed circle/vector final-image pairs are identical PNG bytes. No local live calls were made; Actions used the repository secret and the required image header.

| Condition | Correct origin | None | Mean reported confidence |
| --- | --- | --- | --- |
| Final image only | Undefined | 18/32 | 0.214 |
| Ordered three-frame sequence | 21/32 (65.6%) | 11/32 | 0.360 |
| Middle frame only | 23/32 (71.9%) | 1/32 | 0.515 |
| Same frames shuffled | 23/32 (71.9%) | 9/32 | 0.391 |
| Ordered frames plus structures | 31/32 (96.9%) | 0/32 | 0.476 |
| Structures only, no images | 32/32 (100%) | 0/32 | 0.604 |

## Interpretation

The chronological sequence shows no descriptive advantage over the diagnostic intermediate image or over a nonchronological ordering. In matched cells, ordered vs middle-only and ordered vs shuffled each have 20 successes in common, one success unique to ordered, three unique to the other condition, and eight joint failures. This does not support a special benefit of chronology in these stimuli. The middle frame explicitly exposes the origin-specific construction carriers, so this task may be solved from static evidence.

The textual structural observations alone are sufficient in all 32 tested cells. Adding images yields 31/32, with no paired success unique to the image-plus-structures condition. The high performance with supplied Mental and Generic Spaces cannot be credited to autonomous visual extraction or temporal reconstruction. This does not establish that images have no value in other tasks.

Circle-origin cases are 16/16 in every identifiable condition. The limitation is the vector-origin construction: ordered 5/16, middle-only 7/16, shuffled 7/16, ordered plus structures 15/16, structures-only 16/16. Ordered and shuffled vector errors are abstentions. Middle-only vector errors include eight circle-origin choices and one abstention, so equal aggregate accuracy masks different error types.

Final-only has no unique history target. Jev abstained in 18/32 calls and chose circle origin in 14/32; those 14 choices are unsupported by the identical final geometry and are not counted as correct or incorrect origin classification. The first pilot's 8/8 abstention did not establish robust abstention behavior. This new run uses neutral presentation IDs and revised common prompt wording; its rates must not be pooled directly with the first pilot.

These are two construction templates under eight transformations and two repetitions, not 192 independent geometric problems. No statistical significance or general reasoning claim is made. Repetitions change option codes/order; shuffled repetitions also change the permutation, so repeat agreement mixes these sensitivities and is not a pure reliability measure. Multiple-image input does not establish internal sequential reasoning. Distinguishability is not geometric proof.

## Usage and response handling

359,552 input tokens; 10,518 output tokens. Reported confidence and option probabilities are preserved. Numeric reliability was not supplied and remains null. Sanitization retains typed decisions and numerical fields, excludes free-form response bodies, and never stores the API key. results.json is unchanged from the Actions artifact. run-metadata.json and artifact-verification.json record execution and local integrity checks.

## Next scientific implication

A stronger temporal task would require distinguishing histories whose individual snapshots share the same objects, with only operation order, dependencies or role transitions carrying the answer. The current study identifies diagnostic snapshot and textual sufficiency; it does not yet test that stronger form.

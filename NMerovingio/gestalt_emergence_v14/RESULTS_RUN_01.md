# Panoptikon v1.4 — Three representations of Mental Space emergence

**GitHub Actions live run:** https://github.com/clarismetaverse/merovingio/actions/runs/39023463352  
**Branch:** `experiment/panoptikon-emergence-v1.4`  
**Status:** passed unit tests and 72 authenticated calls to Jev 1.14.0. The original `main` branch is unchanged.

## Research question

Across a succession of geometric constructions, can Jev recognize when the *upper angular pair* and *lower right-angle pair* are cognitively registered, when an abstract left/right alignment becomes available, and when both pairs share one certified physical carrier? Compare three modalities:

- **Annotated image:** single figure at each stage, upper/lower registrations marked using different visual cues.
- **Plain image:** the same physical figure, with no conceptual annotations.
- **Symbolic-only:** only points, carrier endpoints, incidences, current events and their order, no image.

**Critical factor held constant:** All three modalities receive the same short typed history of completed construction events. Thus 'plain' means **visually unannotated**, NOT 'no linguistic context whatsoever'. In isosceles triangles the physical diagram is identical at stage 1 and stage 2 even though the registration history changes.

## Protocol

Four underlying shapes (two isosceles, two scalene) × two histories (upper-first, lower-first) × three stages (given state, first registration, second registration) × three modes = **72 independent API requests**. Each request contained five Noul yes/no judgments and an exploratory choice for future salience. Therefore the scored total is **360 role judgments**. The choice has no objectively unique correct answer and is excluded from the scored accuracy.

No cross-level metrical equality is assumed. Geometric presence, concept registration and certified proposition are separate epistemic statuses. The two angle pairs can each have equal measures *within* their pair without any apex half-angle equalling a base right angle.

## Results

| Mode | Correct / scored | Accuracy | Registered upper | Registered lower | Abstract alignment available | Identical support | Cross-metric equality unproven |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Annotated | **116/120** | **96.7%** | 24/24 | 24/24 | 24/24 | **20/24** | 24/24 |
| Plain | **116/120** | **96.7%** | 24/24 | 24/24 | 24/24 | **20/24** | 24/24 |
| Symbolic only | **112/120** | **93.3%** | 24/24 | **20/24** | 24/24 | **20/24** | 24/24 |

All 12 combinations per mode at stages 0 and 1 were correct (40/40 role judgments at each stage). All mistakes occurred at stage 2:

- Both image conditions each scored 36/40 at stage 2, **all four mistakes** from wrongly denying shared carrier in both isosceles geometries and both histories. Jev returned `p_true` approximately **0.09–0.20** where `true` was independently certified.
- Symbolic mode scored 32/40 at stage 2: the same four isosceles shared-carrier mistakes, plus four incorrect lower-angle-space registrations in `lower_first` histories (probability around 0.40–0.47).
- Scalene negative controls for identical support and the four other role categories were handled reliably.

**Image ablation:** The annotated and plain modalities have identical aggregate accuracy, but are not identical outputs. Absolute differences in per-question probabilities ranged from about 0.004 to 0.040 on average, and three of 24 exploratory choice labels changed. This is *not* evidence of a significant benefit from annotation.

**Usage returned by Jev:** annotated 520,508 input / 3,288 output tokens; plain 520,508 input / 3,288 output; symbolic 28,404 input / 3,290 output. **Overall 1,069,420 input and 9,866 output tokens.** These are reported API usage values, not a confirmed billing amount.

## Main finding and caveats

Registering two Mental Spaces and accepting an abstract correspondence **did not reliably make Jev identify their physical support as identical** in the isosceles case. This may be caused by missing causal links from the completed event to its actual material carrier: the common event history identifies the type of cognitive partition, but does not explicitly associate both operators with physical segment `CD`. Images alone, even with registration markers, were not enough for Jev here.

This does **not** establish that images or annotations are useless. The registration questions are nearly solved directly by the common typed event history, so they are not a fair test of unaided visual discovery. The upper annotation currently highlights the apex rather than two distinctly shaded sectors, and there are only four related shapes. Candidate Mental Spaces are posed as pre-authored Noul questions, not generated autonomously by Jev.

## Next falsifiable experiment

Abandon global accuracy (near ceiling) and target the **missing provenance edge**. Hold image, question text, event order and final geometry fixed. Add just an explicit `event -> produces material carrier` relation to the shared event graph (e.g., both independent isosceles operations reference the exact same canonical `CD`, whereas a scalene control references `CE` vs `CH`). Compare the shared-support Noul probability in matched with/without-provenance pairs. Ensure `joint_abstract` remains available with distinct carriers, and that no certified cross-level angle equality is introduced. This distinguishes a failure of **object-identity binding** from failure to identify or register Mental Spaces.

## Reproduction

- `NMerovingio/gestalt_emergence_v14/emergence_v14.py`
- `NMerovingio/gestalt_emergence_v14/tests/test_emergence_v14.py`
- `.github/workflows/panoptikon-emergence-v14.yml`
- GitHub artifact `panoptikon-emergence-v14`, containing `emergence_v14_results.json` and experiment images.

No keys or raw request bodies are included in outputs. The `TYPESAFE_API_KEY` secret is read only by the CI API step.
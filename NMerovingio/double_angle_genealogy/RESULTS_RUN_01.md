# Panoptikon v1.1 — Double angular-pair genealogies: first live results

**GitHub Actions run:** https://github.com/clarismetaverse/merovingio/actions/runs/39019025609  
**Branch:** `experiment/panoptikon-double-angle-genealogy-v1.1`  
**Jev version:** requested `jev-1.14.0`; 24 successful authenticated calls.  
**Artifacts:** `panoptikon-double-angle-genealogy-v11`; also archived in ChatGPT Library at `/Merovingio/Results/panoptikon-double-angle-v11-results.zip`.

## The research distinction

In an isosceles triangle ABC, an apex bisector meets AB at D and also gives a perpendicular from C to AB. Thus two pairs coexist on the **same physical CD**:

- Upper apex sectors ACD and DCB: equal *within their pair*.
- Lower right angles ADC and CDB: 90° *within their pair*.

An upper half-angle is **not** metrically equal to a lower right angle. An upper/lower correspondence is therefore **a left/right role alignment across two Mental Spaces**, not an assertion of corresponding angle measures.

Two genealogies were encoded over identical final geometries: `apex_first` (upper angle partition becomes salient first) and `base_first` (lower right-angle partition becomes salient first). Each genealogy was shown with chronological event order; some iso symbolic trials also reversed only the *presentation list* while retaining the original numerical step indices.

Two isosceles figures with different apex heights were tested, plus two scalene controls for which the angle bisector and altitude are **different physical carriers**. In scalene controls an abstract binary-partition analogy remains possible, but shared-carrier alignment is not certified.

## Experimental outcomes

- **24/24** correct refusals to infer equality of measure between upper half-angles and lower 90° angles. This is essential epistemically: structural analogy is not metrical identity.
- **22/24** correct yes/no judgments of whether both pairs share the same geometric carrier: image mode 10/10 and symbolic mode 12/14. The two symbolic errors (p=0.43 and p=0.49) were both from presentations with event lists reversed.
- Scalene controls: all 8 calls assigned p(shared physical carrier) between **0.05 and 0.12**. This negative control helps distinguish an actually shared divider from an abstract analogy of binary partitions.
- In isosceles scenes, the *probability assigned to exploring their joint correspondence next* changed with the representation supplied:

| Isosceles condition | Cases | Mean P(joint alignment as next focus) | Mean P(shared-carrier factual judgment) |
| --- | ---: | ---: | ---: |
| Final state only, image | 2 | .360 | .905 |
| Chronological history, image | 4 | **.500** | .755 |
| Final state only, symbolic | 2 | .360 | .965 |
| Chronological history, symbolic | 4 | .400 | .672 |
| Symbolic history events in reverse display order | 4 | .375 | .510 |

The difference between image+history and image only (**+0.140**) is descriptive, not a causal effect estimate. Important confound: the two no-history calls share the same final shapes, and none of these is a large independent sample.

Historical source direction did NOT show a strong separable effect: chronological-history mean P(joint) across image/symbolic was **.463 for apex-first** versus **.438 for base-first**. This is too small a difference to warrant a firm history-direction conclusion.

**Presentation-order confound:** reversing how historical events appeared in the state (even when numerical step indices remained correct) lowered P(shared carrier) and shifted the focus distribution. Some of the apparent genealogical effect may therefore be prompt ordering or recency effects rather than cognitive reconstruction of construction provenance.

In the *scalene image* controls, Jev sometimes prioritized `joint` as a focus even while correctly assigning near-zero probability to the stronger same-carrier claim. This exposes a limitation of the choice prompt: it does not sharply distinguish an abstract correspondence from a literal shared support. Later tests need stricter, role-specific choice descriptions or constrained options.

**Reported token usage:** 36,816 input tokens and 1,872 output tokens, summed across all 24 API responses.

## What we learned / next test

The engine successfully separates four different items:

1. Exact final geometric state, checked deterministically.
2. First emergence of each Mental Space and construction-operator provenance.
3. Generic-space candidate (upper/lower correspondence) with an **epistemic flag**.
4. Independent formal check: shared carrier in an isosceles case, nonshared in scalene.

A scientifically stronger follow-up should compare the same final configuration with histories given as **anonymous operator identifiers and dependency graphs**, not evocative English descriptions. Shuffle presentation order separately from causal order, use multiple repetitions and more held-out geometries, then investigate whether two corresponding Mental Spaces are *generated* or merely ranked.

This test does not prove cognition depends on genealogy, that Jev discovers new mathematical facts, or that proposed Generic Spaces imply Euclidean congruence. It is a reproducible, goal-scoped exploration of the user's hypothesis.

## Reproduction

`NMerovingio/double_angle_genealogy/core.py`  
`NMerovingio/double_angle_genealogy/jev_double_angle.py`  
`NMerovingio/double_angle_genealogy/tests/test_double_angles.py`  
`.github/workflows/panoptikon-double-angle-v11.yml`

# Panoptikon v1.4 — Mental Space emergence in three representations

## The requested comparison

Test **annotated image**, **unannotated image**, and **purely symbolic state** on exactly the same construction snapshots.

The represented objects are the two pairs of angular sectors:
- an apex-angle pair created by the construction of a bisector;
- a base-right-angle pair created by a perpendicular from apex to base.

Isosceles controls: one physical divider serves both roles, including when only one *interpretation* has so far been registered. Scalene controls: bisector and perpendicular are materially distinct segments. Upper half-angles are NOT claimed equal in measure to lower right angles.

## What is held constant

- Four geometries: two isosceles and two scalene.
- Two genealogies: upper pair registered first, or base pair first.
- Three stages: initial, first registration, second registration.
- Three representations: annotated PNG, unannotated PNG, and no-image symbolic graph.
- All 72 trials ask **the same five Noul questions and one optional exploratory Choice question**.
- **Exactly the same event history fields** are supplied in the state for each of the three modalities. This is necessary because in isosceles cases the bare pixels at stage 1 and stage 2 are identical. The non-annotated picture remains visually unannotated, but its event history is still provided as contextual structured data.

Annotated images mark activated apex/base interpretations with two distinct visual cues. Unannotated images show only points and physical segments. Symbolic condition has no image and contains only primitive points, incidence and active carriers, plus the same completed event record. None contains a visual side-by-side candidate answer array.

## Three separate epistemic distinctions

1. **Materially possible**: a geometric relationship holds in the final shape, even if it has not been actively noticed.
2. **Cognitively registered**: an event has introduced or activated a Mental Space in the construction history.
3. **Certified**: a deterministic validator has checked the needed geometric facts.

On an isosceles, the first physical divider might already *also* be a perpendicular/bisector as a mathematical consequence, even though the model registers only one of the two Mental Spaces at that moment. These are not contradictory claims.

### Questions

- Has the upper angular partition been registered?
- Has the base-right-angle partition been registered?
- Have both been registered, allowing an **abstract two-pair Generic Space candidate**?
- Have both been registered **and** do they share the identical physical carrier?
- Has an equality of angular measure between the upper half-angle and a lower right angle been *certified*? Correct answer: never.
- An extra Choice probes which reading to explore next; there is **no objectively unique correct choice**, so Choice is reported as a distribution, not accuracy.

Truth labels are computed offline, NOT inserted in Jev's request.

## What success could mean

A good three-modality result would show that explicit graphical or symbolic structure helps Jev track **when** a proposed Generic Space becomes available, not just whether the final material figure admits an interpretation.

But there is a **fundamental confound to acknowledge**: the common event graph includes typed operator names identifying which cognitive roles were registered. Therefore this measures *tracking/recognition of authored registrations*, NOT autonomous detection of new Mental Spaces or discovery of a new proof. Further experiments must remove this support or add unseen candidate spaces and randomized operator aliases.

## Reproduction

GitHub Actions: `.github/workflows/panoptikon-emergence-v14.yml` on `experiment/panoptikon-emergence-v1.4`. It reads the existing repository secret `TYPESAFE_API_KEY` only in the live evaluation step.

Output: `output/emergence_v14_results.json`, trial images, per-question accuracy by modality and returned `usage` token counters. API keys and full request bodies are never recorded. No modifications to `main`.

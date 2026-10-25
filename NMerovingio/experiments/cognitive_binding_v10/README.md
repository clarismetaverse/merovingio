# Merovingio v10 — Cognitive Binding Consequence Memory

## Why v10 changes direction

The purpose of v10 is **not** to derive or store a formal geometric proof. We want a trace of the *cognitive events* occurring when a prospective double-scope blend becomes physically instantiated and congruence frame roles become available.

We separate three representational statuses:

- **GIVEN / OBSERVED / CONSTRUCTED**: information present from the initial assumption or perceptually available after the bisector construction.
- **BOUND IN A COGNITIVE FRAME**: an available relation has been aligned with an abstract LAL/LLL slot. The relation's cognitive significance changes even if the geometry does not.
- **COGNITIVELY PROJECTED (NOT PROVEN)**: a completed LAL frame introduces a new candidate relationship between the base-side portions as a *consequence of the binding*. That relationship can prime other interpretations, such as MEDIAN and a subsequent LLL rereading. This does not silently turn an analogical expectation into an independently verified theorem.

The aim is to capture a cognitive cycle from the constructed bisector back to the geometrically interpretable figure.

## W0 → W1 → Cognitive consequences

1. Activate canonical TRIANGLE and DIVISION categories, with a potential prospective two-part frame before D/CD exist.
2. Observe the initial external-side relation (equal only in the equilaterals or the appropriate isosceles).
3. Construct the bisector, find new material faces, and bind the prospective abstract roles to their new geometric instances.
4. Register the role bindings for the **common carrier segment** and the **two equal included apex angles**. Seed controls can reverse the inspection order, but not the meaning of the data.
5. When the LAL mental frame has all three verified source roles, append a **COMPLETE_FRAME** event with its parent role-binding IDs.
6. Add a **PROJECT_RELATION** cognitive event about the two opposite base segments, linked causally to the completed frame. Its status is always cognitive_inference_not_proven, not theorem or independent geometry.
7. This new belief state allows **ACTIVATE_ALTERNATIVE_FRAME(MEDIAN)** and **REBASE_FRAME(LLL)**, both referencing the projected relation. The latter must not use the projected base equality as an independent original LLL premise to justify its own existence.
8. Keep an explicit cognitive event DAG and memory of causal ancestry; no SAS proof engine or derived mathematical certificate is part of the v10 experiment.

The cognitively projected relation is not a conclusion directly from a bisector. In a scalene triangle, the outer legs are not equal, so no complete LAL mental frame appears, and **no such cognitive projection is permitted**. Masking the included-angle witness likewise blocks the projection.

## Experimental cases

Geometries: equilateral (all three goal vertices), non-equilateral isosceles (C apex), scalene (C apex).

Conditions: normal; LLL initially favored; without prospection; included-angle witness masked; and, in compatible geometries only, a counterfactual with an explicit additional base equality.

The counterfactual assumption has its own **RECALL_EXTRA_GIVEN** cognitive event and is never disguised as a projection.

48 seeds, with randomized order of observing the common side and included-angle relation. Every event carries frame, status, timestamp index, parents, and material or prospective role information.

## Evaluation

- Does a fully bound LAL frame create a new cognitive relation **only after** all role bindings exist?
- Is the relation grounded in the exact parent frame and corresponding side objects, rather than pre-written AD/DB?
- Can the projected relation trigger new interpretations (MEDIAN, LLL) with traceable causal paths?
- Do negative controls prevent unlicensed cognitive projections?
- Can no cognitive projection accidentally become a formally certified equality?

These are software-engineering invariants of a hand-designed model, not empirical psychological laws.

## Run

    python -m unittest discover -s NMerovingio/experiments/cognitive_binding_v10 -p 'test_*.py' -v
    python NMerovingio/experiments/cognitive_binding_v10/cognitive_memory.py --seeds 48
    python NMerovingio/experiments/cognitive_binding_v10/viewer.py

Artifacts in results/: traces.json, aggregates.json, REPORT.md and offline viewer.html.

# NMerovingio

A deliberately tiny research reasoner for Euclid Book I, restricted to the **isosceles workspace** and propositions **I.5, I.6, I.7, I.18, I.19**.

The goal is not theorem proving by broad search. The goal is to test whether a reasoner can **generate useful analogies and disanalogies from a single stabilized Gestalt**, especially the counterfactual pattern made explicit by I.6.

## Core hypothesis

Use the isosceles triangle as a base Gestalt:

- equal sides <-> equal base angles
- a counterfactual is created by minimally breaking one correspondence
- preserved correspondences become epistemic contacts
- the break is run through the workspace until it propagates, closes coherently, or produces an incompatible Gestalt
- a stabilized counterfactual may become a new base case for later reasoning

The first target is not to reproduce Euclid's proofs verbatim. It is to reconstruct a **visual-inferential grammar** capable of rediscovering relations among I.5, I.6, I.7, I.18 and I.19.

## Allowed primitives

Construction / visual operators:

- `OVERLAY`
- `BREAK_SIDE_EQUALITY`
- `BREAK_ANGLE_EQUALITY`
- `PRESERVE_CONTACT`
- `EXTEND_COLLINEAR`
- `PART_WHOLE`
- `JOIN`
- `RUN`
- `ELIMINATE_INCOMPATIBLE`
- `STABILIZE`

The engine should prefer **minimal breaks**: preserve as much of the base mapping as possible and perturb exactly one relation first.

## Proposition roles

- **I.5**: forward equality pattern: equal sides -> equal base angles.
- **I.6**: counterfactual / converse pressure: equal base angles resist a side-inequality break.
- **I.7**: uniqueness / no-second-closure constraint for a fixed side configuration.
- **I.18**: propagate an ordered side disanalogy into an ordered opposite-angle disanalogy.
- **I.19**: propagate the ordered angle disanalogy back toward the opposite side; can be read as residual elimination once equality and reverse-order cases are blocked.

## Minimal experiment

1. Instantiate the isosceles base Gestalt.
2. Generate only two one-break counterfactuals:
   - one side becomes greater / smaller;
   - one base angle becomes greater / smaller.
3. Retrieve only proposition-patterns whose inferential role matches the active tension.
4. Run candidate continuations.
5. Record:
   - preserved contacts,
   - broken correspondences,
   - eliminated states,
   - newly inferred relations,
   - whether a new Gestalt stabilizes.
6. Do **not** inject a visual analogy to the target theorem.

## Research success criterion

A run is interesting when NMerovingio reaches a useful proposition path because the **inferential tension** of the counterfactual recalls a previous Gestalt, not because the target theorem or its diagram was supplied.

In particular, we want to observe paths such as:

`isosceles base -> minimal break -> counterfactual run -> contact with known equality/disquality regime -> elimination / propagation -> I.18 or I.19-like relation`

## Files

- `SPEC.md` — conceptual and computational contract.
- `data/propositions.json` — tiny proposition memory.
- `src/reasoner.py` — minimal executable prototype.
- `tests/test_reasoner.py` — sanity checks for counterfactual generation and proposition retrieval.

# Merovingio v1.0 — Prospective Generic-Space Binding with Jev Vision

This is a **working experiment**, not an autonomous geometric reasoner.

## Pipeline

1. **Recall** previously curated Generic Spaces from `NMerovingio/graph/generic_space_memory_v0_9.json`. Source IDs and repository file paths are retained.
2. **Bind partial roles** to a new current workspace. The remaining slots are described as missing, not proven.
3. **Propose constructions** deterministically as hypothetical drawings; preserve candidate IDs as anonymous K1–K4 and rotate their order.
4. **Ask Jev** to select the most useful bridge based on raw images and active Mental Spaces, with and without the historic source memory context.
5. **Validate after selection** using separate geometry routines and record before/after structural roles. Jev confidence is not evidence of geometric correctness.

## Historical memory cases

**Paired triangles:** the source `GS_HIST_DOUBLE_TRIANGLE` is abstracted from `workspace_quadrilateral_diagonal_v0_4_1.json`, whose material diagonal AC participates as a common side of two triangles. Current workspace: scalene triangle ABC, active C angle and opposite AB carrier. Candidate constructions join C→D on AB; A→E on BC; B→F on AC; P→Q between sides. Independent verifier checks whether the selected bridge generates the requested two adjacent closed triangles with a shared carrier.

**Common-radius circles:** source `GS_HIST_RADIUS_TRIANGLE` is abstracted from `workspace_two_circles_triangle_v0_4_1.json`. Current workspace: segment AB plus one circle centered A of radius AB. Candidates are a second circle centered B of matching radius, second circle centered B of smaller radius, duplicate circle centered A, or a line at the segment's middle. Verifier checks equal radius identity and circle intersection. A shorter second radius may still generate intersections: intersection alone is not enough to complete the historic Generic Space.

**Negative check:** the catalogue template `GS_PROP_I_5` cannot be instantiated as a theorem application from an arbitrary line construction without its equal-side premise being certified. Jev receives an explicit **none** option here.

## Ablation

- **schema_only:** active Mental Spaces and missing roles, but no historic provenance or source role schema.
- **historical_memory:** the same images and missing roles, plus the retrieved Generic Space's historic source and relation names.

The difference between conditions is **not a proof of memory's causal contribution**. The task wording still exposes the desired structural role in both conditions. A high score validates ranking of generated candidates, not autonomous proposal generation or Generic Space induction.

Each positive family has four rotated candidate-order trials, covering K1–K4 for the intended bridge. There are 16 positive calls plus 2 negative cases, totaling **18 live Jev decisions**. All results and usage are recorded in `output_prospective/prospective_results.json`.

## Interpret carefully

- Earlier workspaces are memory **fixtures and candidate abstractions**, not reconstructed formal proofs.
- Visual construction and symbolic verification are distinct; only verified structural roles are marked completed.
- No Euclid I.10 conclusion or theorem proof is attempted.
- The static candidate generator must eventually be replaced by a broader construction planner with bounded search, counterexamples, back-propagation, and failure analysis.
- For future experiments, introduce more ambiguous and held-out construction families and measure whether historical memory actually improves performance over schema-only.
- No API keys are printed, stored in files, or committed.

Running the GitHub Action is the only way this repository tests Jev live with the secret `TYPESAFE_API_KEY` already stored in GitHub Actions.

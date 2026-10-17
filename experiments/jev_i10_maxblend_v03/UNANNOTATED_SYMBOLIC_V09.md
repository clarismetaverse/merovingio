# Merovingio v0.9: unannotated image vs pure symbolic workspace

One invariant geometric construction: scalene triangle ABC, interior D on AB, connector CD.

Two input modes ONLY:
* **Unannotated diagram** — a single plain black-on-white drawing with only point identifiers (no highlighted sectors or regions, no colored overlays, no alternative annotated images).
* **Symbolic only** — points, carriers, incidences, strict betweenness and non-collinearity, without any image or prepackaged Mental Spaces.

Eight independent Jev Noul questions test four compatible interpretations of the same CD and four false counterexamples:
1. CD partitions angle at C (true).
2. CD partitions angle at A (false).
3. D partitions base AB (true).
4. D partitions BC (false).
5. CD is the shared edge of triangles ACD and BCD (true).
6. CD is simultaneously a boundary edge of ABC and ACD (false).
7. CD links angular fan at C to the segment AB (true).
8. CD joins strictly interior points of CA and CB (false).

No metric equalities, congruence criteria, proposition I.10 result, or theorem proof are supplied. Correctness labels remain in offline Python scoring, never in API payload. A model can accept multiple true mental-space roles instead of being forced to select one.

Design: 4 rigid rotations of the diagram compared with 4 symbol-order perturbations; eight requests, each containing eight independent Noul questions. Both modes see the same question texts; only the workspace representation changes.

The model's typed yes/no outputs cannot invent an unrestricted new mental-space vocabulary. This test measures recognition of hypothesized groupings, NOT unconstrained generation or formal proof.

GitHub Actions workflow: .github/workflows/jev-unannotated-symbolic-v09.yml. Output: output_v09/unannotated_symbolic_results.json. The runtime credential is read from an existing GitHub Actions secret, never stored in source or outputs.

Source documentation:
https://docs.typesafe.ai/primitives/noul
https://docs.typesafe.ai/images

# Merovingio v8 · Prospective Double-Scope Blending

## Research hypothesis

Before constructing CD, a bare triangle and the goal "divide its vertex angle" may activate:

- TRIANGLE: the canonical **angle opposite a nonincident side** relation.
- DIVISION: a generic **one whole → two parts** frame.

Selective projection of DIVISION through TRIANGLE's angle↔side opposition could anticipate **TWO relational role pairs**, even though the physical bisector, intersection point, base subdivisions and two material subtriangles have **not yet been created**.

The prospective blend is a candidate organization, not a metric fact. The construction may subsequently instantiate its missing roles. This tests a component of conceptual integration (composition, completion, elaboration), NOT an empirical psychological law.

## What counts as real novelty?

**Before constructing:** the material workspace has exactly three vertices, three boundary edges and a single triangular face. It does not contain D, CD, AD, DB, left/right subtriangles, equal sub-base parts or a memorized TWO_TRIANGLES frame. Only TRIANGLE and DIVISION appear in abstract frame memory.

**Prospective stage:**

1. Find the goal's angle in the material triangle.
2. Instantiate the TRIANGLE frame to find its *opposite side*.
3. Transport the DIVISION operation through that relation, introducing abstract sector slots (alpha, beta) and opposing subside slots (a, b).
4. Apply the **general polygon face-splitting rule** to a symbolic latent intersection X on that opposite edge. It generates two face cycles: since the parent is a 3-cycle, both happen to be triangles. The grammar also works for a quadrilateral and generates one triangle and a quadrilateral, which is tested.
5. A prospective, incomplete Generic Space holds this organization but **does not modify the material graph**.

**Construction stage:**

- The same geometric construction catalogue exists in ALL ablations: candidate bisectors from each of the three triangle vertices to the nonincident edge.
- The cognitive system chooses a candidate stochastically; goal satisfaction, triangle opposition and prospective frame completion can bias its score depending on the ablation.
- Only after choice, a compass/ruler-like ANGLE BISECTOR primitive computes a ray from the selected vertex, determines its intersection with the opposite edge, creates a new physical point and updates geometric faces.
- The point is derived by the sum of *unit rays*, not by assuming that the bisector bisects the opposite side.
- Independent bottom-up recognition rebuilds the two triangular faces and their opposite angle↔side roles from the constructed geometry.
- The model then tries to bind the *prospective symbolic slots* to the material faces. A construction from the wrong vertex does not count as a correct realization.

**Epistemic:** PROSPECTIVE_ONLY → CONSTRUCTED_STRUCTURAL; PROVEN is never asserted for the equal lengths of subsegments. Even if the triangle is equilateral, equality of base portions is not emitted as a proof; in the scalene and obtuse cases, it is generally false.

## Ablations

| Condition | Triangle opposition memory | Transport DIVISION across opposition | Prospective frame guides construction |
|---|---|---|---|
| full_blend | Yes | Yes | Yes |
| no_opposition | No | Unavailable | No |
| no_transport | Yes | No | No |
| post_construct_only | May be recognized later | No before construction | No |
| goal_only | Goal angle only | No | No |

All conditions use the same initial geometry and operation catalogue. Three shapes (equilateral, scalene, obtuse), all three goal vertices, and 48 seeded trials per combination: **2,160 simulations**. All outcomes must preserve non-provability.

The central success metrics distinguish:
- anticipates two role pairs BEFORE CD exists;
- chooses an operation that bisects the GOAL vertex;
- discovers two subtriangle faces AFTER the construction;
- binds the prospective slots to newly constructed material roles.

## Important limitations

This is a **designed, general combinatorial blending grammar**, not a learned imagination engine. The generic face-split operator and bisector candidate catalogue are programmed. It does not prove that any mathematician, including Euclid, historically performed the same cognitive operations. A prospective slot is not a point with coordinates and cannot be used to certify lengths or angle measurements. The success of the full condition is partly expected because its score explicitly rewards the frame completion.

Important future test: give entirely new polygons and different division operators **without** changing the grammar or numerical salience weights.

## Run from repository root

    python -m unittest discover -s NMerovingio/experiments/prospective_blending_v8 -p 'test_*.py' -v
    python NMerovingio/experiments/prospective_blending_v8/prospective.py --seeds 48
    python NMerovingio/experiments/prospective_blending_v8/viewer.py

Outputs: results/traces.json, results/aggregates.json, results/REPORT.md, results/viewer.html.

Parent branch: experiment/flat-angle-medial-regrouping-v7.

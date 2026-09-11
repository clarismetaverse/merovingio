# Triangle Multi-Agent Parallelogram / Composite-Zero Discovery — Run 06

> Controlled dry run under `MEROVINGIO_COGNITIVE_ARCHITECTURE_V03.md`.
>
> Input: the network after Run 05, where a parallel host is now bidirectionally usable and SAS has generated a strong unresolved pressure of the form `direction preservation + magnitude preservation -> ?`.
>
> Goal: test whether the multi-agent system can reorganize a banalized two-direction quadrilateral workspace into a governed family whose central state is a **composite zero**, without preloading the concepts `RECTANGLE`, `RHOMBUS`, `SQUARE`, or `COMPOSITE_ZERO`.
>
> This is a conceptual/dry run, not yet an autonomous software execution.

---

# 0. Hidden-target discipline

The agents are **not** told to discover:

```text
PARALLELOGRAM_FAMILY
RECTANGLE
RHOMBUS
SQUARE
COMPOSITE_ZERO
SQUARE_AS_ZERO
RIGHT_ANGLE_ZERO
EQUAL_SIDE_ZERO
```

Nor are they told that a 3×3 metric/angular state space is expected.

They may use only:

```text
N5 from Run 05
+ already certified parallel/direction-class machinery
+ banalized proposition-level capabilities equivalent in role to I.33 / I.34
```

A successful run must discover structure rather than terminology.

---

# 1. Frozen input network N5

The network already contains, among other things:

```text
F_TRIANGLE_RELATION
    (LT,LT), (EQ,EQ), (GT,GT)
    central invariant member = equality/equality

F_CORRESPONDENCE_COMPLETION
    INTERNAL
    EXTERNAL_OVERLAY

F_RELATIONAL_COMPLETION_FIELD
    role alignment
    relation constraints
    carriers
    completion rules
    readouts

ROLE_TOPOLOGY = {
    INTERNAL,
    EXTERNAL_OVERLAY,
    DISTRIBUTED_CARRIER
}

CLOSURE_TOPOLOGY = {
    COINCIDENT,
    FINITE_CLOSURE,
    DISTRIBUTED_NONCLOSURE,
    UNKNOWN
}

PARALLEL_HOST
    angle-pattern -> parallel certification
    parallel -> distributed angle completion

ASA
    full cognitive-cycle member of parallel host

SAS
    partial distributed host with strong open pressure:
        one direction class
        + two metric anchors
        + host-generated angle packet
        -> candidate translated/closed structure
```

The open impetus inherited from Run 05 is:

```text
PRESERVE_DIRECTION
+
PRESERVE_MAGNITUDE
+
CLOSE_ENDPOINTS
-> ?
```

---

# 2. Banalized injected quadrilateral workspace Q_raw

The injected material does not contain named quadrilateral subtypes.

Take four points:

```text
A, B, C, D
```

with a closed four-segment chain:

```text
A -- B
|    |
D -- C
```

but the drawing is only schematic.

The reasoner is given two direction-class constraints:

```text
AB || CD
BC || AD
```

and no further subtype labels.

This creates a two-direction distributed workspace:

```text
DIRECTION_CLASS_U = {AB, CD}
DIRECTION_CLASS_V = {BC, AD}
```

The quadrilateral is therefore already a **shared realization** of:

```text
- two parallel direction classes;
- one finite closed four-edge chain;
- two possible triangle decompositions by a diagonal.
```

No equal-side or right-angle assumptions are inserted.

---

# 3. Injected proposition-level capabilities

## 3.1 I.33-like closure capability

Banalized role form:

```text
If one pair of opposite segments is:
    - equal in magnitude
    - in one certified parallel direction class

then joining corresponding endpoints produces a second pair that is:
    - equal in magnitude
    - in one certified parallel direction class.
```

Cognitive reading:

```text
ONE TRANSLATED SEGMENT PAIR
    -> CLOSED TWO-DIRECTION EQUAL-OPPOSITE-SIDE PACKET
```

The theorem remains proposition-certified; the translation interpretation is cognitive.

## 3.2 I.34-like completion capability

For the two-direction closed quadrilateral:

```text
opposite sides match in magnitude
opposite angles match
any diagonal divides the workspace into two congruent triangles
adjacent angles occupy one distributed straight-completion relation
```

The network stores the proof support separately from the Gestalt compilation.

---

# 4. Expansion Agent — follow the SAS impetus

The Expansion Agent receives the unresolved Run-05 pattern:

```text
one certified direction class
+ equal metric anchors
+ completed angular packet
```

It asks whether an equal segment can be realized again at a distinct site while preserving direction.

Candidate construction:

```text
SEGMENT_1 = AB
SEGMENT_2 = CD

AB = CD
AB || CD
```

This is not yet a named quadrilateral.

The agent invokes the I.33-like capability:

```text
AB = CD
AB || CD
JOIN(A,D)
JOIN(B,C)

=> AD = BC
=> AD || BC
```

The result is a closed workspace with two direction classes and two opposite metric correspondences.

New candidate object:

```text
TWO_DIRECTION_CLOSED_TRANSLATION_PACKET
```

Status: `PROP-LICENSED CONSTRUCTION + COGNITIVE CANDIDATE`.

This is the first major result of Run 06:

```text
SAS pressure
    -> translated-segment realization
    -> second direction class
    -> closed four-edge host
```

Thus the previously incomplete SAS-host relation becomes substantially richer.

---

# 5. Completion Agent — compile the two-direction closed packet

The I.34-like capability now supplies:

```text
AB = CD
BC = AD

angle_A = angle_C
angle_B = angle_D

angle_A + angle_B = STRAIGHT
angle_B + angle_C = STRAIGHT
...

diagonal AC:
    triangle ABC congruent triangle CDA
```

The Completion Agent notices that the workspace can be compressed into two repeated direction families:

```text
METRIC FAMILY U/V
ANGULAR FAMILY alpha/beta
```

with:

```text
opposite sides duplicated by direction class
opposite angles duplicated by role
adjacent angles coupled by straight completion
```

The diagonal introduces a second simultaneous reading:

```text
QUADRILATERAL VIEW
    two direction classes

TRIANGLE-PAIR VIEW
    two congruent triangles
```

This is stored as:

```text
GESTALT_OVERLAP
SHARED_REALIZATION
```

not as an analogy edge.

---

# 6. Genealogy Agent — identify the two active variation registers

The Genealogy Agent decomposes the new host and asks:

```text
Which relations can vary without destroying the two-direction closed family?
```

It finds two independent qualitative registers.

## 6.1 Metric register

Compare adjacent direction-family magnitudes:

```text
M = rel(|AB|, |BC|)
```

with:

```text
M in {LT, EQ, GT}
```

Because opposite-side equality is already compiled:

```text
AB = CD
BC = AD
```

`M = EQ` implies all four sides occupy one metric-equality packet.

## 6.2 Angular register

Compare adjacent angle roles:

```text
A = rel(angle_A, angle_B)
```

with:

```text
A in {LT, EQ, GT}
```

Because adjacent angles straight-complete:

```text
angle_A + angle_B = STRAIGHT
```

`A = EQ` implies the two adjacent parts are equal halves of the straight whole.

Therefore the equality state is not just `angle_A = angle_B`; it is a **straight-completion zero**.

The Genealogy Agent reports:

```text
METRIC_DISANALOGY and ANGULAR_DISANALOGY are separable.
```

This is a crucial difference from the earlier triangle family, where side and opposite-angle order were coupled by one transducer.

---

# 7. Expansion Agent — generate the qualitative product space

Given two independently variable registers:

```text
M in {LT,EQ,GT}
A in {LT,EQ,GT}
```

The Expansion Agent generates the 3×3 field:

```text
                      ANGULAR REGISTER
                    LT      EQ      GT

METRIC      LT      x1      x2      x3
REGISTER    EQ      x4      x5      x6
            GT      x7      x8      x9
```

Unlike the triangle family, there is no proposition forcing only the diagonal or anti-diagonal.

All nine cells are provisionally admissible as qualitative members of the same two-direction closed family, subject to nondegeneracy.

This is the first appearance of a **product family**:

```text
F_PRODUCT = METRIC_TRIAD × ANGULAR_TRIAD
```

Status: `COGNITIVE CANDIDATE`.

---

# 8. Disanalogy stress test around equality/equality

The agents now test the central equality/equality state without naming it.

Define:

```text
Q0 = (M=EQ, A=EQ)
```

Then inject minimal breaks separately.

## 8.1 Break metric equality only

```text
BREAK_METRIC_EQUALITY:
    (EQ,EQ) -> (GT,EQ)
```

or mirrored:

```text
(EQ,EQ) -> (LT,EQ)
```

The angular zero survives.

Resulting family members preserve:

```text
all adjacent angles equal-under-straight-completion
opposite side pairs equal
but adjacent side families unequal
```

## 8.2 Break angular equality only

```text
BREAK_ANGULAR_EQUALITY:
    (EQ,EQ) -> (EQ,GT)
```

or mirrored:

```text
(EQ,EQ) -> (EQ,LT)
```

The metric zero survives.

Resulting family members preserve:

```text
all four sides in one equality packet
but adjacent angular roles differ while straight-completing
```

## 8.3 Break both

```text
(EQ,EQ) -> (GT,GT)
(EQ,EQ) -> (GT,LT)
(EQ,EQ) -> (LT,GT)
(EQ,EQ) -> (LT,LT)
```

These are generic doubly-disanalogical members.

The stress test validates that metric and angular breaks define genuinely different axes.

---

# 9. Symmetry Agent / Generic Reasoner — locate invariant states

The reasoner has two independent role reversals.

## 9.1 Metric-family role swap

Swap the two adjacent direction-family labels:

```text
sigma_M:
    LT <-> GT
    EQ -> EQ
```

on the metric register.

## 9.2 Angular-family role reversal

Reverse the adjacent angular role ordering:

```text
sigma_A:
    LT <-> GT
    EQ -> EQ
```

on the angular register.

Applied to the 3×3 family:

```text
sigma_M changes only M orientation
sigma_A changes only A orientation
```

The unique state invariant under **both** reversals is:

```text
(M=EQ, A=EQ)
```

The agents are not yet allowed to call it a square.

They report:

```text
DOUBLE_INVARIANT_STATE_CANDIDATE = (EQ,EQ)
```

Reasons:

```text
- metric disanalogy vanishes;
- angular disanalogy vanishes;
- fixed under metric-role reversal;
- fixed under angular-role reversal;
- lies at the intersection of two independent zero loci;
- all four side roles collapse into one metric class;
- all four angle roles collapse into one equal straight-completion class.
```

---

# 10. Reorganization Agent — discover zero loci before naming shapes

The Reorganization Agent rejects a flat list of nine cases.

It proposes two zero subfamilies.

## 10.1 Metric zero locus

```text
Z_M = {
    (EQ,LT),
    (EQ,EQ),
    (EQ,GT)
}
```

Interpretation:

```text
adjacent side families equal
```

Given opposite-side equality, this means all four sides share one metric role class.

## 10.2 Angular zero locus

```text
Z_A = {
    (LT,EQ),
    (EQ,EQ),
    (GT,EQ)
}
```

Interpretation:

```text
adjacent angle roles equal
and jointly straight-complete
```

Therefore each is half of the straight-angle whole.

## 10.3 Intersection

```text
Z_M ∩ Z_A = {(EQ,EQ)}
```

The Reorganization Agent proposes a new structural notion:

```text
COMPOSITE_ZERO_CANDIDATE
```

meaning:

```text
a family member at the intersection of two independently discovered zero loci.
```

This concept is generated by the run; it is not preloaded.

---

# 11. Compiler Agent — compile three nested family organizations

The Compiler Agent sees that the nine-state product contains natural subfamilies.

It proposes:

```text
F_TWO_DIRECTION_CLOSED
    all 9 qualitative states

F_METRIC_ZERO
    M = EQ

F_ANGULAR_ZERO
    A = EQ

F_DOUBLE_ZERO
    M = EQ and A = EQ
```

The key point is that these are not simple taxonomy labels.

They are **different partializations of one shared constructive workspace**.

A single material quadrilateral may therefore be read as:

```text
- member of the full two-direction closed family;
- member of a metric-zero subfamily;
- member of an angular-zero subfamily;
- member of both simultaneously.
```

---

# 12. Human-facing semantic identification after validation

Only now may the semantic layer map the emergent structures to standard names.

## 12.1 Full family

```text
F_TWO_DIRECTION_CLOSED
    -> parallelogram family
```

## 12.2 Metric-zero locus

```text
M = EQ
    -> rhombus-like family
```

because opposite-side equality is already present and adjacent side families now also coincide metrically.

## 12.3 Angular-zero locus

```text
A = EQ
    -> rectangle-like family
```

because adjacent equal angles also straight-complete, so all angle roles become right-angle roles.

## 12.4 Double-zero intersection

```text
M = EQ
A = EQ
    -> square
```

Thus the system recovers:

```text
SQUARE = intersection(metric-zero, angular-zero)
```

and more deeply:

```text
SQUARE = COMPOSITE ZERO OF THE DISCOVERED PRODUCT FAMILY
```

This is not encoded as "square is special" in advance.

---

# 13. Comparison with the triangle zero discovered in Run 01

The Genealogy Agent compares the two discoveries.

## 13.1 Triangle family

```text
one coupled relation transducer
stable states:
    (LT,LT), (EQ,EQ), (GT,GT)

central state:
    one zero relation packet
```

## 13.2 Two-direction closed family

```text
two independent variation registers
state space:
    {LT,EQ,GT} × {LT,EQ,GT}

central state:
    intersection of two zero loci
```

The Genealogy Agent therefore distinguishes:

```text
SIMPLE_ZERO
    one central zero of one coupled family

COMPOSITE_ZERO
    simultaneous zero of multiple independent family axes
```

Provisional interpretation:

```text
isosceles-like center -> SIMPLE_ZERO
square-like center    -> COMPOSITE_ZERO
```

This distinction is cognitive/family-level, not a Euclidean theorem classification.

---

# 14. Backward enrichment of SAS

The Run-05 SAS impetus is revisited.

Before Run 06:

```text
SAS
    two metric correspondences
    one included-angle correspondence
    one distributed direction class candidate
    unresolved translation/parallelogram host
```

After the I.33-like construction and two-direction closure:

```text
SAS pressure
    -> equal parallel segment realization
    -> second equal parallel segment pair
    -> closed two-direction host
    -> diagonal triangle-pair correspondence
```

Thus SAS gains a new construction affordance:

```text
EVOKE_TRANSLATED_SEGMENT_HOST
```

and a new host membership candidate:

```text
SAS_TRANSLATION_HOST = VALIDATED_AT_CONSTRUCTION_LEVEL
```

Important caution:

```text
SAS != parallelogram
```

The same construction can instantiate both:

```text
G_SAS_PAIR
G_TWO_DIRECTION_CLOSED
```

through shared elements and different partializations.

---

# 15. Backward enrichment of congruence

The diagonal of the two-direction closed host gives two congruent triangles.

Therefore the network can now read the same workspace as:

```text
PARALLEL/DIRECTION VIEW
    two opposite direction classes

QUADRILATERAL VIEW
    closed two-direction packet

TRIANGLE-PAIR VIEW
    congruent diagonal halves
```

This provides a new case of:

```text
CO_CONSTITUTION
```

The congruent triangle pair is not merely "inside" the quadrilateral as a static part.
It is one of the mechanisms through which opposite-side / opposite-angle structure becomes inferentially readable.

Conversely, the two-direction host supplies a constructional environment in which the triangle pair is naturally generated.

---

# 16. Strong analogy event: triangle zero vs quadrilateral zero

A weak system would record:

```text
ISOSCELES ~ SQUARE
```

because both are symmetric special cases.

The multi-agent system rejects this as too shallow.

The Genealogy Agent reports:

```text
shared high-level property:
    role-reversal invariance

but different generative depth:
    triangle zero = central state of one coupled transducer
    quadrilateral zero = intersection of two independently varying zero loci
```

The Reorganization Agent therefore adds not an analogy edge but a higher family concept:

```text
F_ZERO_ORGANIZATION {
    zero_loci
    symmetry_involutions
    independent_variation_axes
    composite_degree
    reachable_disanalogies
}
```

Instances:

```text
TRIANGLE_ZERO_ORGANIZATION:
    composite_degree = 1

QUADRILATERAL_DOUBLE_ZERO_ORGANIZATION:
    composite_degree = 2
```

This is a major conceptual output of Run 06.

---

# 17. New impetus generated by the square-like double zero

The agents now detect several new pressures.

## 17.1 Diagonal pressure

At the double-zero state, a diagonal produces two triangles that inherit both:

```text
metric symmetry
angular symmetry
```

Potential future question:

```text
Does the double-zero host generate a stronger triangle subtype at the diagonal level?
```

Human expectation may involve right-isosceles triangles, but this is not preloaded.

## 17.2 Perpendicular / bisector pressure

Equal adjacent angles that straight-complete imply a highly constrained intersection role.

Potential future host search:

```text
ANGULAR_ZERO
    -> perpendicular / right-angle family?
```

## 17.3 Equidistance pressure

Metric-zero + diagonal structures may create repeated equidistance packets.

Potential future link:

```text
METRIC_ZERO
    -> bisector / diagonal / circle-like hosts?
```

These are logged as expansion impulses only.

---

# 18. Validator checks

The Validator separates theorem-certified facts from cognitive organization.

## 18.1 Certified geometric backbone

Allowed:

```text
- opposite-side parallelism in the workspace;
- I.33-like equal-and-parallel closure consequence;
- I.34-like opposite-side/angle equality;
- adjacent straight-completion from parallel angle structure already available;
- diagonal congruence under the proposition-level support;
```

## 18.2 Cognitive but not theorem identities

The following are family-level interpretations:

```text
METRIC_ZERO_LOCUS
ANGULAR_ZERO_LOCUS
COMPOSITE_ZERO
F_ZERO_ORGANIZATION
SIMPLE_ZERO vs COMPOSITE_ZERO
```

They may guide search but are not used as unproved Euclidean premises.

## 18.3 No target leakage

The agents were not given:

```text
rectangle
rhombus
square
composite zero
```

The semantic labels are attached only after the relational structure is validated.

---

# 19. Network delta N5 -> N6

```text
N6 adds:

+ TWO_DIRECTION_CLOSED_TRANSLATION_PACKET
+ translated-segment construction route from SAS pressure
+ explicit quadrilateral / triangle-pair shared realization
+ METRIC register over adjacent direction families
+ ANGULAR register over adjacent straight-completing angle families
+ full 3×3 product state space
+ independent metric/angular disanalogy seeds
+ two zero loci
+ unique double-invariant member
+ COMPOSITE_ZERO_CANDIDATE
+ F_ZERO_ORGANIZATION
+ SIMPLE_ZERO / COMPOSITE_ZERO distinction
+ SAS_TRANSLATION_HOST
+ new diagonal/perpendicular/equidistance expansion impulses
```

The important change is not one extra quadrilateral theorem.

It is the appearance of a **product-family architecture** and a second, independently discovered type of zero organization.

---

# 20. Main result

Run 06 supports the following cognitive trajectory:

```text
parallel direction classes
    + metric preservation
    -> translated segment pair
    -> closed two-direction host
    -> opposite-role completion
    -> identify two independent variation axes
    -> generate 3×3 family
    -> detect two zero loci
    -> find unique intersection
    -> compile composite zero
```

After semantic interpretation:

```text
parallelogram family
    -> rhombus zero-locus
    -> rectangle zero-locus
    -> square double-zero intersection
```

The key research result is therefore not merely:

```text
"the square is a special parallelogram"
```

but:

```text
A highly symmetric geometric concept can emerge as the intersection
of independently discovered zero conditions in a generative Gestalt family.
```

This gives Merovingio a reusable hypothesis for future domains:

```text
When several independent variation axes are discovered,
search for their zero loci and test whether their intersections
form cognitively privileged composite-zero Gestalten.
```

---

# 21. Recommended next run

Freeze N6.

Do **not** immediately add more quadrilateral taxonomy.

Instead test the strongest new prediction:

```text
Take the double-zero member.
Project through one diagonal.
Decompile the two triangle halves.
Ask whether the agents independently recover a stronger triangle family
from the simultaneous metric-zero and angular-zero constraints.
```

This would test whether the newly discovered composite zero can
**re-enter and reorganize the older triangle network**, completing another full backward-enrichment cycle.

# Transversal Experiment — T0 Run 01

> First executed conceptual run of `TRANSVERSAL_GESTALT_EXPERIMENT_V01.md`.
>
> Scope: **local straight line, local intersection, triangle side-extension, exterior angle**. No two-intersection transversal and no parallelism are available yet.
>
> This run is especially important because it provides a control condition for the later transversal/parallel injection: we record exactly what the triangle network gains from *local* line/intersection Gestalten before any distributed-angle machinery exists.

---

# 0. Status vocabulary

Every result in this run is tagged as one of:

```text
SEED
    primitive geometric organization licensed at T0

PROP-LICENSED
    relation licensed by an already available Euclidean proposition

COMPILED
    recurrent proposition-licensed route promoted to a reusable Gestalt capability

COGNITIVE-CANDIDATE
    useful representational interpretation that is not itself a proof fact

OPEN
    not available yet at T0
```

The cognitive graph may cycle. Proof certificates may not.

---

# 1. Input network

The experiment begins from:

```text
N_triangle = TRIANGLE_GESTALT_NETWORK_V02
```

Important pre-existing resources include:

```text
OBJECT
    isosceles zero
    side <-> opposite-angle order family
    disanalogy genealogy

PAIR
    SAS / SSS / ASA zero masks
    pair congruence
    pair order family
    placement register

OPERATORS
    BREAK
    CUT_OFF
    OVERLAY
    REBASE
    EXTERNALIZE / INTERNALIZE
    MATCH / HOST / COMPLETE / PROJECT
    BACKWARD_ENRICH / EVOKE
    PART_WHOLE
```

The earlier blind side-disanalogy run had an unresolved frontier:

```text
side break
 -> CUT_OFF equal part
 -> local isosceles
 -> angle equality
 -> need cross-vertex angular comparison
 -> STALL
```

T0 explicitly tests whether local line/intersection structure supplies that missing bridge.

---

# 2. T0 seed workspace

Allowed local structures:

```text
CONTINUOUS_LINE
OPPOSITE_RAYS
ANGLE_ADJACENCY
ANGLE_PART_WHOLE
STRAIGHT_ANGLE
STRAIGHT_COMPLETION
INTERSECTION
VERTEX_OPPOSITION
EXTEND_COLLINEAR
TRIANGLE_SIDE_EXTENSION
```

Still forbidden:

```text
PARALLEL
CORRESPONDING_ANGLES_EQUAL
ALTERNATE_ANGLES_EQUAL
DISTRIBUTED_TRANSVERSAL
ANGLE_TRANSPORT_BY_PARALLELS
```

---

# 3. Run A — I.13 and the straight-completion Gestalt

Take a ray `OA` and extend through `O` to the opposite ray `OB`. Let a third ray `OC` divide the straight angular whole.

```text
A ----- O ----- B
       /
      C
```

Two adjacent angles occur:

```text
alpha = angle(AO, OC)
beta  = angle(CO, OB)
```

Because `OA` and `OB` instantiate one continuous straight carrier:

```text
STRAIGHT_COMPLETION(alpha, beta)
```

I.13 licenses the readout that the adjacent pair is equal to two right angles / one straight-angle whole.

## T0-A result

```text
G_STRAIGHT_COMPLETION   [COMPILED]

inputs:
    opposite rays on one continuous line
    an intervening ray

roles:
    ANGULAR_PART_1
    ANGULAR_PART_2
    STRAIGHT_WHOLE

invariant:
    part_1 + part_2 completes one straight whole
```

The key cognitive interpretation is not numerical addition but **whole-completion**:

```text
angular parts
 -> recognized as co-parts of one linear whole
 -> become inferentially co-present
```

## New carrier role

```text
CONTINUOUS_LINE
    -> COMPLETION_CARRIER
```

This is the first T0 enrichment.

---

# 4. Run B — I.15 as shared-whole cancellation

Let two continuous lines intersect at `O`, giving opposite angular sectors `alpha` and `gamma`, with adjacent sector `beta`.

Each opposite angle participates in a straight completion with the **same** adjacent angle:

```text
STRAIGHT_COMPLETION(alpha, beta)
STRAIGHT_COMPLETION(gamma, beta)
```

Both complete the same kind of straight whole.

Hence the shared completion structure forces:

```text
alpha = gamma
```

which is the vertical-angle equality licensed by I.15.

## T0-B result

```text
G_VERTICAL_OPPOSITION   [COMPILED]

opposite sectors
 + intersecting continuous lines
 + shared straight-completion partner
 -> equal angular readout
```

More importantly, the run exposes a reusable structural pattern:

```text
COMMON_WHOLE_COMPLETION

if:
    COMPLETE(x, c) -> W
    COMPLETE(y, c) -> W

then:
    x = y

when the subtraction/cancellation step is propositionally licensed.
```

Working cognitive name:

```text
SHARED_COMPLEMENT / SHARED_SUPPLEMENT CANCELLATION
```

`COMMON_WHOLE_COMPLETION` is logged as a **COGNITIVE-CANDIDATE**, not yet a universal primitive. More examples are required before compilation.

## Disanalogy test

Counterfactual:

```text
BREAK_VERTICAL_OPPOSITION_EQUALITY
alpha != gamma
```

while preserving:

```text
STRAIGHT_COMPLETION(alpha, beta)
STRAIGHT_COMPLETION(gamma, beta)
```

produces a collision: at least one preserved straight-completion relation must fail.

Thus the equality of vertical angles can be interpreted as a **zero-residue state of two shared-whole completions**.

---

# 5. Run C — triangle exterior angle as a multi-Gestalt hinge

Take triangle `ABC` and extend `BC` through `C` to `D`.

```text
B ----- C ----- D
 \     /
  \   /
    A
```

At `C` we now have:

```text
interior_C = angle(BCA)
exterior_C = angle(ACD)
```

Since `CB` and `CD` are opposite rays:

```text
STRAIGHT_COMPLETION(interior_C, exterior_C)
```

The same material angle `exterior_C` now belongs simultaneously to:

```text
G_TRIANGLE_EXTERNAL
G_STRAIGHT_COMPLETION
```

## T0-C result

```text
EXTERIOR_ANGLE_HINGE   [COMPILED]
```

It supports a concrete REBASE:

```text
TRIANGLE_AS_GROUND
    -> REBASE
EXTENDED_SIDE_AS_GROUND
```

without changing the material figure.

This is the first T0 case where one element has genuine **multi-Gestalt membership** and can transport reasoning between them.

## New construction affordance

```text
EVOKE_EXTEND_SIDE

trigger:
    need to compare / reorganize triangle angles

action:
    extend a triangle side into a continuous straight carrier

expected host:
    EXTERIOR_ANGLE_HINGE + STRAIGHT_COMPLETION
```

This affordance is now available for future triangle reasoning.

---

# 6. Run D — I.16 as cross-vertex localization by congruence

I.16 adds more than the proposition:

```text
exterior angle > either remote interior angle
```

Its construction is important for the cognitive graph because it provides a **mechanism** for making a remote interior angle locally readable inside the exterior-angle workspace.

A schematic form of Euclid's route is:

```text
TRIANGLE
  |
  | bisect a side / create equal metric parts
  | extend a constructed segment and copy an equal length
  v
PAIR OF TRIANGLES
  |
  | vertical-angle equality from I.15
  | SAS zero-mask from I.4
  v
CONGRUENT PAIR
  |
  | corresponding-angle readout
  v
REMOTE INTERIOR ANGLE COPIED TO A LOCAL ANGLE
  |
  | local copied angle is a proper part of exterior angle
  v
PART_WHOLE
  |
  v
EXTERIOR ANGLE > REMOTE INTERIOR ANGLE
```

The proof-level details remain propositionally certified by the Euclidean dependencies used in the construction. The cognitive result is the important new capability.

## T0-D result

```text
CROSS_VERTEX_ANGULAR_ORDER   [COMPILED]
```

and, more specifically:

```text
CONGRUENCE_MEDIATED_ANGLE_LOCALIZATION   [COMPILED]
```

Interpretation:

```text
remote angular role
 -> construct a congruent local representative
 -> place representative inside another angle
 -> use PART_WHOLE to obtain order
```

This gives T0 a transport/localization mechanism **before parallelism exists**.

That mechanism must be preserved as a baseline, because later parallelism may provide a cheaper distributed transport route.

---

# 7. Critical retroactive test — revisit the old I.18 frontier

This is the strongest result of T0.

Start from the old side-disanalogy:

```text
triangle ABC
AC > AB
```

Materialize the disanalogy by CUT_OFF:

```text
choose D on AC such that
AD = AB

AC = AD + DC
```

So:

```text
DC = METRIC_RESIDUE
```

Join `BD`.

The local isosceles Gestalt gives:

```text
AB = AD
 -> I.5
angle ABD = angle BDA
```

Before T0, the reasoning stalled because it needed to compare `angle BDA` with the remote angle `angle BCA`.

After T0, observe that `DA` is the extension of `DC` at vertex `D` of triangle `BDC`.

Therefore `angle BDA` is an exterior angle of triangle `BDC`.

The newly compiled I.16 capability gives:

```text
angle BDA > angle BCD
```

and because `D` lies on `AC`:

```text
angle BCD = angle BCA
```

while by angle part-whole at `B`:

```text
angle ABC > angle ABD
```

Combine:

```text
angle ABC
    > angle ABD
    = angle BDA
    > angle BCA
```

hence:

```text
AC > AB
 ->
angle ABC > angle BCA
```

## T0-E result

The previously unresolved side-disanalogy frontier now closes **without importing I.18 as the target theorem**.

```text
OLD FRONTIER
SIDE_BREAK
 -> CUT_OFF
 -> ISOSCELES LOCAL GESTALT
 -> STALL

T0-ENRICHED FRONTIER
SIDE_BREAK
 -> CUT_OFF
 -> ISOSCELES LOCAL GESTALT
 -> EXTERIOR_ANGLE_HINGE
 -> CROSS_VERTEX_ANGULAR_ORDER
 -> PART_WHOLE
 -> STABILIZED ORDER
```

Status:

```text
I18_DISCOVERY_ROUTE_AFTER_T0 = CLOSED
```

This is direct evidence for the research thesis:

```text
a later Gestalt can retroactively reorganize
and complete an earlier stalled reasoning path.
```

---

# 8. Network mutation caused by T0

Let:

```text
N_before = TriangleNet v0.2
N_T0     = N_before + local line/intersection/exterior-angle Gestalten
```

Then the qualitative delta is:

```text
Delta_T0 = {

    + G_STRAIGHT_COMPLETION,
    + G_VERTICAL_OPPOSITION,
    + EXTERIOR_ANGLE_HINGE,
    + CROSS_VERTEX_ANGULAR_ORDER,
    + CONGRUENCE_MEDIATED_ANGLE_LOCALIZATION,

    + EVOKE_EXTEND_SIDE,
    + TRIANGLE -> STRAIGHT_COMPLETION host route,
    + PAIR_CONGRUENCE -> ANGLE_LOCALIZATION route,
    + EXTERIOR_ANGLE -> TRIANGLE_ORDER projection route,

    + backward enrichment of SIDE_BREAK reasoning,
    + closure of old I.18 frontier,

    + candidate COMMON_WHOLE_COMPLETION pattern
}
```

---

# 9. Important cross-level cycle discovered at T0

T0 already exhibits circular cognitive reasoning before any true transversal is introduced.

Existing pair-level congruence participates in the proof/construction of the exterior-angle order capability:

```text
PAIR / SAS
    -> constructed local congruence
    -> local copy of remote angle
    -> exterior-angle order
    -> enrich OBJECT triangle-order reasoning
```

Then the enriched object-level network can more easily generate ordered triangle families.

So we obtain:

```text
PAIR GESTALT
   -> LINE / EXTERIOR HOST
   -> OBJECT ORDER ENRICHMENT
```

This is a genuine cross-level feedback route, while proof dependencies remain acyclic.

---

# 10. A new notion: transport before parallelism

T0 reveals that **angle transport is not introduced for the first time by parallels**.

There is already a construction-heavy transport mechanism:

```text
ANGLE_TRANSPORT_VIA_CONGRUENCE
```

whose cost is approximately:

```text
construct equal parts
+ construct second triangle
+ establish vertical equality
+ certify congruence
+ read corresponding angle
+ part-whole comparison
```

This is a crucial control variable for T1/T2.

Later we will test whether the transversal/parallel Gestalt compiles the same functional result into a shorter path:

```text
ANGLE_TRANSPORT_VIA_DISTRIBUTED_DIRECTION
```

If so, the important effect of parallelism will not be merely that it makes new facts true. It will be that it **compresses an already possible transport operation into a more synoptic Gestalt**.

This is a strong candidate example of:

```text
reasoning past -> object present
```

---

# 11. Counterfactual family available after T0

T0 now supports the following local disanalogies.

```text
D_STRAIGHT_COMPLETION
    seed: break straight completion
    residue: ANGULAR or DIRECTIONAL

D_LINE_CONTINUITY
    seed: bend the extension
    residue: DIRECTIONAL

D_VERTICAL_OPPOSITION
    seed: break opposite-angle equality
    preserved test: shared straight-completion partner
    result: collision unless another carrier relation breaks

D_EXTERIOR_ORDER
    seed: exterior <= remote interior
    result: rejected by I.16 capability

D_EXTERNAL_ANGLE_HINGE
    seed: preserve triangle role but break collinearity of extension
    result: triangle membership survives while straight-completion membership fails
```

The last case is especially useful because it explicitly separates **membership in one Gestalt from membership in another** for the same material angle.

---

# 12. What T0 does NOT yet provide

The control condition is important.

At T0 there is still no licensed mechanism for:

```text
remote angle equality merely because two intersections share a transversal
corresponding-angle equality
alternate-angle equality
same-side interior supplementarity across two intersections
parallel-host membership
transport by parallel direction class
```

Therefore:

```text
ASA_PARALLEL_HOST = OPEN
DISTRIBUTED_STRAIGHT_COMPLETION = OPEN
TWO_INTERSECTION_TRANSVERSAL_FAMILY = OPEN
```

This is a useful negative result.

T0 enriches triangle order reasoning strongly, but it does **not yet** provide the distributed Gestalt hypothesized for ASA.

---

# 13. Synoptic-gain baseline for the next stages

Record two available paths for angular reasoning.

## Path T0-A — local straight completion

```text
adjacent angle roles
 -> continuous-line host
 -> straight whole
```

## Path T0-B — cross-vertex comparison

```text
remote angle
 -> congruent local copy
 -> containment in exterior angle
 -> angular order
```

The next stage should ask whether one continuous transversal across two intersections creates:

```text
remote angle
 -> distributed role correspondence
 -> localizable angular relation
```

with fewer auxiliary constructions.

The comparison target is therefore not merely theorem coverage but:

```text
path length
construction cost
number of new objects
number of active Gestalten
SynopticGain
reusability
new EVOKE affordances
```

---

# 14. T0 verdict

T0 is a positive result.

It demonstrates all of the following before parallelism:

```text
1. straight lines act as angular completion carriers;
2. intersection opposition can be derived from shared completion structure;
3. exterior angles are multi-Gestalt hinges between triangle and line reasoning;
4. congruence can localize a remote angular role;
5. part-whole can turn that localization into angular order;
6. the resulting I.16 capability closes the previously open I.18 side-disanalogy frontier;
7. the injected line/intersection Gestalten therefore modify the effective topology of the older triangle network.
```

Most importantly:

```text
T0 does not merely add I.13 / I.15 / I.16 nodes.

It adds a new route:

TRIANGLE DISANALOGY
 -> EXTEND SIDE
 -> LINEAR HOST
 -> LOCALIZE REMOTE ANGLE
 -> PART_WHOLE
 -> STABILIZE ORDER
```

This is the first concrete experimental instance in NMerovingio of **backward network completion**.

---

# 15. Next stage — T1

T1 should add exactly one new resource:

```text
ONE CONTINUOUS TRANSVERSAL
intersecting TWO otherwise unrelated carrier lines
```

Still do not assume parallelism.

The central T1 test is:

```text
Can the shared transversal itself act as an epistemic contact
that lets the two local intersection packets be LOCALIZED / DISTRIBUTED
without using congruence as the transport mechanism?
```

In other words:

```text
T0 transport = via constructed congruent triangles
T1 candidate transport = via one continuous directional carrier
```

That contrast should be kept explicit in the next run.

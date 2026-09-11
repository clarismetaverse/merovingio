# Triangle Multi-Agent Zero Recompositon — Run 08

> Controlled blind dry run under `MEROVINGIO_COGNITIVE_ARCHITECTURE_V03.md`.
>
> Goal: reverse the logic of Run 07. Start from two local triangle-zero Gestalten, a shared carrier, pair congruence, and one additional angular condition. Hide `SQUARE`, `RECTANGLE`, `RHOMBUS`, `PARALLELOGRAM`, and `COMPOSITE_ZERO`. Ask whether the multi-agent system can invent a higher host through `RECOMPOSE_ZERO` rather than being told which quadrilateral to build.

---

# 0. Hidden-target discipline

The agents are not told to discover:

```text
SQUARE
RECTANGLE
RHOMBUS
PARALLELOGRAM
COMPOSITE_ZERO
RIGHT_ISOSCELES_TRIANGLE
SQUARE_FROM_TWO_TRIANGLES
```

Nor are they told that the local triangle zeros came from a diagonal cut of a richer host.

The run succeeds structurally if the system independently proposes a four-edge host in which:

```text
- the two local triangle zeros are compatible partializations;
- the shared carrier acts as a recomposition hinge;
- boundary metric equalities combine into a global metric zero locus;
- angular correspondences certify two distributed direction classes;
- the additional angular condition creates a second, independent angular zero locus;
- the intersection of the two zero loci yields a unique high-symmetry host state.
```

Only after validation may a human-facing semantic layer identify the host classically.

---

# 1. Input network N7

The current network already contains:

```text
F_TRIANGLE_RELATION
    stable states = {(LT,LT),(EQ,EQ),(GT,GT)}
    central triangle-zero = (EQ,EQ)

F_CORRESPONDENCE_COMPLETION
    internal and external realizations
    SAS / ASA / SSS masks

F_RELATIONAL_COMPLETION_FIELD

F_GLOBAL_CONSTRAINT_COMPLETION

F_ZERO_ORGANIZATION
    SIMPLE_ZERO
    COMPOSITE_ZERO as a structural type

PROJECT_ZERO(host,subworkspace)
    strongly supported by Run 07

RECOMPOSE_ZERO(local_gestalts)
    open candidate from Run 07
```

Run 07 also enriched the triangle zero with the possibility that it may be inherited/projected from a richer host.

The question now is whether the inverse direction can be generated constructively rather than stipulated.

---

# 2. Blind material input

Create two triangle objects sharing one segment `AC`, lying on opposite sides of `AC`.

```text
        B
       / \
      /   \
     A-----C
      \   /
       \ /
        D
```

The system receives only the following structured facts.

## 2.1 Local triangle zero T1

Triangle `ABC` is an instance of the already-discovered triangle relation zero:

```text
AB = BC
angle BAC = angle BCA
```

No subtype name is supplied.

## 2.2 Local triangle zero T2

Triangle `ADC` is another instance of the same local zero family:

```text
AD = DC
angle CAD = angle ACD
```

Again no subtype name is supplied.

## 2.3 Shared carrier

```text
AC = common side
B and D lie in opposite halfplanes of AC
```

`AC` is marked only as a shared material carrier / epistemic contact.

## 2.4 Pair correspondence

The two triangles are supplied as congruent under the role map:

```text
A(T1) <-> C(T2)
B(T1) <-> D(T2)
C(T1) <-> A(T2)
```

or any equivalent validated orientation-preserving/reflected correspondence compatible with the diagram.

The important fact is:

```text
T1 and T2 instantiate one FULL_PAIR_COINCIDENCE packet under an allowed overlay.
```

The system must preserve the fact that they are materially placed on opposite sides of `AC`; pair congruence is correspondence, not literal current placement identity.

## 2.5 One additional angular condition

At one apex, provide a self-supplementary completion signature rather than the label `RIGHT_ANGLE`:

```text
STRAIGHT_COMPLETION(theta_B, theta_B)
```

where:

```text
theta_B = angle ABC
```

Thus `theta_B` occupies two equal halves of one straight whole.

The semantic label `right angle` is hidden.

By pair congruence, the corresponding apex angle at `D` is available as equal once projected through the pair packet.

---

# 3. Initial impetus field

The Generic Reasoner detects several simultaneous pressures.

```text
RECOMPOSITION_IMPETUS
    two local zeros share one carrier and complementary halfplane placement

GENEALOGICAL_IMPETUS
    Run 07 showed that richer host zeros can project into such local zeros

COMPLETION_IMPETUS
    pair congruence supplies cross-triangle role correspondence

REORGANIZATION_IMPETUS
    local triangle and pair views may be incomplete descriptions of one larger workspace

EXPANSION_IMPETUS
    ask whether boundary elements can be promoted into a closed host
```

Crucially the router does not tell any agent that the target should be a quadrilateral.

---

# 4. Expansion Agent — first recomposition move

The Expansion Agent treats the two triangles as compatible partializations around the shared carrier `AC`.

It proposes a constructive operation:

```text
RECOMPOSE_AROUND_SHARED_CARRIER(T1,T2,AC)
```

with preserved facts:

```text
- AC remains internal hinge;
- B and D remain in opposite halfplanes;
- triangle incidence is preserved;
- outer boundary becomes A-B-C-D-A.
```

This produces a candidate larger workspace:

```text
W4 {
    boundary = [AB,BC,CD,DA]
    internal_hinge = AC
    local_views = [T1,T2]
}
```

Status: `CONSTRUCTED HOST CANDIDATE`.

No quadrilateral subtype label is introduced.

---

# 5. Completion Agent — metric zero propagates upward

From the local zeros:

```text
AB = BC
AD = DC
```

and from pair congruence between `T1` and `T2`, the role map supplies cross-triangle boundary correspondences, e.g.:

```text
AB = DC
BC = AD
```

Together the packet closes to:

```text
AB = BC = CD = DA
```

The agent records:

```text
GLOBAL_BOUNDARY_METRIC_ZERO
```

without naming the resulting figure.

This is the first important inversion of Run 07:

```text
Run 07:
    host metric zero -> local triangle zero

Run 08:
    compatible local triangle zeros + pair correspondence
        -> host metric zero
```

The local zero has become upward-generative.

---

# 6. Genealogy Agent — distinguish inheritance from recomposition

The Genealogy Agent compares the new route with Run 07.

It refuses to mark:

```text
RECOMPOSE_ZERO = inverse(PROJECT_ZERO)
```

because one projected local zero may admit multiple possible hosts.

Instead it proposes:

```text
PROJECT_ZERO
    host -> constrained local zero profiles

RECOMPOSE_ZERO
    compatible local zero profiles + hinge + cross-constraints
        -> ranked host candidates
```

Thus the relation is bidirectional at the level of search, but not bijective.

New provenance type:

```text
ZERO_ORIGIN = {
    INTRINSIC,
    INHERITED,
    RECOMPOSED
}
```

The global metric zero in this run is tagged `RECOMPOSED`.

---

# 7. Host Search Agent — do direction classes emerge?

The system now examines the angle relations created by the two triangle zeros and pair congruence around the shared carrier `AC`.

From the local zero packets and pair correspondence, it can align angle roles such as:

```text
angle BAC = angle ACD
angle BCA = angle CAD
```

under a validated orientation map.

These are precisely the sort of distributed angular masks that Run 04 learned can certify nonclosure / parallel direction classes through I.27/I.28-like capabilities.

The Host Search Agent therefore tests:

```text
AB and CD as one distributed direction class
BC and AD as a second distributed direction class
```

After geometric validation:

```text
AB || CD
BC || AD
```

become certified readouts.

The outer host is now no longer merely a four-edge loop.

It has:

```text
TWO_DIRECTION_DISTRIBUTED_CLOSURE {
    direction_class_1 = {AB,CD}
    direction_class_2 = {BC,AD}
    metric_boundary_zero = TRUE
}
```

The classical name remains hidden.

---

# 8. Reorganization Agent — first host family discovered

The Reorganization Agent sees that the candidate host combines:

```text
- four-edge finite closure;
- two opposite distributed direction classes;
- one recomposed metric zero locus;
- one internal diagonal carrier that generates two congruent local zeros.
```

It proposes a new family-level representation:

```text
F_FOUR_EDGE_DISTRIBUTED_CLOSURE {
    direction_class_A
    direction_class_B
    metric_register
    angular_register
    diagonal_partializations
    zero_profiles
}
```

The specific current member satisfies:

```text
metric_register = EQ
angular_register = UNKNOWN / not yet globally compiled
```

This is important: the system does **not** jump directly to the final double-zero host.

It first discovers the one-zero host family.

Human interpretation is still withheld, but structurally this is the equal-side branch of the four-edge distributed-closure family.

---

# 9. Inject the additional angular condition into the host

Recall the only extra non-triangle-zero condition:

```text
STRAIGHT_COMPLETION(theta_B, theta_B)
```

The Completion Agent reads this as:

```text
theta_B = its own straight complement
```

and therefore as a local angular fixed state under supplement reversal.

Pair congruence gives:

```text
theta_D = theta_B
```

so the corresponding opposite apex is in the same local angular fixed state.

The two certified direction classes from Section 7 now make I.29-like packet completion available throughout the host.

Adjacent angular roles complete to a straight whole, and the fixed state at `B` propagates through the distributed host.

The network therefore derives a global angular zero locus:

```text
GLOBAL_BOUNDARY_ANGULAR_ZERO
```

whose members all occupy the same self-supplementary angular role.

Again the semantic word `right` is not needed for discovery.

---

# 10. Composite zero emerges

The current host now carries two independently generated zero conditions:

```text
Z_M:
    boundary metric relation = EQ

Z_A:
    boundary angular relation = self-supplementary/equal fixed state
```

They have distinct genealogies:

```text
Z_M
    <- local triangle zeros
    <- pair congruence
    <- recomposition around AC

Z_A
    <- one supplied angular fixed condition
    <- pair projection
    <- parallel/direction packet completion
```

Therefore:

```text
Z_M != Z_A genetically
```

but they coexist in one host.

The Reorganization Agent detects:

```text
Z_M ∩ Z_A
```

as a unique highly constrained member of `F_FOUR_EDGE_DISTRIBUTED_CLOSURE`.

It assigns the structural label:

```text
COMPOSITE_ZERO_HOST_CANDIDATE
```

without using any classical polygon name.

---

# 11. Symmetry / disanalogy stress test

To determine whether the discovered state is genuinely organizing rather than merely overconstrained, the Expansion Agent breaks the two zero registers independently.

## 11.1 Break metric zero only

Preserve:

```text
angular zero
parallel direction classes
four-edge closure
```

but introduce:

```text
adjacent boundary lengths unequal
```

The host remains coherent.

Thus metric zero is one independent variation axis.

## 11.2 Break angular zero only

Preserve:

```text
metric zero
parallel direction classes
four-edge closure
```

but rotate one direction family so adjacent angles leave the angular fixed state while opposite/parallel structure remains coherent.

The host again remains coherent.

Thus angular zero is a second independent variation axis.

## 11.3 Break both

The generic distributed four-edge family survives.

This validates a product-like organization:

```text
metric axis x angular axis
```

and confirms that the discovered double-zero state is the intersection of two independent zero loci, not a single accidental theorem state.

---

# 12. Compiler Agent — recomposition pattern becomes reusable

The Compiler Agent notices the recurrent sequence:

```text
LOCAL_ZERO_1
+ LOCAL_ZERO_2
+ SHARED_HINGE
+ CROSS-CORRESPONDENCE
    -> GLOBAL_ZERO_1

+ independent local/global condition
    -> GLOBAL_ZERO_2

GLOBAL_ZERO_1 ∩ GLOBAL_ZERO_2
    -> COMPOSITE_ZERO_HOST
```

It proposes a reusable macro:

```text
RECOMPOSE_ZERO {
    inputs:
        local_zero_profiles
        shared_carriers
        placement_compatibility
        cross_correspondence
        optional_extra_constraints

    search:
        candidate host closures
        role topology
        direction classes
        zero propagation routes

    output:
        ranked host candidates
        recomposed zero loci
        composite-zero candidates
        provenance
}
```

Status: `COMPILED COGNITIVE OPERATOR CANDIDATE`.

---

# 13. Human-facing interpretation after validation

Only after the structural run is complete may the semantic layer apply classical names.

The one-zero host discovered before the extra angular condition is the equal-side member of the parallelogram family (rhombus-like).

The double-zero host satisfies:

```text
all four boundary sides equal
all four interior angles right
opposite sides parallel
```

and is therefore the classical **square**.

The local triangle views are the corresponding congruent right-isosceles halves.

But importantly, none of those labels was needed to generate the host organization.

---

# 14. Main result: zero can propagate both downward and upward

Run 07 established:

```text
HOST COMPOSITE ZERO
    -> diagonal partialization
    -> local triangle zero profiles
```

Run 08 establishes the converse search pattern:

```text
compatible LOCAL ZERO PROFILES
+ shared carrier
+ pair constraints
    -> recomposed host zero
```

Therefore the network now supports:

```text
DOWNWARD ZERO PROJECTION
UPWARD ZERO RECOMPOSITION
```

but they are not logical inverses.

The relation is better represented as a generative cycle:

```text
HOST
 -> PROJECT_ZERO
 -> LOCAL ZERO PROFILES
 -> perturb / recombine / compare
 -> RECOMPOSE_ZERO
 -> HOST CANDIDATES
```

A recomposed host may differ from the ancestral host if the local pieces are reattached under different constraints.

This makes the cycle creative rather than merely reversible.

---

# 15. New network delta

```text
N7
 + RECOMPOSE_AROUND_SHARED_CARRIER
 + RECOMPOSED_ZERO provenance
 + F_FOUR_EDGE_DISTRIBUTED_CLOSURE
 + upward metric-zero propagation
 + host direction-class reconstruction from triangle correspondences
 + upward angular-zero propagation
 + validated COMPOSITE_ZERO_HOST discovery
 + independent metric/angular disanalogy axes
 + RECOMPOSE_ZERO operator candidate
```

The most important conceptual change is:

```text
zero is no longer only a state located inside a family.
zero conditions are transportable constraints that can be
projected, inherited, recomposed, and fused across levels.
```

---

# 16. Implication for the deep architecture

The run suggests enriching `ZERO_STRUCTURE` to include not only where a zero exists, but how it moves through the network.

```text
ZeroStructure {
    zero_id
    host_gestalt
    register

    origin:
        INTRINSIC | INHERITED | RECOMPOSED | PROPAGATED

    projection_routes
    recomposition_routes
    compatibility_conditions

    independent_zero_axes
    composite_memberships

    break_signatures
    provenance
}
```

This should eventually allow queries such as:

```text
- Which composite zeros can be built from this local zero?
- Which local zeros are projections of this host?
- Which host candidates explain the coexistence of these local zero profiles?
- Which zero conditions are genetically independent but currently fused?
- Which disanalogy breaks only one component of a composite zero?
```

---

# 17. Why Run 08 matters

The key success is not reconstructing a familiar square.

The important event is that a **local family organization becomes generative upward**.

The system begins from two already-compiled triangle zeros and discovers that their compatibility, common carrier, and pair correspondence demand a richer host organization.

This means the cognitive graph can now support both directions:

```text
rich whole -> partial Gestalten
partial Gestalten -> hypothesize richer whole
```

That is exactly the kind of circular, non-logically-circular reasoning required by the Merovingio architecture.

A strong next experiment is to remove the extra angular condition entirely and ask the agents to explore the full recomposition family generated by two triangle zeros. The expectation should remain hidden: the system may discover a one-zero host family and then use disanalogy/expansion to search for independent second-zero conditions on its own.

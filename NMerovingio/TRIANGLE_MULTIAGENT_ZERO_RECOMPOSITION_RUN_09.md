# Triangle Multi-Agent Zero Recomposition — Run 09

> Creative blind recomposition run under `MEROVINGIO_COGNITIVE_ARCHITECTURE_V03.md`.
>
> This run repeats the inverse direction explored in Run 08 but removes the extra angular condition entirely.
>
> Goal: give the system only two local triangle-zero packets, one shared carrier, and a validated pair-congruence relation, then observe whether the agents:
>
> 1. stop at a one-zero host;
> 2. discover an unresolved independent variation axis;
> 3. invent a candidate second-zero condition without being told `SQUARE`, `RIGHT_ANGLE`, `RECTANGLE`, `RHOMBUS`, or `COMPOSITE_ZERO`.
>
> This is a controlled dry run, not an autonomous software execution.

---

# 0. Hidden-target discipline

The following labels and target structures are hidden from all creative agents:

```text
SQUARE
RHOMBUS
RECTANGLE
PARALLELOGRAM
RIGHT_ANGLE
COMPOSITE_ZERO
METRIC_ZERO
ANGULAR_ZERO
SECOND_ZERO_AXIS
EQUAL_ADJACENT_ANGLES
```

The agents are not asked to recover a named quadrilateral.

They are asked only:

```text
Given these local zero structures and their pair relation,
what larger workspace is naturally supported,
what remains unconstrained,
and what new organization is suggested by the unresolved structure?
```

The run must not treat a visually symmetric sketch as evidence.

---

# 1. Input packet

We provide two triangle objects `T1` and `T2` joined along one common carrier `h`.

Each triangle independently instantiates the previously discovered central member of `F_TRIANGLE_RELATION`:

```text
T1:
    local_side_relation  = EQ
    local_angle_relation = EQ

T2:
    local_side_relation  = EQ
    local_angle_relation = EQ
```

The two triangles additionally satisfy a validated pair relation:

```text
PAIR(T1,T2) = FULL_PAIR_CONGRUENCE
```

and share:

```text
COMMON_CARRIER = h
```

No additional angular whole, perpendicularity, diagonal equality, or external symmetry fact is supplied.

The material workspace is therefore deliberately underdetermined.

---

# 2. Initial impetus field

The Generic Reasoner produces four simultaneous pressures.

```text
RECOMPOSITION_IMPETUS
    two internally organized local zeros share a hinge and a pair relation

COMPLETION_IMPETUS
    the local packets strongly constrain a possible larger boundary

EXPANSION_IMPETUS
    several global relations remain open after local completion

REORGANIZATION_IMPETUS
    the current network has PROJECT_ZERO but only a provisional inverse notion
```

The Router sends these to the Completion, Expansion, Genealogy, Reorganization, and Compiler agents.

---

# 3. Completion Agent — recover only what is forced

The Completion Agent combines:

```text
local zero in T1
local zero in T2
pair congruence
shared carrier h
```

and projects all certified side correspondences onto the boundary of the recomposed four-edge workspace.

It finds that the four boundary edge roles fall into one metric role class.

Provisional readout:

```text
BOUNDARY_EDGE_1 = BOUNDARY_EDGE_2
BOUNDARY_EDGE_2 = BOUNDARY_EDGE_3
BOUNDARY_EDGE_3 = BOUNDARY_EDGE_4
```

The agent packages this as:

```text
GLOBAL_BOUNDARY_METRIC_ZERO
```

but does not assign a classical polygon name.

Status: `VALIDATED READOUT`, conditional on the chosen recomposition embedding.

Crucially the Completion Agent does **not** infer any adjacent-angle equality.

---

# 4. Host Search — minimal four-edge closure

The Host Search Agent asks whether the two triangles can be interpreted as complementary partializations of one four-edge host.

A candidate host is accepted only if:

```text
- both local triangles embed without changing their certified relations;
- the common carrier remains the partition hinge;
- the outer boundary closes consistently;
- pair correspondence is preserved;
- no hidden angular equality is added.
```

The resulting minimal host has:

```text
FOUR_EDGE_CLOSURE
GLOBAL_BOUNDARY_METRIC_ZERO
TWO_TRIANGLE_PARTITION
COMMON_HINGE
```

and an angular register that remains open.

The host is therefore not a full composite-zero object.

Status:

```text
ONE_ZERO_HOST = VALIDATED COGNITIVE HOST
```

---

# 5. Genealogy Agent — what came from where?

The Genealogy Agent distinguishes four origins.

```text
local triangle equalities
    origin = INTRINSIC_ZERO

cross-triangle correspondence
    origin = PAIR_COMPLETION

global boundary side equality
    origin = RECOMPOSED_ZERO

remaining adjacent-angle relation
    origin = UNRESOLVED
```

This yields a stronger zero genealogy:

```text
ZERO_ORIGIN = {
    INTRINSIC,
    INHERITED,
    RECOMPOSED,
    PROPAGATED,
    UNRESOLVED
}
```

The new `UNRESOLVED` status is important: not every structurally adjacent register must receive a zero merely because another register has one.

---

# 6. Expansion Agent — expose the free angular degree

The Expansion Agent now perturbs the recomposed host while preserving:

```text
all boundary edge equalities
common hinge genealogy
pair congruence of the two local triangles
four-edge closure
```

It searches for deformations that change only the global angular organization.

It finds a qualitative family:

```text
A_GLOBAL in {LT, EQ, GT}
```

where `A_GLOBAL` compares the two adjacent angular role classes of the host.

All three orientations are compatible with the already-established metric zero at the purely cognitive family level:

```text
(M = EQ, A = LT)
(M = EQ, A = EQ)
(M = EQ, A = GT)
```

The important discovery is therefore not another zero fact, but an **independent variation axis**.

Output:

```text
FREE_ANGULAR_AXIS_CANDIDATE
```

Status: `VALIDATED AS VARIATION SPACE`, not as a theorem saying every abstract state is constructible without further conditions.

---

# 7. Symmetry stress — discover a central angular candidate without asserting it

The Generic Reasoner applies the host role-reversal symmetry that exchanges the two adjacent angular roles.

It induces:

```text
LT <-> GT
EQ <-> EQ
```

Therefore the Expansion and Reorganization agents jointly identify:

```text
A = EQ
```

as the unique fixed member of the angular variation axis.

They label it only:

```text
ANGULAR_CENTRAL_INVARIANT_CANDIDATE
```

No claim is made that the current input instance occupies this state.

This is the key result of Run 09:

```text
The system discovers the missing second zero locus as a structurally privileged
possibility, without being given a condition that forces the input into it.
```

---

# 8. Reorganization Agent — one-zero host becomes a family slice

The existing host was represented as one object:

```text
ONE_ZERO_HOST
```

The newly exposed angular degree makes this representation too coarse.

The Reorganization Agent proposes:

```text
F_METRIC_ZERO_FOUR_EDGE {
    fixed_register:
        M = EQ

    free_register:
        A in {LT,EQ,GT}

    symmetry:
        LT <-> GT
        EQ fixed

    central_member:
        (M=EQ, A=EQ) [candidate only]
}
```

The input instance belongs to the family but is not automatically assigned to the central member.

This is a substantial improvement over Run 08 because the network now separates:

```text
DISCOVERING A ZERO LOCUS
from
ESTABLISHING THAT THE CURRENT OBJECT LIES ON THAT LOCUS.
```

---

# 9. Recomposition is now explicitly abductive

Run 08 suggested:

```text
RECOMPOSE_ZERO(local_gestalts)
```

Run 09 shows that this is insufficiently precise.

The better operator is:

```text
RECOMPOSE_GESTALTS(local_packets, shared_contacts)
    -> HostCandidate[]
```

followed by:

```text
EXTRACT_INHERITED_CONSTRAINTS(host)
EXPOSE_FREE_REGISTERS(host)
SEARCH_ZERO_LOCI(host_family)
```

Thus recomposition does not promise a unique global zero.

It constructs the strongest licensed host, then asks what dimensions remain free.

This makes recomposition an abductive/generative process rather than a deterministic inverse.

---

# 10. Can the agents invent candidate conditions for the second zero?

The Expansion Agent is now allowed to search for minimal constraints that would collapse:

```text
A in {LT,EQ,GT}
```

to its fixed member:

```text
A = EQ
```

It may propose multiple candidate routes, each kept separate by genealogy.

Candidate classes discovered structurally include:

```text
C1. directly impose equality of the two adjacent angular roles;

C2. impose a local straight-completion condition in which two copies
    of the same angular role complete one straight whole;

C3. search for another global metric relation whose completion propagates
    into the angular register;

C4. search for a second symmetry carrier/partition whose fixed-point condition
    forces the angular role swap to stabilize.
```

These are **construction-search prompts**, not accepted geometric facts.

The Validator requires a separate proof/construction certificate before any candidate can set `A = EQ` in a concrete instance.

---

# 11. Important negative result

The system does **not** conclude:

```text
local triangle zero + local triangle zero + congruence
    -> composite global zero
```

That inference is rejected.

What is actually licensed is:

```text
local triangle zeros
+ pair congruence
+ shared hinge
    -> recomposed host with global metric zero
    -> expose independent angular axis
    -> identify a candidate angular fixed point
```

This negative result is theoretically important because it shows that the multi-agent architecture can preserve incompleteness rather than over-completing toward a desired symmetric answer.

---

# 12. Compiler Agent — discover `ZERO_LOCUS` as a reusable object

Across Runs 06–09 the Compiler now sees several recurring structures:

```text
triangle family:
    one central zero state

four-edge family:
    metric zero locus
    angular zero locus
    possible intersection of loci

recomposition:
    local zeros may induce one global zero locus while leaving others free
```

It proposes a reusable schema:

```text
ZeroLocus {
    id
    host_family
    constrained_registers
    free_registers
    fixed_point_symmetries
    origin
    certification_status
    intersections_with_other_zero_loci
}
```

and upgrades:

```text
ZERO_STRUCTURE
```

to explicitly contain a set of `ZeroLocus` objects rather than a flat list of zero conditions.

This is a useful architectural improvement.

---

# 13. New distinction: centrality vs actuality

Run 09 forces the network to distinguish:

```text
CENTRALITY
    a state is structurally privileged in a family

ACTUALITY
    the current concrete construction is certified to instantiate that state
```

Therefore:

```text
CENTRAL_MEMBER_CANDIDATE != CURRENT_MEMBER_STATE
```

This distinction should become a core safety invariant for future creative runs.

It prevents symmetry discovery from silently becoming theorem assertion.

---

# 14. Network delta

Before Run 09:

```text
RECOMPOSE_ZERO
    provisional inverse of PROJECT_ZERO

composite host in Run 08
    obtained with an explicit extra angular condition
```

After Run 09:

```text
+ RECOMPOSE_GESTALTS
+ strongest-host-first policy
+ EXPOSE_FREE_REGISTERS
+ SEARCH_ZERO_LOCI
+ FREE_ANGULAR_AXIS_CANDIDATE
+ ANGULAR_CENTRAL_INVARIANT_CANDIDATE
+ F_METRIC_ZERO_FOUR_EDGE
+ ZERO_LOCUS schema
+ distinction CENTRALITY != ACTUALITY
+ explicit negative result against automatic composite-zero completion
```

---

# 15. Human semantic interpretation after the blind run

Only after the structural analysis may the semantic layer observe:

```text
A four-edge closed host with all boundary sides equal
corresponds to the classical rhombus family.
```

The discovered free angular axis is exactly the familiar acute/equal/obtuse variation within that family.

Its central equality member is the additional condition that would produce the square case.

But the significant result is that the agents reached this organization **without being given those names or the extra angular condition**.

The network therefore recovers:

```text
ONE-ZERO FAMILY
    -> discover second independent axis
    -> discover central fixed member on that axis
    -> propose but do not assert a composite-zero state
```

---

# 16. Research interpretation

Run 09 strengthens three hypotheses.

First:

```text
A strong Gestalt completion should expose both what is determined
and what remains free.
```

Second:

```text
Disanalogy is not only a way to move away from a zero;
it is a method for discovering the dimensionality of the family itself.
```

Third:

```text
A cognitively powerful reasoner should be able to discover a privileged
state before it has evidence that the current object instantiates it.
```

This is a useful model of mathematical conjecture:

```text
structure suggests a canonical possibility;
proof/construction decides actuality.
```

---

# 17. Next experiment suggested by the network

The natural next run is no longer simply "force the square".

A stronger experiment is:

```text
Take F_METRIC_ZERO_FOUR_EDGE with its free angular axis.
Inject several independent candidate constraints one at a time,
without naming their expected geometric effect.

Ask the agents which constraints:
    - collapse the same angular zero locus;
    - create genuinely different zero loci;
    - are redundant consequences of others;
    - reveal new host families.
```

Candidate injections could include, separately:

```text
- equality of adjacent angular roles;
- equality of the two diagonals;
- a diagonal-bisection relation;
- a perpendicularity relation;
- a second-axis symmetry condition.
```

The important question would be whether apparently different local constraints are discovered to be **multiple access masks to one deeper zero state**, in the same way SAS/ASA/SSS became multiple access masks to congruence.

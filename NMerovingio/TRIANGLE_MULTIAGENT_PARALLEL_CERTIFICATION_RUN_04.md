# Triangle Multi-Agent Parallel Certification — Run 04

> Controlled dry run under `MEROVINGIO_COGNITIVE_ARCHITECTURE_V03.md`.
>
> Input: the reorganized network produced by Run 03 plus proposition-level capabilities corresponding to Euclid I.27 and I.28.
>
> Goal: test what changes when selected **distributed angular patterns can now certify parallelism**, while the converse direction (I.29: parallels -> angle equalities / same-side supplementarity) remains hidden.
>
> This run is intentionally asymmetric. It asks whether a new Gestalt can become a valid **host/readout** before the reverse completion route exists.

---

# 0. Hidden-target discipline

The agents are not told to discover:

```text
ASA_IS_A_PARALLEL_GESTALT
SAS_IS_A_PARALLELOGRAM_GESTALT
PARALLELISM_IS_DISTRIBUTED_CONGRUENCE
TRIANGLE_PARALLEL_ISOMORPHISM
I.29_CONVERSE_CYCLE
```

They may use only:

```text
N3 from Run 03
+ I27-like certification
+ I28-like certification
```

The following remain unavailable:

```text
PARALLEL -> ALTERNATE_ANGLES_EQUAL
PARALLEL -> CORRESPONDING_ANGLES_EQUAL
PARALLEL -> SAME_SIDE_INTERIOR_STRAIGHT_COMPLETION
```

Those belong to the later I.29 injection.

---

# 1. Frozen input network N3

The network already contains:

```text
F_TRIANGLE_RELATION
    stable diagonal states:
        (LT,LT), (EQ,EQ), (GT,GT)
    central invariant state:
        (EQ,EQ)

F_CORRESPONDENCE_COMPLETION
    INTERNAL realization
    EXTERNAL_OVERLAY realization
    SAS / ASA / SSS access masks

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

F_DISTRIBUTED_SUPPLEMENT
    (LT,GT), (EQ,EQ), (GT,LT)

F_RELATION_TRANSDUCER
    PRESERVE_SIGN instance: triangle side-angle family
    REVERSE_SIGN instance: distributed supplement family
```

The distributed transversal packet can align angular roles across two intersections, but it cannot yet conclude parallelism from that alignment alone.

---

# 2. Injected proposition modules

## 2.1 I27-like certification

A continuous transversal `t` crosses two carrier lines `g1`, `g2`.

If an alternate-angle role pair is equal:

```text
ALT_EQ:
    alpha_P = alpha_Q
```

then the carrier lines are certified parallel:

```text
I27_CERTIFY:
    ALT_EQ
        -> PARALLEL(g1,g2)
```

The proof certificate is allowed to use the previously available triangle/exterior-angle capability (I.16-like contradiction under finite closure), but the cognitive layer stores only the certified result plus provenance.

## 2.2 I28-like certification

Two additional entry signatures may certify the same parallel readout:

```text
EXTERIOR_INTERIOR_EQ:
    exterior_angle_at_P = opposite_interior_angle_at_Q
        -> PARALLEL(g1,g2)

SAME_SIDE_STRAIGHT:
    interior_angle_at_P + interior_angle_at_Q = STRAIGHT
        -> PARALLEL(g1,g2)
```

Thus `PARALLEL(g1,g2)` becomes a common readout reachable by multiple distributed angular masks.

---

# 3. First cognitive event: parallelism appears as a multi-mask completion state

The Completion Agent observes:

```text
ALT_EQ --------------------\
EXTERIOR_INTERIOR_EQ -------+--> PARALLEL
SAME_SIDE_STRAIGHT --------/
```

This strongly resembles the already-known organization of pair congruence:

```text
SAS --\
ASA ---+--> FULL_PAIR_COINCIDENCE
SSS --/
```

However the agent is forbidden from collapsing the two concepts.

It reports only:

```text
MULTIPLE LOCAL/DISTRIBUTED MASKS
    -> ONE GLOBAL READOUT
```

and creates:

```text
PARALLEL_ACCESS_PACKET {
    alternate_equality_mask
    exterior_interior_equality_mask
    same_side_straight_mask
    common_readout = PARALLEL
}
```

Status: `COMPILED COGNITIVE PACKET`.

---

# 4. Genealogy Agent: why do congruence and parallelism now look related?

The Genealogy Agent decomposes both common-readout structures.

## 4.1 Pair congruence

```text
partial cross-object constraints
    -> validated overlay completion
    -> zero placement mismatch
    -> FULL_PAIR_COINCIDENCE
```

## 4.2 Parallel certification

```text
distributed angular constraints
    -> test possible finite closure of carrier lines
    -> closure leads to contradiction
    -> reject finite intersection
    -> PARALLEL
```

The agent finds a crucial distinction:

```text
CONGRUENCE:
    completion succeeds by COLLAPSE / OVERLAY

PARALLELISM:
    completion succeeds by REJECTING a candidate COLLAPSE / CLOSURE
```

Therefore the commonality is not `same object` or `same theorem shape`.

It is deeper:

```text
local constraints determine the admissible global organization of a workspace.
```

The agent proposes a neutral schema:

```text
GLOBAL_ORGANIZATION_READOUT {
    local_or_distributed_constraints
    candidate_global_organizations
    completion_test
    rejected_organizations
    stabilized_global_readout
}
```

Status: `COGNITIVE_CANDIDATE`.

---

# 5. Reorganization Agent: introduce closure topology

The Reorganization Agent notices that Run 03's `ROLE_TOPOLOGY` still does not express the most important new distinction.

Two carrier lines crossed by one transversal admit a possible future organization:

```text
FINITE_CLOSURE:
    extend g1 and g2 -> they meet -> triangle closes
```

I.27/I.28 eliminate that possibility under certain angular masks.

The agent therefore proposes a new register:

```text
CLOSURE_TOPOLOGY = {
    COINCIDENT,
    FINITE_CLOSURE,
    DISTRIBUTED_NONCLOSURE,
    UNKNOWN
}
```

Interpretation:

```text
COINCIDENT
    two role domains collapse/overlay

FINITE_CLOSURE
    separated carriers converge to a finite common vertex

DISTRIBUTED_NONCLOSURE
    carriers remain separated under the licensed parallel readout
```

This does not redefine Euclidean parallelism as a numeric distance relation. It records how the construction is organized for reasoning.

High-value refactor proposal:

```text
RELATIONAL PACKETS should track both:
    ROLE_TOPOLOGY
    CLOSURE_TOPOLOGY
```

---

# 6. Parallelism as a zero-residue state — but zero of what?

The agents test several possible zero interpretations.

## 6.1 Rejected proposal: zero placement

```text
PARALLEL = placement zero
```

Rejected because parallel lines are spatially distinct.

## 6.2 Rejected proposal: generic angle equality zero

```text
PARALLEL = angle equality
```

Rejected because I.28 also certifies parallelism via straight-completion masks, not only equality masks.

## 6.3 Better proposal: closure-conflict zero / directional compatibility

The common feature of the certified masks is that they make the `FINITE_CLOSURE` hypothesis incompatible with the active angular packet.

Provisional representation:

```text
PARALLEL_STATE {
    role_topology = DISTRIBUTED_CARRIER
    finite_closure = REJECTED
    directional_residue_under_distribution = ZERO_CANDIDATE
}
```

`directional_residue = ZERO_CANDIDATE` is cognitive, not a Euclidean theorem primitive.

The safer certified readout remains:

```text
PARALLEL(g1,g2)
```

while the zero interpretation remains a family-level hypothesis.

---

# 7. The key counterfactual: parallelism is generated through a triangle that must fail

The Genealogy Agent reconstructs the I.27-style proof path instead of storing only the final theorem.

Given:

```text
alternate angles equal
```

suppose:

```text
NOT parallel
```

and extend the two carriers toward a candidate intersection `C`.

Then the configuration becomes:

```text
        C
       / \
      /   \
     P-----Q
       transversal
```

which activates the triangle/exterior-angle network.

The previously compiled cross-vertex order capability gives a strict inequality incompatible with the hypothesized distributed equality.

Schematic cognitive trace:

```text
DISTRIBUTED ANGULAR ZERO
        |
        | hypothesize finite closure
        v
TRIANGLE HOST
        |
        | exterior-angle / cross-vertex order
        v
STRICT ANGULAR DISANALOGY
        |
        X collision with equality mask

=> reject finite closure
=> stabilize PARALLEL readout
```

This is the strongest event of Run 04.

Parallelism is not merely adjacent to triangle reasoning.
Its certification **temporarily enters the triangle Gestalt and exits by rejecting the triangle closure**.

---

# 8. New multi-Gestalt object: the same construction belongs to triangle and parallel reasoning in different counterfactual states

The Reorganization Agent refuses to represent:

```text
TRIANGLE --- analogy --- PARALLEL
```

Instead it introduces a shared constructive workspace:

```text
W_TWO_CARRIERS_TRANSVERSAL {
    carrier_1
    carrier_2
    transversal
    two intersection packets
    possible extension toward closure
}
```

Two important readings are now available:

```text
G_DISTRIBUTED
    carriers remain at separate sites
    angular packet read distributively

G_TRIANGULAR_CLOSURE
    extend carriers to a common finite vertex
    triangle packet becomes active
```

Parallel certification is represented as:

```text
active distributed constraints
    -> counterfactual switch to G_TRIANGULAR_CLOSURE
    -> collision
    -> return to G_DISTRIBUTED
    -> compile PARALLEL
```

Thus triangle and parallel are different partializations / states of one constructive workspace, not two external conceptual universes.

---

# 9. Rebase is now genuinely bidirectional

The network learns two construction-level moves.

## 9.1 DISTRIBUTED -> TRIANGLE rebase

```text
EXTEND_CARRIERS_TO_CLOSURE
```

If a finite closure is admitted, the transversal configuration rebases into a triangle host.

## 9.2 TRIANGLE -> DISTRIBUTED rebase

Given a triangle, extend/reinterpret two sides as carriers and treat the opposite side (or an auxiliary line) as a transversal packet.

Provisional cognitive operation:

```text
OPEN_TRIANGLE_CLOSURE
```

This does not automatically produce parallels.
It creates a distributed-carrier workspace in which parallel certification may later be tested.

The network therefore gains:

```text
TRIANGLE
    <->
DISTRIBUTED TWO-CARRIER WORKSPACE
```

as a rebase route with different closure states.

---

# 10. ASA probe

Now test the banalized ASA pair:

```text
T1:
    angle_A
    carrier_side s
    angle_B

T2:
    angle_A' = angle_A
    carrier_side s' = s
    angle_B' = angle_B
```

The Host Search Agent asks whether the two angle equalities can instantiate I.27/I.28 access masks after a suitable distributed embedding.

## 10.1 First angular pair

By placing corresponding side/ray roles into a common transversal workspace, one angular equality can certify:

```text
carrier_family_1_parallel
```

provided the role map realizes an allowed alternate/exterior-interior mask.

## 10.2 Second angular pair

The second ASA equality can independently certify:

```text
carrier_family_2_parallel
```

again after validated construction of the correct distributed roles.

## 10.3 Metric carrier

The equal included/carrier side does not certify parallelism.
It preserves a metric correspondence between the two local triangle realizations.

Thus the Host Search Agent proposes:

```text
ASA_PAIR
    -> candidate embedding in a TWO-DIRECTION DISTRIBUTED HOST

angle equality 1 -> parallel class 1
angle equality 2 -> parallel class 2
side equality    -> metric carrier match
```

After geometric validation, status becomes:

```text
ASA_PARALLEL_HOST = CONDITIONALLY_VALIDATED MEMBER
```

with an important qualifier:

```text
membership is established by using ASA's own angular data to certify the host.
The host does NOT yet regenerate those angle equalities, because I.29 is unavailable.
```

This creates a one-way cognitive relation:

```text
ASA data
    -> construct/certify distributed parallel host
```

but not yet:

```text
parallel host
    -> recover ASA angular data
```

---

# 11. Why this is already a real backward enrichment of ASA

Before Run 04, ASA was stored as:

```text
angle EQ
side EQ
angle EQ
    -> congruence
```

After Run 04 it gains a second validated reading:

```text
angle EQ
    -> possible parallel-direction certification

side EQ
    -> metric carrier correspondence

angle EQ
    -> second parallel-direction certification
```

Therefore ASA can now be read as:

```text
LOCAL PAIR VIEW:
    minimal congruence mask

DISTRIBUTED HOST VIEW:
    two direction-class certifications
    + one metric carrier match
```

This is a genuine `BACKWARD_ENRICH` event.

No new theorem was added to ASA itself.
Its **inferential role** changed because a new host family became available.

---

# 12. Does ASA now "become" the parallel Gestalt?

No.

The Reorganization Agent rejects:

```text
ASA = PARALLELISM
```

and also rejects:

```text
ASA is merely analogous to parallelism
```

The stronger representation is:

```text
one material construction may simultaneously instantiate:
    G_ASA_PAIR
    G_CONGRUENCE
    G_TWO_DIRECTION_PARALLEL_HOST
```

These Gestalten overlap over shared elements but partialize them differently.

This is stored as:

```text
GESTALT_OVERLAP
SHARED_REALIZATION
CO_CONSTITUTION_CANDIDATE
```

rather than an analogy edge.

---

# 13. SAS probe

Now test SAS:

```text
side_1 EQ
side_2 EQ
included_angle EQ
```

One included-angle equality may, under a suitable distributed realization, certify **one** parallel/direction class.

But Run 04 cannot generally obtain the second direction class from the two side equalities alone using only I.27/I.28.

Therefore:

```text
SAS_DISTRIBUTED_HOST
    = PARTIALLY_EMBEDDABLE
```

Current readout:

```text
included-angle EQ
    -> one possible parallel certification

side equalities
    -> metric anchors

missing:
    independent angular mask for second direction class
```

The network records a strong open impetus:

```text
Can a later parallel-to-angle completion rule transform
one certified direction class + metric anchors
into the richer translation/parallelogram host?
```

This question is deliberately deferred to I.29 / later parallelogram experiments.

---

# 14. SSS probe

SSS contains no explicit angular equality mask.

Without first compiling congruence and projecting angular equalities, I.27/I.28 cannot directly host SSS in the distributed parallel network.

Two routes are distinguished:

```text
DIRECT HOST:
    unavailable at this stage

INDIRECT ROUTE:
    SSS
      -> FULL_PAIR_COINCIDENCE
      -> angular readouts from congruence
      -> possible distributed embedding
      -> parallel certification
```

The second route is cognitively longer and has different genealogy.

This reinforces:

```text
STATE_IDENTITY != GENETIC_IDENTITY
```

Even if ASA- and SSS-derived constructions later reach the same parallel host, the network must retain their different access paths.

---

# 15. Strong analogy event and Reorganization Agent verdict

The network now sees two major packets:

```text
PAIR CONGRUENCE
    several local masks
        -> global coincidence/overlay state

PARALLEL CERTIFICATION
    several distributed angular masks
        -> global nonclosure/direction state
```

A weak architecture would add:

```text
CONGRUENCE ~ PARALLEL
```

The Reorganization Agent instead asks what both instantiate.

Candidate deeper organization:

```text
F_GLOBAL_CONSTRAINT_COMPLETION {
    workspace
    role_topology
    closure_topology

    local_or_distributed_masks
    candidate_global_states

    counterfactual_tests
    eliminated_global_states
    stabilized_readout

    projection_routes
    rebase_routes
}
```

Instances:

```text
CONGRUENCE:
    role_topology = EXTERNAL_OVERLAY
    preferred closure = COINCIDENT
    residual placement -> ZERO

PARALLEL CERTIFICATION:
    role_topology = DISTRIBUTED_CARRIER
    finite triangular closure -> ELIMINATED
    stabilized closure = DISTRIBUTED_NONCLOSURE
```

This is proposed as a **network refactor**, not as an analogy label.

---

# 16. Completion Agent vs Reorganization Agent — useful disagreement

The Completion Agent prefers to retain:

```text
F_CORRESPONDENCE_COMPLETION
F_PARALLEL_ACCESS_PACKET
```

as separate reusable packets because they have different proof behavior.

The Reorganization Agent proposes placing both under:

```text
F_GLOBAL_CONSTRAINT_COMPLETION
```

The Validator accepts the hierarchy but preserves the branch distinction.

Committed organization:

```text
F_GLOBAL_CONSTRAINT_COMPLETION
│
├── F_CORRESPONDENCE_COMPLETION
│   ├── INTERNAL triangle zero
│   └── EXTERNAL_OVERLAY pair congruence
│
└── F_DISTRIBUTED_NONCLOSURE
    ├── I27 equality mask
    ├── I28 equality mask
    └── I28 straight-completion mask
```

This is a good example of multi-agent architecture preventing both over-fragmentation and over-merging.

---

# 17. New impetus objects generated by Run 04

```text
CYCLE_CLOSURE_IMPETUS
    parallelism has been certified from angles,
    but cannot yet regenerate the angle packet

ASA_HOST_IMPETUS
    ASA now belongs to a validated distributed host,
    but the host relation is one-way

SAS_TRANSLATION_IMPETUS
    SAS supplies one angular direction class + metric anchors;
    ask whether a later rule completes a second class

TRIANGLE_PARALLEL_GENEALOGY_IMPETUS
    parallel certification explicitly enters a triangle counterfactual;
    investigate whether triangle and parallel are closure states of one family

COMPRESSION_IMPETUS
    several masks now terminate in PARALLEL just as several masks terminate in CONGRUENCE
```

These are routed forward rather than prematurely solved.

---

# 18. Network delta N3 -> N4

```text
ADDED:
    PARALLEL_ACCESS_PACKET
    PARALLEL certified readout
    CLOSURE_TOPOLOGY
    G_DISTRIBUTED
    G_TRIANGULAR_CLOSURE
    EXTEND_CARRIERS_TO_CLOSURE
    OPEN_TRIANGLE_CLOSURE

ADDED/ENRICHED:
    ASA_PARALLEL_HOST = conditionally validated member
    SAS_DISTRIBUTED_HOST = partially embeddable
    SSS indirect host route

PROPOSED AND ACCEPTED:
    F_GLOBAL_CONSTRAINT_COMPLETION

PRESERVED:
    F_CORRESPONDENCE_COMPLETION
    F_RELATIONAL_COMPLETION_FIELD
    F_RELATION_TRANSDUCER

STILL OPEN:
    PARALLEL -> angle completion
    full cognitive cycle around parallelism
    SAS -> two-direction translation/parallelogram host
    square/parallelogram zero family
```

---

# 19. Main result

Run 04 does not discover that "triangles are analogous to parallels".

It discovers something structurally stronger:

```text
one distributed two-carrier workspace
can be read in two counterfactual organizations:

1. finite triangular closure
2. distributed nonclosure
```

and the I.27/I.28 angular masks determine which organization survives.

Hence parallelism is compiled through a reasoning cycle of the form:

```text
DISTRIBUTED PATTERN
    -> hypothesize TRIANGLE CLOSURE
    -> activate triangle Gestalt
    -> derive collision
    -> reject closure
    -> return to distributed Gestalt
    -> compile PARALLEL
```

The triangle network is therefore not merely useful to prove a theorem about parallels.
It is part of the **genealogy of the parallel Gestalt itself** in this network.

---

# 20. Immediate next experiment

Inject only I.29-like reverse completion:

```text
PARALLEL
    -> alternate-angle equality
    -> corresponding/exterior-interior equality
    -> same-side interior straight completion
```

Then test whether the one-way structure discovered here closes into:

```text
ANGLE PATTERN
    -> PARALLEL HOST
    -> ANGLE PACKET COMPLETION
    -> PROJECT BACK
    -> ENRICH OLD TRIANGLE/CONGRUENCE GESTALT
    -> EVOKE PARALLEL CONSTRUCTION
```

Key questions for Run 05:

```text
1. Does ASA become a genuine two-way host relation?
2. Does SAS acquire a second direction class and a translation/parallelogram interpretation?
3. Does PARALLEL become a stable zero of a distributed directional family?
4. Does the network discover a stronger common constructive organization beneath triangle closure and parallel nonclosure?
5. Does the new cycle shorten older proofs enough to trigger COMPILE?
```

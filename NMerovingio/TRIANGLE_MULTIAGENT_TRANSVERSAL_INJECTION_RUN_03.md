# Triangle Multi-Agent Transversal Injection — Run 03

> Controlled dry run under `MEROVINGIO_COGNITIVE_ARCHITECTURE_V03.md`.
>
> Goal: freeze the network produced by Run 02, inject a deliberately banalized line/intersection/transversal packet, and observe whether the multi-agent system merely adds links, creates a sister family, or refactors the deeper `F_CORRESPONDENCE_COMPLETION` structure.
>
> No parallelism theorem is available in this run. `PARALLEL`, `ALTERNATE_ANGLES_EQUAL`, `CORRESPONDING_ANGLES_EQUAL`, and any explicit triangle↔parallel mapping are hidden.

---

# 0. Hidden-target discipline

The agents are **not** told to discover:

```text
PARALLELISM
TRIANGLE_AS_PARALLEL_CLOSURE
ASA_AS_PARALLEL_GESTALT
CONGRUENCE_PARALLEL_HOMOLOGY
DISTRIBUTED_STRAIGHT_ANGLE_AS_PARALLEL
```

Nor are they told that the transversal should belong to the same family as triangle congruence.

The only question is:

```text
Does the new material force a better organization of the current network?
```

A successful run may therefore end in any of the following:

```text
A. ADD_EDGE
B. ADD_SISTER_FAMILY
C. ADD_SHARED_GENERATOR
D. REFACTOR_EXISTING_DEEP_FAMILY
E. NO_MAJOR_RESTRUCTURE
```

The preferred result is not predefined.

---

# 1. Frozen input network N2

Run 01 discovered an OBJECT-level triangle family:

```text
F_TRIANGLE_RELATION

stable states:
    (LT,LT)
    (EQ,EQ)
    (GT,GT)

central invariant member:
    O0 = (EQ,EQ)
```

Run 02 then discovered a deeper cross-level organization:

```text
F_CORRESPONDENCE_COMPLETION

internal realization:
    one object
    left/right role correspondence
    O0 as correspondence-complete state

external realization:
    two objects
    cross-object role correspondence
    FULL_PAIR_COINCIDENCE

access masks:
    SAS
    ASA
    SSS
```

A key result of Run 02 was that the difference between internal and external realizations could be expressed by:

```text
DOMAIN_SEPARATION = INTERNAL | EXTERNAL
```

and by two candidate transformations discovered by the agents:

```text
IDENTIFY_ROLE_DOMAINS
SEPARATE_ROLE_DOMAINS
```

The network currently privileges **equality correspondence** as the deep connective material.

That assumption is now placed under stress.

---

# 2. Banalized injected packet T_raw

The injected network contains only material and proposition-level structures.

## 2.1 One straight line

```text
LINE_CONTINUITY
OPPOSITE_RAYS
STRAIGHT_ANGLE
ANGLE_ADJACENCY
```

A pair of adjacent angular parts may occupy one straight whole:

```text
alpha + beta -> STRAIGHT
```

No higher-level `STRAIGHT_COMPLETION_GESTALT` label is initially supplied.

## 2.2 One local intersection

Two continuous lines cross at `O`.

```text
q1 q2 q3 q4
```

Raw facts licensed propositionally:

```text
q1 + q2 -> STRAIGHT
q2 + q3 -> STRAIGHT
q3 + q4 -> STRAIGHT
q4 + q1 -> STRAIGHT

q1 = q3
q2 = q4
```

No `VERTICAL_OPPOSITION_GESTALT` is precompiled.

## 2.3 Two intersections on one continuous transversal

```text
      g1
-------P-------
        \
         \  t
          \
-------Q-------
      g2
```

Raw material facts:

```text
P != Q
P,Q lie on the same continuous line t
P = intersection(t,g1)
Q = intersection(t,g2)
```

Each intersection has a four-angle packet.

No relation between `g1` and `g2` is assumed.
No cross-intersection angle equality is supplied.

---

# 3. Initial tension after injection

The Generic Reasoner sees that N2 and T_raw both contain repeated structures involving:

```text
roles
carriers
partial relations
completion of further relations
zero/nonzero residual possibilities
```

but there is an immediate mismatch.

N2's deep family is currently organized around:

```text
ROLE CORRESPONDENCE + EQUALITY
```

while the transversal already offers something weaker:

```text
ROLE ALIGNMENT WITHOUT EQUALITY
```

because positions at P and Q can be assigned corresponding roles by the shared transversal even though their angle magnitudes remain unknown.

This produces a strong:

```text
REORGANIZATION_IMPETUS
```

and a secondary:

```text
GENEALOGICAL_IMPETUS
```

The key diagnostic question is:

```text
Did Run 02 mistakenly fuse ROLE-MAPPING and EQUALITY into one primitive notion?
```

---

# 4. Completion Agent — compress the local intersection first

The Completion Agent does not search for analogies. It simply closes licensed local relations.

Given:

```text
q1 + q2 = STRAIGHT
q2 + q3 = STRAIGHT
```

it detects that `q1` and `q3` are alternative complements of the same part `q2` into the same whole.

The proposition-level equality:

```text
q1 = q3
```

can therefore be stored with a richer completion trace:

```text
q1 --\
      + q2 -> SAME STRAIGHT WHOLE
q3 --/

=> q1 = q3
```

Likewise:

```text
q2 = q4
```

The agent proposes a reusable candidate:

```text
COMMON_WHOLE_COMPLETION

part A + shared part C -> whole W
part B + shared part C -> whole W
--------------------------------
A and B occupy the same completion role relative to W and C
```

Status: `COGNITIVE_CANDIDATE`.

Important consequence:

```text
EQUALITY can be a READOUT of a completion structure,
not necessarily an input primitive of the structure.
```

This immediately places pressure on `F_CORRESPONDENCE_COMPLETION`, which had treated equality correspondence as the deep starting material.

---

# 5. Genealogy Agent — compare three ways equality appears

The Genealogy Agent decomposes three equality-producing situations already present in N2 + T_raw.

## 5.1 Triangle OBJECT equality

```text
O0:
SIDE_L = SIDE_R
ANGLE_L = ANGLE_R
```

Here equality is an internal correspondence packet.

## 5.2 Triangle PAIR equality

```text
FULL_PAIR_COINCIDENCE:
corresponding roles across T1/T2 match
```

Here equality is an external correspondence packet.

## 5.3 Intersection equality

```text
q1 = q3
q2 = q4
```

Here equality may be reconstructed as a **shared-whole completion readout** over one intersection workspace.

The agent therefore rejects the hypothesis:

```text
ALL IMPORTANT EQUALITY STRUCTURES SHARE ONE EQUALITY-FIRST GENERATOR
```

and proposes instead:

```text
some equalities are primitive/preserved correspondences;
some equalities are generated by a deeper completion organization.
```

This is the first clear deficiency detected in the Run-02 deep structure.

---

# 6. Expansion Agent — distribute one local packet over a continuous carrier

The Expansion Agent now uses the new material fact:

```text
P,Q lie on one continuous transversal t
```

It does **not** infer any angle equality.

Instead it constructs a role map:

```text
P_packet role 1 <-> Q_packet role 1
P_packet role 2 <-> Q_packet role 2
P_packet role 3 <-> Q_packet role 3
P_packet role 4 <-> Q_packet role 4
```

based on:

```text
orientation along t
side-of-t role
incoming/outgoing ray role
local vertical-opposite role
local straight-complement role
```

This creates a new object:

```text
DISTRIBUTED_ROLE_PACKET
```

whose defining property is:

```text
ROLE_ALIGNMENT = PRESENT
MAGNITUDE_EQUALITY = UNKNOWN
```

This is crucial.

The network can now represent:

```text
same inferential role
without
same metric/angular value
```

Run 02 did not need this distinction explicitly.

---

# 7. First major Reorganization Agent proposal

The Reorganization Agent receives two high-pressure signals:

```text
S1. equality can be generated by completion rather than presupposed;
S2. role correspondence can exist before equality is known.
```

It judges the Run-02 family:

```text
F_CORRESPONDENCE_COMPLETION
```

to be too compressed.

It proposes splitting its implicit primitive:

```text
CORRESPONDENCE
```

into at least three layers:

```text
ROLE_ALIGNMENT
RELATION_CONSTRAINT
COMPLETION_READOUT
```

Provisional deeper schema:

```text
RELATIONAL_PACKET {
    workspace
    role_domains
    role_map
    carriers

    relation_constraints
    whole_part_constraints
    residual_registers

    completion_rules
    readouts
}
```

Equality becomes one possible `RELATION_CONSTRAINT` or one possible `READOUT`, not the essence of the packet.

Status: `REFACTOR_NETWORK_PROPOSAL`.

---

# 8. Compiler Agent — identify three completion topologies

The Compiler Agent now sees three recurrent organization modes.

## 8.1 INTERNAL completion

```text
one material object
roles are related inside that object
```

Example:

```text
triangle central state O0
```

## 8.2 EXTERNAL completion

```text
two material objects
roles are aligned across object domains
completion tends toward overlay/coincidence
```

Example:

```text
triangle pair congruence
```

## 8.3 DISTRIBUTED completion

```text
roles live at distinct spatial sites
one continuous carrier gives them a shared genealogy/orientation
completion can propagate across packets without collapsing locations
```

Example:

```text
two intersections on one transversal
```

The agent proposes that `DOMAIN_SEPARATION` from Run 02 is insufficient.

Replace:

```text
DOMAIN_SEPARATION = INTERNAL | EXTERNAL
```

with a richer organization variable:

```text
ROLE_TOPOLOGY = {
    INTERNAL,
    EXTERNAL_OVERLAY,
    DISTRIBUTED_CARRIER
}
```

This is a concrete network upgrade caused by the transversal injection.

---

# 9. Disanalogy stress test on the new distributed topology

To test whether `DISTRIBUTED_CARRIER` is a genuine family mode rather than a descriptive label, the Expansion Agent injects two minimal breaks.

## 9.1 Break the transversal continuity

```text
BREAK(t continuity)
```

while preserving the two local intersection packets.

Result:

```text
local packets remain valid
cross-packet role alignment loses a shared carrier genealogy
DIRECTIONAL_RESIDUE != ZERO
```

This confirms that continuous carrier identity is structurally active.

## 9.2 Rotate only the second crossed carrier

Keep `t` continuous but vary `g2`.

Result:

```text
P packet unchanged
Q packet locally valid
cross-packet angular relation changes
role topology survives
magnitude correspondence changes
```

This cleanly separates:

```text
ROLE_ALIGNMENT
from
RELATION_VALUE
```

and strongly validates the proposed refactor.

---

# 10. Completion Agent discovers a distributed anti-diagonal family

Compress each local intersection into two supplementary angular roles:

```text
P = {alpha_P, beta_P}
Q = {alpha_Q, beta_Q}

alpha_P + beta_P = STRAIGHT
alpha_Q + beta_Q = STRAIGHT
```

Define:

```text
R_alpha = rel(alpha_P, alpha_Q)
R_beta  = rel(beta_P, beta_Q)
```

Then shared-whole completion produces the qualitative inverse relation:

```text
R_alpha = GT -> R_beta = LT
R_alpha = EQ -> R_beta = EQ
R_alpha = LT -> R_beta = GT
```

Stable family:

```text
F_DISTRIBUTED_SUPPLEMENT = {
    (LT,GT),
    (EQ,EQ),
    (GT,LT)
}
```

This is an **anti-diagonal** family.

The existing triangle family was:

```text
F_TRIANGLE_RELATION = {
    (LT,LT),
    (EQ,EQ),
    (GT,GT)
}
```

which is diagonal.

The agents therefore discover that the network now contains at least two distinct propagation grammars:

```text
ORDER_PRESERVING completion
ORDER_REVERSING completion
```

with a shared equality/equality middle state but different disanalogical neighborhoods.

This is not merged away.

---

# 11. Reorganization Agent — second, deeper refactor

The new comparison generates a strong analogy/commonality event:

```text
both families have:
    LT / EQ / GT variation
    a unique equality/equality central state
    oriented disanalogies
    converse propagation routes

but:
    one preserves order sign
    one reverses order sign
```

The Reorganization Agent asks whether adding an analogy edge is sufficient.

It rejects:

```text
F_TRIANGLE_RELATION ~ F_DISTRIBUTED_SUPPLEMENT
```

as too weak.

Instead it proposes a higher family of **relation transducers**:

```text
F_RELATION_TRANSDUCER {
    register_A
    register_B
    central_zero
    variation_axis
    propagation_signature
}
```

with:

```text
TRIANGLE instance:
    propagation_signature = PRESERVE_SIGN

TRANSVERSAL-SUPPLEMENT instance:
    propagation_signature = REVERSE_SIGN
```

Thus the new network does not erase differences. It explains them through a deeper parameterized organization.

Status: `HIGH_VALUE_REFACTOR_PROPOSAL`.

---

# 12. Genealogy Agent — does the transversal belong to F_CORRESPONDENCE_COMPLETION?

The answer is now nuanced.

The agent reports:

```text
NO:
    the transversal packet is not merely another equality-completion criterion.

YES AT A DEEPER LEVEL:
    triangle congruence and transversal packets both instantiate
    role organization + carrier + constraint + completion + readout.
```

It therefore proposes:

```text
F_RELATIONAL_COMPLETION_FIELD
```

above the Run-02 family.

Candidate organization:

```text
F_RELATIONAL_COMPLETION_FIELD
│
├── correspondence-completion branch
│   │
│   ├── INTERNAL realization
│   │      └── triangle O0 / self-role packet
│   │
│   └── EXTERNAL_OVERLAY realization
│          └── pair congruence
│                 ├── SAS
│                 ├── ASA
│                 └── SSS
│
├── whole-part completion branch
│   └── local straight/intersection packet
│
└── DISTRIBUTED_CARRIER branch
    └── two intersection packets on one transversal
```

The transversal therefore does **not** become a sibling criterion of congruence.

Instead it exposes that the previous deep family was itself only one partialization of a still deeper constructive field.

---

# 13. Backward enrichment of the triangle network

Once the refactor is accepted, several old triangle structures gain new interpretations.

## 13.1 Equality no longer has one cognitive status

The network can distinguish:

```text
PRESERVED_EQUALITY
    equality supplied/maintained as correspondence

COMPLETED_EQUALITY
    equality read out from a deeper completion structure
```

This distinction can later be used to compare I.5/I.6, congruence criteria, vertical angles, and parallel-angle theorems.

## 13.2 Carrier becomes first-class

The old triangle criteria had carriers implicitly:

```text
SAS: metric sides + angular hinge
ASA: angular roles + metric carrier
SSS: saturated metric packet
```

After transversal injection, the reasoner explicitly asks:

```text
what persists across separated sites?
what is the carrier of the correspondence?
```

This enriches SAS/ASA without asserting parallelism.

## 13.3 O0 gains a new interpretation

The central triangle state is still the internal equality fixed point.

But it is now also recognized as a special case of:

```text
zero residual inside a relation-transducer family
```

rather than being important only because of equality.

This makes the notion of `zero` more structural.

---

# 14. Does ASA become parallelism here?

No.

At Run 03 the system may discover:

```text
ASA has a role pattern that looks highly embeddable
in a future distributed-carrier workspace.
```

But without a theorem licensing a cross-intersection angle pattern as a parallel-direction class, the correct status is:

```text
ASA_DISTRIBUTED_HOST = EMBEDDABLE_CANDIDATE
```

not:

```text
ASA_DISTRIBUTED_HOST = VALIDATED_MEMBER
```

This negative result is important because it shows that the deeper refactor can happen **before** parallelism is available.

---

# 15. Does SAS change?

Yes, but differently.

The pair criterion:

```text
side_1 EQ
side_2 EQ
included_angle EQ
```

can now be decomposed into:

```text
2 metric correspondence anchors
+
1 angular packet match
```

If that angular match is embedded at two transversal sites, shared-whole completion can generate a second angular relation in the local packets.

Thus SAS gains a candidate distributed-host reading:

```text
SAS
-> metric anchors
+ distributed angular zero
```

but no `PARALLELOGRAM` or `PARALLEL` host is certified in this run.

---

# 16. Validator

The Validator separates four levels of claim.

## 16.1 Geometrically/propositionally licensed

```text
local straight completion
vertical-angle equality
continuous transversal incidence
local part/whole relations
```

## 16.2 Compiled cognitive structures supported by licensed facts

```text
COMMON_WHOLE_COMPLETION
DISTRIBUTED_ROLE_PACKET
F_DISTRIBUTED_SUPPLEMENT
```

## 16.3 Valid network refactors

```text
ROLE_ALIGNMENT != EQUALITY
ROLE_TOPOLOGY = INTERNAL | EXTERNAL_OVERLAY | DISTRIBUTED_CARRIER
F_RELATION_TRANSDUCER
F_RELATIONAL_COMPLETION_FIELD
```

These are cognitive organization claims, not Euclidean propositions.

## 16.4 Still open

```text
PARALLELISM
ASA -> PARALLEL HOST
SAS -> PARALLELOGRAM HOST
TRIANGLE/PARALLEL CLOSURE FAMILY
```

No theorem leakage detected.

---

# 17. Network delta N2 -> N3

Before injection:

```text
F_CORRESPONDENCE_COMPLETION
    INTERNAL
    EXTERNAL
```

After injection:

```text
F_RELATIONAL_COMPLETION_FIELD
│
├── CORRESPONDENCE_COMPLETION
│   ├── INTERNAL
│   └── EXTERNAL_OVERLAY
│
├── COMMON_WHOLE_COMPLETION
│
└── DISTRIBUTED_CARRIER_COMPLETION
```

Additional new structures:

```text
+ ROLE_ALIGNMENT separated from RELATION_VALUE
+ ROLE_TOPOLOGY
+ DISTRIBUTED_ROLE_PACKET
+ DIRECTIONAL_RESIDUE
+ F_DISTRIBUTED_SUPPLEMENT
+ F_RELATION_TRANSDUCER
+ PRESERVE_SIGN vs REVERSE_SIGN propagation signatures
+ richer CARRIER semantics
+ backward enrichment of SAS / ASA / O0
```

The result is therefore:

```text
RUN_03_OUTCOME = REFACTOR_EXISTING_DEEP_FAMILY
```

not merely `ADD_EDGE` or `ADD_SISTER_FAMILY`.

---

# 18. Why this matters

The experiment exposes a real deficiency in the Run-02 abstraction.

Run 02 had correctly discovered that internal triangle equality and pair congruence share a deeper correspondence structure.

Run 03 shows that this was still too concept-specific because it privileged **equality correspondence**.

The transversal forces the network to distinguish:

```text
role organization
from
relation value
from
completion mechanism
from
spatial topology of the roles
```

This is exactly the behavior expected from a strong analogy under the v0.3 architecture:

```text
new commonality
-> current abstraction becomes insufficient
-> Reorganization Agent detects failure
-> deeper factorization proposed
-> old concepts survive as partializations
```

The network is not merely growing. It is changing its own ontology.

---

# 19. The new deepest provisional schema

After Run 03, the most abstract reusable object is provisionally:

```text
RELATIONAL_COMPLETION_FIELD {
    workspace

    role_topology
    role_alignment
    carriers

    relation_registers
    relation_constraints
    whole_part_constraints

    variation_axes
    residual_registers

    completion_rules
    propagation_signature
    readouts

    partializations
    genealogies
}
```

Possible current instances:

```text
triangle-order family
triangle congruence family
local intersection completion
transversal distributed supplement family
```

No claim is made that this schema is final.

Its purpose is to be broken by the next strong construction.

---

# 20. Next blind pressure test

Freeze N3.

Then inject only the proposition-level conditions analogous to Euclid I.27/I.28 that can certify a parallel relation from a distributed angular pattern.

Do **not** inject I.29 yet.

Ask the agents:

```text
1. Does PARALLELISM appear as a new concept, a new family, or a compiled zero of DISTRIBUTED_CARRIER completion?
2. Does the parallel zero share a structural role with pair coincidence zero and triangle O0?
3. Does ASA move from EMBEDDABLE_CANDIDATE to validated host membership?
4. Does the new parallel Gestalt retroactively simplify any triangle or congruence paths?
5. Does the network discover a meaningful closure/non-closure relation between triangles and parallel configurations without being told to look for it?
6. Does the Reorganization Agent refactor again, or is N3 now deep enough to absorb parallelism without ontological change?
```

That is the next genuine test of the architecture.
# Triangle Multi-Agent Zero Discovery — Run 02

> Cross-level conceptual/dry run under `MEROVINGIO_COGNITIVE_ARCHITECTURE_V03.md`.
>
> Goal: start from the OBJECT-level family discovered in Run 01 plus three still-banalized PAIR-level congruence criteria, then ask whether the multi-agent system reorganizes the network toward a deeper shared constructive structure **without preloading** `INTERNALIZED_CONGRUENCE`, `SELF_CONGRUENCE`, `EXTERNALIZE`, `PAIR_ZERO`, or any explicit mapping from the isosceles state to triangle congruence.
>
> This is not an autonomous software execution. It is a controlled dry-run specification whose steps can later be replayed blindly by implemented agents.

---

# 0. Hidden target rule

The agents may use only the structures already available after Run 01 plus raw pair-congruence facts.

The following labels/claims are hidden from the agents:

```text
INTERNALIZED_CONGRUENCE
SELF_CONGRUENCE
ISOSCELES_AS_CONGRUENCE
EXTERNALIZE_ISOSCELES
PAIR_ZERO
OBJECT_ZERO_EQUALS_PAIR_ZERO
SAS_AS_EXTERNALIZED_SIDE_EQUALITY
ASA_AS_EXTERNALIZED_ANGLE_EQUALITY
```

The run succeeds if the system independently proposes a cross-level reorganization with the following structural content, regardless of vocabulary:

```text
1. the OBJECT equality/equality state is a self-correspondence fixed point;
2. PAIR congruence is a global correspondence-completion state;
3. both can be expressed through one deeper correspondence schema;
4. the OBJECT state can be obtained by collapsing/internalizing paired roles;
5. PAIR criteria can be read as different ways of externalizing/unfolding correspondences present in the OBJECT state;
6. the network should be refactored rather than merely linked by an ANALOGY edge.
```

---

# 1. Input network N1

Run 01 has already compiled the OBJECT family:

```text
F_TRIANGLE_RELATION

registers:
    SideRel
    OppositeAngleRel

stable_region:
    (LT,LT)
    (EQ,EQ)
    (GT,GT)

symmetry:
    sigma(LT,LT) = (GT,GT)
    sigma(GT,GT) = (LT,LT)
    sigma(EQ,EQ) = (EQ,EQ)

central invariant member:
    O0 = (EQ,EQ)
```

Human-facing interpretation is withheld from the agents. They know only that `O0` is the unique member fixed by left/right role reversal and that both active disanalogy registers vanish there.

The PAIR graph remains deliberately banalized:

```text
PAIR_SAS_RAW
    side_1 EQ
    side_2 EQ
    included_angle EQ
        -> FULL_PAIR_COINCIDENCE

PAIR_SSS_RAW
    side_1 EQ
    side_2 EQ
    side_3 EQ
        -> FULL_PAIR_COINCIDENCE

PAIR_ASA_RAW
    angle_1 EQ
    carrier_side EQ
    angle_2 EQ
        -> FULL_PAIR_COINCIDENCE
```

No family relation among the criteria is predeclared except that all three terminate in the same `FULL_PAIR_COINCIDENCE` readout.

---

# 2. Initial cross-level tension

The Generic Reasoner notices four facts that were previously stored in unrelated graph regions:

```text
A. OBJECT O0 contains two simultaneous equality correspondences:
       SideRel = EQ
       OppositeAngleRel = EQ

B. O0 is fixed under LEFT <-> RIGHT role reversal.

C. PAIR SAS / SSS / ASA are different partial equality masks that all complete to the same global pair state.

D. both OBJECT and PAIR networks repeatedly use the operation:
       partial correspondence -> completion of further correspondence.
```

This does not yet imply a common family.

It generates:

```text
GENEALOGICAL_IMPETUS
REORGANIZATION_IMPETUS
COMPLETION_IMPETUS
EXPANSION_IMPETUS
```

and a weak high-level commonality event:

```text
COMMONALITY_CANDIDATE:
    "equality-correspondence structure appears at two organizational levels"
```

The event is explicitly not stored as an analogy edge yet.

---

# 3. Genealogy Agent — DECOMPILE both sides

The Genealogy Agent is asked:

```text
WHY do O0 and FULL_PAIR_COINCIDENCE both look correspondence-complete?
```

It runs:

```text
DECOMPILE(O0)
DECOMPILE(FULL_PAIR_COINCIDENCE)
```

## 3.1 Decompile O0

The agent recovers the active role structure:

```text
one triangle T

SIDE_L  <-> SIDE_R
ANGLE_L <-> ANGLE_R

SideRel  = EQ
AngleRel = EQ

sigma:
    LEFT <-> RIGHT
```

It notices that `sigma` acts **inside the same material object**.

Provisional description:

```text
O0 = one object carrying a complete left/right self-correspondence packet.
```

No use of the term `self-congruence` is allowed.

## 3.2 Decompile pair coincidence

The agent recovers:

```text
two triangle objects T1, T2

roles in T1 <-> corresponding roles in T2

FULL_PAIR_COINCIDENCE means:
    all licensed corresponding side roles match
    all licensed corresponding angle roles match
    placement under the active overlay is zero
```

Provisional description:

```text
PAIR_ZERO = two objects carrying a complete cross-object correspondence packet.
```

The label `PAIR_ZERO` is generated here only as an internal placeholder after discovering common termination; it was not supplied as a target concept.

---

# 4. First deep commonality: correspondence topology

The Genealogy Agent compares the two decompositions.

It detects that the principal difference is **where the paired roles live**:

```text
O0:
    role_a(T) <-> role_b(T)
    correspondence is INTERNAL to one object

PAIR_ZERO:
    role_a(T1) <-> role_a(T2)
    correspondence is EXTERNAL across two objects
```

The local relation type is otherwise structurally similar:

```text
equality
role matching
completion packet
zero residual mismatch
```

The agent proposes a deeper neutral schema:

```text
CORRESPONDENCE_PACKET {
    role_domain_A
    role_domain_B
    role_mapping
    equality_constraints
    completion_rules
    residual_registers
}
```

with one variable:

```text
DOMAIN_SEPARATION = INTERNAL | EXTERNAL
```

Status: `COGNITIVE_CANDIDATE`.

This is the first important event of Run 02: the system does not add an `O0 ~ PAIR_ZERO` analogy edge. It proposes a deeper generator in which both are realizations.

---

# 5. Reorganization Agent — test whether the current ontology is too coarse

Current graph:

```text
OBJECT FAMILY                         PAIR CRITERIA

F_TRIANGLE_RELATION                   SAS
       |                              SSS
       O0                             ASA
                                       \
                                        -> FULL_PAIR_COINCIDENCE
```

The Reorganization Agent asks whether adding a simple edge:

```text
O0 --- similar_to --- FULL_PAIR_COINCIDENCE
```

would explain the repeated structure.

It rejects this as low explanatory gain because it does not explain:

```text
- why O0 is swap-invariant;
- why pair criteria are alternative masks;
- why equality packets occur at both levels;
- how one realization could be transformed into the other;
- why different congruence masks should correspond to different internal readings of O0.
```

It therefore raises:

```text
REFACTOR_NETWORK
```

and proposes a hidden common constructive family:

```text
F_CORRESPONDENCE_COMPLETION_CANDIDATE

core registers:
    ROLE_MAPPING
    EQUALITY / ORDER RELATION
    DOMAIN_SEPARATION
    PLACEMENT_RESIDUE
    COMPLETION_STATUS

realization A:
    one-object internal correspondence

realization B:
    two-object external correspondence
```

Status: `PROPOSAL`.

---

# 6. Expansion Agent — attempt cross-level transformations

The Expansion Agent now tries controlled transformations between the two realizations.

It is not given an `EXTERNALIZE` operator by name. It may only:

```text
DUPLICATE
ROLE-SPLIT
OVERLAY
IDENTIFY
PROJECT
REBASE
```

## 6.1 Expand O0 by role-splitting

Starting from one object `T` carrying:

```text
SIDE_L = SIDE_R
ANGLE_L = ANGLE_R
```

it duplicates the role domains:

```text
T
  LEFT roles
  RIGHT roles

-> role-domain split ->

T_L
T_R
```

while preserving the equality mapping:

```text
SIDE(T_L) = SIDE(T_R)
ANGLE(T_L) = ANGLE(T_R)
```

The crucial discovery is that the same relation packet can survive when its two role domains are separated into distinct object carriers.

The agent labels the operation provisionally:

```text
DOMAIN_SEPARATION
```

and its inverse:

```text
DOMAIN_IDENTIFICATION
```

This is structurally equivalent to the later human labels `EXTERNALIZE` and `INTERNALIZE`, but those names were not supplied.

## 6.2 What remains missing?

After domain separation, the packet does not yet determine a full pair of triangles.

The agent sees that different **minimal carrier masks** are required to materialize the split correspondence geometrically.

This becomes the bridge to the congruence criteria.

---

# 7. Completion Agent — compare minimal masks with the split O0 packet

The Completion Agent treats SAS, SSS, and ASA not as theorem names but as partial masks over the externalized correspondence packet.

## 7.1 SAS mask

```text
side_1 EQ
side_2 EQ
included_angle EQ
```

The agent asks whether this mask can be obtained by splitting an internal OBJECT correspondence plus one shared/paired angular role.

It finds a viable organization:

```text
internal metric symmetry
    -> split into two cross-object side equalities

one angular relation
    -> acts as the hinge/carrier that fixes the relative placement of the split copies
```

Candidate interpretation:

```text
SAS = one way to materialize a separated correspondence packet
      by preserving two metric correspondences + one angular hinge.
```

Status: `COGNITIVE_CANDIDATE`, geometrically licensed by the raw SAS rule.

## 7.2 ASA mask

```text
angle_1 EQ
carrier_side EQ
angle_2 EQ
```

The same analysis yields:

```text
internal angular symmetry
    -> split into two cross-object angle correspondences

one metric carrier
    -> fixes separation/scale between the two angular ports
```

Candidate interpretation:

```text
ASA = another way to materialize the same correspondence-completion family,
      but with angular correspondence privileged instead of metric correspondence.
```

## 7.3 SSS mask

```text
side_1 EQ
side_2 EQ
side_3 EQ
```

This mask is interpreted differently:

```text
all three metric correspondences are externally fixed
    -> placement freedom collapses
    -> full pair correspondence becomes readable
```

The agent links this to the already-known placement register from I.7/I.8-like reasoning.

Candidate interpretation:

```text
SSS = metric saturation of the external correspondence packet.
```

---

# 8. Genealogy Agent — common family vs superficial analogy

The Genealogy Agent compares the three criteria after the mask reinterpretation.

It finds:

```text
SAS:
    metric-heavy split correspondence + angular hinge

ASA:
    angular-heavy split correspondence + metric carrier

SSS:
    metric saturation + placement completion
```

All terminate in:

```text
FULL_PAIR_COINCIDENCE
```

and all can be represented as different **partializations of one external correspondence-completion workspace**.

It therefore rejects:

```text
SAS ~ ASA ~ SSS
```

as the primary explanation.

Instead it proposes:

```text
SAS, ASA, SSS
    are sibling realization masks inside one family.
```

This is a family-level reorganization, not an analogy link.

---

# 9. Strong pressure event: O0 and PAIR family share the same deep packet

At this point the blackboard contains two candidate structures:

```text
A. O0 = internal complete correspondence packet

B. SAS/ASA/SSS = external partial masks that complete to a full correspondence packet
```

The Reorganization Agent asks whether these should remain separate families connected by an edge, or be represented under one deeper workspace.

The decisive evidence is transformational:

```text
DOMAIN_SEPARATION(O0)
    preserves role correspondences
    yields an external packet skeleton

DOMAIN_IDENTIFICATION(FULL_PAIR_COINCIDENCE)
    can collapse two corresponding role domains
    into one self-corresponding object view
```

Thus the connection is not merely descriptive.

The same constructive relation packet survives a change in domain separation.

The agent proposes:

```text
F_CORRESPONDENCE_COMPLETION

parameter:
    domain_separation

states/views:
    INTERNAL_SELF_PACKET
    EXTERNAL_PAIR_PACKET

completion modes:
    INTERNAL_RECIPROCAL_COMPLETION
    SAS_MASK_COMPLETION
    ASA_MASK_COMPLETION
    SSS_MASK_COMPLETION
```

Status: `REFACTOR_NETWORK PROPOSAL`.

---

# 10. Compiler Agent — compile the cross-level macro

The Compiler Agent sees a recurrent operation:

```text
one relation packet
    -> separate role domains
    -> preserve selected correspondences
    -> complete missing roles
```

and the inverse:

```text
complete external correspondence packet
    -> identify paired role domains
    -> obtain one-object self-correspondence view
```

It proposes two macro-operators without semantic names:

```text
SEPARATE_ROLE_DOMAINS
IDENTIFY_ROLE_DOMAINS
```

The human-facing architecture may later compile these as:

```text
EXTERNALIZE
INTERNALIZE
```

but the discovery trace preserves that they were induced by repeated cross-level transformations rather than predeclared.

---

# 11. Symmetry test

The Generic Reasoner now applies the OBJECT role swap `sigma` to the internal packet.

At O0:

```text
sigma(O0) = O0
```

The Genealogy Agent then asks what the equivalent operation looks like after role-domain separation.

It becomes a cross-object correspondence reversal:

```text
T1 roles <-> T2 roles
```

while preserving the completed pair state.

This reveals a deeper symmetry relation:

```text
internal fixed point under role swap
    <->
external invariance under pair exchange / correspondence reversal
```

The Reorganization Agent records this as further support that both structures are realizations of one correspondence family.

---

# 12. Validator

The Validator separates cognitive restructuring from proof claims.

## 12.1 Certified geometric support

Licensed:

```text
OBJECT equality packet from raw I.5/I.6-like rules
OBJECT order family from raw I.18/I.19-like rules
SAS -> congruence
SSS -> congruence
ASA -> congruence
role swap symmetry
pair exchange symmetry
```

## 12.2 Cognitive but not theorem-level claims

The following are accepted only as architecture-level interpretations:

```text
O0 as internal correspondence packet
SAS/ASA/SSS as sibling masks
F_CORRESPONDENCE_COMPLETION as shared deep family
SEPARATE_ROLE_DOMAINS / IDENTIFY_ROLE_DOMAINS as cross-level cognitive operators
```

No Euclidean theorem is certified merely from the family interpretation.

## 12.3 Anti-circularity check

The common family is inferred from already licensed routes and transformational invariants.

It is not used to prove the same raw congruence rules from which it was inferred.

Therefore:

```text
COGNITIVE_CYCLE = allowed
PROOF_CIRCULARITY = absent
```

---

# 13. Semantic interpretation after validation

Only after the refactor is validated may the human-facing layer attach familiar names.

The discovered OBJECT central state:

```text
SideRel = EQ
AngleRel = EQ
```

is the classical **isosceles** state.

The discovered deep relation can then be described as:

```text
ISOSCELES ZERO
    = internalized/self-correspondence realization
      of a deeper correspondence-completion family

CONGRUENT TRIANGLE PAIR
    = externalized/two-domain realization
      of the same deeper family
```

And the three criteria become:

```text
SAS
    one external access mask emphasizing metric correspondences + angular hinge

ASA
    one external access mask emphasizing angular correspondences + metric carrier

SSS
    one external access mask emphasizing metric saturation + placement rigidity
```

This language is interpretive and post-hoc; it was not available to the agents during the run.

---

# 14. Did the run discover "internalized congruence"?

Structurally: **yes, in a qualified sense**.

The agents independently recovered the following pattern:

```text
one complete correspondence packet
    |
    | role domains coincide
    v
single self-corresponding object

same correspondence packet
    |
    | role domains separated
    v
pair of corresponding objects
```

This is functionally the architecture meant by `internalized congruence`, even though the hidden phrase itself was never supplied.

The strongest evidence is not superficial similarity but **transformability while preserving the correspondence packet**.

---

# 15. Important non-result: not everything collapses into one concept

The Reorganization Agent explicitly rejects the stronger but misleading refactor:

```text
ISOSCELES = CONGRUENCE
```

because the two readings have different:

```text
workspace cardinality
placement register behavior
active role topology
construction affordances
counterfactual neighborhoods
```

The correct organization is:

```text
shared deep family / constructive packet
    -> different partializations
    -> different stabilized concepts
```

This is consistent with v0.3's principle that deep commonality does not erase conceptual differentiation.

---

# 16. Network refactor N1 -> N2

Before:

```text
F_TRIANGLE_RELATION
    O0

PAIR_SAS_RAW
PAIR_SSS_RAW
PAIR_ASA_RAW
    -> FULL_PAIR_COINCIDENCE
```

After:

```text
F_CORRESPONDENCE_COMPLETION
│
├── INTERNAL REALIZATION
│      └── F_TRIANGLE_RELATION
│             └── O0
│
└── EXTERNAL REALIZATION
       └── F_PAIR_CONGRUENCE
              ├── SAS mask
              ├── ASA mask
              └── SSS mask

cross-level operators:
    SEPARATE_ROLE_DOMAINS
    IDENTIFY_ROLE_DOMAINS

shared deep registers:
    role mapping
    equality/order relation
    completion status
    residual mismatch
    placement where applicable
```

Human semantic overlay:

```text
O0 -> isosceles zero
SEPARATE_ROLE_DOMAINS -> externalize
IDENTIFY_ROLE_DOMAINS -> internalize
external zero -> congruent pair
```

---

# 17. New impetus generated by the refactor

The refactor itself creates new pressures.

## 17.1 Expansion impetus

If SAS/ASA/SSS are masks of one external correspondence family, ask:

```text
What are their minimal disanalogical neighborhoods?
```

This points naturally toward:

```text
I.24 / I.25-like ordered pair families
ASA disanalogy still open
placement counterfactuals
```

## 17.2 Genealogical impetus

Ask whether other highly symmetric triangle concepts are richer internal realizations of the same family.

Candidate future probe:

```text
EQUILATERAL
```

but it is not introduced in this run.

## 17.3 Reorganization impetus

The presence of one deep correspondence family suggests that later transversal/parallel structures should be tested for **shared constructive participation**, not merely analogy.

This creates the proper bridge toward the transversal experiments without pre-assuming their result.

---

# 18. Strongest discovery of Run 02

Run 01 discovered:

```text
ISOSCELES-like equality state
    as the central/fixed member of a triangle relation family.
```

Run 02 discovers a deeper layer:

```text
that central state is special not only because equality is zero disanalogy,
but because it supports a complete INTERNAL role-correspondence packet
that can be unfolded into EXTERNAL pair correspondence.
```

Thus the genealogy deepens:

```text
raw theorem edges
    -> relation family
    -> fixed equality member
    -> internal correspondence packet
    -> shared correspondence-completion family
    -> external congruence masks
```

This is a genuine network refactor rather than an added analogy edge.

---

# 19. Delta summary

```text
N1
    F_TRIANGLE_RELATION
    central invariant O0
    raw SAS / SSS / ASA

N2
    + F_CORRESPONDENCE_COMPLETION
    + F_PAIR_CONGRUENCE
    + cross-level internal/external realization distinction
    + SEPARATE_ROLE_DOMAINS
    + IDENTIFY_ROLE_DOMAINS
    + SAS/ASA/SSS reinterpreted as sibling completion masks
    + O0 reinterpreted as internal complete correspondence packet
    + shared symmetry structure across OBJECT and PAIR levels
    + new expansion / genealogy / reorganization impetus
```

---

# 20. Next blind test

The next run should not immediately add more triangle theorems.

Instead, freeze `N2` and inject a deliberately banalized **local-line / transversal network** containing only:

```text
straight completion
vertical opposition
continuous carrier
external triangle angle
cross-intersection role alignment
```

Then ask the agents whether the new transversal structures:

```text
A. merely add edges to F_CORRESPONDENCE_COMPLETION;
B. create a sibling deep family;
C. force another REFACTOR_NETWORK;
D. expose that "correspondence completion" itself was still too coarse.
```

This preserves the central experimental principle:

```text
STRONG CONNECTION
    -> do not merely connect concepts
    -> test whether the current organization is wrong or incomplete.
```

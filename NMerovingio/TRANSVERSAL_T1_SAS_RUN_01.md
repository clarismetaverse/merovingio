# Transversal Experiment — T1 SAS Run 01

> Scope: test what the already-built **T1 transversal network** does to a SAS pair **before** introducing parallelism via I.27/I.28 and before using I.29. The aim is not to re-prove SAS by theorem-name lookup, but to see whether SAS acquires a new host interpretation, new completion behavior, or new future construction affordances.

---

# 0. Input pattern

Take two triangles `T1 = ABC` and `T2 = A'B'C'` with the SAS zero-mask:

```text
AB = A'B'
AC = A'C'
∠BAC = ∠B'A'C'
```

At TriangleNet level this already licenses:

```text
SAS_ZERO_MASK -> FULL_CONGRUENCE_GESTALT
```

The question of this run is different:

```text
Can the SAS pattern be embedded into the T1 transversal/intersection Gestalt
in a way that reveals a new distributed organization?
```

No parallelism may be assumed.

---

# 1. Constructional host proposal

Use one corresponding side pair as an **orientation carrier** for an embedding.

Cognitively normalize the two triangles so that:

```text
AB  and  A'B'
```

occupy the same oriented carrier role in two separated local views.

This does **not** mean the original segments are already parallel or collinear in the source problem. It is a host construction / overlay normalization:

```text
SAS_PAIR
   -> choose corresponding side as carrier role
   -> distribute two copies along one host orientation
```

Now the included angles become cross-packet angular roles relative to the same carrier genealogy:

```text
∠BAC     -> alpha_P
∠B'A'C'  -> alpha_Q
```

Since SAS gives:

```text
alpha_P = alpha_Q
```

we have a genuine zero in the T1 distributed angular register.

Status:

```text
SAS -> T1_HOST = EMBEDDABLE
```

provided the carrier normalization is explicitly constructed/overlaid rather than inferred from side equality alone.

---

# 2. First T1 effect: one SAS angle equality expands into a whole local angle-packet equality

T1 already compiled:

```text
alpha_P + beta_P = STRAIGHT
alpha_Q + beta_Q = STRAIGHT
```

and vertical-opposite duplications at both intersections.

SAS supplies:

```text
alpha_P = alpha_Q
```

Therefore shared-whole completion gives:

```text
beta_P = beta_Q
```

and vertical opposition propagates the equality through the remaining sectors.

Hence:

```text
ONE INCLUDED-ANGLE EQUALITY
    +
TWO LOCAL INTERSECTION PACKETS
    +
SHARED STRAIGHT-WHOLE ORGANIZATION
    ->
FULL PACKET ROLE-EQUALITY
```

Candidate compiled label:

```text
SAS_ANGLE_PACKET_COMPLETION
```

Important interpretation:

```text
SAS did not originally contain four angular correspondences.
The T1 host makes them simultaneously readable once one included-angle equality is mapped into the distributed intersection structure.
```

This is a genuine **SynopticGain** relative to the triangle-pair view.

---

# 3. Metric information remains independent at T1

SAS also supplies:

```text
AB = A'B'
AC = A'C'
```

The transversal Gestalt by itself does not convert these equalities into directional facts.

At T1 we must keep the distinction:

```text
METRIC_EQ != DIRECTION_EQ
```

and:

```text
SIDE_EQUALITY alone
    does not imply
PARALLEL / SAME_DIRECTION
```

Thus T1 does not yet prove that corresponding sides belong to parallel direction classes.

What it can do is store the equal sides as two metric role classes attached to an already-completed angular packet.

Represent the hosted SAS state as:

```text
HostedSAS_T1 {
    angular_packet_residue = ZERO
    metric_role_1_residue  = ZERO
    metric_role_2_residue  = ZERO
    parallel_status         = OPEN
}
```

---

# 4. New interpretation: SAS as a metric anchor inside a distributed angular zero

Before T1, SAS is represented as:

```text
2 metric zeroes + 1 angular zero
    -> full congruence
```

After hosting in T1, the same data can be reorganized as:

```text
1 distributed angular-packet zero
    +
2 metric anchors
```

because the single included-angle equality expands to the whole local angular packet under T1 completion.

So the enriched SAS view becomes:

```text
SAS_LOCAL_VIEW
    AB = A'B'
    AC = A'C'
    included_angle = included_angle'

SAS_T1_HOST_VIEW
    distributed_angle_packet = ZERO
    metric_anchor_1 = ZERO
    metric_anchor_2 = ZERO
```

This is a **BACKWARD_ENRICHMENT candidate** of SAS.

No new theorem is being added; the old SAS data acquire a different organization.

---

# 5. Comparison with ASA after T1

This run exposes an important asymmetry.

## ASA before T2

ASA supplies:

```text
angle_1 EQ
angle_2 EQ
carrier_side EQ
```

and therefore naturally presents **two angular zeroes** seeking a distributed direction host.

## SAS before T2

SAS supplies:

```text
side_1 EQ
side_2 EQ
included_angle EQ
```

but once the single angular equality is hosted at T1 it expands to:

```text
full local angle-packet EQ
```

Hence both criteria can become embeddable in the transversal network, but through different entry signatures:

```text
ASA:
    multiple explicit angular correspondences
        -> seek distributed host

SAS:
    one angular correspondence
        -> T1 packet completion
        -> distributed angular zero
        + two metric anchors
```

This suggests that T1 does not erase the distinction between SAS and ASA; it reveals two different **routes into the same distributed angular infrastructure**.

---

# 6. Counterfactual SAS in the T1 host

Now apply a minimal SAS disanalogy.

Keep:

```text
AB = A'B'
AC = A'C'
```

but break:

```text
∠BAC = ∠B'A'C'
```

into, for example:

```text
alpha_P > alpha_Q
```

T1 immediately propagates through the supplement transducer:

```text
alpha_P > alpha_Q
    ->
beta_P < beta_Q
```

Thus one angular SAS break generates a **paired anti-oriented residue** in the host:

```text
BREAK_INCLUDED_ANGLE_EQ(GT)
    ->
PRIMARY_ANGULAR_RESIDUE(GT)
    +
SUPPLEMENTARY_PROPAGATED_RESIDUE(LT)
```

This gives the SAS disanalogy a richer genealogy than it had in pair-space alone.

The hosted state records:

```text
seed_break      = INCLUDED_ANGLE
seed_orientation = GT
propagated_break = SUPPLEMENT_ROLE
propagated_orientation = LT
metric_anchors   = preserved EQ, EQ
```

This is a useful new disanalogy family:

```text
D_SAS_ANGLE_BREAK_IN_TRANSVERSAL_HOST
```

---

# 7. Connection to I.24/I.25 without leaking them into the run

TriangleNet already knows that, with two side correspondences fixed, an included-angle disanalogy belongs to the same pair-order family as a third-side disanalogy.

However, this T1 run does **not** use I.24 to derive the third-side order.

Instead it records a new representational fact:

```text
included-angle break
    ->
anti-oriented supplement break in transversal host
```

This means a future proof search toward an I.24-like result can now choose between at least two cognitive routes:

```text
PAIR ORDER route
```

or

```text
HOST included angle in transversal packet
    -> propagate angular residue
    -> search for geometric coupling to third-side register
```

Whether the second route closes is intentionally OPEN at T1.

This is exactly the kind of network restructuring the experiment is meant to detect.

---

# 8. Latent parallelogram host candidate

A further structure appears but must not yet be certified.

If, in a later stage, the hosted equal angular packet can license same-direction/parallel classes, then the two metric anchors of SAS become especially powerful.

Schematic future possibility:

```text
same direction class
    + equal corresponding segment length
    -> translated segment candidate
```

Applied twice:

```text
side family 1: same direction + equal length
side family 2: same direction + equal length
```

could make the SAS pair embeddable into a **parallelogram / translation closure Gestalt**.

At T1 this remains:

```text
SAS_PARALLELOGRAM_HOST = COGNITIVE-CANDIDATE
```

not `MEMBER` and not proof-licensed.

This candidate is important because it predicts a concrete T2 effect:

```text
I.27/I.28-like parallel certification
may transform SAS from a triangle-only congruence mask
into a local view of a parallelogrammatic translation structure.
```

---

# 9. Backward enrichment of the isosceles/SAS connection

TriangleNet already treated the isosceles as an internalized zero related to SAS-like external correspondence.

The T1 host adds a new possible reading:

```text
ISOSCELES
    -> EXTERNALIZE
SAS_PAIR
    -> HOST in distributed intersection packet
    -> one angle-zero expands to packet-zero
```

Therefore the internal angle equality of the isosceles may later be interpreted not only as an equality fact, but as a seed capable of generating a distributed angular packet when externalized.

Status:

```text
BACKWARD_ENRICH(ISOSCELES_ANGLE_ZERO)
    candidate affordance = EXTERNALIZE_TO_DISTRIBUTED_PACKET
```

This remains cognitive until a concrete host construction is validated in a given problem.

---

# 10. T1 SAS delta

Relative to SAS before the transversal network, T1 adds:

```text
1. HOSTABILITY
   SAS can be embedded into a two-intersection angular packet
   after explicit carrier normalization.

2. ANGULAR PACKET COMPLETION
   one included-angle equality expands into the full local intersection packet.

3. RICHER DISANALOGY PROPAGATION
   an included-angle break automatically creates an oppositely oriented
   supplementary-role break.

4. NEW REPRESENTATION
   SAS can be read as:
       distributed angular zero + two metric anchors.

5. FUTURE AFFORDANCE
   latent parallelogram/translation host candidate appears,
   but cannot be certified before parallelism is licensed.
```

No new geometric fact equivalent to SAS is required for these cognitive enrichments.

---

# 11. Critical guards

Do not allow the reasoner to infer at T1:

```text
angle equality -> parallel
side equality  -> same direction
host embedding -> original placement identity
packet equality -> triangle congruence without the SAS proof support
```

The host is a representational completion, not a substitute for the proof graph.

---

# 12. Main result of the run

The strongest T1 result is:

```text
SAS is no longer only
    2 side equalities + 1 included-angle equality.

When hosted in the transversal network it can be reorganized as
    2 metric anchors + 1 distributed angular zero,

because the single included-angle equality completes the whole
intersection-angle packet.
```

This is a real backward enrichment of the SAS Gestalt.

The most important prediction for T2 is:

```text
once an I.27/I.28-like module can certify direction classes from the
cross-packet angular zero, SAS may become embeddable in a higher
parallelogram/translation Gestalt.
```

That prediction must be tested rather than preloaded.

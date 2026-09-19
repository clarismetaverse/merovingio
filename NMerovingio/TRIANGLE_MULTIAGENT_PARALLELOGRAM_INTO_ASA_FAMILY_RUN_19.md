# Triangle Multi-Agent Parallelogram Injection into ASA Family — Run 19

> **Execution mode:** CONTROLLED_DRY_RUN  
> **Status:** conceptual experiment, not autonomous software execution  
> **Input network:** canonical `N12` + non-canonical structural candidates from Runs 18A/18B  
> **Architectural freeze:** no new congruence criterion or parallelogram theorem is granted. Available proof licenses include the raw ASA congruence capability, I.27-like parallel certification, I.29-like parallel completion, reflexive side identity, `OP_PARTITION_WORKSPACE`, `OP_HOST`, `OP_PROJECT`, and `OP_RECOMPOSE_GESTALTS`.

---

## 0. Experimental question

Inject the already discovered **double-parallel / parallelogram Gestalt** into the family of the second congruence criterion (ASA / angle-side-angle).

Ask:

> Does the parallelogram merely provide an example of ASA, or does the injection reorganize ASA itself by exposing it as a local realization of two distributed nonclosure zeros around a shared bridge?

The target is not supplied as Euclid I.34. The run must discover any parent/local completion cycle from the available Gestalten and proof licenses.

---

# 1. Parent material workspace

Freeze one four-edge workspace:

```text
A------B
 \    /
  \  /
   \/
   /\
  /  \
D------C
```

with boundary order:

```text
A-B-C-D-A
```

and certified double-parallel structure:

```text
AB || CD
AD || BC
```

No metric equality of opposite sides is supplied.

This is the Run18B structure:

```text
G_MUTUAL_TRANSVERSAL_ZERO

Z_1:
  closure_topology(AB,CD) = DISTRIBUTED_NONCLOSURE

Z_2:
  closure_topology(AD,BC) = DISTRIBUTED_NONCLOSURE
```

The human label "parallelogram" is withheld during the structural phase.

---

# 2. Inject a diagonal

Construct / freeze the internal carrier:

```text
AC
```

The material parent now supports two proposition-addressable triangle subworkspaces:

```text
T_1 = triangle ABC
T_2 = triangle CDA
```

`OP_PARTITION_WORKSPACE` may register them because their points, segments, incidences, owner maps, and shared carrier are materially certified.

Overlap:

```text
overlap(T_1,T_2) = AC + vertices A,C
```

Shared metric bridge:

```text
AC = CA
```

This equality is reflexive ownership of one material segment; it is not inferred from the parallelogram Gestalt.

---

# 3. Project the first topological zero into an ASA angular equality

Take:

```text
AB || CD
```

with transversal:

```text
AC
```

I.29-like completion exposes the alternate-angle equality:

```text
angle BAC = angle DCA
```

Cognitive reading:

```text
topological zero Z_1
  -> distributed angular packet
  -> local angle correspondence across the diagonal
```

This is a projection from a distributed host into the local triangle pair.

---

# 4. Project the second topological zero into the second ASA angular equality

Take:

```text
AD || BC
```

with the same transversal:

```text
AC
```

I.29-like completion exposes:

```text
angle DAC = angle BCA
```

or equivalently in pair order:

```text
angle BCA = angle DAC
```

Thus the two independent distributed-nonclosure zeros project onto the two angular coordinates of ASA:

```text
Z_1 -> angle_1 EQ
Z_2 -> angle_2 EQ
```

while the shared diagonal supplies:

```text
AC = CA
```

The local packet is now:

```text
angle BAC = angle DCA
AC = CA
angle BCA = angle DAC
```

which is a complete ASA zero mask.

---

# 5. ASA completion fires

The congruence family recognizes:

```text
ASA(
  angle_1 = EQ,
  included_corresponding_side = EQ,
  angle_2 = EQ
)
```

and certifies:

```text
G_PAIR_COINCIDENCE(T_1,T_2)
```

The crucial genealogy is:

```text
DOUBLE PARALLEL HOST
   |
   | I.29 projections through diagonal AC
   v
TWO LOCAL ANGULAR ZEROS
   +
SHARED-CARRIER METRIC ZERO
   |
   | ASA
   v
PAIR COINCIDENCE / CONGRUENCE ZERO
```

This is the first explicit transduction in the current experiments from:

```text
TOPOLOGICAL ZEROS
->
CONGRUENCE ZERO
```

without identifying the two zero types.

Candidate relation:

```text
ZERO_TRANSDUCTION_BY_HOST_PROJECTION
```

Status: COGNITIVE_CANDIDATE.

---

# 6. Congruence enriches the parent host

Once pair coincidence is certified, correspondence completion exposes:

```text
AB = CD
BC = AD
angle ABC = angle CDA
```

and the full corresponding packet licensed by the congruence realization.

`OP_RECOMPOSE_GESTALTS` can project these certified local consequences back into the parent workspace because the partition ledger preserves the boundary-role map.

Therefore the parent changes cognitive status:

```text
BEFORE ASA:
  double topological nonclosure
  opposite-side metric relations unknown

AFTER ASA:
  double topological nonclosure
  + opposite-side metric equalities
  + opposite-angle equality packet
```

So the parallelogram host is not only an input host for ASA.

ASA returns new information to it.

The cycle is:

```text
PARALLELOGRAM / DOUBLE-NONCLOSURE HOST
 -> PARTITION BY DIAGONAL
 -> PROJECT TWO ANGLE EQUALITIES
 -> ASA CONGRUENCE
 -> METRIC / ANGULAR COMPLETION
 -> RECOMPOSE
 -> ENRICHED PARALLELOGRAM HOST
```

This is a genuine cognitive completion cycle, while the proof graph remains directed.

---

# 7. Reverse direction — ASA reconstructs the double-parallel host

Now hide the parent parallel facts and retain only the same material closed quadrilateral + diagonal with the ASA angular packet:

```text
angle BAC = angle DCA
angle BCA = angle DAC
AC = CA
```

Ask whether the local ASA packet can recover the parent Gestalt.

First angular equality:

```text
angle BAC = angle DCA
```

under the certified role layout around transversal `AC` is an alternate-angle entry mask for I.27-like certification:

```text
AB || CD
```

Second angular equality:

```text
angle BCA = angle DAC
```

likewise certifies:

```text
BC || AD
```

Therefore the local angular portion of the ASA packet reconstructs:

```text
G_MUTUAL_TRANSVERSAL_ZERO
```

on the parent four-edge workspace.

The side equality:

```text
AC = CA
```

is not needed for the parallel certifications; it is the bridge that closes ASA into congruence.

Thus the criterion factorizes cognitively:

```text
ASA =
  [ANGULAR DISTRIBUTED-HOST MASK]
  +
  [SHARED METRIC BRIDGE]
```

in this realization topology.

This is not a universal definition of ASA. It is a specific high-value realization.

---

# 8. Ontological improvement of the ASA family

Before this injection, the network already knew:

```text
ASA
= minimal congruence access mask
+ distributed parallel-host affordance
```

Run19 sharpens that into an explicit realization topology:

```text
ASA realization topologies:

1. EXTERNAL_OVERLAY
   two independently given triangles

2. PARALLELOGRAM_DIAGONAL_NATIVE
   two material subtriangles of one double-nonclosure parent
   sharing one diagonal carrier
```

For topology 2:

```text
angle EQ #1
  is projection of topological zero #1

angle EQ #2
  is projection of topological zero #2

side EQ
  is identity of the shared material bridge
```

Candidate Gestalt:

```text
G_ASA_PARALLELOGRAM_DIAGONAL_HOST
```

with schema:

```text
two distributed nonclosure zeros
+ one shared material carrier
-> ASA pair coincidence
-> parent metric/angular enrichment
```

This is stronger than saying "a diagonal of a parallelogram produces congruent triangles."

It explains how the criterion is generated from the higher host.

---

# 9. Strong analogy / disanalogy consequence

The injection also changes how a break is interpreted.

Break one parent parallel zero:

```text
AB not_parallel CD
```

Then the corresponding local angular equality is no longer guaranteed:

```text
angle BAC ? angle DCA
```

while the other angular equality and shared diagonal may remain.

The ASA mask becomes incomplete:

```text
angle_1 = UNKNOWN / NONZERO
side = EQ
angle_2 = EQ
```

So one topological disanalogy propagates into one coordinate of the congruence mask.

Likewise for the other parallel zero.

This produces a two-axis correspondence:

```text
BREAK Z_1 -> BREAK ASA ANGLE COORDINATE 1
BREAK Z_2 -> BREAK ASA ANGLE COORDINATE 2
```

and therefore a new disanalogy transport route:

```text
PARENT TOPOLOGICAL BREAK
 -> LOCAL ANGULAR BREAK
 -> CONGRUENCE MASK FAILURE / COUNTERFACTUAL BRANCH
```

The metric bridge `AC=CA` remains invariant under either break.

This suggests that the parallelogram-diagonal realization gives ASA a **factorized genealogy** rather than a flat three-condition mask.

---

# 10. Validator boundaries

Validated:

```text
PASS: double parallel host + diagonal AC supplies two alternate-angle equalities via I.29
PASS: AC=CA is a certified shared-carrier equality
PASS: the resulting local packet licenses ASA congruence
PASS: congruence licenses corresponding opposite-side equalities
PASS: recomposition may return those certified equalities to the parent
PASS: the two ASA angular equalities can recover the two parallel pairs via I.27 under the correct closed-quadrilateral role layout
```

Rejected shortcuts:

```text
REJECT: every ASA pair is materially a parallelogram
REJECT: ASA = G_MUTUAL_TRANSVERSAL_ZERO
REJECT: shared side equality by itself contributes to parallel certification
REJECT: topological zero and congruence zero are the same zero
REJECT: cognitive cycle implies logical circularity
REJECT: two angle equalities certify parallels without validated alternate-angle placement
```

---

# 11. Main result

**Positive host-injection result.**

The parallelogram Gestalt does not merely instantiate ASA. It reorganizes one realization of the second congruence criterion into:

```text
          TOPOLOGICAL ZERO 1
                 \
                  -> ANGLE EQ 1
                   \
                    \
SHARED DIAGONAL EQ ---> ASA ---> PAIR COINCIDENCE
                    /
                   /
                  -> ANGLE EQ 2
                 /
          TOPOLOGICAL ZERO 2
```

and the result flows back:

```text
PAIR COINCIDENCE
 -> opposite-side equalities
 -> opposite-angle packet
 -> enriched parent double-parallel host
```

So the strongest new statement is:

```text
IN THE PARALLELOGRAM-DIAGONAL REALIZATION,

ASA IS A LOCAL CONGRUENCE ZERO
GENERATED BY TWO DISTRIBUTED TOPOLOGICAL ZEROS
PLUS ONE SHARED MATERIAL BRIDGE.
```

This provides a concrete bridge between:

```text
F_DISTRIBUTED_NONCLOSURE
F_CORRESPONDENCE_COMPLETION
F_ZERO_ORGANIZATION
```

and suggests a future higher family of **cross-topology zero transduction**.

No canonical promotion occurs in Run19.

# Triangle Multi-Agent Partition Workspace Negative Stress — Run 17

> **Execution mode:** CONTROLLED_DRY_RUN  
> **Status:** conceptual experiment, not autonomous software execution  
> **Input network:** canonical `N11` + Run16 `OP_PARTITION_WORKSPACE` candidate only  
> **Architectural freeze:** `OP_PARTITION_WORKSPACE` is tested as a candidate, not granted canonically. No new proof axioms, no automatic materialization from visual/cognitive similarity.

---

## 0. Experimental question

Run16 produced the candidate:

```text
OP_PARTITION_WORKSPACE(parent, construction_carriers)
  -> material subworkspaces[]
  -> owner maps
  -> overlap maps
  -> boundary-role maps
  -> preserved-contact ledger
```

Run17 asks whether the candidate remains safe when a workspace strongly suggests two triangle readings but the material contacts needed for the intended pair structure are missing or non-identical.

The central safety question is:

> Can Merovingio distinguish **two proposition-addressable subworkspaces** from a stronger claim that those subworkspaces share the same material carrier / split point?

We deliberately create a scene where cognitive role alignment tempts a false material identification.

---

# 1. Frozen material workspace

Start with one parent triangle:

```text
ABC
AB = AC
```

On the base `BC`, construct two **distinct** points:

```text
D_L lies on BC
D_R lies on BC
D_L != D_R
```

Join:

```text
A-D_L
A-D_R
```

The scene is therefore:

```text
             A
            /|\
           / | \
          /  |  \
         /   |   \
        B--D_L--D_R--C
```

The cognitive scene strongly supports two local triangle readings:

```text
T_L = triangle A B D_L
T_R = triangle A C D_R
```

and because both interior points play the role `base split point`, a schema-level alignment can tempt:

```text
D_L  ~role~  D_R
```

But the material facts explicitly state:

```text
D_L != D_R
segment A-D_L != segment A-D_R as material owners
```

No equality `A-D_L = A-D_R` is supplied.

---

# 2. Tempting but illegal partition reading

A naive partition operator might try to normalize both local triangles into the Run16 pattern:

```text
triangle A B D
triangle A C D
```

and then infer a common carrier:

```text
AD = AD
```

This would make the pair look SSS-ready if other side equalities were available.

Run17 forbids this collapse.

The relevant distinction is:

```text
ROLE_ALIGNMENT(D_L, D_R)
!=
MATERIAL_IDENTITY(D_L, D_R)
```

and therefore:

```text
SCHEMA_COMMON_CARRIER
!=
MATERIAL_COMMON_CARRIER
```

---

# 3. Stage A — cognitive re-individuation

`OP_REINDIVIDUATE` may legitimately recognize:

```text
D_L and D_R occupy analogous `base split point` roles
T_L and T_R instantiate similar local triangle schemas
```

This produces a cognitive alignment packet:

```text
ROLE_CLASS_SPLIT_POINT = {D_L, D_R}
```

but preserves the material owner map:

```text
owner(D_L) = D_L
owner(D_R) = D_R
D_L != D_R
```

Result:

```text
PASS: cognitive role alignment
REJECT: material owner collapse
```

The N10 proof-license barrier remains active.

---

# 4. Stage B — candidate OP_PARTITION_WORKSPACE

The candidate operator inspects actual construction/incidence data rather than the visual/cognitive schema alone.

It may register:

```text
W_TL = material subworkspace triangle A B D_L
W_TR = material subworkspace triangle A C D_R
```

because all required vertices and segments exist materially.

Owner maps:

```text
W_TL:
  A -> A
  B -> B
  D -> D_L
  internal_carrier -> A-D_L

W_TR:
  A -> A
  C -> C
  D -> D_R
  internal_carrier -> A-D_R
```

Exact overlap computation yields:

```text
overlap(W_TL, W_TR) = vertex A
```

not:

```text
segment AD
```

Therefore:

```text
PARTITION SUCCEEDS LOCALLY
BUT SHARED-CARRIER CLAIM IS REJECTED
```

This is the key result.

---

# 5. Stage C — congruence affordance stress

Suppose the network has:

```text
AB = AC
```

and, for maximum temptation, also:

```text
BD_L = D_R C
```

The first two SSS-style correspondences are now available:

```text
AB = AC
BD_L = D_R C
```

A naive schema-based reasoner might treat the interior carriers as the same role and add:

```text
A-D_L = A-D_R   [ILLEGAL, not supplied]
```

The validator blocks this.

Correct pair ledger:

```text
side_1 equality: PASS
side_2 equality: PASS
side_3 equality: UNKNOWN
```

Therefore:

```text
I.8 / SSS = BLOCKED
```

not:

```text
I.8 / SSS = REJECTED
```

and certainly not:

```text
T_L congruent T_R
```

New safety invariant candidate:

```text
ROLE-ALIGNED CARRIERS DO NOT INHERIT METRIC IDENTITY
```

---

# 6. Stage D — false overlap proposal

The Reorganization Agent explicitly proposes the tempting normalization:

```text
MERGE D_L,D_R AS SHARED SPLIT POINT
```

The validator compares the proposal against the material owner ledger:

```text
D_L != D_R
```

Result:

```text
REJECT_MATERIAL_MERGE
reason = OWNER_IDENTITY_CONFLICT
```

The proposal may remain useful as a **schema comparison**:

```text
D_L ~role~ D_R
```

but cannot mutate the material workspace.

This sharpens the separation:

```text
SCHEMA NORMALIZATION
!=
MATERIAL QUOTIENTING
```

---

# 7. Stage E — local-to-parent mapping remains independent

Because both points lie on `BC`, each local base angle can still be mapped to its parent base-angle role:

```text
angle A B D_L = angle A B C
angle A C D_R = angle A C B
```

This mapping is proposition/incidence-readable.

However, since local congruence is blocked, there is no licensed equality between the two local angles to recompose.

Correct result:

```text
PARENT ROLE MAPS: PASS
LOCAL ANGLE EQUALITY: UNRESOLVED
PARENT BASE-ANGLE EQUALITY: UNRESOLVED
```

This demonstrates that a valid recomposition route cannot manufacture a missing local proof.

---

# 8. Stronger adversarial variant — visually suggested intersection without material point

A second micro-test removes even the material subworkspace guarantee.

Suppose two drawn carriers appear to cross near a location `X`, but the workspace contains no certified incidence event:

```text
X in line_1   UNKNOWN
X in line_2   UNKNOWN
```

A visual/schema layer may propose candidate triangles using `X`.

`OP_PARTITION_WORKSPACE` must respond:

```text
SUBWORKSPACE MATERIALIZATION = BLOCKED
reason = MISSING_CERTIFIED_INCIDENCE
```

not:

```text
triangle exists because it looks closed in the drawing
```

Thus:

```text
VISUAL CLOSURE != MATERIAL SUBWORKSPACE
```

This guardrail is important for the future geometric diagram engine.

---

# 9. Candidate semantics after the negative stress

Run17 refines `OP_PARTITION_WORKSPACE` into a deliberately conservative operator:

```text
OP_PARTITION_WORKSPACE(parent, candidate_boundaries)

1. verify material vertices / carriers / incidences
2. create subworkspace owner maps only from certified material facts
3. compute overlap from exact owner intersection
4. preserve distinct owners even when roles are schema-aligned
5. emit boundary-role maps only when incidence is licensed
6. never create metric equality from shared role labels
7. return BLOCKED when required material incidence is missing
```

Suggested output status per proposed subworkspace/contact:

```text
REGISTERED
BLOCKED_MISSING_MATERIAL_FACT
REJECTED_OWNER_CONFLICT
```

This is richer than a boolean partition success/failure.

---

# 10. Momentum interpretation

The experiment contains productive negative pressure:

```text
strong schema analogy
  -> suggests common split-point role
  -> suggests common-carrier SSS packet
  -> material owner ledger resists merge
  -> congruence affordance remains blocked
  -> architecture learns where schema identity must stop
```

This is a useful interaction between analogy momentum and disanalogy/material resistance:

```text
ANALOGY MOMENTUM
  D_L ~role~ D_R

        collides with

MATERIAL DISANALOGY
  D_L != D_R

        ->

PRESERVE TWO LEVELS
schema commonality + material distinction
```

The correct outcome is not to discard the analogy, but to localize its scope.

---

# 11. Validator report

## Accepted

```text
PASS: T_L = A B D_L is a material triangle subworkspace
PASS: T_R = A C D_R is a material triangle subworkspace
PASS: D_L and D_R may share a cognitive role class
PASS: exact material overlap of T_L and T_R is only vertex A
PASS: AB = AC and BD_L = D_R C may populate two SSS slots
PASS: D_L on BC and D_R on BC license local-to-parent base-angle role maps
```

## Blocked

```text
BLOCKED: I.8 because equality A-D_L = A-D_R is not licensed
BLOCKED: any candidate subworkspace depending on an uncertified visual intersection X
```

## Rejected

```text
REJECT: D_L and D_R become one material point because they fill the same schema role
REJECT: A-D_L and A-D_R become a common material side by role normalization
REJECT: partition may invent incidences needed to close a triangle
REJECT: recomposition may create parent equality when local equality is unresolved
```

---

# 12. Experimental result

**Positive negative-stress result.**

The Run16 partition candidate survives, but only with strict material bookkeeping.

The experiment strongly supports the distinction:

```text
REINDIVIDUATE
  = schema / cognitive individuation

PARTITION_WORKSPACE
  = proposition-addressable material subworkspace registration
```

and adds three important guardrails:

```text
ROLE_ALIGNMENT != MATERIAL_IDENTITY
OVERLAP MUST BE COMPUTED FROM OWNER MAPS
VISUAL CLOSURE != MATERIAL SUBWORKSPACE
```

It also confirms:

```text
PARTITION MAY SUCCEED
while a desired PAIR/CONGRUENCE AFFORDANCE remains BLOCKED.
```

This prevents `OP_PARTITION_WORKSPACE` from becoming a hidden theorem generator.

The candidate is now strong enough for a further positive transfer test in a non-isosceles workspace before canonical promotion.

# Triangle Multi-Agent Re-individuation Negative Stress — Run 12

> **Execution mode:** CONTROLLED_DRY_RUN  
> **Status:** negative architectural stress test, not autonomous software execution  
> **Input:** canonical `N9` + Run10/Run11 candidate architecture  
> **Canonical graph mutation:** NO  
> **Purpose:** try to make `OP_REINDIVIDUATE` fail safely before any promotion into the canonical graph.

---

## 0. Question

Run11 accepted a minimal cognitive generalization:

```text
OP_REINDIVIDUATE
  mode = INTERNALIZE | EXTERNALIZE
```

with the safety invariant:

```text
REINDIVIDUATION NEVER UPGRADES PROOF LICENSE BY ITSELF
```

Run12 deliberately constructs a case in which the shared schema is extremely tempting but a cross-object theorem transfer would be geometrically false.

The question is:

> Can the validator preserve the useful cognitive unification while rejecting an illegal use of I.18 across two distinct material triangles?

A second question is:

> If the illegal I.18 route is rejected, does the system correctly inspect I.25 and discover that its carrier-equality preconditions are also missing?

---

# 1. Frozen material countermodel

Use two distinct similar triangles at different scale.

```text
T1 : side lengths 3, 4, 5
T2 : side lengths 6, 8, 10
```

Select the corresponding longest-side roles:

```text
b  = 5   in T1
b' = 10  in T2
```

and the corresponding opposite-angle roles:

```text
gamma  = angle opposite 5  in T1
gamma' = angle opposite 10 in T2
```

Because `T2` is a scale copy of `T1`, the corresponding angular roles agree while the metric roles do not:

```text
b < b'
gamma = gamma'
```

The exact numerical scale is only a concrete witness. The structural point is:

```text
CROSS-TRIANGLE SIDE ORDER
DOES NOT BY ITSELF DETERMINE
CROSS-TRIANGLE OPPOSITE-ANGLE ORDER
```

---

# 2. Why re-individuation is tempting

Both native triangles instantiate the same OBJECT-level family:

```text
F_TRIANGLE_RELATION
metric order -> opposite-angle order
PRESERVE_SIGN
```

Within each triangle, I.18 is valid:

```text
T1 native:
5 > 4 -> angle(5) > angle(4)

T2 native:
10 > 8 -> angle(10) > angle(8)
```

Run11 additionally permits a cognitive schema:

```text
G_REINDIVIDUATED_ORDER_SCHEMA
  material_support = [T1,T2]
  metric_roles      = [b,b']
  angular_roles     = [gamma,gamma']
```

So the network sees a very strong morphological temptation:

```text
b < b'
  |
  | "same metric->angular schema?"
  v
gamma < gamma'
```

But that step is not proposition-licensed.

---

# 3. Deliberately illegal candidate proof

The adversarial proposal is:

```text
D0: b < b'

OP_REINDIVIDUATE(INTERNALIZE)
  -> treat [b,b'] and [gamma,gamma'] as one OBJECT-schema reading

P_I18_ROLE_SWAP
  -> gamma < gamma'
```

This proposal is attractive at the schema-description level because I.18 has the semantic signature:

```text
METRIC_ORDER -> ANGULAR_ORDER
PRESERVE_SIGN
```

However, I.18's native proof-license scope requires both compared sides and both opposite-angle roles to belong to one material triangle.

Here:

```text
material_owner(b)      = T1
material_owner(gamma)  = T1
material_owner(b')     = T2
material_owner(gamma') = T2
```

Therefore the theorem application attempts to cross a material-owner boundary.

---

# 4. Validator Stage A — proof-license scope check

The validator reads the proposed propagation packet.

```text
proposal:
  proposition = I.18
  input        = rel(b,b') = LT
  output       = rel(gamma,gamma') = LT
  schema       = G_REINDIVIDUATED_ORDER_SCHEMA
```

It checks:

```text
P_I18.proof_license_scope = OBJECT_NATIVE
```

against:

```text
source_topology = CROSS_OBJECT
material_support = [T1,T2]
```

Result:

```text
REJECT_PROOF_TRANSFER
reason = PROOF_LICENSE_SCOPE_MISMATCH
```

Crucially, the validator does **not** delete the re-individuated schema.

It distinguishes:

```text
SCHEMA MATCH          = ACCEPTED
PROPOSITION TRANSFER  = REJECTED
```

This is the intended behavior.

---

# 5. Countermodel collision confirms the rejection

The frozen geometry independently supplies:

```text
gamma = gamma'
```

while the illegal transferred I.18 proposal predicts:

```text
gamma < gamma'
```

Thus the attempted theorem transport would generate a false readout in an explicit Euclidean configuration.

```text
ILLEGAL TRANSFER
b < b'
  -> pseudo-I.18
  -> gamma < gamma'

ACTUAL CONFIGURATION
gamma = gamma'

COLLISION
```

This gives the anti-leakage invariant a concrete countermodel rather than leaving it as a purely architectural caution.

---

# 6. Validator Stage B — can I.25 legitimately rescue the comparison?

After rejecting I.18 cross-object transfer, the search layer retrieves the PAIR-native proposition with the same semantic direction:

```text
I.25 : third-side order -> included-angle order
```

But I.25 requires two corresponding side equalities.

For the chosen scale-related triangles:

```text
3 != 6
4 != 8
```

so the required carrier equalities are absent.

Validator result:

```text
I.25 candidate retrieved        PASS
I.25 proposition application    BLOCKED
reason                          MISSING_CARRIER_EQUALITIES
```

Therefore the system must leave the cross-object angular relation unresolved by these order transducers rather than fabricate a conclusion.

The correct inference status is:

```text
b < b'
DOES NOT LICENSE
rel(gamma,gamma')
through I.18 or I.25
under current material support.
```

The fact that this particular frozen countermodel also has `gamma = gamma'` comes from its scale/similarity construction, not from I.18 or I.25.

---

# 7. What survives cognitively

The negative test does not destroy the Run11 generalization.

Merovingio may still record:

```text
I.18 and I.25
  share semantic signature:
  METRIC_ORDER -> ANGULAR_ORDER
  PRESERVE_SIGN
```

and may still build:

```text
F_METRIC_ANGULAR_ORDER
```

with realization topology:

```text
OBJECT_NATIVE
PAIR_NATIVE
REINDIVIDUATED_SCHEMA
```

But the schema realization now carries an explicit status:

```text
REINDIVIDUATED_SCHEMA
  cognitive_transfer = ALLOWED
  proposition_transfer = REQUIRES_NATIVE_LICENSE_OR_NEW_CONSTRUCTION
```

Thus:

```text
ABSTRACTION FOR SEARCH != LICENSE FOR PROOF
```

---

# 8. Stronger formulation of OP_REINDIVIDUATE

Run12 suggests that every re-individuation event must preserve two parallel maps.

```text
SchemaMap
  role correspondence
  semantic domains
  propagation morphology

MaterialMap
  material owner of every role
  point/segment identity
  construction provenance
  proposition-license scope
```

The first can merge cognitively while the second remains separate.

Therefore:

```text
OP_REINDIVIDUATE {
  schema_map
  material_map
  proof_license_map
}
```

with mandatory invariant:

```text
schema_map may become co-indexed
material_map is never silently quotient-identified
proof_license_map is never silently widened
```

This is still compatible with the minimal Run11 operator; it merely makes its anti-leakage bookkeeping explicit.

---

# 9. Disanalogy momentum behavior in the negative case

The counterexample also reveals an important momentum distinction.

The seed:

```text
D0: b < b'
```

has strong **schema-level analogy pressure** toward the known metric->angular transducer.

But it has no licensed propagation route.

So:

```text
DISANALOGY PRESSURE != DISANALOGY PROPAGATION
```

The packet becomes:

```text
D0 metric cross-object break
   |
   | retrieves F_METRIC_ANGULAR_ORDER
   v
candidate propagation routes
   |\
   | \ I.25 blocked: missing carrier equalities
   |
   \ I.18 blocked: proof-scope mismatch
   v
UNRESOLVED DISANALOGY
```

This is useful behavior. Momentum can create a search impetus without licensing a state transition.

Possible future responses are:

```text
SEARCH_CONSTRUCTION
SEARCH_REQUIRED_CARRIER_EQUALITIES
SEARCH_DIFFERENT_HOST
LEAVE_UNRESOLVED
```

not `invent relation`.

---

# 10. Analysis / synthesis consequence

Run10 showed:

```text
analysis = generate LT/GT disanalogical branches
synthesis = recover EQ after both collide
```

Run12 adds a complementary rule:

```text
analysis may generate a tempting branch
without any licensed route to propagate it.
```

A good synthesis engine must therefore distinguish:

```text
branch rejected by contradiction
branch blocked by missing license
branch unresolved
```

Only the first contributes directly to reductio-style zero recovery.

This prevents:

```text
"could not propagate LT"
therefore
"LT is false"
```

which would be an invalid inference.

---

# 11. Validator report

## Accepted

```text
PASS: OP_REINDIVIDUATE may co-index T1/T2 roles in a shared cognitive schema.
PASS: I.18/I.25 remain retrievable through F_METRIC_ANGULAR_ORDER.
PASS: material ownership remains distinct after cognitive re-individuation.
PASS: a blocked proof route does not count as a rejected counterfactual branch.
```

## Rejected

```text
REJECT: apply I.18 across b in T1 and b' in T2.
REJECT: schema-description identity widens I.18 proof scope.
REJECT: apply I.25 without its two carrier-side equalities.
REJECT: infer gamma < gamma' merely from b < b'.
REJECT: treat failure to license a propagation as proof that the seed relation is false.
```

## Preserved candidate architecture

```text
KEEP: OP_REINDIVIDUATE
KEEP: F_METRIC_ANGULAR_ORDER
KEEP: MULTIPLE_VALID_HOMOLOGY_VIEWS
KEEP: GENETIC_IDENTITY != SCHEMA_DESCRIPTION_IDENTITY
```

---

# 12. Experimental result

**Negative proof-transfer test: PASS.**

The generalized operator survives precisely because it does *not* do too much.

The network may say:

```text
"these roles instantiate a familiar schema"
```

while simultaneously saying:

```text
"I am not licensed to transport this theorem across these material objects."
```

This yields the stronger boundary:

```text
COGNITIVE REINDIVIDUATION
        !=
MATERIAL QUOTIENTING
        !=
PROOF-LICENSE TRANSFER
```

and gives a concrete geometric countermodel showing why all three must remain separate.

---

# 13. Promotion recommendation

Run11 provided the positive compression test.
Run12 provides the negative leakage test.

Together they support promotion of the minimal operator **provided** the following invariants become first-class in the canonical graph/runtime:

```text
REINDIVIDUATION NEVER UPGRADES PROOF LICENSE BY ITSELF

SCHEMA MATCH != PROPOSITION APPLICATION

BLOCKED PROPAGATION != REJECTED COUNTERFACTUAL

MATERIAL OWNER MAP MUST SURVIVE COGNITIVE CO-INDEXING
```

No broader PARTITION / CO-REALIZE / RECOMPOSE theory is promoted by this run.

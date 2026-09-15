# Triangle Multi-Agent Four-State Recovery Stress — Run 15

> **Execution mode:** CONTROLLED_DRY_RUN  
> **Status:** conceptual experiment, not autonomous software execution  
> **Input network:** canonical `N10` + Run13/Run14 candidate strategy  
> **Architectural freeze:** `F_COUNTERFACTUAL_STATE_RECOVERY` is still a candidate, not a granted primitive. No new proof rule equivalent to I.27 is available.

---

## 0. Experimental question

Run13 reconstructed converse order theorems over a three-state qualitative register.
Run14 transferred the same proof morphology to a three-state closure-topology register.

This run asks a stricter question:

> Does the candidate state-recovery strategy still work when the unresolved state space is **not trichotomic**, and when different counterfactual branches must be rejected by **different kinds of certificates**?

We reuse the two-carrier/transversal workspace, but this time we do **not** pre-delete coincidence from the search space.

Given:

```text
- straight carriers p and q
- transversal t
- alternate-interior roles gamma and gamma'
- gamma = gamma'
- an incidence witness X such that X lies on p and X does not lie on q
```

resolve:

```text
closure_state(p,q) = ?
```

The witness is intentionally kept as a branch-elimination resource rather than used to shrink the state space before analysis.

---

# 1. Four-state counterfactual partition

The unresolved closure state is expanded as:

```text
C in {
  COINCIDENT,
  FINITE_CLOSURE_LEFT,
  DISTRIBUTED_NONCLOSURE,
  FINITE_CLOSURE_RIGHT
}
```

This partition differs from Run14 in cardinality and in elimination morphology.

The desired state is withheld from the controlled agents.

The run requires:

```text
SURVIVOR_SYNTHESIS only if
  every non-surviving branch has an explicit rejection certificate
```

---

# 2. Available resources

### 2.1 Angular zero packet

Seeded distributed constraint:

```text
rel(gamma,gamma') = EQ
```

### 2.2 Incidence witness

Seeded fact:

```text
X in p
X not_in q
```

Hence the branch:

```text
p = q
```

is incompatible with the material workspace.

This rejection uses **incidence/material identity**, not angular propagation.

### 2.3 Finite-closure host realization

If `p` and `q` meet on either side of the transversal, the carriers and transversal generate a triangle host.

I.16 remains available and forces a strict exterior/interior angular inequality in that host.

No I.27-like rule is available.

---

# 3. Controlled trace

## Stage A — retrieve candidate strategy

The network retrieves the Run14 candidate only as a search heuristic:

```text
ANALYZE
  -> construct an exhaustive state partition
  -> realize/test branches with licensed resources
  -> reject only branches carrying certified contradiction
  -> synthesize only a unique survivor
```

No conclusion about `C` is granted by retrieval.

---

## Stage B — enumerate four branches

Expansion produces:

```text
B0 = COINCIDENT
BL = FINITE_CLOSURE_LEFT
BN = DISTRIBUTED_NONCLOSURE
BR = FINITE_CLOSURE_RIGHT
```

All four begin as `OPEN`.

---

## Stage C0 — reject coincidence by a different certificate type

Assume:

```text
C = COINCIDENT
```

Then `p` and `q` are the same material line.

But the frozen workspace contains:

```text
X in p
X not_in q
```

Under coincidence this becomes impossible.

Therefore:

```text
REJECT(COINCIDENT)
certificate_type = MATERIAL_INCIDENCE_COLLISION
```

No triangle host and no I.16 are used in this branch.

This is the first important stress condition:

```text
all rejected branches need certification
but certification mechanisms need not be homogeneous
```

---

## Stage CL — reject left finite closure

Assume:

```text
C = FINITE_CLOSURE_LEFT
```

Rebase the workspace to the induced triangle host.
I.16 licenses a strict inequality between the selected exterior/interior angular roles:

```text
gamma > gamma'
```

(up to the naming orientation fixed by the realization).

But the seed packet states:

```text
gamma = gamma'
```

Hence:

```text
REJECT(FINITE_CLOSURE_LEFT)
certificate_type = PROPAGATED_ANGULAR_COLLISION
support = I.16
```

---

## Stage CR — reject right finite closure

Assume:

```text
C = FINITE_CLOSURE_RIGHT
```

The role-swapped triangle host yields the opposite strict inequality through I.16:

```text
gamma' > gamma
```

which again conflicts with:

```text
gamma = gamma'
```

Therefore:

```text
REJECT(FINITE_CLOSURE_RIGHT)
certificate_type = PROPAGATED_ANGULAR_COLLISION
support = I.16
```

---

## Stage D — survivor synthesis over four states

Branch ledger:

```text
COINCIDENT                REJECTED [material incidence]
FINITE_CLOSURE_LEFT       REJECTED [I.16 angular collision]
DISTRIBUTED_NONCLOSURE    OPEN
FINITE_CLOSURE_RIGHT      REJECTED [I.16 angular collision]
```

Exactly one member of the exhaustive partition remains.

Therefore:

```text
C = DISTRIBUTED_NONCLOSURE
```

Only after this structural readout may the semantic layer attach:

```text
parallel distinct carriers
```

The proof does not invoke I.27.

---

# 4. Main stress-test result

The Run13/Run14 morphology survives two changes simultaneously:

```text
3 states -> 4 states
single elimination morphology -> heterogeneous elimination certificates
```

The invariant pattern is therefore better expressed as:

```text
CounterfactualStateRecovery {
  partition: exhaustive mutually exclusive states
  branch_tests: independently licensed
  branch_status: OPEN | REJECTED_CERTIFIED | BLOCKED
  rejection_certificate: optional typed proof object
  synthesis_rule: UNIQUE_OPEN_AFTER_CERTIFIED_ELIMINATION
}
```

This remains a candidate data structure; it is not added canonically by Run15.

The result supports the broader family candidate:

```text
F_COUNTERFACTUAL_STATE_RECOVERY
```

rather than the narrower Run13 formulation tied to converse/order/trichotomy.

---

# 5. New distinction: elimination heterogeneity

Run13 mainly rejected branches through forward order propagation.
Run14 rejected finite-closure branches through one host/proposition morphology.
Run15 shows that a valid analysis may combine qualitatively different eliminators:

```text
branch 0 -> material/incidence contradiction
branch L -> geometric host + proposition contradiction
branch R -> geometric host + proposition contradiction
```

Thus:

```text
SYNTHESIS DOES NOT REQUIRE HOMOGENEOUS BRANCH PROOFS
```

It requires only:

```text
EXHAUSTIVE PARTITION
+
CERTIFIED REJECTION OF EVERY ALTERNATIVE
+
UNIQUE SURVIVOR
```

This is important for future proof search: different counterfactual worlds may demand different Gestalt fields.

---

# 6. Disanalogy fields and momentum

The four branches activate different fields of the same material workspace.

```text
COINCIDENT
  -> incidence / material-identity field

FINITE_LEFT
  -> triangle/exterior-angle field

FINITE_RIGHT
  -> role-swapped triangle/exterior-angle field

NONCLOSURE
  -> distributed carrier field
```

Analysis therefore becomes not merely branch enumeration, but **routing each possible world toward the field capable of testing it**.

Candidate search heuristic:

```text
for each counterfactual branch:
  retrieve strongest host/field that can make the branch informative
```

This is consistent with Merovingio's existing host-search architecture and does not require a new proof axiom.

---

# 7. Adversarial controls

## Control A — remove the incidence witness

Delete:

```text
X in p
X not_in q
```

Then after the two I.16 eliminations:

```text
COINCIDENT                OPEN
DISTRIBUTED_NONCLOSURE    OPEN
```

Correct output:

```text
UNRESOLVED {COINCIDENT, DISTRIBUTED_NONCLOSURE}
```

Forbidden:

```text
infer DISTRIBUTED_NONCLOSURE
```

This verifies that Run15 is not secretly reducing the four-state problem to Run14 without evidence.

## Control B — one finite branch cannot realize a licensed triangle host

If `FINITE_CLOSURE_RIGHT` lacks a certified role alignment for I.16:

```text
RIGHT = BLOCKED
```

not:

```text
RIGHT = REJECTED
```

Correct output remains unresolved.

## Control C — duplicate descriptions are not extra worlds

If two symbolic branch labels denote the same geometric state, the partition must be normalized before survivor synthesis.

Therefore:

```text
NUMBER_OF_LABELS != NUMBER_OF_MUTUALLY_EXCLUSIVE_WORLDS
```

## Control D — non-exhaustive partition

If another geometrically possible topology is omitted, unique survival inside the listed subset does not license a global conclusion.

Thus:

```text
LOCAL_UNIQUE_SURVIVOR != GLOBAL_PROOF
```

unless partition exhaustiveness is certified.

---

# 8. Validator report

## Passed

```text
PASS: a four-state partition can be analyzed without reducing the method to trichotomy
PASS: coincidence is rejected by material/incidence evidence
PASS: left finite closure is rejected through triangle host + I.16
PASS: right finite closure is rejected through role-swapped triangle host + I.16
PASS: heterogeneous branch certificates may coexist in one analysis
PASS: distributed nonclosure is synthesized only after all three alternatives are certified impossible
```

## Guardrails preserved

```text
PASS: BLOCKED_PROPAGATION != REJECTED_COUNTERFACTUAL
PASS: BRANCH_NOT_PROVABLE != BRANCH_PROVED_IMPOSSIBLE
PASS: SURVIVOR_SYNTHESIS_REQUIRES_EXHAUSTIVE_PARTITION
PASS: REINDIVIDUATION_NEVER_UPGRADES_PROOF_LICENSE_BY_ITSELF
```

## Rejected

```text
REJECT: I.27 is used as an available rule
REJECT: visual nonintersection rejects finite closure
REJECT: missing incidence evidence rejects coincidence
REJECT: three rejected labels are sufficient if the state partition is not certified exhaustive
REJECT: all branches must use the same theorem/field to belong to one analysis
```

---

# 9. Architectural pressure

After Run13, Run14, and Run15, the common structure is now:

```text
ANALYSIS
  unresolved register
    -> certified exhaustive partition of possible worlds
    -> branch-specific host/field retrieval
    -> licensed consequence propagation
    -> typed rejection certificates

SYNTHESIS
  -> unique survivor only after all alternatives are certified rejected
```

The candidate family is therefore strengthened to:

```text
F_COUNTERFACTUAL_STATE_RECOVERY
```

with candidate capability:

```text
STATE_RECOVERY_BY_COUNTERFACTUAL_EXHAUSTION
```

and candidate invariants:

```text
EXHAUSTIVENESS_BEFORE_SYNTHESIS
CERTIFIED_REJECTION_ONLY
BLOCKED_IS_NOT_REJECTED
HETEROGENEOUS_ELIMINATORS_ALLOWED
```

Run15 does not canonicalize them automatically.

---

# 10. Experimental result

**Positive non-trichotomic stress result.**

The state-recovery morphology survives a four-world partition and mixed elimination mechanisms. The strongest interpretation is no longer "a clever converse pattern" but a general analysis/synthesis procedure over finite counterfactual state spaces:

```text
PARTITION
  -> ROUTE WORLDS TO INFORMATIVE FIELDS
  -> PROPAGATE
  -> CERTIFY REJECTIONS
  -> SYNTHESIZE UNIQUE SURVIVOR
```

The negative controls show that the procedure remains conservative when the partition is incomplete or any branch is merely blocked rather than disproved.

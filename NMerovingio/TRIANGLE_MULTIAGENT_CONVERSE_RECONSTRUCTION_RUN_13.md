# Triangle Multi-Agent Converse Reconstruction — Run 13

> **Execution mode:** CONTROLLED_DRY_RUN  
> **Status:** conceptual experiment, not autonomous software execution  
> **Input network:** canonical `N10`  
> **Hidden propositions:** Euclid I.19 and I.25 are removed from the available proof rules for this experiment.  
> **Architectural freeze:** no new operators are granted in advance. Any general converse-construction schema must emerge as an experimental candidate.

---

## 0. Experimental question

Can the current Merovingio architecture reconstruct the converse order theorems by **analysis of qualitative alternatives + disanalogy propagation + synthesis of the surviving state**?

We test two structurally parallel targets.

### OBJECT target

Given in one triangle:

```text
A = rel(angle_1, angle_2) = GT
```

resolve:

```text
S = rel(side_1, side_2) = ?
```

Available rules:

```text
I.5  : side EQ -> opposite-angle EQ
I.18 : side GT -> opposite-angle GT
```

I.19 is hidden.

### PAIR target

Given two triangles with the two carrier-side equalities required by the pair-order family:

```text
B = rel(third_side_1, third_side_2) = GT
```

resolve:

```text
H = rel(included_angle_1, included_angle_2) = ?
```

Available rules:

```text
I.4  : included-angle EQ -> third-side EQ
I.24 : included-angle GT -> third-side GT
```

I.25 is hidden.

The run asks whether the same proof morphology appears independently at OBJECT and PAIR level.

---

# 1. Guardrail inherited from N10 / Run12

The experiment distinguishes rigorously:

```text
BRANCH PROVED IMPOSSIBLE
!=
BRANCH NOT PROVABLE
```

and therefore also:

```text
BLOCKED_PROPAGATION
!=
REJECTED_COUNTERFACTUAL
```

A candidate state may be eliminated only if a proposition-licensed propagation reaches a constraint incompatible with the given state.

Failure to find a propagation is not evidence against the branch.

---

# 2. OBJECT reconstruction: hidden I.19

## 2.1 Target state

Given:

```text
A = GT
```

with qualitative source register:

```text
S ∈ {LT, EQ, GT}
```

The desired state is hidden from the agents.

## 2.2 Analysis — generate alternatives

Expansion opens the unresolved source register:

```text
Branch O-EQ : S = EQ
Branch O-LT : S = LT
Branch O-GT : S = GT
```

No branch is initially privileged.

## 2.3 Branch O-EQ

Assume:

```text
S = EQ
```

I.5 is proposition-licensed:

```text
S = EQ
  |
  | I.5
  v
A = EQ
```

But the frozen target constraint is:

```text
A = GT
```

Thus:

```text
EQ collides with GT
```

and the validator records:

```text
REJECT(O-EQ)
```

This branch is **proved impossible**, not merely unsupported.

## 2.4 Branch O-LT

Assume:

```text
S = LT
```

Swap the left/right roles. In the swapped reading:

```text
S_swapped = GT
```

I.18 applies:

```text
S_swapped = GT
      |
      | I.18
      v
A_swapped = GT
```

Returning to the original orientation:

```text
A = LT
```

But the target constraint is:

```text
A = GT
```

Therefore:

```text
REJECT(O-LT)
```

## 2.5 Synthesis

The source relation is trichotomic:

```text
S ∈ {LT, EQ, GT}
```

and we have proposition-certified rejection of:

```text
S = EQ
S = LT
```

Therefore the only surviving state is:

```text
S = GT
```

Readout:

```text
side_1 > side_2
```

This reconstructs the content of I.19 without using I.19 as an available rule.

Genealogy:

```text
angle GT given
   |
   | analyze source register
   +-> side EQ -> I.5 -> angle EQ -> collision
   |
   +-> side LT -> swap + I.18 -> angle LT -> collision
   |
   `-> side GT survives
```

---

# 3. PAIR reconstruction: hidden I.25

## 3.1 Licensing boundary

Two corresponding carrier-side equalities are frozen as proposition-licensed preconditions:

```text
carrier_1(T1) = carrier_1(T2)
carrier_2(T1) = carrier_2(T2)
```

Without them, I.4/I.24 belong to a different proof situation and this experiment must not fire.

## 3.2 Target state

Given:

```text
B = GT
```

Resolve:

```text
H ∈ {LT, EQ, GT}
```

## 3.3 Branch P-EQ

Assume:

```text
H = EQ
```

I.4 is licensed:

```text
H = EQ
  |
  | I.4
  v
B = EQ
```

but the frozen target is:

```text
B = GT
```

Hence:

```text
REJECT(P-EQ)
```

## 3.4 Branch P-LT

Assume:

```text
H = LT
```

Swap the two triangle roles:

```text
H_swapped = GT
```

I.24 gives:

```text
H_swapped = GT
      |
      | I.24
      v
B_swapped = GT
```

Returning to the original orientation:

```text
B = LT
```

which collides with:

```text
B = GT
```

Therefore:

```text
REJECT(P-LT)
```

## 3.5 Synthesis

Trichotomy plus two certified eliminations leaves:

```text
H = GT
```

Readout:

```text
included_angle_1 > included_angle_2
```

This reconstructs the content of I.25 without using I.25 as an available rule.

Genealogy:

```text
third-side GT given
   |
   | analyze source register
   +-> angle EQ -> I.4 -> third-side EQ -> collision
   |
   +-> angle LT -> swap + I.24 -> third-side LT -> collision
   |
   `-> angle GT survives
```

---

# 4. Cross-level comparison

The Genealogy Agent compares the two successful trajectories.

OBJECT:

```text
TARGET angular GT
SOURCE side ?

EQ branch --zero rule--> target EQ --collision
LT branch --order rule--> target LT --collision
GT survives
```

PAIR:

```text
TARGET metric GT
SOURCE angular ?

EQ branch --zero rule--> target EQ --collision
LT branch --order rule--> target LT --collision
GT survives
```

Although the domains are reversed, both instantiate the same higher proof morphology:

```text
QUALITATIVE_SOURCE ∈ {LT,EQ,GT}
TARGET = GT

eliminate EQ via a zero-preserving forward rule
eliminate LT via an order-preserving forward rule + role swap
synthesize GT by exhaustion
```

The Compiler Agent proposes:

```text
F_CONVERSE_BY_DISANALOGY_EXHAUSTION
```

with candidate operator pattern:

```text
CONVERSE_BY_ZERO_AND_ORDER_ELIMINATION
```

This is recorded as a **compiled cognitive candidate**, not yet canonicalized.

---

# 5. Analysis / synthesis result

Run13 gives a concrete operational form to the emerging interpretation.

## Analysis

```text
unresolved qualitative source
   -> instantiate oriented alternatives
   -> propagate each candidate through licensed families
```

Analysis is therefore not merely decomposition of the target statement; it is the generation of **counterfactual disanalogies with explicit genealogies**.

## Synthesis

```text
certified impossible branches removed
   -> surviving state recovered
```

Synthesis is a constructive recovery of the stable state after the nonzero/alternative field has been exhausted.

The important condition is:

```text
EXHAUSTION REQUIRES CERTIFIED ELIMINATION
```

not search failure.

---

# 6. Negative ablation control

To test the guardrail, repeat the OBJECT reconstruction but remove I.5 from the available rules.

Given again:

```text
A = GT
```

we can still reject:

```text
S = LT
```

via swapped I.18.

But for:

```text
S = EQ
```

there is now no licensed propagation to `A = EQ`.

Therefore the correct status is:

```text
O-EQ = UNRESOLVED
```

not:

```text
O-EQ = REJECTED
```

Hence the reasoner must return:

```text
S ∈ {EQ, GT}
UNRESOLVED
```

and must **not** reconstruct I.19.

This control passes the Run12 guardrail:

```text
BLOCKED_PROPAGATION != REJECTED_COUNTERFACTUAL
```

The same logic applies at PAIR level if I.4 is removed: the `H=EQ` branch remains unresolved and I.25 cannot be reconstructed.

---

# 7. Momentum interpretation

Each converse reconstruction is driven by two disanalogy packets converging on the same surviving orientation.

OBJECT:

```text
D_EQ -> collision
D_LT -> collision
        \
         -> pressure toward S=GT
```

PAIR:

```text
D_EQ -> collision
D_LT -> collision
        \
         -> pressure toward H=GT
```

This is a new form of combined disanalogy momentum:

```text
CONVERGENT_ELIMINATION_MOMENTUM
```

where independent rejected alternatives jointly constrain the source register toward one surviving state.

No scalar score is assigned yet.

---

# 8. Validator report

## Proposition-certified within the experiment

```text
PASS: OBJECT EQ branch is rejected via I.5.
PASS: OBJECT LT branch is rejected via role-swap + I.18.
PASS: trichotomy reconstructs OBJECT GT, i.e. I.19 content.

PASS: PAIR EQ branch is rejected via I.4, conditional on the two carrier equalities.
PASS: PAIR LT branch is rejected via role-swap + I.24.
PASS: trichotomy reconstructs PAIR GT, i.e. I.25 content.
```

## Cognitive candidates

```text
CANDIDATE: both trajectories instantiate one converse-by-exhaustion proof family.
CANDIDATE: CONVERSE_BY_ZERO_AND_ORDER_ELIMINATION should become a reusable proof-search schema.
CANDIDATE: convergent branch rejection is a distinct disanalogy-momentum topology.
```

## Rejected / guarded

```text
REJECT: a branch may be eliminated merely because no proof was found for it.
REJECT: hiding I.19/I.25 licenses importing their conclusions as axioms.
REJECT: PAIR reconstruction may ignore I.4/I.24 carrier preconditions.
REJECT: the two reconstructed theorems are genetically identical; they only share a schema description.
```

---

# 9. Experimental result

**Positive.**

Under the controlled dry-run semantics, the current N10 architecture is sufficient to reconstruct both hidden converse order results from forward zero/order rules, trichotomy, role swap, and certified branch elimination.

The strongest result is not merely the two recovered conclusions. It is the emergence of a reusable proof morphology:

```text
FORWARD ZERO RULE
+
FORWARD ORDER RULE
+
ROLE SWAP
+
TRICHOTOMY
+
CERTIFIED COUNTERFACTUAL ELIMINATION

        ↓

CONVERSE_BY_DISANALOGY_EXHAUSTION
```

The negative ablation control shows that the mechanism does not collapse into closed-world reasoning.

---

# 10. Candidate network delta — not canonical yet

```text
+ candidate F_CONVERSE_BY_DISANALOGY_EXHAUSTION
+ candidate CONVERSE_BY_ZERO_AND_ORDER_ELIMINATION
+ candidate CONVERGENT_ELIMINATION_MOMENTUM
+ genealogical reconstruction path for hidden I.19
+ genealogical reconstruction path for hidden I.25
```

Canonical graph remains at N10 pending a transfer test on a new problem family.
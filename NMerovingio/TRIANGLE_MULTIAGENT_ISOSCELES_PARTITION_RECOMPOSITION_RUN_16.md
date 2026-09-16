# Triangle Multi-Agent Isosceles Partition / Recomposition — Run 16

> **Execution mode:** CONTROLLED_DRY_RUN  
> **Status:** conceptual experiment, not autonomous software execution  
> **Input network:** canonical `N11`  
> **Architectural freeze:** `OP_REINDIVIDUATE` and `OP_RECOMPOSE_GESTALTS` are available exactly as canonicalized. No `PARTITION` operator is granted in advance.  
> **Historical note:** this is an architectural isosceles/congruence test, not a claim to reproduce Euclid's exact historical proof of I.5.

---

## 0. Experimental question

Run10–12 showed that `OP_REINDIVIDUATE` can change cognitive role-domain reading without changing material identity. The user noted that a similar movement appears when one geometric object is read as two triangles, those triangles are compared by a congruence criterion, and the result is returned to the original object.

Run16 asks:

> Is `OP_REINDIVIDUATE` already sufficient for this one-object -> two-subtriangles -> congruent pair -> one-enriched-object trajectory, or does the experiment force a new distinction between **cognitive re-individuation** and **material subworkspace extraction**?

The target is deliberately simple so the representational issue is isolated.

---

# 1. Frozen material workspace

Start with an isosceles triangle:

```text
ABC
AB = AC
```

A construction supplies a point `D` on the base `BC` such that:

```text
D lies on BC
BD = DC
```

and joins:

```text
AD
```

This produces a material parent workspace:

```text
W_ISOSCELES_SPLIT

        A
       /|\
      / | \
     /  |  \
    B---D---C
```

The construction facts are frozen as licensed input for this architectural experiment. We do not test how the midpoint/bisecting construction itself is discovered.

The target is:

```text
angle ABC = angle ACB
```

---

# 2. Candidate subworkspaces already present in the material scene

The construction visibly supports two triangle configurations:

```text
T_L = triangle ABD
T_R = triangle ACD
```

They overlap materially:

```text
shared vertices: A, D
shared carrier: AD
parent boundary: B-D-C are collinear on BC
```

Metric packet:

```text
AB = AC        [parent isosceles seed]
BD = DC        [construction seed]
AD = AD        [common carrier]
```

Therefore, **if** `T_L` and `T_R` are proposition-licensed as two material triangle realizations, I.8 / SSS can certify:

```text
T_L congruent T_R
```

and in particular:

```text
angle ABD = angle ACD
```

Because `D` lies on `BC`, the local angle roles coincide with the parent base-angle roles:

```text
angle ABD = angle ABC
angle ACD = angle ACB
```

so the parent target follows.

The experiment is not about whether this geometry is valid; it is about how the current cognitive architecture represents the transitions.

---

# 3. Stage A — attempt with OP_REINDIVIDUATE alone

The Reorganization Agent starts from one material object:

```text
W_ISOSCELES_SPLIT
```

and detects the two candidate triangle readings.

A tempting move is:

```text
OP_REINDIVIDUATE(EXTERNALIZE)
  W_ISOSCELES_SPLIT
    -> [T_L, T_R]
```

The validator stops this interpretation **if** it is read as material generation.

Canonical N10 semantics say that `OP_REINDIVIDUATE`:

```text
changes cognitive individuation / role-domain reading
preserves material identity
may create a shared schema
never upgrades proof license by itself
```

It does **not** currently specify:

```text
create material subworkspace
assign material owners to local roles
record shared boundary / overlap
certify that each local role belongs to one actual triangle
```

Therefore:

```text
PASS:
OP_REINDIVIDUATE may redescribe the parent as supporting two aligned triangle schemas.

REJECT:
OP_REINDIVIDUATE alone creates the proposition-licensed material triangles required by I.8.
```

New distinction exposed:

```text
COGNITIVE_REINDIVIDUATION
!=
MATERIAL_SUBWORKSPACE_EXTRACTION
```

This is the first major result of Run16.

---

# 4. Stage B — freeze the construction-derived material subworkspaces

For the remainder of the run, the validator is allowed to read the already constructed scene itself and register:

```text
W_TL = material subworkspace triangle ABD
W_TR = material subworkspace triangle ACD
```

with explicit parent map:

```text
parent(W_TL) = W_ISOSCELES_SPLIT
parent(W_TR) = W_ISOSCELES_SPLIT
```

and overlap map:

```text
overlap(W_TL, W_TR) = segment AD + vertices A,D
```

This registration is treated as **input bookkeeping**, not as a new canonical operator.

Once the owner map is explicit, the pair workspace is proposition-licensed:

```text
W_PAIR(T_L,T_R)
```

The three SSS equalities are all material/proposition-readable:

```text
AB = AC
BD = DC
AD = AD
```

Now I.8 can fire.

---

# 5. Stage C — congruence completion

Completion Agent activates the known pair-congruence packet:

```text
SSS_ZERO_MASK
  side_1 = EQ
  side_2 = EQ
  side_3 = EQ
```

I.8 licenses:

```text
G_PAIR_COINCIDENCE(T_L,T_R)
```

and exposes corresponding angular equality:

```text
angle ABD = angle ACD
```

Important genealogical record:

```text
parent object
  -> construction-derived local material triangles
  -> pair correspondence workspace
  -> I.8 congruence completion
  -> local angular equality
```

No identity of distinct material points is asserted.

---

# 6. Stage D — return to the parent object

The proof is not complete merely because the pair workspace has an angular equality. The result must be interpreted back in the parent triangle.

The current network already contains:

```text
OP_RECOMPOSE_GESTALTS
```

which was learned in the zero-recomposition experiments as a local-to-richer-host operator preserving contacts and exposing resulting global registers.

Run16 tests whether it can serve here without inventing a new recomposition operator.

Input:

```text
local readout:
  angle ABD = angle ACD

preserved contacts:
  D lies on BC
  ray BD is the B->C base ray
  ray CD is the C->B base ray

parent host:
  W_ISOSCELES_SPLIT
```

Recomposition succeeds at the **cognitive/proof bookkeeping level**:

```text
angle ABD -> parent role angle ABC
angle ACD -> parent role angle ACB
```

therefore:

```text
angle ABC = angle ACB
```

This is not a new geometric theorem produced by `OP_RECOMPOSE_GESTALTS`; the equality is already proposition-certified locally by I.8 and the parent-role identification is licensed by incidence/collinearity.

Thus:

```text
RECOMPOSITION PRESERVES PROOF LICENSE
IT DOES NOT CREATE IT
```

---

# 7. Architectural result

The one-object -> pair -> one-object cycle is therefore only **partially** captured by `OP_REINDIVIDUATE`.

The successful trajectory is:

```text
PARENT MATERIAL WORKSPACE
        |
        | construction creates internal carrier AD
        v
MATERIAL SUBWORKSPACES T_L / T_R
        |
        | pair assembly
        v
PAIR CONGRUENCE GESTALT
        |
        | I.8
        v
LOCAL ANGULAR READOUT
        |
        | OP_RECOMPOSE_GESTALTS + parent role map
        v
ENRICHED PARENT WORKSPACE
```

The missing operation is not another semantic mode of `REINDIVIDUATE`.

It is a candidate operation that explicitly registers substructure in a material workspace:

```text
candidate OP_PARTITION_WORKSPACE
```

Minimal semantics suggested by the run:

```text
OP_PARTITION_WORKSPACE(parent, construction_carriers)
  -> material subworkspaces[]
  -> owner maps
  -> overlap maps
  -> boundary-role maps
  -> preserved-contact ledger
```

No canonical promotion occurs in Run16.

---

# 8. Why this is stronger than the old INTERNALIZE / EXTERNALIZE picture

The earlier picture could suggest:

```text
one triangle
  -> EXTERNALIZE
pair of triangles
  -> INTERNALIZE
one triangle
```

Run16 shows that this collapses two different operations:

```text
A. cognitive re-individuation
   who/what is being treated as one schema or two role domains?

B. material subworkspace extraction
   which actual points, segments, incidences and overlaps constitute each proof object?
```

The correct architecture needs both.

Hence:

```text
REINDIVIDUATE answers:
  "How is the same material support cognitively individuated?"

PARTITION_WORKSPACE would answer:
  "Which proposition-licensed subconfigurations exist inside this material support?"
```

This distinction preserves the N10 anti-leakage barrier rather than weakening it.

---

# 9. Negative controls

## 9.1 Missing BD = DC

If the construction does not certify:

```text
BD = DC
```

then SSS is incomplete.

Correct result:

```text
PAIR CONGRUENCE BLOCKED
```

not:

```text
PAIR CONGRUENCE REJECTED
```

and not base-angle equality.

## 9.2 Cognitive schemas without material owners

If `T_L` and `T_R` exist only as re-individuated schemas but do not carry explicit material owner maps, I.8 cannot fire.

```text
SCHEMA TRIANGLES != PROPOSITION-LICENSED MATERIAL TRIANGLES
```

## 9.3 Missing collinearity / parent-role map

Even if local congruence proves:

```text
angle ABD = angle ACD
```

without `D` certified on `BC` the local angles cannot simply be renamed as the parent base angles.

Correct result:

```text
LOCAL EQUALITY PROVED
PARENT TARGET UNRESOLVED
```

This guards against illegal local-to-global role transport.

---

# 10. Momentum interpretation

The run produces a new kind of representational pressure.

The parent isosceles workspace contains enough material organization for two congruent substructures to become salient, but the current cognitive operator cannot by itself make those substructures proposition-addressable.

Pressure chain:

```text
one-object Gestalt
  -> construction introduces internal carrier
  -> two strong local triangle readings appear
  -> congruence affordance is visible
  -> proof license remains unavailable without material owner maps
  -> representational deficiency detected
  -> PARTITION_WORKSPACE candidate
```

This is a genuine **reorganization impetus generated by blocked proof affordance**.

The block is productive: it identifies exactly which representational layer is missing.

---

# 11. Validator report

## Proposition-certified under frozen construction facts

```text
PASS: AB = AC
PASS: BD = DC
PASS: AD is common
PASS: material triangles ABD and ACD satisfy SSS
PASS: I.8 certifies pair congruence once those material subworkspaces are registered
PASS: corresponding local base angles are equal
PASS: D on BC identifies the local angular roles with the parent base-angle roles
PASS: parent target angle ABC = angle ACB
```

## Cognitive architecture

```text
PASS: OP_REINDIVIDUATE may expose the two-role-domain reading
PASS: OP_RECOMPOSE_GESTALTS may carry a licensed local readout back into the parent when preserved contacts are explicit
REJECT: OP_REINDIVIDUATE alone materializes proposition-licensed subtriangles
CANDIDATE: OP_PARTITION_WORKSPACE should register construction-induced material subspaces and their overlap/owner/boundary maps
```

## Guardrails preserved

```text
COGNITIVE_REINDIVIDUATION != MATERIAL_SUBWORKSPACE_EXTRACTION
SCHEMA_MATCH != PROPOSITION_APPLICATION
BLOCKED_PROPAGATION != REJECTED_COUNTERFACTUAL
LOCAL_READOUT != PARENT_READOUT without a licensed role map
```

---

# 12. Experimental result

**Positive representational stress result.**

Run16 shows that the N10 re-individuation generalization was correctly kept weak. It is useful for changing cognitive individuation, but it should not absorb the materially different act of carving proposition-addressable subworkspaces out of a construction.

The experiment therefore produces a high-value candidate:

```text
OP_PARTITION_WORKSPACE
```

while validating reuse of the existing:

```text
OP_RECOMPOSE_GESTALTS
```

for the return path, provided material contacts and parent-role maps are explicit.

The conceptual cycle becomes:

```text
CONSTRUCTION
  -> PARTITION PRESSURE
  -> LOCAL MATERIAL WORKSPACES
  -> CONGRUENCE COMPLETION
  -> LOCAL READOUT
  -> RECOMPOSE
  -> ENRICHED PARENT
```

This candidate should be stress-tested negatively before any canonical promotion.

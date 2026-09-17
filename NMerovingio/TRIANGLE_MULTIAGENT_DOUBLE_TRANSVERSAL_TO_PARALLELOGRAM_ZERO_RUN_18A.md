# Triangle Multi-Agent Double-Transversal -> Parallelogram Zero — Run 18A

> **Execution mode:** CONTROLLED_DRY_RUN  
> **Status:** conceptual experiment, not autonomous software execution  
> **Input network:** canonical `N12`  
> **Architectural freeze:** `OP_REINDIVIDUATE`, `OP_PARTITION_WORKSPACE`, `OP_RECOMPOSE_GESTALTS`, `F_COUNTERFACTUAL_STATE_RECOVERY`, and the existing transversal/parallel families are available. No new parallelogram-zero family is granted in advance.

---

## 0. Experimental question

Start from one certified pair of parallel carriers and **two distinct transversals** crossing both. Can Merovingio, by comparing the two oriented finite-closure possibilities with the distributed-nonclosure state of the transversal pair, discover a new higher Gestalt in which a parallelogram is the **analogical/disanalogical zero** of the triangle-producing closure family?

The intended result is not supplied as a theorem label.

---

# 1. Material workspace

Freeze:

```text
p || q
```

and two distinct transversals:

```text
t_L intersects p at A and q at D
t_R intersects p at B and q at C
```

with the bounded cell:

```text
A-----B   on p
|     |
D-----C   on q
```

The vertical depiction is only schematic; `t_L` and `t_R` are not assumed parallel.

The material workspace is:

```text
W_DOUBLE_TRANSVERSAL_STRIP
```

with certified ownership:

```text
A,B in p
D,C in q
A,D in t_L
B,C in t_R
p || q
```

The target register is the closure topology of the transversal pair:

```text
C_t = closure_topology(t_L,t_R)
```

Because the transversals are frozen distinct, coincidence is excluded.

Candidate states:

```text
FINITE_CLOSURE_LEFT
DISTRIBUTED_NONCLOSURE
FINITE_CLOSURE_RIGHT
```

---

# 2. Non-zero branches as triangle hosts

If:

```text
C_t = FINITE_CLOSURE_LEFT
```

then `t_L` and `t_R` meet at a finite point `X_L` on one side of the parallel strip. The same material carriers admit triangle hosts with bases on `p` and `q`.

Likewise:

```text
C_t = FINITE_CLOSURE_RIGHT
```

produces the orientation-swapped finite apex `X_R` and the corresponding triangle-host family.

The two finite-closure states are related by side/orientation swap:

```text
sigma(FINITE_LEFT) = FINITE_RIGHT
sigma(FINITE_RIGHT) = FINITE_LEFT
```

Neither branch is treated as erroneous. They are stable non-zero realizations of the transversal-pair closure family.

---

# 3. Expansion / disanalogy reading

The Expansion Agent reads finite closure as an oriented deformation away from distributed nonclosure:

```text
D_L = transversal pair closes left
D_R = transversal pair closes right
```

Each deformation creates a finite apex and therefore a triangle-producing host.

Genealogically:

```text
transversal pair
   -> finite closure orientation
   -> triangle host
   -> ordered angular / incidence consequences
```

The important point is structural:

```text
LEFT and RIGHT closure are mutually swapped disanalogical states.
```

This creates pressure to ask whether the closure family possesses a swap-fixed center.

---

# 4. Candidate zero of the closure family

The Reorganization Agent compares:

```text
FINITE_LEFT <-> FINITE_RIGHT
```

under orientation swap.

The state:

```text
DISTRIBUTED_NONCLOSURE
```

is invariant under the same left/right swap because no finite apex occurs on either side.

Therefore the run proposes:

```text
Z_TRANSVERSAL_PAIR_NONCLOSURE
```

with:

```text
zero_condition:
  closure_topology(t_L,t_R) = DISTRIBUTED_NONCLOSURE

fixed_by:
  SWAP_CLOSURE_SIDE
```

This is a **topological zero**, not a metric equality zero.

Hence:

```text
FINITE_LEFT  <->  ZERO/NONCLOSURE  <->  FINITE_RIGHT
```

is the discovered family organization.

Candidate family:

```text
F_TRANSVERSAL_PAIR_CLOSURE
```

---

# 5. Emergence of the double-parallel cell

The parent workspace already contains:

```text
p || q
```

If the transversal-pair register occupies its discovered zero:

```text
t_L || t_R
```

then the bounded four-edge cell has two opposite direction classes:

```text
p || q
t_L || t_R
```

The cognitive layer compiles:

```text
G_DOUBLE_PARALLEL_CELL
```

The human semantic layer may identify this as a **parallelogram**.

Crucially, the run does not define the parallelogram by arbitrary naming. It reaches it as:

```text
existing parallel family
+
zero of transversal-pair closure family
```

Thus, relative to `F_TRANSVERSAL_PAIR_CLOSURE`:

```text
PARALLELOGRAM = ZERO REALIZATION
```

while relative to the previously compiled `F_PARALLELOGRAM_PRODUCT` the same material object can be an ordinary non-zero/generic member unless further metric/angular zero conditions hold.

This yields:

```text
CANONICALITY_IS_FAMILY_RELATIVE
```

and more strongly:

```text
ZERO_STATUS_IS_GESTALT_RELATIVE
```

---

# 6. Relation to triangles between parallels

The finite non-zero states produce triangle hosts because the two transversals meet. The zero state suppresses finite triangular closure while preserving the same four carriers and the same parallel strip.

So the discovered conceptual trajectory is:

```text
TRIANGLE-PRODUCING LEFT CLOSURE
          \
           \
            DISTRIBUTED ZERO
           /
          /
TRIANGLE-PRODUCING RIGHT CLOSURE
```

The parallelogram cell is therefore read as the **zero / fixed realization of the same material strip after the two possible oriented triangle closures have been neutralized**.

This is a cognitive-family statement, not a claim that Euclid historically defined parallelograms this way.

---

# 7. Analogy / disanalogy momentum

The two finite branches generate disanalogy momentum in opposite orientations:

```text
D_LEFT  -> finite apex left  -> triangle host
D_RIGHT -> finite apex right -> triangle host
```

Their symmetry produces analogy momentum:

```text
same closure mechanism
same material strip
opposite orientation
```

The combined pressure yields a fixed-state search:

```text
opposed disanalogies
  -> detect swap action
  -> search fixed realization
  -> distributed nonclosure
  -> compile topological zero
```

This is the main conceptual result of Run18A.

---

# 8. Validator boundaries

```text
PASS: p || q is frozen input
PASS: t_L,t_R distinct and each intersects both p,q
PASS: finite closure on either side creates a finite triangle-producing host
PASS: left/right finite closures are exchanged by orientation swap
PASS: distributed nonclosure is fixed under closure-side swap
PASS: if t_L,t_R occupy distributed nonclosure then the cell has two opposite parallel pairs
```

Rejected shortcuts:

```text
REJECT: visual near-parallelism counts as distributed nonclosure
REJECT: inability to draw the finite apex proves nonclosure
REJECT: one finite-closure rejection alone identifies the zero
REJECT: the parallelogram is a zero in every family
```

---

# 9. Experimental result

**Positive conceptual result.**

The run discovers a new candidate family:

```text
F_TRANSVERSAL_PAIR_CLOSURE
```

with a topological zero:

```text
Z_TRANSVERSAL_PAIR_NONCLOSURE
```

and a higher Gestalt:

```text
G_DOUBLE_PARALLEL_CELL
```

The human semantic layer identifies the latter as a parallelogram.

Most importantly:

```text
PARALLELOGRAM
= zero of an oriented triangle-producing transversal-closure family
```

relative to this Gestalt organization.

No canonical promotion occurs in Run18A.
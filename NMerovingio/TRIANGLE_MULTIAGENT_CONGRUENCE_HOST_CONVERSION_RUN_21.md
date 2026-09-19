# Triangle Multi-Agent Congruence Host-Conversion Taxonomy — Run 21

> **Execution mode:** CONTROLLED_DRY_RUN  
> **Status:** conceptual experiment, not autonomous software execution  
> **Input network:** canonical `N12` + non-canonical candidates from Runs 18A/18B, Run19 (ASA), Run20 (SAS)  
> **Architectural freeze:** no new Euclidean proposition is granted. The experiment only compares already-licensed congruence access masks (ASA, SAS/I.4, SSS/I.8), I.27/I.29 parallel entry/exit behavior, the diagonal partition, and correspondence completion after congruence.

---

## 0. Experimental question

Use the **same parallelogram / double-nonclosure host with diagonal AC** and compare all three congruence criteria under one fixed material realization.

The goal is not to ask which criterion is "stronger."

The goal is to discover whether the criteria have distinct **host-conversion signatures** between:

```text
T = TOPOLOGICAL / DIRECTIONAL ZERO
M = METRIC ZERO
I = MATERIAL IDENTITY BRIDGE
C = PAIR COINCIDENCE / CONGRUENCE
```

Run19 already suggested:

```text
ASA = T + T + I -> C
```

Run20 suggested:

```text
SAS = T + M + I -> C -> completion of the missing T/M coordinate
```

Run21 adds SSS and asks whether all three fit one higher organization.

---

# 1. Shared parent workspace

Freeze one closed four-edge workspace:

```text
A------B
| \    |
|  \   |
|   \  |
D------C
```

with diagonal:

```text
AC
```

and two material triangle subworkspaces:

```text
T1 = triangle ABC
T2 = triangle CDA
```

The shared material bridge is always:

```text
I := AC = CA
```

The parent has two possible topological registers:

```text
T1_top := AB || CD
T2_top := AD || BC
```

and two possible opposite-side metric registers:

```text
M1 := AB = CD
M2 := AD = BC
```

These four registers are deliberately kept distinct.

---

# 2. Domain map induced by the diagonal

The diagonal AC turns the parent registers into local triangle-pair coordinates.

Topological registers project through I.29:

```text
T1_top
  AB || CD
    -> angle BAC = angle DCA
    -> A1

T2_top
  AD || BC
    -> angle BCA = angle DAC
    -> A2
```

Metric registers project directly:

```text
M1
  AB = CD
    -> S1

M2
  AD = BC
    -> S2
```

Material identity provides:

```text
I
  AC = CA
    -> S_shared
```

So the same parent host offers a local coordinate system:

```text
(A1, A2, S1, S2, I)
```

where angle coordinates are genealogically topological and side coordinates are genealogically metric.

---

# 3. ASA channel

Input:

```text
T1_top + T2_top + I
```

projects to:

```text
A1 + A2 + I
```

which is an ASA mask.

Therefore:

```text
T + T + I
 -> ASA
 -> C
```

Correspondence completion after congruence returns:

```text
M1
M2
```

as opposite-side metric equalities.

Thus the full host-conversion signature is:

```text
ASA:
(T,T) + I
  -> C
  -> (M,M)
```

or:

```text
TOPOLOGY COMPLETE
  -> CONGRUENCE
  -> METRIC COMPLETE
```

The topological information remains available; congruence enriches the parent with the complementary metric packet.

---

# 4. SAS channel A

Input:

```text
T1_top + M1 + I
```

projects to:

```text
A1 + S1 + I
```

which is a SAS mask.

Therefore:

```text
T + M + I
 -> SAS
 -> C
```

Correspondence completion returns:

```text
M2
A2
```

and A2 can certify via I.27:

```text
T2_top
```

Hence:

```text
SAS-A:
(T1,M1) + I
  -> C
  -> (T2,M2)
```

The symmetric channel is:

```text
SAS-B:
(T2,M2) + I
  -> C
  -> (T1,M1)
```

So SAS is a **mixed-domain completion bridge**.

It consumes one topology-metric pair and completes the complementary topology-metric pair.

---

# 5. SSS channel

Now supply the two metric registers:

```text
M1 + M2 + I
```

that is:

```text
AB = CD
AD = BC
AC = CA
```

This is an SSS mask for the two diagonal subtriangles.

Therefore:

```text
M + M + I
 -> SSS / I.8
 -> C
```

Correspondence completion yields the two angular equalities:

```text
A1:
angle BAC = angle DCA

A2:
angle BCA = angle DAC
```

Under the preserved parent role layout, I.27 certifies:

```text
AB || CD
AD || BC
```

Thus:

```text
SSS:
(M,M) + I
  -> C
  -> (T,T)
```

or:

```text
METRIC COMPLETE
  -> CONGRUENCE
  -> TOPOLOGY COMPLETE
```

This is the exact domain-dual of the ASA realization.

---

# 6. Emergent conversion table

The three access masks now have a common host-relative description:

| Criterion | Input domains (besides I) | Pair coincidence | Complementary completion |
|---|---|---|---|
| ASA | T + T | C | M + M |
| SAS | T + M | C | M + T |
| SSS | M + M | C | T + T |

In compressed notation:

```text
ASA : TT + I -> C -> MM
SAS : TM + I -> C -> MT
SSS : MM + I -> C -> TT
```

where the SAS channel is orientation-sensitive but symmetric under pair swap.

This suggests a candidate higher organization:

```text
F_CONGRUENCE_HOST_CONVERSION
```

with one fixed bridge:

```text
I = shared material carrier
```

and two variable source-domain slots:

```text
slot_1 in {T,M}
slot_2 in {T,M}
```

The congruence criterion records which domain inhabits each slot before pair coincidence.

---

# 7. Pair coincidence as a cross-domain completion operator

Previously:

```text
G_PAIR_COINCIDENCE
```

was mainly stored as the common target reached by SAS / ASA / SSS.

Run21 suggests a richer interpretation inside this host:

```text
PAIR COINCIDENCE
= completion environment that makes all corresponding
metric and angular coordinates readable once one valid
access mask has certified the pair.
```

Because angular coordinates can be lifted back to topology through I.27, the local congruence zero can mediate:

```text
TOPOLOGY <-> METRIC
```

through the diagonal triangle pair.

Important:

```text
PAIR COINCIDENCE IS NOT ITSELF A T<->M THEOREM.
```

The conversion requires:

```text
parent role maps
+ diagonal partition
+ proposition licenses
+ projection/recomposition
```

Candidate capability:

```text
CROSS_DOMAIN_COMPLETION_THROUGH_CONGRUENCE
```

---

# 8. A two-bit lattice appears

Ignoring the fixed identity bridge I, the parent provides two independent domain slots.

Each slot can be entered topologically or metrically:

```text
(T,T)
(T,M)
(M,T)
(M,M)
```

The two mixed states are the two orientations of SAS.

Thus the criteria form not merely a list but a small domain lattice:

```text
          TT
       /      \
     TM        MT
       \      /
          MM
```

with:

```text
TT = ASA realization
TM = SAS channel A
MT = SAS channel B
MM = SSS realization
```

The lattice is not an order of logical strength.

It is a space of **genealogical source combinations**.

Pair coincidence acts as the common completion center reachable from every fully licensed corner.

Candidate structure:

```text
G_CONGRUENCE_DOMAIN_LATTICE
```

Status: COGNITIVE_CANDIDATE.

---

# 9. Analogy and disanalogy inside the lattice

A single domain substitution transforms one congruence realization into another.

Example:

```text
TT
 -- replace second T by M -->
TM
```

cognitively:

```text
ASA-like host packet
 -> lose one topological zero
 -> introduce corresponding metric anchor
 -> SAS-like host packet
```

Likewise:

```text
TM
 -- replace first T by M -->
MM
```

gives an SSS-like packet.

This produces a new kind of disanalogy:

```text
DOMAIN-SOURCE DISANALOGY
```

The local equality pattern may still look like a congruence mask, but its coordinates have different genealogical sources.

Therefore:

```text
MASK SHAPE IDENTITY
!=
GENEALOGICAL SOURCE IDENTITY
```

This is a direct analogue of the earlier:

```text
STATE_IDENTITY != GENETIC_IDENTITY
```

but now applied coordinate-wise inside theorem access masks.

---

# 10. Break propagation by criterion

The lattice predicts different failure signatures.

### ASA corner TT

Break one topological zero:

```text
TT -> ?T
```

one angle coordinate loses its license; ASA blocks.

### SAS corner TM

Break the T coordinate:

```text
TM -> ?M
```

the included-angle coordinate loses its license.

Break the M coordinate:

```text
TM -> T?
```

the non-shared side coordinate loses its license.

### SSS corner MM

Break one metric zero:

```text
MM -> ?M
```

one side coordinate loses its license; SSS blocks.

In all cases:

```text
I = shared diagonal identity
```

remains unaffected unless material ownership itself is broken.

Thus each criterion has a distinct **disanalogy signature** inherited from its source-domain signature.

---

# 11. Ontological improvement proposal

The congruence family should no longer represent an access mask only as:

```text
ASA
SAS
SSS
```

with flat symbolic slots.

Candidate richer record:

```text
CONGRUENCE_ACCESS_REALIZATION {
    criterion
    material_host
    partition_genealogy
    shared_identity_bridge
    coordinate_sources[]
    host_conversion_signature
    completion_readouts[]
    reverse_host_routes[]
    disanalogy_signature[]
}
```

For the parallelogram-diagonal host:

```text
ASA:
  sources = [TOPOLOGY, TOPOLOGY, IDENTITY]
  output_enrichment = [METRIC, METRIC]

SAS:
  sources = [TOPOLOGY, METRIC, IDENTITY]
  output_enrichment = [METRIC, TOPOLOGY]

SSS:
  sources = [METRIC, METRIC, IDENTITY]
  output_enrichment = [TOPOLOGY, TOPOLOGY]
```

This is a genuine ontology improvement: theorem criteria become **host-relative conversion patterns**, not only proof masks.

---

# 12. Validator report

Validated under the frozen host and proposition licenses:

```text
PASS: TT + I supplies ASA via two I.29 angular projections
PASS: TM + I supplies SAS when the T and M coordinates correspond to the same side-pair orientation
PASS: MM + I supplies SSS
PASS: congruence completion returns all corresponding side/angle equalities
PASS: returned alternate-angle equalities may recover missing parallel pairs via I.27
PASS: ASA and SSS are domain-dual in this specific host realization
PASS: the two SAS orientations occupy the mixed-domain corners
```

Rejected:

```text
REJECT: ASA/SAS/SSS are globally equivalent to TT/TM/MM in every geometry
REJECT: metric equality and parallelism are interchangeable facts
REJECT: pair coincidence alone proves parallelism without preserved role placement
REJECT: the lattice is an ordering of theorem strength
REJECT: identical equality masks imply identical genealogy
```

---

# 13. Main result

Run21 discovers a compact host-relative taxonomy:

```text
ASA = TT + I -> C -> MM
SAS = TM + I -> C -> MT
SSS = MM + I -> C -> TT
```

with the second SAS orientation supplying the mirrored `MT -> TM` channel.

This yields three strong candidates:

```text
F_CONGRUENCE_HOST_CONVERSION
G_CONGRUENCE_DOMAIN_LATTICE
CROSS_DOMAIN_COMPLETION_THROUGH_CONGRUENCE
```

The deepest consequence is:

```text
CONGRUENCE CRITERIA ARE NOT ONLY DIFFERENT MINIMAL MASKS.

IN A RICH HOST THEY CAN BE DIFFERENT
GENEALOGICAL CONVERSION SIGNATURES
BETWEEN TOPOLOGICAL, METRIC,
AND MATERIAL-IDENTITY STRUCTURE.
```

No canonical promotion occurs in Run21.

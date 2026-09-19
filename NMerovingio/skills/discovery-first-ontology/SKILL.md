# Merovingio Discovery-First Ontology Skill

## Purpose

Use this skill for **all Merovingio conceptual experiments, family injections, analogy/disanalogy work, Gestalt rewrites, ontology changes, and experiment design**.

Its purpose is to prevent a recurrent failure mode:

> importing theorem-prover / verification-first habits into the discovery phase, then inventing new operators whenever a new relation or proof-path appears.

Merovingio is not being developed primarily as a rule engine that blindly combines premises. Its central object of study is the **evolution of families of Gestalten, their genealogies, their multi-realizations, and the ontologies that emerge from repeated conceptual reorganization**.

In the current research phase, **we are not trying to construct proofs at all**. Formalization is used only at a high level to double-check coherence with Merovingio's own evolving conceptual system.

---

# 1. Core stance

## 1.1 Discovery before certification

Default direction:

```text
RICH GESTALT / CONSTRUCTIVE WORKSPACE
        ↓
partializations, breaks, deformations, rebasings
        ↓
multiple simultaneous family readings
        ↓
analogy / disanalogy pressure
        ↓
family deformation / family merger / family split
        ↓
ontology improvement
        ↓
stabilization / compilation
        ↓
MUCH LATER, IN A DIFFERENT PHASE:
proof certification / Euclidean compilation
```

Do **not** make proof availability the main engine of exploration.

A future proof layer may certify a discovery. It must not determine the imagination, ontology, or trajectory of discovery in the present phase.

## 1.2 Current phase gate: cognitive unification only

The present phase is explicitly:

```text
COGNITIVE / UNIFICATION PHASE
```

not:

```text
THEOREM-PROVING PHASE
```

Therefore the central questions are:

```text
How do Gestalt families change?

How does the same structure appear in several families?

Which old concepts become special cases of a richer ontology?

Which analogies force family mergers, splits, or new coordinates?

Which disanalogies reveal hidden dimensions?

What remains invariant when the conceptual reading changes?
```

Do not ask by default:

```text
Can this already be proved?
Which Euclidean proposition licenses this step?
Is there a complete proof path?
```

Those questions belong to a later phase unless they are needed for a coarse consistency check.

---

# 2. Role of formalization in the current phase

Formalization is presently **meta-formalization**, not proof formalization.

Its job is to check the internal coherence of the evolving cognitive architecture.

Use it for high-level double checks such as:

```text
MATERIAL IDENTITY CONSISTENCY
FAMILY MEMBERSHIP CONSISTENCY
GENEALOGY CONSISTENCY
MULTI-REALIZATION CONSISTENCY
ROLE / OWNER-MAP CONSISTENCY
ZERO / FIXED-STATE CONSISTENCY
NO ACCIDENTAL CONCEPT DUPLICATION
NO SILENT CHANGE OF WORKSPACE
NO CONTRADICTION BETWEEN TWO REPRESENTATIONS
```

Formalization may ask:

```text
Can these two family descriptions coexist?

Are we accidentally identifying two materially distinct objects?

Did we call the same phenomenon two different concepts?

Does a proposed family refinement preserve earlier successful readings?

Does the same Gestalt retain a coherent genealogy across several families?
```

It should **not** ask:

```text
Have we proved this theorem from axioms?

Is every cognitive step proposition-licensed?

Can Lean / Tarski / Euclid certify this trajectory now?
```

unless we explicitly switch research phases.

The current relation is:

```text
COGNITIVE DISCOVERY
        ↓
HIGH-LEVEL FORMAL COHERENCE CHECK

not

FORMAL PROOF RULES
        ↓
ALLOWED COGNITIVE DISCOVERY
```

Formalization is a **shadow / audit layer** around the conceptual system, not its generative core.

---

# 3. Anti-pattern to avoid

Do not default to:

```text
new phenomenon
→ name a relation
→ invent OP_X
→ add guardrail
→ ask whether the theorem is licensed
→ freeze
```

This overproduces operators and reproduces the latent ontology of theorem provers.

Instead ask first:

```text
Is this really a new primitive operation?

Or is it:
- a new state of an existing family?
- a new realization of the same Gestalt?
- a family-relative reading?
- a genealogy change?
- a projection between existing families?
- a family split / merge / refinement?
- the same structure appearing under a different ontology?
```

**Operator creation is the last resort.**

---

# 4. What counts as a true operator

A candidate should become an `OP_*` only if all of the following are plausibly true:

1. It describes a **content-independent cognitive/material move**, not one geometric theorem.
2. Existing operators cannot generate the phenomenon as a path.
3. The deficiency appears in **multiple geometrically distinct contexts**, not one local example.
4. Representing it only as a family relation, realization map, genealogy, or derived path would lose essential structure.
5. The operator changes what transformations are available to the system, rather than merely naming what happened.

Provisional small kernel:

```text
BREAK
REBASE
REINDIVIDUATE
PARTITION_WORKSPACE
HOST
PROJECT
RECOMPOSE_GESTALTS
DECOMPILE
COMPILE / STABILIZE
COMPLETE
```

This list is not sacred. The important rule is **kernel pressure toward smallness**.

Examples of things that should normally *not* become operators by default:

```text
ZERO_TRANSDUCTION_BY_HOST_PROJECTION
SAS_TOPOLOGICAL_COMPLETION_BRIDGE
CROSS_DOMAIN_HOST_COMPLETION
HOST_CONVERSION_SIGNATURE
DOMAIN_SOURCE_DISANALOGY
```

These are more naturally relations, family structures, realization signatures, or derived trajectories unless future evidence forces otherwise.

---

# 5. The primary unit: multi-realization of a Gestalt

Do not assume:

```text
one Gestalt = one family = one concept
```

Prefer:

```text
GESTALT G
  material_support = W

  realizations:
    in F1 -> state / zero / role
    in F2 -> state / zero / role
    in F3 -> host / projection / member
    ...
```

The same material/cognitive organization may be:

- a zero in one family,
- a generic state in another,
- a host in a third,
- a projection of a richer object in a fourth,
- a stabilized concept only after several such readings converge.

Therefore always track:

```text
STATE_IDENTITY
GENETIC_IDENTITY
FAMILY_MEMBERSHIP
REALIZATION_TOPOLOGY
MATERIAL_SUPPORT
ROLE_ASSIGNMENT
```

as distinct dimensions.

---

# 6. Family-first experimental protocol

For a new experiment, follow this order.

## Stage A — Inject a rich Gestalt

Start from the strongest meaningful workspace/figure/configuration.

Do **not** reduce it immediately to theorem-premise atoms.

Record its current material support and known Gestalt readings.

## Stage B — Map current family memberships

Ask:

```text
Where does this same Gestalt already live?

In which families is it:
- central?
- zero?
- generic?
- unstable?
- a host?
- a projection?
- a boundary case?
```

## Stage C — Deform it

Apply controlled:

```text
BREAK
REBASE
PARTIALIZATION
REINDIVIDUATION
PARTITION when materially warranted
```

Track which family coordinates change together and which remain invariant.

## Stage D — Look for cross-family echoes

Ask:

```text
Does a deformation in F1 reappear as a familiar structure in F2?

Does a zero in F1 become a generic state in F2?

Does a Gestalt previously treated as another concept appear as a different realization of the same deeper family?

Do several old categories become regions of one richer family?
```

## Stage E — Prefer ontology change

Before naming anything new, ask whether the result demands:

- family refinement,
- family expansion,
- family merge,
- family split,
- new coordinate axis,
- new realization topology,
- new shared host,
- reclassification of existing concepts,
- one concept becoming a special case of a larger organization.

Strong analogy should often produce one of these.

## Stage F — Stabilize only after pressure

Only compile a concept/family when repeated trajectories make the organization useful and compressive.

Do not freeze a structure because it is easy to formalize.

---

# 7. Analogy

A weak representation of analogy is:

```text
G1 --ANALOGOUS_TO--> G2
```

A strong analogy is one that reorganizes the network:

```text
G1 in F1
G2 in F2
        ↓
shared genealogy / transformation / structural pressure
        ↓
discover F*
        ↓
G1 and G2 become
- realizations,
- states,
- projections,
- or partializations
of a deeper common organization
```

**A strong analogy should usually change ontology, not merely add an edge.**

---

# 8. Disanalogy

Do not treat disanalogy merely as failed similarity.

A disanalogy can:

- expose a hidden axis,
- split a family,
- create a new family coordinate,
- reveal an unstable zero,
- force rebase,
- show that two apparently identical forms have different genealogies,
- generate a new conceptual object from the deformation path.

Track the origin of the break:

```text
SEED
PROPAGATED
RESIDUAL
REBASED
```

and ask what **family structure** the break reveals.

---

# 9. Ontology improvement test

A genuine ontology improvement occurs when the system changes **what kind of things it thinks exist** or how previous things are classified.

Examples:

```text
three isolated congruence criteria
→ regions/charts of one host-relative family

triangle / congruence / parallel
→ realizations of a deeper completion topology

parallelogram
→ same Gestalt simultaneously:
   topological zero,
   generic metric/angular state,
   congruence host,
   composite nonclosure organization
```

Merely adding a relation is not automatically ontology improvement.

---

# 10. Discovery-mode coherence monitor

During discovery, replace the old proof-style validator mentality with a **coherence monitor**.

It should protect against:

- material identity errors,
- impossible incidence claims,
- accidentally treating cognitive role alignment as material identity,
- silently changing the frozen workspace,
- contradiction between two representations of the same Gestalt,
- incompatible family assignments,
- genealogy corruption.

It should **not** dominate the run by requiring theorem certificates.

Use statuses such as:

```text
SPECULATIVE
STRUCTURALLY_SUPPORTED
REORGANIZATION_PRESSURE
STABILIZING
UNRESOLVED
INTERNALLY_INCOHERENT
```

The important distinction is:

```text
INTERNALLY_INCOHERENT
!=
NOT YET PROVED
```

In the present phase, "not yet proved" is usually irrelevant.

---

# 11. Future certification phase

A theorem-certification phase may exist later, but it is **not the current research regime**.

Future pipeline:

```text
MATURE COGNITIVE DISCOVERY
        ↓
select a proof-readable projection
        ↓
compile into Euclidean / formal proof language
        ↓
validate correctness
```

Keep:

```text
DISCOVERY GENEALOGY
!=
PROOF CERTIFICATE
```

The proof layer will eventually test whether a stabilized conceptual trajectory has a valid formal projection. It must not retroactively become the explanation of discovery.

---

# 12. No blind-search mythology

Do not pretend the experiment is neutral or theory-free.

Merovingio already has strong theoretical commitments:

- Gestalt organization,
- whole/part dynamics,
- analogy,
- disanalogy,
- genealogy,
- rebase,
- constructive workspaces,
- zero/fixed states,
- family structure,
- gnomonic growth,
- multi-realization.

Use these commitments actively.

The test is not:

```text
"Would this emerge from arbitrary rules with zero conceptual priors?"
```

The test is:

```text
"Does this conceptual machinery repeatedly reorganize mathematics
in fertile, compressive, non-ad-hoc ways across different domains?"
```

Theory-guided discovery is expected.

---

# 13. Preferred run structure

For future Merovingio experiments, default to:

```text
0. QUESTION / CONCEPTUAL PRESSURE
1. RICH SEED GESTALT
2. FAMILY FIELD BEFORE INJECTION
3. DEFORMATION / BREAK / REBASE TRAJECTORY
4. SAME GESTALT ACROSS MULTIPLE FAMILIES
5. ANALOGY / DISANALOGY PRESSURES
6. FAMILY REORGANIZATION
7. ONTOLOGY CHANGE
8. STABILIZATIONS / OPEN STRUCTURES
9. HIGH-LEVEL COHERENCE AUDIT
```

The main result should answer:

> **How did the network's ontology or family organization change?**

The final audit should answer only:

> **Is that reorganization internally coherent with Merovingio as currently constituted?**

not:

> Which deductions were formally proved?

---

# 14. Rewrite rule for older runs

When revisiting Runs 18–21 or similar experiments, reinterpret provisional constructs according to:

```text
TRUE OPERATOR
FAMILY STRUCTURE
REALIZATION MAP
RELATION
DERIVED PATH
GENEALOGY
```

Default assumption:

> if a candidate only names a path through already existing operators and families, it is **not** a new operator.

Also reinterpret old "proof validator" sections as:

```text
HIGH-LEVEL COHERENCE AUDITS
```

unless the experiment explicitly belongs to a later certification phase.

Preserve the experiments. Refactor their interpretation.

---

# 15. Stop conditions

Pause before adding an operator if any of these are true:

- the phenomenon appeared only once,
- it contains theorem-specific vocabulary,
- it can be expressed as a sequence of existing operators,
- it only records a result of projection/recomposition,
- it is better understood as a family-relative state,
- it disappears when the same Gestalt is viewed in another family,
- its apparent novelty comes only from renaming a relation.

Instead, investigate the family structure.

Pause before invoking proof machinery if:

- the purpose is conceptual unification,
- the ontology is still changing,
- the family itself is under rewrite,
- proof pressure would force premature individuation,
- the only question is internal coherence.

---

# 16. Guiding maxim

```text
DO NOT FREEZE TOO EARLY.

THIS PHASE IS COGNITIVE, NOT DEMONSTRATIVE.

Prefer ontology change over rule creation.
Prefer family deformation over relation naming.
Prefer multi-realization over concept duplication.
Prefer genealogy over theorem labels.
Prefer constructive tension over immediate proof closure.

Formalize only enough to check high-level coherence
with Merovingio's own evolving system.

Proof comes later.
```

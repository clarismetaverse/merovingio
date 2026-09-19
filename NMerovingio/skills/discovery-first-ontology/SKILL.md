# Merovingio Discovery-First Ontology Skill

## Purpose

Use this skill for **all Merovingio conceptual experiments, family injections, analogy/disanalogy work, Gestalt rewrites, ontology changes, and experiment design**.

Its purpose is to prevent a recurrent failure mode:

> importing theorem-prover / verification-first habits into the discovery phase, then inventing new operators whenever a new relation or proof-path appears.

Merovingio is not being developed primarily as a rule engine that blindly combines premises. Its central object of study is the **evolution of families of Gestalten, their genealogies, their multi-realizations, and the ontologies that emerge from repeated conceptual reorganization**.

The proof layer remains important, but in this phase it is downstream.

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
ONLY AFTERWARDS:
proof certification / Euclidean compilation
```

Do **not** make proof availability the main engine of exploration.

A proof can certify a discovery later. It need not be the mechanism that generated the discovery.

---

# 2. Anti-pattern to avoid

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

# 3. What counts as a true operator

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

# 4. The primary unit: multi-realization of a Gestalt

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

# 5. Family-first experimental protocol

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

Do multiple theorem masks become regions of one host-relative family?
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

# 6. Analogy

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

# 7. Disanalogy

Do not treat disanalogy merely as failed similarity.

A disanalogy can:

- expose a hidden axis,
- split a family,
- create a new family coordinate,
- reveal an unstable zero,
- force rebase,
- show that two apparently identical masks have different genealogies,
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

# 8. Ontology improvement test

A genuine ontology improvement occurs when the system changes **what kind of things it thinks exist** or how previous things are classified.

Examples:

```text
three isolated theorem masks
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

# 9. Discovery-mode validator

During discovery the validator is deliberately light.

It should protect against:

- material identity errors,
- impossible incidence claims,
- accidentally treating cognitive role alignment as material identity,
- silently changing the frozen workspace,
- obvious contradiction in the scene representation.

It should **not** dominate the run by requiring every conceptual move to have an immediate theorem certificate.

Use statuses such as:

```text
SPECULATIVE
STRUCTURALLY_SUPPORTED
REORGANIZATION_PRESSURE
STABILIZING
UNRESOLVED
```

rather than filling the main experiment with PASS/REJECT bookkeeping.

Proof certification belongs in a later section.

---

# 10. Certification mode

After a conceptual reorganization is interesting enough, run a separate certification pass:

```text
DISCOVERY RESULT
        ↓
identify Euclidean/proof-readable projections
        ↓
find proposition support
        ↓
compile proof graph
        ↓
validate theorem-level correctness
```

Keep this distinction explicit:

```text
DISCOVERY GENEALOGY
!=
PROOF CERTIFICATE
```

and:

```text
COGNITIVE CYCLE
!=
LOGICAL CIRCULARITY
```

The proof layer certifies; it does not retroactively become the story of how the concept was discovered.

---

# 11. No blind-search mythology

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

# 12. Preferred run structure

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
9. ONLY IF USEFUL: PROOF-CERTIFICATION APPENDIX
```

The main result should answer:

> **How did the network's ontology or family organization change?**

not merely:

> Which deductions succeeded?

---

# 13. Rewrite rule for older runs

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

Preserve the experiments. Refactor their interpretation.

---

# 14. Stop conditions

Pause before adding an operator if any of these are true:

- the phenomenon appeared only once,
- it contains theorem-specific vocabulary,
- it can be expressed as a sequence of existing operators,
- it only records a result of projection/recomposition,
- it is better understood as a family-relative state,
- it disappears when the same Gestalt is viewed in another family,
- its apparent novelty comes only from renaming a relation.

Instead, investigate the family structure.

---

# 15. Guiding maxim

```text
DO NOT FREEZE TOO EARLY.

Prefer ontology change over rule creation.
Prefer family deformation over relation naming.
Prefer multi-realization over concept duplication.
Prefer genealogy over theorem labels.
Prefer constructive tension over immediate proof closure.
Use proof as certification after discovery, not as the imagination of discovery.
```

# NMerovingio Specification

## 1. Scope

NMerovingio v0 is intentionally narrow.

It knows only the isosceles-triangle workspace and Euclid Book I propositions:

- I.5
- I.6
- I.7
- I.18
- I.19

It must not use unrelated theorems, coordinate geometry, trigonometry, numeric angle measurement, or broad theorem search.

## 2. Base Gestalt

The base state is a symbolic-perceptual object:

```text
ISOSCELES_BASE
  side_left  = side_right
  angle_left = angle_right
```

The important object is not merely the proposition `side_left = side_right`.
The base Gestalt stores a correspondence network:

```text
side_left  <-> side_right
angle_left <-> angle_right
side_left  opposes angle_right
side_right opposes angle_left
```

The reasoner must preserve provenance: every relation remembers whether it came from the base Gestalt, a counterfactual break, a construction, or a later inference.

## 3. Counterfactual generation

A counterfactual begins by preserving the base mapping and breaking exactly one relation.

Canonical breaks:

```text
BREAK_SIDE_EQUALITY(+)
BREAK_SIDE_EQUALITY(-)
BREAK_ANGLE_EQUALITY(+)
BREAK_ANGLE_EQUALITY(-)
```

Example:

```text
base: side_left = side_right
break: side_left > side_right
preserve initially: angle_left ? angle_right
```

A break is not yet a theorem. It is an impetus-bearing state that asks which other relations can remain coherent.

## 4. Epistemic contacts

A `contact` is a preserved or constructed element shared by the base and counterfactual views.

Contacts are used as inverse middle terms: they do not merely transfer positive facts; they transfer constraints that can eliminate incompatible continuations.

Represent each contact with:

```json
{
  "relation": "...",
  "source": "base|construction|counterfactual",
  "role": "positive_bridge|constraint_bridge"
}
```

## 5. Proposition memory

Each proposition is stored as an inferential pattern, not as a canned proof.

A proposition record contains:

- `id`
- `workspace`
- `preconditions`
- `effect`
- `role`
- `direction`
- `counterfactual_signature`
- `visual_operations`
- `forbidden_shortcuts`

The reasoner should retrieve a proposition because its **role** matches the active tension.

Example:

```text
active tension:
  angle equality is preserved
  side equality has been broken

retrieve I.6 because:
  role = reject side inequality under equal base angles
```

Do not retrieve I.6 merely because the target is tagged as I.6.

## 6. Run loop

A reasoning episode is:

```text
BASE
 -> MINIMAL BREAK
 -> FIND CONTACTS
 -> GENERATE CANDIDATE CONTINUATIONS
 -> RETRIEVE ROLE-ANALOGOUS PATTERNS
 -> APPLY / RUN
 -> ELIMINATE OR PROPAGATE
 -> STABILIZE OR FAIL
```

The engine should log each step as an explicit trace.

## 7. Stabilization

A counterfactual becomes a new Gestalt when it has enough internal structure to be used without constantly referencing the original base.

Example stabilized ordered Gestalt:

```text
side_left > side_right
angle_right > angle_left
```

Once stabilized it can itself become a base for a new counterfactual.

## 8. Backward enrichment

When a later stabilized Gestalt changes how an earlier one can be understood, record a backward-enrichment edge.

Example:

```text
I.18 / I.19 ordered cases
  -> reinterpret isosceles equality as the zero-point of a side-angle order family
```

This is not a proof dependency; it is a conceptual enrichment relation.

## 9. Initial heuristics

Score candidate actions with a small qualitative function:

```text
score =
  + preserved_contacts
  + inferential_role_match
  + new_constraints_exposed
  + potential_for_stabilization
  - arbitrary_new_objects
  - target_leakage
  - forbidden_shortcuts
```

No numeric optimization is required in v0; a deterministic rank is sufficient.

## 10. What v0 must demonstrate

v0 should at minimum:

1. Generate side-break and angle-break counterfactuals from the isosceles base.
2. Retrieve I.6 for an angle-equality / side-inequality tension.
3. Retrieve I.5 for a side-equality / angle-equality propagation.
4. Distinguish I.18 and I.19 by direction of the active break.
5. Use I.7 as a uniqueness / incompatible-second-closure pattern rather than a generic equality theorem.
6. Produce traces without receiving the target theorem's visual analogy.

## 11. Explicit non-goals

v0 does not need to:

- formally prove Euclid in a proof assistant;
- guarantee discovery of a novel proof;
- perform continuous geometry;
- parse arbitrary diagrams;
- solve propositions outside I.5, I.6, I.7, I.18, I.19.

The purpose is to isolate whether **counterfactual analogy / disanalogy can bootstrap useful proof search** from one visual-conceptual workspace.

# Canonical N10 — Re-individuation promotion

`N10` is the first canonical graph state layered on top of the frozen `N0..N9` v1 registries.

It promotes the minimal generalization proposed in Run10, accepted in Run11, and stress-tested negatively in Run12:

```text
OP_INTERNALIZE  = OP_REINDIVIDUATE(mode=INTERNALIZE)
OP_EXTERNALIZE  = OP_REINDIVIDUATE(mode=EXTERNALIZE)
```

The operator changes cognitive individuation / role-domain reading while preserving the material workspace and material owner map.

## Canonical guardrail

```text
REINDIVIDUATION NEVER UPGRADES PROOF LICENSE BY ITSELF
```

Hence:

```text
COGNITIVE_UNIFICATION != MATERIAL_IDENTITY
SCHEMA_MATCH != PROPOSITION_APPLICATION
BLOCKED_PROPAGATION != REJECTED_COUNTERFACTUAL
```

Run12 is essential evidence for this promotion: two similar triangles at different scale can be co-indexed by a shared metric/angular schema, but I.18 cannot be transported across the two material triangles and I.25 remains unavailable unless its carrier equalities are independently licensed.

## New compiled family

N10 compiles the semantic commonality between I.18 and I.25 as:

```text
F_METRIC_ANGULAR_ORDER

METRIC_ORDER -> ANGULAR_ORDER
PRESERVE_SIGN
axis = {LT, EQ, GT}
```

with distinct realization topologies:

```text
I.18  -> OBJECT_NATIVE
I.25  -> PAIR_NATIVE
shared cognitive reading -> REINDIVIDUATED_SCHEMA
```

The shared schema does not erase genealogy or proposition scope.

## Layered canonical storage

The historical `*_v1.json` files remain unchanged through N9. `canonical_manifest.json` declares ordered canonical deltas, beginning with:

```text
canonical_deltas/n10_reindividuation.json
```

`src/cognitive_graph.py` now loads the frozen base plus ordered canonical deltas and validates references and the re-individuation proof-license barrier.

This keeps the history auditable: experimental files remain experiments; promotion into the canonical graph is an explicit event rather than a retroactive rewrite.

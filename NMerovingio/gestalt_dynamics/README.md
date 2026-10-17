# Panoptikon — Gestalt Dynamics v1.0

## Scientific target

Can two **different construction histories** lead to the **same final geometric workspace** while preserving **different genealogies** for the conceptual interpretations recognized along the way?

This is a minimal symbolic research fixture, *not* a trainable geometry reasoner or proof engine. It records the activation, extinction and retrospective reinterpretation of Mental Spaces with independent geometric validation.

### Construction paths

Both start with exactly the same original triangle ABC, and finish with the **same** point D on segment AB and the same connector CD.

1. **Base-first:** select D by an interior proportion of AB; join C to D.
2. **Fan-first:** select a ray from C, intersect it with the original AB at the very same D, then restrict the ray to finite segment CD.

End-state equality is certified by the *exact same material fingerprint*. Constructive and conceptual genealogy are kept separately. The example tests different construction **provenance**, not two distinct final geometric theorems.

### Engine

- Material layer: points, segments, optional ray, ordered construction events and reproducible snapshots.
- Certified relations: strict betweenness, non-degeneracy, shared internal boundary and incidence. Numerical coordinates are used in the validator; no metric equalities are claimed.
- Candidate Mental Spaces: original base, original apex fan, base split, subdivided apex fan, pair of internal triangles, mixed angle–base bridge.
- Candidate Generic Space: two adjacent triangular regions with CD as shared carrier. **An analogy candidate, NOT equality/congruence proof.**
- Genealogy: first appearance of each candidate, producer event, event dependencies and material-to-interpretive role history.
- Back-propagation: after CD appears, the *existing* AB and C receive extra roles without changing their original geometric identity.
- Deformation: slide D along AB, to B and beyond B. At/beyond the endpoint, the internal split and internal paired-region Generic Space are invalidated.

### Jev exploratory probe

Four TypeSafe Jev 1.14 live `choice` evaluations compare role salience for the same final workspace:

| Construction history | Final state only | Final state + construction genealogy |
| --- | --- | --- |
| Base-first | one call | one call |
| Fan-first | one call | one call |

**The two final-state-only payloads are byte-for-byte identical.** History-aware payloads differ only because their actual event sequence and candidate activation order differ.

Jev selects which already enumerated Mental Space to inspect next. There is **no unique correct answer** for salience, so different selections/distributions can be observed but **must not be scored as a theorem-proof or autonomous discovery**. The candidate grammar is hand-authored. No key is stored or printed; GitHub Actions reads `TYPESAFE_API_KEY` from the repository secret.

### Test and run

```bash
cd NMerovingio/gestalt_dynamics
python -m pip install requests
python -m unittest discover -s tests -v
python core.py output/gestalt_dynamics.json
# only with authenticated, securely provided TYPESAFE_API_KEY:
python jev_probe.py
```

The Github Actions workflow is `.github/workflows/panoptikon-gestalt-dynamics-v10.yml`; artifacts `gestalt_dynamics.json` (deterministic genealogies) and `jev_genealogy_probe.json` (Jev distributions/usage). All files stay on `experiment/panoptikon-gestalt-dynamics-v1.0` until a separately approved merge.

### Caveats and future extensions

- A hand-authored grouping grammar cannot establish that cognition or Jev *spontaneously generates* the spaces. It tests representational data structures and a genealogy-sensitive judgment workflow.
- Temporal activation differences are partly determined by the explicitly supplied event order: they show that the formalization preserves history, not that provenance causes an empirically demonstrated human-like perceptual effect.
- Coordinates may be the same despite distinct symbolic constructions; here this is intentionally controlled.
- Jev judgments are independent non-deterministic model evaluations, not mathematical assertions.
- Next: introduce multiple candidate operations, delayed construction and goal-free prospective blending; compare with randomized event labels/held-out geometries and a genealogy-blind control.

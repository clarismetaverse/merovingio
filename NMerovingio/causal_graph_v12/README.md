# Panoptikon v1.2 — Genealogy as a causal graph

The research question is whether **the order of construction of the apex-angle pair and base right-angle pair changes Jev's priority for a joint correspondence**, separately from incidental placement of text within the model request.

## Experimental design

Hold the final geometry fixed within each shape. Use four shapes from v1.1:

- `iso_low`, `iso_high`: the apex bisector and base perpendicular coincide as one physical support.
- `scalene_left`, `scalene_right`: the two carriers are not coincident. An abstract role analogy remains conceivable, but a shared-carrier identity must be rejected.

Each scene has two possible construction histories:

- `upper_first`: apex angular pair created first and base right-angle pair second.
- `lower_first`: the opposite chronological order.

Both involve the same four graph nodes (initial material, apex partition, base orthogonal partition, final workspace). The `requires_material` and `contributes_to_final` edges are unchanged. Only the **event timestamps and the `precedes` edge** switch. In each history, the same graph is serialized in three ways: canonical, reversed and seeded shuffle. These three serializations are mathematically/causally the **same graph**, which is checked by a canonical signature in offline tests.

The benchmark includes two `final_only` baseline repetitions per geometry to measure output variability when no genealogy is supplied.

| Experimental factor | Count |
| --- | ---: |
| Shapes | 4 |
| Baseline calls per shape | 2 |
| History conditions | 2 |
| Serialization permutations | 3 |
| **Total authenticated calls** | **32** |

The TypeSafe `jev-1.14.0` request consists entirely of typed symbolic JSON, **without images**. Every call asks Jev independently:

1. `noul` — do the two angle-pair Mental Spaces share the same physical carrier? Independent geometric yes/no oracle.
2. `noul` — are upper half-angles necessarily equal *in measure* to the base right angles? Correct answer: no. Structural correspondence is NOT metric equality.
3. `choice` — which relation to explore next: upper pair, lower pair, joint correspondence, or independent partition systems? **No single ground-truth best choice exists.** We compare probabilities; this is a salience hypothesis only.
4. Additional history-only `choice` — which angular space was introduced later? Independent temporal oracle. If this fails, a purported genealogy-sensitive effect is difficult to interpret.

## Main causal-versus-ordering contrasts

Within the same shape and history, compare `P(joint)` across canonical/reversed/shuffled serializations. Changes indicate prompt position effects or noise, **not changes in causal structure**. Across upper-first vs lower-first histories holding presentation constant, compare `P(joint)` and conditional priority. Compare the size of that difference to within-history serialization variability and baseline-only repeat noise.

Even a positive difference does NOT prove that Jev understands construction causality. Event operator names remain meaningful, and the sample of four shapes is small. The test evaluates **genealogy-sensitive ranking of pre-authored Mental Spaces**, not autonomous discovery of a Generic Space or Euclidean proof.

## Security and reproducibility

Run via `.github/workflows/panoptikon-causal-graph-v12.yml` on the experiment branch. The pre-existing GitHub Actions secret `TYPESAFE_API_KEY` is injected only in the API step. The runner never prints or writes the key or the complete request payload. Generated output consists solely of responses, numeric distributions, known geometric-oracle labels and the canonical graph signature.

Local sanity tests (no API required):

```bash
python -m pip install requests
python -m unittest discover -s tests -v
```

The final artifact is `output/jev_causal_graph_v12.json`. Do not merge into `main` until after review.
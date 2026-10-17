# Panoptikon v1.3 — geometry, support, time

## Question

Can a change in *temporal precedence alone*, with **exactly the same geometry and material/support relations**, change how Jev prioritizes a hypothetical Generic Space aligning the apex angular pair and the lower right-angle pair?

The v1.2 experiment confounded richer support information with a causal graph. Version 1.3 adds a true **support-only control**, matched serializations and a difference-in-differences analysis.

## Three controlled conditions

**F — final geometry only:** final angular-pair descriptions, point labels and carrier IDs (8 calls: 4 geometries × 2 exact repeats). No event graph.

**S — support graph with NO time:** all F facts plus the fixed material dependency DAG, both partitions and their support edges. Without timestamps or `happens_before`. Identical byte-for-byte for `upper_first` and `lower_first` at matched shape/serialization (24 calls).

**T — support graph PLUS temporal order:** the **same** F and S data, plus `step` on each event and a single typed `happens_before` edge. The only difference across histories is the position of U relative to L (24 calls).

Total **56 calls**, all text/symbolic, model `jev-1.14.0`, without images or any private data. Existing GitHub Actions secret is used server-side and never written to artifacts.

The geometry oracle uses four fixtures: two isosceles (shared CD) and two scalene (apex bisector CE and base perpendicular CH have different carriers). An upper half-angle is **not** generally equal in measure to a lower right angle; no cross-level metric equality is asserted.

## Isolation of serialization bias

For each shape and history, the *same typed graph* is presented in canonical, reversed, and fixed-seed shuffled list order. Canonical hashes after sorting nodes and edges must match across serializations. The supports graph is identical across histories; only temporal step/precedence is changed in T. These exact conditions are enforced by Python unit tests.

Questions shared by F/S/T:
- `noul` shared carrier (objective geometry oracle).
- `noul` cross-pair metric equality (objective false control).
- `choice` exploratory salience: upper, lower, joint correspondence, separate reading. **No uniquely correct choice.**

The three **exact same** typed questions are sent in F, S and T. The temporal-comprehension diagnostic was collected in the earlier pilot run, and removed from this primary ablation to eliminate question-batch differences.

We calculate per-condition averages, the matched support-only variability and the *difference in differences*:

`[p_joint(T, upper_first) − p_joint(T, lower_first)] − [p_joint(S repeat 1) − p_joint(S repeat 2)]`

These are descriptive matched contrasts, **not causal estimators in a randomized experiment**: adding the time fields can change the prompt's salience independently of a conceptual reconstruction. Serializations and shapes are not large independent samples, and meaningful operator names remain. The experimental hypothesis is **not accepted** without replication and held-out geometry.

## Run

```bash
cd NMerovingio/causal_ablation_v13
python -m pip install requests
python -m unittest discover -s tests -v
# Only in an environment securely provisioned with TYPESAFE_API_KEY:
python causal_ablation_v13.py output
```

Workflow: `.github/workflows/panoptikon-causal-ablation-v13.yml`. Artifacts include only sanitized `output/jev_causal_ablation_v13.json`, no request bodies or credentials. No changes are made to `main`.
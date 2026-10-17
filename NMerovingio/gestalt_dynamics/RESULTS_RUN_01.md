# Panoptikon Gestalt Dynamics v1.0 — live experiment 01

**Branch:** `experiment/panoptikon-gestalt-dynamics-v1.0`  
**GitHub Actions:** https://github.com/clarismetaverse/merovingio/actions/runs/39017677622  
**Status:** all deterministic unit tests, artifact generation and 4 Jev 1.14 calls completed successfully.

## Geometrically controlled genealogy experiment

Both `base_first` (select D on AB, then join CD) and `fan_first` (open a ray from C, intersect AB at D, then restrict it to CD) produce the **same final points and segments** and **identical final candidate Mental Space vocabulary**. The SHA-256 fingerprint computed from canonicalized final material coordinates/segments is equal across the two histories.

The two histories have **different sequences and provenance**:
- `base_first`: 2 constructive events, 3 snapshots; base subdivision detected at stage 1 and coupled regions after joining CD at stage 2.
- `fan_first`: 3 constructive events, 4 snapshots; candidate apex-ray role arises at stage 1, base subdivision at stage 2 and coupled regions after making finite CD at stage 3.
- Back-propagation: the already-present AB receives the roles `carrier_of_adjacent_base_parts` then `outer_boundary_of_paired_regions`; C gains `vertex_of_adjacent_angular_sectors`. These are role updates, not changes in material identity.

**Deformation:** D at t=0.37 is strictly within AB, so base subdivision and a two-triangle partition are valid. At t=1.0 and t=1.15, the strict interior condition fails and these internal partitions are withdrawn. No angle/length equality or congruence is assumed.

## Jev live observations

Four authenticated `choice` requests: each genealogy evaluated both with a genealogy-blind final state and with its construction history. All four candidate readings remain mathematically meaningful; **no unique correct focus was specified**.

| Genealogy | Condition | Selected | P(base subdivision) | P(apex sectors) | P(paired regions) | P(angle-base bridge) |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| base-first | final only | paired regions | .07 | .05 | .65 | .23 |
| base-first | history-aware | paired regions | .12 | .04 | .61 | .23 |
| fan-first | final only | paired regions | .09 | .05 | .60 | .26 |
| fan-first | history-aware | **angle-base bridge** | .08 | .05 | .33 | **.54** |

Reported API usage: 3,468 input tokens, 242 output tokens (4 calls). Note that the two final-state-only requests contain the same JSON payload, yet differ slightly in output distribution; this illustrates why a single comparison cannot identify a causal effect.

## Interpretation and epistemic limits

The deterministic **engine** demonstrates that the formalization can distinguish material identity from history, preserve first-appearance provenance, register retroactive role changes, and invalidate groupings under deformation. This is not an empirical proof that human cognition is genealogy-dependent: the grouping grammar is hand-authored.

The **Jev** observation is compatible with genealogy-sensitive prioritization, particularly for the fan-first construction, but is uncontrolled at N=1 per condition/history. It is a test of *ranking* pre-enumerated candidate Mental Spaces, not autonomous creation of a new Gestalt or discovery of a theorem.

## Next decisive test

Repeat the same final-state vs history-aware contrast with many paraphrased histories, unrelated event-order controls, and at least three held-out geometries; compare probability distribution shifts and calibrate against a deterministic salience model. Only then attempt novel constructive bridge generation and prospective blending.

**Files:** `NMerovingio/gestalt_dynamics/core.py`, `jev_probe.py`, `tests/test_dynamics.py`; GitHub Actions artifact `panoptikon-gestalt-dynamics-v10` includes the complete `gestalt_dynamics.json` and `jev_genealogy_probe.json`. No secret is included.

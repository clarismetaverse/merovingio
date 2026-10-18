# Merovingio v1.0 — Prospective Generic Space Binding (live run 01)

**GitHub Actions:** https://github.com/clarismetaverse/merovingio/actions/runs/39158131284  
**Branch:** `experiment/prospective-generic-binding-v1.0`  
**Model:** `jev-1.14.0`  
**Run status:** completed successfully; all 18 Jev responses returned and were evaluated by an independent geometry checker.  
**Results:** downloadable GitHub Actions artifact `merovingio-prospective-binding-v10` containing `prospective_results.json` and candidate images.

## Pipeline actually executed

1. **Recall** two previously curated Generic Space entries from the v0.9 repository memory and a catalogue-based negative rule:
   - `GS_HIST_DOUBLE_TRIANGLE` originates from `W_QUAD_AC`, a quadrilateral with diagonal AC shared by triangle Gestalten.
   - `GS_HIST_RADIUS_TRIANGLE` originates from `W_TWO_CIRCLES`, a common-radius/two-circle construction.
   - `GS_PROP_I_5` is a **catalogued theorem-role template**, not a demonstrated current-workspace premise.
2. **Determine missing roles** before construction. Do not claim they exist yet.
3. **Generate four geometric proposal images** per case using deterministic code, with anonymized K1–K4 and all four position orders represented in each positive family.
4. **Select with Jev** using one `choice` question; compare two conditions on the positive trials: `schema_only` versus `historical_memory`.
5. **Independently check** the selected construction against structural and geometric role conditions; report precisely which slots are completed. No Euclid proof is performed.

## Observed results

| Evaluation mode | Correct / total | Mean choice confidence | Input tokens | Output tokens |
|---|---:|---:|---:|---:|
| Schema and missing roles, without historical memory | 8 / 8 | 0.954 | 118,744 | 408 |
| Schema with historical memory | 8 / 8 on comparable positive trials | approximately 0.964 on all 10 trials | 147,194 (includes 2 negative trials) | 522 |
| Negative controls (historical memory only) | 2 / 2 | 0.970 | included above | included above |
| **Total** | **18 / 18** | — | **265,938** | **930** |

The historical-memory group contains ten calls (eight positive, two negative) while the schema-only group contains eight calls. Therefore the unadjusted 10/10 vs 8/8 should **not** be interpreted as a performance improvement.

### Case-level observations

- Triangle shared-carrier case: Jev selected the C→AB connection in **all eight comparisons** (four candidate-label rotations × two conditions). The checker confirmed the newly shared carrier and two adjacent triangular regions.
- Circle case: Jev selected a second circle centered at B with the AB-matching radius in **all eight comparisons**. The independent checker distinguished this from a shorter-radius circle which can intersect the first circle but does not preserve the common-radius reference.
- I.5 negative controls: Jev chose **none** in both scenes; no arbitrary added line was accepted as proof of an unstated side equality.
- Both positive tasks explicitly described their missing abstract roles. Consequently, good results prove only successful **ranking from a supplied finite proposal set**, not that Jev autonomously generated the construction or discovered the Generic Space.

## Interpretive boundaries

- The memory corpus was **curated from earlier workspace fixtures**; it was not learned automatically from unseen theorem proofs.
- The model did not receive the offline candidate-operation mapping or the independent geometric oracle, but did receive the current missing roles in both conditions.
- A favourable result after retrieval does **not** establish the causal value of historical memory: the schema-only baseline also achieved 100%.
- Checker labels `verified_structural` mean geometric role constraints evaluated in the local coordinate/combinatorial simulator. They do not mean formal proof or theorems certified.
- The negative control tests useful abstention in one narrow missing-premise scenario; it does not prove reliable abstention across other problems.
- The report contains usage returned by the API, not an independent reconciliation against the vendor dashboard.

## Next meaningful experiment

Reduce direct instruction about desired roles and test retrieval-driven multi-step search across **held-out figure families**, requiring the system to choose both which prior Generic Space to activate and which construction can fill its open slots. Add analogous but false retrieved patterns, an explicit no-match class, and geometry-generated adversarial candidates. Benchmark Jev against deterministic graph matching and compare source-memory on/off with identical task formulation.

## Reproducibility

- `experiments/jev_i10_maxblend_v03/src/prospective_memory_v10.py`
- `experiments/jev_i10_maxblend_v03/src/prospective_binding_v10.py`
- `experiments/jev_i10_maxblend_v03/tests/test_prospective_binding_v10.py`
- `.github/workflows/prospective-generic-binding-v10.yml`

No API secret is stored in the repository or in the run artifact. Branch `main` remains unchanged.

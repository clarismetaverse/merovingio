# Merovingio / Jev v0.8: One Geometry, Four Mental Spaces

**Run:** https://github.com/clarismetaverse/merovingio/actions/runs/38986155987  
**Branch:** `experiment/jev-single-construction-reframing-v0.8`  
**Model:** Jev 1.14, live authenticated API, same construction in all calls.

## Experimental design

A scalene triangle ABC, one interior point D on AB, and the connector CD remain **identical** in all trials. D is at 0.37 of AB; the angle bisector would meet at 0.42440, the median at 0.5, and perpendicular foot at 0.27869. CD therefore has no accidentally built-in angular, length or right-angle equality.

Four **simultaneously available interpretations** of the same CD:
- Two angular sectors at C.
- Two ordered subsegments AD and DB.
- Two closed triangular regions ACD and BCD sharing CD.
- An inter-domain connection from apex angular space to base-segment space.

Jev is asked to SELECT the grouping appropriate to the currently active focus; it is **not** asked to generate a new construction. Each of the four groupings is offered as a visual overlay of the same underlying figure. In one ablation, structured grouping membership is supplied as well.

- Four focal prompts × two option orderings × two conditions = 16 decisions.
- Correct K1–K4 labels balanced across two orderings, two correct answers per slot.
- Same underlying coordinates, lines and points for all overlays.
- Independent geometric non-coincidence checks and tests on candidate order, output schema and leakage.

## Real results

| Condition | Correct | Mean choice confidence | Input tokens | Output tokens |
|---|---:|---:|---:|---:|
| Visual grouping overlays | 8/8 | 1.0 | 126,122 | 408 |
| Overlays + structured Mental Spaces | 8/8 | 1.0 | 129,362 | 408 |
| **Total** | **16/16** | | **255,484** | **816** |

Each focal configuration was selected correctly in both label orders. Probability mass in every `choice` distribution was 1.0 for the selected alternative, as returned by Jev. This is **model confidence, not a statistical guarantee**.

## Scientific interpretation

Supports: **a single construction can sustain multiple coexisting conceptual roles**, and Jev can reliably **select** the visual/structured interpretation relevant to a specified focus on this constrained task.

Does **not** establish: spontaneous generation of Mental Spaces, recognition of exact metric relationships, Generic Space invention, or a benefit from adding explicit structural descriptions (A already reaches 8/8). The overlays were designed to foreground precisely the requested roles, so matching could be perceptual/semantic rather than deeper reasoning. One fixed figure and four role categories do not demonstrate generalization.

**Next stress test:** present one *unannotated* figure only, ask Jev for independent role judgments (with abstention/negative controls), and separately test whether a workspace can be regrouped prospectively without pre-authored colored views. A future model that discovers a new partition not among supplied candidates would be genuinely closer to Panoptikon's constructive blending.

**Files:** `experiments/jev_i10_maxblend_v03/src/fixed_workspace_reframing_v08.py`, tests and the workflow `.github/workflows/jev-fixed-reframing-v08.yml`. GitHub artifact `jev-fixed-reframing-v08` contains `reframing_results.json` and all images. No credentials are recorded.

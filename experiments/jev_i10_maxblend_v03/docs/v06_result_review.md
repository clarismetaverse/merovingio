# Jev Vision v0.6 — results and methodological review

**Experiment:** visual-only vs mental-space organization vs candidate generic-space alignment, holding the two scalene triangles and candidate drawings fixed across conditions.  
**Run:** https://github.com/clarismetaverse/merovingio/actions/runs/38982694565  
**Branch:** experiment/jev-mental-spaces-v0.6  
**Model:** jev-1.14.0  
**Result archive:** GitHub Actions artifact `jev-cognitive-ablation-v06` (contains sanitized `ablation_results.json` and diagrams).

## Verified observations

| Condition | Correct | Choices |
|---|---:|---|
| A: raw images | 0/4 | Selected median in all four |
| B: images + mental spaces | 2/4 | Chose option K2 in all four; strong indication of position preference |
| C: images + mental spaces + generic spaces | 1/4 | Chose K2 in three of four |

Per-response confidence was low (0.00–0.30). All twelve responses were returned successfully by the authenticated API and the GitHub Actions job completed.

Summing each response's reported usage: **78,968 input tokens and 420 output tokens** (12 calls; A 6,032 input/call, B 6,626, C 7,084; 35 output/call). These usage values are a better test that the endpoint was invoked than the dashboard's currently reported zero. A delayed or filtered dashboard is a possible explanation, not a verified diagnosis.

## What the experiment does and does not establish

- It demonstrates the usefulness of *controlled representation ablation* as a testing method, not a statistical improvement.
- B/C encode qualitative group membership, betweenness, shared carriers and hypothetical role correspondences.
- Critically, **those fields are true for both candidate constructions**. They do not provide the metric information necessary to determine whether two angular sectors have equal measure. Thus they cannot be expected to resolve the answer by logic alone.
- Jev's B scores should not be called a gain in geometric competence: the repeated preference for K2 fully explains 2/4.
- There is no proof, theorem application, or verified novel generic-space discovery in this test.

## Next experiment

Build a role-sensitive **bridge-selection** dataset where the candidate constructions produce genuinely distinct cross-space structures. Let the deterministic geometry engine calculate and validate those structures; feed Jev only sufficient, non-answer-leaking descriptions and diagrams. Evaluate retrieval/ranking of useful groupings, not direct precision measurement from pixels. Use additional scalene and rotated scenes, balanced label order, unanswerable negatives, a held-out configuration family, confidence calibration, and results against a symbolic baseline.

Retain separate epistemic states: `given`, `constructed`, `candidate`, `verified`, `refuted`. Never interpret candidate generic-space membership as established geometric equality.

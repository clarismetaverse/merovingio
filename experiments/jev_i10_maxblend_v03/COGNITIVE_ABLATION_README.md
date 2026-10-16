# Merovingio × Jev Vision — Mental Spaces ablation v0.6

## Question
Does adding the Merovingio's *organizing representation* improve Jev's selection of an angular partition in scalene-triangle workspace candidates?

Prior observed forced A/B performance in v0.5: 1/4. This benchmark uses the **same two triangle shapes and both candidate orders**, with **three input conditions** for each of the four pairs:

| Condition | Input |
|---|---|
| A: visual | Raw initial image + two anonymous candidate images |
| B: mental | Same images + explicit objects, grouping boundaries, between/incidence and two induced mental spaces *for each candidate* |
| C: generic | Same as B + structural correspondence schemas between left/right groups, all marked **hypothetical** and **not equalities** |

All three conditions use the same narrow question: *which candidate splits the apex angle into two equal angular parts?*

**No proof, theorem, result, or chosen method is provided.** Candidate names are K1/K2; the mapping to angle-bisector vs median exists only in the offline scoring report. The Generic Space mapping does **not** imply equality, congruence, or a guaranteed result.

## Expected outcomes
We measure accuracy by condition (four paired cases each), confidence, distributions and reported token usage. A, B and C are paired within each shape/order; each is sent in a separate Jev API call because questions in a single call do not consume other answers as shared intermediate state.

Even a high C accuracy would support at most a hypothesis about visual judgment *with additional context*, not mathematical proof or automatic discovery. Importantly, qualitative topology and shared role schemas are effectively identical for both candidates. **They contain no missing metric evidence about the angle's equality**; therefore no improvement should be guaranteed or assumed.

## Reproduce
Use workflow `.github/workflows/jev-cognitive-ablation-v06.yml` in the dedicated branch. It uses only the existing GitHub Actions `TYPESAFE_API_KEY` secret and never exposes it.

Local checks, without network:

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```

Runner (GitHub Actions):

```bash
python src/cognitive_ablation_v06.py output_ablation
```

Results: `output_ablation/ablation_results.json` artifact.

## Limitations and next design decision
- N=4 per condition: too small for performance claims.
- Candidate diagrams are not always distinguishable by pixel inspection; adding an image highlight would introduce a new experimental factor.
- B/C supply organization without proving equality, which isolates organizing context but cannot solve missing exact metric data.
- Next: evaluate a **true bridge-choice** task where candidate Generic Spaces differ in their *functional relevance* and an exact symbolic verifier supplies geometric validity; do not turn Jev into a coordinate calculator.
- Review `usage.input_tokens` against account billing if dashboard remains at zero; the dashboard may be filtered or delayed.

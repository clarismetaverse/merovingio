# Merovingio v0.8 — One Construction, Four Mental Spaces

## Question

Can Jev reframe the *same* constructed workspace as the active Mental Space changes?

The diagram always contains the same scalene triangle ABC, the same point D within AB, and the same connector CD. There is **no new construction** between trials. The line is deliberately neither a median, a perpendicular altitude, nor an angle bisector.

Four interpretations are possible and simultaneously legitimate:

| Mental Space / role | What we attend to | What CD contributes |
|---|---|---|
| Angular partition | Apex wedge at C | Two neighboring sectors ACD / DCB |
| Segment partition | Original base AB | Adjacent parts AD / DB, with D between A and B |
| Paired regions | Two triangles ACD / BCD | One shared boundary CD |
| Cross-space linkage | The angle at C and the segment AB | A connector with origin C and endpoint D on AB |

The experiment **does not ask Jev which construction is best**, and does not
ask it to prove anything. It asks which of **four visual annotations of exactly
the same geometry** foregrounds a given conceptual grouping. This is
multi-role reinterpretation, not discovery of a previously unseen bridge.

## Experimental design

- One invariant source geometry and four overlays (candidate mental-space views).
- Four independently varied active focus prompts.
- Two counterbalanced assignment orders (the correct image receives each
  K1/K2/K3/K4 identifier twice).
- Two ablation conditions:
  - A: geometry + four annotated views;
  - B: same geometry/views + typed candidate Mental Space membership/relations.
- **16 Jev API calls total**, with randomized candidate label assignment but
  geometry fixed in all 16.
- Deterministic oracle checks geometry and validates the expected
  concept-to-annotation correspondence.

No candidate operation name, answer key, metric equality, I.10 proof, or
verified congruence is included in Jev inputs. The result includes decision
distribution, confidence, token usage and exact offline scoring.

## Interpretation

**Success would show:** Jev can switch attention among roles of one
construction, rather than recognizing one unique identity of CD.

**Success would NOT show:** Jev autonomously invented the Mental Spaces;
detected angle equality; discovered a proof; or performed prospective
constructive blending. The task descriptions and annotations intentionally
supply candidate interpretive structures. Lexical matching is a possible
alternative explanation, especially in the structured condition.

A is a visual-interpretation baseline. B tests whether adding explicit
structured groups changes performance, but without a unique correct answer to
a purely open-ended MaxBlend problem, the current target is operationally
defined by the active conceptual focus. This experiment is a *test of
reframing*, not metric geometric inference.

## Execute

Use `.github/workflows/jev-fixed-reframing-v08.yml` in branch
`experiment/jev-single-construction-reframing-v0.8`.

The workflow reads GitHub secret `TYPESAFE_API_KEY` in the API step only,
never prints it, and uploads sanitized JSON plus diagrams.

### Next tests

Vary the conceptual framing without using overlapping vocabulary, add
deliberately ambiguous active spaces, and test if Jev can propose a fifth
grouping absent from the candidate list. That tests genuine generic-space
emergence rather than choosing from authored visualizations.

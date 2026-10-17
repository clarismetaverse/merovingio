# Jev v0.9 — single construction, unannotated vs symbolic

Run: https://github.com/clarismetaverse/merovingio/actions/runs/38986708877

Exactly one Euclidean construction ABCD; eight independent structural-role hypotheses (four true, four false), tested in four rigidly rotated bare diagrams and four permutations of a symbolic incidence/betweenness representation.

| Mode | Correct total | True positive | True negative | Input / output tokens |
| --- | --- | --- | --- | --- |
| Plain diagram | 32/32 | 16/16 | 16/16 | 12076 / 592 |
| Symbolic facts only | 25/32 | 9/16 | 16/16 | 4288 / 592 |

In symbolic-only mode, the failure cases were **angular subdivision** (0/4) and **shared triangular boundary** (1/4); all other hypothesis families scored 4/4. Mean probability of true angular subdivision: image 0.935 vs symbol 0.302. Mean probability of true region-boundary alignment: image 0.975 vs symbol 0.385.

Interpretation: symbol lists with incidence and betweenness did not reliably elicit the angle-space and region-space Gestalten despite correctly representing the geometric construction. Future symbolic representations may need cyclic order, orientation and explicit face/sector operators.

Limitations: only one figure with four correlated rotations and repeated symbolic representations; role hypotheses were provided as Noul questions, so results show recognition rather than spontaneous invention of Mental Spaces. No proof or congruence claim. GitHub Action succeeded; no credential data in artifacts.

Library archive: /Merovingio/Results/jev-unannotated-symbolic-v09-results.zip

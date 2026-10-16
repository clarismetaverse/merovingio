# v0.7 — Structural Bridge Selection

## The problem

Jev v0.5 failed to reliably distinguish angular bisector vs median from pixels, while
v0.6 presented identical topological alignments for the two candidates and did not
show a credible improvement from adding Mental Spaces.

Here the **geometric alternatives are structurally different** and the focus is
not metric equality. Instead, each candidate bridge transforms the workspace
and creates one or two new Mental Spaces whose boundaries can be reorganized.

The aim is to test whether Jev identifies the construction with the most
**useful cross-space re-partitioning**, relative to the currently salient
Mental Spaces. This is *not* an Euclidean proof or unrestricted discovery of a
mathematically optimal MaxBlend operation.

## Four candidates, four changing active frames

Start with a scalene triangle ABC. The deterministic construction layer
proposes four structural alternatives:

- A connector from vertex C to an internal point on AB, splitting the C wedge and the opposite carrier.
- A connector from vertex A to an internal point on BC, splitting the A wedge and its opposite carrier.
- A connector from vertex B to an internal point on AC, splitting the B wedge and its opposite carrier.
- A connector between interior points of CA and CB, generating a smaller apex-containing region and a complementary quadrilateral retaining AB.

Each alternative can be useful under some frame. There is **no intrinsically
best construction irrespective of the active spaces**.

We run one task for each active frame, with two scalene shapes and three ablations:
A. Images with original Mental Spaces (no candidate structures).
B. Same images and candidate-generated **Mental Spaces** (boundaries, membership, shared carriers).
C. Same images/spaces plus **candidate Generic Spaces** recording inter-group
   alignments and shared boundaries, all with candidate epistemic status.

The complete experiment: **4 frames × 2 shapes × 3 conditions = 24 live choices**.
Output uses anonymous K1–K4 IDs, counterbalanced so the offline target falls
twice into each ordinal position per condition.

## Independent correctness oracle

Python independently certifies strict betweenness of all generated points
and the combinatorial boundary shared by each pair of created regions.
Each active frame has exactly one structurally matching operation; these
operation names, labels, expected option IDs, and outcomes remain **outside
the Jev request**. No equality/congruence/proof is supplied.

A positive outcome supports sensitivity to focal frames and structural
affordances, not proof verification, novel porism discovery, or inductive
generalization. Do not infer direct metric equivalence from generic-space
correspondences.

## Running

The GitHub workflow `.github/workflows/jev-structural-bridges-v07.yml` uses
the existing GitHub Actions `TYPESAFE_API_KEY` secret only in the runtime
environment. Outputs are sanitized JSON and diagrams; never include the token
or original request body.

Direct non-network test:

```bash
cd experiments/jev_i10_maxblend_v03
pip install -r requirements.txt
python -m unittest discover -s tests -v
```

Live runner with securely provisioned key:

```bash
python src/structural_bridges_v07.py output_bridges
```

## Next validation

- Additional rotated and visually oblique configurations as holdouts.
- Unanswerable negative controls and optional no-match class.
- Ablate target wording to distinguish genuine structural integration
  from trivial string/label matching.
- Compare Jev with a fully deterministic graph-matching baseline.
- Evaluate constructive *sequences*, back-propagation, and generic-space
  emergence, not just one-step selection.

API documentation: https://docs.typesafe.ai/images,
https://docs.typesafe.ai/primitives/choice.

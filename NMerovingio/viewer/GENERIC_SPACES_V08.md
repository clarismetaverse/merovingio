## Generic Space Explorer v0.8

Open `/generic-spaces.html` in the Vite development server (`npm run dev`) or
in a production preview (`npm run build && npm run preview`).

This is a **new synchronized visualization**, not a replacement for the original
Cognitive Graph Explorer or Workspace Atlas. Three coordinated surfaces show:

1. A geometric Workspace where the same carrier CD remains one material object,
   even if it acquires many conceptual roles.
2. An **abstract Generic Space** rendered as candidate role correspondences, with
   missing slots visibly dashed.
3. Provenance and temporal activation showing **memory/retrieval**, **induction**,
   and **blend-emergence**; candidate constructions can be previewed as ghosts.

The stage control follows ABC (initial) → construct CD → reframe through blending.
Hover/click role rows to highlight their geometric realizations. Select a recalled,
induced, blended or incomplete Generic Space; switch between two **illustrative**
ranking dimensions (contextual relevance vs generative potential).

The new fixture is in
`../graph/examples/generic_spaces_v0_8.json`. Role bindings, stage activations,
salience values and genealogies are manually authored to illustrate the cognitive
architecture. No live Jev calls, automated Generic Space discovery, learned
ranking, or mathematical theorem proofs occur in this UI. A proposed parallel line
is explicitly rendered dashed and **never asserted to be constructed**.

CI: `.github/workflows/generic-spaces-v08.yml` tests fixture consistency,
typechecks via TypeScript and builds all three Vite HTML entries.

Scientific next steps: connect the visualization to the deterministic graph
engine and measured Generic Space induction, and replace example scores with
evaluated salience estimates. Verify geometry independently before elevating a
candidate relation to a proven assertion.

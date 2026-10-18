# Merovingio — Generic Space Memory v0.9

## What has changed

This version connects the existing v0.8 abstract Generic Space visualizer to an
**evidence-grounded, reusable memory of previous workspaces and proposition-catalogue roles**.

The memory file `NMerovingio/graph/generic_space_memory_v0_9.json` contains
five *candidate abstractions* from four existing v0.4.1 workspace examples,
plus five *catalogued theorem-role templates* from Euclid I.5, I.6, I.7, I.18 and I.19.

The sources are not equivalent:
- The workspace records identify named Gestalten, material carriers, multi-role
  participations and genealogies. The abstraction is not itself a theorem proof.
- The proposition catalogue stores named preconditions and effects, but is **not**
  a reconstructed workspace or replayed proof. Those records are labelled
  `catalogued_rule_only_not_workspace_proof`.

Every memory item retains its original path and source object IDs and does not
collapse genealogies merely because two entries share a structural family.

## Runtime

`NMerovingio/viewer/src/generic-memory.ts` implements deterministic retrieval
by role/feature overlap and explicit candidate missing-slots; deduplication
groups only matching tag signatures without merging source identities.

`GenericMemoryPanel.tsx` exposes this through the existing
`generic-spaces.html` view. It follows the construction stage (before CD, after CD,
reframing) and can also switch to an earlier circle workspace or I.5
role-transfer context. The inspector shows the ranking, which signature features
matched, missing roles, conceptual role alignment, and a hyperlink to the original
repository file.

**IMPORTANT:** The recall score is a handcrafted candidate-relevance heuristic,
not an output from Jev. A recalled Generic Space is an analogy template, **never**
proof of a geometrical equality or theorem license. Neither v0.8 nor v0.9
automatically extracts arbitrary new Generic Spaces from unknown workspace files;
this seed corpus was curated by inspecting specific existing records.

## Source provenance

- `graph/examples/workspace_quadrilateral_diagonal_v0_4_1.json`
- `graph/examples/workspace_two_circles_triangle_v0_4_1.json`
- `graph/examples/workspace_triangle_genealogy_comparison_v0_4_1.json`
- `graph/examples/workspace_equilateral_same_state_different_genealogy_v0_4_1.json`
- `data/propositions.json`

## How to run

Open `/generic-spaces.html` in the viewer Vite app and scroll the right
inspector to the '04 Memoria inter-workspace' section, or use the
"Memoria teoremi" link in its top bar.

```bash
cd NMerovingio/viewer
npm install
npm run dev
```

CI builds and tests the enhanced viewer on its experimental branch.
No API key is needed, no Jev API calls are run, and main is unchanged.

## Next experiments

1. Derive signatures automatically from normalized source graphs with
   independent type/geometry constraints rather than curate them by hand.
2. Match abstract roles to candidate *bindings* in the current workspace,
   rank prospective missing roles, and track the construction suggestions
   with provenance; no unchecked metric transfer.
3. Evaluate Jev as a secondary salience ranker over candidate Generic Spaces,
   using stable source citations, explicit uncertainty and a deterministic
   correctness checker.

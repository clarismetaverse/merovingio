# Temporal Genealogy / Same Final Figure, Different Construction Histories

SAME_FINAL_STATE != SAME_GENEALOGY.

Base: experiment/prospective-generic-binding-v1.0 at e1277e3 (includes v0.9 memory). Dedicated branch; main untouched. Jev requested model is jev-1.14.0; benchmark version is temporal genealogy pilot 1.

## Historical provenance and structural transformations

Sources: NMerovingio/graph/examples/workspace_equilateral_same_state_different_genealogy_v0_4_1.json and workspace_two_circles_triangle_v0_4_1.json. Full nodes, roles, edges and source hashes are copied to the observer report, never to model input.

A: G_CIRCLE_PAIR_EQ -> M_RADIUS_PACKET -> GEN_EQ_CIRCLE -> G_EQ_TRI_CIRCLE. Base becomes common radial carrier; intersection becomes apex; radius relations become triangle-side relations.
B: G_TRANSLATION_BASIS -> M_TRANSLATION_PACKET -> GEN_EQ_TRANSLATION -> G_EQ_TRI_TRANSLATION. Equal u,v at 60 degrees yield translated copies and closure v-u; translation generators become sides. Both map to G_EQ_STATE_SHARED within F_TRIANGLE_MEDIUM_SHARED. These are structural transformations of carrier participation, role assignment and dependency, not changes of final shape. The two-circles workspace grounds the center/boundary/shared-carrier reconstruction.

Animations are newly reconstructed three-frame interventions, not recovered historical recordings. Initial base and final equilateral rendering are shared. A middle frame shows two base-length circles. B middle frame shows a translated rhombic basis, equal-length ticks and an unlabelled 60-degree sector. No text or option labels are drawn. No AI-generated images are used.

## Protocol

24 calls: 2 origins x 3 conditions x 4 controlled transforms (0/37 degrees, reflected/unreflected). Order shuffled reproducibly, opaque option codes randomized, option order randomized per trial. Image assets expose frame IDs only. Frames remain chronological intentionally. Each call has exactly one typed choice question with two described origins and none. Text supplies no correct option code. Condition 3 adds curated per-frame Mental Spaces, Generic Spaces and role transitions; these are deliberate additional evidence. Its advantage cannot establish autonomous structural extraction or exclude textual cue use.

Final-only pairs have byte-identical requests at a fixed option seed. No unique genealogy target exists. Genealogy accuracy is null; report abstention rate and response matrix against non_identifiable. Never treat 50% binary origin choices as success. Sequence conditions have origin targets. Confusion matrices include none and failures; confidence, reliability and usage are retained when provided. Failures remain in the denominator. Small pilot; no significance or proof claims. Multiple images do not establish internal sequential reasoning.

## Reproduce

python -m unittest discover -s experiments/temporal_genealogy -v
python experiments/temporal_genealogy/benchmark.py --out output_temporal

Open output_temporal/viewer.html offline alongside results.json. Live mode is gated to GitHub Actions and TYPESAFE_API_KEY secret, with TypeSafe-Danger-Zone-Images: true. Push this dedicated branch to run tests, viewer build, generation and live evaluation. No local live calls; no API key in artifacts. Errors retain only status/category; no raw HTTP body. Results are checkpointed after each call and uploaded even after failure. Offline reports explicitly say offline_only, never fabricated Jev outcomes.

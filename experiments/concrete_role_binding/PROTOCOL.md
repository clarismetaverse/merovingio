# Concrete role witnesses and near counterexamples

Parent 7bf7de1, branch codex/concrete-binding-near-misses. Preserve main, v0.9/v1.0 and prior experiments. Jev 1.14.0, live only through Actions with repository secret and required images header.

## Question budget and target

Four calls, twelve Choice questions each, 48 total answers. Each question asks for a finite concrete witness assigning carrier, two region objects and scope host. There are five well-typed assignments with anonymous shuffled labels plus none. Every question has zero or one valid listed witness, checked before execution. Region ordering is immaterial. Object IDs, option order, question order and snapshot/schema aliases vary by replica, alongside rotations 0/37 degrees and reflections +/-1. These are four transformed synthetic replicas, not 48 independent geometries.

The two historical templates use explicit binding contracts: two adjacent triangular regions sharing one entire material side, and one segment participating in both region boundaries and a partition of the whole scope host. Adjacency/non-overlap and full boundary use are now stated explicitly. This extends the local operational contracts rather than silently redefining old benchmark results. In the first schema host is containment context; only the second requires full host coverage.

## Near controls

| Query case | Change | Shared triangles | Polyrole partition |
| --- | --- | --- | --- |
| shared | Actual adjacent triangular pair with the same carrier | Listed witness | Listed witness |
| distinct_coincident | Exactly one boundary-use carrier reference changes to a distinct coincident segment | none | none |
| partial_use | One region uses only part of the same carrier | none | none |
| triangle_quadrilateral | A genuine partition with one triangular and one quadrilateral region | none | Listed witness |
| wrong_host | Same snapshot, but scope is the surrounding rectangle instead of the triangle | Listed witness with changed scope host | none |
| omitted_valid | Same positive snapshot, but the true witness is removed from the options | none | none |

Total per replica: four positive selections and eight none, for sixteen positives and thirty-two none over the pilot. Report both classes separately; always answering none achieves 32/48 overall and is not a successful binding policy. None means no offered full assignment is valid. In omitted_valid a graph binding still exists, so none does not mean the schema is globally absent.

Every snapshot also has a coincident region decoy and three coincident material segments. All offered objects have the right types. A plausible-looking region clone or equal-coordinate segment cannot be accepted unless its exact material incidence satisfies the contract. Invalid choices may fail shared identity, complete-side use, disjoint interiors, host scope, region type or full partition. Their failure reasons remain observer-only.

## Evidence and reference

State contains typed objects, vertex cycles, segment endpoints and boundary-use references. These are declared structural facts, not inferred by Jev from pixels. No gold role assignment, validity flag, case name or correct option label is supplied in state/instructions. Each option itself is a proposed witness to test. Images have no labels, are rendered from host and region boundaries, and do not encode object identity. Shared and distinct_coincident differ in exactly one carrier-reference field and share the exact same image asset. wrong_host and omitted_valid also reuse the shared snapshot and image.

The reference checker verifies types, distinct region identities, exact material IDs and full-use endpoints. Convex clipping checks interior overlap and containment; polygon areas check host coverage. The tolerance is 1e-4 in pixel-coordinate cross-products/areas to accommodate rounded rotations; region areas are orders of magnitude larger. The checker does not consult case labels. Full enumeration independently confirms whether a graph binding exists and whether a listed witness was withheld. Test transform invariance and preserve all chosen witnesses before any downstream rejection.

## Interpretation

This tests selecting supplied role assignments among close alternatives, not generating an unconstrained witness. Success on positives and the pixel-identical identity counterfactuals would show use of object-level structured evidence beyond the general contract wording. It would not show autonomous visual extraction, broad geometric reasoning, internal sequential reasoning or formal proof. Geometry and explicit graph incidences intentionally resolve information absent from the images. A failure cannot be attributed to images alone because the input is multimodal and structured.

Report exact witness accuracy, positive and negative matrices by case/schema, selected invalid-witness reasons, none with and without graph bindings, and paired success on shared versus changed-identity snapshots. Also preserve native probabilities, confidence, optional numeric reliability, usage, failure status, reconstructed input hashes and images. No new Score questions, threshold tuning, retries or long-context header. Offline mode has no invented outputs. Live checkpoints and sanitized artifacts are retained even after failure.

Native structured Choice criteria follow [TypeSafe Choice](https://docs.typesafe.ai/primitives/choice). Requests use only GitHub Actions, TYPESAFE_API_KEY secret and TypeSafe-Danger-Zone-Images: true. Download artifacts, independently reconstruct and audit them, save the offline viewer and report in outputs and the existing Library page.

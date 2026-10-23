# Native relevance scoring of preverified bridges

Parent 95d4f84, branch codex/verified-bridge-relevance. Preserve main, v0.9/v1.0 and all prior experiments. Model jev-1.14.0, live only through GitHub Actions with TYPESAFE_API_KEY secret and TypeSafe-Danger-Zone-Images: true.

## Question and bounded budget

Can Jev prioritize a bridge for a declared structural objective once code has already checked its material bindings? Three vertex-to-opposite-side connectors in one scalene triangle, each yielding two adjacent triangular regions with one shared material carrier and a complete host partition. Every candidate passes BOTH historical local contracts, GS_HIST_DOUBLE_TRIANGLE and GS_HIST_MEDIAL_POLYROLE, through the existing independent convex-polygon and boundary-use checker. Its types, shared carrier identity, full boundary uses, containment, disjoint interiors and area conservation are established before any request. Invalid candidates fail closed.

Use three objectives, one for each vertex: compare the two parts of that vertex's angular fan together with the two parts of its opposite original side, organized by the new common carrier. Each candidate is preferred for exactly one objective. All three remain admissible under every objective. The reference is recomputed from geometric incidences, not a hard-coded candidate alias. It is a prespecified preference under this task, not universal usefulness or creativity.

Two presentations of the same geometry: original and a 37-degree rotation plus reflection. Randomize point labels, candidate aliases/order and GS aliases between presentations. Within a presentation hold state, candidate order, question order, image bytes, certificates and criteria fixed; change ONLY active_objective. Shuffle six serial trial events. Labels identify objects, never the preferred answer. Same monochrome styling for every candidate. The four images in a request are initial host plus three alternatives; they are not chronological frames.

For each candidate ask two four-level native Score questions: relevance of coupling the active Mental Spaces, and usefulness of the certified Generic Space instantiations for organizing that objective. Three candidates x two dimensions = six questions per request; two presentations x three objectives = six requests, 36 Score answers. No Choice, new schema discovery, repair questions or extra controls in this pilot. The two dimensions are correlated views, not independent observations.

## Evidence and role allocation

Supply inline certificates, candidate region vertex cycles and direct structural relations (vertex whose angular fan is split, original side receiving an interior contact, contact point, new carrier, two regions and host). These are objective-independent certified facts for ALL candidates. This intentionally removes the graph-lookup/validation demand from earlier binding tests. Do not supply target-match flags, oracle preferences, winner/rank, target scores, weights or diagnoses. Historical memory provenance and raw checker certificates remain observer-side. The state includes abstract roles and the local operational contracts; these strengthen the historical memory abstractions without asserting metric equality or theorem proof.

Jev judges relevance against the supplied objective using descriptive levels, not mathematical validity. Formal validity is common to all options. Explicit objective descriptions are necessary task context, not hidden correct candidate labels. No claim is made that this tests discovery of an implicit objective or useful research directions.

## Predeclared analysis

Normalize each native score by 3. Fixed composite = .5 Mental relevance + .5 Generic relevance. Preserve native score, level probabilities, confidence, optional numeric reliability/null and usage. No post-hoc weighting or threshold tuning; report all axes and composites, unique top matches, top ties, target-vs-alternative pairwise wins/ties, margins, and same-candidate score changes under objective swaps. A fixed candidate/position wins one of three objectives per presentation (2/6 overall), so objective sensitivity matters beyond a high score for admissibility.

There are six ranking groups, twelve target-vs-alternative comparisons, and six same-candidate objective sensitivity comparisons. They reuse one host and related prompts: not independent samples for significance claims. If any response fails, retain sanitized failure and do not count unobserved ranks. No metric treats downstream code acceptance as Jev accuracy. The proposed role also appeared in the earlier native-score prototype: this experiment isolates preverification and explicit relevance in a smaller design, rather than claiming an entirely new capability or a causal improvement over previous Choice tests.

## Execution and artifacts

Before live: geometry/material mutation tests, objective-only counterfactual invariants, exact request-size budget, transformed geometry, randomized labels, non-leakage, ties/missing-result behavior, guard and offline output. Run existing experiment suites and viewer build on branch. Guard both main and transport; no local API calls, no automatic retries, no long context. HTTP failures use fixed sanitized labels with no server text or credentials; checkpoint each call and stop HTTP 400/401/403.

Download the pinned Actions artifact; reconstruct all requests from image bytes, certify all candidates again, recompute rankings and objective contrasts, then save report, native responses, usage, failures, images, offline viewer and hashes in outputs and Library. No invented results in offline mode. This is not visual extraction, free bridge generation, general Euclid search, formal proof or evidence of internal sequential reasoning.

Official native Score and composite pattern checked 2026-10-23: https://docs.typesafe.ai/primitives/score and https://docs.typesafe.ai/patterns/composite-scoring . Score may lie between ordinal levels; code retains it rather than replacing it with argmax or an external score.

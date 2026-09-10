# Triangle Gestalt Network v0.2

> Operational extension of `TRIANGLE_GESTALT_NETWORK_V01.md`.
>
> **Methodological rule:** v0.1 remains the frozen geometric baseline for the transversal experiment. v0.2 adds the missing operational machinery for Gestalt completion, host-search, projection, backward enrichment, and construction evocation. It does **not** pre-inject transversal/parallel facts into the triangle network.

---

# 0. Goal

The core research claim is now stronger than theorem accumulation or local counterfactual search.

A Euclidean reasoner should be able to:

```text
1. recognize a local pattern;
2. search for a larger Gestalt that can host it;
3. construct/embed the local pattern into that Gestalt;
4. use the host Gestalt to complete missing correspondences;
5. project the completed structure back onto the original figure;
6. enrich the old Gestalt retroactively;
7. learn a new construction affordance for future problems.
```

This creates an **epistemic cycle**:

```text
P
 -> MATCH
 -> HOST
 -> COMPLETE
 -> PROJECT
 -> BACKWARD_ENRICH
 -> P+
 -> EVOKE
```

where `P+` is not a different theorem but a cognitively richer representation of the earlier pattern.

The key invariant is:

```text
P+ != P as an inferential object,
while the underlying geometric facts of P remain unchanged.
```

---

# 1. Preserve the v0.1 triangle baseline

The following structures remain unchanged from v0.1.

## 1.1 Three levels of Gestalt organization

```text
OBJECT
    one geometric object/configuration

PAIR
    correspondence between two objects/configurations

FAMILY
    governed space of canonical states, stable variants,
    disanalogies, symmetries, and rebase routes
```

## 1.2 Object order transducer

For one triangle:

```text
S = rel(side_left, side_right)
A = rel(opposite_angle_left, opposite_angle_right)

OBJECT_ORDER_TRANSDUCER
S <-> A
```

Stable family:

```text
F_OBJECT_ORDER = {
    (LT,LT),
    (EQ,EQ),
    (GT,GT)
}
```

with:

```text
I.5   : side EQ  -> opposite-angle EQ
I.6   : angle EQ -> opposed-side EQ
I.18  : side GT  -> opposite-angle GT
I.19  : angle GT -> opposed-side GT
```

The isosceles state `(EQ,EQ)` is the canonical zero/fixed point.

## 1.3 Pair order transducer

For two triangles with two corresponding sides fixed:

```text
H = rel(included_angle_T1, included_angle_T2)
B = rel(third_side_T1, third_side_T2)

PAIR_ORDER_TRANSDUCER
H <-> B
```

Stable family:

```text
F_PAIR_ORDER = {
    (LT,LT),
    (EQ,EQ),
    (GT,GT)
}
```

with:

```text
I.4   : included-angle EQ -> third-side EQ
I.8   : third-side EQ     -> included-angle EQ
I.24  : included-angle GT -> third-side GT
I.25  : third-side GT     -> included-angle GT
```

## 1.4 Congruence as minimal zero-mask completion

```text
SAS_ZERO_MASK = {
    side_1 = EQ,
    side_2 = EQ,
    included_angle = EQ
}

SSS_ZERO_MASK = {
    side_1 = EQ,
    side_2 = EQ,
    side_3 = EQ
}

ASA_ZERO_MASK = {
    angle_1 = EQ,
    angle_2 = EQ,
    included_or_carrier_side = EQ
}
```

General form:

```text
sufficient_zero_mask
    -> FULL_CONGRUENCE_GESTALT
```

## 1.5 Placement register

```text
PLACEMENT = { ZERO, NONZERO, UNKNOWN }
```

I.7 remains a rigidity/counterfactual pattern testing:

```text
metric_residue    = ZERO
placement_residue = NONZERO
```

## 1.6 Disanalogy genealogy

The distinction remains mandatory:

```text
STATE_IDENTITY != GENETIC_IDENTITY
```

A break is recorded by a `DisanalogySeed` and normalized by a `BreakSignature`.

```text
BreakSignature {
    ground_family
    ground_gestalt
    level
    register
    role_pair
    relation_before
    relation_after
    orientation
}
```

Origin classes:

```text
SEED
PROPAGATED
RESIDUAL
REBASED
```

A disanalogy family is:

```text
D(B) = all Gestalten descended from BreakSignature B
```

## 1.7 Residues

```text
X > Y
    ->
X = Y + R
```

with:

```text
ResidueType = {
    METRIC,
    ANGULAR,
    PLACEMENT
}
```

A rebase must preserve genetic provenance:

```text
role_now    = CANONICAL
origin_role = RESIDUE
```

---

# 2. New central distinction: proof graph vs cognitive graph

The system must maintain two related but non-identical graphs.

## 2.1 Proof graph

Contains licensed inferential dependencies.

```text
ProofGraph
    propositions
    constructions
    validated relations
    dependency edges
    proof certificates
```

A proof certificate may not depend on the proposition it is certifying.

## 2.2 Cognitive Gestalt graph

Contains representational and generative relations.

```text
CognitiveGraph
    Gestalten
    family membership
    analogy/disanalogy
    host relations
    projections
    completion events
    rebase routes
    construction affordances
    backward enrichments
```

This graph **may contain cycles**.

Therefore:

```text
COGNITIVE_CYCLE != LOGICAL_CIRCULARITY
```

A cycle such as:

```text
TRIANGLE_PATTERN
 -> PARALLEL_HOST
 -> COMPLETION
 -> ENRICHED_TRIANGLE_PATTERN
 -> EVOKE_PARALLEL_HOST
```

is allowed as a cognitive learning cycle, provided the proof certificate for any theorem does not use that theorem itself as evidence.

---

# 3. What COMPLETE means

`COMPLETE` is no longer defined as merely filling unknown relation slots.

## 3.1 Strong definition

```text
COMPLETE(P, G)
```

means:

```text
Given a partial pattern P and a candidate host Gestalt G:

1. map roles of P into roles of G;
2. validate that the mapping can be geometrically constructed;
3. identify host invariants that explain the mapped relations;
4. infer only those additional relations licensed by G;
5. return the completed host-view plus a trace of why each relation became readable.
```

Completion is therefore:

```text
local relations
    -> host membership
    -> global invariants
    -> additional local readouts
```

## 3.2 Completion is not arbitrary closure

The reasoner must never infer:

```text
"these relations look similar, therefore the whole Gestalt holds"
```

A `CompletionEvent` requires a validated embedding and licensed bridge relations.

---

# 4. Local facts as traces of a host Gestalt

A local proposition can be stored at two explanatory depths.

## 4.1 Fact view

Example:

```text
angle_1 = angle_1'
```

## 4.2 Host view

The reasoner asks:

```text
Which larger Gestalt would make this equality a natural local readout?
```

A host interpretation may transform:

```text
angle equality
    ->
shared direction-class membership
```

or:

```text
side equality
    ->
shared metric-carrier membership
```

This is not automatically true for every equality. It is a **candidate explanation** that must be constructed and validated.

---

# 5. New operational entities

## 5.1 PartialPattern

```text
PartialPattern {
    id
    source_gestalt
    level

    objects
    roles
    known_relations
    unknown_relations

    active_contacts
    active_breaks
    target_readout

    provenance
}
```

## 5.2 RoleClass

A role class groups elements that occupy the same inferential function in an active Gestalt.

```text
RoleClass {
    id
    gestalt_id
    semantic_role
    members
    invariant
    provenance
}
```

Examples:

```text
DIRECTION_CLASS_1
DIRECTION_CLASS_2
METRIC_CARRIER_CLASS
OPPOSITE_ANGLE_CLASS
PLACEMENT_CLASS
```

### Optional visualization rule

Colors may render `RoleClass` membership in diagrams:

```text
same color ~= same active inferential role
```

but color itself is never evidence. It is a visualization of graph annotations.

## 5.3 HostCandidate

```text
HostCandidate {
    id
    host_gestalt_id
    source_pattern_id

    role_mapping
    required_constructions
    preserved_contacts
    expected_invariants

    coverage
    unresolved_roles
    conflicts

    status: CANDIDATE | VALIDATED | REJECTED
    provenance
}
```

## 5.4 CompletionEvent

```text
CompletionEvent {
    id
    source_pattern
    host_gestalt

    validated_embedding
    role_mapping
    host_invariants_used

    newly_readable_relations
    newly_created_role_classes
    unresolved_relations

    construction_trace
    proof_support
    provenance
}
```

## 5.5 Projection

```text
Projection {
    id
    source_host_gestalt
    target_view

    role_map
    preserved_invariants
    local_readouts

    provenance
}
```

## 5.6 EnrichedGestaltView

```text
EnrichedGestaltView {
    base_gestalt_id

    original_inference_packet
    added_inference_packet

    new_host_links
    new_projection_links
    new_family_memberships
    new_construction_affordances
    new_rebase_routes

    enrichment_source
    provenance
}
```

## 5.7 ConstructionAffordance

```text
ConstructionAffordance {
    id
    source_gestalt
    target_host_family

    trigger_signature
    construction_operator
    expected_role_mapping
    expected_gain

    learned_from_completion_event
    certification_status
    provenance
}
```

---

# 6. New operators

The cross-level operator set is extended.

```text
ANALOGIZE
DISANALOGIZE
BREAK
OVERLAY
CUT_OFF
RESIDUALIZE
REBASE

EXTERNALIZE
INTERNALIZE
FAMILY_LIFT
INSTANTIATE

MATCH
HOST
COMPLETE
PROJECT
BACKWARD_ENRICH
EVOKE
```

## 6.1 MATCH

Search for already-known Gestalten whose role schema partially matches the active pattern.

```text
MATCH(P, Network)
    -> ranked HostCandidate[]
```

Matching uses:

```text
role compatibility
relation compatibility
preserved contacts
register compatibility
construction feasibility
family homology
```

Do not rank by theorem-name or target leakage.

## 6.2 HOST

`HOST` attempts to embed the local pattern in a larger Gestalt.

```text
HOST(P, G)
    -> HostCandidate
```

A larger Gestalt can be at the same formal level but a larger workspace, or at a higher organizational level.

Examples:

```text
triangle pair -> distributed directional workspace
triangle      -> larger symmetric construction
local angle   -> intersection/transversal workspace
```

## 6.3 COMPLETE

```text
COMPLETE(P, validated_host)
    -> CompletionEvent
```

It runs the host invariants and exposes relations that become inferentially co-present.

## 6.4 PROJECT

Map a completed host Gestalt back into a local view.

```text
PROJECT(G_host, target_view)
    -> Projection
```

The projection answers:

```text
What does this global structure look like when read again as a triangle,
pair of triangles, angle configuration, or other prior Gestalt?
```

## 6.5 BACKWARD_ENRICH

Retroactively add a new inferential interpretation to an already-existing Gestalt.

```text
BACKWARD_ENRICH(G_old, CompletionEvent, Projection)
    -> EnrichedGestaltView
```

It may add:

```text
new role interpretation
new host membership
new construction affordance
new projection path
new family membership
new rebase route
shorter future search path
```

It may **not** rewrite historical provenance or silently add unproved geometric facts.

## 6.6 EVOKE

Use an enriched Gestalt to propose a construction that recreates a previously discovered host.

```text
EVOKE(G_enriched, active_problem)
    -> ConstructionAffordance[]
```

This is the generative inverse of host recognition.

Core idea:

```text
recognize a whole from its parts
    +
learn to regenerate the whole from the parts
```

---

# 7. The completion cycle

The primary new reasoning cycle is:

```text
P0
 |
 | MATCH
 v
HostCandidate[]
 |
 | validate construction
 v
G_host
 |
 | COMPLETE
 v
CompletedHostView
 |
 | PROJECT
 v
P_projected
 |
 | BACKWARD_ENRICH
 v
P+
 |
 | EVOKE on future problem
 v
construction toward G_host
```

Formal shorthand:

```text
P0
 -> MATCH
 -> HOST
 -> COMPLETE
 -> PROJECT
 -> BACKWARD_ENRICH
 -> P+
```

and later:

```text
P+ + new_problem
 -> EVOKE
 -> reconstruct candidate host
```

This is the operational definition of **circular Gestalt reasoning**.

---

# 8. Completion as inferential co-presence

A Gestalt is useful when relations that were distributed or separately derived become simultaneously readable.

Define a qualitative quantity:

```text
SynopticGain(G, P)
```

which increases when hosting/completion makes more relations directly readable without replaying their full derivation.

Possible components:

```text
+ newly_readable_relations
+ merged_role_classes
+ shorter_access_paths
+ reusable_construction_affordances
+ new_cross-level projections
- unsupported assumptions
- arbitrary auxiliary objects
- theorem leakage
```

No numeric optimization is required initially.

The working thesis is:

```text
GESTALT_VALUE ~= INFERENTIAL_CO_PRESENCE + REUSABLE_GENERATIVITY
```

---

# 9. Completion types: empirical labels, not yet primitive operators

The following phenomena should be logged during experiments but should **not** yet be hard-coded as separate primitive operators.

```text
RELATIONAL_COMPLETION
    separated relations become one correspondence packet

CORRESPONDENCE_CLOSURE
    a partial role-map expands toward a global figure correspondence

PLACEMENT_COMPLETION
    metric/angular constraints force a placement state

ROLE_COMPLETION
    an element acquires a new mathematical role after readout

DISTRIBUTED_COMPLETION
    locally separate relations become members of one distributed Gestalt

TRANSPORT_COMPLETION
    a relation becomes readable at another location through a carrier

LOCALIZATION_COMPLETION
    distributed relations are rearranged into one local synoptic configuration
```

After enough examples, recurrent labels may be compiled into higher-level operators.

---

# 10. Example template: congruence criterion inside a host Gestalt

For a pair of triangles with ASA-like data:

```text
P_ASA = {
    angle_1(T1) = angle_1(T2),
    carrier_side(T1) = carrier_side(T2),
    angle_2(T1) = angle_2(T2)
}
```

Before any transversal/parallel injection, v0.2 knows only:

```text
P_ASA matches ASA_ZERO_MASK
    -> FULL_CONGRUENCE_GESTALT
```

The following is an **experimental host hypothesis**, not a baseline fact:

```text
HYPOTHESIS:
P_ASA may embed into a future TRANSVERSAL/PARALLEL Gestalt as:

angle_1 equality
    <-> candidate DIRECTION_CLASS_1

angle_2 equality
    <-> candidate DIRECTION_CLASS_2

carrier-side equality
    <-> candidate METRIC_CARRIER / translated-carrier relation
```

If the transversal experiment validates that host mapping, then the completion cycle may yield:

```text
ASA_PAIR
 -> HOST(PARALLEL_GESTALT)
 -> direction classes become explicit
 -> COMPLETE distributed correspondence
 -> PROJECT back to triangle-pair view
 -> BACKWARD_ENRICH ASA
```

The enriched ASA view might then acquire a future affordance such as:

```text
EVOKE_PARALLEL_THROUGH_VERTEX
```

but this affordance must **not** be present before the host mapping is experimentally validated.

---

# 11. From local equality to structural explanation

The reasoner must distinguish:

```text
FACT:
    alpha = alpha'
```

from:

```text
STRUCTURAL EXPLANATION CANDIDATE:
    alpha and alpha' instantiate one distributed direction class
```

Thus a fact can acquire multiple host explanations over time.

```text
FactNode
    -> explained_by HostGestalt_A
    -> explained_by HostGestalt_B
    -> explained_by HostGestalt_C
```

This enables multi-family membership without collapsing distinct explanations.

---

# 12. Gestalt membership and embeddability

Introduce two distinct states.

```text
Embeddable(P, G)
```

means:

```text
P satisfies enough role constraints for a construction to potentially place it inside G.
```

while:

```text
Member(P, G)
```

means:

```text
a validated embedding/construction has established P as an instantiated view of G.
```

Transition:

```text
Embeddable(P,G)
    -> CONSTRUCT / VALIDATE
    -> Member(P,G)
```

This prevents the reasoner from turning visual similarity into unjustified Gestalt membership.

---

# 13. Internalize / externalize / host / project are distinct

These operators must not be conflated.

```text
EXTERNALIZE
    internal correspondence in one object
    -> correspondence across multiple objects

INTERNALIZE
    external correspondence
    -> self-correspondence in one object

HOST
    local pattern
    -> larger Gestalt in which it occupies named roles

PROJECT
    larger Gestalt
    -> local view/readout

REBASE
    peripheral/residual/currently secondary structure
    -> new active ground
```

A typical multi-step transformation may therefore be:

```text
ISOSCELES
 -> EXTERNALIZE
 -> ASA_PAIR
 -> HOST
 -> DISTRIBUTED_ANGULAR_GESTALT
 -> PROJECT
 -> ENRICHED_ASA
```

---

# 14. Backward enrichment as a first-class graph mutation

A later Gestalt may change what an earlier Gestalt is **for reasoning**.

Represent this explicitly:

```text
BackwardEnrichmentEdge {
    source_new_gestalt
    target_old_gestalt

    enrichment_type
    added_role
    added_affordance
    added_family_membership
    shortened_paths

    evidence_completion_event
    proposition_context
    provenance
}
```

Possible enrichment types:

```text
NEW_HOST_EXPLANATION
NEW_CONSTRUCTION_AFFORDANCE
NEW_FAMILY_MEMBERSHIP
NEW_PROJECTION_PATH
NEW_REBASE_ROUTE
ROLE_REINTERPRETATION
PATH_COMPRESSION
```

Backward enrichment does not alter the historical theorem statement.

It alters:

```text
InferencePacket(G_old)
```

into:

```text
InferencePacket(G_old)+
```

---

# 15. Construction affordances

The graph should store not only what follows from a Gestalt, but what constructions it suggests.

Example form:

```text
Affordance:
    IF active pattern has signature S
    AND host family G previously completed a matching pattern
    THEN propose construction C that attempts to recreate G
```

Thus later reasoning can move from:

```text
"Which theorem applies?"
```

to:

```text
"Which larger Gestalt could make these relations co-present,
and what construction would evoke it?"
```

This is one of the principal generative mechanisms of NMerovingio.

---

# 16. Operational search loop

A reasoning episode can now run at two interacting layers.

## 16.1 Local/counterfactual loop

```text
BASE
 -> MINIMAL BREAK
 -> CONTACTS
 -> CANDIDATES
 -> PROPAGATE / COLLIDE
 -> STABILIZE
 -> REBASE
```

## 16.2 Gestalt completion loop

```text
ACTIVE_PATTERN
 -> MATCH known families
 -> propose HOST candidates
 -> construct candidate embedding
 -> validate embedding
 -> COMPLETE host
 -> PROJECT readouts
 -> compare with active goal
 -> BACKWARD_ENRICH if new structural explanation found
 -> register EVOKE affordance
```

The reasoner may switch between loops when one stalls.

Example:

```text
counterfactual loop stalls
    -> search for host Gestalt
    -> complete in larger workspace
    -> project new constraint
    -> resume counterfactual loop
```

---

# 17. Suggested data-model additions

Extend the abstract Gestalt model:

```text
Gestalt {
    id
    level: OBJECT | PAIR | FAMILY

    workspace
    roles
    role_classes
    registers
    relations

    canonical_state
    stable_region
    counterfactual_region

    active_breaks
    fixed_contacts
    variation_axes

    residues
    symmetries

    family_memberships
    inference_packet

    host_links
    projection_links
    construction_affordances
    completion_history
    backward_enrichments

    genealogy
    provenance
}
```

Extend edge operators:

```text
GestaltEdge.operator = {
    ANALOGIZE,
    DISANALOGIZE,
    BREAK,
    OVERLAY,
    CUT_OFF,
    RESIDUALIZE,
    REBASE,

    EXTERNALIZE,
    INTERNALIZE,
    FAMILY_LIFT,
    INSTANTIATE,

    MATCH,
    HOST,
    COMPLETE,
    PROJECT,
    BACKWARD_ENRICH,
    EVOKE,
    COMPILE
}
```

---

# 18. Functional API sketch

This is intentionally implementation-neutral pseudocode.

```text
match_hosts(
    pattern: PartialPattern,
    network: CognitiveGraph,
    allowed_families=None
) -> list[HostCandidate]
```

```text
validate_host(
    pattern: PartialPattern,
    candidate: HostCandidate,
    proof_graph: ProofGraph
) -> HostCandidate
```

```text
complete(
    pattern: PartialPattern,
    host: HostCandidate,
    proof_graph: ProofGraph
) -> CompletionEvent
```

```text
project(
    completion: CompletionEvent,
    target_view: str
) -> Projection
```

```text
backward_enrich(
    old_gestalt: Gestalt,
    completion: CompletionEvent,
    projection: Projection
) -> EnrichedGestaltView
```

```text
evoke(
    enriched_view: EnrichedGestaltView,
    active_problem: PartialPattern
) -> list[ConstructionAffordance]
```

```text
run_completion_cycle(
    pattern,
    cognitive_graph,
    proof_graph
) -> CompletionCycleTrace
```

---

# 19. CompletionCycleTrace

Every cycle must be inspectable.

```text
CompletionCycleTrace {
    source_pattern

    match_candidates
    selected_host
    rejected_hosts

    construction_attempts
    embedding_validation

    completion_event
    projection

    backward_enrichment
    learned_affordances

    proof_dependencies_used
    circularity_checks

    network_delta
}
```

This trace is essential for comparing machine reasoning with Euclid's selected construction/proposition path.

---

# 20. Circularity guard

Because v0.2 deliberately introduces cognitive cycles, the validator must enforce a hard separation between **discovery** and **certification**.

## 20.1 Allowed

```text
A later theorem/Gestalt enriches an earlier Gestalt.
The enriched earlier Gestalt later suggests a construction resembling the later Gestalt.
```

## 20.2 Forbidden

```text
Use proposition P to construct host G,
then use G to certify proposition P,
while G itself depends on P.
```

Validation rule:

```text
proof_certificate(target=P)
    must be acyclic with respect to P
```

A cognitive cycle can generate hypotheses, constructions, and analogies.
Only an acyclic licensed proof path can certify the result.

---

# 21. Reinterpreting proposition updates

Extend `PropositionUpdate`:

```text
PropositionUpdate {
    proposition_id

    network_before
    start_gestalt
    construction

    invoked_gestalts
    selected_prior_propositions
    trajectory

    states_eliminated
    states_stabilized

    completion_events
    host_gestalts_used
    projections_created

    edges_added
    edges_reweighted

    gestalt_compiled
    gestalt_enriched

    new_family_memberships
    new_rebase_routes
    new_construction_affordances
    backward_enrichments

    network_after
}
```

A proposition can therefore contribute in at least four distinct ways:

```text
PROVE
    certify a new relation

COMPILE
    compress a repeated path into a reusable Gestalt/operator

CONNECT
    create a bridge between previously separate Gestalt families

ENRICH_BACKWARD
    change the inferential role of earlier structures
```

---

# 22. Revised experiment architecture

Preserve the original factual baseline:

```text
N0 = TRIANGLENET_0_1
```

Add the generic operational machinery of this file without adding new geometry:

```text
O = COMPLETION_CYCLE_OPERATORS

N0* = N0 + O
```

Important:

```text
GeometricFacts(N0*) = GeometricFacts(N0)
```

Only the **available meta-operations** differ.

Then independently build:

```text
T = TRANSVERSAL_INTERSECTION_NETWORK
```

and inject:

```text
N1 = INJECT(N0*, T)
```

Measure:

```text
DeltaN = N1 - N0*
```

---

# 23. Primary measurements after transversal injection

The experiment must record at least:

```text
NEW_HOST_MATCHES
NEW_COMPLETION_EVENTS
NEW_PROJECTIONS
NEW_BACKWARD_ENRICHMENTS
NEW_CONSTRUCTION_AFFORDANCES
NEW_REBASE_ROUTES
NEW_FAMILY_MEMBERSHIPS
PATH_SHORTENING
COUNTERFACTUAL_COLLAPSE
ROLE_REINTERPRETATION
```

Special attention:

```text
Does ASA gain a validated host in a transversal/parallel family?

Do equal-angle premises become interpretable as distributed direction classes?

Can a triangle Gestalt acquire an affordance to evoke a parallel through a vertex?

Can a parallel/transversal Gestalt project back into a congruence criterion?

Do I.5/I.6 or the isosceles family gain new angular-host interpretations?

Do old triangle Gestalten become more connected without adding new theorem facts?
```

---

# 24. Null hypothesis and non-forcing rule

Do not encode the expected ASA/parallel correspondence as true before the experiment.

The network must be allowed to return:

```text
NO_VALID_HOST
PARTIAL_HOST_ONLY
HOST_WITH_UNRESOLVED_BRIDGE
MULTIPLE_COMPETING_HOSTS
```

The experiment is valuable even if the expected host mapping fails.

The aim is to discover whether the transversal network actually reorganizes the triangle network under the generic completion machinery.

---

# 25. Updated research thesis

v0.1 hypothesis:

```text
Euclidean reasoning is progressive reorganization of a network of Gestalten.
```

v0.2 adds:

```text
A Gestalt does not only store relations.
It can make distributed relations inferentially co-present.

A later Gestalt can become a structural explanation of an earlier local pattern.

Once that explanation is learned, the earlier pattern can acquire the ability
to evoke the larger Gestalt constructively in future reasoning.
```

Therefore the network evolves through cycles of:

```text
LOCAL PATTERN
 -> LARGER HOST
 -> COMPLETION
 -> PROJECTION
 -> RETROACTIVE ENRICHMENT
 -> NEW CONSTRUCTION AFFORDANCE
```

or more compactly:

```text
RECOGNIZE THE WHOLE FROM THE PARTS
+
LEARN TO REGENERATE THE WHOLE FROM THE PARTS
```

This is the operational meaning of **circular Gestalt reasoning** in NMerovingio v0.2.
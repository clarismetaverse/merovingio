# Merovingio Cognitive Architecture v0.3

> Conceptual and operational redesign built on `TRIANGLE_GESTALT_NETWORK_V02.md` and the transversal experiments.
>
> v0.3 moves the project beyond a theorem-centric or analogy-centric reasoner. The central object is now a **dynamic cognitive network of constructive workspaces and Gestalt readings**, continuously reorganized by multiple types of impetus.
>
> Earlier files remain historical baselines. This file is the new architectural reference.

---

# 0. Core thesis

Merovingio should not treat mathematical concepts as isolated nodes connected by analogies.

The stronger hypothesis is:

```text
CONSTRUCTIVE FIELD / WORKSPACE
        |
        | selective organization / partialization
        v
GESTALT READING
        |
        | stabilization / compilation
        v
CONCEPTUAL OBJECT
```

A single material construction may support several simultaneous Gestalt readings.

Therefore:

```text
same construction != same Gestalt
same Gestalt != same genealogy
same final relation != same generative path
```

and:

```text
REACHABILITY != ANALOGICAL STRENGTH
```

In Euclidean geometry, many constructions can in principle be transformed into many others through points, lines, extensions, copies, overlays, cuts, and joins. Mere existence of a path is therefore weak evidence.

What matters is the **impact of a newly detected connection on the current cognitive network**.

---

# 1. Deep conceptual priority

## 1.1 Do not privilege pre-existing concepts

Merovingio must not assume that the primary units are concepts such as:

```text
ISOSCELES
CONGRUENCE
PARALLELISM
TRANSVERSAL
BISECTOR
PERPENDICULAR
```

These may instead be stabilized readings of deeper constructive organization.

A concept is provisionally modeled as:

```text
Concept ~= COMPILE(GestaltReading)
```

where a GestaltReading is itself a selective organization of a richer workspace.

## 1.2 Gestalt as partialization

A Gestalt is not merely a set of properties and not merely a visual shape.

Define:

```text
GestaltReading = Partialize(
    ConstructiveWorkspace,
    active_roles,
    active_relations,
    completion_rules,
    inferential_focus
)
```

A Gestalt therefore says:

```text
"read these elements of this workspace in these roles,
with these relations simultaneously active,
and with these completion affordances available"
```

## 1.3 Multiple readings of one workspace

The same material configuration may support, for example:

```text
VIEW A: triangle-pair congruence
VIEW B: transversal/intersection packets
VIEW C: parallel direction classes
VIEW D: possible triangular closure
VIEW E: straight-angle completion
```

These are not external analogies between separate universes.

They are **different inferential organizations of partially shared material structure**.

---

# 2. New primitive: ConstructiveWorkspace

The deepest shared object should be the workspace, not the named concept.

```text
ConstructiveWorkspace {
    id

    points
    rays
    lines
    segments
    angles
    regions

    incidence_relations
    order_relations
    equality_relations
    containment_relations
    side_of_line_relations

    construction_history
    available_operations

    active_gestalt_views
    latent_gestalt_candidates

    provenance
}
```

The workspace preserves material continuity while Gestalt readings may change.

Example:

```text
W = two triangle-shaped regions + a common carrier + line extensions

possible readings:
    G_congruence
    G_transversal
    G_parallel
    G_closure
```

---

# 3. Revised Gestalt schema

```text
Gestalt {
    id
    name
    level: OBJECT | PAIR | FAMILY

    workspace_id

    partialization_signature

    active_roles
    role_classes
    active_relations
    active_registers

    canonical_state
    stable_region
    counterfactual_region

    completion_affordances
    construction_affordances
    projection_affordances
    rebase_affordances

    fixed_contacts
    residues
    symmetries
    variation_axes

    family_memberships
    shared_realizations

    inference_packet
    genealogy
    provenance
}
```

## 3.1 PartializationSignature

```text
PartializationSignature {
    selected_elements
    ignored_or_backgrounded_elements
    role_assignment
    privileged_relations
    completion_mode
    active_ground
}
```

This allows two Gestalten to use the same workspace differently.

## 3.2 RoleClass

```text
RoleClass {
    id
    gestalt_id
    semantic_role
    members
    invariant
    origin
    provenance
}
```

Color in diagrams may render RoleClass membership, but color is never itself evidence.

---

# 4. Shared realization, overlap, and co-constitution

Do not encode every deep relation as `ANALOGY`.

Use stronger distinctions.

## 4.1 GESTALT_OVERLAP

Two Gestalten partially organize the same workspace or share material elements.

```text
GestaltOverlap {
    gestalt_a
    gestalt_b
    shared_workspace
    shared_elements
    shared_relations
    differently_assigned_roles
}
```

## 4.2 SHARED_REALIZATION

One construction realizes both Gestalten at once.

```text
SharedRealization {
    workspace
    gestalt_a
    gestalt_b
    simultaneous_role_map
}
```

## 4.3 CONVERGENT_READOUT

Different genealogies produce the same final relation.

Example:

```text
ISOSCELES -> angle equality
VERTICAL OPPOSITION -> angle equality
PARALLEL HOST -> angle equality
```

The equality-state is shared; genetic identity is not.

## 4.4 CO_CONSTITUTION

Use when two Gestalten become mutually explanatory inside a shared construction.

```text
CoConstitution {
    workspace
    gestalt_a
    gestalt_b

    a_makes_visible_in_b
    b_makes_visible_in_a

    backward_enrichments
    shared_construction_affordances
}
```

This is stronger than superficial analogy but does not assert that the concepts are identical.

---

# 5. Analogy becomes network-relative

An analogy has no useful absolute strength.

Define:

```text
AnalogyStrength(A, B | NetworkState_t)
```

not merely:

```text
AnalogyStrength(A, B)
```

The same connection may be surprising at time `t` and obvious after the network is reorganized.

## 5.1 Strong analogy criterion

A connection is strong when it exerts pressure on the current network.

Candidate components:

```text
SURPRISE
    current network predicted the concepts should be distant

COMPRESSION_GAIN
    one new organization shortens many previous paths

CONNECTIVITY_GAIN
    previously separate families become structurally connected

GENERATIVE_GAIN
    new constructions or predictions become available

DIAGNOSTIC_POWER
    reveals that current roles/families/granularity are inadequate

SYNOPTIC_GAIN
    more relations become simultaneously readable
```

No numeric scoring is required initially.

## 5.2 Possible effects of a strong analogy

```text
ADD_EDGE
ADD_GESTALT
ADD_FAMILY
ADD_SHARED_WORKSPACE
PROMOTE_HIDDEN_REGISTER
REFACTOR_ROLES
SPLIT_GESTALT
MERGE_FAMILIES
CHANGE_CANONICAL_ZERO
REFACTOR_NETWORK
```

A powerful analogy may therefore modify the graph schema itself, not merely add a link.

---

# 6. Commonality is a probe, not a conclusion

When two objects show high-level commonality, Merovingio must not immediately conclude that they instantiate one abstract generic structure.

Instead:

```text
COMMONALITY
    -> DECOMPILE
    -> TRACE GENERATORS
    -> TRACE FAMILIES
    -> TRACE WORKSPACES
    -> COMPARE GENEALOGIES
    -> RECONSTRUCT CANDIDATE SHARED STRUCTURE
    -> VALIDATE
```

The commonality asks:

```text
WHY do these structures look alike in the current network?
```

Possible answers include:

```text
SAME_FAMILY
SHARED_ANCESTRAL_GESTALT
SHARED_WORKSPACE_PARTIALIZATION
GENERATOR_OVERLAP
SHARED_OPERATOR_PACKET
SHARED_COMPLETION_DYNAMICS
CONVERGENT_READOUT_ONLY
SUPERFICIAL_SIMILARITY
```

---

# 7. DECOMPILE as first-class operator

Earlier versions emphasized `COMPILE`.

v0.3 requires its explicit inverse-like operation:

```text
DECOMPILE
```

`DECOMPILE(X)` does not erase a concept. It reopens its constructional and inferential history.

```text
DECOMPILE(X) -> {
    generating_gestalts,
    construction_history,
    family_memberships,
    role_classes,
    completion_events,
    residues,
    rebases,
    operators_used,
    shared_workspaces,
    ancestral_paths
}
```

This supports conceptual archaeology.

---

# 8. Genealogical search

Introduce:

```text
TRACE_GESTALT_ANCESTRY(X)
COMPARE_ANCESTRY(A, B)
```

Example output:

```text
AncestryComparison {
    shared_families
    shared_ancestral_gestalts
    shared_workspaces
    shared_generators
    shared_operators
    shared_break_signatures
    shared_completion_patterns
    convergent_readouts
    conflicting_genealogies
}
```

The genealogy is a DAG, not necessarily one linear chain.

---

# 9. Impetus becomes a typed cognitive pressure

`Impetus` is no longer one generic notion.

It represents a pressure created by the mismatch between:

```text
what the current network can already see
```

and:

```text
what the active construction seems to make possible
```

Schema:

```text
Impetus {
    id
    type

    source_workspace
    source_gestalt
    trigger_event

    active_tension
    broken_expectation
    unresolved_relation

    suggested_direction
    expected_gain
    urgency
    confidence

    provenance
}
```

## 9.1 Initial impetus types

```text
COMPLETION_IMPETUS
    "this partial structure wants to close"

BREAK_IMPETUS
    "the present network cannot comfortably absorb this connection"

EXPANSION_IMPETUS
    "this structure has fertile unexplored variants"

GENEALOGICAL_IMPETUS
    "this commonality may have a deeper shared constitution"

REBASE_IMPETUS
    "a peripheral/residual element can become a new ground"

COMPRESSION_IMPETUS
    "this recurrent reasoning path may deserve compilation"

VALIDATION_IMPETUS
    "a cognitive candidate now needs geometric certification"

HOST_IMPETUS
    "this local pattern may be a projection of a richer workspace"
```

---

# 10. Multi-agent architecture

Merovingio v0.3 is not one monolithic reasoner.

The generic core maintains the state and emits tensions. Specialized agents respond to different impetus types.

```text
                         MEROVINGIO CORE
                               |
                        events / tensions
                               |
                               v
                         IMPETUS ROUTER
                               |
      +-------------+----------+----------+-------------+
      |             |          |          |             |
      v             v          v          v             v
 COMPLETE       EXPAND    REORGANIZE   GENEALOGY     COMPILE
  AGENT          AGENT       AGENT       AGENT         AGENT
      \             |          |          |             /
       \            |          |          |            /
        +------------+----------+----------+-----------+
                               |
                           proposals
                               |
                               v
                            VALIDATOR
                               |
                               v
                         NETWORK COMMIT
```

No creative agent directly mutates the canonical network.

---

# 11. Generic Merovingio Core

Responsibilities:

```text
- maintain ConstructiveWorkspaces
- maintain Gestalt graph
- maintain ProofGraph separately
- preserve genealogy
- preserve residue provenance
- track family membership
- emit events and tensions
- route Impetus objects
- store proposals
- arbitrate accepted network updates
```

The core should remain relatively conservative.

It is not responsible for inventing every restructuring itself.

---

# 12. Completion / Optimization Agent

Primary impetus:

```text
COMPLETION_IMPETUS
HOST_IMPETUS
```

Bias:

```text
"the present representation is probably useful;
extract more of what is already latent in it"
```

Operations:

```text
MATCH
HOST
COMPLETE
PROJECT
PROPAGATE
CLOSE_PACKET
SHORTEN_PATH
MERGE_ROLE_CLASSES_IF_LICENSED
FIND_ZERO_MASK
```

Typical example:

```text
alpha_P = alpha_Q
alpha_P + beta_P = STRAIGHT
alpha_Q + beta_Q = STRAIGHT

-> beta_P = beta_Q
```

It optimizes existing structure rather than redesigning it.

---

# 13. Expansion / Explorer Agent

Primary impetus:

```text
EXPANSION_IMPETUS
REBASE_IMPETUS
```

Bias:

```text
"what nearby structure has not yet been explored?"
```

Operations:

```text
BREAK
DISANALOGIZE
COUNTERFACTUAL_VARIATION
RESIDUALIZE
REBASE
EXTERNALIZE
INTERNALIZE
DISTRIBUTE
LOCALIZE
HOST_SEARCH
GENERATE_NEIGHBORHOOD
FAMILY_EXPANSION
```

It treats surviving counterfactuals and residues as potentially productive, not merely as failures.

---

# 14. Reorganization Agent

Primary impetus:

```text
BREAK_IMPETUS
strong analogy with poor current explanation
repeated exceptions
unexpected short bridge between distant regions
```

Bias:

```text
"perhaps the network representation itself is wrong"
```

This is the agent most sensitive to conceptual rupture.

Candidate operations:

```text
SPLIT_GESTALT
MERGE_FAMILIES
INTRODUCE_SHARED_WORKSPACE
PROMOTE_HIDDEN_REGISTER
REFACTOR_ROLES
CHANGE_CANONICAL_ZERO
INTRODUCE_NEW_FAMILY
REASSIGN_PARTIALIZATION
REFACTOR_NETWORK
```

It may propose a new ontology/granularity.

Example:

```text
OLD:
CONGRUENCE ---- analogy ---- PARALLELISM

PROPOSED:
            SHARED CONSTRUCTIVE FIELD
               /               \
      CONGRUENCE VIEW      PARALLEL VIEW
```

The proposal remains cognitive until validated and committed.

---

# 15. Genealogy / Decompilation Agent

Primary impetus:

```text
GENEALOGICAL_IMPETUS
```

Bias:

```text
"do not explain similarity by abstraction until generative history has been inspected"
```

Operations:

```text
DECOMPILE
TRACE_GESTALT_ANCESTRY
COMPARE_ANCESTRY
TRACE_GENERATORS
TRACE_SHARED_WORKSPACES
TRACE_BREAK_SIGNATURES
TRACE_COMPLETION_HISTORY
RECONSTRUCT_SHARED_ANCESTOR
```

Possible outputs:

```text
SAME_FAMILY
SHARED_ANCESTRAL_GESTALT
SHARED_WORKSPACE_PARTIALIZATION
GENERATOR_OVERLAP
CONVERGENT_READOUT_ONLY
NO_DEEP_LINK_FOUND
```

This agent prevents "everything is analogous to everything" from becoming an explanatory dead end.

---

# 16. Compiler Agent

Primary impetus:

```text
COMPRESSION_IMPETUS
```

Bias:

```text
"recurrent reasoning should become directly readable"
```

Operations:

```text
COMPILE_PATH
COMPILE_OPERATOR
COMPILE_GESTALT
COMPILE_FAMILY
CACHE_PROJECTION
CACHE_HOST_AFFORDANCE
```

Core principle:

```text
reasoning past -> object present
```

Examples:

```text
repeated side-order <-> angle-order reasoning
    -> OBJECT_ORDER_TRANSDUCER

repeated intersection completion
    -> TWO-ROLE_ANGULAR_PACKET
```

Compilation is necessary to prevent uncontrolled network growth.

---

# 17. Validator Agent

The Validator is epistemically separate from all creative agents.

Responsibilities:

```text
- check construction feasibility
- check proposition licensing
- check proof circularity
- distinguish proof facts from cognitive hypotheses
- detect theorem leakage
- verify preserved contacts
- verify claimed role mappings
- verify residue accounting
- reject unsupported host membership
```

Status vocabulary:

```text
SEED
COGNITIVE_CANDIDATE
CONSTRUCTIBLE_CANDIDATE
PROP_LICENSED
VALIDATED_GESTALT
COMPILED
REJECTED
OPEN
```

The cognitive graph may contain cycles.

The proof graph may not certify a theorem using itself.

Therefore:

```text
COGNITIVE_CYCLE != LOGICAL_CIRCULARITY
```

---

# 18. Impetus Router

The router decides which agents should inspect an event.

It is allowed to dispatch the same event to multiple agents.

Example:

```text
EVENT = STRONG_COMMONALITY(A,B)
```

Possible routing:

```text
CompletionAgent:
    can existing structure explain/complete the link?

GenealogyAgent:
    do A and B share generators/workspaces/families?

ReorganizationAgent:
    does the current network incorrectly keep A and B apart?

ExpansionAgent:
    what new family members should exist if the connection is real?

CompilerAgent:
    is this connection recurrent enough to compile?
```

The outputs are not votes. They are different cognitive operations on one tension.

---

# 19. Proposal Blackboard

Agents write proposals to a shared intermediate layer rather than mutating the graph.

```text
NetworkProposal {
    id
    proposing_agent
    source_impetus

    proposal_type
    affected_workspaces
    affected_gestalts
    affected_families

    proposed_nodes
    proposed_edges
    proposed_role_changes
    proposed_rebases

    expected_gain
    expected_risks

    required_validation
    evidence
    provenance
}
```

Proposal types:

```text
ADD_EDGE
ADD_GESTALT
ADD_FAMILY
ADD_HOST_LINK
ADD_SHARED_WORKSPACE
ADD_CONSTRUCTION_AFFORDANCE
REFACTOR_ROLES
SPLIT_GESTALT
MERGE_FAMILIES
REFACTOR_NETWORK
COMPILE_PATH
```

---

# 20. Network update protocol

Canonical mutation pipeline:

```text
EVENT
  -> IMPETUS
  -> ROUTE
  -> AGENT PROPOSALS
  -> VALIDATE
  -> COMPARE ALTERNATIVES
  -> COMMIT
  -> RECOMPUTE LOCAL CONSEQUENCES
  -> EMIT NEW IMPETUS
```

Thus the network can evolve recursively without uncontrolled direct writes.

---

# 21. Three levels remain, but are now readings rather than ontological boxes

Earlier levels remain useful:

```text
OBJECT
PAIR
FAMILY
```

but they are organizational frequencies, not rigid entity types.

## OBJECT

One configuration under one active role organization.

## PAIR

Correspondence/disanalogy/overlay between two configurations.

## FAMILY

Governed space of canonical zero, stable variants, counterfactual regions, symmetries, and rebase routes.

Cross-level operators remain:

```text
EXTERNALIZE
INTERNALIZE
FAMILY_LIFT
INSTANTIATE
REBASE
PROJECT
HOST
```

A shared workspace may support Gestalten at multiple levels simultaneously.

---

# 22. Rebase revised

`REBASE` changes active inferential ground while preserving material configuration and genealogy when possible.

```text
REBASE(G, x)
    x peripheral/residual/secondary
        ->
    x active ground in G'
```

Types:

```text
HORIZONTAL_REBASE
    change canonical focus inside one family

VERTICAL_REBASE
    reinterpret a structure as a member/substructure of a richer family

CROSS_LEVEL_REBASE
    OBJECT <-> PAIR <-> FAMILY

VIEW_REBASE
    same workspace, different Gestalt partialization becomes active
```

`VIEW_REBASE` is new in v0.3 and is central for triangle/congruence/transversal/parallel reinterpretation.

---

# 23. Completion revised

`COMPLETE` means more than filling missing slots.

```text
COMPLETE(P,G)
```

requires:

```text
1. validated role mapping
2. constructible host relation
3. host invariants
4. newly co-present relations
5. traceable readout back to the source pattern
```

Strong completion cycle:

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

The key learning condition is:

```text
P+ can later regenerate the host that once explained it.
```

---

# 24. Circular reasoning revised

Circularity in the cognitive network is desirable when it represents mutual enrichment.

Example:

```text
TRIANGLE PATTERN
 -> hosted in TRANSVERSAL/PARALLEL view
 -> new distributed angular organization
 -> projected back to TRIANGLE
 -> triangle gains new construction affordance
 -> future triangle can evoke TRANSVERSAL/PARALLEL view
```

This is not proof circularity.

It is **representational bootstrapping**.

---

# 25. Deep commonality search

When a strong commonality is detected:

```text
COMMONALITY(A,B)
```

Merovingio should run:

```text
1. current-network explanation check
2. DECOMPILE(A)
3. DECOMPILE(B)
4. COMPARE_ANCESTRY(A,B)
5. compare shared workspaces
6. compare shared generators/operators
7. compare completion dynamics
8. reconstruct candidate common organization
9. validate constructionally
10. decide whether to:
       ADD_EDGE
       ADD_GESTALT
       ADD_FAMILY
       REFACTOR_NETWORK
```

The system should prefer the deepest explanation that survives validation, not the most abstract verbal description.

---

# 26. Generative depth of a similarity

A useful qualitative scale:

```text
DEPTH 0
    same final property

DEPTH 1
    same relation schema

DEPTH 2
    same operator packet

DEPTH 3
    shared Gestalt generator

DEPTH 4
    shared family / ancestral family

DEPTH 5
    same constructive workspace partialized differently
```

This is not a truth ranking. It is a heuristic for where to search next.

---

# 27. Analogy as network pressure

The strongest formulation in v0.3 is:

```text
A strong analogy is not valuable because it links two objects.
It is valuable because it exerts pressure on the best organization
of the current cognitive network.
```

Therefore:

```text
STRONG_ANALOGY
    -> possible NETWORK_REVISION
```

A weak analogy may merely add a redundant route.

A strong analogy may expose:

```text
missing role
missing register
wrong family boundary
wrong canonical zero
wrong node granularity
missing shared workspace
premature compilation
```

---

# 28. Conceptual failure modes

The Reorganization Agent should detect at least:

```text
EDGE_OVERLOAD
    too many ad-hoc cross-family edges

EXCEPTION_OVERLOAD
    one Gestalt requires repeated special cases

DUPLICATED_REASONING
    same constructional logic appears under unrelated concepts

HIDDEN_REGISTER
    recurrent residue cannot be represented in current schema

WRONG_GRANULARITY
    named concepts are too coarse to explain shared operators

PREMATURE_ABSTRACTION
    abstract similarity was accepted before generator search

PREMATURE_COMPILATION
    one local proof path was promoted to a universal Gestalt too early
```

Each should emit `BREAK_IMPETUS` or `GENEALOGICAL_IMPETUS`.

---

# 29. Example: congruence / transversal / parallel field

Current experimental hypothesis:

```text
ConstructiveWorkspace W
    contains triangles, lines, extensions, intersections, angles

Possible readings:
    G_TRIANGLE_PAIR
    G_CONGRUENCE
    G_TRANSVERSAL
    G_PARALLEL
    G_CLOSURE
```

The system should not encode:

```text
CONGRUENCE isomorphic_to PARALLEL
```

Instead it should test:

```text
- do they share a workspace?
- do they share carrier roles?
- do they use related completion dynamics?
- do they converge on angle equalities through different genealogies?
- can one view project into the other?
- can one view evoke the construction of the other?
- does their overlap force a new family-level organization?
```

Possible result:

```text
GESTALT_OVERLAP
SHARED_REALIZATION
CO_CONSTITUTION
```

rather than abstract isomorphism.

---

# 30. Example: zero states remain local to registers

Do not collapse all zeros into one concept.

Examples:

```text
ZERO_SIDE_DISANALOGY
    isosceles side equality

ZERO_PLACEMENT_RESIDUE
    coincidence under overlay

ZERO_DIRECTION_RESIDUE
    candidate parallel direction class

ZERO_STRAIGHT_COMPLETION_RESIDUE
    two angular parts complete one straight whole
```

High-symmetry objects may later emerge as intersections of several zero conditions.

This will be important for later experiments on parallelogram/rhombus/rectangle/square families.

---

# 31. Agent-specific objectives

There is deliberately no single global objective function.

```text
CompletionAgent
    maximize closure/coherence using current structure

ExpansionAgent
    maximize fertile reachable structure

ReorganizationAgent
    maximize explanatory adequacy of representation

GenealogyAgent
    maximize generative depth of explanations

CompilerAgent
    maximize reusable compression

ValidatorAgent
    maximize epistemic licensing / prevent false certification
```

Intelligence is expected to emerge from the tension among these objectives.

---

# 32. Suggested implementation skeleton

```text
MerovingioCore
    WorkspaceStore
    GestaltStore
    FamilyStore
    ProofGraph
    CognitiveGraph
    GenealogyStore
    EventBus
    ImpetusRouter
    ProposalBlackboard
    NetworkCommitter

Agents
    CompletionAgent
    ExpansionAgent
    ReorganizationAgent
    GenealogyAgent
    CompilerAgent
    ValidatorAgent
```

Pseudo-loop:

```text
while active_problem_or_experiment:
    events = core.observe()

    for event in events:
        impetus_list = router.classify(event)

        for impetus in impetus_list:
            agents = router.dispatch(impetus)

            for agent in agents:
                proposals += agent.run(core.snapshot(), impetus)

    validated = validator.evaluate(proposals, core.snapshot())
    committed_updates = committer.select_and_apply(validated)

    core.emit_consequences(committed_updates)
```

---

# 33. Required graph queries in v0.3

The graph should eventually support:

```text
1. Which Gestalten partially organize workspace W?
2. Which material elements change role across two Gestalt readings?
3. Which concepts are compiled from the same workspace?
4. Which equal final relations have different genealogies?
5. Which strong analogies caused network refactors?
6. Which family boundaries are crossed by repeated constructions?
7. Which hidden registers are suggested by recurrent residues?
8. Which Gestalten are reachable by VIEW_REBASE without new construction?
9. Which similarities are only convergent readouts?
10. Which similarities have shared generators?
11. Which commonalities reach DEPTH 5 shared-workspace status?
12. Which network regions have exception overload?
13. Which paths are recurrent enough to compile?
14. Which compiled concepts can be decompressed back into their generating workspaces?
15. Which later Gestalten backward-enriched earlier concepts?
16. Which construction affordances were learned through circular completion cycles?
```

---

# 34. Experimental protocol going forward

For every new Euclidean domain:

```text
A. build local constructive workspace
B. identify candidate Gestalt readings
C. keep proof facts separate from cognitive readings
D. run completion/exploration/disanalogy
E. inject into existing network
F. measure new overlaps and backward enrichments
G. detect strong commonalities
H. run genealogical search
I. allow ReorganizationAgent to propose refactors
J. validate
K. compile only after recurrence/stability
```

The next running domain remains:

```text
TRANSVERSAL -> PARALLEL -> TRIANGLE BACKWARD ENRICHMENT
```

Later candidate domains:

```text
PARALLELOGRAM / RHOMBUS / RECTANGLE / SQUARE
EQUILATERAL / BISECTOR / MIDPOINT / PERPENDICULAR
CIRCLE / RADIUS / EQUIDISTANCE
```

---

# 35. Research thesis of v0.3

The project now tests the following stronger hypothesis:

```text
Mathematical intelligence is not primarily navigation among fixed concepts.

It is the ability to:

- organize a constructive field into Gestalten;
- switch partializations of the same field;
- detect productive disanalogies;
- complete partial structures;
- trace the genealogy of surprising commonalities;
- reorganize the conceptual network when a strong relation breaks its current ontology;
- compile recurrent reasoning into new directly readable structure;
- reopen compiled concepts when deeper structure becomes relevant.
```

Compactly:

```text
CONSTRUCT
 -> PARTIALIZE
 -> GESTALT
 -> EXPLORE / COMPLETE / BREAK
 -> REBASE / HOST / PROJECT
 -> GENEALOGICAL SEARCH
 -> REORGANIZE
 -> VALIDATE
 -> COMPILE
 -> DECOMPILE WHEN NEEDED
 -> REPEAT
```

The network is therefore not a static graph of concepts.

It is a **self-reorganizing cognitive geometry**.

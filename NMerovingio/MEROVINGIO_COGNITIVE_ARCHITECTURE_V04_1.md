# Merovingio Cognitive Architecture v0.4.1 — Workspace Co-Constitution and Medial Carriers

> **Phase:** cognitive / unification  
> **Status:** architectural refinement of v0.4; not theorem proving  
> **Active reference:** v0.4 + this refinement  
> **New center of gravity:** the workspace is not passive support but a **derivational environment** in which multiple Gestalten co-participate through materially shared carriers.

---

# 0. Core correction

v0.4 correctly made the Family Atlas the multiperspectival conceptual organization of one constructive support.

v0.4.1 adds the missing concrete layer:

~~~text
WORKSPACE
!=
passive container of already-formed Gestalten
~~~

Instead:

~~~text
WORKSPACE
=
GENETIC FIELD OF CO-CONSTITUTING GESTALTEN
CONNECTED BY SHARED MATERIAL CARRIERS
~~~

The workspace is the place where:

- several Gestalten coexist,
- several families become simultaneously available,
- one material element participates in multiple Gestalten,
- relations can be carried across those participations,
- new higher Gestalten become visible because lower Gestalten are already materially interwoven.

The Family Atlas is the multiperspectival conceptual organization of that field.

So the architecture becomes:

~~~text
DERIVATIONAL WORKSPACE
    ↓
co-participating Gestalten
    ↓
medial carriers / shared regions
    ↓
cross-Gestalt relation transport
    ↓
family atlas
    ↓
higher stabilization / new class of objects
~~~

---

# 1. Workspace as environment of derivation

A workspace should no longer be represented as:

~~~text
Workspace {
  points
  lines
  segments
  active_gestalts
}
~~~

only.

It should be represented as a **living local environment**:

~~~text
ConstructiveWorkspace {
    material_elements
    material_regions
    incidence_structure

    active_gestalts[]
    latent_gestalts[]

    medial_carriers[]
    shared_regions[]
    carrier_participations[]

    family_realizations[]
    family_charts[]

    co_constitution_structure
    derivational_routes[]
    latent_rebases[]

    genealogy
}
~~~

The workspace therefore contains not only objects, but the **conditions under which objects derive from one another**.

---

# 2. Shared interpretation is weaker than shared participation

v0.4 emphasized that one material element may receive different roles in different Gestalten.

v0.4.1 distinguishes two cases.

## 2.1 Multiple interpretation

~~~text
same material segment S

in G1:
  role = side

in G2:
  role = diagonal
~~~

This already matters.

But it is still only:

~~~text
ONE OBJECT
+
MULTIPLE READINGS
~~~

## 2.2 Shared material participation

A stronger case is:

~~~text
S materially belongs to G1
AND
S materially belongs to G2
AND
S is one of the elements through which G1 and G2
are jointly constituted in a larger workspace.
~~~

Then S is not merely interpreted twice.

It is a **common constitutive element**.

This yields:

~~~text
MULTIPLE_INTERPRETATION
!=
CO_CONSTITUTIVE_PARTICIPATION
~~~

---

# 3. MedialCarrier

Introduce a new ontological entity type:

~~~text
MedialCarrier
~~~

This is **not an operator**.

A MedialCarrier is a materially identical element that participates in several Gestalten and preserves enough relational structure to make cross-Gestalt organization possible.

Conceptual schema:

~~~text
MedialCarrier {
    id
    material_identity

    carrier_kind:
      POINT
      SEGMENT
      LINE
      RAY
      ANGLE
      REGION
      CIRCLE
      ARC
      FACE
      SOLID_SECTION
      OTHER

    participates_in[]:
      {
        gestalt_id
        family_id
        local_role
        role_class
        active_relations
      }

    carried_relations[]
    preserved_contacts[]
    orientation_data

    genealogy

    rebase_potential
    blending_potential
    classification_potential
}
~~~

---

# 4. Why “medial”

The carrier is “medial” because it stands **between several Gestalt organizations without being external to them**.

It is simultaneously:

~~~text
inside G1
inside G2
inside G3
...
~~~

and therefore can mediate:

~~~text
G1 <-> G2
G2 <-> G3
G1 <-> higher blend
~~~

without creating a separate copied element for each view.

This is stronger than analogy.

It is stronger than an edge saying two figures “share a side.”

It is a statement of **common material constitution**.

---

# 5. Example: diagonal as medial carrier

Take a quadrilateral ABCD with diagonal AC.

The same material segment AC may be:

~~~text
in triangle ABC:
  side

in triangle ACD:
  side

in quadrilateral ABCD:
  diagonal

in a parallel-family reading:
  transversal

in a symmetry-family reading:
  possible axis / carrier

in a correspondence family:
  shared identity bridge
~~~

There are not five copies of AC.

There is one:

~~~text
material_identity = AC
~~~

with several participations.

Therefore:

~~~text
AC_triangle_1
=
AC_triangle_2
=
AC_quadrilateral
=
AC_transversal
~~~

by material identity, not analogy.

This is exactly why AC can carry relations between the corresponding Gestalten.

---

# 6. CarrierParticipation

A carrier needs an explicit participation record.

~~~text
CarrierParticipation {
    carrier_id
    gestalt_id
    family_id

    local_role
    local_orientation
    local_relations

    constitutive_weight:
      CORE
      BOUNDARY
      BRIDGE
      RESIDUAL
      LATENT

    shared_with[]
}
~~~

This allows the system to say:

~~~text
AC is CORE in triangle ABC
AC is CORE in triangle ACD
AC is BRIDGE in diagonal correspondence
AC is TRANSVERSAL in the parallel reading
~~~

while preserving one material identity.

---

# 7. Co-constitution

The workspace should explicitly represent when several Gestalten are not merely colocated but **co-constitute** a higher organization.

~~~text
CoConstitutionStructure {
    workspace_id

    participating_gestalts[]
    shared_carriers[]
    shared_regions[]

    mutual_dependencies[]
    higher_gestalt_candidates[]

    blending_mode
    genealogy
}
~~~

Possible blending modes:

~~~text
OVERLAP
HINGE
SHARED_CARRIER
SHARED_REGION
MUTUAL_BOUNDARY
NESTED
RESIDUAL
INTERSECTION
CROSSING
COINCIDENT_ROLE
OTHER
~~~

Again: these are descriptive modes, not operators.

---

# 8. Fused / blended objects

Sometimes the same medial carrier does more than connect two Gestalten.

It supports a higher object in which their local organizations are **fused**.

Example:

~~~text
triangle G1
triangle G2
shared AC
        ↓
same workspace
        ↓
higher quadrilateral / correspondence Gestalt
~~~

The higher object is not simply:

~~~text
G1 + G2
~~~

It is:

~~~text
BLEND(
  G1,
  G2,
  shared material carrier AC,
  cross-role correspondences,
  preserved contacts
)
~~~

This does not require a new BLEND operator in the kernel.

“Blend” here names a **workspace state of co-constitution**.

---

# 9. Medial carriers as relation carriers

A MedialCarrier can carry more than identity.

It may carry:

~~~text
orientation
adjacency
order
equality context
incidence
direction class
opposition
boundary role
residue
symmetry pressure
~~~

across several Gestalten.

This is why one shared segment may make a relation visible in one family and re-readable in another.

Conceptually:

~~~text
RELATION IN G1
        ↓
shared carrier participation
        ↓
RELATIONAL PRESSURE IN G2
~~~

The carrier does not “prove” the relation.

It makes the cross-Gestalt transport cognitively available.

---

# 10. Germini medi / medial seeds

A particularly important subclass is the **MedialSeed**.

A MedialSeed is a carrier whose multi-participation has not yet been fully exploited, but whose presence makes new rebases or higher Gestalten likely.

~~~text
MedialSeed {
    carrier_id

    current_participations[]
    latent_participations[]

    unresolved_relational_pressure
    candidate_family_bridges[]
    candidate_higher_gestalts[]
}
~~~

Examples:

~~~text
diagonal in a quadrilateral
intersection point of two circles
common tangent
shared chord
axis through two constructions
common face of two solids
section plane through a solid
~~~

The MedialSeed is therefore a **carrier of derivational potential**.

---

# 11. Workspace and Family Atlas have different roles

The distinction should now be explicit.

## Workspace

~~~text
WORKSPACE
=
concrete genetic field
~~~

It stores:

~~~text
material identity
co-participation
shared carriers
shared regions
constructional contact
latent blends
derivational potential
~~~

## Family Atlas

~~~text
FAMILY ATLAS
=
multiperspectival conceptual organization
of the same genetic field
~~~

It stores:

~~~text
charts
strata
fibers
family positions
rebases
cross-chart genealogies
stabilizations
~~~

Therefore:

~~~text
WORKSPACE : ATLAS
=
GENETIC FIELD : CONCEPTUAL ORGANIZATION
~~~

Neither reduces to the other.

---

# 12. DerivationEnvironment

A workspace may now be summarized at a higher level as:

~~~text
DerivationEnvironment {
    workspace_id

    current_gestalts[]
    current_families[]

    medial_carriers[]
    medial_seeds[]

    co_constitution_clusters[]

    available_rebases[]
    latent_family_transitions[]

    emerging_object_classes[]
}
~~~

This is the layer that makes visible:

> how one class of objects can arise from the interaction of Gestalten belonging to different families.

---

# 13. Object-class derivation

A new object class may emerge when several Gestalten repeatedly stabilize around the same carrier structure.

Example:

~~~text
parallel family
+ transversal family
+ diagonal triangle-pair medium
+ shared carriers
        ↓
recurrent cross-family organization
        ↓
parallelogram-like class
~~~

The new class is therefore not defined only by a property list.

It can be identified by:

~~~text
GENETIC SIGNATURE
+
CARRIER PARTICIPATION PATTERN
+
FAMILY ATLAS POSITION
~~~

This gives Merovingio a richer way to recognize derived classes.

---

# 14. Multi-perspectival hierarchy through carrier structure

Hierarchies can now be generated from carrier participation.

Example:

~~~text
segment AC
  participates in:
    triangle ABC
    triangle ACD
    quadrilateral ABCD
    transversal reading
    correspondence reading
~~~

This induces a local hierarchy:

~~~text
material carrier
   ↓
local Gestalten
   ↓
family charts
   ↓
higher blended Gestalt
~~~

But another carrier may induce a different hierarchy over the same workspace.

Therefore the system naturally supports:

~~~text
MULTIPLE OVERLAPPING HIERARCHIES
~~~

anchored in different medial carriers.

---

# 15. Visual architecture

The new workspace ontology should be directly visible.

## 15.1 Material layer

Show the figure normally.

## 15.2 Carrier layer

Highlight medial carriers with a distinct interaction state.

Selecting one carrier should reveal:

~~~text
all Gestalten it participates in
all local roles
all family memberships
all carried relations
all latent rebases
~~~

## 15.3 Co-constitution layer

Show clusters such as:

~~~text
G1
 \
  AC
 /
G2
  \
   G_higher
~~~

where the shared carrier remains visually the same object.

## 15.4 Atlas layer

Show how each participating Gestalt appears in its families.

This yields a synchronized visual explanation:

~~~text
same material element
-> several local roles
-> several family positions
-> one higher derivation
~~~

---

# 16. Perspective switch must preserve carrier identity

When switching perspectives:

~~~text
triangle view
quadrilateral view
parallel view
circle view
~~~

the same medial carrier should remain anchored.

Only its role and relational halo should change.

Example:

~~~text
AC remains AC
~~~

while labels shift:

~~~text
SIDE
SIDE
DIAGONAL
TRANSVERSAL
IDENTITY BRIDGE
~~~

This is the visual expression of:

~~~text
MATERIAL IDENTITY PRESERVED
ROLE IDENTITY CHANGES
FAMILY PARTICIPATION CHANGES
~~~

---

# 17. Coherence monitor additions

The discovery-phase coherence monitor should now check:

~~~text
MEDIAL CARRIER IDENTITY CONSISTENCY
PARTICIPATION CONSISTENCY
CO-CONSTITUTION CONSISTENCY
NO DUPLICATION OF ONE MATERIAL CARRIER ACROSS VIEWS
NO FALSE FUSION OF DISTINCT MATERIAL ELEMENTS
CROSS-GESTALT ROLE COMPATIBILITY
GENEALOGY CONTINUITY ACROSS CARRIER PARTICIPATIONS
~~~

This remains high-level coherence checking, not theorem proving.

---

# 18. No new operator proliferation

v0.4.1 adds no operator.

The following are ontology / data-structure additions:

~~~text
MedialCarrier
CarrierParticipation
MedialSeed
CoConstitutionStructure
DerivationEnvironment
~~~

Existing operators remain sufficient:

~~~text
BREAK
REBASE
REINDIVIDUATE
PARTITION_WORKSPACE
HOST
PROJECT
RECOMPOSE_GESTALTS
DECOMPILE
COMPLETE
COMPILE
~~~

The new expressivity comes from a richer workspace ontology.

---

# 19. Updated architectural picture

~~~text
                    CONSTRUCTIVE WORKSPACE
                            |
          +-----------------+-----------------+
          |                 |                 |
     Gestalt G1        Gestalt G2        Gestalt G3
          \                |                /
           \               |               /
            +------ MEDIAL CARRIERS --------+
                         |
                  CO-CONSTITUTION
                         |
                 DERIVATIONAL ROUTES
                         |
                  GESTALT FAMILY ATLAS
                  /       |        \
              chart A  chart B   chart C
                  \       |        /
                   \      |       /
                  STABILIZED CONCEPT
~~~

The workspace is therefore not underneath the ontology as dead substrate.

It is the **genetic engine-room** of the ontology.

---

# 20. Updated central maxim

~~~text
A WORKSPACE IS NOT WHERE GESTALTEN HAPPEN.

A WORKSPACE IS A STRUCTURE IN WHICH
GESTALTEN CO-CONSTITUTE ONE ANOTHER
THROUGH SHARED MATERIAL CARRIERS.

THE ATLAS MAKES THAT CO-CONSTITUTION
CONCEPTUALLY VISIBLE.
~~~

And:

~~~text
ONE MATERIAL ELEMENT
CAN BE SHARED BY MANY FIGURES,
CARRY DIFFERENT RELATIONAL ROLES,
AND BECOME THE SEED OF A HIGHER BLENDED OBJECT
WITHOUT EVER CEASING TO BE THE SAME ELEMENT.
~~~

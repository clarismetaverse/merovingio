# Merovingio Cognitive Architecture v0.4 — Multiperspectival Family Atlas

> **Phase:** cognitive / unification  
> **Status:** architectural redesign, not theorem proving  
> **Supersedes as active conceptual reference:** v0.3  
> **Preserves:** constructive workspaces, Gestalt readings, genealogy, analogy/disanalogy, rebase, partition, family organization  
> **New center of gravity:** figures as relational media, multi-perspectival family atlases, hierarchical cross-family classification

---

# 0. Core thesis

Merovingio should no longer model geometry primarily as a network of named figures and properties.

The stronger architecture is:

~~~text
CONSTRUCTIVE SUPPORT
      ↓
GESTALT
      ↓
REBASE THROUGH ONE OR MORE RELATIONAL MEDIA
      ↓
FAMILY CHARTS / STRATA / FIBERS
      ↓
CROSS-CHART STABILIZATION
      ↓
CONCEPTUAL OBJECT
~~~

A mathematical figure is therefore not only:

~~~text
an object to classify
~~~

It may also be:

~~~text
a medium through which another structure is read,
reorganized, and reclassified
~~~

The same triangle, quadrilateral, circle, polygon, or solid may function both as an object and as a relational medium.

---

# 1. Figures as relational media

The key new distinction is:

~~~text
FIGURE AS OBJECT
!=
FIGURE AS RELATIONAL MEDIUM
~~~

A triangle as object may be classified by side/angle relations.

A triangle as medium provides a ternary relational frame:

~~~text
three vertices
three sides
three angles
side-angle opposition
adjacency
orientation
closure
equality/order relations
~~~

This relational frame can be used to read structures whose primary ontology is not triangular.

Examples:

~~~text
parallel system
 -> rebase through triangle medium
 -> expose finite closure / angle-side correspondences

circle intersections
 -> rebase through triangle medium
 -> expose radius equalities / equilateral or isosceles packets

quadrilateral + diagonal
 -> rebase through paired triangle media
 -> expose correspondence structures

solid
 -> rebase through triangular/tetrahedral/sectional media
 -> expose face/edge/angle correspondence
~~~

The medium is not necessarily a decomposition into literal pieces.

It is a **relational coordinate system** that makes certain structures readable.

---

# 2. RelationalMedium

Conceptual schema:

~~~text
RelationalMedium {
    kind
    support_requirements

    role_slots
    admissible_correspondences
    internal_oppositions
    internal_adjacencies
    variation_axes

    zero_regions
    residual_regions

    source_family_signatures
    target_family_affordances
}
~~~

Examples:

~~~text
TRIANGLE_MEDIUM
QUADRILATERAL_MEDIUM
CIRCLE_MEDIUM
TRANSVERSAL_MEDIUM
GNOMONIC_MEDIUM
TETRAHEDRAL_MEDIUM
SECTION_MEDIUM
~~~

These are not new operators.

They are reusable **modes of organization**.

---

# 3. REBASE becomes representational change of basis

REBASE should now be understood more generally.

Old reading:

~~~text
change active inferential ground
~~~

v0.4 reading:

~~~text
REBASE(
    same constructive support,
    new relational medium
)
->
new family coordinates
+ new visible correspondences
+ preserved genealogy
~~~

Examples:

~~~text
double parallel cell
  REBASE through transversal medium
  -> closure coordinates

same cell
  REBASE through diagonal triangle-pair medium
  -> correspondence coordinates

same cell
  REBASE through metric/angular quadrilateral medium
  -> four-edge metric/angular coordinates
~~~

A rebase does not imply that the old reading was wrong.

It changes which relations become foreground structure.

---

# 4. Genetic class is different from static figure class

Two geometrically identical figures may have different genealogical roles.

Example:

~~~text
equilateral triangle from:
  - intersection of equal-radius circles
  - polygonal decomposition
  - parallel/translation construction
~~~

Same final metric/angular state, different genetic constitution.

Therefore track:

~~~text
STATIC_STATE
GENETIC_SIGNATURE
MEDIUM_OF_ORIGIN
ACTIVE_FAMILY_ROLE
~~~

separately.

Possible informal human labels such as:

~~~text
circle-derived triangle
parallel-derived triangle
parallelogram-derived triangle
~~~

are useful as genealogical descriptions, not necessarily as new primitive concepts.

This generalizes:

~~~text
STATE_IDENTITY != GENETIC_IDENTITY
~~~

into:

~~~text
FIGURE_IDENTITY != MEDIUM_HISTORY
~~~

---

# 5. Composite figures are multi-medium objects

A composite figure should not be represented by one privileged decomposition.

Instead:

~~~text
COMPOSITE_GESTALT {
    material_support

    admissible_media[]
    family_charts[]
    chart_states[]
    cross_chart_genealogies[]

    nested_subgestalts[]
    residual_regions[]

    stabilization_signature
}
~~~

Examples for a quadrilateral:

~~~text
triangle-pair medium
transversal-pair medium
opposite-side medium
diagonal medium
circle medium
gnomonic/residual medium
symmetry medium
~~~

Examples for a solid:

~~~text
face medium
section medium
tetrahedral medium
symmetry medium
adjacency-cycle medium
projection medium
~~~

No one reading owns the object.

---

# 6. From taxonomy trees to multiperspectival hierarchies

Classical taxonomies often look like:

~~~text
quadrilateral
  -> parallelogram
     -> rectangle
     -> rhombus
     -> square
~~~

Merovingio should instead support:

~~~text
                  SAME CONSTRUCTIVE SUPPORT
                  /       |       |       \
                 /        |       |        \
        closure chart  metric  diagonal  circular
                         chart    chart     chart
                 \        |       |        /
                  \       |       |       /
                 cross-family stabilization
~~~

A concept may therefore occupy several hierarchical positions at once.

Hierarchy is:

~~~text
MULTI-PARENT
MULTI-PERSPECTIVAL
GENEALOGICAL
CONTEXT-RELATIVE
~~~

not a single inheritance tree.

---

# 7. Family charts, strata, and fibers

Run23 suggests that family transitions are not always functions.

A state in one chart may determine only a constrained region in another.

Therefore:

~~~text
FamilyChart {
    family
    coordinates
    central_states
    residual_states
    strata
}

ChartRelation {
    source_chart
    target_chart

    mapping_kind:
      FUNCTIONAL
      PARTIAL
      RELATIONAL
      FIBERED

    genealogy
}
~~~

Example:

~~~text
closure state:
  (ZERO, RIGHT)

may correspond to

many metric/angular realizations
~~~

So:

~~~text
topological state
-> fiber of compatible metric/angular states
~~~

This is why the correct metaphor is a:

~~~text
GESTALT CONSTRAINT ATLAS
~~~

not a classical coordinate atlas with globally invertible transformations.

---

# 8. Triangles as first interlingua, not final privileged ontology

Triangles are especially important because they are minimal rich ternary media.

But v0.4 does **not** privilege triangles absolutely.

Instead:

~~~text
triangle
quadrilateral
circle
gnomon
tetrahedron
section
...
~~~

may each serve as media when they expose useful relational structure.

The triangle is simply the first case where this becomes very clear.

Its role:

~~~text
object
+
relational coordinate frame
+
analogy carrier
+
disanalogy carrier
+
rebase medium
+
generator of higher classifications
~~~

Other figures may later acquire equally important medium roles.

---

# 9. Higher-order classification by medium packets

A composite object may be classified through the organization of the relational packets extracted by its media.

Example quadrilateral with a diagonal:

~~~text
Q
  -> triangle medium 1
  -> triangle medium 2
  -> relation between the two packets
~~~

The relation may track:

~~~text
side correspondences
angle correspondences
orientation
closure genealogy
source family
residual structure
~~~

The quadrilateral's conceptual class can then emerge from the organization of these packets.

This is different from merely checking four-edge properties.

The same principle applies to:

~~~text
circular configurations
polygonal configurations
solid configurations
sectional configurations
~~~

---

# 10. Congruence criteria become central slices, not primary ontology

Run21/23 suggest:

~~~text
ASA
SAS
SSS
~~~

should not be treated primarily as isolated theorem masks.

Inside a rich diagonal correspondence family, they may appear as central source profiles:

~~~text
TT
TM
MT
MM
~~~

and more generally as zero slices of a richer residual field where each coordinate has state:

~~~text
T = {LEFT, ZERO, RIGHT}
M = {LT, EQ, GT}
~~~

Thus:

~~~text
CONGRUENCE
=
zero locus / stabilization region
inside a broader correspondence family
~~~

This pattern may generalize beyond triangle congruence.

---

# 11. Analogy now operates between family organizations

A strong analogy should preferentially produce:

~~~text
family merge
family split
new coordinate
new chart
new stratum
new fiber relation
shared medium
shared genealogy
cross-family stabilization
~~~

rather than a new analogy edge.

Strong analogy:

~~~text
two apparently different concepts
->
discover they are regions/charts/stabilizations
of a deeper family organization
~~~

---

# 12. Disanalogy becomes motion through family space

A disanalogy is not merely:

~~~text
property mismatch
~~~

It is:

~~~text
one genealogical deformation
with several chart images
~~~

Example:

~~~text
break one parallel zero
  closure chart
    -> ZERO -> RIGHT

  whole/part chart
    -> residual band between nested triangles

  diagonal correspondence chart
    -> one centered coordinate + one oriented residue

  metric/angular chart
    -> constrained free fiber
~~~

Therefore:

~~~text
ONE DISANALOGY
=
ONE GENEALOGY
+
MULTIPLE FAMILY-RELATIVE EXPRESSIONS
~~~

---

# 13. Residue becomes structural, not merely metric

A residue may be:

~~~text
metric residue
angular residue
placement residue
directional residue
topological residue
regional / gnomonic residue
genealogical residue
~~~

v0.4 emphasizes:

~~~text
RESIDUE
=
what remains structurally visible
when one Gestalt is deformed relative to another
~~~

The trapezoid-like band between nested triangles is a geometric example:

~~~text
larger triangle
minus
smaller triangle
=
residual four-edge region
~~~

This residual region may itself become a new Gestalt or medium.

---

# 14. Hierarchical organization is generated, not preloaded

Merovingio should not begin with a fixed hierarchy such as:

~~~text
point -> line -> triangle -> quadrilateral -> polygon
~~~

Hierarchies should emerge from successful rebases and stabilizations.

Examples:

~~~text
circle system
 -> triangle medium
 -> equilateral/isosceles correspondence family

double closure field
 -> parallelogram mutual zero
 -> trapezoid-like residual strata
 -> nested-triangle reading

quadrilateral
 -> diagonal pair medium
 -> correspondence field
 -> metric/topological reclassification
~~~

The system may therefore generate several overlapping hierarchies over the same support.

---

# 15. New architectural center: GestaltFamilyAtlas

Conceptual schema:

~~~text
GestaltFamilyAtlas {
    support_id

    stabilized_gestalt

    charts[]
    media[]
    strata[]
    fibers[]

    rebases[]
    cross_chart_relations[]

    shared_genealogies[]
    disanalogy_trajectories[]
    analogy_reorganizations[]

    nested_atlases[]
}
~~~

A mature concept may be represented less as:

~~~text
Concept {
  properties
}
~~~

and more as:

~~~text
Concept ~= STABILIZE(GestaltFamilyAtlas)
~~~

This is the central v0.4 proposal.

---

# 16. Hierarchical nesting of atlases

A medium extracted from one atlas can itself become the support of another.

Example:

~~~text
QUADRILATERAL ATLAS
    |
    | rebase through diagonal triangle pair
    v
TRIANGLE-CORRESPONDENCE ATLAS
    |
    | rebase one triangle through circle genealogy
    v
CIRCLE-DERIVED TRIANGLE ATLAS
~~~

Thus Merovingio needs recursive organization:

~~~text
ATLAS
  contains / references
    SUB-ATLAS
      contains / references
        SUB-ATLAS
~~~

But recursion is not a rigid containment tree.

The same sub-atlas may participate in several parents.

---

# 17. Visualization becomes architecturally central

The new ontology should be visible.

The interface should support at least four synchronized views.

## 17.1 Material view

Show the constructive support:

~~~text
points
segments
lines
circles
regions
solid faces
~~~

## 17.2 Family-atlas view

Show the active charts around the same Gestalt:

~~~text
closure
metric/angular
diagonal correspondence
circular
gnomonic
symmetry
...
~~~

## 17.3 Hierarchy view

Show:

~~~text
which Gestalten are acting as media for which others
which atlases are nested
which concepts are stabilized across several charts
~~~

This should be a DAG / multi-parent hierarchy, not a tree.

## 17.4 Genealogy/deformation view

Animate or trace:

~~~text
one BREAK / REBASE
->
all chart images changing together
~~~

This is likely the clearest visual expression of Merovingio's core idea.

---

# 18. Visual design principle: perspective switch without object duplication

When the user switches from:

~~~text
closure perspective
to
triangle perspective
to
circle perspective
~~~

the underlying material object should remain visually anchored.

Only:

~~~text
roles
highlighted relations
family coordinates
active nested Gestalten
~~~

should change.

This makes:

~~~text
MATERIAL_IDENTITY PRESERVED
ROLE / FAMILY IDENTITY CHANGES
~~~

visually obvious.

---

# 19. Agent implications

The multi-agent system remains, but priorities change.

## Reorganization Agent

Primary job:

~~~text
detect when several concepts are better represented
as charts/strata of one family atlas
~~~

## Genealogy Agent

Primary job:

~~~text
track one deformation across multiple charts
and preserve one cross-chart identity
~~~

## Expansion Agent

Primary job:

~~~text
search nearby family strata and alternative media
~~~

## Compiler Agent

Primary job:

~~~text
stabilize recurrent atlases and useful chart transitions
without collapsing them into flat property bundles
~~~

## Coherence Monitor

Primary job:

~~~text
check support identity,
family compatibility,
genealogy consistency,
and cross-chart coherence
~~~

No proof-first gate is active in this phase.

---

# 20. What should not be added

v0.4 explicitly resists creating separate operators for:

~~~text
triangle-to-quadrilateral conversion
circle-to-triangle conversion
parallelogram-to-ASA conversion
SAS-to-parallel conversion
trapezoid-to-triangle conversion
~~~

These should normally be represented as:

~~~text
REBASE
+ family chart change
+ genealogy
+ relation between media
~~~

Only repeated evidence of a genuinely content-independent transformation should pressure the operator kernel.

---

# 21. Migration from v0.3

Keep:

~~~text
ConstructiveWorkspace
Gestalt
family membership
genealogy
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

Reinterpret:

~~~text
Concept
  from single compiled Gestalt
  to stabilized multi-chart atlas

Family
  from governed set of states
  to chart/field that may overlap with other fields

Analogy
  from relation between nodes
  to pressure for atlas/family reorganization

Disanalogy
  from mismatch
  to motion with cross-chart images

Hierarchy
  from type tree
  to multi-parent atlas nesting

Figure
  from object-only
  to object-or-medium
~~~

---

# 22. High-level coherence check

The v0.4 redesign is consistent with the strongest earlier Merovingio principles:

~~~text
same construction != same Gestalt
same Gestalt != same genealogy
STATE_IDENTITY != GENETIC_IDENTITY
MATERIAL_IDENTITY != ROLE_IDENTITY
ZERO_STATUS_IS_FAMILY_RELATIVE
COGNITIVE_REINDIVIDUATION != MATERIAL_PARTITION
~~~

It also explains why recent experiments became difficult when forced into a flat operator/relation ontology.

The missing structure was not more rules.

It was a richer representation of:

~~~text
same support
many media
many charts
nested family structure
cross-chart genealogies
~~~

---

# 23. Research program opened by v0.4

Immediate experiments should test:

~~~text
1. triangle as medium across:
   parallel-derived
   circle-derived
   quadrilateral-derived
   gnomonic-derived cases

2. quadrilateral as medium for:
   triangle-pair families
   circular families
   symmetry families

3. circle as medium for:
   triangle generation
   chord/angle families
   polygonal families

4. recursive atlas nesting:
   one medium becoming support of another atlas

5. visual synchronized rebase:
   one material object, several family charts changing together
~~~

The central question is no longer:

> Which theorem follows?

It is:

> Which family ontology becomes visible when this Gestalt is rebased through another relational medium?

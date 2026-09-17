from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cognitive_graph import CognitiveGraph


def graph() -> CognitiveGraph:
    return CognitiveGraph.from_directory(ROOT / "graph")


def test_graph_references_are_coherent():
    assert graph().validate() == []


def test_all_controlled_runs_form_n0_to_n12_chain():
    g = graph()
    expected = [
        ("RUN01", "N0", "N1"),
        ("RUN02", "N1", "N2"),
        ("RUN03", "N2", "N3"),
        ("RUN04", "N3", "N4"),
        ("RUN05", "N4", "N5"),
        ("RUN06", "N5", "N6"),
        ("RUN07", "N6", "N7"),
        ("RUN08", "N7", "N8"),
        ("RUN09", "N8", "N9"),
        ("RUN10_CANONICAL_REINDIVIDUATION", "N9", "N10"),
        ("RUN11_CANONICAL_COUNTERFACTUAL_RECOVERY", "N10", "N11"),
        ("RUN12_CANONICAL_PARTITION_WORKSPACE", "N11", "N12"),
    ]
    assert [(r, g.run(r).input_snapshot, g.run(r).output_snapshot) for r, _, _ in expected] == expected
    assert all(g.run(r).raw["execution_mode"] == "CONTROLLED_DRY_RUN" for r, _, _ in expected)
    assert g.summary()["latest_snapshot"] == "N12"


def test_triangle_zero_is_swap_fixed_and_member_of_triangle_family():
    g = graph()
    zero = g.entity("G_TRIANGLE_ZERO")
    assert zero.raw["state"] == {
        "side_relation": "EQ",
        "opposite_angle_relation": "EQ",
    }
    assert "SWAP_LEFT_RIGHT" in zero.raw["symmetries"]
    assert any(
        edge.target == "F_TRIANGLE_RELATION" and edge.type == "MEMBER_OF"
        for edge in g.outgoing("G_TRIANGLE_ZERO")
    )


def test_pair_coincidence_has_multiple_genealogies():
    g = graph()
    genealogies = g.genealogies_for("G_PAIR_COINCIDENCE")
    assert len(genealogies) == 1
    path_ids = {path["id"] for path in genealogies[0].raw["paths"]}
    assert path_ids == {"GEN_PAIR_SAS", "GEN_PAIR_SSS", "GEN_PAIR_ASA"}


def test_triangle_and_supplement_families_have_different_propagation_signatures():
    g = graph()
    triangle = g.entity("F_TRIANGLE_RELATION")
    supplement = g.entity("F_DISTRIBUTED_SUPPLEMENT")
    assert triangle.raw["properties"]["propagation_signature"] == "PRESERVE_SIGN"
    assert supplement.raw["properties"]["propagation_signature"] == "REVERSE_SIGN"


def test_square_is_composite_zero_of_two_independent_loci():
    g = graph()
    composite = g.entity("Z_SQUARE_COMPOSITE")
    assert composite.raw["zero_conditions"] == [
        "Z_PARALLELOGRAM_METRIC",
        "Z_PARALLELOGRAM_ANGULAR",
    ]
    assert composite.raw["properties"]["composite_degree"] == 2


def test_run09_preserves_centrality_actuality_distinction():
    g = graph()
    candidate = g.entity("Z_ANGULAR_CENTRAL_CANDIDATE")
    assert candidate.raw["properties"]["centrality"] == "swap_fixed"
    assert candidate.raw["properties"]["actuality"] == "NOT_INFERRED_IN_RUN09"


def test_reindividuation_generalizes_old_modes_without_proof_license_leakage():
    g = graph()
    operator = g.entity("OP_REINDIVIDUATE")
    props = operator.raw["properties"]
    assert set(props["known_modes"]) == {"INTERNALIZE", "EXTERNALIZE"}
    assert props["proof_license_policy"] == "NEVER_UPGRADES_PROOF_LICENSE_BY_ITSELF"
    assert props["asserts_material_identity"] is False
    assert props["asserts_congruence"] is False

    incoming = {(edge.source, edge.type, edge.raw.get("relation", {}).get("mode")) for edge in g.incoming("OP_REINDIVIDUATE")}
    assert ("OP_INTERNALIZE", "INSTANCE_OF", "INTERNALIZE") in incoming
    assert ("OP_EXTERNALIZE", "INSTANCE_OF", "EXTERNALIZE") in incoming


def test_i18_i25_compile_into_shared_metric_to_angular_family_but_keep_realization_scope():
    g = graph()
    family = g.entity("F_METRIC_ANGULAR_ORDER")
    assert family.raw["properties"]["propagation_signature"] == "PRESERVE_SIGN"
    assert family.raw["properties"]["member_readings"] == {
        "P_I18": "OBJECT_NATIVE",
        "P_I25": "PAIR_NATIVE",
        "G_REINDIVIDUATED_ORDER_SCHEMA": "REINDIVIDUATED_SCHEMA",
    }

    members = {
        edge.source: edge.raw.get("relation", {}).get("realization_topology")
        for edge in g.incoming("F_METRIC_ANGULAR_ORDER", "MEMBER_OF")
    }
    assert members["P_I18"] == "OBJECT_NATIVE"
    assert members["P_I25"] == "PAIR_NATIVE"
    assert members["G_REINDIVIDUATED_ORDER_SCHEMA"] == "REINDIVIDUATED_SCHEMA"


def test_counterfactual_state_recovery_is_exhaustive_and_certified():
    g = graph()
    family = g.entity("F_COUNTERFACTUAL_STATE_RECOVERY")
    assert family.raw["properties"]["supports_nontrichotomic_partitions"] is True
    assert family.raw["properties"]["supports_heterogeneous_eliminators"] is True
    assert family.raw["properties"]["requires_unique_survivor"] is True
    assert g.entity("INV_EXHAUSTIVENESS_BEFORE_SYNTHESIS").raw["properties"]["statement"] == (
        "SURVIVOR SYNTHESIS REQUIRES EXHAUSTIVE PARTITION"
    )
    assert g.entity("INV_CERTIFIED_REJECTION_ONLY").raw["properties"]["statement"] == (
        "ONLY CERTIFIED IMPOSSIBILITY REJECTS A COUNTERFACTUAL BRANCH"
    )


def test_partition_workspace_is_material_and_not_reindividuation_converse():
    g = graph()
    partition = g.entity("OP_PARTITION_WORKSPACE")
    props = partition.raw["properties"]
    assert props["layer"] == "MATERIAL_PROOF_TOPOLOGY"
    assert props["may_register_subworkspaces"] is True
    assert props["asserts_unverified_incidence"] is False
    assert props["asserts_role_identity_as_material_identity"] is False
    assert props["proof_license_policy"] == (
        "PARTITION_REGISTERS_MATERIAL_STRUCTURE_BUT_DOES_NOT_BY_ITSELF_LICENSE_DOWNSTREAM_THEOREMS"
    )

    layer_split = g.entity("INV_REINDIVIDUATE_PARTITION_LAYER_SPLIT")
    assert layer_split.raw["properties"]["statement"] == (
        "COGNITIVE_REINDIVIDUATION != MATERIAL_SUBWORKSPACE_EXTRACTION"
    )


def test_partition_requires_material_owner_maps_and_preserves_theorem_barrier():
    g = graph()
    barrier = g.entity("INV_PARTITION_OWNER_MAP_BARRIER")
    assert barrier.raw["properties"]["statement"] == "OVERLAP MUST BE COMPUTED FROM MATERIAL OWNER MAPS"
    corollaries = set(barrier.raw["properties"]["corollaries"])
    assert "ROLE_ALIGNMENT != MATERIAL_IDENTITY" in corollaries
    assert "VISUAL_CLOSURE != MATERIAL_SUBWORKSPACE" in corollaries
    assert "PARTITION_SUCCESS != DOWNSTREAM_THEOREM_LICENSE" in corollaries

    outgoing = {(edge.target, edge.type) for edge in g.outgoing("OP_PARTITION_WORKSPACE")}
    assert ("INV_PARTITION_OWNER_MAP_BARRIER", "USES") in outgoing
    assert ("INV_REINDIVIDUATE_PARTITION_LAYER_SPLIT", "USES") in outgoing


def test_run12_guardrail_is_canonicalized_as_invariants():
    g = graph()
    barrier = g.entity("INV_REINDIVIDUATION_PROOF_LICENSE_BARRIER")
    blocked = g.entity("INV_BLOCKED_PROPAGATION_NOT_REJECTED")
    assert barrier.raw["properties"]["statement"] == "REINDIVIDUATION NEVER UPGRADES PROOF LICENSE BY ITSELF"
    assert blocked.raw["properties"]["statement"] == "BLOCKED_PROPAGATION != REJECTED_COUNTERFACTUAL"


def test_reachability_is_not_named_analogy_strength():
    g = graph()
    reached = g.reachable("G_TRIANGLE_ZERO", max_depth=3)
    assert "G_TRIANGLE_ZERO" in reached
    # This query intentionally returns only topological reachability. The architecture
    # keeps analogical strength as a future context-relative scoring problem.
    assert isinstance(reached["G_TRIANGLE_ZERO"], int)

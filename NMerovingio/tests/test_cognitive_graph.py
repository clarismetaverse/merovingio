from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cognitive_graph import CognitiveGraph


def graph() -> CognitiveGraph:
    return CognitiveGraph.from_directory(ROOT / "graph")


def test_graph_references_are_coherent():
    assert graph().validate() == []


def test_all_controlled_runs_form_n0_to_n9_chain():
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
    ]
    assert [(r, g.run(r).input_snapshot, g.run(r).output_snapshot) for r, _, _ in expected] == expected
    assert all(g.run(r).raw["execution_mode"] == "CONTROLLED_DRY_RUN" for r, _, _ in expected)


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


def test_reachability_is_not_named_analogy_strength():
    g = graph()
    reached = g.reachable("G_TRIANGLE_ZERO", max_depth=3)
    assert "G_TRIANGLE_ZERO" in reached
    # This query intentionally returns only topological reachability. The architecture
    # keeps analogical strength as a future context-relative scoring problem.
    assert isinstance(reached["G_TRIANGLE_ZERO"], int)

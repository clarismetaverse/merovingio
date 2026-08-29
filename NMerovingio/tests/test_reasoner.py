from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from reasoner import NMerovingio, Relation


def engine() -> NMerovingio:
    return NMerovingio.from_json(ROOT / "data" / "propositions.json")


def test_side_break_preserves_angle_as_open_question():
    cf = engine().break_side_equality(Relation.GT)
    assert cf.target.side_relation == Relation.GT
    assert cf.target.angle_relation == Relation.UNKNOWN
    assert cf.break_kind == "side"


def test_angle_break_preserves_side_as_open_question():
    cf = engine().break_angle_equality(Relation.GT)
    assert cf.target.angle_relation == Relation.GT
    assert cf.target.side_relation == Relation.UNKNOWN
    assert cf.break_kind == "angle"


def test_i6_is_role_adjacent_to_angle_break_when_target_hidden():
    r = engine()
    cf = r.break_angle_equality(Relation.GT)
    ids = {p.proposition_id for p in r.retrieve_by_role(cf, exclude={"I.19"})}
    assert "I.6" in ids


def test_i5_i6_i7_are_available_as_prior_patterns_for_side_break():
    r = engine()
    cf = r.break_side_equality(Relation.GT)
    ids = {p.proposition_id for p in r.retrieve_by_role(cf, exclude={"I.18"})}
    assert {"I.5", "I.6", "I.7"}.issubset(ids)


def test_base_eliminates_equality_mismatch():
    r = engine()
    cf = r.break_side_equality(Relation.GT)
    trace = r.run_counterfactual(cf, hide_target=True)
    text = str(trace)
    assert "rejects angle '=' with side inequality" in text
    assert "Stop before target leakage" in text

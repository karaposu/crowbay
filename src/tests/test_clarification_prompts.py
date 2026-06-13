# filepath: src/tests/test_clarification_prompts.py

"""The semantic attribute checker (services/prompts/clarification_prompts).

Keyless: the prompt, the schema, and the engine-mapping are pure Python and
testable without LangChain or an API key. The live LLM call (check_attributes)
is exercised only by the §8 manual smoke checklist with a real key.
"""

from services import clarifier_registry as registry
from services.prompts import (
    ATTRIBUTE_CODE_MAP,
    SEMANTIC_ATTRIBUTE_CHECKER,
    AttributeReport,
    to_entry_results,
)

# The 11 meta-definition attributes (kind 4 + instance 7).
_ALL_ATTRS = list(ATTRIBUTE_CODE_MAP)


def test_schema_has_exactly_the_eleven_attributes():
    bool_fields = [
        name for name, f in AttributeReport.model_fields.items()
        if f.annotation is bool
    ]
    assert sorted(bool_fields) == sorted(_ALL_ATTRS)
    assert len(bool_fields) == 11


def test_map_covers_the_kind_and_instance_entries_exactly():
    codes = set(ATTRIBUTE_CODE_MAP.values())
    expected = {e.code for e in registry.entries_in_order()
                if e.klass in ("kind", "instance")}
    assert codes == expected
    assert len(codes) == 11


def test_prompt_states_the_data_not_instructions_rule():
    # CJ-X1's hard rule must travel with the prompt (injection defense).
    assert "DATA" in SEMANTIC_ATTRIBUTE_CHECKER
    assert "definedness, not truth" in SEMANTIC_ATTRIBUTE_CHECKER
    # all 11 field names appear as questions
    for attr in _ALL_ATTRS:
        assert attr in SEMANTIC_ATTRIBUTE_CHECKER


def test_polarity_true_is_clear_false_is_fired():
    """True = attribute holds -> clear; False = flaw present -> the detection
    fires. This is the inverse the engine consumes."""
    all_good = AttributeReport(**{a: True for a in _ALL_ATTRS})
    results = {r.code: r.result for r in to_entry_results(all_good)}
    assert set(results.values()) == {"clear"}

    missing_target = AttributeReport(**{a: True for a in _ALL_ATTRS} | {"target_identified": False})
    by_code = {r.code: r.result for r in to_entry_results(missing_target)}
    assert by_code["CJ-I2"] == "fired"  # target_identified=False fires CJ-I2
    assert by_code["CJ-K1"] == "clear"


def test_uncertain_overrides_the_boolean():
    """Policy doubt must surface as uncertain (-> hold), never a False guess."""
    report = AttributeReport(
        **{a: True for a in _ALL_ATTRS},
        uncertain=["policy_permissible"],
    )
    by_code = {r.code: r.result for r in to_entry_results(report)}
    assert by_code["CJ-K3"] == "uncertain"  # routes to human hold downstream


def test_normal_form_slot_passthrough():
    nf = (
        "Like the 3 most recent photos on ⟨target⟩ until all 3 show a "
        "filled heart, within one session."
    )
    report = AttributeReport(**{a: True for a in _ALL_ATTRS}, normal_form=nf)
    assert "⟨target⟩" in report.normal_form
    # round-trips through structured-output serialization
    assert AttributeReport.model_validate(report.model_dump()).normal_form == report.normal_form

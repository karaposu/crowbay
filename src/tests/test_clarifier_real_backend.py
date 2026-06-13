# filepath: src/tests/test_clarifier_real_backend.py

"""The real backend's structured-output integration (BOM §3, the LLM path).

Keyless: we never call the live API. We verify the ConsumerReport -> LLMOutput
mapping covers all 20 detections with correct polarity, that the schema reuses
the 11-attribute checker, and that RealClarifierBackend's retry/fail contract
holds — by substituting consume_submission with a fake that returns a canned
report (exactly what a real LLM would yield).
"""

import pytest

from config import settings
from db.models import DraftStatus, TaskDraft, User
from services import clarifier
from services import clarifier_registry as registry
from services.clarifier_backend import ClarifierBackendError, RealClarifierBackend
from services.prompts import AttributeReport, ConsumerReport, to_llm_output

_ALL_ATTRS = list(AttributeReport.model_fields) + list(ConsumerReport.model_fields)


def _good_report(**overrides) -> ConsumerReport:
    """A fully-clean ConsumerReport (every axis good) with overrides."""
    bools = {
        name: True
        for name, f in ConsumerReport.model_fields.items()
        if f.annotation is bool
    }
    return ConsumerReport(**(bools | {"tos_category": "neutral"} | overrides))


def test_consumer_report_extends_the_attribute_checker():
    # ConsumerReport IS an AttributeReport (the 11 reused verbatim, not copied)
    assert issubclass(ConsumerReport, AttributeReport)
    for attr in ("digital", "atomic", "policy_permissible"):
        assert attr in ConsumerReport.model_fields


def test_mapping_covers_all_twenty_detections():
    out = to_llm_output(_good_report())
    codes = {r.code for r in out.results}
    expected = {e.code for e in registry.entries_in_order()}
    assert codes == expected
    assert len(codes) == 20
    assert all(r.result == "clear" for r in out.results)  # all-good report


def test_mapping_polarity_channel_and_composition():
    # False on a channel/composition axis -> that detection fires
    out = to_llm_output(_good_report(free_of_injection=False, consistent_with_fields=False))
    by_code = {r.code: r.result for r in out.results}
    assert by_code["CJ-X1"] == "fired"  # free_of_injection=False
    assert by_code["CJ-C1"] == "fired"  # consistent_with_fields=False
    assert by_code["CJ-X4"] == "clear"


def test_mapping_derives_c5_from_tos_category():
    # engagement row -> CJ-C5 (disclosure) fires; neutral -> clear
    eng = {r.code: r.result for r in to_llm_output(_good_report(tos_category="engagement")).results}
    assert eng["CJ-C5"] == "fired"
    neu = {r.code: r.result for r in to_llm_output(_good_report(tos_category="neutral")).results}
    assert neu["CJ-C5"] == "clear"


def test_mapping_slots_and_restatement_passthrough():
    out = to_llm_output(_good_report(
        actions=["like the 3 most recent photos"],
        end_state="all 3 show a filled heart",
        normal_form="Like the 3 most recent photos on ⟨target⟩ until all 3 show a filled heart.",
    ))
    assert out.slots.actions == ["like the 3 most recent photos"]
    assert out.slots.end_state == "all 3 show a filled heart"
    assert out.restatement and "filled heart" in out.restatement


def test_real_backend_retries_once_then_raises(monkeypatch):
    calls = {"n": 0}

    def _boom(desc, ctx=None, **kw):
        calls["n"] += 1
        raise RuntimeError("api down")

    monkeypatch.setattr(
        "services.prompts.consumer_prompts.consume_submission", _boom
    )
    with pytest.raises(ClarifierBackendError):
        RealClarifierBackend().run("like my photos")
    assert calls["n"] == 2  # one try + one retry (BOM §3)


def test_real_backend_feeds_the_engine_end_to_end(db_session, monkeypatch):
    """A fake 'real' LLM (canned ConsumerReport) drives a full run through the
    engine to the right archetype — proving the structured path plugs in."""
    monkeypatch.setattr(settings, "CLARIFIER_BACKEND", "real")

    # canned report: a well-formed engagement task that's missing its target
    report = _good_report(target_identified=False, tos_category="engagement",
                          actions=["like the 3 most recent photos"])

    def _fake_consume(desc, ctx=None, **kw):
        return to_llm_output(report)

    monkeypatch.setattr(
        "services.prompts.consumer_prompts.consume_submission", _fake_consume
    )

    u = User(email="real-be@example.com", password_hash="x")
    db_session.add(u)
    db_session.flush()
    draft = TaskDraft(owner_id=u.id, payload={"desc": "like my photos to give me a boost"})
    db_session.add(draft)
    db_session.flush()

    run = clarifier.run_clarifier(db_session, draft)
    assert run.backend == "real" and run.status == "complete"
    by_code = {r.code: r.result for r in run.detections}
    assert by_code["CJ-I2"] == "fired"  # missing target
    assert by_code["CJ-C5"] == "fired"  # engagement disclosure
    assert clarifier.run_result(run).archetype == "clarify"
    assert draft.status == DraftStatus.AWAITING_APPROVAL.value

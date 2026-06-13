# filepath: src/tests/test_phone_verification.py

import re
from datetime import timedelta

import pytest

from db.base import utcnow
from db.models import SmsVerification
from services.sms import MockTwilioBackend


@pytest.fixture(autouse=True)
def _clean_outbox():
    MockTwilioBackend.reset()
    yield
    MockTwilioBackend.reset()


def _last_code() -> str:
    assert MockTwilioBackend.outbox, "no SMS was sent"
    match = re.search(r"\b(\d{6})\b", MockTwilioBackend.outbox[-1].body)
    assert match, f"no code in SMS body: {MockTwilioBackend.outbox[-1].body!r}"
    return match.group(1)


def test_full_phone_verification_flow(client, register):
    headers, _ = register("phones@example.com")

    r = client.post(
        "/auth/phone/request", headers=headers, json={"phone_number": "+49 170 123-4567"}
    )
    assert r.status_code == 200, r.text

    sent = MockTwilioBackend.outbox[-1]
    assert sent.to == "+491701234567"  # normalized before sending
    assert sent.sid.startswith("SM")

    r = client.post("/auth/phone/verify", headers=headers, json={"code": _last_code()})
    assert r.status_code == 200

    me = client.get("/users/me", headers=headers).json()
    assert me["phone_number"] == "+491701234567"
    assert me["is_phone_verified"] is True


def test_invalid_phone_format_rejected(client, register):
    headers, _ = register("badphone@example.com")
    for bad in ("12345", "+12", "0170 1234567", "not-a-phone"):
        r = client.post("/auth/phone/request", headers=headers, json={"phone_number": bad})
        assert r.status_code == 400, f"{bad!r} should be rejected"
    # 00-prefix is accepted as international form
    r = client.post(
        "/auth/phone/request", headers=headers, json={"phone_number": "0049 170 1234567"}
    )
    assert r.status_code == 200
    assert MockTwilioBackend.outbox[-1].to == "+491701234567"


def test_wrong_code_attempts_are_capped_and_persist(client, register):
    headers, _ = register("attempts@example.com")
    client.post("/auth/phone/request", headers=headers, json={"phone_number": "+491701111111"})
    real_code = _last_code()
    wrong = "000000" if real_code != "000000" else "111111"

    for _ in range(5):  # SMS_MAX_ATTEMPTS
        r = client.post("/auth/phone/verify", headers=headers, json={"code": wrong})
        assert r.status_code == 400
        assert r.json()["detail"] == "Invalid code"

    # cap reached: even the CORRECT code is now refused
    r = client.post("/auth/phone/verify", headers=headers, json={"code": real_code})
    assert r.status_code == 400
    assert "Too many attempts" in r.json()["detail"]


def test_expired_code_rejected(client, register, db_session):
    headers, _ = register("expired@example.com")
    client.post("/auth/phone/request", headers=headers, json={"phone_number": "+491702222222"})
    code = _last_code()

    challenge = db_session.query(SmsVerification).one()
    challenge.expires_at = utcnow() - timedelta(minutes=1)
    db_session.commit()

    r = client.post("/auth/phone/verify", headers=headers, json={"code": code})
    assert r.status_code == 400
    assert "expired" in r.json()["detail"]


def test_resend_cooldown(client, register):
    headers, _ = register("cooldown@example.com")
    body = {"phone_number": "+491703333333"}
    assert client.post("/auth/phone/request", headers=headers, json=body).status_code == 200
    r = client.post("/auth/phone/request", headers=headers, json=body)
    assert r.status_code == 429


def test_new_request_invalidates_old_code(client, register, monkeypatch):
    from config import settings

    monkeypatch.setattr(settings, "SMS_RESEND_COOLDOWN_SECONDS", 0)
    headers, _ = register("invalidate@example.com")
    body = {"phone_number": "+491704444444"}

    client.post("/auth/phone/request", headers=headers, json=body)
    old_code = _last_code()
    client.post("/auth/phone/request", headers=headers, json=body)
    new_code = _last_code()

    if old_code == new_code:  # 1-in-a-million; nothing to assert then
        return
    r = client.post("/auth/phone/verify", headers=headers, json={"code": old_code})
    assert r.status_code == 400
    r = client.post("/auth/phone/verify", headers=headers, json={"code": new_code})
    assert r.status_code == 200


def test_phone_uniqueness_across_accounts(client, register):
    h1, _ = register("first-owner@example.com")
    client.post("/auth/phone/request", headers=h1, json={"phone_number": "+491705555555"})
    client.post("/auth/phone/verify", headers=h1, json={"code": _last_code()})

    h2, _ = register("second-owner@example.com")
    r = client.post("/auth/phone/request", headers=h2, json={"phone_number": "+491705555555"})
    assert r.status_code == 409


def test_verify_without_request(client, register):
    headers, _ = register("norequest@example.com")
    r = client.post("/auth/phone/verify", headers=headers, json={"code": "123456"})
    assert r.status_code == 400
    assert "request one first" in r.json()["detail"]


def test_phone_endpoints_require_auth(client):
    assert (
        client.post("/auth/phone/request", json={"phone_number": "+491700000000"}).status_code
        == 401
    )
    assert client.post("/auth/phone/verify", json={"code": "123456"}).status_code == 401


def test_phone_audit_events(client, register, db_session):
    headers, _ = register("audit-phone@example.com")
    client.post("/auth/phone/request", headers=headers, json={"phone_number": "+491706666666"})
    client.post("/auth/phone/verify", headers=headers, json={"code": _last_code()})

    from db.models import AuditEvent

    types = [e.event_type for e in db_session.query(AuditEvent).all()]
    assert "auth.phone_code_requested" in types
    assert "auth.phone_verified" in types


def test_resend_verification_email(client, register):
    headers, _ = register("resend@example.com")
    r = client.post("/auth/resend-verification", headers=headers)
    assert r.status_code == 200
    assert r.json()["msg"] == "Verification email sent"

    # after verifying, resend reports already-verified
    from services.auth import create_email_verify_token

    uid = client.get("/users/me", headers=headers).json()["id"]
    client.get("/auth/verify-email", params={"token": create_email_verify_token(uid)})
    r = client.post("/auth/resend-verification", headers=headers)
    assert r.json()["msg"] == "Email already verified"


def test_resend_verification_for_telegram_only_account(client):
    r = client.post(
        "/auth/telegram",
        json={"telegram_id": 555_001, "telegram_handle": "noemail"},
        headers={"X-Bridge-Secret": "test-bridge-secret"},
    )
    headers = {"Authorization": f"Bearer {r.json()['access_token']}"}
    r = client.post("/auth/resend-verification", headers=headers)
    assert r.status_code == 400
    assert "no email" in r.json()["detail"]

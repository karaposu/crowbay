# filepath: src/tests/test_auth.py

from datetime import timedelta

from services.auth import (
    TokenPurpose,
    _mint,
    create_email_verify_token,
    create_pw_reset_token,
)


def test_register_login_me_roundtrip(client, register):
    headers, pair = register("alice@example.com")
    assert pair["token_type"] == "bearer"

    r = client.get("/users/me", headers=headers)
    assert r.status_code == 200
    body = r.json()
    assert body["email"] == "alice@example.com"
    assert body["is_email_verified"] is False
    assert body["verifications"] == []


def test_duplicate_register_rejected_case_insensitively(client, register):
    register("Bob.Builder@Example.COM")
    r = client.post(
        "/auth/register",
        json={"email": "bob.builder@example.com", "password": "password1234"},
    )
    assert r.status_code == 400
    assert "already registered" in r.json()["detail"]


def test_login_wrong_password_and_unknown_user_same_error(client, register):
    register("carol@example.com")
    r1 = client.post(
        "/auth/login", json={"email": "carol@example.com", "password": "wrong-password"}
    )
    r2 = client.post(
        "/auth/login", json={"email": "ghost@example.com", "password": "wrong-password"}
    )
    assert r1.status_code == r2.status_code == 401
    assert r1.json()["detail"] == r2.json()["detail"]


def test_refresh_rotation(client, register):
    _, pair = register("dave@example.com")
    r = client.post("/auth/refresh", json={"refresh_token": pair["refresh_token"]})
    assert r.status_code == 200
    new_pair = r.json()
    r = client.get("/users/me", headers={"Authorization": f"Bearer {new_pair['access_token']}"})
    assert r.status_code == 200


def test_wrong_purpose_tokens_rejected_as_access(client, register):
    _, pair = register("erin@example.com")
    # refresh token used as access token
    r = client.get("/users/me", headers={"Authorization": f"Bearer {pair['refresh_token']}"})
    assert r.status_code == 401
    # email-verify token used as access token
    everify = create_email_verify_token(1)
    r = client.get("/users/me", headers={"Authorization": f"Bearer {everify}"})
    assert r.status_code == 401


def test_access_token_not_accepted_as_refresh(client, register):
    _, pair = register("frank@example.com")
    r = client.post("/auth/refresh", json={"refresh_token": pair["access_token"]})
    assert r.status_code == 401


def test_expired_token_rejected(client, register):
    register("grace@example.com")
    expired = _mint("1", TokenPurpose.ACCESS, timedelta(seconds=-5))
    r = client.get("/users/me", headers={"Authorization": f"Bearer {expired}"})
    assert r.status_code == 401
    assert r.json()["detail"] == "Token expired"


def test_email_verify_flow_is_idempotent(client, register):
    headers, _ = register("henry@example.com")
    token = create_email_verify_token(client.get("/users/me", headers=headers).json()["id"])
    assert client.get("/auth/verify-email", params={"token": token}).status_code == 200
    assert client.get("/auth/verify-email", params={"token": token}).status_code == 200
    assert client.get("/users/me", headers=headers).json()["is_email_verified"] is True


def test_password_reset_full_flow(client, register):
    headers, _ = register("iris@example.com", password="original-pass1")
    uid = client.get("/users/me", headers=headers).json()["id"]

    # no account enumeration: identical answers for existing and ghost accounts
    r1 = client.post("/auth/request-password-reset", json={"email": "iris@example.com"})
    r2 = client.post("/auth/request-password-reset", json={"email": "ghost@example.com"})
    assert r1.status_code == r2.status_code == 200
    assert r1.json() == r2.json()

    token = create_pw_reset_token(uid)
    r = client.post(
        "/auth/reset-password", json={"token": token, "new_password": "brand-new-pass1"}
    )
    assert r.status_code == 200

    assert (
        client.post(
            "/auth/login", json={"email": "iris@example.com", "password": "original-pass1"}
        ).status_code
        == 401
    )
    assert (
        client.post(
            "/auth/login", json={"email": "iris@example.com", "password": "brand-new-pass1"}
        ).status_code
        == 200
    )

    # a reset token must never authenticate requests
    r = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 401


def test_short_password_rejected(client):
    r = client.post("/auth/register", json={"email": "short@example.com", "password": "short"})
    assert r.status_code == 422


def test_audit_events_written(client, register, db_session):
    register("judy@example.com")
    client.post("/auth/login", json={"email": "judy@example.com", "password": "password1234"})
    from db.models import AuditEvent

    types = [e.event_type for e in db_session.query(AuditEvent).all()]
    assert "auth.register" in types
    assert "auth.login" in types

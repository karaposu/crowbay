# filepath: src/tests/test_telegram_bridge.py

BRIDGE_HEADERS = {"X-Bridge-Secret": "test-bridge-secret"}


def _bridge(client, telegram_id=777_000_001, handle="crowfan", headers=BRIDGE_HEADERS):
    return client.post(
        "/auth/telegram",
        json={"telegram_id": telegram_id, "telegram_handle": handle},
        headers=headers,
    )


def test_bridge_requires_secret(client):
    r = client.post("/auth/telegram", json={"telegram_id": 1, "telegram_handle": "x"})
    assert r.status_code == 422  # missing header

    r = _bridge(client, headers={"X-Bridge-Secret": "wrong-secret"})
    assert r.status_code == 401


def test_bridge_disabled_when_unconfigured(client, monkeypatch):
    from config import settings

    monkeypatch.setattr(settings, "BOT_BRIDGE_SECRET", None)
    r = _bridge(client)
    assert r.status_code == 503


def test_bridge_creates_account_and_token_works(client, db_session):
    r = _bridge(client)
    assert r.status_code == 200
    access = r.json()["access_token"]

    me = client.get("/users/me", headers={"Authorization": f"Bearer {access}"})
    assert me.status_code == 200
    body = me.json()
    assert body["telegram_handle"] == "crowfan"
    assert body["email"] is None

    from db.models import AuditEvent

    events = [
        e for e in db_session.query(AuditEvent).all() if e.event_type == "auth.telegram_bridge"
    ]
    assert len(events) == 1
    assert events[0].payload == {"created": True}


def test_bridge_is_idempotent_and_tracks_handle_drift(client, db_session):
    _bridge(client, handle="old_handle")
    r = _bridge(client, handle="new_handle")
    assert r.status_code == 200

    from db.models import User

    users = db_session.query(User).filter(User.telegram_id == "777000001").all()
    assert len(users) == 1
    assert users[0].telegram_handle == "new_handle"


def test_telegram_account_can_use_task_endpoints(client):
    access = _bridge(client).json()["access_token"]
    headers = {"Authorization": f"Bearer {access}"}
    r = client.post(
        "/tasks",
        headers=headers,
        json={"desc": "bridged launch", "total_budget": 5, "you_earn": 5, "num_jumpers": 1},
    )
    assert r.status_code == 201


def test_password_login_rejected_for_telegram_only_account(client, db_session):
    """A bridged account that later gets an email but has no password must not
    be password-loggable — and the error must stay generic (no enumeration)."""
    _bridge(client)
    from db.models import User

    user = db_session.query(User).filter(User.telegram_id == "777000001").one()
    user.email = "bridged@example.com"
    db_session.commit()

    r = client.post("/auth/login", json={"email": "bridged@example.com", "password": "whatever123"})
    assert r.status_code == 401
    assert r.json()["detail"] == "Invalid email or password"

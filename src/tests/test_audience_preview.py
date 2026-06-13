# filepath: src/tests/test_audience_preview.py

"""Audience preview endpoint (matching C4) + advisory warnings (C6)."""

from db.models import User
from services.attributes import FIELD_GENDER, grant_verified_attributes

FEMALE_ONLY = {"basic_filters": {"gender": "female"}}


def _grant_many(db, n: int, **attrs):
    for i in range(n):
        user = User(email=f"crowd{i}@example.com")
        db.add(user)
        db.flush()
        grant_verified_attributes(db, user, attrs)
    db.commit()


def test_preview_below_privacy_floor(client, register):
    headers, _ = register("launcher@example.com")
    r = client.post("/tasks/audience-preview", headers=headers, json={"filters": FEMALE_ONLY})
    assert r.status_code == 200
    body = r.json()
    assert body["eligible_count"] is None
    assert body["display"] == "fewer than 10"


def test_preview_exact_above_floor(client, register, db_session):
    headers, _ = register("launcher@example.com")
    _grant_many(db_session, 12, **{FIELD_GENDER: "female"})

    r = client.post("/tasks/audience-preview", headers=headers, json={"filters": FEMALE_ONLY})
    body = r.json()
    assert body["eligible_count"] == 12
    assert body["display"] == "12"


def test_preview_excludes_the_launcher_themselves(client, register, db_session):
    headers, _ = register("launcher@example.com")
    _grant_many(db_session, 10, **{FIELD_GENDER: "female"})
    # launcher matches their own filter too — must not count themselves
    launcher = db_session.query(User).filter(User.email == "launcher@example.com").one()
    grant_verified_attributes(db_session, launcher, {FIELD_GENDER: "female"})
    db_session.commit()

    body = client.post(
        "/tasks/audience-preview", headers=headers, json={"filters": FEMALE_ONLY}
    ).json()
    assert body["eligible_count"] == 10


def test_preview_surfaces_raw_location_warning(client, register):
    headers, _ = register("launcher@example.com")
    filters = {"basic_filters": {"location_filter": {"raw_statement": "EMEA but not Russia"}}}
    body = client.post("/tasks/audience-preview", headers=headers, json={"filters": filters}).json()
    assert any("free text" in w for w in body["warnings"])


def test_preview_requires_auth(client):
    assert client.post("/tasks/audience-preview", json={"filters": None}).status_code == 401

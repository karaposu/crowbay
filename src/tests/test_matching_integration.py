# filepath: src/tests/test_matching_integration.py

"""Jump gate (C2) + filtered feed (C3) through the API."""

from db.models import User
from services.attributes import FIELD_GENDER, grant_verified_attributes

FEMALE_ONLY = {"basic_filters": {"gender": "female"}}


def _grant(db, email: str, **attrs):
    user = db.query(User).filter(User.email == email).one()
    grant_verified_attributes(db, user, attrs)
    db.commit()


def _launch(client, headers, filters=None, desc="task"):
    body = {"desc": desc, "total_budget": 10, "you_earn": 5, "num_jumpers": 2}
    if filters is not None:
        body["filters"] = filters
    r = client.post("/tasks", headers=headers, json=body)
    assert r.status_code == 201, r.text
    return r.json()["id"]


def test_jump_gate_blocks_then_allows_after_grant(client, register, db_session):
    launcher, _ = register("launcher@example.com")
    jumper, _ = register("jumper@example.com")
    tid = _launch(client, launcher, filters=FEMALE_ONLY)

    r = client.post(f"/tasks/{tid}/jump", headers=jumper)
    assert r.status_code == 403
    assert "gender" in r.json()["detail"]

    _grant(db_session, "jumper@example.com", **{FIELD_GENDER: "female"})
    r = client.post(f"/tasks/{tid}/jump", headers=jumper)
    assert r.status_code == 201, r.text


def test_jump_gate_ignores_unfiltered_tasks(client, register):
    launcher, _ = register("launcher@example.com")
    jumper, _ = register("jumper@example.com")
    tid = _launch(client, launcher)  # no filters
    assert client.post(f"/tasks/{tid}/jump", headers=jumper).status_code == 201


def test_feed_hides_ineligible_tasks(client, register, db_session):
    launcher, _ = register("launcher@example.com")
    jumper, _ = register("jumper@example.com")
    _launch(client, launcher, desc="open to all")
    _launch(client, launcher, filters=FEMALE_ONLY, desc="women only")

    body = client.get("/tasks", headers=jumper).json()
    assert body["total"] == 1
    assert body["items"][0]["desc"] == "open to all"

    _grant(db_session, "jumper@example.com", **{FIELD_GENDER: "female"})
    body = client.get("/tasks", headers=jumper).json()
    assert body["total"] == 2


def test_feed_pagination_counts_only_eligible(client, register):
    launcher, _ = register("launcher@example.com")
    jumper, _ = register("jumper@example.com")
    for i in range(3):
        _launch(client, launcher, desc=f"open {i}")
    _launch(client, launcher, filters=FEMALE_ONLY, desc="hidden")

    r = client.get("/tasks", headers=jumper, params={"page": 1, "size": 2}).json()
    assert r["total"] == 3
    assert len(r["items"]) == 2
    r = client.get("/tasks", headers=jumper, params={"page": 2, "size": 2}).json()
    assert len(r["items"]) == 1

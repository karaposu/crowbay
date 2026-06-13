# filepath: src/tests/test_tasks.py

FILTERS = {
    "basic_filters": {
        "location_filter": {
            "raw_statement": "EMEA but not Russia, plus Istanbul",
            "regions": [{"name": "EMEA", "exceptions": {"countries": ["Russia"]}}],
            "cities": [{"name": "Istanbul"}],
        },
        "age_range": {"min": 18, "max": 25},
        "gender": "female",
    },
    "advanced_filters": {"min_instagram_followers": 1000},
}


def _launch(client, headers, **overrides):
    body = {
        "desc": "Review our app",
        "total_budget": 30,
        "you_earn": 10,
        "num_jumpers": 2,
        "category": "reviews",
    }
    body.update(overrides)
    r = client.post("/tasks", headers=headers, json=body)
    assert r.status_code == 201, r.text
    return r.json()


def test_launch_requires_auth(client):
    r = client.post("/tasks", json={"desc": "x", "total_budget": 1})
    assert r.status_code == 401


def test_filters_roundtrip_verbatim(client, register):
    headers, _ = register("launcher@example.com")
    task = _launch(client, headers, filters=FILTERS)

    # nothing dropped, nothing synthesized — byte-identical structure
    assert task["filters"] == FILTERS

    r = client.get(f"/tasks/{task['id']}", headers=headers)
    assert r.json()["filters"] == FILTERS


def test_budget_must_cover_payouts(client, register):
    headers, _ = register("launcher@example.com")
    r = client.post(
        "/tasks",
        headers=headers,
        json={"desc": "x", "total_budget": 5, "you_earn": 10, "num_jumpers": 2},
    )
    assert r.status_code == 422


def test_browse_pagination(client, register):
    headers, _ = register("launcher@example.com")
    for i in range(3):
        _launch(client, headers, desc=f"task {i}")

    r = client.get("/tasks", headers=headers, params={"page": 1, "size": 2})
    body = r.json()
    assert body["total"] == 3
    assert len(body["items"]) == 2
    r = client.get("/tasks", headers=headers, params={"page": 2, "size": 2})
    assert len(r.json()["items"]) == 1


def test_jump_lifecycle(client, register):
    launcher, _ = register("launcher@example.com")
    j1, _ = register("jumper1@example.com")
    j2, _ = register("jumper2@example.com")
    j3, _ = register("jumper3@example.com")

    task = _launch(client, launcher)  # num_jumpers=2
    tid = task["id"]

    # guards
    assert client.post(f"/tasks/{tid}/jump", headers=launcher).status_code == 400  # own task
    assert client.post("/tasks/99999/jump", headers=j1).status_code == 404

    # fill it
    assert client.post(f"/tasks/{tid}/jump", headers=j1).status_code == 201
    assert client.post(f"/tasks/{tid}/jump", headers=j1).status_code == 409  # duplicate
    assert client.post(f"/tasks/{tid}/jump", headers=j2).status_code == 201
    assert client.get(f"/tasks/{tid}", headers=j1).json()["status"] == "full"
    assert client.post(f"/tasks/{tid}/jump", headers=j3).status_code == 409  # full

    # forfeit frees the slot and reopens the task
    assert client.post(f"/tasks/{tid}/forfeit", headers=j2).status_code == 200
    assert client.get(f"/tasks/{tid}", headers=j1).json()["status"] == "open"
    assert client.post(f"/tasks/{tid}/forfeit", headers=j2).status_code == 409  # twice
    assert client.post(f"/tasks/{tid}/jump", headers=j3).status_code == 201

    # listings
    mine = client.get("/tasks/my", headers=launcher).json()
    assert [t["id"] for t in mine] == [tid]
    participated = client.get("/tasks/participated", headers=j2).json()
    assert len(participated) == 1
    assert participated[0]["jump"]["status"] == "forfeited"
    assert participated[0]["task"]["id"] == tid


def test_manual_approval_path(client, register):
    launcher, _ = register("launcher@example.com")
    j1, _ = register("jumper1@example.com")
    j2, _ = register("jumper2@example.com")

    task = _launch(
        client,
        launcher,
        num_jumpers=1,
        you_earn=5,
        total_budget=10,
        accept_jumpers_manually=True,
    )
    tid = task["id"]

    # pending jumps don't consume capacity — several can apply
    r1 = client.post(f"/tasks/{tid}/jump", headers=j1)
    r2 = client.post(f"/tasks/{tid}/jump", headers=j2)
    assert r1.json()["status"] == "pending"
    assert r2.json()["status"] == "pending"
    assert client.get(f"/tasks/{tid}", headers=j1).json()["status"] == "open"

    jump1_id, jump2_id = r1.json()["id"], r2.json()["id"]

    # only the Launcher approves
    assert client.post(f"/tasks/{tid}/jumps/{jump1_id}/approve", headers=j2).status_code == 403
    r = client.post(f"/tasks/{tid}/jumps/{jump1_id}/approve", headers=launcher)
    assert r.status_code == 200
    assert r.json()["status"] == "active"
    assert client.get(f"/tasks/{tid}", headers=j1).json()["status"] == "full"

    # capacity reached — second pending jump can't be approved
    assert (
        client.post(f"/tasks/{tid}/jumps/{jump2_id}/approve", headers=launcher).status_code == 409
    )


def test_task_audit_events(client, register, db_session):
    launcher, _ = register("launcher@example.com")
    j1, _ = register("jumper1@example.com")
    task = _launch(client, launcher)
    client.post(f"/tasks/{task['id']}/jump", headers=j1)
    client.post(f"/tasks/{task['id']}/forfeit", headers=j1)

    from db.models import AuditEvent

    types = [e.event_type for e in db_session.query(AuditEvent).all()]
    for expected in ("task.launched", "task.jumped", "task.forfeited"):
        assert expected in types

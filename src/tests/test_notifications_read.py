# filepath: src/tests/test_notifications_read.py

"""GET /users/me/notifications — the polling endpoint for the dev web client."""


def _launch_manual(client, headers):
    r = client.post(
        "/tasks",
        headers=headers,
        json={
            "desc": "curated",
            "total_budget": 10,
            "you_earn": 5,
            "num_jumpers": 1,
            "accept_jumpers_manually": True,
        },
    )
    return r.json()["id"]


def test_requires_auth(client):
    assert client.get("/users/me/notifications").status_code == 401


def test_empty_for_new_user(client, register):
    headers, _ = register("quiet@example.com")
    assert client.get("/users/me/notifications", headers=headers).json() == []


def test_lifecycle_events_visible_with_text(client, register):
    launcher, _ = register("launcher@example.com")
    jumper, _ = register("jumper@example.com")

    tid = _launch_manual(client, launcher)
    jump = client.post(f"/tasks/{tid}/jump", headers=jumper).json()
    client.post(f"/tasks/{tid}/jumps/{jump['id']}/approve", headers=launcher)

    launcher_rows = client.get("/users/me/notifications", headers=launcher).json()
    launcher_types = [r["event_type"] for r in launcher_rows]
    assert "jump.pending" in launcher_types
    assert "task.full" in launcher_types

    jumper_rows = client.get("/users/me/notifications", headers=jumper).json()
    assert jumper_rows[0]["event_type"] == "jump.approved"
    assert f"#{tid}" in jumper_rows[0]["text"]  # rendered text is stored now
    assert jumper_rows[0]["payload"]["task_id"] == tid


def test_users_see_only_their_own(client, register):
    launcher, _ = register("launcher@example.com")
    jumper, _ = register("jumper@example.com")
    bystander, _ = register("bystander@example.com")

    tid = _launch_manual(client, launcher)
    client.post(f"/tasks/{tid}/jump", headers=jumper)

    # the unfiltered launch fan-out DOES reach the bystander (task.matched) —
    # isolation means they never see events addressed to others
    bystander_rows = client.get("/users/me/notifications", headers=bystander).json()
    assert bystander_rows and all(r["event_type"] == "task.matched" for r in bystander_rows)
    launcher_rows = client.get("/users/me/notifications", headers=launcher).json()
    assert all(r["event_type"] == "jump.pending" for r in launcher_rows)


def test_since_id_polling(client, register):
    launcher, _ = register("launcher@example.com")
    jumper, _ = register("jumper@example.com")

    tid = _launch_manual(client, launcher)
    jump = client.post(f"/tasks/{tid}/jump", headers=jumper).json()

    rows = client.get("/users/me/notifications", headers=launcher).json()
    assert rows, "launcher should have jump.pending"
    last_seen = max(r["id"] for r in rows)

    # nothing new since last_seen
    fresh = client.get(
        "/users/me/notifications", headers=launcher, params={"since_id": last_seen}
    ).json()
    assert fresh == []

    # approving fills the task -> launcher gets task.full, visible via since_id
    client.post(f"/tasks/{tid}/jumps/{jump['id']}/approve", headers=launcher)
    fresh = client.get(
        "/users/me/notifications", headers=launcher, params={"since_id": last_seen}
    ).json()
    assert [r["event_type"] for r in fresh] == ["task.full"]

# filepath: src/tests/test_jump_management.py


def _launch_manual(client, headers, num_jumpers=2):
    r = client.post(
        "/tasks",
        headers=headers,
        json={
            "desc": "curated task",
            "total_budget": 20,
            "you_earn": 5,
            "num_jumpers": num_jumpers,
            "accept_jumpers_manually": True,
        },
    )
    assert r.status_code == 201, r.text
    return r.json()["id"]


def test_list_jumps_owner_only_with_status_filter(client, register):
    launcher, _ = register("launcher@example.com")
    j1, _ = register("jumper1@example.com")
    j2, _ = register("jumper2@example.com")

    tid = _launch_manual(client, launcher)
    jump1 = client.post(f"/tasks/{tid}/jump", headers=j1).json()
    client.post(f"/tasks/{tid}/jump", headers=j2)
    client.post(f"/tasks/{tid}/jumps/{jump1['id']}/approve", headers=launcher)

    # non-owner forbidden
    assert client.get(f"/tasks/{tid}/jumps", headers=j1).status_code == 403

    # owner sees all
    all_jumps = client.get(f"/tasks/{tid}/jumps", headers=launcher).json()
    assert len(all_jumps) == 2

    # status filter
    pending = client.get(
        f"/tasks/{tid}/jumps", headers=launcher, params={"status": "pending"}
    ).json()
    assert len(pending) == 1
    assert pending[0]["jumper_id"] == all_jumps[1]["jumper_id"]


def test_reject_pending_jump(client, register, db_session):
    launcher, _ = register("launcher@example.com")
    j1, _ = register("jumper1@example.com")

    tid = _launch_manual(client, launcher, num_jumpers=1)
    jump = client.post(f"/tasks/{tid}/jump", headers=j1).json()

    # non-owner cannot reject
    assert client.post(f"/tasks/{tid}/jumps/{jump['id']}/reject", headers=j1).status_code == 403

    r = client.post(f"/tasks/{tid}/jumps/{jump['id']}/reject", headers=launcher)
    assert r.status_code == 200
    assert r.json()["status"] == "rejected"
    assert r.json()["resolved_at"] is not None

    # task stays open — a rejected pending jump never consumed a slot
    assert client.get(f"/tasks/{tid}", headers=launcher).json()["status"] == "open"

    # cannot reject twice
    assert (
        client.post(f"/tasks/{tid}/jumps/{jump['id']}/reject", headers=launcher).status_code == 409
    )

    from db.models import AuditEvent

    types = [e.event_type for e in db_session.query(AuditEvent).all()]
    assert "task.jump_rejected" in types


def test_reject_active_jump_refused(client, register):
    launcher, _ = register("launcher@example.com")
    j1, _ = register("jumper1@example.com")

    # auto-approve task: jump goes straight to active
    r = client.post(
        "/tasks",
        headers=launcher,
        json={"desc": "open task", "total_budget": 5, "you_earn": 5, "num_jumpers": 1},
    )
    tid = r.json()["id"]
    jump = client.post(f"/tasks/{tid}/jump", headers=j1).json()
    assert jump["status"] == "active"

    r = client.post(f"/tasks/{tid}/jumps/{jump['id']}/reject", headers=launcher)
    assert r.status_code == 409

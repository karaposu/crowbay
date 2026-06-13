# filepath: src/tests/test_notifications.py

"""Fan-out (C7), notifier backends (C8), ledger + mute (C9)."""

import pytest

from db.models import Notification, Task, User
from services.attributes import FIELD_GENDER, grant_verified_attributes
from services.notifications import fan_out_task_matched
from services.notifier import ConsoleNotifierBackend

FEMALE_ONLY = {"basic_filters": {"gender": "female"}}


@pytest.fixture(autouse=True)
def _clean_outbox():
    ConsoleNotifierBackend.reset()
    yield
    ConsoleNotifierBackend.reset()


def _grant_many(db, n: int, **attrs) -> list[User]:
    users = []
    for i in range(n):
        user = User(email=f"crowd{i}@example.com")
        db.add(user)
        db.flush()
        grant_verified_attributes(db, user, attrs)
        users.append(user)
    db.commit()
    return users


def _launch(client, headers, filters=None, **overrides):
    body = {"desc": "notify me", "total_budget": 10, "you_earn": 5, "num_jumpers": 1}
    if filters is not None:
        body["filters"] = filters
    body.update(overrides)
    r = client.post("/tasks", headers=headers, json=body)
    assert r.status_code == 201, r.text
    return r.json()["id"]


def test_fanout_notifies_matching_jumpers_not_launcher(client, register, db_session):
    _grant_many(db_session, 3, **{FIELD_GENDER: "female"})
    launcher_headers, _ = register("launcher@example.com")
    tid = _launch(client, launcher_headers, filters=FEMALE_ONLY)

    rows = db_session.query(Notification).filter_by(event_type="task.matched").all()
    assert len(rows) == 3
    assert all(r.status == "sent" and r.provider_ref for r in rows)
    assert all(r.dedupe_key == f"task.matched:{tid}:{r.user_id}" for r in rows)

    launcher = db_session.query(User).filter_by(email="launcher@example.com").one()
    assert launcher.id not in {r.user_id for r in rows}
    assert len(ConsoleNotifierBackend.outbox) == 3
    assert "earn 5" in ConsoleNotifierBackend.outbox[0].text


def test_fanout_cap(client, register, db_session, monkeypatch):
    from config import settings

    monkeypatch.setattr(settings, "MATCH_NOTIFY_CAP", 2)
    _grant_many(db_session, 5, **{FIELD_GENDER: "female"})
    headers, _ = register("launcher@example.com")
    _launch(client, headers, filters=FEMALE_ONLY)

    assert db_session.query(Notification).filter_by(event_type="task.matched").count() == 2


def test_fanout_is_idempotent(client, register, db_session):
    _grant_many(db_session, 2, **{FIELD_GENDER: "female"})
    headers, _ = register("launcher@example.com")
    tid = _launch(client, headers, filters=FEMALE_ONLY)

    task = db_session.get(Task, tid)
    fan_out_task_matched(db_session, task)  # second fan-out, same task
    db_session.commit()

    assert db_session.query(Notification).filter_by(event_type="task.matched").count() == 2


def test_muted_user_gets_ledger_row_but_no_delivery(client, register, db_session):
    users = _grant_many(db_session, 1, **{FIELD_GENDER: "female"})
    users[0].notifications_muted = True
    db_session.commit()

    headers, _ = register("launcher@example.com")
    _launch(client, headers, filters=FEMALE_ONLY)

    row = db_session.query(Notification).filter_by(event_type="task.matched").one()
    assert row.status == "skipped"
    assert row.skip_reason == "muted"
    assert len(ConsoleNotifierBackend.outbox) == 0


def test_jump_lifecycle_notifications(client, register, db_session):
    launcher, _ = register("launcher@example.com")
    j1, _ = register("jumper1@example.com")
    j2, _ = register("jumper2@example.com")

    tid = _launch(client, launcher, accept_jumpers_manually=True, num_jumpers=1)
    jump1 = client.post(f"/tasks/{tid}/jump", headers=j1).json()
    jump2 = client.post(f"/tasks/{tid}/jump", headers=j2).json()

    types = lambda: {  # noqa: E731
        (n.event_type, n.user_id)
        for n in db_session.query(Notification).all()
        if n.event_type != "task.matched"
    }
    launcher_id = db_session.query(User).filter_by(email="launcher@example.com").one().id
    j1_id = db_session.query(User).filter_by(email="jumper1@example.com").one().id
    j2_id = db_session.query(User).filter_by(email="jumper2@example.com").one().id

    # two pending applications -> launcher notified twice
    assert ("jump.pending", launcher_id) in types()

    client.post(f"/tasks/{tid}/jumps/{jump1['id']}/approve", headers=launcher)
    assert ("jump.approved", j1_id) in types()
    assert ("task.full", launcher_id) in types()  # capacity 1 reached

    client.post(f"/tasks/{tid}/jumps/{jump2['id']}/reject", headers=launcher)
    assert ("jump.rejected", j2_id) in types()


def test_full_notification_on_auto_accept(client, register, db_session):
    launcher, _ = register("launcher@example.com")
    j1, _ = register("jumper1@example.com")
    tid = _launch(client, launcher, num_jumpers=1)
    client.post(f"/tasks/{tid}/jump", headers=j1)

    row = db_session.query(Notification).filter_by(event_type="task.full").one()
    assert row.dedupe_key == f"task.full:{tid}"


def test_mute_endpoint(client, register):
    headers, _ = register("mute-me@example.com")
    assert client.get("/users/me", headers=headers).json()["notifications_muted"] is False

    r = client.post("/users/me/notifications", headers=headers, json={"muted": True})
    assert r.status_code == 200
    assert client.get("/users/me", headers=headers).json()["notifications_muted"] is True


def test_delivery_failure_marks_failed_not_500(client, register, db_session, monkeypatch):
    """A broken notifier must never break the launch request."""
    from services import notifications as notif_module

    class ExplodingBackend:
        def send(self, chat_id, text):
            raise RuntimeError("boom")

    monkeypatch.setattr(notif_module, "get_notifier", lambda: ExplodingBackend())
    _grant_many(db_session, 1, **{FIELD_GENDER: "female"})
    headers, _ = register("launcher@example.com")
    tid = _launch(client, headers, filters=FEMALE_ONLY)  # asserts 201 inside

    assert tid is not None
    row = db_session.query(Notification).filter_by(event_type="task.matched").one()
    assert row.status == "failed"

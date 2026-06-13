# filepath: src/tests/test_bot_flows.py

"""Bot handler tests: real handlers + real API (ASGI in-process), with
duck-typed fakes for Telegram objects. Handlers only touch attributes, so
lightweight fakes are enough — no Telegram network anywhere.
"""

import httpx
import pytest

from app import app
from bot.api_client import ApiClient, ApiError
from bot.flows import launch as launch_flow
from bot.flows import my_jumps, my_tasks, start, submit

# --- fakes --------------------------------------------------------------


class FakeUser:
    def __init__(self, tg_id: int, username: str = "testcrow"):
        self.id = tg_id
        self.username = username


class FakeMessage:
    def __init__(self, text: str = "", user: FakeUser | None = None):
        self.text = text
        self.from_user = user
        self.video = None
        self.document = None
        self.sent: list[str] = []

    async def answer(self, text: str, reply_markup=None, **kwargs):
        self.sent.append(text)

    @property
    def last(self) -> str:
        return self.sent[-1] if self.sent else ""


class FakeQuery:
    def __init__(self, data: str, user: FakeUser, message: FakeMessage | None = None):
        self.data = data
        self.from_user = user
        self.message = message or FakeMessage(user=user)
        self.answers: list[str] = []

    async def answer(self, text: str = "", show_alert: bool = False, **kwargs):
        self.answers.append(text)


class FakeState:
    def __init__(self):
        self._state = None
        self._data: dict = {}

    async def set_state(self, state=None):
        self._state = state

    async def get_state(self):
        return self._state

    async def update_data(self, **kwargs):
        self._data.update(kwargs)

    async def get_data(self) -> dict:
        return dict(self._data)

    async def clear(self):
        self._state = None
        self._data = {}


class FakeFile:
    def __init__(self, size_bytes: int):
        self.file_size = size_bytes


@pytest.fixture()
async def api():
    client = ApiClient("http://test", "test-bridge-secret", transport=httpx.ASGITransport(app=app))
    yield client
    await client.close()


# --- launch flow end to end ----------------------------------------------


async def test_launch_flow_full_path_creates_real_task(api):
    user = FakeUser(31001)
    state = FakeState()

    msg = FakeMessage("/launch", user)
    await launch_flow.cmd_launch(msg, state)
    assert state._state == launch_flow.LaunchFlow.desc

    await launch_flow.step_desc(FakeMessage("Review our shiny app", user), state)
    assert state._state == launch_flow.LaunchFlow.budget

    await launch_flow.step_budget(FakeMessage("50", user), state)
    await launch_flow.step_you_earn(FakeMessage("5", user), state)
    await launch_flow.step_num_jumpers(FakeMessage("10", user), state)
    assert state._state == launch_flow.LaunchFlow.filter_location

    await launch_flow.step_location_text(FakeMessage("EMEA but not Russia", user), state)
    q = FakeQuery(f"{launch_flow.AGE_PREFIX}18-25", user)
    await launch_flow.step_age_button(q, state)
    q = FakeQuery(f"{launch_flow.GENDER_PREFIX}female", user)
    await launch_flow.step_gender(q, state)

    await launch_flow.step_deadline_text(FakeMessage("7", user), state)
    q = FakeQuery(f"{launch_flow.MANUAL_PREFIX}no", user)
    await launch_flow.step_manual(q, state, api)
    assert state._state == launch_flow.LaunchFlow.confirm
    assert "Confirm" in q.message.last
    # audience preview line + raw-location advisory on the card
    assert "fewer than" in q.message.last
    assert "free text" in q.message.last

    q = FakeQuery(launch_flow.CONFIRM, user)
    await launch_flow.step_confirm(q, state, api)
    assert state._state is None  # flow finished and cleared
    assert "launched" in q.message.last

    # the task really exists, with the filters the flow assembled
    tasks = await api.my_tasks(user.id)
    assert len(tasks) == 1
    assert tasks[0]["filters"]["basic_filters"]["location_filter"]["raw_statement"] == (
        "EMEA but not Russia"
    )
    assert tasks[0]["filters"]["basic_filters"]["age_range"] == {"min": 18, "max": 25}
    assert tasks[0]["submission_deadline"] is not None


async def test_launch_flow_budget_guard_keeps_user_in_flow(api):
    user = FakeUser(31002)
    state = FakeState()
    await launch_flow.cmd_launch(FakeMessage("/launch", user), state)
    await launch_flow.step_desc(FakeMessage("task", user), state)
    await launch_flow.step_budget(FakeMessage("10", user), state)
    await launch_flow.step_you_earn(FakeMessage("5", user), state)

    msg = FakeMessage("100", user)  # 100 x 5 > 10
    await launch_flow.step_num_jumpers(msg, state)
    assert state._state == launch_flow.LaunchFlow.num_jumpers  # still here
    assert "2" in msg.last  # max affordable hint

    msg = FakeMessage("2", user)
    await launch_flow.step_num_jumpers(msg, state)
    assert state._state == launch_flow.LaunchFlow.filter_location


async def test_launch_rejects_garbage_numbers(api):
    user = FakeUser(31003)
    state = FakeState()
    await launch_flow.cmd_launch(FakeMessage("/launch", user), state)
    await launch_flow.step_desc(FakeMessage("task", user), state)

    msg = FakeMessage("not a number", user)
    await launch_flow.step_budget(msg, state)
    assert state._state == launch_flow.LaunchFlow.budget  # re-asked


async def test_cancel_clears_any_flow_state():
    user = FakeUser(31004)
    state = FakeState()
    await launch_flow.cmd_launch(FakeMessage("/launch", user), state)
    await state.update_data(desc="half-finished")

    msg = FakeMessage("/cancel", user)
    await start.cmd_cancel(msg, state)
    assert state._state is None
    assert await state.get_data() == {}


async def test_cancel_with_nothing_in_progress():
    state = FakeState()
    msg = FakeMessage("/cancel", FakeUser(31005))
    await start.cmd_cancel(msg, state)
    assert "Nothing in progress" in msg.last


# --- jump / manage round trip via handlers ---------------------------------


async def test_jump_and_launcher_approval_via_handlers(api):
    launcher, jumper = FakeUser(32001), FakeUser(32002)

    task = await api.launch_task(
        launcher.id,
        {
            "desc": "curated",
            "total_budget": 10,
            "you_earn": 5,
            "num_jumpers": 1,
            "accept_jumpers_manually": True,
        },
    )

    # jumper applies through the browse handler
    from bot.flows import browse

    q = FakeQuery(f"{browse.JUMP_PREFIX}{task['id']}:1", jumper)
    await browse.cb_jump(q, api)
    assert any("Jumped" in a for a in q.answers)
    assert "approves Jumpers manually" in q.message.sent[0]

    # launcher sees the pending jump and approves it through the handler
    jumps = await api.task_jumps(launcher.id, task["id"])
    assert jumps[0]["status"] == "pending"
    q2 = FakeQuery(f"{my_tasks.APPROVE_PREFIX}{task['id']}:{jumps[0]['id']}", launcher)
    await my_tasks.cb_approve(q2, api)
    assert (await api.task_jumps(launcher.id, task["id"]))[0]["status"] == "active"

    # duplicate jump through the handler surfaces a friendly alert, no crash
    q3 = FakeQuery(f"{browse.JUMP_PREFIX}{task['id']}:1", jumper)
    await browse.cb_jump(q3, api)
    assert any("Can't jump" in a for a in q3.answers)


async def test_forfeit_via_handler(api):
    launcher, jumper = FakeUser(32003), FakeUser(32004)
    task = await api.launch_task(
        launcher.id, {"desc": "t", "total_budget": 5, "you_earn": 5, "num_jumpers": 1}
    )
    await api.jump(jumper.id, task["id"])

    q = FakeQuery(f"{my_jumps.FORFEIT_PREFIX}{task['id']}", jumper)
    await my_jumps.cb_forfeit(q, api)
    parts = await api.participated(jumper.id)
    assert parts[0]["jump"]["status"] == "forfeited"


# --- submit flow size guard --------------------------------------------------


async def test_submit_flow_size_guard():
    user = FakeUser(33001)
    state = FakeState()

    q = FakeQuery(f"{my_jumps.SUBMIT_PREFIX}42", user)
    await submit.cb_submit(q, state)
    assert state._state == submit.SubmitFlow.waiting_file
    assert (await state.get_data())["task_id"] == 42

    # too big: stays in flow with guidance
    big = FakeMessage("", user)
    big.video = FakeFile(25 * 1024 * 1024)
    await submit.on_file(big, state)
    assert "MB" in big.last
    assert state._state == submit.SubmitFlow.waiting_file

    # small enough: stub acceptance, state cleared
    ok = FakeMessage("", user)
    ok.video = FakeFile(5 * 1024 * 1024)
    await submit.on_file(ok, state)
    assert "Got your recording" in ok.last
    assert state._state is None


async def test_submit_rejects_non_file():
    user = FakeUser(33002)
    state = FakeState()
    await submit.cb_submit(FakeQuery(f"{my_jumps.SUBMIT_PREFIX}1", user), state)
    msg = FakeMessage("here is text instead", user)
    await submit.on_not_a_file(msg)
    assert "video or file" in msg.last


# --- profile & api client error surface ---------------------------------------


async def test_profile_handler_renders_bridged_account(api):
    user = FakeUser(34001, username="profilecrow")
    msg = FakeMessage("/profile", user)
    await api.ensure_account(user.id, user.username)
    await start.cmd_profile(msg, api)
    assert "profilecrow" in msg.last


async def test_api_error_passthrough(api):
    with pytest.raises(ApiError) as exc_info:
        await api.get_task(35001, 999_999)
    assert exc_info.value.status_code == 404

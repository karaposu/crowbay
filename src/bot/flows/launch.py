# filepath: src/bot/flows/launch.py

"""The launch flow: guided task creation, six logical steps, every step
validated and cancellable, nothing sent to the API before the confirmation
card is accepted.

Location is stored as raw_statement only — the bot does not geocode; parsing
raw statements into structured location filters is the matching component's
job (devdocs/filter_design.md).
"""

from datetime import datetime, timedelta, timezone

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from bot import keyboards, texts
from bot.api_client import ApiClient

router = Router(name="launch")


class LaunchFlow(StatesGroup):
    desc = State()
    budget = State()
    you_earn = State()
    num_jumpers = State()
    filter_location = State()
    filter_age = State()
    filter_gender = State()
    deadline = State()
    manual = State()
    confirm = State()


# --- keyboards -----------------------------------------------------------

SKIP_LOCATION = "lf:loc:skip"
AGE_PREFIX = "lf:age:"
GENDER_PREFIX = "lf:gender:"
SKIP_DEADLINE = "lf:deadline:skip"
MANUAL_PREFIX = "lf:manual:"
CONFIRM = "lf:confirm"
RESTART = "lf:restart"


def _skip_location_kb() -> InlineKeyboardMarkup:
    return keyboards.options_kb([("🌍 Anywhere (skip)", SKIP_LOCATION)])


def _age_kb() -> InlineKeyboardMarkup:
    return keyboards.options_kb(
        [
            ("18–25", f"{AGE_PREFIX}18-25"),
            ("25–35", f"{AGE_PREFIX}25-35"),
            ("18+", f"{AGE_PREFIX}18-"),
            ("Any age (skip)", f"{AGE_PREFIX}skip"),
        ]
    )


def _gender_kb() -> InlineKeyboardMarkup:
    return keyboards.options_kb(
        [
            ("Female", f"{GENDER_PREFIX}female"),
            ("Male", f"{GENDER_PREFIX}male"),
            ("Any (skip)", f"{GENDER_PREFIX}skip"),
        ]
    )


def _deadline_kb() -> InlineKeyboardMarkup:
    return keyboards.options_kb([("No deadline (skip)", SKIP_DEADLINE)])


def _manual_kb() -> InlineKeyboardMarkup:
    return keyboards.options_kb(
        [
            ("⚡ Auto-accept Jumpers", f"{MANUAL_PREFIX}no"),
            ("✅ I'll approve each Jumper", f"{MANUAL_PREFIX}yes"),
        ]
    )


def _confirm_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🚀 Launch it", callback_data=CONFIRM)],
            [InlineKeyboardButton(text="↩️ Start over", callback_data=RESTART)],
            keyboards.cancel_row(),
        ]
    )


# --- payload / summary ---------------------------------------------------


def build_payload(data: dict) -> dict:
    basic: dict = {}
    if data.get("location_raw"):
        basic["location_filter"] = {"raw_statement": data["location_raw"]}
    if data.get("age_min") is not None or data.get("age_max") is not None:
        age: dict = {}
        if data.get("age_min") is not None:
            age["min"] = data["age_min"]
        if data.get("age_max") is not None:
            age["max"] = data["age_max"]
        basic["age_range"] = age
    if data.get("gender"):
        basic["gender"] = data["gender"]

    payload: dict = {
        "desc": data["desc"],
        "total_budget": data["budget"],
        "you_earn": data["you_earn"],
        "num_jumpers": data["num_jumpers"],
        "accept_jumpers_manually": data.get("manual", False),
    }
    if basic:
        payload["filters"] = {"basic_filters": basic}
    if data.get("deadline_days"):
        deadline = datetime.now(timezone.utc) + timedelta(days=data["deadline_days"])
        payload["submission_deadline"] = deadline.isoformat()
    return payload


def summary_text(data: dict, audience: str | None = None, warnings: list[str] | None = None) -> str:
    parts = []
    if data.get("location_raw"):
        parts.append(f"location: {data['location_raw']}")
    if data.get("age_min") is not None or data.get("age_max") is not None:
        lo = data.get("age_min") or ""
        hi = data.get("age_max") or ""
        parts.append(f"age {lo}–{hi}".rstrip("–"))
    if data.get("gender"):
        parts.append(data["gender"])
    filters_line = ", ".join(parts) if parts else "anyone"
    deadline_line = f"{data['deadline_days']} days" if data.get("deadline_days") else "none"
    approval = "manual approval" if data.get("manual") else "auto-accept"
    text = texts.LAUNCH_SUMMARY.format(
        desc=data["desc"],
        budget=data["budget"],
        you_earn=data["you_earn"],
        num_jumpers=data["num_jumpers"],
        filters=filters_line,
        deadline=deadline_line,
        approval=approval,
    )
    extra = []
    if audience is not None:
        extra.append(texts.LAUNCH_AUDIENCE_LINE.format(audience=audience))
    for warning in warnings or []:
        extra.append(f"⚠️ <i>{warning}</i>")
    if extra:
        text = text.replace("Launch it?", "\n".join(extra) + "\n\nLaunch it?")
    return text


# --- entry ---------------------------------------------------------------


async def _begin(target: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(LaunchFlow.desc)
    await target.answer(texts.LAUNCH_ASK_DESC, reply_markup=keyboards.cancel_kb())


@router.message(Command("launch"))
async def cmd_launch(message: Message, state: FSMContext) -> None:
    await _begin(message, state)


@router.callback_query(F.data == keyboards.MENU_LAUNCH)
async def cb_launch(query: CallbackQuery, state: FSMContext) -> None:
    await query.answer()
    await _begin(query.message, state)


@router.callback_query(F.data == RESTART)
async def cb_restart(query: CallbackQuery, state: FSMContext) -> None:
    await query.answer("Starting over")
    await _begin(query.message, state)


# --- step 1: description --------------------------------------------------


@router.message(LaunchFlow.desc, F.text)
async def step_desc(message: Message, state: FSMContext) -> None:
    text = message.text.strip()
    if not 1 <= len(text) <= 5000:
        await message.answer(texts.LAUNCH_DESC_INVALID, reply_markup=keyboards.cancel_kb())
        return
    await state.update_data(desc=text)
    await state.set_state(LaunchFlow.budget)
    await message.answer(texts.LAUNCH_ASK_BUDGET, reply_markup=keyboards.cancel_kb())


# --- step 2: money (budget -> pay -> slots) --------------------------------


def _parse_positive_number(text: str) -> float | None:
    try:
        value = float(text.replace(",", ".").strip())
    except ValueError:
        return None
    return value if value > 0 else None


@router.message(LaunchFlow.budget, F.text)
async def step_budget(message: Message, state: FSMContext) -> None:
    value = _parse_positive_number(message.text)
    if value is None:
        await message.answer(texts.LAUNCH_NUMBER_INVALID, reply_markup=keyboards.cancel_kb())
        return
    await state.update_data(budget=value)
    await state.set_state(LaunchFlow.you_earn)
    await message.answer(texts.LAUNCH_ASK_YOU_EARN, reply_markup=keyboards.cancel_kb())


@router.message(LaunchFlow.you_earn, F.text)
async def step_you_earn(message: Message, state: FSMContext) -> None:
    value = _parse_positive_number(message.text)
    if value is None:
        await message.answer(texts.LAUNCH_NUMBER_INVALID, reply_markup=keyboards.cancel_kb())
        return
    data = await state.get_data()
    if value > data["budget"]:
        await message.answer(
            texts.LAUNCH_EARN_EXCEEDS_BUDGET.format(budget=data["budget"]),
            reply_markup=keyboards.cancel_kb(),
        )
        return
    await state.update_data(you_earn=value)
    await state.set_state(LaunchFlow.num_jumpers)
    await message.answer(texts.LAUNCH_ASK_NUM_JUMPERS, reply_markup=keyboards.cancel_kb())


@router.message(LaunchFlow.num_jumpers, F.text)
async def step_num_jumpers(message: Message, state: FSMContext) -> None:
    try:
        value = int(message.text.strip())
    except ValueError:
        value = 0
    if not 1 <= value <= 10_000:
        await message.answer(texts.LAUNCH_COUNT_INVALID, reply_markup=keyboards.cancel_kb())
        return
    data = await state.get_data()
    # the API will reject this anyway — catch it here so the user fixes it in-flow
    if data["you_earn"] * value > data["budget"]:
        max_affordable = int(data["budget"] // data["you_earn"])
        await message.answer(
            texts.LAUNCH_BUDGET_SHORT.format(
                total=data["you_earn"] * value,
                budget=data["budget"],
                max_affordable=max_affordable,
            ),
            reply_markup=keyboards.cancel_kb(),
        )
        return
    await state.update_data(num_jumpers=value)
    await state.set_state(LaunchFlow.filter_location)
    await message.answer(texts.LAUNCH_ASK_LOCATION, reply_markup=_skip_location_kb())


# --- step 3: filters -------------------------------------------------------


@router.message(LaunchFlow.filter_location, F.text)
async def step_location_text(message: Message, state: FSMContext) -> None:
    await state.update_data(location_raw=message.text.strip()[:200])
    await state.set_state(LaunchFlow.filter_age)
    await message.answer(texts.LAUNCH_ASK_AGE, reply_markup=_age_kb())


@router.callback_query(LaunchFlow.filter_location, F.data == SKIP_LOCATION)
async def step_location_skip(query: CallbackQuery, state: FSMContext) -> None:
    await query.answer()
    await state.set_state(LaunchFlow.filter_age)
    await query.message.answer(texts.LAUNCH_ASK_AGE, reply_markup=_age_kb())


def parse_age_range(text: str) -> tuple[int | None, int | None] | None:
    """'18-25' -> (18, 25); '18-' -> (18, None); 'skip' -> (None, None)."""
    if text == "skip":
        return (None, None)
    if "-" not in text:
        return None
    lo_s, _, hi_s = text.partition("-")
    try:
        lo = int(lo_s) if lo_s else None
        hi = int(hi_s) if hi_s else None
    except ValueError:
        return None
    if lo is not None and hi is not None and lo > hi:
        return None
    if (lo is not None and not 0 <= lo <= 130) or (hi is not None and not 0 <= hi <= 130):
        return None
    return (lo, hi)


@router.callback_query(LaunchFlow.filter_age, F.data.startswith(AGE_PREFIX))
async def step_age_button(query: CallbackQuery, state: FSMContext) -> None:
    await query.answer()
    parsed = parse_age_range(query.data.removeprefix(AGE_PREFIX))
    if parsed is None:
        return
    lo, hi = parsed
    await state.update_data(age_min=lo, age_max=hi)
    await state.set_state(LaunchFlow.filter_gender)
    await query.message.answer(texts.LAUNCH_ASK_GENDER, reply_markup=_gender_kb())


@router.message(LaunchFlow.filter_age, F.text)
async def step_age_text(message: Message, state: FSMContext) -> None:
    parsed = parse_age_range(message.text.strip())
    if parsed is None:
        await message.answer(texts.LAUNCH_AGE_INVALID, reply_markup=_age_kb())
        return
    lo, hi = parsed
    await state.update_data(age_min=lo, age_max=hi)
    await state.set_state(LaunchFlow.filter_gender)
    await message.answer(texts.LAUNCH_ASK_GENDER, reply_markup=_gender_kb())


@router.callback_query(LaunchFlow.filter_gender, F.data.startswith(GENDER_PREFIX))
async def step_gender(query: CallbackQuery, state: FSMContext) -> None:
    await query.answer()
    choice = query.data.removeprefix(GENDER_PREFIX)
    if choice != "skip":
        await state.update_data(gender=choice)
    await state.set_state(LaunchFlow.deadline)
    await query.message.answer(texts.LAUNCH_ASK_DEADLINE, reply_markup=_deadline_kb())


# --- step 4: deadline ------------------------------------------------------


@router.message(LaunchFlow.deadline, F.text)
async def step_deadline_text(message: Message, state: FSMContext) -> None:
    try:
        days = int(message.text.strip())
    except ValueError:
        days = 0
    if not 1 <= days <= 365:
        await message.answer(texts.LAUNCH_DEADLINE_INVALID, reply_markup=_deadline_kb())
        return
    await state.update_data(deadline_days=days)
    await state.set_state(LaunchFlow.manual)
    await message.answer(texts.LAUNCH_ASK_MANUAL, reply_markup=_manual_kb())


@router.callback_query(LaunchFlow.deadline, F.data == SKIP_DEADLINE)
async def step_deadline_skip(query: CallbackQuery, state: FSMContext) -> None:
    await query.answer()
    await state.set_state(LaunchFlow.manual)
    await query.message.answer(texts.LAUNCH_ASK_MANUAL, reply_markup=_manual_kb())


# --- step 5: approval mode -------------------------------------------------


@router.callback_query(LaunchFlow.manual, F.data.startswith(MANUAL_PREFIX))
async def step_manual(query: CallbackQuery, state: FSMContext, api: ApiClient) -> None:
    await query.answer()
    await state.update_data(manual=query.data.removeprefix(MANUAL_PREFIX) == "yes")
    await state.set_state(LaunchFlow.confirm)
    data = await state.get_data()

    # Audience preview on the confirmation card (matching C4); raw-location
    # advisory warnings surface here too (C6). Preview failure never blocks
    # the flow — the card just omits the line.
    audience = None
    warnings: list[str] = []
    try:
        preview = await api.audience_preview(query.from_user.id, build_payload(data).get("filters"))
        audience = preview["display"]
        warnings = preview.get("warnings") or []
    except Exception:  # noqa: BLE001 — preview is decorative, the flow is not
        pass

    await query.message.answer(
        summary_text(data, audience=audience, warnings=warnings), reply_markup=_confirm_kb()
    )


# --- step 6: confirm -> POST /tasks ----------------------------------------


@router.callback_query(LaunchFlow.confirm, F.data == CONFIRM)
async def step_confirm(query: CallbackQuery, state: FSMContext, api: ApiClient) -> None:
    await query.answer()
    data = await state.get_data()
    task = await api.launch_task(query.from_user.id, build_payload(data))
    await state.clear()
    await query.message.answer(
        texts.LAUNCH_DONE.format(task_id=task["id"], num_jumpers=task["num_jumpers"]),
        reply_markup=keyboards.main_menu(),
    )

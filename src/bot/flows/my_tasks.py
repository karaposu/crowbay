# filepath: src/bot/flows/my_tasks.py

"""Launcher view: own tasks, and per-task Jumper management (approve/decline)."""

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from bot import keyboards, texts
from bot.api_client import ApiClient

router = Router(name="my_tasks")

JUMPERS_PREFIX = "mt:jumps:"
APPROVE_PREFIX = "mt:approve:"
REJECT_PREFIX = "mt:reject:"
SHOWN_LIMIT = 10


def render_tasks(tasks: list[dict]) -> tuple[str, InlineKeyboardMarkup | None]:
    if not tasks:
        return texts.MY_TASKS_EMPTY, None

    lines = [texts.MY_TASKS_HEADER]
    buttons: list[list[InlineKeyboardButton]] = []
    for t in tasks[:SHOWN_LIMIT]:
        emoji = texts.TASK_STATUS_EMOJI.get(t["status"], "▫️")
        lines.append(
            f"{emoji} <b>#{t['id']}</b> {t['desc'][:60]} — "
            f"{t['num_jumpers']} slot(s) · <i>{t['status']}</i>"
        )
        buttons.append(
            [
                InlineKeyboardButton(
                    text=f"👥 Jumpers of #{t['id']}",
                    callback_data=f"{JUMPERS_PREFIX}{t['id']}",
                )
            ]
        )
    if len(tasks) > SHOWN_LIMIT:
        lines.append(texts.MY_TASKS_TRUNCATED.format(shown=SHOWN_LIMIT, total=len(tasks)))
    return "\n".join(lines), InlineKeyboardMarkup(inline_keyboard=buttons)


def render_jumps(task_id: int, jumps: list[dict]) -> tuple[str, InlineKeyboardMarkup | None]:
    if not jumps:
        return texts.TASK_JUMPS_EMPTY.format(task_id=task_id), None

    lines = [texts.TASK_JUMPS_HEADER.format(task_id=task_id)]
    buttons: list[list[InlineKeyboardButton]] = []
    for j in jumps:
        emoji = texts.STATUS_EMOJI.get(j["status"], "▫️")
        lines.append(f"{emoji} Jumper {j['jumper_id']} — <i>{j['status']}</i>")
        if j["status"] == "pending":
            buttons.append(
                [
                    InlineKeyboardButton(
                        text=f"✅ Approve {j['jumper_id']}",
                        callback_data=f"{APPROVE_PREFIX}{task_id}:{j['id']}",
                    ),
                    InlineKeyboardButton(
                        text=f"❌ Decline {j['jumper_id']}",
                        callback_data=f"{REJECT_PREFIX}{task_id}:{j['id']}",
                    ),
                ]
            )
    kb = InlineKeyboardMarkup(inline_keyboard=buttons) if buttons else None
    return "\n".join(lines), kb


async def _show_tasks(target: Message, api: ApiClient, tg_id: int) -> None:
    tasks = await api.my_tasks(tg_id)
    text, kb = render_tasks(tasks)
    await target.answer(text, reply_markup=kb)


async def _show_jumps(target: Message, api: ApiClient, tg_id: int, task_id: int) -> None:
    jumps = await api.task_jumps(tg_id, task_id)
    text, kb = render_jumps(task_id, jumps)
    await target.answer(text, reply_markup=kb)


@router.message(Command("mytasks"))
async def cmd_my_tasks(message: Message, api: ApiClient) -> None:
    await _show_tasks(message, api, message.from_user.id)


@router.callback_query(F.data == keyboards.MENU_MY_TASKS)
async def cb_my_tasks(query: CallbackQuery, api: ApiClient) -> None:
    await query.answer()
    await _show_tasks(query.message, api, query.from_user.id)


@router.callback_query(F.data.startswith(JUMPERS_PREFIX))
async def cb_jumpers(query: CallbackQuery, api: ApiClient) -> None:
    await query.answer()
    try:
        task_id = int(query.data.removeprefix(JUMPERS_PREFIX))
    except ValueError:
        return
    await _show_jumps(query.message, api, query.from_user.id, task_id)


def _parse_pair(data: str, prefix: str) -> tuple[int, int] | None:
    a, _, b = data.removeprefix(prefix).partition(":")
    try:
        return int(a), int(b)
    except ValueError:
        return None


@router.callback_query(F.data.startswith(APPROVE_PREFIX))
async def cb_approve(query: CallbackQuery, api: ApiClient) -> None:
    pair = _parse_pair(query.data, APPROVE_PREFIX)
    if pair is None:
        await query.answer()
        return
    task_id, jump_id = pair
    await api.approve_jump(query.from_user.id, task_id, jump_id)
    await query.answer("Approved ✅")
    await _show_jumps(query.message, api, query.from_user.id, task_id)


@router.callback_query(F.data.startswith(REJECT_PREFIX))
async def cb_reject(query: CallbackQuery, api: ApiClient) -> None:
    pair = _parse_pair(query.data, REJECT_PREFIX)
    if pair is None:
        await query.answer()
        return
    task_id, jump_id = pair
    await api.reject_jump(query.from_user.id, task_id, jump_id)
    await query.answer("Declined")
    await _show_jumps(query.message, api, query.from_user.id, task_id)

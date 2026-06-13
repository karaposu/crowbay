# filepath: src/bot/flows/my_jumps.py

"""Jumper view: participations with status, forfeit, and submit-proof entry."""

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from bot import keyboards, texts
from bot.api_client import ApiClient

router = Router(name="my_jumps")

FORFEIT_PREFIX = "mj:forfeit:"
SUBMIT_PREFIX = "mj:submit:"
SHOWN_LIMIT = 10


def render(participations: list[dict]) -> tuple[str, InlineKeyboardMarkup | None]:
    if not participations:
        return texts.MY_JUMPS_EMPTY, None

    lines = [texts.MY_JUMPS_HEADER]
    buttons: list[list[InlineKeyboardButton]] = []
    for p in participations[:SHOWN_LIMIT]:
        jump, task = p["jump"], p["task"]
        emoji = texts.STATUS_EMOJI.get(jump["status"], "▫️")
        lines.append(
            f"{emoji} <b>#{task['id']}</b> {task['desc'][:60]} — "
            f"{task['you_earn']} USDT · <i>{jump['status']}</i>"
        )
        if jump["status"] in ("pending", "active"):
            row = [
                InlineKeyboardButton(
                    text=f"🏳️ Forfeit #{task['id']}",
                    callback_data=f"{FORFEIT_PREFIX}{task['id']}",
                )
            ]
            if jump["status"] == "active":
                row.append(
                    InlineKeyboardButton(
                        text=f"📤 Submit proof #{task['id']}",
                        callback_data=f"{SUBMIT_PREFIX}{task['id']}",
                    )
                )
            buttons.append(row)
    if len(participations) > SHOWN_LIMIT:
        lines.append(texts.MY_JUMPS_TRUNCATED.format(shown=SHOWN_LIMIT, total=len(participations)))

    kb = InlineKeyboardMarkup(inline_keyboard=buttons) if buttons else None
    return "\n".join(lines), kb


async def _show(target: Message, api: ApiClient, tg_id: int) -> None:
    participations = await api.participated(tg_id)
    text, kb = render(participations)
    await target.answer(text, reply_markup=kb)


@router.message(Command("myjumps"))
async def cmd_my_jumps(message: Message, api: ApiClient) -> None:
    await _show(message, api, message.from_user.id)


@router.callback_query(F.data == keyboards.MENU_MY_JUMPS)
async def cb_my_jumps(query: CallbackQuery, api: ApiClient) -> None:
    await query.answer()
    await _show(query.message, api, query.from_user.id)


@router.callback_query(F.data.startswith(FORFEIT_PREFIX))
async def cb_forfeit(query: CallbackQuery, api: ApiClient) -> None:
    try:
        task_id = int(query.data.removeprefix(FORFEIT_PREFIX))
    except ValueError:
        await query.answer()
        return
    await api.forfeit(query.from_user.id, task_id)
    await query.answer("Forfeited")
    await query.message.answer(texts.FORFEITED_OK.format(task_id=task_id))
    await _show(query.message, api, query.from_user.id)

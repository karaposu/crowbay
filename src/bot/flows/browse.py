# filepath: src/bot/flows/browse.py

"""Browse open tasks: one card per page, prev/next paging, Jump button.

Paging edits the card message in place to keep the chat clean.
"""

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from bot import keyboards, texts
from bot.api_client import ApiClient, ApiError

router = Router(name="browse")

PAGE_PREFIX = "br:page:"
JUMP_PREFIX = "br:jump:"


def card_text(task: dict, index: int, total: int) -> str:
    return texts.BROWSE_CARD.format(
        index=index,
        total=total,
        desc=task["desc"][:300],
        you_earn=task["you_earn"],
        num_jumpers=task["num_jumpers"],
        category=task["category"] or "general",
        approval="manual approval" if task["accept_jumpers_manually"] else "auto-accept",
    )


def card_kb(task: dict, page: int, total: int) -> InlineKeyboardMarkup:
    nav: list[InlineKeyboardButton] = []
    if page > 1:
        nav.append(InlineKeyboardButton(text="⬅️ Prev", callback_data=f"{PAGE_PREFIX}{page - 1}"))
    if page < total:
        nav.append(InlineKeyboardButton(text="Next ➡️", callback_data=f"{PAGE_PREFIX}{page + 1}"))
    rows = []
    if nav:
        rows.append(nav)
    rows.append(
        [
            InlineKeyboardButton(
                text="🐦 Jump on this", callback_data=f"{JUMP_PREFIX}{task['id']}:{page}"
            )
        ]
    )
    rows.append([InlineKeyboardButton(text="↩️ Menu", callback_data="br:menu")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


async def _render_page(
    api: ApiClient, tg_id: int, page: int
) -> tuple[str, InlineKeyboardMarkup | None]:
    data = await api.browse(tg_id, page=page, size=1, status="open")
    total = data["total"]
    if total == 0 or not data["items"]:
        return texts.BROWSE_EMPTY, None
    task = data["items"][0]
    return card_text(task, page, total), card_kb(task, page, total)


@router.message(Command("browse"))
async def cmd_browse(message: Message, api: ApiClient) -> None:
    text, kb = await _render_page(api, message.from_user.id, 1)
    await message.answer(text, reply_markup=kb)


@router.callback_query(F.data == keyboards.MENU_BROWSE)
async def cb_browse(query: CallbackQuery, api: ApiClient) -> None:
    await query.answer()
    text, kb = await _render_page(api, query.from_user.id, 1)
    await query.message.answer(text, reply_markup=kb)


@router.callback_query(F.data == "br:menu")
async def cb_menu(query: CallbackQuery) -> None:
    await query.answer()
    await query.message.answer(texts.WELCOME, reply_markup=keyboards.main_menu())


@router.callback_query(F.data.startswith(PAGE_PREFIX))
async def cb_page(query: CallbackQuery, api: ApiClient) -> None:
    await query.answer()
    try:
        page = int(query.data.removeprefix(PAGE_PREFIX))
    except ValueError:
        return
    text, kb = await _render_page(api, query.from_user.id, max(1, page))
    await query.message.edit_text(text, reply_markup=kb)


@router.callback_query(F.data.startswith(JUMP_PREFIX))
async def cb_jump(query: CallbackQuery, api: ApiClient) -> None:
    payload = query.data.removeprefix(JUMP_PREFIX)
    task_id_s, _, page_s = payload.partition(":")
    try:
        task_id = int(task_id_s)
        page = int(page_s) if page_s else 1
    except ValueError:
        await query.answer()
        return

    try:
        jump = await api.jump(query.from_user.id, task_id)
    except ApiError as e:
        # full / duplicate / own task — show why, keep browsing
        await query.answer(f"Can't jump: {e.detail}", show_alert=True)
        return

    await query.answer("Jumped! 🐦")
    done_text = (texts.JUMP_PENDING if jump["status"] == "pending" else texts.JUMP_ACTIVE).format(
        task_id=task_id
    )
    await query.message.answer(done_text)

    # refresh the card so slot counts/status stay honest
    text, kb = await _render_page(api, query.from_user.id, page)
    try:
        await query.message.edit_text(text, reply_markup=kb)
    except Exception:  # message may be unchanged or too old to edit — not worth failing
        pass

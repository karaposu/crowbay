# filepath: src/bot/flows/start.py

"""Entry points: /start, /help, /cancel, /profile and their menu buttons."""

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot import keyboards, texts
from bot.api_client import ApiClient

router = Router(name="start")


@router.message(CommandStart())
async def cmd_start(message: Message, api: ApiClient, state: FSMContext) -> None:
    await state.clear()  # /start always escapes any flow
    user = message.from_user
    await api.ensure_account(user.id, user.username)
    await message.answer(texts.WELCOME, reply_markup=keyboards.main_menu())


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    await message.answer(texts.HELP)


@router.callback_query(F.data == keyboards.MENU_HELP)
async def cb_help(query: CallbackQuery) -> None:
    await query.answer()
    await query.message.answer(texts.HELP)


@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext) -> None:
    if await state.get_state() is None:
        await message.answer(texts.NOTHING_TO_CANCEL)
        return
    await state.clear()
    await message.answer(texts.CANCELLED)


@router.callback_query(F.data == keyboards.CANCEL)
async def cb_cancel(query: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await query.answer("Cancelled")
    await query.message.answer(texts.CANCELLED)


def format_profile(me: dict) -> str:
    verifs = me.get("verifications") or []
    vtext = ", ".join(f"{v['verification_name']} ({v['status']})" for v in verifs) or "none yet"
    trust = me.get("trust_score")
    return texts.PROFILE_TEMPLATE.format(
        handle=me.get("telegram_handle") or "—",
        email=me.get("email") or "—",
        verifications=vtext,
        trust=trust if trust is not None else "—",
    )


@router.message(Command("profile"))
async def cmd_profile(message: Message, api: ApiClient) -> None:
    me = await api.me(message.from_user.id)
    await message.answer(format_profile(me))


@router.callback_query(F.data == keyboards.MENU_PROFILE)
async def cb_profile(query: CallbackQuery, api: ApiClient) -> None:
    await query.answer()
    me = await api.me(query.from_user.id)
    await query.message.answer(format_profile(me))

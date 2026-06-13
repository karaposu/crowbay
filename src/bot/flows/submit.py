# filepath: src/bot/flows/submit.py

"""Submit-proof flow, Stage A (tg_bot_bom.md §5).

Accepts a screen recording and enforces the Telegram download cap with
friendly guidance. Actual storage/verification is the verification
component's job — until PROOF_UPLOAD_ENABLED, accepted files get a
"received, coming soon" stub so the UX is exercisable end to end.

Stage B (self-hosted Bot API server) only changes TG_FILE_LIMIT_MB.
"""

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from bot import keyboards, texts
from bot.flows.my_jumps import SUBMIT_PREFIX
from config import settings

router = Router(name="submit")


class SubmitFlow(StatesGroup):
    waiting_file = State()


@router.callback_query(F.data.startswith(SUBMIT_PREFIX))
async def cb_submit(query: CallbackQuery, state: FSMContext) -> None:
    try:
        task_id = int(query.data.removeprefix(SUBMIT_PREFIX))
    except ValueError:
        await query.answer()
        return
    await query.answer()
    await state.set_state(SubmitFlow.waiting_file)
    await state.update_data(task_id=task_id)
    await query.message.answer(
        texts.SUBMIT_ASK_FILE.format(task_id=task_id, limit=settings.TG_FILE_LIMIT_MB),
        reply_markup=keyboards.cancel_kb(),
    )


@router.message(SubmitFlow.waiting_file, F.video | F.document)
async def on_file(message: Message, state: FSMContext) -> None:
    file = message.video or message.document
    size = file.file_size or 0
    limit_bytes = settings.TG_FILE_LIMIT_MB * 1024 * 1024

    if size > limit_bytes:
        await message.answer(
            texts.FILE_TOO_BIG.format(
                size_mb=round(size / (1024 * 1024), 1), limit=settings.TG_FILE_LIMIT_MB
            ),
            reply_markup=keyboards.cancel_kb(),
        )
        return  # stay in the flow; the user can retry with a smaller file

    data = await state.get_data()
    task_id = data.get("task_id")
    await state.clear()

    if not settings.PROOF_UPLOAD_ENABLED:
        await message.answer(texts.SUBMIT_RECEIVED_STUB.format(task_id=task_id))
        return

    # Verification component lands here: download via bot API / hand the
    # file_id to the backend upload endpoint, flip jump to "submitted".
    await message.answer(texts.SUBMIT_RECEIVED_STUB.format(task_id=task_id))


@router.message(SubmitFlow.waiting_file)
async def on_not_a_file(message: Message) -> None:
    await message.answer(texts.SUBMIT_NOT_A_FILE, reply_markup=keyboards.cancel_kb())

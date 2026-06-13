# filepath: src/bot/middleware.py

import logging
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware, Bot
from aiogram.types import CallbackQuery, Message, TelegramObject

from bot import texts

logger = logging.getLogger(__name__)


class PrivateChatOnlyMiddleware(BaseMiddleware):
    """Reject group/channel usage politely; the bot is a private-chat product."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        chat = None
        if isinstance(event, Message):
            chat = event.chat
        elif isinstance(event, CallbackQuery) and event.message:
            chat = event.message.chat

        if chat is not None and chat.type != "private":
            if isinstance(event, Message):
                await event.answer(texts.GROUP_REJECT)
            elif isinstance(event, CallbackQuery):
                await event.answer(texts.GROUP_REJECT, show_alert=True)
            return None
        return await handler(event, data)


class FloodGuardMiddleware(BaseMiddleware):
    """Per-user token bucket: BURST updates instantly, refill RATE/sec.

    Throttled users get one notice, then silence until they slow down.
    """

    BURST = 5
    RATE = 1.0  # tokens per second

    def __init__(self):
        self._buckets: dict[int, tuple[float, float]] = {}  # user_id -> (tokens, last_ts)
        self._notified: set[int] = set()

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        import time

        user = getattr(event, "from_user", None)
        if user is None:
            return await handler(event, data)

        now = time.monotonic()
        tokens, last = self._buckets.get(user.id, (float(self.BURST), now))
        tokens = min(float(self.BURST), tokens + (now - last) * self.RATE)

        if tokens < 1.0:
            self._buckets[user.id] = (tokens, now)
            if user.id not in self._notified:
                self._notified.add(user.id)
                if isinstance(event, Message):
                    await event.answer("Easy there — give me a second. 🐦")
                elif isinstance(event, CallbackQuery):
                    await event.answer("Slow down a little 🐦")
            return None

        self._notified.discard(user.id)
        self._buckets[user.id] = (tokens - 1.0, now)
        return await handler(event, data)


async def error_handler(event, bot: Bot) -> bool:
    """Catch-all boundary: apologize in chat, log the truth, never go silent."""
    exc = event.exception
    update = event.update

    chat_id = None
    if update.message:
        chat_id = update.message.chat.id
    elif update.callback_query and update.callback_query.message:
        chat_id = update.callback_query.message.chat.id

    text = texts.friendly_api_error(exc)
    logger.exception("Handler error (chat_id=%s): %s", chat_id, exc)

    if chat_id is not None:
        try:
            await bot.send_message(chat_id, text)
        except Exception:  # last resort: never raise out of the error handler
            logger.exception("Failed to deliver error message to chat %s", chat_id)
    return True

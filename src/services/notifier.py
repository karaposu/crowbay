# filepath: src/services/notifier.py

"""Notification delivery backends (matching C8).

- console (default): logs + records to an outbox tests can read.
- telegram: the API process sends DIRECTLY via the Bot API (httpx) — the
  bot process stays a pure client and is not involved in delivery.
"""

import logging
from dataclasses import dataclass

import httpx

from config import settings

logger = logging.getLogger(__name__)


class NotifyDeliveryError(Exception):
    pass


class RecipientBlockedError(NotifyDeliveryError):
    """The user blocked the bot — permanent, don't retry."""


@dataclass
class SentNotification:
    chat_id: str
    text: str


class ConsoleNotifierBackend:
    outbox: list[SentNotification] = []  # class-level so tests can inspect

    def send(self, chat_id: str, text: str) -> str:
        self.outbox.append(SentNotification(chat_id=chat_id, text=text))
        logger.info("NOTIFY (console) chat_id=%s text=%r", chat_id, text)
        return f"console-{len(self.outbox)}"

    @classmethod
    def reset(cls) -> None:
        cls.outbox.clear()


class TelegramNotifierBackend:
    def __init__(self, bot_token: str):
        self._url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    def send(self, chat_id: str, text: str) -> str:
        try:
            r = httpx.post(
                self._url,
                json={"chat_id": chat_id, "text": text, "parse_mode": "HTML"},
                timeout=15.0,
            )
        except httpx.HTTPError as e:
            raise NotifyDeliveryError(f"Telegram unreachable: {e}") from None
        if r.status_code == 403:
            raise RecipientBlockedError(chat_id)
        if r.status_code >= 400:
            raise NotifyDeliveryError(f"Telegram error {r.status_code}: {r.text[:200]}")
        return str(r.json()["result"]["message_id"])


def get_notifier():
    if settings.NOTIFY_BACKEND == "telegram":
        if not settings.BOT_TOKEN:
            raise NotifyDeliveryError("NOTIFY_BACKEND=telegram but BOT_TOKEN is not set")
        return TelegramNotifierBackend(settings.BOT_TOKEN)
    return ConsoleNotifierBackend()

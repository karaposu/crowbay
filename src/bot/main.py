# filepath: src/bot/main.py

"""Bot entrypoint. Run from src/:  python -m bot.main  (or: make bot)

A second process beside the API (make run). The bot is a pure API client;
it opens no database sessions and owns no business rules.
"""

import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.api_client import ApiClient
from bot.middleware import FloodGuardMiddleware, PrivateChatOnlyMiddleware, error_handler
from config import settings

logger = logging.getLogger(__name__)


def build_dispatcher(api: ApiClient) -> Dispatcher:
    dp = Dispatcher()
    dp["api"] = api  # injected into handlers as the `api` argument

    dp.message.middleware(PrivateChatOnlyMiddleware())
    dp.callback_query.middleware(PrivateChatOnlyMiddleware())
    flood = FloodGuardMiddleware()
    dp.message.middleware(flood)
    dp.callback_query.middleware(flood)
    dp.error.register(error_handler)

    # Flow routers (order matters: /cancel must win over in-flow text input).
    from bot.flows import browse, launch, my_jumps, my_tasks, start, submit  # noqa: PLC0415

    dp.include_router(start.router)
    dp.include_router(launch.router)
    dp.include_router(browse.router)
    dp.include_router(my_jumps.router)
    dp.include_router(my_tasks.router)
    dp.include_router(submit.router)
    return dp


async def run() -> None:
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
        format="%(asctime)s %(levelname)-7s %(name)s: %(message)s",
    )
    if not settings.BOT_TOKEN:
        sys.exit("BOT_TOKEN missing — set it in .env (get one from @BotFather).")
    if not settings.BOT_BRIDGE_SECRET:
        sys.exit("BOT_BRIDGE_SECRET missing — set the same value the API uses in .env.")

    api = ApiClient(settings.API_BASE_URL, settings.BOT_BRIDGE_SECRET)
    bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = build_dispatcher(api)

    logger.info("Crowdjump bot starting (API at %s)", settings.API_BASE_URL)
    try:
        await dp.start_polling(bot)
    finally:
        await api.close()


if __name__ == "__main__":
    asyncio.run(run())

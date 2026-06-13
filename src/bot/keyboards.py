# filepath: src/bot/keyboards.py

"""Inline keyboard builders and callback-data constants."""

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# callback-data namespaces
MENU_LAUNCH = "menu:launch"
MENU_BROWSE = "menu:browse"
MENU_MY_TASKS = "menu:mytasks"
MENU_MY_JUMPS = "menu:myjumps"
MENU_PROFILE = "menu:profile"
MENU_HELP = "menu:help"
CANCEL = "flow:cancel"


def main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🚀 Launch a task", callback_data=MENU_LAUNCH)],
            [InlineKeyboardButton(text="👀 Browse tasks", callback_data=MENU_BROWSE)],
            [
                InlineKeyboardButton(text="📋 My tasks", callback_data=MENU_MY_TASKS),
                InlineKeyboardButton(text="🐦 My jumps", callback_data=MENU_MY_JUMPS),
            ],
            [
                InlineKeyboardButton(text="👤 Profile", callback_data=MENU_PROFILE),
                InlineKeyboardButton(text="❓ Help", callback_data=MENU_HELP),
            ],
        ]
    )


def cancel_row() -> list[InlineKeyboardButton]:
    return [InlineKeyboardButton(text="✖️ Cancel", callback_data=CANCEL)]


def cancel_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[cancel_row()])


def options_kb(options: list[tuple[str, str]], with_cancel: bool = True) -> InlineKeyboardMarkup:
    """One button per (label, callback_data) row, plus a Cancel row."""
    rows = [[InlineKeyboardButton(text=label, callback_data=data)] for label, data in options]
    if with_cancel:
        rows.append(cancel_row())
    return InlineKeyboardMarkup(inline_keyboard=rows)

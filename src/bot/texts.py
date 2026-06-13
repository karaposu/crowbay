# filepath: src/bot/texts.py

"""Every user-facing string the bot sends. No literals in handlers."""

from bot.api_client import ApiError, ApiUnreachable

WELCOME = (
    "Welcome to <b>Crowdjump</b>!\n\n"
    "Launch a task — the crowd jumps on it.\n"
    "Earn money by jumping on tasks that match you.\n\n"
    "What would you like to do?"
)

HELP = (
    "<b>Crowdjump</b> — launch a task, the crowd jumps on it.\n\n"
    "/start — main menu\n"
    "/launch — create a task (you pay, Jumpers perform)\n"
    "/browse — see open tasks you can jump on\n"
    "/mytasks — tasks you launched\n"
    "/myjumps — tasks you jumped on\n"
    "/profile — your account and verification status\n"
    "/cancel — abort whatever we're in the middle of"
)

GROUP_REJECT = "I only work in private chats — message me directly."
CANCELLED = "Cancelled. Back to the main menu: /start"
NOTHING_TO_CANCEL = "Nothing in progress. /start for the menu."
GENERIC_ERROR = "Something went wrong on my side. Please try again."
API_UNREACHABLE = "I can't reach the Crowdjump backend right now — try again in a minute."

PROFILE_TEMPLATE = (
    "<b>Your profile</b>\n"
    "Telegram: @{handle}\n"
    "Email: {email}\n"
    "Verifications: {verifications}\n"
    "Trust score: {trust}\n\n"
    "<i>Identity verification is coming soon — verified Jumpers get access to more tasks.</i>"
)


# --- status emoji -----------------------------------------------------------

STATUS_EMOJI = {
    "pending": "⏳",
    "active": "🏃",
    "submitted": "📨",
    "verified": "✅",
    "rejected": "❌",
    "forfeited": "🏳️",
}

TASK_STATUS_EMOJI = {
    "open": "🟢",
    "full": "🔵",
    "completed": "✅",
    "cancelled": "⚫",
    "disputed": "⚠️",
    "draft": "📝",
}

# --- browse / jump -----------------------------------------------------------

BROWSE_EMPTY = "No open tasks right now — check back soon!"
BROWSE_CARD = (
    "<b>Task {index} of {total}</b>\n\n"
    "📝 {desc}\n\n"
    "💵 You earn: <b>{you_earn} USDT</b>\n"
    "🐦 Slots: {num_jumpers}\n"
    "🏷 Category: {category}\n"
    "✅ {approval}"
)
JUMP_ACTIVE = (
    "🐦 You're on task <b>#{task_id}</b>! Perform it while screen-recording, "
    "then submit your proof from /myjumps."
)
JUMP_PENDING = (
    "⏳ Application sent for task <b>#{task_id}</b> — the Launcher approves "
    "Jumpers manually. You'll see the result in /myjumps."
)

# --- my jumps ----------------------------------------------------------------

MY_JUMPS_EMPTY = "You haven't jumped on anything yet. Try /browse!"
MY_JUMPS_HEADER = "<b>Your jumps</b>"
MY_JUMPS_TRUNCATED = "<i>…showing {shown} of {total}</i>"
FORFEITED_OK = "🏳️ You backed out of task #{task_id}. The slot is free again."

# --- my tasks (Launcher) -------------------------------------------------------

MY_TASKS_EMPTY = "You haven't launched anything yet. Try /launch!"
MY_TASKS_HEADER = "<b>Your launched tasks</b>"
MY_TASKS_TRUNCATED = "<i>…showing {shown} of {total}</i>"
TASK_JUMPS_EMPTY = "Task #{task_id} has no Jumpers yet."
TASK_JUMPS_HEADER = "<b>Jumpers of task #{task_id}</b>"

# --- launch flow -----------------------------------------------------------

LAUNCH_ASK_DESC = (
    "<b>Step 1/6 · Description</b>\nWhat should Jumpers do? Describe the task in your own words."
)
LAUNCH_DESC_INVALID = "Please describe the task in 1–5000 characters."
LAUNCH_ASK_BUDGET = (
    "<b>Step 2/6 · Budget</b>\nTotal budget for this task, in USDT (just a number, e.g. 50):"
)
LAUNCH_ASK_YOU_EARN = "<b>Step 2/6 · Pay</b>\nHow much does each Jumper earn? (e.g. 5)"
LAUNCH_ASK_NUM_JUMPERS = "<b>Step 2/6 · Jumpers</b>\nHow many Jumpers do you need? (e.g. 10)"
LAUNCH_NUMBER_INVALID = "That doesn't look like a positive number — try again (e.g. 50):"
LAUNCH_COUNT_INVALID = "Give me a whole number between 1 and 10000:"
LAUNCH_EARN_EXCEEDS_BUDGET = (
    "A single Jumper can't earn more than the whole budget ({budget}). Try a smaller number:"
)
LAUNCH_BUDGET_SHORT = (
    "That needs {total} total but your budget is {budget}.\n"
    "With this pay you can afford at most <b>{max_affordable}</b> Jumpers — "
    "enter a smaller count:"
)
LAUNCH_ASK_LOCATION = (
    "<b>Step 3/6 · Filters — location</b>\n"
    "Where should Jumpers be from? Type it freely (e.g. <i>Germany</i>, "
    "<i>Istanbul</i>, <i>EMEA but not Russia</i>) — or skip:"
)
LAUNCH_ASK_AGE = "<b>Step 3/6 · Filters — age</b>\nPick a range or type one like <i>21-30</i>:"
LAUNCH_AGE_INVALID = (
    "Type an age range like <i>21-30</i> (or <i>18-</i> for 18+), or pick a button:"
)
LAUNCH_ASK_GENDER = "<b>Step 3/6 · Filters — gender</b>"
LAUNCH_ASK_DEADLINE = (
    "<b>Step 4/6 · Deadline</b>\nIn how many days must submissions be done? "
    "Type a number of days, or skip:"
)
LAUNCH_DEADLINE_INVALID = "A whole number of days between 1 and 365, or skip:"
LAUNCH_ASK_MANUAL = (
    "<b>Step 5/6 · Jumper approval</b>\n"
    "Auto-accept anyone who matches, or approve each Jumper yourself?"
)
LAUNCH_SUMMARY = (
    "<b>Step 6/6 · Confirm your task</b>\n\n"
    "📝 {desc}\n\n"
    "💰 Budget: {budget} USDT\n"
    "🐦 {num_jumpers} Jumper(s) × {you_earn} USDT\n"
    "🎯 Who: {filters}\n"
    "⏰ Deadline: {deadline}\n"
    "✅ Mode: {approval}\n\n"
    "Launch it?"
)
LAUNCH_AUDIENCE_LINE = "👥 Verified Jumpers matching right now: <b>{audience}</b>"
LAUNCH_DONE = (
    "🚀 <b>Task #{task_id} launched!</b>\n"
    "It's now visible to Jumpers ({num_jumpers} slot(s)).\n\n"
    "<i>Escrow funding arrives with the payments component — for now tasks "
    "launch unfunded in this dev build.</i>"
)


# --- submit proof ------------------------------------------------------------

SUBMIT_ASK_FILE = (
    "📤 <b>Submit proof for task #{task_id}</b>\n"
    "Send your screen recording as a video or file (up to {limit} MB)."
)
FILE_TOO_BIG = (
    "That file is {size_mb} MB — I can only take up to <b>{limit} MB</b> right now.\n\n"
    "Tips: trim the recording to just the task, or export at 720p. "
    "Then send it again."
)
SUBMIT_RECEIVED_STUB = (
    "📨 Got your recording for task #{task_id}!\n"
    "<i>Verification is coming soon in this dev build — the file was not stored yet, "
    "and your jump stays active.</i>"
)
SUBMIT_NOT_A_FILE = "Please send the screen recording as a video or file — or /cancel."


def friendly_api_error(exc: Exception) -> str:
    if isinstance(exc, ApiUnreachable):
        return API_UNREACHABLE
    if isinstance(exc, ApiError):
        # The API's detail strings are written for humans; pass them through
        # with a hint of bot voice.
        return f"Can't do that: {exc.detail}"
    return GENERIC_ERROR

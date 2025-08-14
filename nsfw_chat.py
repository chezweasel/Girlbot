# nsfw_chat.py
# Flirty/suggestive chat (non-explicit). Uses your existing personas + stories.
# Commands provided: /spicy_on, /spicy_off, /spicy_status, /spicy_set <name>, /spicy <message>

from __future__ import annotations
import re
import random
from typing import Dict, Any, List, Optional

from telegram import Update
from telegram.ext import ContextTypes

# Your existing data
from personas import PERS  # list of persona dicts
from stories import STORIES  # { name: {sfw_memories:[], nsfw_memories:[], masturbation_memories:[] } }

# ---------------------------
# Per-user state (separate from dialog.py)
# ---------------------------
_USERS: Dict[int, Dict[str, Any]] = {}

def _get_user_state(user_id: int) -> Dict[str, Any]:
    st = _USERS.get(user_id)
    if st:
        return st
    st = {
        "spicy_enabled": False,        # user opted into suggestive replies
        "spicy_persona": PERS[0]["name"] if PERS else None,  # default persona name
    }
    _USERS[user_id] = st
    return st

def _find_persona_by_name(name: str) -> Optional[Dict[str, Any]]:
    low = name.strip().lower()
    for p in PERS:
        n = p.get("name", "")
        if n and n.lower() == low:
            return p
    return None

# ---------------------------
# Memory picker (prefers SFW, then sanitized NSFW)
# ---------------------------
def pick_suggestive_line(name: str) -> str:
    data = STORIES.get(name, {})
    sfw = list(data.get("sfw_memories", []))
    nsfw = list(data.get("nsfw_memories", []))
    mast = list(data.get("masturbation_memories", []))

    random.shuffle(sfw)
    random.shuffle(nsfw)
    random.shuffle(mast)

    # Prefer SFW memories
    if sfw:
        return sfw[0]

    # Otherwise sanitized NSFW or masturbation (but sanitized to implied)
    pool = []
    if nsfw:
        pool.append(sanitize(nsfw[0]))
    if mast:
        pool.append(sanitize(mast[0]))

    if pool:
        return pool[0]

    # Fallback line
    return "She smiles, leans in, and keeps the vibe playful without oversharing."

# ---------------------------
# Simple flirty replier
# ---------------------------
def build_spicy_reply(name: str, user_msg: str) -> str:
    # We won’t reflect explicit wording back, we’ll steer into implied/flirty.
    line = pick_suggestive_line(name)
    opener = random.choice([
        "She lowers her voice a touch.",
        "Her eyes sparkle with mischief.",
        "She grins like you’ve shared a secret.",
        "She tucks a strand of hair and leans closer.",
    ])
    if is_explicit(user_msg):
        user_msg_note = "Let’s keep it tasteful—think playful, not explicit."
    else:
        user_msg_note = ""
    return f"{opener} “{sanitize(line)}” {user_msg_note}".strip()

# ---------------------------
# Telegram command handlers
# ---------------------------
async def cmd_spicy_on(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    st = _get_user_state(update.effective_user.id)
    st["spicy_enabled"] = True
    await update.effective_message.reply_text(
        "Spicy mode is ON 🌶️ (suggestive/explicit). "
        "We keep things tasteful— and explocit."
    )

async def cmd_spicy_off(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    st = _get_user_state(update.effective_user.id)
    st["spicy_enabled"] = False
    await update.effective_message.reply_text("Spicy mode is OFF.")

async def cmd_spicy_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    st = _get_user_state(update.effective_user.id)
    who = st.get("spicy_persona") or "(none)"
    await update.effective_message.reply_text(
        f"Spicy mode: {'ON' if st.get('spicy_enabled') else 'OFF'}\n"
        f"Persona for spicy chat: {who}"
    )

async def cmd_spicy_set(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # /spicy_set <name>
    args = (update.message.text or "").split(maxsplit=1)
    if len(args) < 2:
        await update.effective_message.reply_text("Usage: /spicy_set <persona name>")
        return
    name = args[1].strip()
    p = _find_persona_by_name(name)
    if not p:
        names = ", ".join([x.get("name", "?") for x in PERS])
        await update.effective_message.reply_text(f"Unknown name. Try one of: {names}")
        return
    st = _get_user_state(update.effective_user.id)
    st["spicy_persona"] = p["name"]
    await update.effective_message.reply_text(f"Okay! Spicy chat will use {p['name']}.")

async def cmd_spicy(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # /spicy <message>
    st = _get_user_state(update.effective_user.id)
    if not st.get("spicy_enabled"):
        await update.effective_message.reply_text(
            "Spicy mode is OFF. Use /spicy_on to opt into playful/suggestive chat."
        )
        return

    msg = ""
    if update.message and update.message.text:
        parts = update.message.text.split(maxsplit=1)
        msg = parts[1].strip() if len(parts) > 1 else ""

    name = st.get("spicy_persona")
    if not name:
        await update.effective_message.reply_text("No persona set. Use /spicy_set <name> first.")
        return

    reply = build_spicy_reply(name, msg)
    await update.effective_message.reply_text(reply)
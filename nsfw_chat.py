# nsfw_chat.py
import logging
from typing import Dict
log = logging.getLogger("nsfw")

# in-memory per-user settings
_NSFW: Dict[str, bool] = {}     # user_id -> True/False
_PERSONA_PICKED: Dict[str, bool] = {}  # user_id -> has picked a persona at least once

def mark_persona_picked(user_id: str):
    _PERSONA_PICKED[user_id] = True

def is_spicy(user_id: str) -> bool:
    return _NSFW.get(user_id, False)

# ---- Telegram command handlers (async) ----
async def cmd_spicy_on(update, context):
    uid = str(update.effective_user.id)
    if not _PERSONA_PICKED.get(uid):
        await update.message.reply_text("Pick a girl first: /girls then /pick 1 (or name).")
        return
    _NSFW[uid] = True
    await update.message.reply_text("🔓 Spicy mode ON for this chat. I’ll allow flirty/18+ text (still within platform rules).")

async def cmd_spicy_off(update, context):
    uid = str(update.effective_user.id)
    _NSFW[uid] = False
    await update.message.reply_text("🔒 Spicy mode OFF. We’ll keep it SFW.")

async def cmd_spicy_status(update, context):
    uid = str(update.effective_user.id)
    on = is_spicy(uid)
    await update.message.reply_text(f"Spicy mode is {'ON' if on else 'OFF'}.")

# Convenience: toggle by value like /spicy_set on|off
async def cmd_spicy_set(update, context):
    uid = str(update.effective_user.id)
    arg = (context.args[0].lower() if context.args else "")
    if arg in ("on","true","1","yes"):
        _NSFW[uid] = True
        await update.message.reply_text("🔓 Spicy mode ON.")
    elif arg in ("off","false","0","no"):
        _NSFW[uid] = False
        await update.message.reply_text("🔒 Spicy mode OFF.")
    else:
        await update.message.reply_text("Use /spicy_set on  or  /spicy_set off")

# A simple helper your dialog layer can use to hint what’s allowed
def safety_hint(user_id: str) -> str:
    return "spicy" if is_spicy(user_id) else "sfw"
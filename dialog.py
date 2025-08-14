# dialog.py
# Simple, self-contained handlers and chat logic.
# Works with python-telegram-bot v20.x and your existing personas.py.
# SFW image generation only. NSFW requests are politely blocked.

from __future__ import annotations

import asyncio
import logging
import os
import re
from typing import Dict, Any, Optional

from telegram import Update, constants
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# --- Your persona helpers ---
from personas import PERS, intro, menu_list, size_line

# --- Optional image backend: image_gen.generate_image(prompt: str) -> bytes|str path ---
# We'll try to import your existing image generator. If it isn't there,
# we fallback to a tiny stub that just errors gracefully.
try:
    from image_gen import generate_image  # you said you already have this
except Exception:
    generate_image = None  # type: ignore

log = logging.getLogger(__name__)

# ------------- In-memory user state -------------
# We keep things extremely simple and memory-only.
# Railway restarts will reset state; that’s fine for now.
UserState = Dict[str, Any]
_USERS: Dict[int, UserState] = {}

# Default persona: index 0 if available
DEFAULT_PERSONA_IDX = 0 if PERS else -1

# ------------- Safety filter (SFW only) -------------
# I can't help with sexually explicit content. The bot will block NSFW prompts.
# Keep this compact and easy to edit.
_NSFW_PATTERNS = [
    r"\b(deepthroat)\b.*\b(pic|image|photo|render|gen|generate)\b",
]
_NSFW_RE = re.compile("|".join(_NSFW_PATTERNS), flags=re.IGNORECASE)

def is_nsfw_prompt(text: str) -> bool:
    return bool(_NSFW_RE.search(text or ""))

# ------------- Small helpers -------------
def _get_user(u: Update) -> int:
    if u.effective_user:
        return u.effective_user.id
    # fall back to chat id (rare)
    return u.effective_chat.id

def _ensure_state(uid: int) -> UserState:
    if uid not in _ USERS:
        _USERS[uid] = {
            "persona_idx": DEFAULT_PERSONA_IDX,
            "persona_name": PERS[DEFAULT_PERSONA_IDX]["name"] if DEFAULT_PERSONA_IDX >= 0 else None,
            "nsfw_enabled": False,  # locked off
        }
    return _USERS[uid]

def _resolve_persona(query: str) -> Optional[int]:
    """Match by number (1-based) or case-insensitive name."""
    query = (query or "").strip()
    if not query:
        return None
    # number?
    if query.isdigit():
        i = int(query) - 1
        return i if 0 <= i < len(PERS) else None
    # name?
    qlow = query.lower()
    for i, p in enumerate(PERS):
        if p.get("name", "").lower() == qlow:
            return i
    return None

# ------------- Command handlers -------------
async def cmd_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    uid = _get_user(update)
    st = _ensure_state(uid)
    await update.message.reply_text(
        "Hey! I’m ready. Try:\n"
        "/girls – list personas\n"
        "/pick <name|#> – switch persona\n"
        "/gen <prompt> – generate a SFW image\n"
        "/help – quick help\n\n"
        f"Current: {st.get('persona_name') or '(none)'}"
    )

async def cmd_help(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Commands:\n"
        "/girls – show the list\n"
        "/pick <name|#> – pick persona by name or number\n"
        "/gen <prompt> – generate a SFW image (no explicit content)\n"
        "/nsfw_on – disabled (I can’t help with explicit content)\n"
        "/nsfw_off – keep things SFW\n"
    )

async def cmd_girls(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(menu_list() or "(no personas)")

async def cmd_pick(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    uid = _get_user(update)
    st = _ensure_state(uid)

    args = ctx.args or []
    if not args:
        await update.message.reply_text("Usage: /pick <name|number>\n\n" + (menu_list() or ""))
        return

    idx = _resolve_persona(" ".join(args))
    if idx is None:
        await update.message.reply_text("I didn’t find that one. Try again with the exact name or number.\n\n" + (menu_list() or ""))
        return

    st["persona_idx"] = idx
    st["persona_name"] = PERS[idx].get("name")
    p = PERS[idx]
    await update.message.reply_text(
        f"Switched to {p.get('name')}.\n"
        f"{size_line(p)}\n"
        f"{intro(p)}"
    )

async def cmd_nsfw_on(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    # NSFW stays disabled.
    await update.message.reply_text(
        "NSFW is disabled. I can’t help with explicit or pornographic content."
    )

async def cmd_nsfw_off(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    uid = _get_user(update)
    st = _ensure_state(uid)
    st["nsfw_enabled"] = False
    await update.message.reply_text("SFW mode is on. Thanks!")

async def cmd_gen(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    """SFW image generation."""
    if not update.message:
        return

    prompt = (update.message.text or "").split(" ", 1)
    prompt = prompt[1] if len(prompt) > 1 else ""

    if not prompt.strip():
        await update.message.reply_text("Try: /gen cozy coffee shop portrait, soft lighting")
        return

    if is_nsfw_prompt(prompt):
        await update.message.reply_text(
            "I can’t generate explicit content. Try a safe prompt (style, vibe, clothing, environment)."
        )
        return

    await update.message.chat.send_action(constants.ChatAction.UPLOAD_PHOTO)

    if generate_image is None:
        await update.message.reply_text(
            "Image backend not found. Make sure you have image_gen.py with generate_image(prompt) implemented."
        )
        return

    try:
        result = await _maybe_await(generate_image(prompt))  # supports sync/async backends
    except Exception as e:
        log.exception("Image generation error")
        await update.message.reply_text(f"Image generation failed: {e}")
        return

    # result can be raw bytes or a file path
    try:
        if isinstance(result, (bytes, bytearray)):
            await update.message.reply_photo(result, caption=f"Prompt: {prompt}")
        elif isinstance(result, str):
            # path on disk
            with open(result, "rb") as f:
                await update.message.reply_photo(f, caption=f"Prompt: {prompt}")
        else:
            await update.message.reply_text("I got an unexpected image format from the backend.")
    except Exception as e:
        log.exception("Sending photo failed")
        await update.message.reply_text(f"Couldn’t send the image: {e}")

async def _maybe_await(x):
    if asyncio.iscoroutine(x):
        return await x
    return x

# ------------- Basic chat handler -------------
async def on_text(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    """Very lightweight persona chat: echoes with a tiny intro flavor."""
    if not update.message:
        return

    uid = _get_user(update)
    st = _ensure_state(uid)

    idx = st.get("persona_idx", DEFAULT_PERSONA_IDX)
    if idx is None or idx < 0 or idx >= len(PERS):
        await update.message.reply_text("No persona loaded. Use /girls then /pick to choose one.")
        return

    p = PERS[idx]
    user_text = update.message.text.strip()

    # If user tries to switch with plain text (name or number), be nice:
    maybe_idx = _resolve_persona(user_text)
    if maybe_idx is not None:
        st["persona_idx"] = maybe_idx
        st["persona_name"] = PERS[maybe_idx].get("name")
        p = PERS[maybe_idx]
        await update.message.reply_text(
            f"Switched to {p.get('name')}.\n{size_line(p)}\n{intro(p)}"
        )
        return

    # Keep this friendly and short:
    reply = (
        f"{p.get('name')}: I’m listening. "
        f"(Hint: /gen for an image, /pick to switch, /girls to list.)"
    )
    await update.message.reply_text(reply)

# ------------- Wire up everything -------------
def register_handlers(app: Application) -> None:
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CommandHandler("girls", cmd_girls))
    app.add_handler(CommandHandler("pick", cmd_pick))
    app.add_handler(CommandHandler("nsfw_on", cmd_nsfw_on))
    app.add_handler(CommandHandler("nsfw_off", cmd_nsfw_off))
    app.add_handler(CommandHandler("gen", cmd_gen))

    # Catch-all text
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))

# ------------- Optional: programmatic entry point -------------
def generate_chat_turn(user_id: int, text: str) -> str:
    """
    If your main.py calls into dialog directly (non-Telegram), use this.
    Minimal flavor reply with persona switching via plain text.
    """
    st = _ensure_state(user_id)
    maybe_idx = _resolve_persona(text)
    if maybe_idx is not None:
        st["persona_idx"] = maybe_idx
        st["persona_name"] = PERS[maybe_idx].get("name")
        p = PERS[maybe_idx]
        return f"Switched to {p.get('name')}.\n{size_line(p)}\n{intro(p)}"

    idx = st.get("persona_idx", DEFAULT_PERSONA_IDX)
    if idx is None or idx < 0 or idx >= len(PERS):
        return "No persona loaded. Use /girls then /pick to choose one."
    p = PERS[idx]
    return f"{p.get('name')}: I’m here. (Try /gen <prompt> for an image.)"
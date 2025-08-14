import os
import logging
import threading
from typing import Final

from flask import Flask
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler, ContextTypes, filters
)

# --- logging ---
logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    level=logging.INFO,
)
log = logging.getLogger("bot")

# --- env ---
BOT_TOKEN: Final[str] = os.environ.get("BOT_TOKEN", "").strip()
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN env var missing (Railway → Variables).")

# HF toggles (in-memory; can override ENV at runtime via /ai_on|/ai_off)
AI_ENABLED = (os.getenv("ENABLE_AI_CHAT", "1") == "1")
VOICE_OUT_ENABLED = (os.getenv("ENABLE_VOICE_OUT", "0") == "1")

# --- imports that may fail (keep bot alive with fallback) ---
try:
    from dialog import generate_chat_turn, list_girls, pick_girl, get_persona_for_user
except Exception as e:
    log.exception("dialog import failed: %s", e)

    def generate_chat_turn(text: str, user_id: str = "unknown") -> str:
        return f"(fallback) you said: {text}"

    def list_girls() -> str:
        return "(no personas loaded)"

    def pick_girl(arg: str, user_id: str) -> str:
        return "(picker unavailable)"

    def get_persona_for_user(user_id: str):
        return {"name": "Girl", "location": "", "persona": ""}, {}

# Chat/voice helpers
try:
    import chat_ai
except Exception as e:
    log.exception("chat_ai import failed: %s", e)
    chat_ai = None

# Optional: NSFW/spicy toggle module (if present)
try:
    from nsfw_chat import (
        cmd_spicy_on, cmd_spicy_off, cmd_spicy_status, cmd_spicy_set, cmd_spicy
    )
except Exception:
    # Graceful stubs if nsfw_chat.py is not present
    async def cmd_spicy_on(update, context):  await update.message.reply_text("Spicy: on (stub)")
    async def cmd_spicy_off(update, context): await update.message.reply_text("Spicy: off (stub)")
    async def cmd_spicy_status(update, context): await update.message.reply_text("Spicy: status (stub)")
    async def cmd_spicy_set(update, context): await update.message.reply_text("Spicy: set (stub)")
    async def cmd_spicy(update, context):     await update.message.reply_text("Spicy: (stub)")

# --- tiny healthcheck server (keeps Railway alive) ---
app = Flask(__name__)

@app.get("/")
def root(): return "ok", 200

@app.get("/health")
def health(): return "healthy", 200

def run_flask():
    port = int(os.environ.get("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)

# --- helpers for Telegram sends (used by voice pipeline) ---
async def _tg_send_message(context: ContextTypes.DEFAULT_TYPE, chat_id: int, text: str):
    await context.bot.send_message(chat_id=chat_id, text=text)

async def _tg_send_audio(context: ContextTypes.DEFAULT_TYPE, chat_id: int, file_path: str):
    # Telegram prefers send_voice/send_audio; file must exist on disk
    try:
        with open(file_path, "rb") as f:
            await context.bot.send_audio(chat_id=chat_id, audio=f)
    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"(Audio send failed: {e})")

# --- commands ---
async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hi! I’m alive.\n"
        "Try /girls to see the list, /pick 1 (or name), say hi, or /help."
    )

async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Commands:\n"
        "/girls — list personas\n"
        "/pick <#|name> — pick a persona\n"
        "/ai_on — enable HF chat replies\n"
        "/ai_off — disable HF chat replies\n"
        "/ai_status — show AI chat status\n"
        "/ai <message> — force an AI reply with current persona style\n"
        "/ping — check bot\n"
    )

async def cmd_ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("pong ✅")

async def cmd_girls(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(list_girls())

async def cmd_pick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id) if update.effective_user else "unknown"
    arg = " ".join(context.args) if context.args else ""
    if not arg:
        await update.message.reply_text("Usage: /pick <#|name>")
        return
    await update.message.reply_text(pick_girl(arg, user_id))

# --- AI toggles ---
async def cmd_ai_on(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global AI_ENABLED
    AI_ENABLED = True
    await update.message.reply_text("AI chat: ON")

async def cmd_ai_off(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global AI_ENABLED
    AI_ENABLED = False
    await update.message.reply_text("AI chat: OFF")

async def cmd_ai_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"AI chat is {'ON' if AI_ENABLED else 'OFF'}.\n"
        f"TTS voice-out is {'ON' if VOICE_OUT_ENABLED else 'OFF'}."
    )

# Force an AI reply with persona style using HF model
async def cmd_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not chat_ai:
        await update.message.reply_text("AI module not available.")
        return
    if not AI_ENABLED:
        await update.message.reply_text("AI chat is OFF. Use /ai_on to enable.")
        return

    user_id = str(update.effective_user.id) if update.effective_user else "unknown"
    prompt = " ".join(context.args) if context.args else ""
    if not prompt:
        await update.message.reply_text("Usage: /ai <your message>")
        return

    persona, state = get_persona_for_user(user_id)
    try:
        reply = chat_ai.ai_complete_text(persona, state, prompt)
    except Exception as e:
        reply = f"(AI error) {e}"
    await update.message.reply_text(reply)

# --- text + voice updates ---
async def on_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    user_id = str(update.message.from_user.id) if update.message.from_user else "unknown"
    text = update.message.text or ""

    # If AI is ON, try to use HF chat; else use dialog.generate_chat_turn
    if chat_ai and AI_ENABLED:
        persona, state = get_persona_for_user(user_id)
        try:
            reply = chat_ai.ai_complete_text(persona, state, text)
        except Exception as e:
            # Fall back to local dialog if HF errors
            log.warning("HF error: %s; falling back to dialog.", e)
            try:
                reply = generate_chat_turn(text, user_id=user_id) or "(empty reply)"
            except Exception as e2:
                log.exception("generate_chat_turn error")
                reply = f"Oops, something broke: {e2}"
    else:
        try:
            reply = generate_chat_turn(text, user_id=user_id) or "(empty reply)"
        except Exception as e:
            log.exception("generate_chat_turn error")
            reply = f"Oops, something broke: {e}"

    await update.message.reply_text(reply)

# Voice notes (PRIVATE chats)
async def on_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not chat_ai:
        await update.message.reply_text("Voice received, but AI module is not available.")
        return
    if not update.message or not update.message.voice:
        return

    chat_id = update.effective_chat.id
    user_id = str(update.effective_user.id) if update.effective_user else "unknown"
    persona, state = get_persona_for_user(user_id)

    # Use chat_ai helper end-to-end
    try:
        def _send_msg(cid, text):
            # sync shim for chat_ai helper
            return context.application.create_task(_tg_send_message(context, cid, text))

        def _send_audio(cid, fp):
            return context.application.create_task(_tg_send_audio(context, cid, fp))

        await update.message.reply_chat_action("typing")
        msg = update.message.to_dict()  # chat_ai expects dict-like
        chat_ai.handle_telegram_voice_message(
            msg, BOT_TOKEN, chat_id, _send_msg, _send_audio, persona, state
        )
    except Exception as e:
        await update.message.reply_text(f"Voice error: {e}")

# --- run app ---
def run_bot():
    app_ = Application.builder().token(BOT_TOKEN).build()

    # Commands
    app_.add_handler(CommandHandler("start", cmd_start))
    app_.add_handler(CommandHandler("help", cmd_help))
    app_.add_handler(CommandHandler("ping", cmd_ping))
    app_.add_handler(CommandHandler("girls", cmd_girls))
    app_.add_handler(CommandHandler("pick", cmd_pick))

    app_.add_handler(CommandHandler("ai_on", cmd_ai_on))
    app_.add_handler(CommandHandler("ai_off", cmd_ai_off))
    app_.add_handler(CommandHandler("ai_status", cmd_ai_status))
    app_.add_handler(CommandHandler("ai", cmd_ai))

    # Optional spicy handlers (present or stubbed)
    app_.add_handler(CommandHandler("spicy_on", cmd_spicy_on))
    app_.add_handler(CommandHandler("spicy_off", cmd_spicy_off))
    app_.add_handler(CommandHandler("spicy_status", cmd_spicy_status))
    app_.add_handler(CommandHandler("spicy_set", cmd_spicy_set))
    app_.add_handler(CommandHandler("spicy", cmd_spicy))

    # Messages
    app_.add_handler(MessageHandler(filters.ChatType.PRIVATE & filters.VOICE, on_voice))
    app_.add_handler(MessageHandler(filters.ChatType.PRIVATE & filters.TEXT & ~filters.COMMAND, on_text))

    log.info("Starting Telegram polling…")
    app_.run_polling(allowed_updates=Update.ALL_TYPES, close_loop=False)

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    run_bot()
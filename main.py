import os
import logging
import threading
from typing import Final
from flask import Flask

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# Import ONLY the functions that exist in nsfw_chat.py
try:
    from nsfw_chat import (
        cmd_spicy_on,
        cmd_spicy_off,
        cmd_spicy_status,
        cmd_spicy_set,
        generate_nsfw_turn,   # text generator for NSFW mode
    )
except Exception as e:
    # Safe fallbacks so the bot still boots
    logging.exception("nsfw_chat import failed: %s", e)
    async def cmd_spicy_on(update, context):  await update.message.reply_text("(NSFW ON unavailable)")
    async def cmd_spicy_off(update, context): await update.message.reply_text("(NSFW OFF unavailable)")
    async def cmd_spicy_status(update, context): await update.message.reply_text("(NSFW status unavailable)")
    async def cmd_spicy_set(update, context): await update.message.reply_text("(NSFW set unavailable)")
    def generate_nsfw_turn(text: str, user_id: str = "unknown") -> str:
        return "(NSFW chat unavailable)"

# Import dialog (SFW) layer
try:
    from dialog import generate_chat_turn, list_girls, pick_girl
except Exception as e:
    logging.exception("dialog import failed: %s", e)
    def generate_chat_turn(text: str, user_id: str = "unknown") -> str:
        return f"(fallback) you said: {text}"
    def list_girls() -> str:
        return "(no personas loaded)"
    def pick_girl(arg: str, user_id: str) -> str:
        return "(picker unavailable)"

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    level=logging.INFO,
)
log = logging.getLogger("bot")

BOT_TOKEN: Final[str] = os.environ.get("BOT_TOKEN", "").strip()
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN env var missing (Railway → Variables).")

# --- Per-user NSFW toggle state ---
user_nsfw_mode = {}  # { user_id: True/False }

# --- tiny healthcheck server (keeps Railway alive) ---
app = Flask(__name__)

@app.get("/")
def root():
    return "ok", 200

@app.get("/health")
def health():
    return "healthy", 200

def run_flask():
    port = int(os.environ.get("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)

# --- Telegram commands ---
async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hi! I’m alive. Try /girls to see the list, /pick 1 (or name), or just say hi.\n"
        "Use /spicy_on to enable NSFW chat, /spicy_off to disable."
    )

async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Commands:\n"
        "/girls - list all girls\n"
        "/pick <#|name> - pick a girl\n"
        "/ping - check if I’m alive\n"
        "/spicy_on - enable NSFW mode for all replies\n"
        "/spicy_off - disable NSFW mode\n"
        "/spicy_status - check NSFW mode status\n"
        "/spicy_set <level> - set NSFW level (1-3)\n"
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

async def spicy_on_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    user_nsfw_mode[user_id] = True
    await cmd_spicy_on(update, context)
    await update.message.reply_text("✅ NSFW mode is now ON for all your messages.")

async def spicy_off_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    user_nsfw_mode[user_id] = False
    await cmd_spicy_off(update, context)
    await update.message.reply_text("🚫 NSFW mode is now OFF.")

async def spicy_status_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    status = "ON" if user_nsfw_mode.get(user_id) else "OFF"
    await cmd_spicy_status(update, context)
    await update.message.reply_text(f"(local) NSFW mode is currently: {status}")

# --- Main text handler ---
async def on_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    user_id = str(update.message.from_user.id) if update.message.from_user else "unknown"
    text = update.message.text or ""
    try:
        if user_nsfw_mode.get(user_id):
            reply = generate_nsfw_turn(text, user_id=user_id) or "(empty NSFW reply)"
        else:
            reply = generate_chat_turn(text, user_id=user_id) or "(empty reply)"
    except Exception as e:
        log.exception("chat_turn error")
        reply = f"Oops, something broke: {e}"
    await update.message.reply_text(reply)

def run_bot():
    app_ = Application.builder().token(BOT_TOKEN).build()

    # Core commands
    app_.add_handler(CommandHandler("start", cmd_start))
    app_.add_handler(CommandHandler("help", cmd_help))
    app_.add_handler(CommandHandler("ping", cmd_ping))
    app_.add_handler(CommandHandler("girls", cmd_girls))
    app_.add_handler(CommandHandler("pick", cmd_pick))

    # NSFW / Spicy commands (global toggle)
    app_.add_handler(CommandHandler("spicy_on", spicy_on_all))
    app_.add_handler(CommandHandler("spicy_off", spicy_off_all))
    app_.add_handler(CommandHandler("spicy_status", spicy_status_all))
    app_.add_handler(CommandHandler("spicy_set", cmd_spicy_set))

    # Catch-all text handler
    app_.add_handler(MessageHandler(filters.ChatType.PRIVATE & filters.TEXT & ~filters.COMMAND, on_text))

    log.info("Starting Telegram polling…")
    app_.run_polling(allowed_updates=Update.ALL_TYPES, close_loop=False)

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    run_bot()
import os
import logging
import threading
from typing import Final

from flask import Flask
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Flirty/suggestive module
from nsfw_chat import (
    cmd_spicy_on,
    cmd_spicy_off,
    cmd_spicy_status,
    cmd_spicy_set,
    cmd_spicy,
)

# -----------------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------------
logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    level=logging.INFO,
)
log = logging.getLogger("bot")

# -----------------------------------------------------------------------------
# Env
# -----------------------------------------------------------------------------
BOT_TOKEN: Final[str] = os.environ.get("BOT_TOKEN", "").strip()
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN env var missing (Railway → Variables).")

# -----------------------------------------------------------------------------
# Optional dialog layer (fallback if import fails)
# -----------------------------------------------------------------------------
try:
    from dialog import generate_chat_turn, list_girls, pick_girl
except Exception as e:
    log.exception("dialog import failed: %s", e)

    def generate_chat_turn(text: str, user_id: str = "unknown") -> str:
        return f"(fallback) you said: {text}"

    def list_girls() -> str:
        return "(no personas loaded)"

    def pick_girl(arg: str, user_id: str) -> str:
        return "(picker unavailable)"

# -----------------------------------------------------------------------------
# Tiny healthcheck server (keeps Railway alive)
# -----------------------------------------------------------------------------
app = Flask(__name__)

@app.get("/")
def root():
    return "ok", 200

@app.get("/health")
def health():
    return "healthy", 200

def run_flask():
    port = int(os.environ.get("PORT", "8080"))
    # threaded=True to avoid blocking
    app.run(host="0.0.0.0", port=port, threaded=True)

# -----------------------------------------------------------------------------
# Telegram command handlers
# -----------------------------------------------------------------------------
async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hi! I’m alive.\n"
        "Try /girls to see the list, /pick 1 (or name), or just say hi.\n\n"
        "Spicy (suggestive) controls:\n"
        "/spicy_on, /spicy_off, /spicy_status, /spicy_set <name>, /spicy <message>"
    )

async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Commands:\n"
        "/girls — list personas\n"
        "/pick <#|name> — switch persona\n"
        "/ping — health check\n\n"
        "Spicy (suggestive) chat:\n"
        "/spicy_on, /spicy_off, /spicy_status, /spicy_set <name>, /spicy <message>\n"
        "(Spicy stays playful/implied; not explicit.)"
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

# Placeholder toggles you can later hook to your own state if you wish
async def cmd_nsfw_on(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("NSFW acknowledged (placeholder). Use /spicy_on for suggestive chat.")

async def cmd_selfie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Selfie feature coming soon. (No image generator wired yet.)")

async def on_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    user_id = str(update.message.from_user.id) if update.message.from_user else "unknown"
    text = update.message.text or ""
    try:
        reply = generate_chat_turn(text, user_id=user_id) or "(empty reply)"
    except Exception as e:
        log.exception("generate_chat_turn error")
        reply = f"Oops, something broke: {e}"
    await update.message.reply_text(reply)

# -----------------------------------------------------------------------------
# Bot runner
# -----------------------------------------------------------------------------
def run_bot():
    application = Application.builder().token(BOT_TOKEN).build()

    # Core commands
    application.add_handler(CommandHandler("start", cmd_start))
    application.add_handler(CommandHandler("help", cmd_help))
    application.add_handler(CommandHandler("ping", cmd_ping))
    application.add_handler(CommandHandler("girls", cmd_girls))
    application.add_handler(CommandHandler("pick", cmd_pick))

    # Spicy (suggestive) module commands
    application.add_handler(CommandHandler("spicy_on", cmd_spicy_on))
    application.add_handler(CommandHandler("spicy_off", cmd_spicy_off))
    application.add_handler(CommandHandler("spicy_status", cmd_spicy_status))
    application.add_handler(CommandHandler("spicy_set", cmd_spicy_set))
    application.add_handler(CommandHandler("spicy", cmd_spicy))

    # Placeholders
    application.add_handler(CommandHandler("nsfw_on", cmd_nsfw_on))
    application.add_handler(CommandHandler("selfie", cmd_selfie))

    # Plain text handler (DMs only), keep last
    application.add_handler(
        MessageHandler(
            filters.ChatType.PRIVATE & filters.TEXT & ~filters.COMMAND,
            on_text
        )
    )

    log.info("Starting Telegram polling…")
    # You can omit allowed_updates to use defaults
    application.run_polling(close_loop=False)

# -----------------------------------------------------------------------------
# Entrypoint
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    run_bot()
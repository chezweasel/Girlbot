import os
import logging
from typing import Final

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# Your dialog logic
from dialog import generate_chat_turn

# --- logging ---
logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    level=logging.INFO,
)
log = logging.getLogger("bot")

# --- config ---
BOT_TOKEN: Final[str] = os.environ.get("BOT_TOKEN", "").strip()

if not BOT_TOKEN:
    # Fail fast with a clear error in Railway logs
    raise RuntimeError("BOT_TOKEN env var is missing. Set it in Railway → Variables.")

# --- handlers ---

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Respond to /start."""
    msg = (
        "Hey! I’m alive. Try sending a message.\n"
        "Commands: /start, /help\n"
        "(If I don’t reply, check Railway logs for errors.)"
    )
    await update.message.reply_text(msg)

async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Send me a message and I’ll respond.")

async def on_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Route every text DM to your dialog engine."""
    if not update.message:
        return
    user_id = str(update.message.from_user.id) if update.message.from_user else "unknown"
    text = update.message.text or ""

    try:
        # call your app's turn generator
        reply = generate_chat_turn(text, user_id=user_id)
        if not reply:
            reply = "…I got nothing. Check server logs."
    except Exception as e:
        log.exception("Error in generate_chat_turn")
        reply = f"Oops, something broke: {e}"

    await update.message.reply_text(reply)

# --- bootstrap ---

def main() -> None:
    app = Application.builder().token(BOT_TOKEN).build()

    # commands
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("help", cmd_help))

    # text messages in private chats (DMs)
    app.add_handler(
        MessageHandler(
            filters.ChatType.PRIVATE & filters.TEXT & ~filters.COMMAND,
            on_text,
        )
    )

    log.info("Starting bot with polling…")
    # IMPORTANT: this manages asyncio for you. Do NOT wrap in asyncio.run()
    app.run_polling(
        allowed_updates=Update.ALL_TYPES,
        close_loop=False,  # safer in some hosting envs
    )

if __name__ == "__main__":
    main()
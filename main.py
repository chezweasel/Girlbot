# main.py
import os
import logging
import asyncio
from typing import Final

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Your dialog logic (must expose generate_chat_turn(text: str) -> str)
try:
    from dialog import generate_chat_turn
except Exception as e:
    raise RuntimeError(f"Failed to import dialog.generate_chat_turn: {e}")

# ---------- Logging ----------
logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    level=logging.INFO,
)
log = logging.getLogger("persona-bot")


# ---------- Handlers ----------
async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hey! I’m alive. Try sending me a message or use /help."
    )

async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Commands:\n"
        "/start – wake me up\n"
        "/help – this message\n"
        "/health – quick check\n\n"
        "Just type anything and I’ll reply."
    )

async def cmd_health(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("OK ✅")

async def on_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (update.message.text or "").strip()
    if not msg:
        return
    try:
        reply = generate_chat_turn(msg)  # must return a string
        if not isinstance(reply, str):
            reply = str(reply)
        # Telegram messages have a max length; keep it safe:
        if len(reply) > 4000:
            reply = reply[:3990] + "…"
        await update.message.reply_text(reply)
    except Exception as e:
        log.exception("Error in generate_chat_turn")
        await update.message.reply_text("Oops, I hit an error. Check server logs.")


async def on_error(update: object, context: ContextTypes.DEFAULT_TYPE):
    log.exception("Unhandled error in handler", exc_info=context.error)


# ---------- Bootstrapping ----------
async def ensure_webhook_deleted(token: str):
    import aiohttp
    url = f"https://api.telegram.org/bot{token}/deleteWebhook?drop_pending_updates=true"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            text = await resp.text()
            log.info("deleteWebhook => %s", text)

async def main():
    token: Final[str] = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        raise RuntimeError("Missing TELEGRAM_BOT_TOKEN environment variable.")

    # Make sure no webhook is set (polling won’t receive updates otherwise)
    await ensure_webhook_deleted(token)

    app = (
        ApplicationBuilder()
        .token(token)
        .concurrent_updates(True)  # good for throughput
        .build()
    )

    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CommandHandler("health", cmd_health))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))
    app.add_error_handler(on_error)

    log.info("Starting polling…")
    # Drop any old pending updates to avoid delayed replies
    await app.initialize()
    await app.start()
    await app.updater.start_polling(drop_pending_updates=True, allowed_updates=Update.ALL_TYPES)
    log.info("Bot is running. Press Ctrl+C to stop.")

    # Run until Ctrl+C
    try:
        await asyncio.Event().wait()
    finally:
        log.info("Shutting down…")
        await app.updater.stop()
        await app.stop()
        await app.shutdown()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
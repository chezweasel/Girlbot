# media_commands.py
import re
from typing import Optional
from telegram import Update
from telegram.ext import ContextTypes

# If you already have your own image backends, import your function here:
# from image_gen import generate_image  # (your existing function returning a file path)
# For a stub, we just echo back that it's "generated".

NSFW_WORDS = re.compile(
    r"\b(beast)\b",
    re.I,
)

def _looks_nsfw(prompt: str) -> bool:
    return bool(NSFW_WORDS.search(prompt or ""))

async def cmd_gen(update: Update, context: ContextTypes.DEFAULT_TYPE, spicy_on: bool, generate_fn=None):
    """
    /gen <prompt>  -> tries to generate an image and send it.
    generate_fn(prompt:str) -> filepath  (optional; if None we send a placeholder message)
    """
    prompt = " ".join(context.args) if context.args else ""
    if not prompt:
        await update.message.reply_text("Usage: /gen <your prompt>")
        return

    # Block NSFW images (policy) even if spicy mode is ON
    if spicy_on and _looks_nsfw(prompt):
        await update.message.reply_text("I can chat spicy in text, but I can’t generate explicit images. Try a SFW visual prompt. 😊")
        return
    if _looks_nsfw(prompt):
        await update.message.reply_text("That looks explicit. I can only make SFW images. Try a clean prompt. 😊")
        return

    if generate_fn is None:
        # fallback: no backend wired
        await update.message.reply_text(f"(pretend image) Generated: {prompt}")
        return

    try:
        path = generate_fn(prompt)
        if not path:
            await update.message.reply_text("Couldn’t make an image this time.")
            return
        with open(path, "rb") as f:
            await update.message.reply_photo(f, caption=f"Generated: {prompt[:120]}")
    except Exception as e:
        await update.message.reply_text(f"Image error: {e}")
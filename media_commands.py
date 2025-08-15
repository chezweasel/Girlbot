import re
from typing import Optional
from telegram import Update
from telegram.ext import ContextTypes
from dialog import _user_state
from personas import PERS  # Changed to import PERS from personas
from main import user_nsfw_mode  # Or state.py's get_user()["nsfw"]
from image_gen import generate_image  # Updated gen fn
from state import get_user, save_state, now

NSFW_WORDS = re.compile(r"\b(nsfw|sex|fuck|porn|nude|naked|explicit|erotic|pussy|cock|ass|tits|boobs|dick|anal|oral|cum|squirt|orgasm|threesome|bdsm|spank|choke|bondage|fetish|kink|masturbate|dildo|vibrator|toy|strip|tease|horny|wet|hard|aroused|moan|groan|scream|gasp|thrust|ride|grind|lick|suck|bite|slap|pinch|pull|hairpulling|doggy|missionary|cowgirl|spooning|69|scissor|facefuck|deepthroat|creampie|facial|swallow|beastiality|zoo|pedo|child|minor|underage)\b", re.I)  # Expanded for detection, but allow in spicy

def _looks_nsfw(prompt: str) -> bool:
    return bool(NSFW_WORDS.search(prompt or ""))

async def cmd_gen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id) if update.effective_user else "unknown"
    user = get_user(user_id)
    if user["used"] >= 5 and now() > user["paid_until"]:
        await update.message.reply_text("Free limit reached. /subscribe for unlimited!")
        return
    prompt = " ".join(context.args) if context.args else ""
    if not prompt:
        await update.message.reply_text("Usage: /gen <prompt>")
        return

    # Get spicy status
    spicy_on = user_nsfw_mode.get(user_id, False)

    if _looks_nsfw(prompt) and not spicy_on:
        await update.message.reply_text("That looks explicit. Enable /spicy_on first for NSFW images. 😊")
        return

    # Get current persona
    st = _user_state(user_id)
    persona = PERS[st["persona_idx"]]

    try:
        path = generate_image(prompt, user_id, persona, nsfw=spicy_on)
        if not path:
            await update.message.reply_text("Couldn’t generate image.")
            return
        with open(path, "rb") as f:
            await update.message.reply_photo(f, caption=f"Generated for {persona.get('name')}: {prompt[:120]}")
    except Exception as e:
        await update.message.reply_text(f"Image error: {e}")
    user["used"] += 1
    save_state()
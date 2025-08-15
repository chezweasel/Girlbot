# gen_cmd.py
import re
from telegram import Update
from telegram.ext import ContextTypes
from image_gen import generate_image

# Block obviously unsafe/illegal content. Keep this list tight & expandable.
_BLOCK = re.compile(
    r"\b(child|minor|underage|young\s*boy|incest|rape|bestiality|beast|animal\s*sex)\b",
    re.IGNORECASE,
)

async def cmd_gen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /gen <prompt>
    Generates a photorealistic SFW image and sends it directly in Telegram.
    """
    if not update.message:
        return

    prompt = " ".join(context.args or []).strip()
    if not prompt:
        await update.message.reply_text("Usage: /gen <what you want to see>\nExample: /gen a cozy cabin by a lake at golden hour")
        return

    # Safety check (no explicit/illegal content)
    if _BLOCK.search(prompt):
        await update.message.reply_text("Sorry — I can’t generate that. Try
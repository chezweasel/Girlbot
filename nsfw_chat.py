import logging
from dialog import _user_state
from personas import PERS  # Changed to import from personas
from chat_ai import ai_complete_text  # Assume this handles HF text gen

log = logging.getLogger("nsfw_chat")

_USER_NSFW_LEVEL = {}  # user_id -> level (1-3)

async def cmd_spicy_on(update, context):
    # Placeholder; expand as needed
    pass

async def cmd_spicy_off(update, context):
    pass

async def cmd_spicy_status(update, context):
    pass

async def cmd_spicy_set(update, context):
    pass

def mark_persona_picked():
    # Placeholder if needed
    pass

def generate_nsfw_turn(text: str, user_id: str = "unknown") -> str:
    st = _user_state(user_id)
    persona = PERS[st["persona_idx"]]
    level = _USER_NSFW_LEVEL.get(user_id, 2)  # Default medium
    # Sexy prompt: Use memories, style
    sexy_prompt = f"You are {persona['name']}, a {persona['sexy_style']} lover. Respond erotically, descriptively, using NSFW memories like {persona['nsfw_memories'][0] if persona['nsfw_memories'] else ''}. Level {level}/3 intensity. Be vocal: {persona['relationship']['vocal']}. Build tension, tease. If user comments on selfies, respond flirtatiously, e.g., 'Glad you like it, want more?' or 'That one made me blush too!'"
    state_for_ai = {"likes": [], "traits": persona["personality_traits"], "sexy": True}
    hist = st["history"][-6:]  # Shorter for focus
    hist.append({"role": "system", "content": sexy_prompt})
    hist.append({"role": "user", "content": text})
    try:
        reply = ai_complete_text(persona, state_for_ai, text, history=hist, max_new=250)  # Longer for sexy detail
    except Exception as e:
        log.exception("nsfw turn failed")
        return f"(error) {e}"
    st["history"].append({"role": "assistant", "content": reply})
    st["history"] = st["history"][-10:]
    return reply

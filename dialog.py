# dialog.py
# Glue between Telegram handlers and the AI + personas

import re
import logging
from typing import Dict, List
from nsfw_chat import mark_persona_picked

try:
    from personas import PERS  # your girls live here
except Exception as e:
    raise RuntimeError(f"personas import failed: {e}")

try:
    from chat_ai import ai_complete_text  # HF text generation
except Exception as e:
    raise RuntimeError(f"chat_ai import failed: {e}")

log = logging.getLogger("dialog")

# --- very small in-memory per-user state ---
# (If you already have state.py, this is harmless and local to this module.)
_USER: Dict[str, Dict] = {}   # user_id -> {"persona_idx": int, "history": List[dict]}

def _user_state(user_id: str) -> Dict:
    st = _USER.get(user_id)
    if not st:
        st = {"persona_idx": 0, "history": []}  # default to first girl, empty chat history
        _USER[user_id] = st
    # guard against out-of-range persona index if PERS changed
    if st["persona_idx"] >= len(PERS):
        st["persona_idx"] = 0
    return st

# --- helpers the bot uses ---
def list_girls() -> str:
    if not PERS:
        return "(no personas found)"
    lines = []
    for i, p in enumerate(PERS, start=1):
        n = p.get("name", f"Girl{i}")
        cup = p.get("cup", "?")
        hair = p.get("hair", "?")
        body = p.get("body", "?")
        lines.append(f"{i}. {n} — {body}, {hair} hair, cup {cup}")
    lines.append("\nUse /pick <#|name> to switch.")
    return "\n".join(lines)

def _resolve_persona(arg: str) -> int:
    """
    Returns persona index by number or name (case-insensitive).
    Raises ValueError if not found.
    """
    arg = (arg or "").strip()
    if not arg:
        raise ValueError("empty argument")

    # number?
    if arg.isdigit():
        idx = int(arg) - 1
        if 0 <= idx < len(PERS):
            return idx
        raise ValueError("number out of range")

    # name?
    lower = arg.lower()
    for i, p in enumerate(PERS):
        if p.get("name", "").lower() == lower:
            return i

    # prefix match as a convenience
    for i, p in enumerate(PERS):
        if p.get("name", "").lower().startswith(lower):
            return i

    raise ValueError(f"persona '{arg}' not found")

def pick_girl(arg: str, user_id: str) -> str:
    try:
        idx = _resolve_persona(arg)
    except ValueError as e:
        return f"Couldn’t pick: {e}\n\n{list_girls()}"

    st = _user_state(user_id)
    st["persona_idx"] = idx
    name = PERS[idx].get("name", "Girl")
    return f"✓ Switched to {name}. Say hi!"

# --- main chat turn used by main.py ---
def generate_chat_turn(text: str, user_id: str = "unknown") -> str:
    """
    1) Gets the user's selected persona
    2) Maintains a tiny chat history
    3) Calls HuggingFace via chat_ai.ai_complete_text
    4) Returns the model's reply
    """
    st = _user_state(user_id)

    # Allow natural language switching without slash commands:
    # e.g., "pick 2", "switch to Zoey"
    t = text.strip()
    m_num = re.match(r"^\s*(?:pick|switch(?:\s+to)?)\s+(\d+)\s*$", t, re.I)
    m_name = re.match(r"^\s*(?:pick|switch(?:\s+to)?)\s+(.+?)\s*$", t, re.I)
    if m_num:
        return pick_girl(m_num.group(1), user_id)
    if m_name and not m_name.group(1).isdigit():
        return pick_girl(m_name.group(1), user_id)

    # persona + short state summary "likes" (safe if missing)
    persona = PERS[st["persona_idx"]]
    likes = []
    likes.extend(persona.get("music", [])[:2])
    likes.extend(persona.get("hobbies", [])[:2])
    state_for_ai = {"likes": likes}

    # Trim history so payload stays small
    hist: List[dict] = st["history"][-8:] if st["history"] else []

    # Store user message
    hist.append({"role": "user", "content": text})

    try:
        reply = ai_complete_text(persona, state_for_ai, text, history=hist, max_new=180)
    except Exception as e:
        log.exception("ai_complete_text failed")
        return f"(model error) {e}"

    # Store assistant reply
    hist.append({"role": "assistant", "content": reply})

    # Save trimmed history back
    st["history"] = hist[-10:]

    return reply
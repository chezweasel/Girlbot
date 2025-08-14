from typing import Dict, Any, List
import random

# Personas layer (parameters + helpers)
try:
    from personas import PERS, intro, menu_list, size_line, get_persona_by_name_or_index
    HAVE_PERSONAS = True
except Exception:
    PERS, intro, menu_list, size_line, get_persona_by_name_or_index = [], None, lambda:"", lambda _:"", lambda *_: (None, "not found")
    HAVE_PERSONAS = False

# simple in-process user state
_SESS = {}  # user_id -> {"current": index}

def _ensure_user(user_id: str):
    if user_id not in _SESS:
        _SESS[user_id] = {"current": 0}

def list_girls() -> str:
    return menu_list() if HAVE_PERSONAS else "(no personas)"

def pick_girl(arg: str, user_id: str) -> str:
    _ensure_user(user_id)
    p, msg = get_persona_by_name_or_index(arg)
    if not p:
        return f"Couldn’t pick: {msg}\n\n{menu_list()}"
    _SESS[user_id]["current"] = PERS.index(p)
    return f"Picked {p.get('name','?')}."

def _current(user_id: str):
    _ensure_user(user_id)
    idx = _SESS[user_id]["current"]
    if 0 <= idx < len(PERS):
        return PERS[idx]
    return PERS[0] if PERS else {}

def _safe_sample(lst: List[str]) -> str:
    return random.choice(lst) if lst else ""

def generate_chat_turn(user_text: str, user_id: str = "unknown") -> str:
    if not HAVE_PERSONAS or not PERS:
        return f"you said: {user_text}"

    p = _current(user_id)

    # greet on first message or when user says hi
    low = user_text.strip().lower()
    if low in ("hi","hello","hey","start") or not _SESS[user_id].get("welcomed"):
        _SESS[user_id]["welcomed"] = True
        return intro(p)

    # reply with a simple SFW memory echo (safe)
    mem = _safe_sample(p.get("sfw_memories", []))
    if mem:
        return f"{p.get('name','')} says: {mem}"
    return f"{p.get('name','')} is listening…"
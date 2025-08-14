# dialog.py — minimal, safe implementation expected by main.py

import re
import random
from typing import Dict, Optional

# These must exist in personas.py
from personas import PERS, intro, menu_list, size_line

# Per-user state: which girl is picked
_USER_STATE: Dict[str, Dict[str, str]] = {}

def _find_persona(selector: str) -> Optional[dict]:
    """
    selector can be a number (1-based index from menu) or a name (case-insensitive).
    """
    selector = (selector or "").strip()
    if not selector:
        return None

    # Try numeric index first
    if selector.isdigit():
        idx = int(selector) - 1
        if 0 <= idx < len(PERS):
            return PERS[idx]

    # Try case-insensitive name match
    sel_low = selector.lower()
    for p in PERS:
        if p.get("name","").lower() == sel_low:
            return p

    # Try partial name startswith
    for p in PERS:
        if p.get("name","").lower().startswith(sel_low):
            return p

    return None


# --- API expected by main.py ---

def list_girls() -> str:
    """
    Returns a pretty list of girls.
    """
    return menu_list()

def pick_girl(arg: str, user_id: str) -> str:
    """
    Sets the active girl for this user.
    """
    persona = _find_persona(arg)
    if not persona:
        return "I couldn't find that girl. Try /girls, then /pick <#|name>."

    _USER_STATE.setdefault(user_id, {})
    _USER_STATE[user_id]["current_name"] = persona.get("name","")

    # Friendly intro line from personas.py
    try:
        return intro(persona)
    except Exception:
        # Never crash user flows on intro
        return f"Switched to {persona.get('name','(unknown)')}."

def _current_persona(user_id: str) -> Optional[dict]:
    state = _USER_STATE.get(user_id) or {}
    name = state.get("current_name")
    if not name:
        return None
    for p in PERS:
        if p.get("name") == name:
            return p
    return None

def generate_chat_turn(text: str, user_id: str = "unknown") -> str:
    """
    Core chat turn. Keeps it simple and safe.
    """
    p = _current_persona(user_id)
    if not p:
        # If no pick yet, gently nudge
        return (
            "Hey! Pick a girl first: /girls then /pick <#|name>\n\n"
            + menu_list()
        )

    # Tiny, friendly logic demo (no heavy NLP on purpose)
    t = (text or "").strip().lower()

    if re.search(r"\b(size|height|weight|stats)\b", t):
        return f"{p['name']}: {size_line(p)}"

    if re.search(r"\b(favorite|favourite|music|song)\b", t):
        mp = p.get("music_pick") or (p.get("music") or ["music"])[0]
        return f"{p['name']}: I’m into {mp} lately."

    if re.search(r"\b(movie|film)\b", t):
        mv = p.get("movie_pick") or (p.get("movies") or ["movies"])[0]
        return f"{p['name']}: My comfort movie is {mv}."

    if re.search(r"\b(tv|show|series)\b", t):
        tv = p.get("tv_pick") or (p.get("tv") or ["TV"])[0]
        return f"{p['name']}: I’ve been watching {tv}."

    # Default friendly reply
    first_name = p.get("name","She")
    return f"{first_name}: I’m here—tell me more! 😊"
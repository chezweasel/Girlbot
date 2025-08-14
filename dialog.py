# dialog.py
from typing import Dict, Any, List, Optional
from personas import PERS, STORIES, BOOKS, menu_list, intro, size_line

# ---- helpers ---------------------------------------------------------------

def _normalize_name(name: str) -> str:
    return (name or "").strip().lower()

def _find_persona(query: str):
    """Find by number (1-based), exact name, or prefix-insensitive match."""
    q = query.strip()
    if not q:
        return None

    # number pick
    if q.isdigit():
        idx = int(q) - 1
        if 0 <= idx < len(PERS):
            return PERS[idx]

    # name / fuzzy prefix
    qn = _normalize_name(q)
    # exact name match (case-insensitive)
    for p in PERS:
        if _normalize_name(p.get("name", "")) == qn:
            return p
    # startswith
    cands = [p for p in PERS if _normalize_name(p.get("name","")).startswith(qn)]
    if len(cands) == 1:
        return cands[0]
    return None

def _current_persona(state: Dict[str, Any]):
    name = state.get("current_name")
    if not name:
        return None
    for p in PERS:
        if p.get("name") == name:
            return p
    return None

def _pick_memory(p: Dict[str, Any], nsfw: bool) -> Optional[str]:
    """Choose an SFW or NSFW memory if available."""
    import random
    if nsfw:
        pool = p.get("nsfw_memories") or []
        if pool:
            return random.choice(pool)
    # fallback to sfw or life
    pool = p.get("sfw_memories") or p.get("life_memories") or []
    if pool:
        return random.choice(pool)
    return None

def _books_line(p: Dict[str, Any]) -> str:
    items = (BOOKS or {}).get(p.get("name", ""), [])
    if not items:
        return "(no books set)"
    parts = []
    for b in items[:3]:
        t = b.get("title","?")
        q = b.get("quote")
        if q:
            parts.append(f"{t} — “{q}”")
        else:
            parts.append(t)
    return "; ".join(parts)

def _help_text() -> str:
    return (
        "Commands:\n"
        "/girls — list all girls\n"
        "/pick <#|name> — choose who to chat with (e.g., /pick 2 or /pick Nicole)\n"
        "/nsfw_on, /nsfw_off — toggle NSFW memory picks\n"
        "/intro — show a short intro from current girl\n"
        "/size — height/weight/cup line\n"
        "/books — show book picks if present\n"
        "/who — show who’s selected\n"
        "/help — this help\n"
        "Type anything else to chat and I’ll pull a memory.\n"
    )

# ---- main turn -------------------------------------------------------------

def generate_chat_turn(state: Dict[str, Any], user_msg: str) -> str:
    """
    state: {
      'current_name': Optional[str],
      'nsfw': bool
    }
    returns a response string
    """
    msg = (user_msg or "").strip()

    # commands
    if msg.lower() in ("/help", "help", "?"):
        return _help_text()

    if msg.lower() == "/girls":
        return menu_list()

    if msg.lower().startswith("/pick"):
        arg = msg[5:].strip()
        if not arg:
            return "Usage: /pick <#|name> (e.g., /pick 1 or /pick Zoey)"
        p = _find_persona(arg)
        if not p:
            return f"Couldn’t find '{arg}'. Try /girls and pick by number or name."
        state["current_name"] = p.get("name")
        return f"Picked {p.get('name')}.\nSay /intro or type a message."

    if msg.lower() in ("/nsfw_on", "/nsfw off", "/nsfw_off", "/nsfw on"):
        # normalize
        on = msg.lower() in ("/nsfw_on", "/nsfw on")
        state["nsfw"] = bool(on)
        return f"NSFW is now {'ON' if state['nsfw'] else 'OFF'}."

    if msg.lower() == "/intro":
        p = _current_persona(state)
        if not p:
            return "Pick a girl first with /girls then /pick <#|name>."
        return intro(p)

    if msg.lower() == "/size":
        p = _current_persona(state)
        if not p:
            return "Pick a girl first with /girls then /pick <#|name>."
        return size_line(p)

    if msg.lower() == "/books":
        p = _current_persona(state)
        if not p:
            return "Pick a girl first with /girls then /pick <#|name>."
        return _books_line(p)

    if msg.lower() == "/who":
        p = _current_persona(state)
        if not p:
            return "Nobody picked. Use /girls then /pick."
        return f"Talking to {p.get('name')} (NSFW {'ON' if state.get('nsfw') else 'OFF'})."

    # normal chat: pull a memory and echo a simple line + memory
    p = _current_persona(state)
    if not p:
        return "Pick someone first: /girls → /pick <#|name> (try /help)."

    mem = _pick_memory(p, state.get("nsfw", False))
    pre = f"{p.get('name')} says:"
    if mem:
        return f"{pre} {mem}"
    return f"{pre} I’m thinking… tell me something about you?"
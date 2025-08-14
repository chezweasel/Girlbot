# dialog.py
import re
import random
from typing import Dict, Tuple

# Pull persona data + helpers
from personas import PERS, intro, menu_list, size_line
from stories import STORIES, BOOKS

# ---------------- State helpers ----------------
def _default_state() -> Dict:
    return {
        "selected": PERS[0]["name"] if PERS else None,
        "nsfw_on": False,
        "seed": 42,
        "history": [],
    }

def _find_persona(query: str):
    """Find by (1-based) index or by name (case-insensitive)."""
    if not query:
        return None
    query = query.strip()
    # Index?
    if query.isdigit():
        idx = int(query) - 1
        if 0 <= idx < len(PERS):
            return PERS[idx]
    # Name?
    low = query.lower()
    for p in PERS:
        if p["name"].lower() == low:
            return p
    return None

def _get_selected(state: Dict):
    sel = state.get("selected")
    for p in PERS:
        if p["name"] == sel:
            return p
    # fallback
    if PERS:
        state["selected"] = PERS[0]["name"]
        return PERS[0]
    return None

def _rand(seed_bump=0):
    return random.Random(10_001 + seed_bump)

# ---------------- Format helpers ----------------
def _format_books(p):
    b = BOOKS.get(p["name"], [])
    if not b:
        return "No saved books."
    lines = []
    for i, bk in enumerate(b, 1):
        title = bk.get("title", "Untitled")
        quote = bk.get("quote", "")
        memo  = bk.get("memory", "")
        line = f"{i}. {title}"
        if quote:
            line += f' — “{quote}”'
        if memo:
            line += f"  [{memo}]"
        lines.append(line)
    return "\n".join(lines)

def _pick_memory(p, kind: str, rng: random.Random):
    s = STORIES.get(p["name"], {})
    pool = s.get(kind, [])
    if not pool:
        return "(no memories found)"
    return rng.choice(pool)

def _short_profile(p):
    return (
        f"{p['name']} — {p.get('ethnicity','')}, {p.get('hometown','')}\n"
        f"{size_line(p)} | {p.get('body','')} | {p.get('hair','')} hair, {p.get('eyes','')} eyes, {p.get('cup','?')} cup\n"
        f"Job: {p.get('job','?')} | Edu: {p.get('education','?')}\n"
        f"Fav Music: {', '.join(p.get('music',[])[:2]) or '—'} | Movies: {', '.join(p.get('movies',[])[:2]) or '—'} | TV: {', '.join(p.get('tv',[])[:2]) or '—'}\n"
        f"Hobbies: {', '.join(p.get('hobbies',[])[:3]) or '—'}"
    )

# ---------------- Command handling ----------------
_HELP_TEXT = """Commands:
/girls                     -> list available personas
/pick <#|name>            -> switch persona
/intro                    -> persona intro line
/profile                  -> compact profile of current persona
/books                    -> current persona's books
/memory sfw|nsfw|mast     -> pull a random memory (nsfw requires /nsfw_on)
/nsfw_on                  -> enable NSFW memories
/nsfw_off                 -> disable NSFW memories
/help                     -> this help
"""

def _handle_command(state: Dict, msg: str) -> str:
    p = _get_selected(state)
    if not p:
        return "(no personas loaded)"
    parts = msg.strip().split(maxsplit=1)
    cmd = parts[0].lower()
    arg = parts[1] if len(parts) > 1 else ""

    if cmd == "/girls":
        return menu_list()

    if cmd == "/pick":
        if not arg:
            return "Usage: /pick <#|name>"
        found = _find_persona(arg)
        if not found:
            return f"Couldn't find '{arg}'. Try /girls."
        state["selected"] = found["name"]
        return f"✓ Selected: {found['name']}"

    if cmd == "/intro":
        return intro(p)

    if cmd == "/profile":
        return _short_profile(p)

    if cmd == "/books":
        return _format_books(p)

    if cmd == "/memory":
        if not arg:
            return "Usage: /memory sfw|nsfw|mast"
        key = arg.lower().strip()
        rng = _rand()
        if key in ("sfw", "safe", "life"):
            return _pick_memory(p, "sfw_memories", rng)
        if key in ("nsfw", "spicy"):
            if not state.get("nsfw_on"):
                return "(nsfw is off — use /nsfw_on first)"
            return _pick_memory(p, "nsfw_memories", rng)
        if key in ("mast", "masturbation"):
            if not state.get("nsfw_on"):
                return "(nsfw is off — use /nsfw_on first)"
            return _pick_memory(p, "masturbation_memories", rng)
        return "Unknown memory type. Use: sfw | nsfw | mast"

    if cmd == "/nsfw_on":
        state["nsfw_on"] = True
        return "NSFW enabled."

    if cmd == "/nsfw_off":
        state["nsfw_on"] = False
        return "NSFW disabled."

    if cmd == "/help":
        return _HELP_TEXT

    return "Unknown command. Try /help"

# ---------------- Chat turn ----------------
def _free_chat(state: Dict, user_msg: str) -> str:
    """
    Super lightweight persona reply:
    - references a fav pick
    - sometimes pulls a memory (sfw if nsfw_off)
    """
    p = _get_selected(state)
    if not p:
        return "(no personas loaded)"
    rng = _rand()
    bits = [f"{p['name']}: "]

    # Small talk flavor
    fav_music = p.get("music_pick") or (p.get("music") or ["music"])[0]
    bits.append(f"I'm thinking about {fav_music} and ")
    fav_movie = p.get("movie_pick") or (p.get("movies") or ["movies"])[0]
    bits.append(f"{fav_movie.lower()} vibes. ")

    # Pull a memory now and then
    if rng.random() < 0.5:
        key = "sfw_memories"
        if state.get("nsfw_on") and rng.random() < 0.4:
            key = rng.choice(["sfw_memories", "nsfw_memories"])
        mem = _pick_memory(p, key, rng)
        bits.append(mem)

    return "".join(bits)

def generate_chat_turn(state: Dict, user_msg: str) -> Tuple[Dict, str]:
    """
    Primary entry point used by main.py:
    - Takes state and a user message
    - Returns (updated_state, text_response)
    """
    if not state:
        state = _default_state()

    text = user_msg.strip()
    if text.startswith("/"):
        reply = _handle_command(state, text)
    else:
        reply = _free_chat(state, text)

    # keep short history
    state["history"].append({"you": user_msg, "bot": reply})
    if len(state["history"]) > 50:
        state["history"] = state["history"][-50:]

    return state, reply
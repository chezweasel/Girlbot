# dialog.py
# Tiny, friendly wrapper around personas.py.
# It handles commands and builds a reply using intro() + one memory line.

import random
from settings import stable_seed
from personas import PERS, BOOKS, intro, menu_list, size_line

def init_state():
    """Call this once at app start."""
    return {
        "current": PERS[0]["name"] if PERS else None,  # which girl is active
        "nsfw": False,                                  # toggle for spicy memories
    }

def find_persona(name):
    """Find a persona by name (case-insensitive)."""
    if not name:
        return None
    name = name.strip().lower()
    for p in PERS:
        if p["name"].lower() == name:
            return p
    return None

def pick_memory(persona, nsfw_enabled, user_text):
    """
    Choose one memory line to say.
    - If nsfw is ON, prefer nsfw_memories (fallback to sfw).
    - If user mentions 'solo' or 'masturbat', prefer masturbation_memories.
    """
    text = (user_text or "").lower()

    # default pool is SFW
    pool = persona.get("sfw_memories", [])[:]

    # switch pool if user asked about solo
    if "masturbat" in text or "solo" in text:
        pool = persona.get("masturbation_memories", []) or pool
    # else if nsfw toggle is on, try nsfw pool
    elif nsfw_enabled:
        pool = persona.get("nsfw_memories", []) or pool

    if not pool:
        return ""  # nothing to say
    # deterministic-ish pick so it feels consistent per name + input length
    seed_val = stable_seed(persona["name"]) + len(text)
    rnd = random.Random(seed_val)
    return rnd.choice(pool)

def handle_command(state, text):
    """
    Handle slash commands. Returns (output_or_None, state).
    If it's not a command, returns (None, state).
    """
    t = (text or "").strip()

    if t.startswith("/girls"):
        return menu_list(), state

    if t.startswith("/nsfw_on"):
        state["nsfw"] = True
        return "NSFW is ON.", state

    if t.startswith("/nsfw_off"):
        state["nsfw"] = False
        return "NSFW is OFF.", state

    if t.startswith("/pick"):
        # supports: /pick 3   or   /pick Zoey
        parts = t.split(maxsplit=1)
        if len(parts) == 2:
            key = parts[1].strip()
            chosen = None
            if key.isdigit():
                idx = int(key) - 1
                if 0 <= idx < len(PERS):
                    chosen = PERS[idx]
            else:
                chosen = find_persona(key)

            if chosen:
                state["current"] = chosen["name"]
                return f"Picked {chosen['name']}. [{size_line(chosen)}]", state
        return "Couldn’t pick—try `/pick 1` or `/pick Zoey`.", state

    if t.startswith("/books"):
        cur = find_persona(state.get("current")) or (PERS[0] if PERS else None)
        if not cur:
            return "No personas loaded.", state
        items = BOOKS.get(cur["name"], [])
        if not items:
            return f"{cur['name']} has no saved books.", state
        lines = [f"• {it.get('title','?')} — {it.get('quote','')}".rstrip(" — ")
                 for it in items]
        return f"{cur['name']}'s shelf:\n" + "\n".join(lines), state

    if t.startswith("/help"):
        return ("Commands: /girls, /pick #|name, /books, /nsfw_on, /nsfw_off, /help"),
        state

    # not a command
    return None, state

def generate_chat_turn(state, user_text):
    """
    Main entry point called by main.py.
    Returns (assistant_text, updated_state).
    """
    # 1) Commands first
    out, state = handle_command(state, user_text)
    if out is not None:
        return out, state

    # 2) Normal conversational turn
    cur = find_persona(state.get("current")) or (PERS[0] if PERS else None)
    if not cur:
        return "No personas loaded.", state

    # A little intro + one memory line (pool depends on /nsfw_on & message)
    preface = intro(cur)
    memory_line = pick_memory(cur, state.get("nsfw", False), user_text)
    reply = preface + ("\n\n" + memory_line if memory_line else "")

    return reply, state
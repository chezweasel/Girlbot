# media_commands.py
# Centralized handlers for /selfie and /gen (plus NSFW gating & safety).
# These functions DO NOT import your app; you pass in the bits from main.py.

from typing import Optional

# ===== NSFW TEASES FOR NON-OWNER =====
TEASE_LINES = [
    "mm, not yet… tease me back first. What’s the last song that gave you goosebumps?",
    "you’ve got me warm, but you have to earn the next step 😇 tell me a very specific thing you notice about mouths.",
    "close… say one thing you’d whisper in my ear, then maybe I’ll behave badly."
]

# ===== HARD SAFETY CHECKS (no minors / under-18 / young-looking) =====
def _contains_minor_terms(t: str) -> bool:
    if not t:
        return False
    bad = [
        "minor", "underage", "young-looking", "young looking", "kid", "child",
        "freshman", "sophomore", "schoolgirl", "school boy", "middle school",
        "teen", "preteens", "pre-teen", "pre teen",
        "13", "14", "15", "16", "17"
    ]
    low = t.lower()
    return any(w in low for w in bad)

# ===== OWNER/NSFW GATE =====
def send_tease_or_allow_nsfw(p, s, uid, chat, send_message, save_state, OWNER_ID) -> bool:
    """
    Returns True if NSFW is allowed (owner), False if we teased (non-owner).
    For non-owner with NSFW on, sends a rotating tease and blocks NSFW.
    """
    # Always allow owner
    if str(uid) == str(OWNER_ID):
        return True

    # Non-owner → send tease instead
    i = s.get("tease_count", 0) % len(TEASE_LINES)
    s["tease_count"] = s.get("tease_count", 0) + 1
    save_state()
    send_message(chat, f"{p.get('name','Girl')}: {TEASE_LINES[i]}")
    return False

# ===== /selfie helper: build a consistent persona prompt =====
def _selfie_prompt_for(p, vibe: str, nsfw: bool) -> str:
    name = p.get("name", "Girl")
    body = f"{p.get('body','slim')} body, {p.get('hair','brunette')} hair, {p.get('eyes','brown')} eyes"
    cup = p.get("cup")
    if cup:
        body += f", proportions consistent with {cup}-cup bust"
    base = (
        f"photo portrait of {name} (adult), {p.get('img_tags','')}, {body}, "
        "realistic, shallow depth of field, cinematic lighting"
    )
    if not nsfw:
        base += ", tasteful playful tease (no explicit nudity)"
    else:
        base += ", tasteful lingerie vibe (no explicit anatomy)"
    if vibe:
        base += f", vibe: {vibe}"
    return base

# ===== PUBLIC ENTRY: handle /selfie and /gen in one place =====
def handle_media_commands(
    low: str,
    text: str,
    p: dict,
    s: dict,
    uid: int,
    chat: int,
    *,
    send_message,
    save_state,
    stable_seed,
    _spawn_image_job,
    OWNER_ID,
    STATE,
) -> Optional[tuple]:
    """
    Call this once inside your hook() AFTER you computed: low, text, p, s, uid, chat.
    Returns ("OK", 200) when a command is handled; otherwise None.
    """

    # ---- /selfie ----
    if low.startswith("/selfie"):
        # parse vibe (optional)
        parts = text.split(maxsplit=1)
        vibe = parts[1] if len(parts) > 1 else "teasing, SFW"

        # respect daily quota (non-owner)
        if (str(uid) != str(OWNER_ID)) and (s.get("used", 0) >= s.get("daily_quota", 0) if "daily_quota" in s else False):
            # if you don’t track daily_quota in s, the app-level allowed() already guards this
            pass

        # use whatever your app has for NSFW flag
        is_nsfw = bool(s.get("nsfw", False))

        prompt = _selfie_prompt_for(p, vibe, nsfw=is_nsfw)
        seed = stable_seed(p.get("name", "Girl"))
        send_message(chat, "📸 One moment…")
        try:
            # keep under free-tier size caps (Horde/HF): 576x704 is a safe portrait
            _spawn_image_job(chat, prompt, w=576, h=704, seed=seed, nsfw=is_nsfw)
            # tick usage for non-owner
            if str(uid) != str(OWNER_ID):
                STATE[str(uid)]["used"] = STATE[str(uid)].get("used", 0) + 1
                save_state()
        except Exception as e_img:
            send_message(chat, f"Image queue: {e_img}")
        return "OK", 200

    # ---- /gen ----
    if low.startswith("/gen"):
        parts = text.split(maxsplit=1)
        if len(parts) < 2:
            send_message(chat, "/gen <prompt>")
            return "OK", 200

        user_prompt = parts[1].strip()

        # hard safety
        if _contains_minor_terms(user_prompt):
            send_message(chat, "I can’t do anything under-18 or young-looking.")
            return "OK", 200

        # block non-owners with a tease (and stop)
        if not send_tease_or_allow_nsfw(p, s, uid, chat, send_message, save_state, OWNER_ID):
            return "OK", 200

        # build a consistent-look hint for the persona
        hint = (
            f"{p.get('name','Girl')} consistent look: {p.get('img_tags','')}, "
            f"{p.get('hair','')} hair, {p.get('eyes','')} eyes, {p.get('body','')}"
        )
        cup = p.get("cup")
        if cup:
            hint += f", proportions consistent with {cup}-cup bust"

        full_prompt = hint + ". " + (user_prompt or "tasteful nude portrait")

        seed = stable_seed(p.get("name", "Girl"))
        send_message(chat, "🎨 One moment…")
        try:
            _spawn_image_job(chat, full_prompt, w=576, h=704, seed=seed, nsfw=True)
            if str(uid) != str(OWNER_ID):
                STATE[str(uid)]["used"] = STATE[str(uid)].get("used", 0) + 1
                save_state()
        except Exception as e_img:
            send_message(chat, f"Image queue: {e_img}")
        return "OK", 200

    # nothing matched
    return None
    
    # ===== NSFW TEASES FOR NON-OWNER =====
TEASE_LINES = [
    "mm, not yet… tease me back first. What’s the last song that gave you goosebumps?",
    "you’ve got me warm, but you have to earn the next step 😇 tell me a very specific thing you notice about mouths.",
    "close… say one thing you’d whisper in my ear, then maybe I’ll behave badly."
]

def send_tease_or_allow_nsfw(p, s, uid, chat, OWNER_ID, send_message, save_state) -> bool:
    """
    Returns True if NSFW is allowed (owner), False if we teased (non-owner).
    For non-owner with NSFW on, sends a rotating tease and blocks NSFW.
    """
    if str(uid) == str(OWNER_ID):
        return True  # Owner always allowed

    # Send tease instead of NSFW
    i = s.get("tease_count", 0) % len(TEASE_LINES)
    s["tease_count"] = s.get("tease_count", 0) + 1
    save_state()
    send_message(chat, f"{p.get('name', 'Girl')}: {TEASE_LINES[i]}")
    return False


# ===== /gen COMMAND HANDLER =====
def handle_gen_command(low, text, p, s, uid, chat, send_message, save_state, stable_seed, _spawn_image_job, OWNER_ID, STATE):
    if not low.startswith("/gen"):
        return None  # Not our command

    parts = text.split(maxsplit=1)
    if len(parts) < 2:
        send_message(chat, "/gen <prompt>")
        return "OK", 200

    user_prompt = parts[1].strip()

    # Hard safety: no under-18 content
    if _contains_minor_terms(user_prompt):
        send_message(chat, "I can’t do anything under-18 or young-looking.")
        return "OK", 200

    # Tease for non-owners
    if not send_tease_or_allow_nsfw(p, s, uid, chat, OWNER_ID, send_message, save_state):
        return "OK", 200

    # Build persona appearance hint
    hint = (
        f"{p.get('name','Girl')} consistent look: {p.get('img_tags','')}, "
        f"{p.get('hair','')} hair, {p.get('eyes','')} eyes, {p.get('body','')}"
    )
    cup = p.get("cup")
    if cup:
        hint += f", proportions consistent with {cup}-cup bust"

    full_prompt = hint + ". " + (user_prompt or "tasteful nude portrait")

    # Generate the image
    seed = stable_seed(p.get("name", "Girl"))
    send_message(chat, "🎨 One moment…")
    try:
        _spawn_image_job(chat, full_prompt, w=576, h=704, seed=seed, nsfw=True)
        if str(uid) != str(OWNER_ID):
            STATE[str(uid)]["used"] = STATE[str(uid)].get("used", 0) + 1
            save_state()
    except Exception as e_img:
        send_message(chat, f"Image queue: {e_img}")

    return "OK", 200
# ===== END /gen =====

# ============================================
# media_commands.py  —  Selfie & NSFW commands
# ============================================

# ===== Command Help Text =====
HELP = (
    "Commands:\n"
    "/start - Begin chatting with the bot\n"
    "/selfie [vibe] - Generate a
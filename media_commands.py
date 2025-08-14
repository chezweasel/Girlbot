# media_commands.py
# Centralized handlers for /selfie and /gen (plus NSFW gating & safety).
# These functions DO NOT import your app; you pass in the bits from main.py.

from typing import Optional

# ===============================
# Tease lines for non-owner users
# ===============================
TEASE_LINES = [
    "mm, not yet… tease me back first. What’s the last song that gave you goosebumps?",
    "you’ve got me warm, but you have to earn the next step 😇 tell me a very specific thing you notice about mouths.",
    "close… say one thing you’d whisper in my ear, then maybe I’ll behave badly."
]

# ==========================================
# Hard safety: never allow under-18 concepts
# ==========================================
def _contains_minor_terms(t: str) -> bool:
    if not t:
        return False
    bad = [
        "minor", "underage", "young-looking", "young looking",
        "kid", "child", "children", "schoolgirl", "school boy",
        "middle school", "highschool", "high school",
        "freshman", "sophomore",
        "teen", "preteens", "pre-teen", "pre teen",
        "13", "14", "15", "16", "17"
    ]
    low = t.lower()
    return any(w in low for w in bad)

# ==================================
# NSFW gate: only owner gets NSFW out
# ==================================
def send_tease_or_allow_nsfw(
    p: dict, s: dict, uid: int, chat: int, *,
    send_message, save_state, OWNER_ID
) -> bool:
    """
    Returns True if NSFW is allowed (owner), False if we teased (non-owner).
    Non-owners get a rotating tease and we block NSFW generation.
    """
    if str(uid) == str(OWNER_ID):
        return True  # Owner always allowed

    # Non-owner → send tease and block
    i = s.get("tease_count", 0) % len(TEASE_LINES)
    s["tease_count"] = s.get("tease_count", 0) + 1
    save_state()
    send_message(chat, f"{p.get('name','Girl')}: {TEASE_LINES[i]}")
    return False

# ==================================================
# Selfie helper: build a consistent persona photo prompt
# ==================================================
def _selfie_prompt_for(p: dict, vibe: str, *, nsfw: bool) -> str:
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

# ======================================================
# Public entry: handle /selfie and /gen in one function
# ======================================================
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
    Call this once inside your hook() AFTER you computed:
      low, text, p, s, uid, chat
    Returns ("OK", 200) when a command is handled; otherwise None.
    """

    # -------- /selfie --------
    if low.startswith("/selfie"):
        # vibe is optional
        parts = text.split(maxsplit=1)
        vibe = parts[1] if len(parts) > 1 else "teasing, SFW"

        is_nsfw = bool(s.get("nsfw", False))
        # If selfie would be NSFW and user is NOT owner, tease & stop
        if is_nsfw and not send_tease_or_allow_nsfw(
            p, s, uid, chat,
            send_message=send_message, save_state=save_state, OWNER_ID=OWNER_ID
        ):
            return "OK", 200

        prompt = _selfie_prompt_for(p, vibe, nsfw=is_nsfw)
        seed = stable_seed(p.get("name", "Girl"))
        send_message(chat, "📸 One moment…")
        try:
            # keep under free-tier limits (576x704 is safe portrait)
            _spawn_image_job(chat, prompt, w=576, h=704, seed=seed, nsfw=is_nsfw)
            # tick usage for non-owner
            if str(uid) != str(OWNER_ID):
                STATE[str(uid)]["used"] = STATE[str(uid)].get("used", 0) + 1
                save_state()
        except Exception as e_img:
            send_message(chat, f"Image queue: {e_img}")
        return "OK", 200

    # -------- /gen --------
    if low.startswith("/gen"):
        parts = text.split(maxsplit=1)
        if len(parts) < 2:
            send_message(chat, "/gen <prompt>")
            return "OK", 200

        user_prompt = parts[1].strip()

        # hard safety: absolutely no minors / young-looking
        if _contains_minor_terms(user_prompt):
            send_message(chat, "I can’t do anything under-18 or young-looking.")
            return "OK", 200

        # Only owner gets NSFW output
        if not send_tease_or_allow_nsfw(
            p, s, uid, chat,
            send_message=send_message, save_state=save_state, OWNER_ID=OWNER_ID
        ):
            return "OK", 200

        # Persona-consistent hint
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
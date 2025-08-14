# media_commands.py
from typing import Optional
from settings import stable_seed
from image_backends import generate_image, send_photo

TEASE_LINES = [
    "mm, not yet… tease me back first. What’s the last song that gave you goosebumps?",
    "you’ve got me warm, but you have to earn the next step 😇 tell me a very specific thing you notice about mouths.",
    "close… say one thing you’d whisper in my ear, then maybe I’ll behave badly."
]

def _contains_minor_terms(t: str) -> bool:
    if not t: return False
    bad = ["minor","underage","young-looking","young looking","kid","child","13","14","15","16","17"]
    low = t.lower()
    return any(w in low for w in bad)

def _selfie_prompt(p, vibe: str, nsfw: bool) -> str:
    name = p.get("name","Girl")
    body = f"{p.get('body','slim')} body, {p.get('hair','brunette')} hair, {p.get('eyes','brown')} eyes"
    cup = p.get("cup")
    if cup: body += f", proportions consistent with {cup}-cup bust"
    base = (f"photo portrait of {name} (adult), {p.get('img_tags','')}, {body}, "
            "realistic, shallow depth of field, cinematic lighting")
    if not nsfw: base += ", tasteful playful tease (no explicit nudity)"
    else:        base += ", tasteful lingerie vibe (no explicit anatomy)"
    if vibe: base += f", vibe: {vibe}"
    return base

def handle_media_commands(low, text, p, s, uid, chat, *, send_message, save_state, OWNER_ID, STATE) -> Optional[tuple]:
    # /selfie
    if low.startswith("/selfie"):
        parts = text.split(maxsplit=1)
        vibe = parts[1] if len(parts)>1 else "teasing, SFW"
        is_nsfw = bool(s.get("nsfw", False))
        prompt = _selfie_prompt(p, vibe, nsfw=is_nsfw)
        seed = stable_seed(p.get("name","Girl"))
        send_message(chat, "📸 One moment…")
        try:
            out = generate_image(prompt, w=576, h=704, seed=seed, nsfw=is_nsfw)
            send_photo(chat, out)
            if str(uid) != str(OWNER_ID):
                STATE[str(uid)]["used"] = STATE[str(uid)].get("used", 0) + 1
                save_state()
        except Exception as e:
            send_message(chat, f"Image queue: {e}")
        return "OK", 200

    # /gen
    if low.startswith("/gen"):
        parts = text.split(maxsplit=1)
        if len(parts)<2:
            send_message(chat, "/gen <prompt>")
            return "OK", 200
        user_prompt = parts[1].strip()
        if _contains_minor_terms(user_prompt):
            send_message(chat, "I can’t do anything under-18 or young-looking.")
            return "OK", 200
        # tease gate for non-owner
        if str(uid) != str(OWNER_ID):
            i = s.get("tease_count",0) % len(TEASE_LINES)
            s["tease_count"] = s.get("tease_count",0) + 1
            save_state()
            send_message(chat, f"{p.get('name','Girl')}: {TEASE_LINES[i]}")
            return "OK", 200

        # owner → allow NSFW generation
        hint = (f"{p.get('name','Girl')} consistent look: {p.get('img_tags','')}, "
                f"{p.get('hair','')} hair, {p.get('eyes','')} eyes, {p.get('body','')}")
        cup = p.get("cup")
        if cup: hint += f", proportions consistent with {cup}-cup bust"
        full = hint + ". " + user_prompt
        seed = stable_seed(p.get("name","Girl"))
        send_message(chat, "🎨 One moment…")
        try:
            out = generate_image(full, w=576, h=704, seed=seed, nsfw=True)
            send_photo(chat, out)
        except Exception as e:
            send_message(chat, f"Image queue: {e}")
        return "OK", 200

    return None
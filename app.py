from flask import Flask, request
import requests
import os
import time
import random

from utils import *  # Import all from utils.py

# ===== ENV / TG =====
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
OWNER_ID = os.getenv("OWNER_ID", "").strip()
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "").strip()
if WEBHOOK_URL and not WEBHOOK_URL.endswith("/telegram/pix3lhook"):
    WEBHOOK_URL = WEBHOOK_URL.rstrip("/") + "/telegram/pix3lhook"
API = f"https://api.telegram.org/bot{BOT_TOKEN}"
assert BOT_TOKEN and OWNER_ID and WEBHOOK_URL, "Missing BOT_TOKEN/OWNER_ID/WEBHOOK_URL"

app = Flask(__name__)
PROCESSED = set()

# ===== TG HELPERS =====
def send_message(cid, text):
    r = requests.post(f"{API}/sendMessage", json={"chat_id": int(cid), "text": text}, timeout=20)
    if r.status_code != 200:
        print("SEND ERR:", r.text[:200])

def send_photo(cid, path):
    with open(path, "rb") as f:
        r = requests.post(f"{API}/sendPhoto", data={"chat_id": int(cid)}, files={"photo": f}, timeout=120)
    if r.status_code != 200:
        print("PHOTO ERR:", r.text[:200])

@app.route("/telegram/pix3lhook", methods=["GET", "POST"])
def hook():
    if request.method == "GET":
        return "hook ok", 200

    up = request.get_json(force=True, silent=True) or {}
    print("TG UPDATE RAW:", str(up)[:500])

    try:
        if "update_id" in up:
            if up["update_id"] in PROCESSED:
                return "OK", 200
            PROCESSED.add(up["update_id"])

        msg = up.get("message") or up.get("edited_message")
        if not msg:
            return "OK", 200

        chat = msg["chat"]["id"]
        uid = msg["from"]["id"]
        text = (msg.get("text") or "").strip()
        low = text.lower()

        if not PERS:
            send_message(chat, "No girls loaded yet.")
            return "OK", 200

        s = get_user(uid)
        s["u_msg"] += 1
        save_state()

        mid = msg.get("message_id")
        if s.get("last_msg_id") == mid:
            return "OK", 200
        s["last_msg_id"] = mid
        save_state()

        p = PERS[s["g"] % len(PERS)]

        if low in {"hi", "hello", "hey", "/start"}:
            send_message(chat, intro(p))
            return "OK", 200

        if low.startswith("/help"):
            send_message(chat, HELP)
            return "OK", 200

        if low.startswith("/girls"):
            send_message(chat, menu_list())
            return "OK", 200

        if low.startswith("/pick"):
            parts = text.split(maxsplit=1)
            if len(parts) < 2:
                send_message(chat, "Use: /pick 1-99 or name")
                return "OK", 200
            t = parts[1].strip()
            idx = None
            if t.isdigit():
                n = int(t)
                if 1 <= n <= len(PERS):
                    idx = n - 1
            else:
                t_low = t.lower()
                for i, pp in enumerate(PERS):
                    if pp.get("name", "").lower() == t_low:
                        idx = i
                        break
            if idx is None:
                send_message(chat, "Can’t find her 😉 Try /girls")
                return "OK", 200
            s["g"] = idx
            save_state()
            send_message(chat, intro(PERS[idx]))
            return "OK", 200

        if low.startswith("/who"):
            size = size_line(p)
            send_message(chat, f"Your girl: {p.get('name', 'Girl')} — {p.get('persona', '')} ({p.get('age', 0)}) from {p.get('location', '')} ({size}).")
            return "OK", 200

        if low.startswith("/bio"):
            size = size_line(p)
            send_message(chat, f"{p.get('name', 'Girl')} · {p.get('age', 0)} · {p.get('location', '')} ({size})\n{p.get('origin', '')}\nJob: {p.get('job', '')} · Family: {p.get('family', '')}")
            return "OK", 200

        if low.startswith("/style"):
            send_message(chat, "Quirks: " + ", ".join(p.get("quirks", [])) +
                               f"\nFavs: {p.get('fav_color', '?')} · {p.get('fav_flower', '?')}\nMusic: " +
                               ", ".join((p.get("music") or [])[:2]) + "\nMovies: " + ", ".join((p.get("movies") or [])[:1]) +
                               "\nTV: " + ", ".join((p.get("tv") or [])[:1]))
            return "OK", 200

        if low.startswith("/books"):
            send_message(chat, books_card(p))
            return "OK", 200

        if low.startswith("/nsfw_on"):
            s["nsfw"] = True
            save_state()
            send_message(chat, f"{p.get('name', 'Girl')}: NSFW on. Adult consenting fantasy only.")
            return "OK", 200

        if low.startswith("/nsfw_off"):
            s["nsfw"] = False
            save_state()
            send_message(chat, f"{p.get('name', 'Girl')}: keeping it suggestive.")
            return "OK", 200

        if low.startswith("/spice"):
            send_message(chat, nsfw_card(p, s))
            return "OK", 200

        if low.startswith("/likes"):
            parts = text.split(maxsplit=1)
            if len(parts) < 2:
                send_message(chat, "Use: /likes coffee, films")
                return "OK", 200
            likes = [x.strip() for x in parts[1].split(",") if x.strip()]
            s["likes"] = list(dict.fromkeys((s["likes"] + likes)))[:8]
            save_state()
            send_message(chat, "Noted: " + ", ".join(s["likes"]))
            return "OK", 200

        if low.startswith("/switch"):
            s["g"] = random.randrange(len(PERS))
            save_state()
            send_message(chat, intro(PERS[s["g"]]))
            return "OK", 200

        if low.startswith("/reset"):
            s["likes"] = []
            s["u_msg"] = 0
            s["teased"] = False
            s["arousal"] = 0.0
            save_state()
            send_message(chat, "Memory cleared.")
            return "OK", 200

        if low.startswith("/status"):
            left = max(0, FREE_PER_DAY - s.get("used", 0))
            send_message(chat, "✅ Unlimited" if str(uid) == OWNER_ID else f"🧮 Free images left: {left}/{FREE_PER_DAY}")
            return "OK", 200

        if low.startswith("/diag"):
            lines = []
            test_prompt = "tiny test image of a red square"

            def attempt(label, fn):
                t0 = time.time()
                try:
                    fn()
                    lines.append(f"{label}: ✅ {time.time() - t0:.1f}s")
                except Exception as e:
                    lines.append(f"{label}: ❌ {str(e)[:160]}")

            lines.append(
                "Keys -> "
                f"FAL:{'set' if FAL_KEY else '—'} | "
                f"Replicate:{'set' if REPLICATE else '—'} | "
                f"Horde:{'set' if HORDE else '—'}"
            )

            if FAL_KEY:
                attempt("FAL", lambda: gen_fal(test_prompt, 96, 96, seed=1))
            else:
                lines.append("FAL: (skipped, no FAL_KEY)")

            if REPLICATE:
                attempt("Replicate", lambda: gen_replicate(test_prompt, 96, 96, seed=1))
            else:
                lines.append("Replicate: (skipped, no REPLICATE_API_TOKEN)")

            if HORDE:
                attempt("Horde", lambda: gen_horde(test_prompt, 96, 96, seed=1, nsfw=False))
            else:
                lines.append("Horde: (skipped, no HORDE_API_KEY)")

            lines.append("— Failover chain (generate_image) —")
            t0 = time.time()
            try:
                out_path = generate_image(test_prompt, 96, 96, seed=1, nsfw=False)
                lines.append(f"generate_image(): ✅ {time.time() - t0:.1f}s (saved {out_path})")
            except Exception as e:
                lines.append(f"generate_image(): ❌ {str(e)[:200]}")

            send_message(chat, "\n".join(lines))
            return "OK", 200

        if low.startswith("/selfie"):
            vibe = text.split(maxsplit=1)[1] if len(text.split()) > 1 else "teasing, SFW"
            if (str(uid) != OWNER_ID) and not allowed(uid):
                send_message(chat, "Free image limit hit.")
                return "OK", 200
            prompt = selfie_prompt(p, vibe, nsfw=s.get("nsfw", False))
            seed = stable_seed(p.get("name", "Girl"))
            send_message(chat, "📸 One moment…")
            try:
                fn = generate_image(prompt, nsfw=s.get("nsfw", False), seed=seed)
                send_photo(chat, fn)
                if str(uid) != OWNER_ID:
                    STATE[str(uid)]["used"] = STATE[str(uid)].get("used", 0) + 1
                    save_state()
            except Exception as e_img:
                send_message(chat, f"Image queue: {e_img}")
            return "OK", 200

        if low.startswith("/old18"):
            if (str(uid) != OWNER_ID) and not allowed(uid):
                send_message(chat, "Free image limit hit.")
                return "OK", 200
            seed = stable_seed(p.get("name", "Girl"), "old18")
            send_message(chat, "🗂️ Digging out an old (18) selfie…")
            try:
                fn = generate_image(old18_prompt(p), nsfw=False, seed=seed)
                send_photo(chat, fn)
                if str(uid) != OWNER_ID:
                    STATE[str(uid)]["used"] = STATE[str(uid)].get("used", 0) + 1
                    save_state()
            except Exception as e_old:
                send_message(chat, f"Image queue: {e_old}")
            return "OK", 200

        if low.startswith("/poster"):
            parts = text.split(maxsplit=1)
            if len(parts) < 2:
                send_message(chat, "/poster <movie>")
                return "OK", 200
            send_message(chat, "🎬 Designing poster…")
            try:
                fn = generate_image(poster_prompt(parts[1]), nsfw=False)
                send_photo(chat, fn)
            except Exception as e_pos:
                send_message(chat, f"Image queue: {e_pos}")
            return "OK", 200

        if low.startswith("/draw"):
            parts = text.split(maxsplit=1)
            if len(parts) < 2:
                send_message(chat, "/draw <subject>")
                return "OK", 200
            send_message(chat, "🎨 Sketching it…")
            try:
                fn = generate_image(art_prompt(p, parts[1]), nsfw=False)
                send_photo(chat, fn)
            except Exception as e_draw:
                send_message(chat, f"Image queue: {e_draw}")
            return "OK", 200

        if low.startswith("/gen"):
            parts = text.split(maxsplit=1)
            if len(parts) < 2:
                send_message(chat, "/gen <prompt>")
                return "OK", 200
            if not s.get("nsfw", False):
                send_message(chat, "Turn on /nsfw_on for spicy pics.")
                return "OK", 200
            if not clean_ok(parts[1]):
                send_message(chat, "I won’t generate that.")
                return "OK", 200
            if (str(uid) != OWNER_ID) and not allowed(uid):
                send_message(chat, "Free image limit hit.")
                return "OK", 200
            hint = (f"{p.get('name', 'Girl')} consistent look: {p.get('img_tags', '')}, "
                    f"{p.get('hair', '')} hair, {p.get('eyes', '')} eyes, {p.get('body', '')}")
            cup = p.get("cup")
            if cup:
                hint += f", proportions consistent with {cup}-cup bust"
            send_message(chat, "🖼️ Generating…")
            try:
                fn = generate_image(hint + ". " + parts[1], nsfw=True, seed=stable_seed(p.get('name', 'Girl')))
                send_photo(chat, fn)
                if str(uid) != OWNER_ID:
                    STATE[str(uid)]["used"] = STATE[str(uid)].get("used", 0) + 1
                    save_state()
            except Exception as e_gen:
                send_message(chat, f"Image queue: {e_gen}")
            return "OK", 200

        if text and not text.startswith("/"):
            t = text.strip()
            idx = None
            if t.isdigit():
                n = int(t)
                if 1 <= n <= len(PERS):
                    idx = n - 1
            else:
                t_low = t.lower()
                for i, pp in enumerate(PERS):
                    if pp.get("name", "").lower() == t_low:
                        idx = i
                        break

            if idx is not None:
                s["g"] = idx
                save_state()
                send_message(chat, intro(PERS[idx]))
                return "OK", 200

        if not clean_ok(text):
            send_message(chat, "Nope.")
            return "OK", 200

        ar = float(s.get("arousal", 0.0))
        slow = bool(p.get("arousal_slow", True))
        bump = 1.0 if not slow else 0.5
        if any(k in low for k in ["kiss", "hot", "sexy", "turn on", "turn-on", "blush", "moan", "wet"]):
            ar += bump
        if any(k in low for k in ["book", "music", "movie", "walk", "coffee"]):
            ar += 0.2
        ar = min(3.0, ar)
        s["arousal"] = ar
        save_state()

        if (not s.get("teased")) and s.get("u_msg", 0) >= 5:
            try:
                seed = stable_seed(p.get("name", "Girl"))
                fn = generate_image(selfie_prompt(p, vibe="teasing smile, shoulder-up, tasteful, SFW", nsfw=False),
                                    nsfw=False, seed=seed)
                send_photo(chat, fn)
                send_message(chat, "there's more of these and it only gets better ✨")
                s["teased"] = True
                save_state()
            except Exception as e_tease:
                print("TEASE ERR:", e_tease)

        fact = (p.get("origin", "") or "").split(";")[0]
        taste = random.choice([
            ", ".join((p.get("music") or [])[:1]),
            ", ".join((p.get("movies") or [])[:1]),
            ", ".join((p.get("tv") or [])[:1])
        ])
        bookline = (" " + book_snack(p)) if random.random() < 0.3 else ""
        feels = arousal_line(p, s)
        if ar < 1:
            hook = "I'm curious; what's your vibe?"
        elif ar < 2:
            hook = "...okay now I'm leaning in closer."
        elif ar < 3:
            hook = "I'm warming up—my cheeks and maybe more."
        else:
            hook = "Say one more nice thing and I might need a cold shower."

        send_message(chat, f"{p.get('name', 'Girl')} ({p.get('persona', '')}, {p.get('age', 0)}): "
                           f"\"{text[:80]}\" — {feels}. {fact}. I'm into {taste}.{bookline} {hook}")
        return "OK", 200

    except Exception as e:
        print("PROCESS ERROR:", e)
        return "OK", 200

@app.route("/", methods=["GET", "POST"])
def root():
    return "ok", 200

def set_webhook():
    try:
        requests.post(f"{API}/deleteWebhook", timeout=8)
    except:
        pass
    r = requests.post(f"{API}/setWebhook",
                      json={"url": WEBHOOK_URL, "allowed_updates": ["message", "edited_message"]}, timeout=15)
    print("SET HOOK RESP:", r.status_code, r.text)

if __name__ == "__main__":
    set_webhook()
    print("URL MAP:", app.url_map)
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)))

# app.py  (rename to main.py if you prefer)
import os, time
from flask import Flask, request
from settings import BOT_TOKEN, OWNER_ID, WEBHOOK_URL
from telegram_io import API, send_message
from state import get_user, save_state, allowed, STATE
from personas import PERS, intro, menu_list, size_line
from dialog import generate_chat_turn
from media_commands import handle_media_commands

assert BOT_TOKEN and OWNER_ID and WEBHOOK_URL, "Missing BOT_TOKEN/OWNER_ID/WEBHOOK_URL"

app = Flask(__name__)
PROCESSED = set()

@app.route("/telegram/pix3lhook", methods=["GET","POST"])
def hook():
    if request.method == "GET":
        return "hook ok", 200

    up = request.get_json(force=True, silent=True) or {}
    print("TG UPDATE RAW:", str(up)[:500])

    try:
        if "update_id" in up:
            if up["update_id"] in PROCESSED: return "OK", 200
            PROCESSED.add(up["update_id"])

        msg = up.get("message") or up.get("edited_message")
        if not msg: return "OK", 200

        chat = msg["chat"]["id"]
        uid  = msg["from"]["id"]
        text = (msg.get("text") or "").strip()
        low  = text.lower()

        if not PERS:
            send_message(chat, "No girls loaded yet.")
            return "OK", 200

        s = get_user(uid)
        s["u_msg"] += 1
        save_state()

        mid = msg.get("message_id")
        if s.get("last_msg_id") == mid: return "OK", 200
        s["last_msg_id"] = mid
        save_state()

        p = PERS[s["g"] % len(PERS)]

        # Centralized media commands
        handled = handle_media_commands(
            low, text, p, s, uid, chat,
            send_message=send_message, save_state=save_state,
            OWNER_ID=OWNER_ID, STATE=STATE
        )
        if handled: return handled

        # Simple handlers
        if low in {"hi","hello","hey","/start"}:
            send_message(chat, intro(p)); return "OK", 200
        if low.startswith("/help"):
            send_message(chat, "(try /girls, /pick #|name, /books, /nsfw_on, /selfie cozy, /gen prompt, /help)")
            return "OK", 200
        if low.startswith("/girls"):
            send_message(chat, menu_list()); return "OK", 200
        if low.startswith("/pick"):
            parts = text.split(maxsplit=1)
            if len(parts)<2: send_message(chat,"Use: /pick 1-99 or name"); return "OK", 200
            t = parts[1].strip(); idx=None
            if t.isdigit():
                n=int(t); 
                if 1<=n<=len(PERS): idx=n-1
            else:
                t_low=t.lower()
                for i,pp in enumerate(PERS):
                    if pp.get("name","").lower()==t_low: idx=i; break
            if idx is None:
                send_message(chat,"Can’t find her 😉 Try /girls"); return "OK", 200
            s["g"]=idx; save_state(); send_message(chat, intro(PERS[idx])); return "OK", 200
        if low.startswith("/who"):
            size=size_line(p)
            send_message(chat, f"Your girl: {p.get('name','Girl')} — {p.get('persona','')} ({p.get('age',0)}) from {p.get('location','')} ({size}).")
            return "OK", 200
        if low.startswith("/nsfw_on"):
            s["nsfw"]=True; save_state(); send_message(chat, f"{p.get('name','Girl')}: NSFW on. Adult consenting fantasy only."); return "OK", 200
        if low.startswith("/nsfw_off"):
            s["nsfw"]=False; save_state(); send_message(chat, f"{p.get('name','Girl')}: keeping it suggestive."); return "OK", 200
        if low.startswith("/status"):
            from settings import FREE_PER_DAY
            left = max(0, FREE_PER_DAY - s.get("used",0))
            send_message(chat, "✅ Unlimited" if str(uid)==str(OWNER_ID) else f"🧮 Free images left: {left}/{FREE_PER_DAY}")
            return "OK", 200

        # Pick by typing just the name/number
        if text and not text.startswith("/"):
            t=text.strip(); idx=None
            if t.isdigit():
                n=int(t); 
                if 1<=n<=len(PERS): idx=n-1
            else:
                t_low=t.lower()
                for i,pp in enumerate(PERS):
                    if pp.get("name","").lower()==t_low: idx=i; break
            if idx is not None:
                s["g"]=idx; save_state(); send_message(chat, intro(PERS[idx])); return "OK", 200

        # default reply
        send_message(chat, generate_chat_turn(p,s,text))
        return "OK", 200

    except Exception as e:
        print("PROCESS ERROR:", e)
        return "OK", 200

@app.route("/", methods=["GET","POST"])
def root(): return "ok", 200

def set_webhook():
    import requests
    try: requests.post(f"{API}/deleteWebhook", timeout=8)
    except: pass
    url = WEBHOOK_URL.rstrip("/")
    if not url.endswith("/telegram/pix3lhook"):
        url = url + "/telegram/pix3lhook"
    r = requests.post(f"{API}/setWebhook", json={"url": url, "allowed_updates": ["message","edited_message"]}, timeout=15)
    print("SET HOOK RESP:", r.status_code, r.text)

if __name__ == "__main__":
    from telegram_io import API
    set_webhook()
    print("Webhook set. Ready.")

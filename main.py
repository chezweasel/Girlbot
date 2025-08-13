import os, json, time, base64, requests
from flask import Flask, request

# ===== ENV (trim spaces to avoid 404s) =====
BOT_TOKEN = os.getenv("BOT_TOKEN","").strip()
OWNER_ID = os.getenv("OWNER_ID","").strip()
WEBHOOK_URL = os.getenv("WEBHOOK_URL","").strip()
HORDE_KEY = os.getenv("HORDE_API_KEY","0000000000").strip()
API = f"https://api.telegram.org/bot{BOT_TOKEN}"

# ===== Personas (renamed) =====
PERS = [
  ("Nicole","playful"),
  ("Lurleen","down home country girl"),
  ("Tia","adventurous"),
  ("Cassidy","romantic"),
  ("Carly","bold"),
  ("Kate","flirty"),
  ("Ivy","retro"),
  ("Chelsey","teasing"),
  ("Juliet","passionate"),
  ("Riley","sweet"),
  ("Scarlett","bossy"),
  ("Tessa","dreamy"),
  ("Brittany","tender"),
  ("Zoey","party"),
  ("Grace","calm")
]

# ===== Safety + limits =====
FREE_PER_DAY = 2
FORBID = {
  "teen","minor","underage","child","young-looking",
  "incest","stepbro","stepsis","rape","forced","nonconsensual",
  "bestiality","animal","beast","loli","shota",
  "real name","celebrity","celeb","revenge porn","deepfake","face swap"
}

# ===== Simple state (json file) =====
STATE_FILE = "state.json"
def load_state():
    if os.path.exists(STATE_FILE):
        try: return json.load(open(STATE_FILE))
        except: return {}
    return {}
STATE = load_state()

def save_state(): 
    try: json.dump(STATE, open(STATE_FILE,"w"))
    except: pass

def now(): return time.time()

def gu(uid):
    u = str(uid)
    if u not in STATE:
        STATE[u] = {"f":0,"g":0,"t":now(),"ok":(u==OWNER_ID),"nsfw":False}
        save_state()
    # reset daily
    if now() - STATE[u]["t"] > 86400:
        STATE[u]["f"] = 0
        STATE[u]["t"] = now()
        save_state()
    return STATE[u]

def allowed(uid):
    s = gu(uid)
    return s["ok"] or s["f"] < FREE_PER_DAY

def mark(uid):
    s = gu(uid)
    if not s["ok"]:
        s["f"] += 1
        save_state()

def names_list():
    return "\n".join(f"{i+1}. {n}" for i,(n,_) in enumerate(PERS))

def vibe(uid):
    s = gu(uid); i = s["g"] % len(PERS)
    n,d = PERS[i]
    return n,d,f"{n} vibe {d}. supportive, flirty, AI fantasy"

def clean_ok(text):
    t = (text or "").lower()
    return not any(bad in t for bad in FORBID)

# ===== Telegram helpers =====
def send_message(chat_id, text):
    r = requests.post(f"{API}/sendMessage", json={"chat_id":int(chat_id),"text":text}, timeout=15)
    print("API_SEND:", r.status_code, r.text[:180]); return r

def send_photo(chat_id, filepath):
    with open(filepath,"rb") as f:
        r = requests.post(f"{API}/sendPhoto", data={"chat_id":int(chat_id)}, files={"photo":f}, timeout=120)
    print("API_PHOTO:", r.status_code, r.text[:180]); return r

# ===== Stable Horde image gen =====
H="https://stablehorde.net/api/v2"
def horde_generate(prompt, steps=28, w=832, h=1216, nsfw=True):
    headers={"apikey":HORDE_KEY,"Client-Agent":"flirtpixel/1.0"}
    job={"prompt":prompt,"params":{"steps":steps,"width":w,"height":h,"n":1,"nsfw":nsfw},
         "r2":True,"censor_nsfw":False}
    rid=requests.post(f"{H}/generate/async",json=job,headers=headers,timeout=45).json().get("id")
    if not rid: raise RuntimeError("Horde busy; try again.")
    waited=0
    while True:
        chk=requests.get(f"{H}/generate/check/{rid}",timeout=30).json()
        if chk.get("faulted"): raise RuntimeError("Horde fault; try simpler prompt.")
        if chk.get("done"): break
        time.sleep(2); waited+=2
        if waited>180: raise TimeoutError("Horde queue slow; try later.")
    st=requests.get(f"{H}/generate/status/{rid}",timeout=45).json()
    gens=st.get("generations",[])
    if not gens: raise RuntimeError("No image returned.")
    img_b64=gens[0]["img"]; fn=f"out_{int(now())}.png"
    open(fn,"wb").write(base64.b64decode(img_b64))
    return fn

# ===== Bot logic =====
HELP = ("Commands:\n"
"hi — menu\n/girls — list\n/pick # or name — choose\n/who — current girl\n"
"/nsfw_on — enable 18+\n/nsfw_off — disable\n/gen <prompt> — image\n"
"/status — free left today\n/token <code> — unlock unlimited")

def handle_message(msg):
    chat = msg["chat"]["id"]
    text = msg.get("text","").strip()
    uid = msg["from"]["id"]
    s = gu(uid)

    lower = text.lower()

    if lower in {"hi","hello","hey","hiya"}:
        send_message(chat, "Hi 😘 Pick:\n"+names_list()+"\n"+HELP); return

    if lower.startswith("/girls"):
        send_message(chat, names_list()); return

    if lower.startswith("/pick"):
        parts = text.split(maxsplit=1)
        if len(parts)<2: send_message(chat,"Use: /pick 1-15 or name"); return
        t = parts[1].strip().lower(); idx=None
        if t.isdigit():
            n=int(t); idx = n-1 if 1<=n<=len(PERS) else None
        else:
            for i,(n,_) in enumerate(PERS):
                if n.lower()==t: idx=i; break
        if idx is None: send_message(chat,"Can’t find her 😉 Try /girls"); return
        s["g"]=idx; save_state()
        send_message(chat, f"You picked {PERS[idx][0]} 💋"); return

    if lower.startswith("/who"):
        n,_,_=vibe(uid); send_message(chat, f"Your girl: {n}."); return

    if lower.startswith("/nsfw_on"):
        s["nsfw"]=True; save_state()
        send_message(chat,"NSFW on. 18+ only. No real people/illegal content."); return

    if lower.startswith("/nsfw_off"):
        s["nsfw"]=False; save_state()
        send_message(chat,"NSFW off. Keeping it suggestive 😇"); return

    if lower.startswith("/token"):
        parts=text.split(maxsplit=1)
        if len(parts)<2: send_message(chat,"Use: /token YOUR_CODE"); return
        code=parts[1].strip()
        # simple: any non-empty code unlocks (tighten later if you want)
        if code:
            s["ok"]=True; save_state(); send_message(chat,"✅ Unlimited unlocked.")
        else:
            send_message(chat,"❌ Invalid code.")
        return

    if lower.startswith("/status"):
        left=max(0,FREE_PER_DAY-s["f"])
        send_message(chat, "✅ Unlimited" if s["ok"] else f"🧮 Free images left today: {left}/{FREE_PER_DAY}")
        return

    if lower.startswith("/gen"):
        parts=text.split(maxsplit=1)
        if len(parts)<2: send_message(chat,"/gen <prompt>"); return
        prompt=parts[1].strip()
        if not s["nsfw"]: send_message(chat,"Turn on /nsfw_on for spicy pics."); return
        if not clean_ok(prompt): send_message(chat,"I won’t generate that. Try something else."); return
        if not allowed(uid): send_message(chat,"Baby, you’ve used your free ones 😏"); return
        n,d,v=vibe(uid)
        send_message(chat,"🎨 One moment…")
        try:
            fn=horde_generate(f"{v}. {prompt}")
            send_photo(chat, fn); mark(uid)
        except Exception as e:
            send_message(chat, f"Queue/busy: {e}")
        return

    # flirty fallback chat
    if not clean_ok(text):
        send_message(chat,"Nope."); return
    n,d,_=vibe(uid)
    send_message(chat, f"{n} ({d}): I like this 😘" if not s["nsfw"]
                     else f"{n} ({d}): mm… keep going; I want details.")

# ===== Flask app + webhook =====
app = Flask(__name__)

@app.route("/")
def root(): return "ok",200

@app.route("/telegram/pix3lhook", methods=["GET","POST"])
def webhook():
    if request.method=="GET": return "hook ok",200
    update = request.get_json(force=True, silent=True) or {}
    print("TG UPDATE RAW:", str(update)[:600])
    try:
        if "message" in update: handle_message(update["message"])
        elif "edited_message" in update: handle_message(update["edited_message"])
    except Exception as e:
        print("PROCESS ERROR:", e)
    return "OK",200

def set_webhook():
    # Delete old and set new (POST with json)
    try:
        requests.post(f"{API}/deleteWebhook", timeout=10)
    except: pass
    r = requests.post(f"{API}/setWebhook", json={"url":WEBHOOK_URL,
                      "allowed_updates":["message","edited_message"]}, timeout=15)
    print("SET HOOK RESP:", r.status_code, r.text)

if __name__=="__main__":
    # sanity: make sure values are present
    assert BOT_TOKEN and OWNER_ID and WEBHOOK_URL, "Missing env vars"
    set_webhook()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT",8080)))

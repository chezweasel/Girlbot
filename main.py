import os, time, json, base64, threading, requests
from flask import Flask, render_template_string, request
from telebot import TeleBot, types

# ===== ENV =====
TG_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
OWNER_ID = os.environ["OWNER_ID"]                    # e.g. "7414541468"
PUBLIC_URL = os.environ["PUBLIC_URL"]                # e.g. https://flirtpixel.up.railway.app
WEBHOOK_SECRET = os.environ["WEBHOOK_SECRET"]        # any random string
HORDE_KEY = os.getenv("HORDE_API_KEY","0000000000")  # optional free key
TOKEN_CODES = set(x.strip() for x in os.getenv("TOKEN_CODES","").split(",") if x.strip())

# ===== SETTINGS / SAFETY =====
FREE_PER_DAY = 2
PRIVATE_ONLY = True
FORBID = {
  "minor","underage","child","young-looking","stepbro",
  "rape","forced","nonconsensual","bestiality","animal","beast","loli","shota",
  "revenge porn","deepfake"
}
PERS=[("Rochelle","playful"),("Sophia","elegant"),("Nicole","adventurous"),("Tia","romantic"),
      ("Kendra","bold"),("Cassandra","flirty"),("Ivy","retro"),("Jade","teasing"),
      ("Brittany","passionate"),("Riley","sweet"),("Scarlett","bossy"),("Tess","dreamy"),
      ("Ana","tender"),("Zoey","party"),("Chelsea","calm")]

# ===== BOT + STATE (persist) =====
bot=TeleBot(TG_TOKEN, parse_mode=None)
STATE_FILE="state.json"; STATE={}
def load_state():
    global STATE
    if os.path.exists(STATE_FILE):
        try: STATE=json.load(open(STATE_FILE)); 
        except: STATE={}
def save_state():
    try: json.dump(STATE, open(STATE_FILE,"w"))
    except: pass
def now(): return time.time()
def is_private(m): return getattr(m.chat,"type","private")=="private"
def gu(uid):
    u=str(uid)
    if u not in STATE: STATE[u]={"f":0,"g":0,"t":now(),"ok":(u==OWNER_ID),"nsfw":False}
    if now()-STATE[u]["t"]>86400: STATE[u]["f"]=0; STATE[u]["t"]=now(); save_state()
    return STATE[u]
def allowed(uid): s=gu(uid); return s["ok"] or s["f"]<FREE_PER_DAY
def mark(uid): s=gu(uid); s["f"]+=0 if s["ok"] else 1; save_state()
def clean_ok(t): return not any(w in t.lower() for w in FORBID)
def names_list(): return "\n".join(f"{i+1}. {n}" for i,(n,_) in enumerate(PERS))
def vibe(uid):
    s=gu(uid); i=s["g"]%len(PERS); n,d=PERS[i]
    return n,d,f"{n} vibe {d}. supportive, flirty, AI fantasy"

# ===== STABLE HORDE (NSFW OK, with guardrails) =====
H="https://stablehorde.net/api/v2"
def horde_generate(prompt,steps=28,w=832,h=1216,nsfw=True):
    hd={"apikey":HORDE_KEY,"Client-Agent":"tg-girlbot/1.0"}
    job={"prompt":prompt,"params":{"steps":steps,"width":w,"height":h,"n":1,"nsfw":nsfw},
         "r2":True,"censor_nsfw":False}
    rid=requests.post(f"{H}/generate/async",json=job,headers=hd,timeout=45).json().get("id")
    if not rid: raise RuntimeError("Horde rejected job or busy.")
    waited=0
    while True:
        s=requests.get(f"{H}/generate/check/{rid}",timeout=30).json()
        if s.get("faulted"): raise RuntimeError("Horde fault; try simpler prompt.")
        if s.get("done"): break
        time.sleep(2); waited+=2
        if waited>180: raise TimeoutError("Horde queue slow; try later.")
    st=requests.get(f"{H}/generate/status/{rid}",timeout=45).json()
    g=st.get("generations",[])
    if not g: raise RuntimeError("No image returned.")
    fn=f"out_{int(now())}.png"
    open(fn,"wb").write(base64.b64decode(g[0]["img"]))
    return fn

# ===== HANDLERS =====
HELP_TXT=("Commands:\n"
"hi — menu\n/girls — list\n/pick # or name — choose\n/who — show current\n"
"/nsfw_on — enable 18+\n/nsfw_off — disable\n/gen <prompt> — make pic\n"
"/status — free images left\n/token <code> — unlock unlimited")

@bot.message_handler(commands=["help","start"])
def help(m): 
    if PRIVATE_ONLY and not is_private(m): return
    bot.reply_to(m, HELP_TXT)

@bot.message_handler(func=lambda m:m.text and m.text.lower().strip() in {"hi","hello","hey","hiya"})
def greet(m):
    if PRIVATE_ONLY and not is_private(m): return
    gu(m.from_user.id)
    bot.reply_to(m,"Hi 😘 Pick:\n"+names_list()+"\n"+HELP_TXT)

@bot.message_handler(commands=["girls"])
def girls(m):
    if PRIVATE_ONLY and not is_private(m): return
    bot.reply_to(m,names_list())

@bot.message_handler(commands=["pick"])
def pick(m):
    if PRIVATE_ONLY and not is_private(m): return
    a=m.text.split(maxsplit=1)
    if len(a)<2: return bot.reply_to(m,"Use: /pick 1-15 or name")
    t=a[1].strip().lower(); idx=None
    if t.isdigit(): n=int(t); idx=n-1 if 1<=n<=len(PERS) else None
    else:
        for i,(n,_) in enumerate(PERS):
            if n.lower()==t: idx=i; break
    if idx is None: return bot.reply_to(m,"Can’t find her 😉 Try /girls")
    gu(m.from_user.id)["g"]=idx; save_state()
    bot.reply_to(m,f"You picked {PERS[idx][0]} 💋")

@bot.message_handler(commands=["who"])
def who(m):
    if PRIVATE_ONLY and not is_private(m): return
    n,_,_=vibe(m.from_user.id); bot.reply_to(m,f"Your girl: {n}.")

@bot.message_handler(commands=["nsfw_on"])
def nsfw_on(m):
    if PRIVATE_ONLY and not is_private(m): return
    gu(m.from_user.id)["nsfw"]=True; save_state()
    bot.reply_to(m,"NSFW on. 18+ only. No real people/illegal content.")

@bot.message_handler(commands=["nsfw_off"])
def nsfw_off(m):
    if PRIVATE_ONLY and not is_private(m): return
    gu(m.from_user.id)["nsfw"]=False; save_state()
    bot.reply_to(m,"NSFW off. Keeping it suggestive 😇")

@bot.message_handler(commands=["token"])
def token_cmd(m):
    if PRIVATE_ONLY and not is_private(m): return
    a=m.text.split(maxsplit=1)
    if len(a)<2: return bot.reply_to(m,"Use: /token YOUR_CODE")
    if a[1].strip() in TOKEN_CODES: gu(m.from_user.id)["ok"]=True; save_state(); bot.reply_to(m,"✅ Unlimited unlocked.")
    else: bot.reply_to(m,"❌ Invalid code.")

@bot.message_handler(commands=["status"])
def status_cmd(m):
    if PRIVATE_ONLY and not is_private(m): return
    s=gu(m.from_user.id); left=max(0,FREE_PER_DAY-s["f"])
    bot.reply_to(m,"✅ Unlimited" if s["ok"] else f"🧮 Free images left today: {left}/{FREE_PER_DAY}")

@bot.message_handler(commands=["gen"])
def gen(m):
    if PRIVATE_ONLY and not is_private(m): return
    u=str(m.from_user.id); s=gu(u); a=m.text.split(maxsplit=1)
    if len(a)<2: return bot.reply_to(m,"/gen <prompt>")
    p=a[1].strip()
    if not s["nsfw"]: return bot.reply_to(m,"Turn on /nsfw_on for spicy pics.")
    if not clean_ok(p): return bot.reply_to(m,"I won’t generate that. Try something else.")
    if not allowed(u): return bot.reply_to(m,"Baby, you’ve used your free ones 😏")
    n,d,v=vibe(u); bot.reply_to(m,"🎨 One moment…")
    try: fn=horde_generate(f"{v}. {p}"); bot.send_photo(m.chat.id,open(fn,"rb")); mark(u)
    except Exception as e: bot.reply_to(m,f"Queue/busy: {e}")

@bot.message_handler(func=lambda m:m.text and not m.text.startswith("/"))
def chatty(m):
    if PRIVATE_ONLY and not is_private(m): return
    t=m.text.strip()
    if not clean_ok(t): return bot.reply_to(m,"Nope.")
    n,d,_=vibe(m.from_user.id)
    bot.reply_to(m, f"{n} ({d}): I like this 😘" if not gu(m.from_user.id)["nsfw"]
                   else f"{n} ({d}): mm… keep going; I want details.")

# ===== WEBSITE + WEBHOOK =====
app=Flask(__name__)
HOME="""<!doctype html><html><head><meta name=viewport content="width=device-width,initial-scale=1">
<title>Girlbot</title><style>body{font-family:system-ui;background:#0f0f12;color:#eee;margin:0}
.wrap{max-width:860px;margin:0 auto;padding:40px}.card{background:#17171c;border:1px solid #2a2a33;border-radius:14px;padding:24px;margin:16px 0}
h1{font-size:28px;margin:0 0 6px}.muted{color:#aaa}.btn{display:inline-block;padding:10px 14px;border-radius:10px;background:#6b5cff;color:#fff;text-decoration:none}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px}.girl{padding:12px;background:#1d1d24;border-radius:12px;border:1px solid #2b2b34}
</style></head><body><div class=wrap><h1>AI Girlfriend Bot</h1>
<p class=muted>Telegram-first. This site shows status.</p>
<div class=card><p>Status: <b>{{status}}</b> | Horde key: <b>{{horde}}</b> | Free/day: <b>{{free}}</b></p>
<p>Commands: <code>hi</code>, <code>/pick</code>, <code>/who</code>, <code>/nsfw_on</code>, <code>/nsfw_off</code>, <code>/gen</code>, <code>/status</code>, <code>/token</code></p>
<a class=btn href="https://t.me/{{bot_username}}" target=_blank>Open Telegram Bot</a></div>
<div class=card><h3>Girls</h3><div class=grid>{% for n,d in girls %}<div class=girl><b>{{n}}</b><br><span class=muted>{{d}}</span></div>{% endfor %}</div></div>
<div class=muted>No user data shown.</div></div></body></html>"""
@app.route("/")
def home():
    try: name="@"+bot.get_me().username
    except: name="(bot offline?)"
    status="online ✅" if name.startswith("@") else "starting…"
    hk="set ✅" if HORDE_KEY!="0000000000" else "anonymous (slower)"
    return render_template_string(HOME,status=status,horde=hk,free=FREE_PER_DAY,girls=PERS,bot_username=name.strip("@"))
@app.route("/_up")
def up(): return "ok",200
@app.route(f"/telegram/{WEBHOOK_SECRET}",methods=["POST"])
def telegram():
    upd=types.Update.de_json(request.get_data().decode("utf-8"))
    bot.process_new_updates([upd]); return "ok",200

def set_webhook():
    try:
        requests.get(f"https://api.telegram.org/bot{TG_TOKEN}/deleteWebhook",timeout=10)
        requests.get(f"https://api.telegram.org/bot{TG_TOKEN}/setWebhook",
                     params={"url":f"{PUBLIC_URL}/telegram/{WEBHOOK_SECRET}"},timeout=10)
        bot.send_message(OWNER_ID,"✅ READY — webhook set")
    except Exception as e:
        print("Webhook error:",e)

if __name__=="__main__":
    load_state()
    threading.Thread(target=set_webhook,daemon=True).start()
    app.run(host="0.0.0.0",port=int(os.environ.get("PORT",8080)))

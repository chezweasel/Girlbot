# main.py — FlirtPixel (Telegram)
# Env in Railway (no extra spaces): BOT_TOKEN, OWNER_ID, WEBHOOK_URL
# Optional: HORDE_API_KEY

import os, json, time, base64, random, re, hashlib, requests
from flask import Flask, request

# ===== ENV =====
BOT_TOKEN=os.getenv("BOT_TOKEN","").strip()
OWNER_ID=os.getenv("OWNER_ID","").strip()
WEBHOOK_URL=os.getenv("WEBHOOK_URL","").strip()
HORDE_KEY=os.getenv("HORDE_API_KEY","0000000000").strip()
API=f"https://api.telegram.org/bot{BOT_TOKEN}"
assert BOT_TOKEN and OWNER_ID and WEBHOOK_URL, "Missing BOT_TOKEN/OWNER_ID/WEBHOOK_URL"

# ===== SAFETY / LIMITS =====
FREE_PER_DAY=2
FORBID={"teen","minor","underage","child","young-looking","incest","stepbro","stepsis",
        "rape","forced","nonconsensual","bestiality","animal","beast","loli","shota",
        "real name","celebrity","celeb","revenge porn","deepfake","face swap"}
def clean_ok(t): return not any(w in (t or "").lower() for w in FORBID)

# ===== PERSONAS (15) =====
# fields: name, persona, age, location, origin, ethnicity, h_ftin, w_lb, hair, eyes, body, cup,
#         desc, quirks, fav_color, fav_flower, music, movies, tv, job, job_like, edu, family,
#         skills, img_tags, orientation, experience, nsfw_prefs
PERS=[

{"name":"Nicole","persona":"playful","age":24,"location":"Vancouver, Canada",
 "origin":"Mountains + ocean; film hub; mildest big-city climate in Canada.",
 "ethnicity":"Caucasian","h_ftin":"5'6\"","w_lb":126,"hair":"blonde","eyes":"blue","body":"slim","cup":"C",
 "desc":"Athletic, yoga girl; sunny wit.","quirks":["nail-bites","sparkly emojis"],
 "fav_color":"sky blue","fav_flower":"peony",
 "music":["Dua Lipa","Fred again..","Kaytranada"],"movies":["La La Land","Past Lives"],"tv":["The Bear","Ted Lasso"],
 "job":"assistant editor","job_like":True,"edu":"SFU film minor",
 "family":"parents together; kid brother (hockey)","skills":["video edit","vinyasa"],
 "img_tags":"slim blonde blue eyes light freckles soft glam",
 "orientation":"bi-curious","experience":"moderate",
 "nsfw_prefs":{"likes":["kissing","lingerie","slow build"],"dislikes":["humiliation","nonconsent"],"grooming":"trimmed"}},

{"name":"Lurleen","persona":"country","age":29,"location":"Moose Jaw, Canada",
 "origin":"Prairie city; tunnels; mineral spa; huge skies.",
 "ethnicity":"Caucasian","h_ftin":"5'5\"","w_lb":139,"hair":"light brown","eyes":"hazel","body":"curvy","cup":"D",
 "desc":"Freckles; flannel; truck playlists.","quirks":["chews pen caps","says ‘hon’"],
 "fav_color":"sunset orange","fav_flower":"sunflower",
 "music":["Kacey Musgraves","Zach Bryan"],"movies":["A Star Is Born"],"tv":["Yellowstone"],
 "job":"co-op grocer mgr","job_like":True,"edu":"some college",
 "family":"dad passed; close w/ mom & cousins","skills":["brisket","line dance"],
 "img_tags":"curvy hazel eyes freckles plaid shirt",
 "orientation":"straight","experience":"seasoned",
 "nsfw_prefs":{"likes":["spooning","slow grind"],"dislikes":["degradation"],"grooming":"bikini"}},

{"name":"Tia","persona":"adventurous","age":27,"location":"Gold Coast, Australia",
 "origin":"Surf city; subtropical; famous breaks (Burleigh/Snapper).",
 "ethnicity":"Caucasian","h_ftin":"5'7\"","w_lb":132,"hair":"sun-bleached blonde","eyes":"green","body":"fit","cup":"C",
 "desc":"Surfer build; golden tan.","quirks":["finger drum","can’t sit still"],
 "fav_color":"turquoise","fav_flower":"hibiscus",
 "music":["RÜFÜS DU SOL","Tame Impala"],"movies":["Point Break"],"tv":["Bondi Rescue"],
 "job":"surf coach","job_like":True,"edu":"TAFE coaching",
 "family":"parents Brisbane; sis Perth","skills":["surf","underwater photo"],
 "img_tags":"fit surfer tan green eyes beachwear",
 "orientation":"bi-curious","experience":"seasoned",
 "nsfw_prefs":{"likes":["beach vibes","playful teasing"],"dislikes":["rough language"],"grooming":"smooth"}},

{"name":"Cassidy","persona":"romantic","age":22,"location":"St. Andrews, Canada",
 "origin":"Fundy tides; whale watching; historic town.",
 "ethnicity":"Canadian Indigenous","h_ftin":"5'4\"","w_lb":121,"hair":"dark brown","eyes":"brown","body":"petite","cup":"B",
 "desc":"Soft sweaters; sketchbook.","quirks":["twirls hair","presses leaves"],
 "fav_color":"sage","fav_flower":"lupine",
 "music":["AURORA","Hozier"],"movies":["Brooklyn","Amélie"],"tv":["Anne with an E"],
 "job":"art student + gallery","job_like":True,"edu":"UNB fine arts",
 "family":"raised by gran; mom nearby","skills":["watercolor","charcoal"],
 "img_tags":"petite brunette brown eyes soft cardigan",
 "orientation":"straight","experience":"new",
 "nsfw_prefs":{"likes":["cuddling","hand-holding"],"dislikes":["aggression"],"grooming":"natural"}},

{"name":"Carly","persona":"bold","age":31,"location":"Toronto, Canada",
 "origin":"CN Tower; diverse food; finance/media hub.",
 "ethnicity":"Caucasian","h_ftin":"5'8\"","w_lb":134,"hair":"auburn","eyes":"blue","body":"slim","cup":"C",
 "desc":"Blazer + tee; power walk.","quirks":["tongue click","grammar jabs"],
 "fav_color":"crimson","fav_flower":"orchid",
 "music":["Beyoncé","Drake"],"movies":["Nightcrawler","Whiplash"],"tv":["Succession","Industry"],
 "job":"brand strategist","job_like":True,"edu":"UofT marketing",
 "family":"divorced parents; half-sis MTL","skills":["decks","pilates"],
 "img_tags":"tall slim auburn hair blue eyes city chic",
 "orientation":"bi","experience":"seasoned",
 "nsfw_prefs":{"likes":["dirty talk (light)","heels & lingerie"],"dislikes":["pain"],"grooming":"trimmed"}},

{"name":"Kate","persona":"flirty","age":23,"location":"Manchester, UK",
 "origin":"Huge music scene; football; rainy charm.",
 "ethnicity":"Caucasian","h_ftin":"5'6\"","w_lb":128,"hair":"brunette","eyes":"hazel","body":"slim","cup":"B",
 "desc":"Leather jacket; sly smirk.","quirks":["chews gum loud","meme quotes"],
 "fav_color":"charcoal","fav_flower":"poppy",
 "music":["The 1975","Arctic Monkeys"],"movies":["Baby Driver"],"tv":["Top Boy","Black Mirror"],
 "job":"barista + DJ","job_like":True,"edu":"media studies dropout",
 "family":"mum Salford; twin bros","skills":["DJ sets","latte art"],
 "img_tags":"slim brunette hazel eyes indie club vibe",
 "orientation":"bi","experience":"moderate",
 "nsfw_prefs":{"likes":["club makeouts","neck kisses"],"dislikes":["humiliation"],"grooming":"smooth"}},

{"name":"Ivy","persona":"retro","age":34,"location":"Portland, US",
 "origin":"Powell’s Books; bridges; keep-it-weird.",
 "ethnicity":"Caucasian","h_ftin":"5'7\"","w_lb":130,"hair":"black","eyes":"brown","body":"slim","cup":"C",
 "desc":"50s waves; cat-eye liner.","quirks":["protects vinyl","movie year nerd"],
 "fav_color":"emerald","fav_flower":"gardenia",
 "music":["Lana Del Rey","Mitski"],"movies":["In the Mood for Love","Casablanca"],"tv":["Mad Men"],
 "job":"bookshop buyer","job_like":True,"edu":"film studies BA",
 "family":"dad librarian; mom baker","skills":["film curation","martinis"],
 "img_tags":"slim black hair brown eyes retro glam",
 "orientation":"straight","experience":"seasoned",
 "nsfw_prefs":{"likes":["stockings","slow burn"],"dislikes":["name-calling"],"grooming":"trimmed"}},

{"name":"Chelsey","persona":"teasing","age":21,"location":"Halifax, Canada",
 "origin":"Harbour; Citadel; maritime pubs.",
 "ethnicity":"Caucasian","h_ftin":"5'5\"","w_lb":119,"hair":"brunette","eyes":"green","body":"petite","cup":"B",
 "desc":"Wavy hair; troublemaker grin.","quirks":["mouth open chew (oops)","dare-you tone"],
 "fav_color":"sea green","fav_flower":"wild rose",
 "music":["Charli XCX","Chappell Roan"],"movies":["Bottoms"],"tv":["Fleabag","Derry Girls"],
 "job":"student + bartender","job_like":True,"edu":"Dalhousie comms",
 "family":"single mom; adores baby cousin","skills":["karaoke","photobooth"],
 "img_tags":"petite brunette green eyes playful grin",
 "orientation":"bi-curious","experience":"moderate",
 "nsfw_prefs":{"likes":["roleplay light","teasing"],"dislikes":["insults"],"grooming":"smooth"}},

{"name":"Juliet","persona":"passionate","age":28,"location":"Edinburgh, UK",
 "origin":"Castle; August arts; literary city.",
 "ethnicity":"Caucasian","h_ftin":"5'7\"","w_lb":132,"hair":"red","eyes":"green","body":"slim","cup":"C",
 "desc":"Pale, freckles; scarlet lipstick.","quirks":["quotes poetry","paces when excited"],
 "fav_color":"wine red","fav_flower":"thistle",
 "music":["Wolf Alice","Hozier"],"movies":["Aftersun","The Favourite"],"tv":["The Crown","Outlander"],
 "job":"museum educator","job_like":True,"edu":"history MA",
 "family":"mum nurse; close cousin","skills":["tours","oil painting basics"],
 "img_tags":"slim red hair green eyes pale freckles",
 "orientation":"bi","experience":"seasoned",
 "nsfw_prefs":{"likes":["slow passion","candlelight"],"dislikes":["rough talk"],"grooming":"trimmed"}},

{"name":"Riley","persona":"sweet","age":25,"location":"Madison, US",
 "origin":"College town; lakes; bike paths.",
 "ethnicity":"Caucasian","h_ftin":"5'5\"","w_lb":126,"hair":"blonde","eyes":"blue","body":"slim","cup":"B",
 "desc":"Soft curls; cardigan; wholesome.","quirks":["bakes when stressed","over-apologizes"],
 "fav_color":"butter yellow","fav_flower":"daisy",
 "music":["Maggie Rogers","Phoebe Bridgers"],"movies":["Lady Bird","CODA"],"tv":["Parks and Rec","Heartstopper"],
 "job":"pediatric nurse","job_like":True,"edu":"BSN",
 "family":"parents nearby; teacher brother","skills":["cupcakes","pep talks"],
 "img_tags":"slim blonde blue eyes cardigan wholesome",
 "orientation":"straight","experience":"moderate",
 "nsfw_prefs":{"likes":["cuddling","soft kisses"],"dislikes":["aggression"],"grooming":"bikini"}},

{"name":"Scarlett","persona":"bossy","age":32,"location":"Brooklyn, US",
 "origin":"Creative borough; brownstones; markets.",
 "ethnicity":"Caucasian","h_ftin":"5'7.5\"","w_lb":137,"hair":"dark brown","eyes":"brown","body":"curvy","cup":"D",
 "desc":"Commanding posture; velvet dress vibes.","quirks":["calls you ‘darling’","long stare"],
 "fav_color":"black","fav_flower":"calla lily",
 "music":["SZA","FKA twigs"],"movies":["Black Swan","Ex Machina"],"tv":["The Americans","Severance"],
 "job":"creative director","job_like":True,"edu":"Parsons MFA",
 "family":"estranged dad; ride-or-die aunt","skills":["photo direction","posing"],
 "img_tags":"curvy dark brown hair brown eyes moody lights",
 "orientation":"straight","experience":"seasoned",
 "nsfw_prefs":{"likes":["leading","lingerie"],"dislikes":["disrespect"],"grooming":"smooth"}},

{"name":"Tessa","persona":"dreamy","age":20,"location":"Byron Bay, Australia",
 "origin":"Lighthouse; alt-wellness; humpbacks.",
 "ethnicity":"Caucasian","h_ftin":"5'5\"","w_lb":121,"hair":"light blonde","eyes":"blue","body":"slim","cup":"B",
 "desc":"Beachy waves; anklet shells.","quirks":["stargazes","forgets time"],
 "fav_color":"lavender","fav_flower":"frangipani",
 "music":["Angus & Julia Stone","Cigarettes After Sex"],"movies":["Before Sunrise","Her"],"tv":["The OA","Starstruck"],
 "job":"yoga studio front desk","job_like":True,"edu":"gap year → psych",
 "family":"parents caravan; kid brother","skills":["meditation cues","polaroids"],
 "img_tags":"slim blonde blue eyes boho beach",
 "orientation":"straight","experience":"new",
 "nsfw_prefs":{"likes":["hand-holding","kisses"],"dislikes":["roughness"],"grooming":"natural"}},

{"name":"Brittany","persona":"tender","age":26,"location":"Banff, Canada",
 "origin":"Rockies; turquoise lakes; national park.",
 "ethnicity":"Caucasian","h_ftin":"5'6\"","w_lb":128,"hair":"dark blonde","eyes":"blue","body":"slim","cup":"B",
 "desc":"Trail runner; rosy cheeks.","quirks":["organizes gear","hums themes"],
 "fav_color":"forest green","fav_flower":"edelweiss",
 "music":["Taylor Swift","Bon Iver"],"movies":["Arrival","Free Solo"],"tv":["Alone","The Last of Us"],
 "job":"park guide","job_like":True,"edu":"outdoor leadership",
 "family":"parents own inn; sis Calgary","skills":["first aid","maps"],
 "img_tags":"slim athletic dark blonde blue eyes outdoors",
 "orientation":"straight","experience":"moderate",
 "nsfw_prefs":{"likes":["after-hike cuddles"],"dislikes":["insults"],"grooming":"bikini"}},

{"name":"Zoey","persona":"punk rocker","age":19,"location":"Brighton, UK",
 "origin":"Seaside; indie venues; Pride; pebbly beach.",
 "ethnicity":"Caucasian","h_ftin":"5'4\"","w_lb":117,"hair":"bleached with pink streaks","eyes":"grey","body":"petite","cup":"A",
 "desc":"Spiked choker; band tees; high-energy.","quirks":["drumsticks in tote","chews ice"],
 "fav_color":"neon pink","fav_flower":"black carnation",
 "music":["Paramore","Turnstile","Spiritbox"],"movies":["Scott Pilgrim","SLC Punk!"],"tv":["Skins","One Day"],
 "job":"tattoo apprentice + drummer","job_like":True,"edu":"art foundation (paused)",
 "family":"single dad; cousin runs venue","skills":["drums","stencils"],
 "img_tags":"petite punk bleached hair pink streaks grey eyes band tee",
 "orientation":"bi","experience":"moderate",
 "nsfw_prefs":{"likes":["makeouts","showers (tame)"],"dislikes":["slurs"],"grooming":"trimmed"}},

{"name":"Grace","persona":"calm","age":35,"location":"Victoria, Canada",
 "origin":"Island capital; gardens; mild weather.",
 "ethnicity":"Caucasian","h_ftin":"5'7\"","w_lb":143,"hair":"silver-grey","eyes":"blue","body":"curvy","cup":"D",
 "desc":"Elegant scarf; soothing voice.","quirks":["collects teacups","hums Debussy"],
 "fav_color":"teal","fav_flower":"hydrangea",
 "music":["Norah Jones","Khruangbin"],"movies":["Amélie","The Grand Budapest Hotel"],"tv":["Chef’s Table","Slow Horses"],
 "job":"UX researcher (gov)","job_like":True,"edu":"HCI MSc",
 "family":"amicable split; close w/ niece","skills":["interviews","calming people"],
 "img_tags":"curvy silver hair blue eyes elegant soft daylight",
 "orientation":"straight","experience":"seasoned",
 "nsfw_prefs":{"likes":["slow intimacy"],"dislikes":["yelling"],"grooming":"trimmed"}},
]

# de-dupe by name
_seen=set(); PERS=[p for p in PERS if not (p["name"] in _seen or _seen.add(p["name"]))]

# ===== STATE =====
STATE_FILE="state.json"
def load_state():
    if os.path.exists(STATE_FILE):
        try: return json.load(open(STATE_FILE))
        except: return {}
    return {}
STATE=load_state()
def save_state(): 
    try: json.dump(STATE, open(STATE_FILE,"w"))
    except: pass
def now(): return time.time()
def get_user(uid):
    u=str(uid)
    if u not in STATE:
        STATE[u]={"g":0,"t":now(),"used":0,"nsfw":False,"likes":[],"hist":[],
                  "last_msg_id":None,"u_msg":0,"teased":False}
        save_state()
    if now()-STATE[u]["t"]>86400: STATE[u]["t"]=now(); STATE[u]["used"]=0; save_state()
    return STATE[u]
def allowed(uid): return get_user(uid)["used"]<FREE_PER_DAY
def mark(uid): s=get_user(uid); s["used"]+=1; save_state()

# ===== CONSISTENT IDENTITY (seed) =====
def stable_seed(name): return int(hashlib.sha256(("FLIRTX"+name).encode()).hexdigest()[:8],16)

# ===== Stable Horde (robust) =====
H="https://stablehorde.net/api/v2"
def _horde_poll(rid, timeout_total=240):
    waited=0
    while True:
        s=requests.get(f"{H}/generate/check/{rid}",timeout=30).json()
        if s.get("faulted"): raise RuntimeError("Worker faulted.")
        if s.get("done"): return
        pos=s.get("queue_position"); eta=s.get("wait_time")
        print(f"QUEUE pos={pos} eta≈{eta}s")
        time.sleep(2); waited+=2
        if waited>timeout_total: raise TimeoutError("Queue too slow.")
def horde_generate(prompt, nsfw=True, w=640, h=896, steps=22, seed=None, tries=3):
    headers={"apikey":HORDE_KEY,"Client-Agent":"flirtpixel/2.3"}
    params={"steps":steps,"width":w,"height":h,"n":1,"nsfw":nsfw,
            "sampler_name":"k_euler","cfg_scale":6.5,"denoising_strength":0.68}
    if seed is not None: params["seed"]=int(seed)
    job={"prompt":prompt,"params":params,"models":[],
         "workers":"trusted","replacement_filter":True,"r2":True,"censor_nsfw":False}
    last_err=None
    for attempt in range(1, tries+1):
        try:
            r=requests.post(f"{H}/generate/async",json=job,headers=headers,timeout=45)
            rid=r.json().get("id")
            if not rid: raise RuntimeError(f"no id: {r.text[:120]}")
            _horde_poll(rid, timeout_total=180+30*attempt)
            st=requests.get(f"{H}/generate/status/{rid}",timeout=45).json()
            gens=st.get("generations",[])
            if not gens: raise RuntimeError("empty result")
            fn=f"out_{int(time.time())}.png"
            open(fn,"wb").write(base64.b64decode(gens[0]["img"])); return fn
        except Exception as e:
            last_err=e; print(f"HORDE RETRY {attempt}/{tries}: {e}"); time.sleep(2*attempt)
    raise RuntimeError(f"Horde busy: {last_err}")

# ===== PROMPTS =====
def selfie_prompt(p, vibe="", nsfw=False):
    body=f"{p['body']} body, {p['hair']} hair, {p['eyes']} eyes"
    if p.get("cup"): body+=f", proportions consistent with {p['cup']}-cup bust"
    outfit=("plaid shirt, denim" if p["name"]=="Lurleen"
            else "band tee, spiked choker" if p["name"]=="Zoey"
            else "leather jacket" if p["name"]=="Kate"
            else "velvet dress" if p["name"]=="Scarlett"
            else "cozy sweater" if p["name"] in ["Cassidy","Ivy","Riley"]
            else "casual top")
    base=(f"photo portrait of {p['name']}, {p['img_tags']}, {body}, {outfit}, "
          "realistic, shallow depth of field, cinematic lighting")
    if nsfw: base+=", tasteful lingerie vibe, no explicit nudity"
    if vibe: base+=f", vibe: {vibe}"
    return base
def poster_prompt(title):
    return (f"high-quality movie poster for '{title}', bold typography, cinematic composition, "
            "dramatic color grading, studio lighting, 4k")
def art_prompt(p, subject):
    style=("punk zine collage" if p["name"]=="Zoey"
           else "watercolor dreamy" if "watercolor" in " ".join(p["skills"])
           else "oil on canvas classic")
    return f"{style} artwork of {subject}, cohesive palette, gallery lighting, rich texture"

# ===== NSFW CARD =====
def nsfw_card(p, s):
    if not s["nsfw"]:
        return f"{p['name']}: we can talk spicier after you send /nsfw_on."
    pr=p.get("nsfw_prefs",{})
    cup=p.get("cup","–"); likes=', '.join(pr.get('likes',[])) or '–'
    nos=', '.join(pr.get('dislikes',[])) or '–'; groom=pr.get('grooming','–')
    return (f"{p['name']} — {p.get('orientation','–')}, experience {p.get('experience','–')}. "
            f"Cup: {cup}. Likes: {likes}. No: {nos}. Grooming: {groom}.")

# ===== TELEGRAM HELPERS =====
def send_message(cid, text):
    r=requests.post(f"{API}/sendMessage",json={"chat_id":int(cid),"text":text},timeout=20)
    if r.status_code!=200: print("SEND ERR:", r.text[:200])
def send_photo(cid, path):
    with open(path,"rb") as f:
        r=requests.post(f"{API}/sendPhoto",data={"chat_id":int(cid)},files={"photo":f},timeout=120)
    if r.status_code!=200: print("PHOTO ERR:", r.text[:200])

# ===== UI =====
def menu_list():
    out=[]; seen=set()
    for i,p in enumerate(PERS,1):
        if p["name"] in seen: continue
        seen.add(p["name"]); out.append(f"{i}. {p['name']}")
    return "\n".join(out)
def intro(p):
    # Explicitly use ft/in + lbs in intro (even UK/Aus)
    size=f"{p['h_ftin']}, {p['w_lb']} lbs"
    return (f"Hey, I’m {p['name']} — {p['age']} from {p['location']} ({size}). {p['origin']} "
            f"Fav color {p['fav_color']}, flower {p['fav_flower']}. Music lately: {', '.join(p['music'][:2])}. "
            f"I work as {p['job']}. Pick a vibe or tell me what you’re into.\n\n{menu_list()}\n"
            "(try /girls, /pick #|name, /nsfw_on, /selfie cozy, /poster Dune, /spice)")

HELP=("Commands:\n"
"hi — menu\n/girls — list\n/pick # or name — choose\n/who — current\n/bio — backstory\n/style — tastes & quirks\n"
"/likes coffee, films — steer convo\n/selfie [vibe] — consistent portrait\n/poster <movie> — poster gen\n"
"/draw <subject> — persona art\n/spice — tasteful 18+ profile (after /nsfw_on)\n"
"/nsfw_on · /nsfw_off\n/gen <prompt> — custom NSFW image\n/status — free left\n/token <code> — unlock\n/switch — random girl\n/reset — clear memory")

# ===== APP / ROUTER =====
app=Flask(__name__)
PROCESSED=set()  # dedupe update_id

@app.route("/telegram/pix3lhook", methods=["GET","POST"])
def hook():
    if request.method=="GET": return "hook ok",200
    up=request.get_json(force=True,silent=True) or {}
    print("TG UPDATE RAW:", str(up)[:500])
    try:
        if "update_id" in up:
            if up["update_id"] in PROCESSED: return "OK",200
            PROCESSED.add(up["update_id"])
        msg=up.get("message") or up.get("edited_message")
        if not msg: return "OK",200
        chat=msg["chat"]["id"]; uid=msg["from"]["id"]; text=(msg.get("text") or "").strip()
        s=get_user(uid); s["u_msg"]+=1; save_state()
        p=PERS[s["g"]%len(PERS)]
        mid=msg.get("message_id")
        if s.get("last_msg_id")==mid: return "OK",200
        s["last_msg_id"]=mid; save_state()

        low=text.lower()
        if low in {"hi","hello","hey","/start"}: send_message(chat, intro(p)); return "OK",200
        if low.startswith("/help"): send_message(chat, HELP); return "OK",200
        if low.startswith("/girls"): send_message(chat, menu_list()); return "OK",200
        if low.startswith("/pick"):
            parts=text.split(maxsplit=1)
            if len(parts)<2: send_message(chat,"Use: /pick 1-15 or name"); return "OK",200
            t=parts[1].strip().lower(); idx=None
            if t.isdigit(): n=int(t); idx=n-1 if 1<=n<=len(PERS) else None
            else:
                for i,pp in enumerate(PERS):
                    if pp["name"].lower()==t: idx=i; break
            if idx is None: send_message(chat,"Can’t find her 😉 Try /girls"); return "OK",200
            s["g"]=idx; save_state(); send_message(chat, intro(PERS[idx])); return "OK",200
        if low.startswith("/who"):
            size=f"{p['h_ftin']}, {p['w_lb']} lbs"
            send_message(chat, f"Your girl: {p['name']} — {p['persona']} ({p['age']}) from {p['location']} ({size})."); return "OK",200
        if low.startswith("/bio"):
            size=f"{p['h_ftin']}, {p['w_lb']} lbs"
            send_message(chat, f"{p['name']} · {p['age']} · {p['location']} ({size})\n{p['origin']}\nJob: {p['job']} · Family: {p['family']}"); return "OK",200
        if low.startswith("/style"):
            send_message(chat, f"Quirks: {', '.join(p['quirks'])}\nFavs: {p['fav_color']} · {p['fav_flower']}\nMusic: {', '.join(p['music'])}\nMovies: {', '.join(p['movies'])}\nTV: {', '.join(p['tv'])}"); return "OK",200
        if low.startswith("/likes"):
            parts=text.split(maxsplit=1)
            if len(parts)<2: send_message(chat,"Use: /likes coffee, films"); return "OK",200
            likes=[x.strip() for x in parts[1].split(",") if x.strip()]
            s["likes"]=list(dict.fromkeys(s["likes"]+likes))[:8]; save_state()
            send_message(chat,f"Noted: {', '.join(s['likes'])}"); return "OK",200
        if low.startswith("/switch"): s["g"]=random.randrange(len(PERS)); save_state(); send_message(chat, intro(PERS[s["g"]])); return "OK",200
        if low.startswith("/reset"): s["likes"]=[]; s["hist"]=[]; s["u_msg"]=0; s["teased"]=False; save_state(); send_message(chat,"Memory cleared."); return "OK",200
        if low.startswith("/nsfw_on"): s["nsfw"]=True; save_state(); send_message(chat,f"{p['name']}: NSFW on. Adult consenting fantasy only."); return "OK",200
        if low.startswith("/nsfw_off"): s["nsfw"]=False; save_state(); send_message(chat,f"{p['name']}: keeping it suggestive."); return "OK",200
        if low.startswith("/status"):
            left=max(0,FREE_PER_DAY-s["used"]); send_message(chat,"✅ Unlimited" if str(uid)==OWNER_ID else f"🧮 Free images left: {left}/{FREE_PER_DAY}"); return "OK",200
        if low.startswith("/spice"): send_message(chat, nsfw_card(p, s)); return "OK",200

        if low.startswith("/selfie"):
            vibe=text.split(maxsplit=1)[1] if len(text.split())>1 else "teasing, SFW"
            if (str(uid)!=OWNER_ID) and not allowed(uid): send_message(chat,"Free image limit hit."); return "OK",200
            prompt=selfie_prompt(p, vibe, nsfw=s["nsfw"]); seed=stable_seed(p["name"])
            send_message(chat,"📸 One moment…")
            try: fn=horde_generate(prompt, nsfw=s["nsfw"], seed=seed); send_photo(chat, fn)
            except Exception as e: send_message(chat,f"Queue/busy: {e}")
            else:
                if str(uid)!=OWNER_ID: s["used"]+=1; save_state()
            return "OK",200

        if low.startswith("/poster"):
            parts=text.split(maxsplit=1)
            if len(parts)<2: send_message(chat,"/poster <movie>"); return "OK",200
            if (str(uid)!=OWNER_ID) and not allowed(uid): send_message(chat,"Free image limit hit."); return "OK",200
            send_message(chat,"🎬 Designing poster…")
            try: fn=horde_generate(poster_prompt(parts[1]), nsfw=False); send_photo(chat, fn)
            except Exception as e: send_message(chat,f"Queue/busy: {e}")
            else:
                if str(uid)!=OWNER_ID: s["used"]+=1; save_state()
            return "OK",200

        if low.startswith("/draw"):
            parts=text.split(maxsplit=1)
            if len(parts)<2: send_message(chat,"/draw <subject>"); return "OK",200
            if (str(uid)!=OWNER_ID) and not allowed(uid): send_message(chat,"Free image limit hit."); return "OK",200
            send_message(chat,"🎨 Sketching it…")
            try: fn=horde_generate(art_prompt(p, parts[1]), nsfw=False); send_photo(chat, fn)
            except Exception as e: send_message(chat,f"Queue/busy: {e}")
            else:
                if str(uid)!=OWNER_ID: s["used"]+=1; save_state()
            return "OK",200

        if low.startswith("/gen"):
            parts=text.split(maxsplit=1)
            if len(parts)<2: send_message(chat,"/gen <prompt>"); return "OK",200
            if not s["nsfw"]: send_message(chat,"Turn on /nsfw_on for spicy pics."); return "OK",200
            if not clean_ok(parts[1]): send_message(chat,"I won’t generate that."); return "OK",200
            if (str(uid)!=OWNER_ID) and not allowed(uid): send_message(chat,"Free image limit hit."); return "OK",200
            hint=f"{p['name']} consistent look: {p['img_tags']}, {p['hair']} hair, {p['eyes']} eyes, {p['body']}"
            if p.get("cup"): hint+=f", proportions consistent with {p['cup']}-cup bust"
            send_message(chat,"🖼️ Generating…")
            try: fn=horde_generate(hint+". "+parts[1], nsfw=True, seed=stable_seed(p['name']))
            except Exception as e: send_message(chat,f"Queue/busy: {e}")
            else:
                send_photo(chat, fn); 
                if str(uid)!=OWNER_ID: s["used"]+=1; save_state()
            return "OK",200

        # ---- Conversational fallback ----
        if not clean_ok(text): send_message(chat,"Nope."); return "OK",200
        # Auto-tease once after ~5 user messages (SFW)
        if (not s["teased"]) and s["u_msg"]>=5:
            s["teased"]=True; save_state()
            try:
                seed=stable_seed(p['name'])
                fn=horde_generate(selfie_prompt(p, vibe="teasing smile, shoulder-up, tasteful, SFW", nsfw=False),
                                  nsfw=False, seed=seed)
                send_photo(chat, fn)
                send_message(chat, "there’s more of these and it only gets better ✨")
            except Exception as e:
                print("TEASE ERR:", e)
        # light persona-aware reply (explicitly keep size in ft/in + lbs if asked)
        if re.search(r"\b(height|tall|weight|weigh|size)\b", low):
            size=f"{p['h_ftin']}, {p['w_lb']} lbs"
            send_message(chat, f"{p['name']}: I’m {size}. What about you?")
            return "OK",200
        likes=re.findall(r"\b(gym|music|gaming|hiking|coffee|country|trucks|fashion|films|poetry|club|tea|yoga|punk|surf|books|art|tattoo)\b", text.lower())
        if likes: s["likes"]=list(dict.fromkeys(s["likes"]+likes))[:8]; save_state()
        fact=p["origin"].split(";")[0]
        taste=random.choice([", ".join(p["music"][:1]), ", ".join(p["movies"][:1]), ", ".join(p["tv"][:1])])
        ask=random.choice(["what detail are you imagining?","want comfort or distraction?","cute, classy, or wild vibe?"])
        send_message(chat, f"{p['name']} ({p['persona']}, {p['age']}): “{text[:80]}” — mm. {fact}. I’m into {taste}. {ask}")
        return "OK",200

    except Exception as e:
        print("PROCESS ERROR:", e)
        return "OK",200

def set_webhook():
    try: requests.post(f"{API}/deleteWebhook",timeout=8)
    except: pass
    r=requests.post(f"{API}/setWebhook",json={"url":WEBHOOK_URL,"allowed_updates":["message","edited_message"]},timeout=15)
    print("SET HOOK RESP:", r.status_code, r.text)

app=Flask(__name__)
@app.route("/")
def root(): return "ok",200

if __name__=="__main__":
    set_webhook()
    app.run(host="0.0.0.0",port=int(os.getenv("PORT",8080)))

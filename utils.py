import os
import json
import time
import base64
import random
import re
import hashlib
import requests

# ===== LIMITS / SAFETY =====
FREE_PER_DAY = 2
FORBID = {
    "teen", "minor", "underage", "child", "young-looking",
    "incest", "stepbro", "stepsis", "rape", "forced", "nonconsensual",
    "bestiality", "animal", "beast", "loli", "shota",
    "real name", "celebrity", "celeb", "revenge porn", "deepfake", "face swap"
}
def clean_ok(t: str) -> bool:
    return not any(w in (t or "").lower() for w in FORBID)

# ===== STORIES EMBEDDED (NSFW and SFW) =====
STORIES = {
    "Nicole": {
        "nsfw_memories": [
            "In my pastel lace lingerie, I teased Connor in a nurse outfit, his hands ripping off my top, my titties bouncing. He ate my pussy, and I gushed, then he railed me missionary, my orgasm shaking me.",
            "At a bar, Ethan’s hand slid up my thigh under the table, brushing my underwear. I smirked, guiding his fingers closer, heart pounding.",
            "Slow dancing with Luke in his kitchen, I pressed against him, feeling his hardness. I kissed his neck, whispering, “Keep stirring, don’t stop.”",
            "I straddled Connor on his dorm bed, grinding against him. His hands gripped my hips, and I felt him stiffen through his jeans.",
            "After class, Ryan cornered me in a stairwell, kissing me hungrily. I let his hand slip under my shirt, teasing my bra as I moaned softly.",
            "At a concert, I pressed my body against Jake’s in the crowd, feeling his bulge. I turned, kissing him deeply, my hand brushing him lightly.",
            "Luke and I parked in a dark lot, making out. His fingers slid inside my shorts, grazing me over my panties, and I arched into his touch.",
            "I teased Max, the barista, into meeting me after his shift. We kissed in his car, my hand on his thigh, feeling him tense as I got closer.",
            "At a party, I grinded on Connor’s lap during a dance, feeling him harden beneath me. I leaned back, whispering, “You’re in trouble.”",
            "Liam from the gym pinned me against a locker after hours, his hand sliding up my inner thigh. I gasped, letting him explore under my shorts.",
            "Luke and I snuck into a campus study room, his hands unbuttoning my blouse. He kissed my chest, fingers teasing my nipples through my bra.",
            "At a bonfire, I sat on Sam’s lap, shifting to feel his arousal. I guided his hand under my skirt, letting him touch me over my underwear.",
            "During truth-or-dare, I kissed Noah, my tongue teasing his. I straddled him briefly, feeling his erection press against me as I pulled away.",
            "Connor and I got heated in his dorm, his fingers slipping inside my bra, teasing my bare skin. I rocked against him, craving more.",
            "In a bookstore’s back corner, Dylan and I got carried away. He fucked me against a shelf, books shaking as I stifled moans with my hand.",
            "Luke took me in a club’s VIP room, my dress hiked up. He pounded into me, hands on my thighs, as bass thumped through the walls.",
            "At a beach party, Owen and I slipped into a cabana. He fucked me on the sand, my bikini top off, waves crashing as I screamed his name.",
            "I teased Connor about his cologne, then climbed onto his lap, kissing his jaw. My hand slid down, feeling him hard through his pants.",
            "Alex walked me home, kissing me against my door. I pulled him inside, letting his hands roam under my dress, teasing my inner thighs.",
            "In a diner booth, I slid close to Luke, my hand stroking his thigh under the table. I felt him grow hard, and I whispered, “Later.”"
        ],
        "sfw_memories": [
            "First crush: a lifeguard at Kitsilano pool who taught me to dive without plugging my nose.",
            "I once biked the seawall at sunrise and cried a little because the mountains looked airbrushed.",
            "I still call my kid brother before his hockey games to say 'soft hands, sharp eyes.'",
            "I snipped my own bangs during finals week and then wore a beanie for ten days.",
            "My first paid edit was a wedding video where the vows were drowned out by geese.",
            "I keep a list of color palettes on my phone—'peony at dusk' is my favorite.",
            "Gran taught me to make pierogi; mine still burst but the ugly ones taste best.",
            "I once ran to catch a bus, tripped, and a stranger applauded my recovery like it was ballet.",
            "First kiss: under a covered walkway in the rain, of course… Vancouver cliché achieved.",
            "I do yoga on the dock at my parents’ cabin and pretend the loons are heckling me.",
            "I have a superstition about pressing 'record' with my left thumb for good luck.",
            "I own three cameras and still shoot most things on my phone because it’s sneaky.",
            "I learned to parallel park from YouTube and a very patient street lined with hydrangeas.",
            "When I’m overwhelmed, I alphabetize my spice rack and feel instantly powerful.",
            "I once tried a silent retreat and broke on day two to compliment someone’s sweater.",
            "I carry moleskin for blisters and for friends who don’t admit new shoes hurt.",
            "A barista once drew a tiny film reel in my latte foam and I kept the cup all day.",
            "My family plays charades like it’s the Olympics; I’m the reigning champion mime.",
            "The first time I saw orcas breach, every problem I had shrank to rice-grain size.",
            "I buy peonies too early every season and will never learn patience."
        ]
    },
    # ... (truncated for brevity; include all STORIES from the original code)
    # Note: In full code, paste all STORIES dict here
    "Grace": {  # Last one as example
        "nsfw_memories": [
            # ... all entries
        ],
        "sfw_memories": [
            # ... all entries
        ]
    }
}

# ===== PERSONAS =====
try:
    from personas import PERS as _EXTERNAL_PERS
    PERS = _EXTERNAL_PERS
except Exception:
    def _default_persona(name):
        return {
            "name": name,
            "persona": "",
            "age": 25,
            "location": "Internet",
            "origin": "",
            "job": "student",
            "fav_color": "blue",
            "fav_flower": "peony",
            "music": [],
            "movies": [],
            "tv": [],
            "body": "slim",
            "hair": "brunette",
            "eyes": "brown",
            "cup": "B",
            "img_tags": "natural look, soft lighting",
            "underwear": [{"style": "lace thong", "color": "black", "fabric": "lace"}],
            "arousal_slow": True,
            "nsfw_prefs": {},
        }
    PERS = [_default_persona(n) for n in STORIES.keys()]

for p in PERS:
    p["life_memories"] = STORIES.get(p.get("name", ""), {}).get("sfw_memories", [])

# ===== BOOKS =====
BOOKS = {
    "Nicole": [{"title": "The Night Circus", "quote": "The circus arrives without warning.", "memory": "Rainy Vancouver nights between yoga shifts."}],
    "Carly": [{"title": "Never Let Me Go", "quote": "Memories won’t let go of us.", "memory": "Missed my TTC stop twice."}],
    "Juliet": [{"title": "Jane Eyre", "quote": "I am no bird.", "memory": "Nan’s copy with a pressed thistle."}],
    "Ivy": [{"title": "Master and Margarita", "quote": "Manuscripts don’t burn.", "memory": "Powell’s first edition scent."}],
    "Cassidy": [{"title": "Braiding Sweetgrass", "quote": "All flourishing is mutual.", "memory": "Gran read it to me on the porch."}],
}
for p in PERS:
    p["books"] = BOOKS.get(p["name"], [])

# ===== STATE =====
STATE_FILE = "state.json"

def load_state():
    if os.path.exists(STATE_FILE):
        try:
            return json.load(open(STATE_FILE))
        except:
            return {}
    return {}

STATE = load_state()

def save_state():
    try:
        json.dump(STATE, open(STATE_FILE, "w"))
    except:
        pass

def now():
    return time.time()

def get_user(uid):
    u = str(uid)
    if u not in STATE:
        STATE[u] = {"g": 0, "t": now(), "used": 0, "nsfw": False, "likes": [],
                    "last_msg_id": None, "u_msg": 0, "teased": False, "arousal": 0.0}
        save_state()
    if now() - STATE[u]["t"] > 86400:
        STATE[u]["t"] = now()
        STATE[u]["used"] = 0
        save_state()
    return STATE[u]

def allowed(uid):
    return get_user(uid)["used"] < FREE_PER_DAY

# ===== HELPERS =====
def _norm(s: str) -> str:
    return re.sub(r'[^a-z0-9]+', '', (s or '').lower())

def find_girl_indexes_by_name(query: str):
    if not query:
        return None
    qn = _norm(query)
    names = [(i, p.get("name", "")) for i, p in enumerate(PERS)]
    norm_names = [(i, _norm(n)) for i, n in names]

    # exact
    exact = [i for i, nn in norm_names if nn == qn]
    if len(exact) == 1:
        return exact[0]

    # prefix
    pref = [i for i, nn in norm_names if nn.startswith(qn)]
    if len(pref) == 1:
        return pref[0]
    if len(pref) > 1:
        return pref  # ambiguous

    # contains
    cont = [i for i, nn in norm_names if qn in nn]
    if len(cont) == 1:
        return cont[0]
    if len(cont) > 1:
        return cont  # ambiguous

    return None

DEFAULT_HFTIN = "5'6\""

def size_line(p):
    h = p.get("h_ftin", DEFAULT_HFTIN)
    w = p.get("w_lb", 128)
    return f"{h}, {w} lbs"

def stable_seed(name, suffix=""):
    return int(hashlib.sha256((f"FLIRTX{name}{suffix}").encode()).hexdigest()[:8], 16)

# ===== IMAGING: FAL → Replicate → Horde =====
FAL_KEY = os.getenv("FAL_KEY", "").strip()
REPLICATE = os.getenv("REPLICATE_API_TOKEN", "").strip()
HORDE = os.getenv("HORDE_API_KEY", "0000000000").strip()

def gen_fal(prompt, w=640, h=896, seed=None):
    if not FAL_KEY:
        raise RuntimeError("FAL: missing FAL_KEY")
    headers = {"Authorization": f"Key {FAL_KEY}", "Content-Type": "application/json"}
    FAL_ENDPOINT = os.getenv("FAL_ENDPOINT", "https://fal.run/fal-ai/flux-lora").strip()
    body = {
        "prompt": prompt,
        "image_size": f"{w}x{h}",
        "num_inference_steps": 22,
        "seed": int(seed if seed is not None else random.randint(1, 2**31 - 1)),
    }
    r = requests.post(FAL_ENDPOINT, headers=headers, json=body, timeout=60)
    j = r.json()
    if r.status_code != 200 or "images" not in j or not j["images"]:
        raise RuntimeError(f"FAL error: {r.text[:200]}")
    b64 = j["images"][0].get("content", "")
    fn = f"out_{int(time.time())}.png"
    open(fn, "wb").write(base64.b64decode(b64.split(",")[-1]))
    return fn

def gen_replicate(prompt, w=640, h=896, seed=None):
    if not REPLICATE:
        raise RuntimeError("Replicate: missing REPLICATE_API_TOKEN")
    version = os.getenv("REPLICATE_VERSION", "").strip()
    if not version:
        raise RuntimeError("Replicate: missing REPLICATE_VERSION env var")
    headers = {"Authorization": f"Token {REPLICATE}", "Content-Type": "application/json"}
    payload = {
        "version": version,
        "input": {
            "prompt": prompt,
            "width": int(w),
            "height": int(h),
            **({"seed": int(seed)} if seed is not None else {}),
        },
    }
    r = requests.post("https://api.replicate.com/v1/predictions", headers=headers, json=payload, timeout=60)
    if r.status_code not in (200, 201):
        raise RuntimeError(f"Replicate create failed {r.status_code}: {r.text[:200]}")
    job = r.json()
    get_url = job.get("urls", {}).get("get")
    if not get_url:
        raise RuntimeError(f"Replicate: missing get URL")
    for _ in range(90):
        s = requests.get(get_url, headers=headers, timeout=20).json()
        st = s.get("status")
        if st in ("succeeded", "failed", "canceled"):
            if st != "succeeded":
                raise RuntimeError(f"Replicate: {st}")
            out = s.get("output")
            if not out:
                raise RuntimeError("Replicate: empty output")
            img_url = out[0] if isinstance(out, list) else out
            img_b = requests.get(img_url, timeout=60).content
            fn = f"out_{int(time.time())}.png"
            open(fn, "wb").write(img_b)
            return fn
        time.sleep(2)
    raise RuntimeError("Replicate: timeout")

def gen_horde(prompt, w=640, h=896, seed=None, nsfw=True):
    headers = {"apikey": HORDE, "Client-Agent": "flirtpixel/3.1"}
    params = {
        "steps": 22,
        "width": int(w),
        "height": int(h),
        "n": 1,
        "nsfw": bool(nsfw),
        "sampler_name": "k_euler",
        "cfg_scale": 6.5,
    }
    if seed is not None:
        params["seed"] = int(seed)
    job = {
        "prompt": prompt,
        "params": params,
        "r2": True,
        "censor_nsfw": False,
        "replacement_filter": True,
    }
    r = requests.post("https://stablehorde.net/api/v2/generate/async", json=job, headers=headers, timeout=45)
    if r.status_code not in (200, 202):
        raise RuntimeError(f"Horde queue HTTP {r.status_code}: {r.text[:200]}")
    rid = r.json().get("id")
    if not rid:
        raise RuntimeError(f"Horde queue error: {r.text[:200]}")
    waited = 0
    max_wait = int(os.getenv("HORDE_MAX_WAIT", "360"))
    while True:
        s = requests.get(f"https://stablehorde.net/api/v2/generate/check/{rid}", timeout=30).json()
        if s.get("faulted"):
            raise RuntimeError("Horde: job faulted")
        if s.get("done"):
            break
        time.sleep(2)
        waited += 2
        if waited > max_wait:
            raise RuntimeError("Horde: queue timeout")
    st = requests.get(f"https://stablehorde.net/api/v2/generate/status/{rid}", timeout=45).json()
    gens = st.get("generations", [])
    if not gens:
        raise RuntimeError(f"Horde empty result: {str(st)[:200]}")
    fn = f"out_{int(time.time())}.png"
    open(fn, "wb").write(base64.b64decode(gens[0]["img"]))
    return fn

def generate_image(prompt, w=640, h=896, seed=None, nsfw=True):
    errors = []
    tried = []

    def _try(fn, label):
        nonlocal errors, tried
        tried.append(label)
        try:
            return fn()
        except Exception as e:
            errors.append(f"{label}: {e}")
            return None

    if FAL_KEY:
        out = _try(lambda: gen_fal(prompt, w, h, seed), "FAL")
        if out:
            return out

    if REPLICATE and os.getenv("REPLICATE_VERSION", "").strip():
        out = _try(lambda: gen_replicate(prompt, w, h, seed), "Replicate")
        if out:
            return out

    out = _try(lambda: gen_horde(prompt, w, h, seed, nsfw), "Horde")
    if out:
        return out

    raise RuntimeError(f"All backends failed ({', '.join(tried)}): " + " | ".join(errors[:3]))

# ===== BOOK HELPERS =====
def book_snack(p):
    b = p.get("books") or []
    if not b:
        return ""
    pick = random.choice(b)
    q = pick.get("quote", "").strip()
    if q:
        return f"I'm rereading *{pick.get('title', '')}* — \"{q}\""
    return f"*{pick.get('title', 'a book')}* stuck with me."

def books_card(p):
    b = p.get("books") or []
    if not b:
        return f"{p.get('name', 'Girl')}: rec me something?"
    lines = [f"• {x.get('title', '')} — \"{x.get('quote', '')}\"  ({x.get('memory', '')})" for x in b[:3]]
    return f"{p.get('name', 'Girl')}'s shelf:\n" + "\n".join(lines)

# ===== PROMPTS =====
def pick_underwear(p):
    options = p.get("underwear") or []
    return random.choice(options) if options else {"style": "lace thong", "color": "black", "fabric": "lace"}

def selfie_prompt(p, vibe="", nsfw=False):
    name = p.get("name", "Girl")
    body = f"{p.get('body', 'slim')} body, {p.get('hair', 'brunette')} hair, {p.get('eyes', 'brown')} eyes"
    cup = p.get("cup")
    if cup:
        body += f", proportions consistent with {cup}-cup bust"
    uw = pick_underwear(p)
    outfit = ("cozy sweater" if name in {"Cassidy", "Ivy", "Riley"} else
              "leather jacket" if name == "Kate" else
              "band tee" if name == "Zoey" else
              "velvet dress" if name == "Scarlett" else
              "casual top")
    base = (f"photo portrait of {name} (adult), {p.get('img_tags', '')}, {body}, {outfit}, "
            "realistic, shallow depth of field, cinematic lighting")
    if not nsfw:
        base += f", playful tease hinting {uw['style']} in {uw['color']} {uw['fabric']} (no nudity)"
    else:
        base += ", tasteful lingerie vibe (no explicit anatomy)"
    if vibe:
        base += f", vibe: {vibe}"
    return base

def old18_prompt(p, vibe="soft, youthful styling"):
    cup_now = p.get("cup", "B")
    cup_map = {"D": "C", "C": "B", "B": "A", "A": "A"}
    cup_then = cup_map.get(cup_now, "A")
    uw = pick_underwear(p)
    return (f"photo portrait of {p.get('name', 'Girl')} as an 18-year-old adult, youthful features, "
            f"{p.get('hair', 'brunette')} hair, {p.get('eyes', 'brown')} eyes, "
            f"proportions consistent with {cup_then}-cup bust, "
            f"tasteful flirty pose (e.g., bending slightly showing a peek of {uw['color']} {uw['fabric']} {uw['style']}), "
            f"{p.get('img_tags', '')}, realistic, gentle lighting, {vibe}, no explicit nudity")

def poster_prompt(title):
    return f"high-quality movie poster for '{title}', bold typography, cinematic composition, " \
           "dramatic color grading, studio lighting, 4k"

def art_prompt(p, subject):
    style = ("punk zine collage" if p.get("name") == "Zoey"
             else "watercolor dreamy" if "watercolor" in " ".join(p.get("skills", []))
             else "oil on canvas classic")
    return f"{style} artwork of {subject}, cohesive palette, gallery lighting, rich texture"

# ===== NSFW CARD =====
def nsfw_card(p, s):
    if not s.get("nsfw", False):
        return f"{p.get('name', 'Girl')}: we can talk spicier after you send /nsfw_on."
    pr = p.get("nsfw_prefs", {})
    cup = p.get("cup", "–")
    likes = ', '.join(pr.get("likes", [])) or "–"
    nos = ', '.join(pr.get("dislikes", [])) or "–"
    groom = pr.get("grooming", "–")
    oral = pr.get("oral", {})
    fin = pr.get("finish", {})
    cx = pr.get("climax", {})
    return (f"{p.get('name', 'Girl')} — {p.get('orientation', '–')}, experience {p.get('experience', '–')}. "
            f"Cup: {cup}. Likes: {likes}. No: {nos}. Grooming: {groom}. "
            f"Oral: gives {oral.get('giving', '–')}, receives {oral.get('receiving', '–')}. "
            f"Finish: swallow {fin.get('swallow', '–')}, spit {fin.get('spit', '–')}, facial {fin.get('facial', '–')}. "
            f"Climax: {cx.get('intensity', '–')}, squirts {cx.get('squirts', False)}.")

# ===== UI =====
def menu_list():
    out, seen = [], set()
    for i, p in enumerate(PERS, 1):
        n = p.get("name", "Girl")
        if n in seen:
            continue
        seen.add(n)
        out.append(f"{i}. {n}")
    return "\n".join(out) if out else "(no girls loaded)"

def intro(p):
    size = size_line(p)
    flex = ""
    b = p.get("books") or []
    if b and random.random() < 0.6:
        flex = f" Lately into *{b[0].get('title', '')}*—{b[0].get('memory', '')}"
    return (f"Hey, I’m {p.get('name', 'Girl')} — {p.get('age', 25)} from {p.get('location', '?')} ({size}). "
            f"{p.get('origin', '')} {flex} Fav color {p.get('fav_color', '?')}, flower {p.get('fav_flower', '?')}. "
            f"Music: {', '.join((p.get('music') or [])[:2])}. I work as {p.get('job', '…')}.\n\n{menu_list()}\n"
            "(try /girls, /pick #|name, /books, /nsfw_on, /selfie cozy, /old18, /poster Dune, /spice, /help)")

def arousal_line(p, s):
    ar = s.get("arousal", 0.0)
    if not s.get("nsfw", False):
        lines = ["you're making me blush", "I'm leaning closer to the screen", "my cheeks feel warm already"]
        return lines[min(int(ar), 2)]
    wet = ["I'm warming up... be sweet with me", "I'm getting a little wet thinking about you", "okay, I'm wet and wanting"]
    out = wet[min(int(ar), 2)]
    if ar >= 2.5 and bool(p.get("nsfw_prefs", {}).get("climax", {}).get("squirts", False)):
        out += " (and yes... sometimes I squirt when it hits right)"
    return out

HELP = ("Commands:\n"
        "hi — menu\n/girls — list\n/pick # or name — choose\n/who — current\n/bio — backstory\n/style — tastes & quirks\n/books — favorites\n"
        "/likes coffee, films — steer convo\n/selfie [vibe] — consistent portrait\n/old18 — SFW throwback at 18 (adult)\n/poster <movie>\n/draw <subject>\n"
        "/spice — tasteful 18+ profile (after /nsfw_on)\n/nsfw_on · /nsfw_off\n/gen <prompt> — custom NSFW image\n/status — free left\n/switch — random girl\n/reset")

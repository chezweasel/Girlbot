import random

# Stable seed (optional). If settings.py missing, we fall back.
try:
    from settings import stable_seed as _stable_seed
except Exception:
    def _stable_seed(*parts) -> int:
        s = "|".join(str(p) for p in parts)
        return abs(hash(s)) % (2**31)

# Load stories (SFW/NSFW memories). If missing, we continue safely.
try:
    from stories import STORIES
except Exception:
    STORIES = {}

# -------- Persona roster (15), names match your stories keys --------
NAMES = [
    "Nicole","Lurleen","Tia","Cassidy","Carly","Kate","Ivy","Chelsey",
    "Juliet","Riley","Scarlett","Tessa","Brittany","Zoey","Grace"
]

# Helper to pick deterministic choices
def _pick(name: str, seq):
    if not seq: return None
    rnd = random.Random(_stable_seed(name, "pick"))
    return seq[rnd.randrange(len(seq))]

# Minimal datasets for parameters (clean, non-graphic)
ETHNICITIES = {
    # Most Caucasian, 1 Indigenous Canadian, 1 Black, 1 Japanese-descent American (names are kept per your request)
    "Nicole": "Caucasian",
    "Lurleen": "Caucasian",
    "Tia": "Caucasian (Australian)",
    "Cassidy": "Caucasian",
    "Carly": "Caucasian",
    "Kate": "Caucasian (UK)",
    "Ivy": "Black (Canadian)",                # changed ethnicity
    "Chelsey": "Caucasian",
    "Juliet": "Caucasian (UK)",
    "Riley": "Caucasian",
    "Scarlett": "Caucasian",
    "Tessa": "Caucasian",
    "Brittany": "Caucasian",
    "Zoey": "Caucasian (US)",
    "Grace": "Indigenous Canadian (Mi'kmaq)", # changed ethnicity
}

HOMETOWNS = {
    "Nicole":"Vancouver, Canada",
    "Lurleen":"Saskatoon, Canada",
    "Tia":"Byron Bay, Australia",
    "Cassidy":"St. Andrews, Canada",
    "Carly":"Toronto, Canada",
    "Kate":"Manchester, UK",
    "Ivy":"Toronto, Canada",
    "Chelsey":"Halifax, Canada",
    "Juliet":"Edinburgh, UK",
    "Riley":"Seattle, USA",
    "Scarlett":"Montreal, Canada",
    "Tessa":"Melbourne, Australia",
    "Brittany":"Banff, Canada",
    "Zoey":"Brooklyn, USA",
    "Grace":"Halifax, Canada",
}

JOBS = {
    "Nicole":"Student / videography",
    "Lurleen":"Operations / co-op organizer",
    "Tia":"Surf instructor",
    "Cassidy":"Art student / gallery volunteer",
    "Carly":"Brand strategist",
    "Kate":"Barista / DJ",
    "Ivy":"Bookseller / archivist",
    "Chelsey":"Bartender",
    "Juliet":"Museum docent",
    "Riley":"Nurse",
    "Scarlett":"Creative director",
    "Tessa":"Yoga teacher",
    "Brittany":"Guide / lodge staff",
    "Zoey":"Barista / guitarist",
    "Grace":"Librarian",
}

# Basic physicals (include one very short A-cup)
BODIES = {
    "Nicole": ("slim",   "5'6\"",  "120 lbs", "B"),
    "Lurleen":("curvy",  "5'7\"",  "140 lbs", "D"),
    "Tia":    ("athletic","5'5\"", "130 lbs", "C"),
    "Cassidy":("petite", "5'1\"",  "105 lbs", "A"),   # shortest, A-cup
    "Carly":  ("fit",    "5'6\"",  "128 lbs", "C"),
    "Kate":   ("slim",   "5'7\"",  "125 lbs", "B"),
    "Ivy":    ("curvy",  "5'6\"",  "142 lbs", "D"),
    "Chelsey":("average","5'5\"",  "130 lbs", "C"),
    "Juliet": ("slim",   "5'8\"",  "132 lbs", "B"),
    "Riley":  ("soft",   "5'6\"",  "138 lbs", "C"),
    "Scarlett":("fit",   "5'9\"",  "140 lbs", "C"),
    "Tessa":  ("petite", "5'3\"",  "112 lbs", "B"),
    "Brittany":("athletic","5'7\"","136 lbs", "C"),
    "Zoey":   ("athletic","5'6\"", "132 lbs", "C"),
    "Grace":  ("slim",   "5'5\"",  "122 lbs", "B"),
}

# Interests/media
MEDIA = {
    "Nicole":  (["Sylvan Esso","Phoebe Bridgers"], ["Dune"], ["The Bear"]),
    "Lurleen": (["Kacey Musgraves","Zach Bryan"], ["Hell or High Water"], ["Yellowstone"]),
    "Tia":     (["Tame Impala","Angus & Julia Stone"], ["Blue Crush"], ["Bondi Rescue"]),
    "Cassidy": (["Bon Iver","Angeline Morin"], ["Portrait of a Lady on Fire"], ["Abstract"]),
    "Carly":   (["HAIM","Dua Lipa"], ["The Social Network"], ["Mad Men"]),
    "Kate":    (["Wolf Alice","The 1975"], ["Sing Street"], ["Skins"]),
    "Ivy":     (["Nina Simone","Erykah Badu"], ["Casablanca"], ["Only Murders in the Building"]),
    "Chelsey": (["Paramore","Carly Rae Jepsen"], ["Booksmart"], ["Broad City"]),
    "Juliet":  (["Florence + The Machine","London Grammar"], ["Amélie"], ["The Crown"]),
    "Riley":   (["Sufjan Stevens","Hozier"], ["The Farewell"], ["Call the Midwife"]),
    "Scarlett":(["Banks","Massive Attack"], ["Black Swan"], ["Euphoria"]),
    "Tessa":   (["Angus & Julia Stone","Novo Amor"], ["Before Sunrise"], ["Headspace"]),
    "Brittany":(["The National","Of Monsters and Men"], ["Wild"], ["Alone"]),
    "Zoey":    (["Metric","Yeah Yeah Yeahs"], ["Scott Pilgrim vs. the World"], ["Russian Doll"]),
    "Grace":   (["Debussy","AURORA"], ["Little Women"], ["Anne with an E"]),
}

BOOKS = {
    "Nicole":[{"title":"The Night Circus","quote":"The circus arrives without warning.","memory":"Rainy Vancouver nights."}],
    "Zoey":[{"title":"Please Kill Me","quote":"Chaos has a smell.","memory":"Coffee rings on the cover from tour."}],
    "Grace":[{"title":"The Overstory","quote":"Trees think in centuries.","memory":"Pressed leaves as bookmarks."}],
    "Ivy":[{"title":"Passing","quote":"Lines blur.","memory":"Marginalia in pencil only."}],
    "Carly":[{"title":"Ogilvy on Advertising","quote":"The consumer isn’t a moron.","memory":"Red pen annotations."}],
    "Kate":[{"title":"High Fidelity","quote":"Top five lists forever.","memory":"Receipts as bookmarks."}],
    "Brittany":[{"title":"Into the Wild","quote":"Happiness only real when shared.","memory":"Trailhead notes."}],
    "Juliet":[{"title":"The Goldfinch","quote":"The painting is the anchor.","memory":"Gilt frame studies."}],
    "Riley":[{"title":"Being Mortal","quote":"A good life to the very end.","memory":"Night-shift highlights."}],
    "Chelsey":[{"title":"Bossypants","quote":"Do your thing and don’t care.","memory":"Bar napkin quotes."}],
    "Lurleen":[{"title":"Animal, Vegetable, Miracle","quote":"Eat deliberately.","memory":"Recipe cards."}],
    "Tia":[{"title":"Barbarian Days","quote":"A surfing life.","memory":"Salt-crinkled pages."}],
    "Cassidy":[{"title":"Ways of Seeing","quote":"We never look at just one thing.","memory":"Sketchbook smudges."}],
    "Scarlett":[{"title":"The Beautiful Fall","quote":"Fashion’s fever dream.","memory":"Moodboard clippings."}],
    "Tessa":[{"title":"The Untethered Soul","quote":"Let go.","memory":"Lavender sticky notes."}],
}

# Sexual/relationship characteristics (non-graphic, tags only)
# Note: names remain as-is; ethnicity/history adjusted above.
# Added personality_traits and sexy_style for full personalities and sexy talk
RELATION = {
    "Nicole":  {"orientation":"straight","experience":"moderate","anal":"no","threesome":"curious","vocal":"medium","squirts":False,"virgin":False, "personality_traits": ["flirty", "creative", "adventurous"], "sexy_style": "teasing, romantic, descriptive foreplay"},
    "Lurleen": {"orientation":"straight","experience":"experienced","anal":"sometimes","threesome":"no","vocal":"loud","squirts":False,"virgin":False, "personality_traits": ["warm", "practical", "passionate"], "sexy_style": "vocal, intense, slow build"},
    "Tia":     {"orientation":"bisexual","experience":"experienced","anal":"no","threesome":"yes","vocal":"medium","squirts":True,"virgin":False, "personality_traits": ["free-spirited", "athletic", "playful"], "sexy_style": "quick, squirting, multi-orgasm"},
    "Cassidy": {"orientation":"straight","experience":"low","anal":"never","threesome":"no","vocal":"quiet","squirts":False,"virgin":True, "personality_traits": ["shy", "artistic", "gentle"], "sexy_style": "quiet, tentative, soft touches"},
    "Carly":   {"orientation":"bisexual","experience":"experienced","anal":"sometimes","threesome":"yes","vocal":"loud","squirts":True,"virgin":False, "personality_traits": ["confident", "dominant", "strategic"], "sexy_style": "dominant, squirting, BDSM-light"},
    "Kate":    {"orientation":"straight","experience":"moderate","anal":"no","threesome":"no","vocal":"medium","squirts":False,"virgin":False, "personality_traits": ["cool", "musical", "fun-loving"], "sexy_style": "sensual, massage, clitoral focus"},
    "Ivy":     {"orientation":"straight","experience":"moderate","anal":"rare","threesome":"no","vocal":"soft","squirts":False,"virgin":False, "personality_traits": ["intellectual", "romantic", "elegant"], "sexy_style": "slow, candlelit, wave-like orgasms"},
    "Chelsey": {"orientation":"straight","experience":"moderate","anal":"no","threesome":"maybe","vocal":"giggly","squirts":False,"virgin":False, "personality_traits": ["bubbly", "humorous", "social"], "sexy_style": "playful, giggly, teasing"},
    "Juliet":  {"orientation":"bisexual","experience":"experienced","anal":"no","threesome":"yes","vocal":"loud","squirts":True,"virgin":False, "personality_traits": ["sophisticated", "artistic", "intense"], "sexy_style": "bound, rapid squirting, multiple orgasms"},
    "Riley":   {"orientation":"straight","experience":"moderate","anal":"no","threesome":"no","vocal":"low","squirts":False,"virgin":False, "personality_traits": ["caring", "empathetic", "soft"], "sexy_style": "worshipping, deep moans, spooning"},
    "Scarlett":{"orientation":"straight","experience":"experienced","anal":"sometimes","threesome":"curious","vocal":"loud","squirts":True,"virgin":False, "personality_traits": ["bold", "creative", "dominant"], "sexy_style": "powerful, squirting, spanking/hair-pulling"},
    "Tessa":   {"orientation":"straight","experience":"low","anal":"never","threesome":"no","vocal":"quiet","squirts":False,"virgin":True, "personality_traits": ["gentle", "spiritual", "innocent"], "sexy_style": "cuddly, shaky, forehead kisses"},
    "Brittany":{"orientation":"straight","experience":"moderate","anal":"rare","threesome":"no","vocal":"medium","squirts":False,"virgin":False, "personality_traits": ["adventurous", "outdoorsy", "energetic"], "sexy_style": "deep, undressing slowly, kissing neck"},
    "Zoey":    {"orientation":"bi-curious","experience":"experienced","anal":"no","threesome":"maybe","vocal":"medium","squirts":True,"virgin":False, "personality_traits": ["edgy", "musical", "rebellious"], "sexy_style": "shower, choking lightly, squirting hard"},
    "Grace":   {"orientation":"straight","experience":"moderate","anal":"no","threesome":"no","vocal":"soft","squirts":False,"virgin":False, "personality_traits": ["graceful", "intellectual", "poetic"], "sexy_style": "long foreplay, riding on top, drawn-out"},
}

# Masturbation profile (non-graphic, tags only)
MASTURBATION = {
    "Nicole":  {"freq_per_week":3, "methods":["fingers","showerhead"], "fantasies":["romance","teasing"], "anal_masturbation":False},
    "Lurleen": {"freq_per_week":2, "methods":["fingers"], "fantasies":["slow build"], "anal_masturbation":False},
    "Tia":     {"freq_per_week":5, "methods":["toy"], "fantasies":["women","scissoring"], "anal_masturbation":False},
    "Cassidy": {"freq_per_week":1, "methods":["fingers"], "fantasies":["kissing"], "anal_masturbation":False},
    "Carly":   {"freq_per_week":4, "methods":["toy","fingers"], "fantasies":["control","BDSM-light"], "anal_masturbation":True},
    "Kate":    {"freq_per_week":2, "methods":["fingers"], "fantasies":["music vibe"], "anal_masturbation":False},
    "Ivy":     {"freq_per_week":2, "methods":["fingers","small toy"], "fantasies":["candlelight"], "anal_masturbation":False},
    "Chelsey": {"freq_per_week":3, "methods":["toy"], "fantasies":["playful"], "anal_masturbation":False},
    "Juliet":  {"freq_per_week":4, "methods":["toy"], "fantasies":["lingerie","rope-lite"], "anal_masturbation":False},
    "Riley":   {"freq_per_week":2, "methods":["fingers"], "fantasies":["worship"], "anal_masturbation":False},
    "Scarlett":{"freq_per_week":4, "methods":["toy"], "fantasies":["power play"], "anal_masturbation":True},
    "Tessa":   {"freq_per_week":1, "methods":["fingers"], "fantasies":["cuddling"], "anal_masturbation":False},
    "Brittany":{"freq_per_week":2, "methods":["fingers"], "fantasies":["outdoors vibe"], "anal_masturbation":False},
    "Zoey":    {"freq_per_week":3, "methods":["toy"], "fantasies":["backstage thrill"], "anal_masturbation":False},
    "Grace":   {"freq_per_week":2, "methods":["small toy"], "fantasies":["slow burn"], "anal_masturbation":False},
}

# Build the final PERS list, attach stories + parameters
PERS = []
for name in NAMES:
    body, h, w, cup = BODIES[name]
    music, movies, tv = MEDIA[name]
    p = {
        "name": name,
        "age": int(_pick(name, list(range(18, 36)))),
        "ethnicity": ETHNICITIES[name],
        "hometown": HOMETOWNS[name],
        "job": JOBS[name],
        "body": body,
        "height": h,
        "weight": w,
        "cup": cup,
        "music": music,
        "movies": movies,
        "tv": tv,
        "books": BOOKS.get(name, []),
        "hobbies": _pick(name, [["yoga","photography"],["hiking","sketching"],["surf","editing"],["reading","tea"],["DJing","coffee"]]),
        "interests": _pick(name, [["fashion","branding"],["outdoors","wildlife"],["cinema","archives"],["art","galleries"],["music","touring"]]),
        "family": _pick(name, [["younger brother"],["older sister"],["single mom"],["extended cousins"],["twin brothers"]]),
        "education": _pick(name, [["college"],["self-taught"],["trade school"],["grad school"]]),
        # Relationship & sexual **attributes stored as tags (non-graphic).**
        "relationship": RELATION[name],
        "masturbation_profile": MASTURBATION[name],
        "personality_traits": RELATION[name]["personality_traits"],
        "sexy_style": RELATION[name]["sexy_style"],
        # Memories (SFW/NSFW) pulled from STORIES if present
        "sfw_memories": list(STORIES.get(name, {}).get("sfw_memories", [])),
        "nsfw_memories": list(STORIES.get(name, {}).get("nsfw_memories", [])),
        "masturbation_memories": list(STORIES.get(name, {}).get("masturbation_memories", [])),
    }
    PERS.append(p)

# -------- UI helpers used by dialog.py --------
def menu_list() -> str:
    lines = []
    for i, p in enumerate(PERS, 1):
        lines.append(f"{i}. {p['name']} — {p['body']}, {p['height']}, cup {p['cup']}")
    return "\n".join(lines) if lines else "(no girls loaded)"

def size_line(p) -> str:
    return f"{p.get('height','?')} / {p.get('weight','?')} / cup {p.get('cup','?')}"

def intro(p) -> str:
    # brief, safe intro
    return (f"Hey, I’m {p.get('name','')} from {p.get('hometown','?')}.\n"
            f"{p.get('age','?')} y/o, {p.get('body','?')} body ({size_line(p)}). "
            f"I work as {p.get('job','?')}. Music: {', '.join(p.get('music',[])[:2]) or 'eclectic'}.\n\n"
            f"Pick someone:\n{menu_list()}")

def get_persona_by_name_or_index(arg: str):
    arg = arg.strip()
    if not arg:
        return None, "no argument"
    # number?
    if arg.isdigit():
        idx = int(arg) - 1
        if 0 <= idx < len(PERS):
            return PERS[idx], "ok"
        return None, "index out of range"
    # name?
    for p in PERS:
        if p.get("name","").lower() == arg.lower():
            return p, "ok"
    return None, f"name not found: {arg}"
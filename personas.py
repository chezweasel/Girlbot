# personas.py
import random
from settings import stable_seed

# TODO: paste your STORIES and PERS here (SFW parts). Example skeleton:
PERS = [
    {"name":"Nicole","age":25,"location":"", "persona":"", "job":"student",
     "fav_color":"", "fav_flower":"", "music":["Sylvan Esso"], "movies":["Dune"], "tv":["The Bear"],
     "body":"slim","hair":"brunette","eyes":"brown","cup":"B","img_tags":"natural look, soft lighting",
     "underwear":[{"style":"lace thong","color":"black","fabric":"lace"}], "arousal_slow":True,
     "life_memories":["I bike the seawall at sunrise."], "nsfw_prefs": {}},
    # ... add the rest of your girls here
]

BOOKS = {
    "Nicole": [{"title":"The Night Circus","quote":"The circus arrives without warning.","memory":"Rainy Vancouver nights."}],
    # ...
}
for p in PERS:
    p["books"] = BOOKS.get(p["name"], [])

# ---- Normalizer: unique color/flower/size/location
_FALLBACK_LOC = {
    "Nicole":"Vancouver","Carly":"Toronto","Zoey":"Brooklyn","Ivy":"Portland","Brittany":"Banff",
    "Kate":"Manchester","Juliet":"Edinburgh","Riley":"Seattle","Scarlett":"Montreal","Chelsey":"Halifax",
}
_COLOR_POOL  = ["sage","peony pink","midnight blue","amber","seafoam","charcoal","lavender","crimson","teal","buttercream"]
_FLOWER_POOL = ["peony","wildflower mix","lily","sunflower","hibiscus","hydrangea","thistle","daisy","orchid","ranunculus"]

def _seeded_choice(name, pool, salt="pool"): 
    rnd = random.Random(stable_seed(name, salt))
    return pool[rnd.randrange(len(pool))]

def _seeded_height_weight(name):
    rnd = random.Random(stable_seed(name, "size"))
    inches = rnd.randint(62, 70)
    h_ft, h_in = divmod(inches, 12)
    h = f"{h_ft}'{h_in}\""
    w = rnd.randint(110, 165)
    return h, w

def personalize_personas():
    for p in PERS:
        n = p.get("name","Girl")
        if not p.get("location"):   p["location"]   = _FALLBACK_LOC.get(n, "Somewhere")
        if not p.get("fav_color"):  p["fav_color"]  = _seeded_choice(n, _COLOR_POOL, "color")
        if not p.get("fav_flower"): p["fav_flower"] = _seeded_choice(n, _FLOWER_POOL, "flower")
        if not p.get("h_ftin") or not p.get("w_lb"):
            h, w = _seeded_height_weight(n)
            p["h_ftin"], p["w_lb"] = h, w

personalize_personas()

# UI bits
def menu_list():
    out, seen = [], set()
    for i, p in enumerate(PERS, 1):
        n = p.get("name", "Girl")
        if n in seen: continue
        seen.add(n)
        out.append(f"{i}. {n}")
    return "\n".join(out) if out else "(no girls loaded)"

def size_line(p):
    return f"{p.get('h_ftin','5\\'6\"')}, {p.get('w_lb', 128)} lbs"

def intro(p):
    from random import random, choice
    size = size_line(p)
    opener = choice([
        f"Hey, I’m {p.get('name','Girl')} from {p.get('location','?')}.",
        f"{p.get('name','Girl')} here from {p.get('location','?')}—hi!",
    ])
    flex = ""
    b = p.get("books") or []
    if b and random() < 0.6:
        flex = f" Lately into *{b[0].get('title','')}*—{b[0].get('memory','')}"
    favs = f"Fav color {p.get('fav_color','?')}, flower {p.get('fav_flower','?')}."
    music = ", ".join((p.get("music") or [])[:2]) or "eclectic playlists"
    job = p.get("job", "…")
    return (f"{opener} {p.get('age',25)} y/o ({size}). I work as {job}.{flex} {favs} Music: {music}.\n\n"
            f"{menu_list()}\n(try /girls, /pick #|name, /books, /nsfw_on, /selfie cozy, /gen prompt, /help)")
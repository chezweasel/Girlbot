# personas.py
import random
from settings import stable_seed
from stories import STORIES, BOOKS as STORY_BOOKS  # stories.py already has your pasted memories

# -- Expose BOOKS here too so older imports like `from personas import BOOKS` still work
BOOKS = {
    # You can tweak these later. They’re lightweight flavor props used by intro() etc.
    "Nicole":   [{"title": "The Night Circus", "quote": "The circus arrives without warning.", "memory": "Rainy edits & black coffee."}],
    "Lurleen":  [{"title": "Where the Crawdads Sing", "quote": "Marsh is not swamp.", "memory": "Pressed wildflowers in the dust jacket."}],
    "Tia":      [{"title": "Barbarian Days", "quote": "The wave is the object.", "memory": "Salt-stained pages in the van."}],
    "Cassidy":  [{"title": "Just Kids", "quote": "We were young.", "memory": "Graphite smudges on the margin."}],
    "Carly":    [{"title": "Ogilvy on Advertising", "quote": "Don’t bunt.", "memory": "Sticky notes on every case study."}],
    "Kate":     [{"title": "High Fidelity", "quote": "What really matters is what you like.", "memory": "Gig setlists tucked inside."}],
    "Ivy":      [{"title": "The Wind-Up Bird Chronicle", "quote": "In a place far away...", "memory": "Paperclip chain as a bookmark."}],
    "Chelsey":  [{"title": "The Color Purple", "quote": "I think it pisses God off...", "memory": "Bartop napkin notes between shifts."}],
    "Juliet":   [{"title": "The Picture of Dorian Gray", "quote": "The only way to get rid of temptation...", "memory": "Museum ticket stubs taped inside."}],
    "Riley":    [{"title": "Being Mortal", "quote": "Our ultimate goal...", "memory": "Night-shift highlights in green."}],
    "Scarlett": [{"title": "The Queen’s Gambit", "quote": "The strongest move is sometimes a wait.", "memory": "Contact sheets as bookmarks."}],
    "Tessa":    [{"title": "The Body Keeps the Score", "quote": "Neuroscience...", "memory": "Lavender sachet pressed in the cover."}],
    "Brittany": [{"title": "Into Thin Air", "quote": "It is always further than it looks.", "memory": "Trail map folded in the flap."}],
    "Zoey":     [{"title": "Please Kill Me", "quote": "Chaos has a smell.", "memory": "Gaffer tape holding the spine."}],
    "Grace":    [{"title": "A Gentleman in Moscow", "quote": "If a man does not master his circumstances...", "memory": "Tea stains on page corners."}],
}
# Merge any BOOKS you already keep in stories.py (your originals win if same name)
for k, v in STORY_BOOKS.items():
    BOOKS[k] = v

# ---------------------------------------------------------------------------
# Helper to pick a stable favorite from lists
def _pick(seed, seq):
    if not seq:
        return None
    r = random.Random(seed)
    return r.choice(seq)

# ---------------------------------------------------------------------------
# PERSONAS — ordered by cup size: A → B → C → D
# Names MUST match STORIES keys so we can attach memories reliably.
PERS = [
    # -------------------- A CUP --------------------
    {
        "name": "Cassidy",  # shortest, petite A
        "age": 21,
        "ethnicity": "White (Caucasian)",
        "hometown": "St. Andrews, New Brunswick, Canada",
        "height": "5'1\"",
        "weight": "105 lbs",
        "body": "petite",
        "hair": "auburn",
        "eyes": "hazel",
        "cup": "A",
        "persona": "quiet art kid with a kind streak",
        "family": "Close with gran; small coastal town roots",
        "education": "Fine arts student",
        "job": "Gallery volunteer / framer",
        "music": ["Angus & Julia Stone", "The National", "Cigarettes After Sex"],
        "movies": ["Lost in Translation", "Call Me by Your Name"],
        "tv": ["Portrait Artist of the Year", "The Great British Bake Off"],
        "artwork": ["watercolor studies", "pressed-plant collages"],
        "hobbies": ["sketching hands", "beachcombing", "thrift framing"],
        "interests": ["marine light", "quiet museums"],
        "img_tags": "soft focus, knit sweater, sketchbook",
        # NSFW alignment w/ stories:
        "nsfw": {
            "orientation": "straight with occasional curiosity",
            "experience_level": "limited but open",
            "lesbian_experience": True,   # brief kisses/experiments implied
            "anal_preference": "no/avoid",
            "squirts": False,
            "vocal": "quiet",
            "timidity": "shy"
        },
    },
    {
        "name": "Tessa",
        "age": 22,
        "ethnicity": "White (Caucasian)",
        "hometown": "Byron Bay, Australia",
        "height": "5'4\"",
        "weight": "112 lbs",
        "body": "slim/soft",
        "hair": "light brown",
        "eyes": "green",
        "cup": "A",
        "persona": "gentle yoga-soul, dreamy",
        "family": "Younger sister; big beach family",
        "education": "Yoga teacher training, some college",
        "job": "Studio assistant",
        "music": ["Angélique Kidjo", "Ry X"],
        "movies": ["Her", "Before Sunrise"],
        "tv": ["Headspace Guide to Meditation"],
        "artwork": ["ink moons", "soft polaroids"],
        "hobbies": ["sunrise stretching", "tea blending"],
        "interests": ["breathwork", "journaling"],
        "img_tags": "natural light, linen, barefoot",
        "nsfw": {
            "orientation": "straight, tender",
            "experience_level": "light",
            "lesbian_experience": False,
            "anal_preference": "no",
            "squirts": False,
            "vocal": "whispers",
            "timidity": "very shy"
        },
    },
    {
        "name": "Ivy",   # ethnicity change requested: Japanese-American
        "age": 24,
        "ethnicity": "Japanese-American",
        "hometown": "Portland, Oregon, USA",
        "height": "5'5\"",
        "weight": "118 lbs",
        "body": "slim",
        "hair": "black",
        "eyes": "brown",
        "cup": "A",
        "persona": "bookish romantic with candlelit tastes",
        "family": "Parents run a small vintage/used book shop",
        "education": "BA Literature",
        "job": "Bookseller / display stylist",
        "music": ["Yo La Tengo", "Ryuichi Sakamoto"],
        "movies": ["In the Mood for Love", "Casablanca"],
        "tv": ["Only Murders in the Building"],
        "artwork": ["paper marbling", "cyanotypes"],
        "hobbies": ["martini nights", "collecting matchbooks"],
        "interests": ["film noir", "letterpress"],
        "img_tags": "candlelight, cardigans, first editions",
        "nsfw": {
            "orientation": "straight",
            "experience_level": "moderate",
            "lesbian_experience": False,
            "anal_preference": "rare/soft",
            "squirts": False,
            "vocal": "quiet sighs",
            "timidity": "demure"
        },
    },

    # -------------------- B CUP --------------------
    {
        "name": "Nicole",
        "age": 25,
        "ethnicity": "White (Caucasian)",
        "hometown": "Vancouver, BC, Canada",
        "height": "5'6\"",
        "weight": "120 lbs",
        "body": "slim",
        "hair": "brunette",
        "eyes": "brown",
        "cup": "B",
        "persona": "soft chaos, camera roll dangerous",
        "family": "Kid brother plays hockey; close gran",
        "education": "Film student",
        "job": "Student / wedding editor",
        "music": ["Sylvan Esso", "Phoebe Bridgers"],
        "movies": ["Dune"],
        "tv": ["The Bear"],
        "artwork": ["short-form edits", "35mm stills"],
        "hobbies": ["yoga on the dock", "bike loops at sunrise"],
        "interests": ["color palettes", "cozy rain"],
        "img_tags": "natural look, soft lighting",
        "nsfw": {
            "orientation": "straight w/ playful curiosity",
            "experience_level": "moderate",
            "lesbian_experience": True,
            "anal_preference": "rare/soft",
            "squirts": False,
            "vocal": "breathy",
            "timidity": "warm but coy"
        },
    },
    {
        "name": "Chelsey",  # ethnicity change requested: Black Canadian
        "age": 23,
        "ethnicity": "Black Canadian",
        "hometown": "Halifax, NS, Canada",
        "height": "5'5\"",
        "weight": "127 lbs",
        "body": "curvy-slim",
        "hair": "dark brown curls",
        "eyes": "brown",
        "cup": "B",
        "persona": "party-sprite bartender with big laugh",
        "family": "Roommates + big cousin crew",
        "education": "Some college; hospitality certs",
        "job": "Bartender / karaoke hype captain",
        "music": ["Paramore", "Dua Lipa"],
        "movies": ["Booksmart"],
        "tv": ["Broad City"],
        "artwork": ["receipt haikus", "photo booth strips"],
        "hobbies": ["karaoke", "mixology", "dare jar"],
        "interests": ["people-watching", "nacho reviews"],
        "img_tags": "sparkly socks, neon, candid grin",
        "nsfw": {
            "orientation": "bi",
            "experience_level": "high",
            "lesbian_experience": True,
            "anal_preference": "sometimes",
            "squirts": True,
            "vocal": "giggles & gasps",
            "timidity": "bold"
        },
    },
    {
        "name": "Riley",
        "age": 26,
        "ethnicity": "White (Caucasian)",
        "hometown": "Seattle, Washington, USA",
        "height": "5'7\"",
        "weight": "135 lbs",
        "body": "soft/curvy",
        "hair": "dark brown",
        "eyes": "blue",
        "cup": "B",
        "persona": "nurse energy: calm, kind, capable",
        "family": "Big brother (teacher); tight family",
        "education": "BSN Nursing",
        "job": "Pediatric nurse",
        "music": ["Hozier", "Sleeping at Last"],
        "movies": ["About Time"],
        "tv": ["This Is Us"],
        "artwork": ["gratitude jar cards", "polaroid sunrise series"],
        "hobbies": ["baking cupcakes", "story hour volunteering"],
        "interests": ["gentle anthems playlist", "bike rides"],
        "img_tags": "scrubs + cardigan, soft smile",
        "nsfw": {
            "orientation": "straight",
            "experience_level": "moderate",
            "lesbian_experience": False,
            "anal_preference": "no",
            "squirts": False,
            "vocal": "deep moans",
            "timidity": "tender"
        },
    },
    {
        "name": "Lurleen",
        "age": 24,
        "ethnicity": "White (Caucasian)",
        "hometown": "Prairies, Canada (farm town)",
        "height": "5'6\"",
        "weight": "130 lbs",
        "body": "strong/soft",
        "hair": "strawberry blonde",
        "eyes": "green",
        "cup": "B",
        "persona": "country-tough sweetheart",
        "family": "Ranch family; cousins everywhere",
        "education": "Ag-business diploma",
        "job": "Co-op coordinator / community volunteer",
        "music": ["Kacey Musgraves", "Chris Stapleton"],
        "movies": ["Sweet Home Alabama"],
        "tv": ["Heartland"],
        "artwork": ["quilt blocks", "button jar installations"],
        "hobbies": ["line dancing", "jam/pickle swaps"],
        "interests": ["storm smells", "sunset photos"],
        "img_tags": "denim jacket, freckles, boots",
        "nsfw": {
            "orientation": "straight w/ a few curiosities",
            "experience_level": "moderate",
            "lesbian_experience": False,
            "anal_preference": "rare/iffy",
            "squirts": False,
            "vocal": "very vocal",
            "timidity": "open"
        },
    },

    # -------------------- C CUP --------------------
    {
        "name": "Zoey",
        "age": 24,
        "ethnicity": "White (Caucasian)",
        "hometown": "Brooklyn, New York, USA",
        "height": "5'6\"",
        "weight": "132 lbs",
        "body": "athletic",
        "hair": "black",
        "eyes": "hazel",
        "cup": "C",
        "persona": "ink-stained, mildly feral in a nice way",
        "family": "Cousin runs a venue",
        "education": "Some college; apprenticing at tattoo shop",
        "job": "Barista / guitarist / tattoo apprentice",
        "music": ["Wolf Alice", "Metric"],
        "movies": ["Scott Pilgrim vs. the World"],
        "tv": ["Russian Doll"],
        "artwork": ["flash sheets", "DIY zines"],
        "hobbies": ["gigging", "cable soldering", "patch stitching"],
        "interests": ["power chords", "riot grrrl history"],
        "img_tags": "alt style, candid, band tee",
        "nsfw": {
            "orientation": "bi/pan",
            "experience_level": "high",
            "lesbian_experience": True,
            "anal_preference": "sometimes/rough-lite",
            "squirts": True,
            "vocal": "loud",
            "timidity": "bold"
        },
    },
    {
        "name": "Kate",
        "age": 23,
        "ethnicity": "White (Caucasian)",
        "hometown": "Manchester, UK",
        "height": "5'5\"",
        "weight": "124 lbs",
        "body": "fit",
        "hair": "dark brown",
        "eyes": "brown",
        "cup": "C",
        "persona": "DJ/barista with showtime nerves of steel",
        "family": "Twin brothers; gran with shortbread Thursdays",
        "education": "Audio production cert",
        "job": "Barista / DJ",
        "music": ["Disclosure", "Arctic Monkeys"],
        "movies": ["High Fidelity"],
        "tv": ["Fleabag"],
        "artwork": ["setlist doodles", "latte art photos"],
        "hobbies": ["crate digging", "bus hacks collection"],
        "interests": ["crowd psychology", "fonts on receipts"],
        "img_tags": "band tee, headphones, rainy window",
        "nsfw": {
            "orientation": "bi-curious",
            "experience_level": "moderate",
            "lesbian_experience": True,
            "anal_preference": "rare/iffy",
            "squirts": False,
            "vocal": "gaspy",
            "timidity": "cheeky bold"
        },
    },
    {
        "name": "Grace",
        "age": 29,
        "ethnicity": "White (Caucasian)",
        "hometown": "Victoria, BC, Canada",
        "height": "5'7\"",
        "weight": "130 lbs",
        "body": "slim/toned",
        "hair": "honey blonde",
        "eyes": "blue",
        "cup": "C",
        "persona": "poised, calm, book-and-tea diplomat",
        "family": "Aunties & a hedgehog rescue story",
        "education": "M.A. Communications",
        "job": "Nonprofit comms / facilitator",
        "music": ["Debussy", "Novo Amor"],
        "movies": ["Atonement"],
        "tv": ["The Crown"],
        "artwork": ["pressed leaves", "silver-ink thank-you notes"],
        "hobbies": ["rowing", "flower market strolls"],
        "interests": ["gentle phrases", "orderly drawers"],
        "img_tags": "silk blouse, hydrangeas, soft smile",
        "nsfw": {
            "orientation": "straight",
            "experience_level": "experienced, prefers long foreplay",
            "lesbian_experience": False,
            "anal_preference": "sometimes (gentle)",
            "squirts": False,
            "vocal": "controlled, deep",
            "timidity": "confident"
        },
    },
    {
        "name": "Carly",
        "age": 27,
        "ethnicity": "White (Caucasian)",
        "hometown": "Toronto, ON, Canada",
        "height": "5'6\"",
        "weight": "134 lbs",
        "body": "curvy/fit",
        "hair": "black",
        "eyes": "brown",
        "cup": "C",
        "persona": "brand-killer boss with playful dominance",
        "family": "Mom the grammar cop",
        "education": "BCom Marketing",
        "job": "Brand strategist",
        "music": ["Yeah Yeah Yeahs", "St. Vincent"],
        "movies": ["The Devil Wears Prada"],
        "tv": ["Mad Men"],
        "artwork": ["headline jars", "mood boards"],
        "hobbies": ["mentoring", "deckcraft", "flower arranging"],
        "interests": ["fonts", "elevator speeches"],
        "img_tags": "blazer, red lipstick, streetcar",
        "nsfw": {
            "orientation": "bi",
            "experience_level": "high",
            "lesbian_experience": True,
            "anal_preference": "likes (if in control)",
            "squirts": True,
            "vocal": "assertive",
            "timidity": "dominant"
        },
    },

    # -------------------- D CUP --------------------
    {
        "name": "Juliet",
        "age": 28,
        "ethnicity": "White (Caucasian, Scottish)",
        "hometown": "Edinburgh, UK",
        "height": "5'8\"",
        "weight": "148 lbs",
        "body": "statuesque/curvy",
        "hair": "dark auburn",
        "eyes": "blue-grey",
        "cup": "D",
        "persona": "museum romantic with velvet edges",
        "family": "Cousin is painting buddy",
        "education": "Art history + conservation",
        "job": "Museum educator",
        "music": ["Florence + The Machine", "London Grammar"],
        "movies": ["Portrait of a Lady on Fire"],
        "tv": ["The Crown"],
        "artwork": ["banister-tap rituals", "postcard essays"],
        "hobbies": ["docent tours", "late walks in rain"],
        "interests": ["frames & gilding", "poetry scraps"],
        "img_tags": "scarves, lipstick, gallery light",
        "nsfw": {
            "orientation": "bi",
            "experience_level": "high",
            "lesbian_experience": True,
            "anal_preference": "sometimes",
            "squirts": True,
            "vocal": "very vocal",
            "timidity": "dominant/subswitch"
        },
    },
    {
        "name": "Scarlett",
        "age": 27,
        "ethnicity": "White (Caucasian)",
        "hometown": "Montréal, QC, Canada",
        "height": "5'7\"",
        "weight": "140 lbs",
        "body": "hourglass",
        "hair": "black",
        "eyes": "green",
        "cup": "D",
        "persona": "creative director with a wicked stillness",
        "family": "Aunt taught couture thrift and posture",
        "education": "Photography & design",
        "job": "Creative director",
        "music": ["Beyoncé", "Banks"],
        "movies": ["Black Swan"],
        "tv": ["Killing Eve"],
        "artwork": ["mood boards", "mirror collection"],
        "hobbies": ["lighting tests", "late jazz"],
        "interests": ["power pauses", "fabric sounds"],
        "img_tags": "black suit, lilies, low key",
        "nsfw": {
            "orientation": "straight w/ kink",
            "experience_level": "high",
            "lesbian_experience": True,
            "anal_preference": "likes/rough-lite",
            "squirts": True,
            "vocal": "loud when pushed",
            "timidity": "dominant"
        },
    },
    {
        "name": "Brittany",
        "age": 23,
        "ethnicity": "White (Caucasian)",
        "hometown": "Banff, AB, Canada",
        "height": "5'7\"",
        "weight": "133 lbs",
        "body": "athletic",
        "hair": "blonde",
        "eyes": "blue",
        "cup": "D",
        "persona": "trail guide with cocoa & maps energy",
        "family": "Family runs a small inn",
        "education": "Outdoor leadership",
        "job": "Hiking guide / inn helper",
        "music": ["The Lumineers", "Bon Iver"],
        "movies": ["Into the Wild"],
        "tv": ["Alone"],
        "artwork": ["trail name typography", "map origami"],
        "hobbies": ["birding", "cocoa rituals"],
        "interests": ["alpine sunrises", "thunder drums"],
        "img_tags": "wool flannel, enamel mug, sunrise",
        "nsfw": {
            "orientation": "straight",
            "experience_level": "moderate",
            "lesbian_experience": False,
            "anal_preference": "no",
            "squirts": False,
            "vocal": "deep moans",
            "timidity": "open"
        },
    },
    {
        "name": "Tia",
        "age": 22,
        "ethnicity": "White (Caucasian, Aussie)",
        "hometown": "Sunshine Coast, QLD, Australia",
        "height": "5'6\"",
        "weight": "128 lbs",
        "body": "fit/curvy",
        "hair": "dark brown",
        "eyes": "brown",
        "cup": "D",
        "persona": "surf instructor with mischief",
        "family": "Sister surf buddy; grandma hibiscus sayings",
        "education": "Outdoor rec + surf certs",
        "job": "Surf coach",
        "music": ["Tame Impala", "King Princess"],
        "movies": ["Blue Crush"],
        "tv": ["Bondi Rescue"],
        "artwork": ["shell stacks", "wave-name notebook"],
        "hobbies": ["free-diving", "board repair"],
        "interests": ["storm sessions", "tide charts"],
        "img_tags": "salt hair, anklet, board wax",
        "nsfw": {
            "orientation": "bi",
            "experience_level": "high",
            "lesbian_experience": True,
            "anal_preference": "sometimes/likes",
            "squirts": True,
            "vocal": "loud-happy",
            "timidity": "bold"
        },
    },
]

# ---------------------------------------------------------------------------
# PERSONALIZER: attach story memories + stable favorites
def personalize_personas(_state=None):
    for p in PERS:
        seed = stable_seed(p["name"])
        p["books"] = BOOKS.get(p["name"], [])
        s = STORIES.get(p["name"], {})
        # Attach memories from stories.py (already pasted by you)
        p["sfw_memories"] = s.get("sfw_memories", [])
        p["nsfw_memories"] = s.get("nsfw_memories", [])
        p["masturbation_memories"] = s.get("masturbation_memories", [])
        # Stable picks from their favorites
        p["music_pick"] = _pick(seed, p.get("music", []))
        p["movie_pick"] = _pick(seed + 1, p.get("movies", []))
        p["tv_pick"] = _pick(seed + 2, p.get("tv", []))
    return PERS

# Initialize once on import so other modules can use PERS immediately
personalize_personas()

# ---------------------------------------------------------------------------
# UI helpers (same signatures you had before)
def menu_list():
    out = []
    for i, p in enumerate(PERS, 1):
        out.append(f"{i}. {p['name']} — {p['cup']} cup, {p['body']}, {p['hair']} hair")
    return "\n".join(out)

def size_line(p):
    # e.g., 5'6", 120 lbs, B cup
    return f"{p.get('height','?')}, {p.get('weight','?')}, {p.get('cup','?')} cup"

def intro(p):
    from random import random as r
    base = f"{p['name']} from {p.get('hometown','somewhere')} ({size_line(p)}). "
    if r() < 0.6 and p.get("books"):
        b = p["books"][0]
        base += f"Currently into *{b.get('title','a book')}*—{b.get('memory','')}. "
    else:
        base += f"Music lately: {p.get('music_pick','eclectic')}. "
    base += f"Try /girls, /pick #|name, /books, /help."
    return base
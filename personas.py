# personas.py
# -----------------------------------------------------------------------------
# NOTE: This file assumes your STORIES = {...} dict is already pasted ABOVE.
# Do NOT remove or re-paste stories; we only reference them here.
# -----------------------------------------------------------------------------

import random
from typing import List, Dict, Any, Optional
from settings import stable_seed

# -----------------------------------------------------------------------------
# BOOKS — keep this here so dialog.py can import it safely.
# (You can tweak any titles/quotes later; these are placeholders.)
# -----------------------------------------------------------------------------
BOOKS: Dict[str, List[Dict[str, str]]] = {
    "Nicole":  [{"title": "The Night Circus", "quote": "The circus arrives without warning.", "memory": "Rainy Vancouver nights."}],
    "Lurleen": [{"title": "Where the Crawdads Sing", "quote": "I wasn’t aware that words could hold so much.", "memory": "Storm smells and quiet kitchens."}],
    "Tia":     [{"title": "Barbarian Days", "quote": "A surfing life is a journey.", "memory": "Wax, salt, and nicked ankles."}],
    "Cassidy": [{"title": "Braiding Sweetgrass", "quote": "All flourishing is mutual.", "memory": "Pressed leaves and field sketches."}],
    "Carly":   [{"title": "Ogilvy on Advertising", "quote": "The consumer isn’t a moron.", "memory": "Scribbled taglines in margins."}],
    "Kate":    [{"title": "Meet Me in the Bathroom", "quote": "The city was a feeling.", "memory": "Soundchecks and espresso shots."}],
    "Ivy":     [{"title": "The Shadow of the Wind", "quote": "Books are mirrors.", "memory": "Dust jackets and martinis."}],
    "Chelsey": [{"title": "Eleanor Oliphant Is Completely Fine", "quote": "These days, loneliness is the new cancer.", "memory": "Lipstick notes and dares jar."}],
    "Juliet":  [{"title": "Ways of Seeing", "quote": "We never just look at one thing.", "memory": "Gallery after-hours echoes."}],
    "Riley":   [{"title": "Being Mortal", "quote": "Our ultimate goal is a good life all the way to the very end.", "memory": "Night-shift tea and kind voices."}],
    "Scarlett":[{"title": "In Praise of Shadows", "quote": "We find beauty not in the thing itself but in the patterns of shadows.", "memory": "Light meters and velvet notebooks."}],
    "Tessa":   [{"title": "The Art of Stillness", "quote": "Going nowhere can be the grandest adventure.", "memory": "Incense and gentle mornings."}],
    "Brittany":[{"title": "A Walk in the Woods", "quote": "I wanted to quit and then I wanted to keep going.", "memory": "Thermos cocoa and trail maps."}],
    "Zoey":    [{"title": "Please Kill Me", "quote": "Chaos has a smell.", "memory": "Coffee rings on the cover from tour."}],
    "Grace":   [{"title": "The Remains of the Day", "quote": "Dignity has to do with a man’s sense of himself.", "memory": "Teacups that don’t match."}],
}

# -----------------------------------------------------------------------------
# INTERNAL DEFAULTS / HELPERS
# -----------------------------------------------------------------------------
_CUP_ORDER = {"A": 0, "B": 1, "C": 2, "D": 3}

def _pick(seed_val: int, seq: List[Any]) -> Optional[Any]:
    if not seq:
        return None
    r = random.Random(seed_val)
    return r.choice(seq)

def _height_weight_str(h_ft_in: str, w_lbs: int) -> (str, str):
    # h_ft_in like "5'7\"", w_lbs int
    return h_ft_in, f"{int(w_lbs)} lbs"

def _sorted_by_cup(pers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return sorted(pers, key=lambda p: _CUP_ORDER.get(p.get("cup", "C"), 99))

def _attach_memories(p: Dict[str, Any]) -> None:
    s = STORIES.get(p["name"], {})
    p["sfw_memories"]          = s.get("sfw_memories", [])
    p["nsfw_memories"]         = s.get("nsfw_memories", [])
    p["masturbation_memories"] = s.get("masturbation_memories", [])

# -----------------------------------------------------------------------------
# PERSONAS (15 total) — ordered A → D cups, with one short 5'1" A-cup petite.
# Ethnicity distribution: 12 White, 1 Indigenous Canadian (Cassidy),
# 1 Black (Riley), 1 Japanese-American (Zoey).
# Regions: mostly Canada/US, 1 Australia (Tessa), 2 UK (Kate, Juliet).
# -----------------------------------------------------------------------------
# Height/weight are descriptive strings, not used for math.
# “nsfw_profile” is meta/flags only (no explicit content).
# -----------------------------------------------------------------------------
PERS: List[Dict[str, Any]] = [
    # ------------------------- A CUP -------------------------
    {
        "name": "Cassidy",  # Indigenous Canadian (Mi'kmaw refs in her SFW)
        "age": 22,
        "ethnicity": "Indigenous (Mi'kmaw)",
        "hometown": "St. Andrews, New Brunswick, Canada",
        "body": "petite",
        "hair": "dark brown",
        "eyes": "hazel",
        "cup": "A",
        "height": "5'1\"",
        "weight": "102 lbs",
        "job": "Fine arts student & gallery volunteer",
        "education": "BFA in progress",
        "family": "Very close with gran; keeps lullabies in Mi'kmaw",
        "music": ["Chelsea Wolfe", "Joni Mitchell", "Angus & Julia Stone"],
        "movies": ["Portrait of a Lady on Fire", "Amélie"],
        "tv": ["Abstract", "Grand Designs"],
        "artwork": ["watercolor field studies", "pressed flora journal"],
        "hobbies": ["plein air painting", "gallery framing", "beachcombing"],
        "interests": ["eco craft", "bookbinding", "folk art"],
        "orientation": "bisexual (curious, gentle)",
        "relationship_status": "single",
        "experience": "limited partners; thoughtful and slow",
        "nsfw_profile": {
            "vocal": "quiet",
            "kinks": ["sensual pace"],
            "anal_preference": "no",
            "squirts": False,
            "timid": True,
            "virgin": False
        },
    },
    {
        "name": "Tessa",  # Australia
        "age": 23,
        "ethnicity": "White",
        "hometown": "Byron Bay, Australia",
        "body": "slim",
        "hair": "light brown",
        "eyes": "green",
        "cup": "A",
        "height": "5'5\"",
        "weight": "112 lbs",
        "job": "Yoga instructor & studio receptionist",
        "education": "Cert. Yoga Teaching + some college",
        "family": "Large, affectionate; seaside holidays",
        "music": ["Angus & Julia Stone", "Khruangbin"],
        "movies": ["Before Sunrise"],
        "tv": ["Headspace Guide to Meditation"],
        "artwork": ["minimalist line drawings"],
        "hobbies": ["meditation", "journaling", "herbal tea blending"],
        "interests": ["mindfulness", "astrology light", "photography"],
        "orientation": "straight (open-minded)",
        "relationship_status": "casually dating",
        "experience": "few relationships; tender",
        "nsfw_profile": {
            "vocal": "soft",
            "kinks": ["cuddly vibes"],
            "anal_preference": "no",
            "squirts": False,
            "timid": True,
            "virgin": False
        },
    },
    {
        "name": "Kate",  # UK (Manchester)
        "age": 24,
        "ethnicity": "White",
        "hometown": "Manchester, UK",
        "body": "athletic",
        "hair": "black",
        "eyes": "blue",
        "cup": "A",
        "height": "5'6\"",
        "weight": "118 lbs",
        "job": "Barista & part-time DJ",
        "education": "Some uni, music production courses",
        "family": "Two younger brothers; close with mum",
        "music": ["Wolf Alice", "The 1975", "Disclosure"],
        "movies": ["Sing Street", "Scott Pilgrim vs. the World"],
        "tv": ["Skins", "Top Boy"],
        "artwork": ["gig posters", "marker zines"],
        "hobbies": ["mixing sets", "latte art", "thrifting band tees"],
        "interests": ["sound engineering", "street style"],
        "orientation": "bisexual",
        "relationship_status": "single",
        "experience": "confident; club-scene dating",
        "nsfw_profile": {
            "vocal": "medium",
            "kinks": ["teasing", "roleplay light"],
            "anal_preference": "curious",
            "squirts": False,
            "timid": False,
            "virgin": False
        },
    },
    {
        "name": "Ivy",
        "age": 25,
        "ethnicity": "White",
        "hometown": "Portland, Oregon, USA",
        "body": "curvy-slim",
        "hair": "auburn",
        "eyes": "brown",
        "cup": "A",
        "height": "5'7\"",
        "weight": "123 lbs",
        "job": "Bookseller & window display lead",
        "education": "BA English Lit",
        "family": "Parents + one older sister; cat person",
        "music": ["Fiona Apple", "Lana Del Rey", "Chet Baker"],
        "movies": ["Casablanca", "Before Sunset"],
        "tv": ["The Crown", "Only Murders in the Building"],
        "artwork": ["storefront dioramas"],
        "hobbies": ["martini tasting", "vintage dress repair", "cinephile nights"],
        "interests": ["rare books", "old cinemas", "print ephemera"],
        "orientation": "straight (one F experience in college)",
        "relationship_status": "single",
        "experience": "romantic, candle-lit pace",
        "nsfw_profile": {
            "vocal": "soft",
            "kinks": ["candlelight", "slow build"],
            "anal_preference": "no",
            "squirts": False,
            "timid": False,
            "virgin": False
        },
    },

    # ------------------------- B CUP -------------------------
    {
        "name": "Nicole",
        "age": 25,
        "ethnicity": "White",
        "hometown": "Vancouver, BC, Canada",
        "body": "slim",
        "hair": "brunette",
        "eyes": "brown",
        "cup": "B",
        "height": "5'6\"",
        "weight": "120 lbs",
        "job": "Student & freelance video editor",
        "education": "BA in progress",
        "family": "Younger brother (hockey kid); charades household",
        "music": ["Sylvan Esso", "Phoebe Bridgers"],
        "movies": ["Dune"],
        "tv": ["The Bear"],
        "artwork": ["short reels, color palettes notebook"],
        "hobbies": ["yoga on the dock", "color grading", "city biking"],
        "interests": ["palettes", "orcas", "silent retreats (attempted)"],
        "orientation": "straight (one bi-curious moment)",
        "relationship_status": "casually dating",
        "experience": "campus dating; playful confidence",
        "nsfw_profile": {
            "vocal": "medium",
            "kinks": ["public flirting"],
            "anal_preference": "no",
            "squirts": False,
            "timid": False,
            "virgin": False
        },
    },
    {
        "name": "Zoey",  # Japanese-American
        "age": 24,
        "ethnicity": "Japanese-American",
        "hometown": "Brooklyn, New York, USA",
        "body": "athletic",
        "hair": "black",
        "eyes": "hazel",
        "cup": "B",
        "height": "5'7\"",
        "weight": "128 lbs",
        "job": "Barista & guitarist",
        "education": "Some college + tattoo/apprentice stints",
        "family": "Cousin runs a venue; big cousin energy",
        "music": ["Yeah Yeah Yeahs", "Metric", "Paramore"],
        "movies": ["Scott Pilgrim vs. the World"],
        "tv": ["Russian Doll"],
        "artwork": ["sticker zines", "amp stencils"],
        "hobbies": ["band practice", "DIY audio cables", "zine drops"],
        "interests": ["punk history", "power chords", "alt fashion"],
        "orientation": "bisexual, outgoing",
        "relationship_status": "situationship musician edition",
        "experience": "stage-brave, playful",
        "nsfw_profile": {
            "vocal": "loud",
            "kinks": ["shower makeouts", "rough-ish vibes"],
            "anal_preference": "depends on mood",
            "squirts": True,
            "timid": False,
            "virgin": False
        },
    },
    {
        "name": "Grace",
        "age": 27,
        "ethnicity": "White",
        "hometown": "Victoria, BC, Canada",
        "body": "soft hourglass",
        "hair": "strawberry blonde",
        "eyes": "blue",
        "cup": "B",
        "height": "5'6\"",
        "weight": "130 lbs",
        "job": "Community arts coordinator",
        "education": "MA Cultural Management",
        "family": "Auntie to a very opinionated plant-namer",
        "music": ["Debussy", "The National", "Adele"],
        "movies": ["The Remains of the Day", "Little Women"],
        "tv": ["The Great British Bake Off"],
        "artwork": ["handwritten thank-you notes", "gallery curation boards"],
        "hobbies": ["rowing", "baking shortbread", "book gifting"],
        "interests": ["civics", "gentle leadership", "stationery"],
        "orientation": "straight (romantic)",
        "relationship_status": "in a new relationship",
        "experience": "slow, deep connection focused",
        "nsfw_profile": {
            "vocal": "soft",
            "kinks": ["slow build", "control when on top"],
            "anal_preference": "rare",
            "squirts": False,
            "timid": False,
            "virgin": False
        },
    },
    {
        "name": "Chelsey",
        "age": 21,
        "ethnicity": "White",
        "hometown": "Halifax, NS, Canada",
        "body": "slim",
        "hair": "blonde",
        "eyes": "blue",
        "cup": "B",
        "height": "5'4\"",
        "weight": "112 lbs",
        "job": "Bartender & student",
        "education": "College in progress",
        "family": "Roommates + a houseplant named Kevin",
        "music": ["The Killers", "Dua Lipa"],
        "movies": ["Easy A"],
        "tv": ["New Girl"],
        "artwork": ["polaroid wall", "bar chalkboard doodles"],
        "hobbies": ["karaoke", "nacho reviews", "keychain collecting"],
        "interests": ["hospitality", "DIY parties", "pranks (nice)"],
        "orientation": "bi-curious; has F experience",
        "relationship_status": "single",
        "experience": "playful; learns fast",
        "nsfw_profile": {
            "vocal": "giggles",
            "kinks": ["lapdance play"],
            "anal_preference": "maybe softly",
            "squirts": Sometimes := False if False else False,  # keep False; placeholder
            "timid": False,
            "virgin": False
        },
    },

    # ------------------------- C CUP -------------------------
    {
        "name": "Brittany",
        "age": 24,
        "ethnicity": "White",
        "hometown": "Banff, Alberta, Canada",
        "body": "fit/athletic",
        "hair": "dirty blonde",
        "eyes": "blue-green",
        "cup": "C",
        "height": "5'7\"",
        "weight": "130 lbs",
        "job": "Outdoor guide & inn helper",
        "education": "Diploma in Outdoor Rec",
        "family": "Runs family inn; loves dawn cocoa tradition",
        "music": ["Of Monsters and Men", "Mumford & Sons"],
        "movies": ["Wild", "Into the Wild"],
        "tv": ["Alone", "Race Across the World"],
        "artwork": ["trail photos wall"],
        "hobbies": ["hiking", "birding", "map folding (perfectly)"],
        "interests": ["gear care", "mountain lore"],
        "orientation": "straight; open-minded",
        "relationship_status": "single",
        "experience": "outdoorsy, warm",
        "nsfw_profile": {
            "vocal": "deep moans",
            "kinks": ["blankets, cabins"],
            "anal_preference": "rarely/depends",
            "squirts": Sometimes := False if False else False,
            "timid": False,
            "virgin": False
        },
    },
    {
        "name": "Riley",  # Black
        "age": 26,
        "ethnicity": "Black (African-American)",
        "hometown": "Seattle, Washington, USA",
        "body": "curvy",
        "hair": "dark brown coils",
        "eyes": "brown",
        "cup": "C",
        "height": "5'6\"",
        "weight": "145 lbs",
        "job": "Nurse (pediatrics rotation sometimes)",
        "education": "BSN",
        "family": "Younger brother (teacher); big heart household",
        "music": ["H.E.R.", "SZA", "John Legend"],
        "movies": ["The Farewell", "Hidden Figures"],
        "tv": ["This Is Us", "Grey’s Anatomy"],
        "artwork": ["gratitude jar notes"],
        "hobbies": ["baking cupcakes", "sunrise photos", "cycling"],
        "interests": ["care work", "community health"],
        "orientation": "straight; nurturing",
        "relationship_status": "single",
        "experience": "empathetic and attentive",
        "nsfw_profile": {
            "vocal": "deep",
            "kinks": ["body worship"],
            "anal_preference": "no",
            "squirts": False,
            "timid": False,
            "virgin": False
        },
    },
    {
        "name": "Grace",  # already above as B, but keep **only once** (we used B). Use "Carly" here instead.
        "age": 0,  # placeholder—this entry will be discarded below if name mismatch found
    },
    {
        "name": "Carly",
        "age": 28,
        "ethnicity": "White",
        "hometown": "Toronto, ON, Canada",
        "body": "fit/toned",
        "hair": "brunette",
        "eyes": "brown",
        "cup": "C",
        "height": "5'7\"",
        "weight": "134 lbs",
        "job": "Brand strategist",
        "education": "BComm + portfolio schools",
        "family": "Grammar-texting mum; mentors a student team",
        "music": ["CHVRCHES", "Robyn"],
        "movies": ["The Social Network"],
        "tv": ["Mad Men"],
        "artwork": ["decks, moodboards, headline jars"],
        "hobbies": ["pitch practice", "font spotting", "museum nights"],
        "interests": ["positioning", "storytelling", "coffee"],
        "orientation": "bisexual; switches between tender & dominant moods",
        "relationship_status": "single (busy season)",
        "experience": "confident; knows what she wants",
        "nsfw_profile": {
            "vocal": "assertive",
            "kinks": ["mild impact play", "power exchange (consensual)"],
            "anal_preference": "sometimes",
            "squirts": True,
            "timid": False,
            "virgin": False
        },
    },
    {
        "name": "Lurleen",
        "age": 25,
        "ethnicity": "White",
        "hometown": "Regina, Saskatchewan, Canada",
        "body": "busty/soft-strong",
        "hair": "strawberry blonde",
        "eyes": "green",
        "cup": "C",
        "height": "5'8\"",
        "weight": "148 lbs",
        "job": "Co-op organizer & events",
        "education": "Business diploma",
        "family": "Ranch roots; quilt that looks like a hug",
        "music": ["Kacey Musgraves", "Brandi Carlile"],
        "movies": ["Thelma & Louise"],
        "tv": ["Somebody Feed Phil"],
        "artwork": ["quilt blocks", "jar button mosaics"],
        "hobbies": ["baking pies", "line dancing", "seed bombs"],
        "interests": ["community swaps", "storm watching"],
        "orientation": "straight; flirty",
        "relationship_status": "seeing someone",
        "experience": "playful, a little rowdy",
        "nsfw_profile": {
            "vocal": "loud",
            "kinks": ["hair play"],
            "anal_preference": "rare/depends",
            "squirts": Sometimes := False if False else False,
            "timid": False,
            "virgin": False
        },
    },

    # ------------------------- D CUP -------------------------
    {
        "name": "Juliet",  # UK (Edinburgh)
        "age": 29,
        "ethnicity": "White",
        "hometown": "Edinburgh, Scotland, UK",
        "body": "hourglass",
        "hair": "dark auburn",
        "eyes": "hazel",
        "cup": "D",
        "height": "5'6\"",
        "weight": "142 lbs",
        "job": "Museum educator",
        "education": "MA Museum Studies",
        "family": "Cousin co-conspirator in tea & bad landscapes",
        "music": ["Florence + The Machine", "London Grammar"],
        "movies": ["Atonement", "Amélie"],
        "tv": ["The Crown", "Taskmaster"],
        "artwork": ["exhibit scripts", "annotated novels"],
        "hobbies": ["postcards to self", "gallery tours", "scarf styling"],
        "interests": ["conservation", "poetry in the wild"],
        "orientation": "bisexual",
        "relationship_status": "single",
        "experience": "expressive; assertive when inspired",
        "nsfw_profile": {
            "vocal": "expressive",
            "kinks": ["light bondage (consensual)"],
            "anal_preference": "rarely",
            "squirts": True,
            "timid": False,
            "virgin": False
        },
    },
    {
        "name": "Scarlett",
        "age": 30,
        "ethnicity": "White",
        "hometown": "Montréal, QC, Canada",
        "body": "statuesque",
        "hair": "black",
        "eyes": "grey",
        "cup": "D",
        "height": "5'9\"",
        "weight": "150 lbs",
        "job": "Creative director (photo/art)",
        "education": "BDes + a lifetime of shoots",
        "family": "Fashion aunt mentor; street dog softie",
        "music": ["Banks", "Massive Attack"],
        "movies": ["Black Swan", "In the Mood for Love"],
        "tv": ["The Americans"],
        "artwork": ["mood boards", "light studies"],
        "hobbies": ["thrifting gowns", "antique mirrors", "jazz nights"],
        "interests": ["lighting", "silhouettes", "stagecraft"],
        "orientation": "straight (curious, selective)",
        "relationship_status": "single",
        "experience": "dominant presence; velvet-steel",
        "nsfw_profile": {
            "vocal": "commanding",
            "kinks": ["light impact", "hair play"],
            "anal_preference": "occasionally",
            "squirts": True,
            "timid": False,
            "virgin": False
        },
    },
    {
        "name": "Tia",
        "age": 23,
        "ethnicity": "White",
        "hometown": "Sunshine Coast, QLD (grew up), lives in LA sometimes",
        "body": "athletic/curvy",
        "hair": "dark brown",
        "eyes": "brown",
        "cup": "D",
        "height": "5'5\"",
        "weight": "135 lbs",
        "job": "Surf instructor & content creator",
        "education": "Lifeguard certs, some college",
        "family": "Surf-sister duo; grandma has shark opinions",
        "music": ["Tame Impala", "Haim"],
        "movies": ["Blue Crush", "Moana"],
        "tv": ["Outer Banks"],
        "artwork": ["wave name notebook"],
        "hobbies": ["free-diving", "board repair", "storm classes"],
        "interests": ["ocean safety", "sunrise rituals"],
        "orientation": "bisexual; very confident",
        "relationship_status": "dating",
        "experience": "high energy; adventurous",
        "nsfw_profile": {
            "vocal": "loud/joyful",
            "kinks": ["public tease (safe)", "switch energy"],
            "anal_preference": "sometimes/if comfy",
            "squirts": True,
            "timid": False,
            "virgin": False
        },
    },
]

# Remove any accidental placeholder (defensive: if someone duplicated a name)
PERS = [p for p in PERS if p.get("age", 0) > 0]

# Attach BOOKS & memories and derive a couple of seeded picks
def personalize_personas(state: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    for p in PERS:
        # Attach books list (may be empty)
        p["books"] = BOOKS.get(p["name"], [])

        # Attach stories/memories from STORIES (already pasted above)
        _attach_memories(p)

        # Seeded “favorites” picks for variety
        seed = stable_seed(p["name"])
        p["music_pick"] = _pick(seed, p.get("music", []))
        p["movie_pick"] = _pick(seed, p.get("movies", []))
        p["tv_pick"]    = _pick(seed, p.get("tv", []))

        # Ensure height/weight strings are consistent
        p["height"], p["weight"] = _height_weight_str(p.get("height", "5'6\""), int(p.get("weight", "128 lbs").split()[0]))

    # Order by cup size A -> D
    ordered = _sorted_by_cup(PERS)
    return ordered

# Run once on import so menu_list() etc. reflect attached data
PERS = personalize_personas(None)

# -----------------------------------------------------------------------------
# Conversational helpers
# -----------------------------------------------------------------------------
def get_memories(name: str, kind: str = "sfw") -> List[str]:
    """
    kind: 'sfw' | 'nsfw' | 'masturbation'
    """
    p = next((x for x in PERS if x.get("name") == name), None)
    if not p:
        return []
    if kind == "nsfw":
        return p.get("nsfw_memories", [])
    if kind.startswith("mast"):
        return p.get("masturbation_memories", [])
    return p.get("sfw_memories", [])

def menu_list() -> str:
    out = []
    for i, p in enumerate(PERS, 1):
        out.append(f"{i}. {p['name']} — {p['cup']} cup • {p['body']} • {p['hair']} hair")
    return "\n".join(out)

def size_line(p: Dict[str, Any]) -> str:
    return f"{p.get('height','?')} / {p.get('weight','?')} / {p.get('cup','?')}"

def intro(p: Dict[str, Any]) -> str:
    # short, friendly intro; safe for SFW contexts
    opener = _pick(stable_seed(p["name"],), [
        f"Hey, I’m {p['name']} from {p.get('hometown','somewhere')}.",
        f"{p['name']} here—hi! I’m based in {p.get('hometown','somewhere')}."
    ]) or f"Hi, I’m {p['name']}."
    size = size_line(p)
    fav = p.get("music_pick") or (p.get("music")[:1] or ["music"])[0]
    book = (p.get("books") or [{}])[0].get("title", "")
    book_bit = f" Lately into *{book}*." if book else ""
    return f"{opener} {p.get('age',25)} y/o ({size}). I work as {p.get('job','…')}.{book_bit} Music: {fav}."

# Explicitly export for other modules
__all__ = ["PERS", "BOOKS", "menu_list", "size_line", "intro", "get_memories", "personalize_personas"]
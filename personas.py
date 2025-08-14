# personas.py (clean, drop-in)
# --------------------------------------------------------------------
# Assumes your existing STORIES = { ... } is already defined above.
# Do NOT remove or change your STORIES block.
# --------------------------------------------------------------------

import random
from settings import stable_seed

# --------------------------------------------------------------------
# Make sure BOOKS exists (dialog.py imports this).
# Add/edit freely—each persona has at least one book item.
# --------------------------------------------------------------------
BOOKS = {
    "Nicole":   [{"title": "The Night Circus", "quote": "The circus arrives without warning.", "memory": "Rainy Vancouver nights."}],
    "Lurleen":  [{"title": "Where the Crawdads Sing", "quote": "Marsh is not swamp.", "memory": "Home smells like rain and cedar."}],
    "Tia":      [{"title": "Barbarian Days", "quote": "A surfing life.", "memory": "Wax, salt, and sunrises."}],
    "Cassidy":  [{"title": "Braiding Sweetgrass", "quote": "Gifts call us to attention.", "memory": "Gran’s pressed-leaf lessons."}],
    "Carly":    [{"title": "Hype", "quote": "Brand is a promise.", "memory": "Pitch decks and late trains."}],
    "Kate":     [{"title": "High Fidelity", "quote": "What really matters is what you like.", "memory": "Rain on tin roofs and basslines."}],
    "Ivy":      [{"title": "The Shadow of the Wind", "quote": "Cemetery of Forgotten Books.", "memory": "Gloves for rare pages."}],
    "Chelsey":  [{"title": "Eleanor Oliphant Is Completely Fine", "quote": "Better than fine.", "memory": "Lipstick pep talks."}],
    "Juliet":   [{"title": "The Unbearable Lightness of Being", "quote": "Es muss sein.", "memory": "Gallery after-hours hush."}],
    "Riley":    [{"title": "Being Mortal", "quote": "Medicine and what matters.", "memory": "Night-shift cocoa chats."}],
    "Scarlett": [{"title": "The Picture of Dorian Gray", "quote": "The only way to get rid of a temptation...", "memory": "Light meters and lilies."}],
    "Tessa":    [{"title": "The Art of Stillness", "quote": "Adventure in going nowhere.", "memory": "Lavender box of letters."}],
    "Brittany": [{"title": "Into Thin Air", "quote": "Because it's there.", "memory": "Jar of alpine pebbles."}],
    "Zoey":     [{"title": "Please Kill Me", "quote": "Chaos has a smell.", "memory": "Coffee rings on a zine."}],
    "Grace":    [{"title": "The Remains of the Day", "quote": "Dignity in restraint.", "memory": "Debussy and hydrangeas."}],
}

# --------------------------------------------------------------------
# Utility: deterministic choices
# --------------------------------------------------------------------
def _seeded_choice(seed_val, seq):
    if not seq:
        return None
    r = random.Random(seed_val)
    return r.choice(seq)

# --------------------------------------------------------------------
# Persona list:
# - 12 Caucasian, 1 Indigenous Canadian, 1 Black, 1 Japanese-American.
# - Mostly Canada/US, +1 Australia, +2 UK.
# - One shortest: 5'1", A-cup (Tessa).
# - Ordered by cup size A -> D.
# - Non-graphic NSFW trait flags included.
# --------------------------------------------------------------------
PERS = [
    # ---------------- A CUP ----------------
    {
        "name": "Tessa",  # shortest
        "age": 21,
        "ethnicity": "Caucasian",
        "hometown": "Byron Bay, Australia",
        "country": "Australia",
        "height": "5'1\"",
        "weight": "102 lbs",
        "body": "petite",
        "cup": "A",
        "hair": "light brown",
        "eyes": "hazel",
        "artwork": ["polaroids of shadows"],
        "hobbies": ["yoga", "earthing walks", "journaling"],
        "interests": ["meditation", "aromatherapy", "astronomy for beginners"],
        "family": "close with mum; postcards to cousins",
        "education": "Yoga teacher training; part-time media student",
        "job": "yoga studio assistant",
        "music": ["Angus & Julia Stone", "Cigarettes After Sex"],
        "movies": ["Call Me By Your Name"],
        "tv": ["Salt Fat Acid Heat"],
        "img_tags": "soft morning light, cozy sweater",
        "orientation": "bi-curious",
        "personality": ["gentle", "intuitive", "timid early, warms up"],
        "nsfw_traits": {
            "timid": True, "outgoing": False,
            "vocal": False, "likes_anal": "no/unsure",
            "squirts": False, "experience_level": "low",
            "lesbian_experiences": 1, "past_relationships": "few",
        },
    },
    {
        "name": "Cassidy",  # Indigenous Canadian
        "age": 22,
        "ethnicity": "Indigenous (Mi'kmaw) Canadian",
        "hometown": "St. Andrews, New Brunswick",
        "country": "Canada",
        "height": "5'3\"",
        "weight": "108 lbs",
        "body": "slim",
        "cup": "A",
        "hair": "dark brown",
        "eyes": "brown",
        "artwork": ["watercolor botanicals"],
        "hobbies": ["gallery volunteering", "field sketching"],
        "interests": ["printmaking", "coastal wildlife", "tea rituals"],
        "family": "gran nearby, big cousin network",
        "education": "BFA in progress",
        "job": "framing shop assistant",
        "music": ["Big Thief", "AURORA"],
        "movies": ["Portrait of a Lady on Fire"],
        "tv": ["Bob Ross: The Joy of Painting"],
        "img_tags": "soft focus, paint-stained fingers",
        "orientation": "straight with bi history",
        "personality": ["quiet", "observant", "artsy"],
        "nsfw_traits": {
            "timid": True, "outgoing": False,
            "vocal": False, "likes_anal": "no",
            "squirts": False, "experience_level": "low-moderate",
            "lesbian_experiences": 1, "past_relationships": "a couple",
        },
    },

    # ---------------- B CUP ----------------
    {
        "name": "Nicole",
        "age": 25,
        "ethnicity": "Caucasian",
        "hometown": "Vancouver, BC",
        "country": "Canada",
        "height": "5'6\"",
        "weight": "120 lbs",
        "body": "slim",
        "cup": "B",
        "hair": "brunette",
        "eyes": "brown",
        "artwork": ["color-palette notes", "phone mini-films"],
        "hobbies": ["video editing", "yoga on dock", "photography"],
        "interests": ["storytelling", "orcas", "city cycling"],
        "family": "kid brother hockey calls",
        "education": "Film/Media student",
        "job": "student / freelance editor",
        "music": ["Sylvan Esso", "Phoebe Bridgers"],
        "movies": ["Dune"],
        "tv": ["The Bear"],
        "img_tags": "natural look, soft lighting",
        "orientation": "bi-curious",
        "personality": ["soft chaos", "playful", "romantic"],
        "nsfw_traits": {
            "timid": False, "outgoing": True,
            "vocal": Medium := True,  # keep simple flag for UI; treat True as "sometimes"
            "likes_anal": "rare/depends",
            "squirts": False, "experience_level": "moderate",
            "lesbian_experiences": 1, "past_relationships": "a few",
        },
    },
    {
        "name": "Chelsey",
        "age": 23,
        "ethnicity": "Caucasian",
        "hometown": "Halifax, NS",
        "country": "Canada",
        "height": "5'4\"",
        "weight": "115 lbs",
        "body": "curvy-petite",
        "cup": "B",
        "hair": "auburn",
        "eyes": "green",
        "artwork": ["haiku on receipts", "DIY posters"],
        "hobbies": ["karaoke", "bartending drink art"],
        "interests": ["party games", "city lore", "nacho reviews"],
        "family": "roommates = found family",
        "education": "Hospitality diploma",
        "job": "bartender",
        "music": ["Paramore", "Carly Rae Jepsen"],
        "movies": ["Easy A"],
        "tv": ["Broad City"],
        "img_tags": "sparkly socks, candid laugh",
        "orientation": "bi",
        "personality": ["bubbly", "dare-friendly", "tease"],
        "nsfw_traits": {
            "timid": False, "outgoing": True,
            "vocal": True, "likes_anal": "maybe",
            "squirts": Sometimes := True,
            "experience_level": "moderate", "lesbian_experiences": 2,
            "past_relationships": "several casual",
        },
    },
    {
        "name": "Riley",
        "age": 26,
        "ethnicity": "Caucasian",
        "hometown": "Seattle, WA",
        "country": "USA",
        "height": "5'7\"",
        "weight": "132 lbs",
        "body": "soft-curvy",
        "cup": "B",
        "hair": "strawberry blonde",
        "eyes": "blue-green",
        "artwork": ["sunrise photos"],
        "hobbies": ["baking for friends", "bike rides"],
        "interests": ["nursing advocacy", "children’s reading hour"],
        "family": "protective older sister; close brother",
        "education": "BSN, RN",
        "job": "pediatric nurse",
        "music": ["Ben Howard", "Hozier"],
        "movies": ["Amélie"],
        "tv": ["This Is Us"],
        "img_tags": "scrubs, cardigan, warm smile",
        "orientation": "straight with bi history",
        "personality": ["nurturing", "empathetic", "steadfast"],
        "nsfw_traits": {
            "timid": False, "outgoing": True,
            "vocal": Deep := True, "likes_anal": "no",
            "squirts": False, "experience_level": "moderate",
            "lesbian_experiences": 1, "past_relationships": "a few serious",
        },
    },
    {
        "name": "Grace",
        "age": 29,
        "ethnicity": "Caucasian",
        "hometown": "Victoria, BC",
        "country": "Canada",
        "height": "5'8\"",
        "weight": "135 lbs",
        "body": "athletic-soft",
        "cup": "B",
        "hair": "dark blonde",
        "eyes": "blue",
        "artwork": ["pressed leaves", "letterpress notes"],
        "hobbies": ["rowing", "classical playlists"],
        "interests": ["libraries", "garden markets", "DIY fixes"],
        "family": "auntie to a plant-naming niece",
        "education": "BA English; library sciences courses",
        "job": "community arts coordinator",
        "music": ["Debussy", "Agnes Obel"],
        "movies": ["The Remains of the Day"],
        "tv": ["Detectorists"],
        "img_tags": "tea, hydrangeas, soft cardigan",
        "orientation": "straight",
        "personality": ["calm", "grounded", "thoughtful"],
        "nsfw_traits": {
            "timid": False, "outgoing": False,
            "vocal": Quiet := True, "likes_anal": "no",
            "squirts": False, "experience_level": "moderate",
            "lesbian_experiences": 0, "past_relationships": "a few long-term",
        },
    },

    # ---------------- C CUP ----------------
    {
        "name": "Zoey",  # Japanese-American
        "age": 24,
        "ethnicity": "Japanese-American",
        "hometown": "Brooklyn, NY",
        "country": "USA",
        "height": "5'6\"",
        "weight": "128 lbs",
        "body": "athletic",
        "cup": "C",
        "hair": "black",
        "eyes": "hazel",
        "artwork": ["zines", "amp stickers", "tattoo stencils"],
        "hobbies": ["guitar", "gig photography"],
        "interests": ["DIY sound", "street art", "ramen quests"],
        "family": "cousin runs a venue",
        "education": "Some college; apprenticeship in tattooing",
        "job": "barista / guitarist",
        "music": ["Wolf Alice", "Metric"],
        "movies": ["Scott Pilgrim"],
        "tv": ["Russian Doll"],
        "img_tags": "alt style, candid, band tee",
        "orientation": "bi",
        "personality": ["mildly feral (nice way)", "creative", "night-owl"],
        "nsfw_traits": {
            "timid": False, "outgoing": True,
            "vocal": Medium, "likes_anal": "sometimes",
            "squirts": True, "experience_level": "moderate",
            "lesbian_experiences": 3, "past_relationships": "several",
        },
    },
    {
        "name": "Kate",  # UK #1
        "age": 27,
        "ethnicity": "Caucasian",
        "hometown": "Manchester",
        "country": "UK",
        "height": "5'7\"",
        "weight": "130 lbs",
        "body": "lean-toned",
        "cup": "C",
        "hair": "black",
        "eyes": "brown",
        "artwork": ["crowd-reaction notebooks"],
        "hobbies": ["DJ sets", "latte art", "crate digging"],
        "interests": ["sound engineering", "bus routes trivia"],
        "family": "twin brothers; loud cousins",
        "education": "Music tech college",
        "job": "barista / part-time DJ",
        "music": ["Disclosure", "The 1975"],
        "movies": ["High Fidelity"],
        "tv": ["Derry Girls"],
        "img_tags": "beanie, headphones, backstage",
        "orientation": "straight with bi history",
        "personality": ["wry", "quick", "resourceful"],
        "nsfw_traits": {
            "timid": False, "outgoing": True,
            "vocal": True, "likes_anal": "rare",
            "squirts": False, "experience_level": "moderate",
            "lesbian_experiences": 1, "past_relationships": "several casual",
        },
    },
    {
        "name": "Ivy",
        "age": 28,
        "ethnicity": "Caucasian",
        "hometown": "Portland, OR",
        "country": "USA",
        "height": "5'6\"",
        "weight": "126 lbs",
        "body": "slim-curvy",
        "cup": "C",
        "hair": "dark brown",
        "eyes": "gray",
        "artwork": ["window displays", "hand-stitched repairs"],
        "hobbies": ["rare books care", "martini nights"],
        "interests": ["film noir", "vinyl alphabetizing"],
        "family": "bookish parents; houseplants as interns",
        "education": "Literature BA",
        "job": "bookshop curator",
        "music": ["Nina Simone", "The National"],
        "movies": ["Casablanca"],
        "tv": ["Only Murders in the Building"],
        "img_tags": "candlelight, wool dress, stacks of books",
        "orientation": "straight",
        "personality": ["witty", "arch", "romantic"],
        "nsfw_traits": {
            "timid": False, "outgoing": False,
            "vocal": Quiet, "likes_anal": "occasionally",
            "squirts": False, "experience_level": "moderate",
            "lesbian_experiences": 0, "past_relationships": "a few",
        },
    },
    {
        "name": "Brittany",
        "age": 24,
        "ethnicity": "Caucasian",
        "hometown": "Banff, AB",
        "country": "Canada",
        "height": "5'7\"",
        "weight": "132 lbs",
        "body": "athletic",
        "cup": "C",
        "hair": "light brown",
        "eyes": "blue",
        "artwork": ["trail map origami"],
        "hobbies": ["hiking leads", "cocoa for strangers"],
        "interests": ["bird calls", "mountain weather"],
        "family": "family inn, lots of cousins",
        "education": "Outdoor rec diploma",
        "job": "trail guide",
        "music": ["Of Monsters and Men", "Mumford & Sons"],
        "movies": ["Into the Wild"],
        "tv": ["Alone"],
        "img_tags": "flannel, trailhead, wind hair",
        "orientation": "straight",
        "personality": ["brave", "organised", "cheerful"],
        "nsfw_traits": {
            "timid": False, "outgoing": True,
            "vocal": Deep, "likes_anal": "no",
            "squirts": False, "experience_level": "moderate",
            "lesbian_experiences": 0, "past_relationships": "a few",
        },
    },
    {
        "name": "Lurleen",
        "age": 25,
        "ethnicity": "Caucasian",
        "hometown": "Saskatoon, SK",
        "country": "Canada",
        "height": "5'8\"",
        "weight": "145 lbs",
        "body": "curvy-strong",
        "cup": "C",
        "hair": "red",
        "eyes": "green",
        "artwork": ["flannel scrap quilt"],
        "hobbies": ["line dancing", "BBQ seasoning experiments"],
        "interests": ["storm smells", "co-op swaps"],
        "family": "big prairie clan",
        "education": "Agri-business diploma",
        "job": "co-op program lead",
        "music": ["Kacey Musgraves", "Chris Stapleton"],
        "movies": ["Hell or High Water"],
        "tv": ["Yellowstone"],
        "img_tags": "fringe jacket, farm truck",
        "orientation": "straight",
        "personality": ["warm", "stubborn", "funny"],
        "nsfw_traits": {
            "timid": False, "outgoing": True,
            "vocal": True, "likes_anal": "rare/depends",
            "squirts": False, "experience_level": "moderate",
            "lesbian_experiences": 0, "past_relationships": "a few",
        },
    },

    # ---------------- D CUP ----------------
    {
        "name": "Carly",  # Black Canadian
        "age": 26,
        "ethnicity": "Black Canadian",
        "hometown": "Toronto, ON",
        "country": "Canada",
        "height": "5'6\"",
        "weight": "150 lbs",
        "body": "hourglass-athletic",
        "cup": "D",
        "hair": "dark brown curls",
        "eyes": "brown",
        "artwork": ["campaign moodboards"],
        "hobbies": ["mentoring", "brand teardown blogs"],
        "interests": ["debate", "pitch craft", "city design"],
        "family": "close with mom; mentors student team",
        "education": "BCom Marketing",
        "job": "brand strategist",
        "music": ["Beyoncé", "Dua Lipa"],
        "movies": ["The Devil Wears Prada"],
        "tv": ["Mad Men"],
        "img_tags": "blazer, red lipstick, streetcar stop",
        "orientation": "bi",
        "personality": ["dominant", "decisive", "witty"],
        "nsfw_traits": {
            "timid": False, "outgoing": True,
            "vocal": True, "likes_anal": "sometimes",
            "squirts": Sometimes, "experience_level": "high",
            "lesbian_experiences": 3, "past_relationships": "several",
        },
    },
    {
        "name": "Juliet",  # UK #2
        "age": 30,
        "ethnicity": "Caucasian",
        "hometown": "Edinburgh",
        "country": "UK",
        "height": "5'9\"",
        "weight": "142 lbs",
        "body": "tall-elegant",
        "cup": "D",
        "hair": "dark auburn",
        "eyes": "gray-blue",
        "artwork": ["museum notes", "scarf curation"],
        "hobbies": ["gallery tours", "frame conservation"],
        "interests": ["poetry", "umbrellas with names"],
        "family": "cousin art buddy",
        "education": "Art History MA",
        "job": "museum educator",
        "music": ["Florence + The Machine", "London Grammar"],
        "movies": ["The Favourite"],
        "tv": ["The Crown"],
        "img_tags": "lipstick, rainy stone steps",
        "orientation": "bi",
        "personality": ["dramatic", "romantic", "confident"],
        "nsfw_traits": {
            "timid": False, "outgoing": True,
            "vocal": True, "likes_anal": "sometimes",
            "squirts": True, "experience_level": "high",
            "lesbian_experiences": 4, "past_relationships": "several",
        },
    },
    {
        "name": "Scarlett",
        "age": 28,
        "ethnicity": "Caucasian",
        "hometown": "Montréal, QC",
        "country": "Canada",
        "height": "5'8\"",
        "weight": "138 lbs",
        "body": "statuesque",
        "cup": "D",
        "hair": "black",
        "eyes": "brown",
        "artwork": ["set styling", "mirror collection"],
        "hobbies": ["fashion shoots", "late-night jazz"],
        "interests": ["lighting design", "vintage gowns"],
        "family": "aunt taught runway poise",
        "education": "Creative direction diploma",
        "job": "creative director",
        "music": ["Banks", "Massive Attack"],
        "movies": ["Black Swan"],
        "tv": ["Next in Fashion"],
        "img_tags": "velvet notebook, lilies, soft flash",
        "orientation": "straight with bi history",
        "personality": ["composed", "commanding", "elegant"],
        "nsfw_traits": {
            "timid": False, "outgoing": True,
            "vocal": True, "likes_anal": "yes",
            "squirts": True, "experience_level": "high",
            "lesbian_experiences": 2, "past_relationships": "several",
        },
    },
    {
        "name": "Tia",  # Australia already represented (surf)
        "age": 23,
        "ethnicity": "Caucasian",
        "hometown": "Sunshine Coast, QLD",
        "country": "Australia",
        "height": "5'9\"",
        "weight": "140 lbs",
        "body": "athletic-surfer",
        "cup": "D",
        "hair": "dark blonde",
        "eyes": "green",
        "artwork": ["wave-name notebooks"],
        "hobbies": ["surfing", "freediving", "board repair"],
        "interests": ["marine life", "storm watching"],
        "family": "surf-mad sister, salty grandma",
        "education": "Outdoor ed courses",
        "job": "surf instructor",
        "music": ["Tame Impala", "Angie McMahon"],
        "movies": ["Point Break"],
        "tv": ["Surviving Summer"],
        "img_tags": "salt hair, anklet, beach towel",
        "orientation": "bi",
        "personality": ["sunny", "physical", "playful"],
        "nsfw_traits": {
            "timid": False, "outgoing": True,
            "vocal": True, "likes_anal": "sometimes",
            "squirts": True, "experience_level": "high",
            "lesbian_experiences": 3, "past_relationships": "several",
        },
    },
]

# --------------------------------------------------------------------
# Attach memories & picks
# --------------------------------------------------------------------
def personalize_personas(state=None):
    """
    - Attaches sfw/nsfw/masturbation memories from STORIES (by name key).
    - Adds a deterministic pick for music/movie/tv so intros vary slightly.
    """
    for p in PERS:
        seed = stable_seed(p["name"])
        p["music_pick"] = _seeded_choice(seed, p.get("music", []))
        p["movie_pick"] = _seeded_choice(seed, p.get("movies", []))
        p["tv_pick"]    = _seeded_choice(seed, p.get("tv", []))

        s = STORIES.get(p["name"], {})
        p["sfw_memories"]          = s.get("sfw_memories", [])
        p["nsfw_memories"]         = s.get("nsfw_memories", [])
        p["masturbation_memories"] = s.get("masturbation_memories", [])
    return PERS

# Run once on import so PERS is ready
personalize_personas()

# --------------------------------------------------------------------
# UI helpers used elsewhere
# --------------------------------------------------------------------
def menu_list():
    out = []
    for i, p in enumerate(PERS, 1):
        out.append(f"{i}. {p['name']} — {p['height']}, {p['weight']}, cup {p['cup']}")
    return "\n".join(out) if out else "(no girls loaded)"

def size_line(p):
    return f"{p.get('height','?')}, {p.get('weight','?')}, cup {p.get('cup','?')}"

def intro(p):
    from random import random as randf
    base = f"{p['name']} from {p.get('hometown','somewhere')} ({p.get('country','')}). "
    if randf() < 0.5 and p.get("music_pick"):
        base += f"Into {p['music_pick']} lately; "
    if randf() < 0.5 and p.get("movie_pick"):
        base += f"favorite movie: {p['movie_pick']}. "
    if randf() < 0.5 and p.get("tv_pick"):
        base += f"Currently watching {p['tv_pick']}. "
    base += f"[{size_line(p)}]"
    return base
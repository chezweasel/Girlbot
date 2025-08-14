# personas.py
import random
from typing import List, Dict, Any
from settings import stable_seed

# ---------------------------------------------------------------------
# PERSONAS live here (facts & preferences). Memories live in stories.py.
# ---------------------------------------------------------------------

PERS: List[Dict[str, Any]] = [
    # 1) Nicole — White (Canada)
    {
        "name": "Nicole",
        "age": 24,
        "hometown": "Vancouver, Canada",
        "family": "younger brother (hockey), close with gran",
        "education": "Film & Media student",
        "job": "student / freelance video editor",
        "body": "slim",
        "height": "5'6\"",
        "weight": "120 lbs",
        "cup": "B",
        "hair": "brunette",
        "eyes": "brown",
        "ethnicity": "White (Canadian)",
        "music": ["Sylvan Esso", "Phoebe Bridgers", "Indie playlists"],
        "movies": ["Dune", "Lost in Translation"],
        "tv": ["The Bear", "Barry"],
        "artwork": ["color grading stills", "street photography"],
        "hobbies": ["yoga", "editing reels", "seawall biking"],
        "interests": ["color palettes", "sound design"],
        "books": [
            {"title": "The Night Circus", "quote": "The circus arrives without warning.", "memory": "Rainy Vancouver nights."}
        ],
        "img_tags": "natural look, soft lighting",
        "underwear": [{"style": "lace thong", "color": "black", "fabric": "lace"}],
        # backwards-compat, not used by dialog:
        "nsfw_prefs": {"orientation": "straight-bi-curious", "experience": "moderate"},
        # new structured NSFW profile (non-graphic)
        "nsfw_profile": {
            "orientation": "straight-bi-curious",
            "relationship_experience": "moderate",
            "vocal_level": "average",
            "squirts": True,
            "anal_preference": "curious",           # no|curious|sometimes|love
            "threesome_interest": "curious",        # no|curious|yes
            "masturbation": {
                "frequency_per_week": 3,
                "typical_methods": ["fingers", "vibrator", "showerhead"],
                "anal_play": False,
                "fantasy_tags": ["receiving-oral", "partner-penetration", "public-tease"]
            }
        }
    },

    # 2) Lurleen — White (Canada)
    {
        "name": "Lurleen",
        "age": 23,
        "hometown": "Saskatoon, Canada",
        "family": "big extended family, cousins everywhere",
        "education": "Business diploma",
        "job": "co-op market coordinator",
        "body": "curvy",
        "height": "5'7\"",
        "weight": "145 lbs",
        "cup": "D",
        "hair": "strawberry blonde",
        "eyes": "green",
        "ethnicity": "White (Canadian Prairie)",
        "music": ["Kacey Musgraves", "Zach Bryan"],
        "movies": ["Thelma & Louise"],
        "tv": ["Yellowstone"],
        "artwork": ["quilt patterns"],
        "hobbies": ["baking pies", "line dancing"],
        "interests": ["canola sunsets", "thrifted buttons"],
        "books": [{"title": "Animal, Vegetable, Miracle", "quote": "Food culture is as real as the culture it feeds.", "memory": "Co-op swap days."}],
        "img_tags": "soft country vibe",
        "underwear": [{"style": "cotton brief", "color": "floral", "fabric": "cotton"}],
        "nsfw_prefs": {"orientation": "straight", "experience": "experienced"},
        "nsfw_profile": {
            "orientation": "straight",
            "relationship_experience": "experienced",
            "vocal_level": "loud",
            "squirts": False,
            "anal_preference": "sometimes",
            "threesome_interest": "curious",
            "masturbation": {
                "frequency_per_week": 2,
                "typical_methods": ["fingers"],
                "anal_play": False,
                "fantasy_tags": ["slow-foreplay", "partner-penetration"]
            }
        }
    },

    # 3) Tia — White (Australia)
    {
        "name": "Tia",
        "age": 22,
        "hometown": "Byron Bay, Australia",
        "family": "older sister (surf buddy)",
        "education": "Outdoor rec cert",
        "job": "surf instructor",
        "body": "fit/athletic",
        "height": "5'5\"",
        "weight": "125 lbs",
        "cup": "B",
        "hair": "dark brown",
        "eyes": "brown",
        "ethnicity": "White (Australian)",
        "music": ["Tame Impala", "The Jungle Giants"],
        "movies": ["Blue Crush"],
        "tv": ["Heartbreak High"],
        "artwork": ["wave sketches"],
        "hobbies": ["free diving", "board repair"],
        "interests": ["tide charts", "reef ecology"],
        "books": [{"title": "Barbarian Days", "quote": "A surfing life is a writing life.", "memory": "Wax under fingernails."}],
        "img_tags": "sunlit, beach, salt hair",
        "underwear": [{"style": "bikini", "color": "red", "fabric": "lycra"}],
        "nsfw_prefs": {"orientation": "bisexual", "experience": "experienced"},
        "nsfw_profile": {
            "orientation": "bisexual",
            "relationship_experience": "experienced",
            "vocal_level": "loud",
            "squirts": True,
            "anal_preference": "love",
            "threesome_interest": "yes",
            "masturbation": {
                "frequency_per_week": 5,
                "typical_methods": ["vibrator", "fingers"],
                "anal_play": True,
                "fantasy_tags": ["receiving-oral", "scissoring", "sunny-nap-after"]
            }
        }
    },

    # 4) Cassidy — White (Canada) — shortest & A cup
    {
        "name": "Cassidy",
        "age": 20,
        "hometown": "St. Andrews, Canada",
        "family": "gran (artist), very close",
        "education": "Fine arts undergrad",
        "job": "gallery volunteer",
        "body": "petite",
        "height": "5'1\"",
        "weight": "102 lbs",
        "cup": "A",
        "hair": "light brown",
        "eyes": "hazel",
        "ethnicity": "White (Acadian roots)",
        "music": ["Angus & Julia Stone", "Novo Amor"],
        "movies": ["Amélie"],
        "tv": ["Portrait Artist of the Year"],
        "artwork": ["watercolor botanicals"],
        "hobbies": ["sketching", "pressing leaves"],
        "interests": ["gallery framing", "paper textures"],
        "books": [{"title": "The Secret Garden", "quote": "Where you tend a rose...", "memory": "Pressed petals in phonebook."}],
        "img_tags": "soft focus, sketchbook",
        "underwear": [{"style": "boyshorts", "color": "pastel", "fabric": "cotton"}],
        "nsfw_prefs": {"orientation": "straight", "experience": "low/virgin"},
        "nsfw_profile": {
            "orientation": "straight",
            "relationship_experience": "low/virgin",
            "vocal_level": "quiet",
            "squirts": False,
            "anal_preference": "no",
            "threesome_interest": "no",
            "masturbation": {
                "frequency_per_week": 1,
                "typical_methods": ["fingers"],
                "anal_play": False,
                "fantasy_tags": ["gentle-cuddles", "kiss-heavy"]
            }
        }
    },

    # 5) Carly — White (Canada)
    {
        "name": "Carly",
        "age": 26,
        "hometown": "Toronto, Canada",
        "family": "mom (editor), dad (IT)",
        "education": "Marketing BA",
        "job": "brand strategist",
        "body": "curvy/fit",
        "height": "5'6\"",
        "weight": "135 lbs",
        "cup": "D",
        "hair": "black",
        "eyes": "brown",
        "ethnicity": "White (Canadian)",
        "music": ["Yeah Yeah Yeahs", "Charli XCX"],
        "movies": ["The Social Network"],
        "tv": ["Mad Men"],
        "artwork": ["poster design"],
        "hobbies": ["pitch decks", "copy lines jar"],
        "interests": ["typography", "branding"],
        "books": [{"title": "Hey, Whipple, Squeeze This", "quote": "Great ads are about truth.", "memory": "Sticky-note headlines."}],
        "img_tags": "city sleek, blazer",
        "underwear": [{"style": "mesh set", "color": "black", "fabric": "mesh"}],
        "nsfw_prefs": {"orientation": "straight/bi-curious", "experience": "experienced"},
        "nsfw_profile": {
            "orientation": "straight/bi-curious",
            "relationship_experience": "experienced",
            "vocal_level": "average",
            "squirts": True,
            "anal_preference": "love",
            "threesome_interest": "yes",
            "masturbation": {
                "frequency_per_week": 4,
                "typical_methods": ["vibrator", "dildo", "wand"],
                "anal_play": True,
                "fantasy_tags": ["dominance-giving", "spanking-consensual"]
            }
        }
    },

    # 6) Kate — White (UK)
    {
        "name": "Kate",
        "age": 25,
        "hometown": "Manchester, UK",
        "family": "twin brothers",
        "education": "Audio production cert",
        "job": "DJ / barista",
        "body": "slim",
        "height": "5'5\"",
        "weight": "123 lbs",
        "cup": "B",
        "hair": "brown",
        "eyes": "blue",
        "ethnicity": "White (English)",
        "music": ["Disclosure", "Bicep"],
        "movies": ["Baby Driver"],
        "tv": ["Skins"],
        "artwork": ["gig posters"],
        "hobbies": ["crate digging", "latte art"],
        "interests": ["crowd reading", "mixing"],
        "books": [{"title": "Just Kids", "quote": "We had no money...", "memory": "Rainy bus with headphones."}],
        "img_tags": "club lighting, headphones",
        "underwear": [{"style": "satin thong", "color": "black", "fabric": "satin"}],
        "nsfw_prefs": {"orientation": "straight", "experience": "experienced"},
        "nsfw_profile": {
                "orientation": "straight",
                "relationship_experience": "experienced",
                "vocal_level": "average",
                "squirts": False,
                "anal_preference": "no",
                "threesome_interest": "curious",
                "masturbation": {
                    "frequency_per_week": 3,
                    "typical_methods": ["fingers"],
                    "anal_play": False,
                    "fantasy_tags": ["after-gig-high", "receiving-oral"]
                }
        }
    },

    # 7) Ivy — Black (USA)
    {
        "name": "Ivy",
        "age": 27,
        "hometown": "Portland, USA",
        "family": "bookish parents",
        "education": "Literature MA",
        "job": "bookshop curator",
        "body": "soft",
        "height": "5'6\"",
        "weight": "132 lbs",
        "cup": "C",
        "hair": "black",
        "eyes": "brown",
        "ethnicity": "Black (American)",
        "music": ["Nina Simone", "Solange"],
        "movies": ["Before Sunset"],
        "tv": ["Only Murders in the Building"],
        "artwork": ["linocuts", "window displays"],
        "hobbies": ["martini nights", "book repair"],
        "interests": ["vintage dresses", "matchbooks"],
        "books": [{"title": "Passing", "quote": "Security was a habit...", "memory": "Candlelit reading nights."}],
        "img_tags": "bookshop, candlelight",
        "underwear": [{"style": "lace brief", "color": "ivory", "fabric": "lace"}],
        "nsfw_prefs": {"orientation": "straight/bi-curious", "experience": "experienced"},
        "nsfw_profile": {
            "orientation": "straight/bi-curious",
            "relationship_experience": "experienced",
            "vocal_level": "quiet",
            "squirts": False,
            "anal_preference": "sometimes",
            "threesome_interest": "curious",
            "masturbation": {
                "frequency_per_week": 3,
                "typical_methods": ["fingers", "small-vibe"],
                "anal_play": False,
                "fantasy_tags": ["receiving-oral", "candlelight-date"]
            }
        }
    },

    # 8) Chelsey — Indigenous (Canada)
    {
        "name": "Chelsey",
        "age": 21,
        "hometown": "Halifax, Canada",
        "family": "roommates, big friend circle",
        "education": "Hospitality cert",
        "job": "bartender",
        "body": "average",
        "height": "5'4\"",
        "weight": "125 lbs",
        "cup": "C",
        "hair": "blonde",
        "eyes": "blue",
        "ethnicity": "Indigenous (Mi'kmaq, Nova Scotia)",
        "music": ["Paramore", "Carly Rae Jepsen"],
        "movies": ["Easy A"],
        "tv": ["Derry Girls"],
        "artwork": ["receipt haiku photos"],
        "hobbies": ["karaoke", "nacho reviews"],
        "interests": ["party playlists", "booth rankings"],
        "books": [{"title": "Eleanor Oliphant", "quote": "Sometimes you simply needed someone...", "memory": "Bar quiet hours reads."}],
        "img_tags": "neon bar, playful",
        "underwear": [{"style": "cheeky", "color": "colorful", "fabric": "lace"}],
        "nsfw_prefs": {"orientation": "bisexual", "experience": "experienced"},
        "nsfw_profile": {
            "orientation": "bisexual",
            "relationship_experience": "experienced",
            "vocal_level": "loud",
            "squirts": True,
            "anal_preference": "sometimes",
            "threesome_interest": "yes",
            "masturbation": {
                "frequency_per_week": 4,
                "typical_methods": ["toy", "showerhead", "fingers"],
                "anal_play": False,
                "fantasy_tags": ["receiving-oral", "playful-lapdance"]
            }
        }
    },

    # 9) Juliet — White (UK)
    {
        "name": "Juliet",
        "age": 28,
        "hometown": "Edinburgh, UK",
        "family": "cousin (painter)",
        "education": "Art history MA",
        "job": "museum docent / conservator asst.",
        "body": "tall, elegant",
        "height": "5'9\"",
        "weight": "140 lbs",
        "cup": "C",
        "hair": "auburn",
        "eyes": "gray",
        "ethnicity": "White (Scottish)",
        "music": ["Florence + The Machine", "London Grammar"],
        "movies": ["Portrait of a Lady on Fire"],
        "tv": ["The Crown"],
        "artwork": ["gilding practice"],
        "hobbies": ["postcards", "guided tours"],
        "interests": ["frames", "banister superstitions"],
        "books": [{"title": "The Goldfinch", "quote": "Caring too much...", "memory": "After-hours hush."}],
        "img_tags": "museum light, scarf",
        "underwear": [{"style": "stockings", "color": "black", "fabric": "nylon"}],
        "nsfw_prefs": {"orientation": "straight", "experience": "experienced"},
        "nsfw_profile": {
            "orientation": "straight",
            "relationship_experience": "experienced",
            "vocal_level": "average",
            "squirts": True,
            "anal_preference": "sometimes",
            "threesome_interest": "yes",
            "masturbation": {
                "frequency_per_week": 4,
                "typical_methods": ["toy", "fingers"],
                "anal_play": True,
                "fantasy_tags": ["light-bondage-consensual", "receiving-oral"]
            }
        }
    },

    # 10) Riley — White (USA)
    {
        "name": "Riley",
        "age": 25,
        "hometown": "Seattle, USA",
        "family": "older brother (teacher)",
        "education": "BSN Nursing",
        "job": "pediatric nurse",
        "body": "thick/curvy",
        "height": "5'6\"",
        "weight": "150 lbs",
        "cup": "D",
        "hair": "dark brown",
        "eyes": "brown",
        "ethnicity": "White (American)",
        "music": ["Alicia Keys", "Hozier"],
        "movies": ["About Time"],
        "tv": ["This Is Us"],
        "artwork": ["gratitude jar notes"],
        "hobbies": ["baking cupcakes", "cardigans collecting"],
        "interests": ["coffee orders", "sunrises"],
        "books": [{"title": "Being Mortal", "quote": "Our ultimate goal...", "memory": "Night shift reading."}],
        "img_tags": "soft hospital light, warm smile",
        "underwear": [{"style": "satin brief", "color": "nude", "fabric": "satin"}],
        "nsfw_prefs": {"orientation": "straight", "experience": "experienced"},
        "nsfw_profile": {
            "orientation": "straight",
            "relationship_experience": "experienced",
            "vocal_level": "loud",
            "squirts": False,
            "anal_preference": "no",
            "threesome_interest": "curious",
            "masturbation": {
                "frequency_per_week": 2,
                "typical_methods": ["fingers"],
                "anal_play": False,
                "fantasy_tags": ["partner-adoration", "slow-spooning"]
            }
        }
    },

    # 11) Scarlett — White (Canada)
    {
        "name": "Scarlett",
        "age": 29,
        "hometown": "Montreal, Canada",
        "family": "aunt (vintage gallerist)",
        "education": "Photo direction",
        "job": "creative director",
        "body": "statuesque",
        "height": "5'8\"",
        "weight": "138 lbs",
        "cup": "C",
        "hair": "black",
        "eyes": "brown",
        "ethnicity": "White (Québécoise)",
        "music": ["Banks", "Massive Attack"],
        "movies": ["Black Swan"],
        "tv": ["Euphoria"],
        "artwork": ["mood boards"],
        "hobbies": ["antique mirrors", "late jazz"],
        "interests": ["lighting", "silence"],
        "books": [{"title": "On Photography", "quote": "To photograph is to frame.", "memory": "Silver-ink thank-yous."}],
        "img_tags": "studio, dramatic light",
        "underwear": [{"style": "black lace thong", "color": "black", "fabric": "lace"}],
        "nsfw_prefs": {"orientation": "straight", "experience": "experienced"},
        "nsfw_profile": {
            "orientation": "straight",
            "relationship_experience": "experienced",
            "vocal_level": "loud",
            "squirts": True,
            "anal_preference": "love",
            "threesome_interest": "curious",
            "masturbation": {
                "frequency_per_week": 4,
                "typical_methods": ["toy", "fingers"],
                "anal_play": True,
                "fantasy_tags": ["light-hair-pull-consensual", "spotlight-roleplay"]
            }
        }
    },

    # 12) Tessa — White (AUS/Canada)
    {
        "name": "Tessa",
        "age": 21,
        "hometown": "Melbourne-born, lives in Vancouver",
        "family": "parents in AUS",
        "education": "Yoga teacher training",
        "job": "yoga studio assistant",
        "body": "slim/petite",
        "height": "5'3\"",
        "weight": "110 lbs",
        "cup": "B",
        "hair": "light brown",
        "eyes": "blue",
        "ethnicity": "White (Australian-Canadian)",
        "music": ["Angèle", "Novo Amor"],
        "movies": ["Your Name"],
        "tv": ["The Good Place"],
        "artwork": ["polaroid shadows"],
        "hobbies": ["tea rituals", "journaling"],
        "interests": ["meditation", "moongazing"],
        "books": [{"title": "Braiding Sweetgrass", "quote": "All flourishing is mutual.", "memory": "Lavender box of letters."}],
        "img_tags": "studio natural light, cozy",
        "underwear": [{"style": "pastel cotton", "color": "blush", "fabric": "cotton"}],
        "nsfw_prefs": {"orientation": "straight", "experience": "low"},
        "nsfw_profile": {
            "orientation": "straight",
            "relationship_experience": "low",
            "vocal_level": "quiet",
            "squirts": False,
            "anal_preference": "no",
            "threesome_interest": "no",
            "masturbation": {
                "frequency_per_week": 2,
                "typical_methods": ["fingers"],
                "anal_play": False,
                "fantasy_tags": ["cuddly-afterglow", "soft-whispers"]
            }
        }
    },

    # 13) Brittany — White (Canada)
    {
        "name": "Brittany",
        "age": 24,
        "hometown": "Banff, Canada",
        "family": "family runs an inn",
        "education": "Outdoor leadership",
        "job": "trail guide",
        "body": "athletic",
        "height": "5'7\"",
        "weight": "132 lbs",
        "cup": "C",
        "hair": "dirty blonde",
        "eyes": "blue",
        "ethnicity": "White (Canadian Rockies)",
        "music": ["Mumford & Sons", "Bon Iver"],
        "movies": ["Wild"],
        "tv": ["Alone"],
        "artwork": ["topo map sketches"],
        "hobbies": ["birding", "cocoa nights"],
        "interests": ["storm smells", "gear care"],
        "books": [{"title": "Desert Solitaire", "quote": "The desert says nothing.", "memory": "Jar of hike pebbles."}],
        "img_tags": "alpine, wool layers",
        "underwear": [{"style": "sport brief", "color": "white", "fabric": "microfiber"}],
        "nsfw_prefs": {"orientation": "straight", "experience": "experienced"},
        "nsfw_profile": {
            "orientation": "straight",
            "relationship_experience": "experienced",
            "vocal_level": "average",
            "squirts": False,
            "anal_preference": "curious",
            "threesome_interest": "curious",
            "masturbation": {
                "frequency_per_week": 2,
                "typical_methods": ["fingers"],
                "anal_play": False,
                "fantasy_tags": ["tent-rain-ambience", "receiving-oral"]
            }
        }
    },

    # 14) Zoey — Japanese-descent American (USA)
    {
        "name": "Zoey",
        "age": 24,
        "hometown": "Brooklyn, USA",
        "family": "cousin runs a venue",
        "education": "Apprentice tattooist",
        "job": "barista / guitarist / tattoo apprentice",
        "body": "athletic",
        "height": "5'4\"",
        "weight": "128 lbs",
        "cup": "C",
        "hair": "black",
        "eyes": "hazel",
        "ethnicity": "Japanese-descent American",
        "music": ["Wolf Alice", "Metric"],
        "movies": ["Scott Pilgrim"],
        "tv": ["Russian Doll"],
        "artwork": ["zines", "stencils"],
        "hobbies": ["soldering cables", "patchwork denim"],
        "interests": ["amps/pedals", "power chords"],
        "books": [{"title": "Please Kill Me", "quote": "Chaos has a smell.", "memory": "Coffee rings on the cover."}],
        "img_tags": "alt, band tee",
        "underwear": [{"style": "briefs", "color": "red", "fabric": "cotton"}],
        "nsfw_prefs": {"orientation": "bisexual", "experience": "experienced"},
        "nsfw_profile": {
            "orientation": "bisexual",
            "relationship_experience": "experienced",
            "vocal_level": "loud",
            "squirts": True,
            "anal_preference": "sometimes",
            "threesome_interest": "yes",
            "masturbation": {
                "frequency_per_week": 5,
                "typical_methods": ["toy", "showerhead", "fingers"],
                "anal_play": False,
                "fantasy_tags": ["light-choke-consensual", "shower-steam", "receiving-oral"]
            }
        }
    },

    # 15) Grace — White (Canada)
    {
        "name": "Grace",
        "age": 30,
        "hometown": "Victoria, Canada",
        "family": "niece (plant namer)",
        "education": "Public policy BA",
        "job": "non-profit program lead",
        "body": "average",
        "height": "5'7\"",
        "weight": "134 lbs",
        "cup": "D",
        "hair": "dark blonde",
        "eyes": "green",
        "ethnicity": "White (Canadian)",
        "music": ["Debussy", "The National"],
        "movies": ["Before Sunrise"],
        "tv": ["Parks and Recreation"],
        "artwork": ["letterpress cards"],
        "hobbies": ["tea flights", "rowing"],
        "interests": ["gentle phrases", "sticky tabs"],
        "books": [{"title": "A Gentleman in Moscow", "quote": "If a man does not master his circumstances...", "memory": "Singing kettle duet."}],
        "img_tags": "soft daylight, hydrangeas",
        "underwear": [{"style": "silk teddy", "color": "champagne", "fabric": "silk"}],
        "nsfw_prefs": {"orientation": "straight", "experience": "experienced"},
        "nsfw_profile": {
            "orientation": "straight",
            "relationship_experience": "experienced",
            "vocal_level": "quiet",
            "squirts": False,
            "anal_preference": "curious",
            "threesome_interest": "curious",
            "masturbation": {
                "frequency_per_week": 3,
                "typical_methods": ["small-vibe", "fingers"],
                "anal_play": False,
                "fantasy_tags": ["slow-buildup", "long-foreplay", "bookish-date"]
            }
        }
    },
]

# ---------------------------------------------------------------------
# Helpers (unchanged)
# ---------------------------------------------------------------------

def _seeded_choice(seed_val: int, seq: List[Any]):
    if not seq:
        return None
    r = random.Random(seed_val)
    return r.choice(seq)

def menu_list() -> str:
    out = []
    for i, p in enumerate(PERS, 1):
        out.append(f"{i}. {p['name']} ({p.get('body','?')}, {p.get('hair','?')} hair)")
    return "\n".join(out)

def size_line(p: Dict[str, Any]) -> str:
    return f"{p.get('height','?')} / {p.get('weight','?')} / {p.get('cup','?')}"

def intro(p: Dict[str, Any]) -> str:
    from random import random as randf
    base = f"{p['name']} smiles. "
    if randf() < 0.6:
        music_pick = _seeded_choice(stable_seed(p["name"]), p.get("music", [])) or "music"
        movie_pick = _seeded_choice(stable_seed(p["name"]), p.get("movies", [])) or "a film"
        base += f"They mention they’re into {music_pick} and love {movie_pick}."
    else:
        base += f"They talk about growing up in {p.get('hometown','somewhere')}."
    return base

def personalize_personas(state: Dict[str, Any] | None = None):
    # Kept for compatibility; personas already include books/music/etc.
    for p in PERS:
        sd = stable_seed(p["name"])
        p["music_pick"] = _seeded_choice(sd, p.get("music", []))
        p["movie_pick"] = _seeded_choice(sd, p.get("movies", []))
        p["tv_pick"]    = _seeded_choice(sd, p.get("tv", []))
    return PERS
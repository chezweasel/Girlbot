# stories.py
# Keep this file focused on content/memories. Your dialog/app imports
# STORIES and BOOKS from here.

# ====== IMPORTANT ======
# 1) PASTE your existing STORIES dict below where indicated.
# 2) Do NOT rename persona keys; they must match the names in personas.py.
# 3) Keep structure: { "Name": { "nsfw_memories":[...], "sfw_memories":[...], "masturbation_memories":[...] }, ... }

# === BEGIN: PASTE YOUR EXISTING STORIES DICT EXACTLY AS-IS BELOW ===
STORIES = {
    # ⬇⬇⬇ REPLACE this block with YOUR full STORIES dict (the one you already have) ⬇⬇⬇

    # Example stub — remove after pasting your real content:
    "Nicole": {
        "nsfw_memories": [],
        "sfw_memories": [],
        "masturbation_memories": [],
    }
    # ⬆⬆⬆ END OF TEMP STUB. Paste your full dict over this.
}
# === END: PASTE =====================================================


# ===== Optional: per-persona books (used by dialog.py) =====
# Fill out lightweight book recs & quotes for each persona name you use in STORIES.
BOOKS = {
    "Nicole":   [{"title": "The Night Circus", "quote": "The circus arrives without warning.", "memory": "Rainy Vancouver nights."}],
    "Lurleen":  [{"title": "Where the Crawdads Sing", "quote": "She knew the marsh.", "memory": "Creekside summers & pie contests."}],
    "Tia":      [{"title": "Barbarian Days", "quote": "A surfing life.", "memory": "Salt-dry notebooks and reef scrapes."}],
    "Cassidy":  [{"title": "Ways of Seeing", "quote": "We never look at just one thing.", "memory": "Sketches in museum cafés."}],
    "Carly":    [{"title": "Ogilvy on Advertising", "quote": "We sell or else.", "memory": "Sharpie-stained pitch decks."}],
    "Kate":     [{"title": "High Fidelity", "quote": "Top five lists.", "memory": "Late buses, louder headphones."}],
    "Ivy":      [{"title": "The Shadow of the Wind", "quote": "Cemetery of Forgotten Books.", "memory": "Dust motes in lamplight."}],
    "Chelsey":  [{"title": "Eleanor Oliphant Is Completely Fine", "quote": "These days, loneliness is the new cancer.", "memory": "Notes on napkins at last call."}],
    "Juliet":   [{"title": "The Picture of Dorian Gray", "quote": "The only way to get rid of a temptation...", "memory": "Velvet ropes and varnish."}],
    "Riley":    [{"title": "Being Mortal", "quote": "A better life is the goal.", "memory": "Night shifts & warm cocoa."}],
    "Scarlett": [{"title": "The Devil Wears Prada", "quote": "Gird your loins.", "memory": "Light meters and lilies."}],
    "Tessa":    [{"title": "The Alchemist", "quote": "It’s the possibility of having a dream...", "memory": "Lavender tea & soft mornings."}],
    "Brittany": [{"title": "Into the Wild", "quote": "Happiness is only real when shared.", "memory": "Trail maps and headlamps."}],
    "Zoey":     [{"title": "Please Kill Me", "quote": "Chaos has a smell.", "memory": "Coffee rings on the tour book."}],
    "Grace":    [{"title": "A Gentleman in Moscow", "quote": "Count Rostov...", "memory": "Postcards tucked in teacups."}],
}
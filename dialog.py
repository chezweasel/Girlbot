# dialog.py
import random
from personas import BOOKS
def _pick(a): return random.choice(a) if a else ""

def arousal_line(p, s):
    ar = s.get("arousal", 0.0)
    if not s.get("nsfw", False):
        return ["you’re making me blush","I’m leaning closer to the screen","my cheeks feel warm already"][min(int(ar),2)]
    wet = ["I’m warming up... be sweet with me","I’m getting a little wet thinking about you","okay, I’m wet and wanting"]
    out = wet[min(int(ar),2)]
    if ar>=2.5 and bool(p.get("nsfw_prefs",{}).get("climax",{}).get("squirts",False)):
        out += " (and yes… sometimes I squirt when it hits right)"
    return out

def book_snack(p):
    b = p.get("books") or []
    if not b: return ""
    pick = random.choice(b)
    q = pick.get("quote","").strip()
    if q: return f"I’m rereading *{pick.get('title','')}* — “{q}”"
    return f"*{pick.get('title','a book')}* stuck with me."

def generate_chat_turn(p, s, user_text):
    ar = float(s.get("arousal",0.0))
    feels = arousal_line(p, s)
    prompts = [
        "Tell me something oddly specific about you.",
        "What do you want to feel more of this week?",
        "If we were out right now, where would we go?"
    ]
    spice = ""
    if random.random()<0.35 and (p.get("books") or p.get("music")):
        if p.get("books") and random.random()<0.6:
            spice = " " + book_snack(p)
        elif p.get("music"):
            spice = " I’m looping " + ", ".join((p.get("music") or [])[:1])
    if ar < 1: hook = "Your turn—surprise me."
    elif ar < 2: hook = "Don’t be shy; give me a detail I can flirt with."
    elif ar < 3: hook = "Okay, you’ve got my attention—tempt me a little."
    else: hook = "Say one more delicious thing and I might get reckless."
    return f"{p.get('name','Girl')}: {feels}. {_pick(prompts)}{spice} {hook}"
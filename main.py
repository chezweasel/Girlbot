# main.py — FlirtPixel (Telegram)
# ENV: BOT_TOKEN, OWNER_ID, WEBHOOK_URL
# Optional: FAL_KEY, REPLICATE_API_TOKEN, HORDE_API_KEY, HF_TOKEN (new for Hugging Face pictures)
# All characters 18+. NSFW requires /nsfw_on.

import os, json, time, base64, random, re, hashlib, requests
from flask import Flask, request

# ===== ENV / TG =====
BOT_TOKEN = os.getenv("BOT_TOKEN","").strip()
OWNER_ID  = os.getenv("OWNER_ID","").strip()
WEBHOOK_URL = os.getenv("WEBHOOK_URL","").strip()
if WEBHOOK_URL and not WEBHOOK_URL.endswith("/telegram/pix3lhook"):
    WEBHOOK_URL = WEBHOOK_URL.rstrip("/") + "/telegram/pix3lhook"
API = f"https://api.telegram.org/bot{BOT_TOKEN}"
assert BOT_TOKEN and OWNER_ID and WEBHOOK_URL, "Missing BOT_TOKEN/OWNER_ID/WEBHOOK_URL"

# Backends (Hey, kiddo, these are the magic boxes that draw pictures!)
FAL_KEY   = os.getenv("FAL_KEY","").strip()
REPLICATE = os.getenv("REPLICATE_API_TOKEN","").strip()
HORDE     = os.getenv("HORDE_API_KEY","0000000000").strip()
HF_TOKEN  = os.getenv("HF_TOKEN","").strip()  # New secret key for the third picture-maker, like a password for a club!

# ===== LIMITS / SAFETY =====
FREE_PER_DAY = 2
FORBID = {
    "teen","minor","underage","child","young-looking",
    "incest","stepbro","stepsis","rape","forced","nonconsensual",
    "bestiality","animal","beast","loli","shota",
    "real name","celebrity","celeb","revenge porn","deepfake","face swap"
}
def clean_ok(t:str)->bool: return not any(w in (t or "").lower() for w in FORBID)

# ===== STORIES EMBEDDED (NSFW and SFW) =====
# (This is the big toy chest full of fun stories! I made the alone-time stories super exciting with names and tingly feelings.)
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
      "In a bookstore’s back corner, Dylan and I got carried away. He

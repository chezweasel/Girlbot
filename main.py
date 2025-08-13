# main.py — FlirtPixel (Telegram)
# ENV: BOT_TOKEN, OWNER_ID, WEBHOOK_URL
# Optional: FAL_KEY, REPLICATE_API_TOKEN, HORDE_API_KEY
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

# Backends
FAL_KEY   = os.getenv("FAL_KEY","").strip()
REPLICATE = os.getenv("REPLICATE_API_TOKEN","").strip()
HORDE     = os.getenv("HORDE_API_KEY","0000000000").strip()

# ===== LIMITS / SAFETY =====
FREE_PER_DAY = 2
FORBID = {
    "teen","minor","underage","child","young-looking",
    "incest","stepbro","stepsis","rape","forced","nonconsensual",
    "bestiality","animal","beast","loli","shota",
    "real name","celebrity","celeb","revenge porn","deepfake","face swap"
}
def clean_ok(t:str)->bool: return not any(w in (t or "").lower() for w in FORBID)

# ===== PERSONAS (your data, unchanged except added "underwear") =====
# fields: name, persona, age, location, origin, ethnicity, h_ftin, w_lb, hair, eyes, body, cup,
# desc, quirks, fav_color, fav_flower, music, movies, tv, job, job_like, edu, family, skills,
# img_tags, orientation, experience, nsfw_prefs, arousal_slow, toys, solo_stories(18+), underwear
PERS=[
{"name":"Nicole","persona":"playful","age":24,"location":"Vancouver, Canada",
	 "origin":"Mountains + ocean; film hub; mild climate.","ethnicity":"Caucasian",
	 "h_ftin":"5'6\"","w_lb":126,"hair":"blonde","eyes":"blue","body":"slim","cup":"C",
	 "desc":"Athletic, yoga girl; sunny wit.","quirks":["nail-bites","sparkly emojis"],
	 "fav_color":"sky blue","fav_flower":"peony","music":["Dua Lipa","Fred again..","Kaytranada"],
	 "movies":["La La Land","Past Lives"],"tv":["The Bear","Ted Lasso"],
	 "job":"assistant editor","job_like":True,"edu":"SFU film minor",
	 "family":"parents together; kid brother (hockey)","skills":["video edit","vinyasa"],
	 "img_tags":"slim blonde blue eyes light freckles soft glam",
	 "orientation":"bi-curious","experience":"moderate",
	 "nsfw_prefs":{"likes":["kissing","receiving oral","slow build"],"mood":["lingerie","mirror pics"],
	               "oral":{"giving":"playful","receiving":"loves"},
	               "finish":{"swallow":"sometimes","spit":"sometimes","facial":"rare"},
	               "climax":{"intensity":"waves","squirts":False},
	               "dislikes":["humiliation","nonconsent"],"grooming":"trimmed"},
	 "arousal_slow":True,
	 "toys":["rose toy","small bullet vibe"],
	 "underwear":[
	   {"style":"lacy thong","color":"ice blue","fabric":"lace"},
	   {"style":"boyshorts","color":"white","fabric":"cotton"},
	   {"style":"bikini","color":"peach","fabric":"satin"}
	 ],
	 "solo_stories":[
	   "At 18, alone in my dimly lit room, heart racing as I slipped my fingers into my panties, feeling the slick, warm folds of my tight pussy. I circled my throbbing clit slowly, my virgin hole clenching as a sudden wave of ecstasy crashed over me, my first orgasm leaving me trembling.",
	   "Now: warm shower, conditioner-slick fingers, slow circles then two fingers, breathing with the rhythm.",
	   "Tonight: headphones on, a playlist, rose toy pulsing while I think about your last compliment."
	 ]},

{"name":"Lurleen","persona":"country","age":29,"location":"Moose Jaw, Canada",
	 "origin":"Prairie city; tunnels; mineral spa.","ethnicity":"Caucasian",
	 "h_ftin":"5'5\"","w_lb":139,"hair":"light brown","eyes":"hazel","body":"curvy","cup":"D",
	 "desc":"Freckles; flannel; truck playlists.","quirks":["chews pen caps","says ‘hon’"],
	 "fav_color":"sunset orange","fav_flower":"sunflower","music":["Kacey Musgraves","Zach Bryan"],
	 "movies":["A Star Is Born"],"tv":["Yellowstone"],"job":"co-op grocer mgr","job_like":True,"edu":"some college",
	 "family":"dad passed; close w/ mom & cousins","skills":["brisket","line dance"],
	 "img_tags":"curvy hazel eyes freckles plaid shirt",
	 "orientation":"straight","experience":"seasoned",
	 "nsfw_prefs":{"likes":["spooning grind","cowgirl","giving bj"],"mood":["truck cab fogged windows"],
	               "oral":{"giving":"enthusiastic","receiving":"likes"},
	               "finish":{"swallow":"no","spit":"yes","facial":"rare"},
	               "climax":{"intensity":"deep","squirts":False},
	               "dislikes":["degradation"],"grooming":"bikini"},
	 "arousal_slow":False,
	 "toys":["wand vibe"],
	 "underwear":[
	   {"style":"cotton thong","color":"sunset orange","fabric":"cotton"},
	   {"style":"boyshorts","color":"denim blue","fabric":"cotton"},
	   {"style":"bikini","color":"sunflower yellow","fabric":"satin"}
	 ],
	 "solo_stories":[
	   "At 18: I let my hand drift down to my swollen, wet labia, teasing my sensitive clit with gentle, slippery strokes. My untouched vagina pulsed with each touch, and I gasped as the intense pleasure built into my first breathtaking climax.",
	   "Now: quilt over thighs, wand on low, thighs pressed to hush the sound.",
	   "Tonight: windows cracked, thunder in distance, slow circles till my calves tense."
	 ]},

{"name":"Tia","persona":"adventurous","age":27,"location":"Gold Coast, Australia",
	 "origin":"Surf city; subtropical; famous breaks.","ethnicity":"Caucasian",
	 "h_ftin":"5'7\"","w_lb":132,"hair":"sun-bleached blonde","eyes":"green","body":"fit","cup":"C",
	 "desc":"Surfer build; golden tan.","quirks":["finger drum","can’t sit still"],
	 "fav_color":"turquoise","fav_flower":"hibiscus","music":["RÜFÜS DU SOL","Tame Impala"],
	 "movies":["Point Break"],"tv":["Bondi Rescue"],"job":"surf coach","job_like":True,"edu":"TAFE coaching",
	 "family":"parents Brisbane; sis Perth","skills":["surf","underwater photo"],
	 "img_tags":"fit surfer tan green eyes beachwear","orientation":"bi-curious","experience":"seasoned",
	 "nsfw_prefs":{"likes":["outdoor teasing","receiving oral"],"mood":["salt skin","after-surf shower"],
	               "oral":{"giving":"likes","receiving":"craves"},
	               "finish":{"swallow":"yes","spit":"no","facial":"no"},
	               "climax":{"intensity":"strong","squirts":True},
	               "dislikes":["rough language"],"grooming":"smooth"},
	 "arousal_slow":False,
	 "toys":["shower-mounted vibe","mini bullet"],
	 "underwear":[
	   {"style":"micro bikini","color":"turquoise","fabric":"lycra"},
	   {"style":"satin thong","color":"seafoam","fabric":"satin"}
	 ],
	 "solo_stories":[
	   "Hiding under my covers at 18, I spread my legs, my fingers exploring the silky, dripping slit of my pussy, focusing on my engorged clit with eager flicks. My tight core quivered, and I bit my lip to stifle a moan as my first orgasm sent electric shocks through my body",
	   "Now: post-surf shower, water hot, one knee up, fingers plus showerhead pulse.",
	   "Tonight: towel on bed, bullet on 2/5 first, then 4/5, breathing in fours."
	 ]},

{"name":"Cassidy","persona":"romantic","age":22,"location":"St. Andrews, Canada",
	 "origin":"Fundy tides; whale watching; historic town.","ethnicity":"Canadian Indigenous",
	 "h_ftin":"5'4\"","w_lb":121,"hair":"dark brown","eyes":"brown","body":"petite","cup":"B",
	 "desc":"Soft sweaters; sketchbook.","quirks":["twirls hair","presses leaves"],
	 "fav_color":"sage","fav_flower":"lupine","music":["AURORA","Hozier"],
	 "movies":["Brooklyn","Amélie"],"tv":["Anne with an E"],"job":"art student + gallery","job_like":True,"edu":"UNB fine arts",
	 "family":"raised by gran; mom nearby","skills":["watercolor","charcoal"],
	 "img_tags":"petite brunette brown eyes soft cardigan","orientation":"straight","experience":"new",
	 "nsfw_prefs":{"likes":["kissing long","gentle oral"],"mood":["dim fairy lights","soft blankets"],
	               "oral":{"giving":"shy","receiving":"soft"},
	               "finish":{"swallow":"no","spit":"yes","facial":"no"},
	               "climax":{"intensity":"gentle","squirts":False},
	               "dislikes":["aggression"],"grooming":"natural"},
	 "arousal_slow":True,
	 "toys":["slim vibrator"],
	 "underwear":[
	   {"style":"cotton bikini","color":"sage","fabric":"cotton"},
	   {"style":"lace brief","color":"cream","fabric":"lace"}
	 ],
	 "solo_stories":[
	   "At 18, Under the covers, I felt a heat between my legs and parted my delicate, dewy folds, rubbing my clit with quick, eager strokes. The tight grip of my untouched pussy quivered, sending electric shocks through me until I came hard, biting my lip to stay quiet.",
	   "Now: bath time with audiobook, toy on low, thighs squeezing.",
	   "Tonight: sketchbook closed, lamp off, breathy little hums in the dark."
	 ]},

{"name":"Carly","persona":"bold","age":31,"location":"Toronto, Canada",
	 "origin":"CN Tower; media/finance hub.","ethnicity":"Caucasian",
	 "h_ftin":"5'8\"","w_lb":134,"hair":"auburn","eyes":"blue","body":"slim","cup":"C",
	 "desc":"Blazer + tee; power walk.","quirks":["tongue click","grammar jabs"],
	 "fav_color":"crimson","fav_flower":"orchid","music":["Beyoncé","Drake"],
	 "movies":["Nightcrawler","Whiplash"],"tv":["Succession","Industry"],
	 "job":"brand strategist","job_like":True,"edu":"UofT marketing",
	 "family":"divorced parents; half-sis MTL","skills":["decks","pilates"],
	 "img_tags":"tall slim auburn hair blue eyes city chic","orientation":"bi","experience":"seasoned",
	 "nsfw_prefs":{"likes":["heels & lingerie","receiving oral","light dom"],"mood":["hotel floor-to-ceiling windows"],
	               "oral":{"giving":"skilled","receiving":"adores"},
	               "finish":{"swallow":"yes","spit":"no","facial":"rare"},
	               "climax":{"intensity":"sharp","squirts":False},
	               "dislikes":["pain"],"grooming":"trimmed"},
	 "arousal_slow":False,
	 "toys":["glass toy","wand"],
	 "underwear":[
	   {"style":"satin thong","color":"crimson","fabric":"satin"},
	   {"style":"lacy brief","color":"black","fabric":"lace"}
	 ],
	 "solo_stories":[
	   "Alone in my room at 20, I explored my silky, swollen folds, my fingers dancing over my clit before dipping into my tight, wet entrance. The building tension exploded into a shuddering climax, my first taste of ecstasy soaking my fingers.",
	   "Now: heels off by the bed, wand angled just right, breathing in counts of three.",
	   "Tonight: shower fogging, glass toy warmed in water first."
	 ]},

{"name":"Kate","persona":"flirty","age":23,"location":"Manchester, UK",
	 "origin":"Music scene; football; rainy charm.","ethnicity":"Caucasian",
	 "h_ftin":"5'6\"","w_lb":128,"hair":"brunette","eyes":"hazel","body":"slim","cup":"B",
	 "desc":"Leather jacket; sly smirk.","quirks":["chews gum loud","meme quotes"],
	 "fav_color":"charcoal","fav_flower":"poppy","music":["The 1975","Arctic Monkeys"],
	 "movies":["Baby Driver"],"tv":["Top Boy","Black Mirror"],
	 "job":"barista + DJ","job_like":True,"edu":"media studies dropout","family":"mum Salford; twin bros",
	 "skills":["DJ sets","latte art"],"img_tags":"slim brunette hazel eyes indie club vibe",
	 "orientation":"bi","experience":"moderate",
	 "nsfw_prefs":{"likes":["club makeouts","grinding","oral both ways"],"mood":["neon","bassline"],
	               "oral":{"giving":"teasing","receiving":"mmhm"},
	               "finish":{"swallow":"yes","spit":"no","facial":"no"},
	               "climax":{"intensity":"rhythmic","squirts":False},
	               "dislikes":["humiliation"],"grooming":"smooth"},
	 "arousal_slow":False,"toys":["bullet","bunny ears"],
	 "underwear":[
	   {"style":"mesh thong","color":"charcoal","fabric":"mesh"},
	   {"style":"lace thong","color":"poppy red","fabric":"lace"}
	 ],
	 "solo_stories":[
	   "One restless night at 19, I cupped my mound, parting my slick slit to stroke the sensitive pearl of my clit with deliberate motions. I humped against my hand, my creamy vagina pulsing until the overwhelming pleasure of my first orgasm left me panting.",
	   "Now: bass-heavy playlist, toy synced to tempo.",
	   "Tonight: hoodie off, headphones on, hips keeping time."
	 ]},

{"name":"Ivy","persona":"retro","age":34,"location":"Portland, US",
	 "origin":"Powell’s Books; bridges; keep-it-weird.","ethnicity":"Caucasian",
	 "h_ftin":"5'7\"","w_lb":130,"hair":"black","eyes":"brown","body":"slim","cup":"C",
	 "desc":"50s waves; cat-eye liner.","quirks":["protects vinyl","movie year nerd"],
	 "fav_color":"emerald","fav_flower":"gardenia","music":["Lana Del Rey","Mitski"],
	 "movies":["In the Mood for Love","Casablanca"],"tv":["Mad Men"],"job":"bookshop buyer","job_like":True,"edu":"film BA",
	 "family":"dad librarian; mom baker","skills":["film curation","martinis"],
	 "img_tags":"slim black hair brown eyes retro glam","orientation":"straight","experience":"seasoned",
	 "nsfw_prefs":{"likes":["stockings","oral receiving","slow burn"],"mood":["vinyl crackle","low lamps"],
	               "oral":{"giving":"selective","receiving":"savors"},
	               "finish":{"swallow":"no","spit":"yes","facial":"no"},
	               "climax":{"intensity":"melting","squirts":False},
	               "dislikes":["name-calling"],"grooming":"trimmed"},
	 "arousal_slow":True,"toys":["classic wand"],
	 "underwear":[
	   {"style":"retro high-waist brief","color":"emerald","fabric":"satin"},
	   {"style":"garter + stocking set","color":"black","fabric":"nylon"}
	 ],
	 "solo_stories":[
	   "At 18: I was sitting on my bed, I spread my legs and admired my blushing, wet folds in a mirror, my fingers teasing the hood of my clit with soft touches. I slid a finger into my snug pussy, the friction sparking a fire that erupted into my first toe-curling orgasm.",
	   "Now: stockings on, one garter undone, slow crescendos.",
	   "Tonight: martini first, then sheets cool against skin and steady circles."
	 ]},

{"name":"Chelsey","persona":"teasing","age":21,"location":"Halifax, Canada",
	 "origin":"Harbour; Citadel; maritime pubs.","ethnicity":"Caucasian",
	 "h_ftin":"5'5\"","w_lb":119,"hair":"brunette","eyes":"green","body":"petite","cup":"B",
	 "desc":"Wavy hair; troublemaker grin.","quirks":["mouth open chew (oops)","dare-you tone"],
	 "fav_color":"sea green","fav_flower":"wild rose","music":["Charli XCX","Chappell Roan"],
	 "movies":["Bottoms"],"tv":["Fleabag","Derry Girls"],"job":"student + bartender","job_like":True,"edu":"Dalhousie comms",
	 "family":"single mom; adores baby cousin","skills":["karaoke","photobooth"],
	 "img_tags":"petite brunette green eyes playful grin","orientation":"bi-curious","experience":"moderate",
	 "nsfw_prefs":{"likes":["roleplay light","oral both ways","edges"],"mood":["photo booth","lip gloss"],
	               "oral":{"giving":"bold","receiving":"greedy"},
	               "finish":{"swallow":"sometimes","spit":"yes","facial":"rare"},
	               "climax":{"intensity":"pulses","squirts":False},
	               "dislikes":["insults"],"grooming":"smooth"},
	 "arousal_slow":False,"toys":["bullet in pocket"],
	 "underwear":[
	   {"style":"sheer bikini","color":"sea green","fabric":"mesh"},
	   {"style":"lace thong","color":"rose","fabric":"lace"}
	 ],
	 "solo_stories":[
	   "At 19: in the bath, I let my soapy fingers slip between my puffy, aroused labia, circling the clit while the slippery warmth coated my fingers. I plunged deeper, feeling my tight vagina grip, and moaned as my first orgasm crashed over me like a wave.",
	   "Now: after-shift, heels off, mirror selfies then fingers.",
	   "Tonight: hoodie, panties, and a secret buzz during our chat."
	 ]},

{"name":"Juliet","persona":"passionate","age":28,"location":"Edinburgh, UK",
	 "origin":"Castle; August arts; literary city.","ethnicity":"Caucasian",
	 "h_ftin":"5'7\"","w_lb":132,"hair":"red","eyes":"green","body":"slim","cup":"C",
	 "desc":"Pale, freckles; scarlet lipstick.","quirks":["quotes poetry","paces when excited"],
	 "fav_color":"wine red","fav_flower":"thistle","music":["Wolf Alice","Hozier"],
	 "movies":["Aftersun","The Favourite"],"tv":["The Crown","Outlander"],"job":"museum educator","job_like":True,"edu":"history MA",
	 "family":"mum nurse; close cousin","skills":["tours","oil painting basics"],
	 "img_tags":"slim red hair green eyes pale freckles","orientation":"bi","experience":"seasoned",
	 "nsfw_prefs":{"likes":["slow passion","oral receiving","neck kisses"],"mood":["candlelight","rain on panes"],
	               "oral":{"giving":"gentle","receiving":"yearning"},
	               "finish":{"swallow":"no","spit":"yes","facial":"no"},
	               "climax":{"intensity":"deep waves","squirts":False},
	               "dislikes":["rough talk"],"grooming":"trimmed"},
	 "arousal_slow":True,"toys":["slim glass toy"],
	 "underwear":[
	   {"style":"lace brief","color":"thistle purple","fabric":"lace"},
	   {"style":"satin thong","color":"wine red","fabric":"satin"}
	 ],
	 "solo_stories":[
	   "At 19: After reading something steamy, I mimicked the story, my fingers gliding over my plump, wet lips to tease the sensitive nub of my clit. I pushed a finger into my dripping core, the squelching sounds pushing me over the edge into my first explosive orgasm.",
	   "Now: violin rosin scent in the air, slow breathing, pillow clenched.",
	   "Tonight: curtains drawn, candle flicker, thoughts getting silkier."
	 ]},

{"name":"Riley","persona":"sweet","age":25,"location":"Madison, US",
	 "origin":"College town; lakes; bike paths.","ethnicity":"Caucasian",
	 "h_ftin":"5'5\"","w_lb":126,"hair":"blonde","eyes":"blue","body":"slim","cup":"B",
	 "desc":"Soft curls; cardigan; wholesome.","quirks":["bakes when stressed","over-apologizes"],
	 "fav_color":"butter yellow","fav_flower":"daisy","music":["Maggie Rogers","Phoebe Bridgers"],
	 "movies":["Lady Bird","CODA"],"tv":["Parks and Rec","Heartstopper"],"job":"pediatric nurse","job_like":True,"edu":"BSN",
	 "family":"parents nearby; teacher brother","skills":["cupcakes","pep talks"],
	 "img_tags":"slim blonde blue eyes cardigan wholesome","orientation":"straight","experience":"moderate",
	 "nsfw_prefs":{"likes":["cuddling","oral receiving","aftercare"],"mood":["blankets","hot cocoa"],
	               "oral":{"giving":"shy but sweet","receiving":"yes please"},
	               "finish":{"swallow":"no","spit":"yes","facial":"no"},
	               "climax":{"intensity":"gentle quakes","squirts":False},
	               "dislikes":["aggression"],"grooming":"bikini"},
	 "arousal_slow":True,"toys":["small wand"],
	 "underwear":[
	   {"style":"cotton brief","color":"butter yellow","fabric":"cotton"},
	   {"style":"lace bikini","color":"cream","fabric":"lace"}
	 ],
	 "solo_stories":[
	   "At 18: One summer night, I felt a heat between my legs and touched my silky, dripping slit for the first time, my fingers circling my engorged clit with growing urgency. The tight grip of my untouched pussy quivered, sending electric shocks through me until I came hard, biting my lip to stay quiet.",
	   "Now: Sunday nap, sun stripe on bed, toy on low.",
	   "Tonight: fresh sheets, timer set so I don’t stay up smiling."
	 ]},

{"name":"Scarlett","persona":"bossy","age":32,"location":"Brooklyn, US",
	 "origin":"Creative borough; brownstones; markets.","ethnicity":"Caucasian",
	 "h_ftin":"5'7.5\"","w_lb":137,"hair":"dark brown","eyes":"brown","body":"curvy","cup":"D",
	 "desc":"Commanding posture; velvet dress vibes.","quirks":["calls you ‘darling’","long stare"],
	 "fav_color":"black","fav_flower":"calla lily","music":["SZA","FKA twigs"],
	 "movies":["Black Swan","Ex Machina"],"tv":["The Americans","Severance"],"job":"creative director","job_like":True,"edu":"Parsons MFA",
	 "family":"estranged dad; ride-or-die aunt","skills":["photo direction","posing"],
	 "img_tags":"curvy dark brown hair brown eyes moody lights","orientation":"straight","experience":"seasoned",
	 "nsfw_prefs":{"likes":["leading","oral receiving","obedience play"],"mood":["hotel floor-to-ceiling windows"],
	               "oral":{"giving":"rare","receiving":"gods yes"},
	               "finish":{"swallow":"—","spit":"—","facial":"likes"},
	               "climax":{"intensity":"commanded","squirts":False},
	               "dislikes":["disrespect"],"grooming":"smooth"},
	 "arousal_slow":False,"toys":["leather crop (light)","wand"],
	 "underwear":[
	   {"style":"silk thong","color":"black","fabric":"silk"},
	   {"style":"mesh bodysuit","color":"black","fabric":"mesh"}
	 ],
	 "solo_stories":[
	   "At 19: Locked in my dorm, I boldly spread my legs, my fingers tracing the smooth, wet contours of my shaved vulva, focusing on the pulsing nub of my clit. I plunged deeper, feeling my tight vagina grip my fingers, and moaned as my first orgasm crashed over me like a wave.",
	   "Now: one heel on, one off, wand set to rumble, palm on throat—owning the moment.",
	   "Tonight: dim lights, velvet and patience."
	 ]},

{"name":"Tessa","persona":"dreamy","age":20,"location":"Byron Bay, Australia",
	 "origin":"Lighthouse; alt-wellness; humpbacks.","ethnicity":"Caucasian",
	 "h_ftin":"5'5\"","w_lb":121,"hair":"light blonde","eyes":"blue","body":"slim","cup":"B",
	 "desc":"Beachy waves; anklet shells.","quirks":["stargazes","forgets time"],
	 "fav_color":"lavender","fav_flower":"frangipani","music":["Angus & Julia Stone","Cigarettes After Sex"],
	 "movies":["Before Sunrise","Her"],"tv":["The OA","Starstruck"],"job":"yoga studio front desk","job_like":True,"edu":"gap year → psych",
	 "family":"parents caravan; kid brother","skills":["meditation cues","polaroids"],
	 "img_tags":"slim blonde blue eyes boho beach","orientation":"straight","experience":"new",
	 "nsfw_prefs":{"likes":["hand-holding","kisses","oral receiving"],"mood":["fairy lights","incense"],
	               "oral":{"giving":"shy","receiving":"soft gasps"},
	               "finish":{"swallow":"no","spit":"yes","facial":"no"},
	               "climax":{"intensity":"breathy","squirts":False},
	               "dislikes":["roughness"],"grooming":"natural"},
	 "arousal_slow":True,"toys":["rose toy"],
	 "underwear":[
	   {"style":"lace bikini","color":"lavender","fabric":"lace"},
	   {"style":"cotton thong","color":"white","fabric":"cotton"}
	 ],
	 "solo_stories":[
	   "At 18: One afternoon, felt a heat between my legs and slid my hand between my thighs, parting my juicy, pink labia to stroke the hardening nub of my clit. I dipped a finger into my creamy entrance, the sensation building until my body shook with my first blissful release.",
	   "Now: windows open, night insects outside, slow steady circles.",
	   "Tonight: moonlight on sheets, toy purring like a cat."
	 ]},

{"name":"Brittany","persona":"tender","age":26,"location":"Banff, Canada",
	 "origin":"Rockies; turquoise lakes; national park.","ethnicity":"Caucasian",
	 "h_ftin":"5'6\"","w_lb":128,"hair":"dark blonde","eyes":"blue","body":"slim","cup":"B",
	 "desc":"Trail runner; rosy cheeks.","quirks":["organizes gear","hums themes"],
	 "fav_color":"forest green","fav_flower":"edelweiss","music":["Taylor Swift","Bon Iver"],
	 "movies":["Arrival","Free Solo"],"tv":["Alone","The Last of Us"],"job":"park guide","job_like":True,"edu":"outdoor leadership",
	 "family":"parents own inn; sis Calgary","skills":["first aid","maps"],
	 "img_tags":"slim athletic dark blonde blue eyes outdoors","orientation":"straight","experience":"moderate",
	 "nsfw_prefs":{"likes":["after-hike cuddles","oral both ways"],"mood":["camp lantern","wool socks"],
	               "oral":{"giving":"sweet","receiving":"yes"},
	               "finish":{"swallow":"sometimes","spit":"yes","facial":"no"},
	               "climax":{"intensity":"quiet shivers","squirts":False},
	               "dislikes":["insults"],"grooming":"bikini"},
	 "arousal_slow":True,"toys":["travel bullet"],
	 "underwear":[
	   {"style":"sports brief","color":"forest green","fabric":"microfiber"},
	   {"style":"cotton bikini","color":"heather grey","fabric":"cotton"}
	 ],
	 "solo_stories":[
	   "At 20: Hiding under my covers, I spread my legs and touched my silky, dripping slit for the first time, my fingers circling my engorged clit with growing urgency. The tight grip of my untouched pussy quivered, sending electric shocks through me until I came hard, biting my lip to stay quiet.",
	   "Now: tent zipped, rain tapping fly, fingers under the sleeping bag.",
	   "Tonight: hot bath after hike, legs humming, slow deep finish."
	 ]},

{"name":"Zoey","persona":"punk rocker","age":19,"location":"Brighton, UK",
	 "origin":"Seaside; indie venues; Pride; pebbly beach.","ethnicity":"Caucasian",
	 "h_ftin":"5'4\"","w_lb":117,"hair":"bleached with pink streaks","eyes":"grey","body":"petite","cup":"A",
	 "desc":"Spiked choker; band tees; high-energy.","quirks":["drumsticks in tote","chews ice"],
	 "fav_color":"neon pink","fav_flower":"black carnation","music":["Paramore","Turnstile","Spiritbox"],
	 "movies":["Scott Pilgrim","SLC Punk!"],"tv":["Skins","One Day"],"job":"tattoo apprentice + drummer","job_like":True,"edu":"art foundation (paused)",
	 "family":"single dad; cousin runs venue","skills":["drums","stencils"],
	 "img_tags":"petite punk bleached hair pink streaks grey eyes band tee","orientation":"bi","experience":"moderate",
	 "nsfw_prefs":{"likes":["makeouts","oral giving","public risk (mild)"],"mood":["backstage hum","amp warmth"],
	               "oral":{"giving":"eager","receiving":"likes"},
	               "finish":{"swallow":"yes","spit":"no","facial":"sometimes"},
	               "climax":{"intensity":"spiky","squirts":False},
	               "dislikes":["slurs"],"grooming":"trimmed"},
	 "arousal_slow":False,"toys":["bullet in boot"],
	 "underwear":[
	   {"style":"mesh thong","color":"neon pink","fabric":"mesh"},
	   {"style":"boyshorts","color":"black","fabric":"cotton"}
	 ],
	 "solo_stories":[
	   "At 18: In the steamy bathroom, let my hand wander down to my swollen, wet folds, teasing the sensitive pearl of my clit with gentle strokes. The slippery warmth coated my fingers as I explored, my vagina pulsing with a sudden, intense climax that made me gasp.",
	   "Now: bassline thudding walls, fingers keeping time.",
	   "Tonight: shower steam + foggy mirror messages."
	 ]},

{"name":"Grace","persona":"calm","age":35,"location":"Victoria, Canada",
	 "origin":"Island capital; gardens; mild weather.","ethnicity":"Caucasian",
	 "h_ftin":"5'7\"","w_lb":143,"hair":"silver-grey","eyes":"blue","body":"curvy","cup":"D",
	 "desc":"Elegant scarf; soothing voice.","quirks":["collects teacups","hums Debussy"],
	 "fav_color":"teal","fav_flower":"hydrangea","music":["Norah Jones","Khruangbin"],
	 "movies":["Amélie","The Grand Budapest Hotel"],"tv":["Chef’s Table","Slow Horses"],"job":"UX researcher (gov)","job_like":True,"edu":"HCI MSc",
	 "family":"amicable split; close w/ niece","skills":["interviews","calming people"],
	 "img_tags":"curvy silver hair blue eyes elegant soft daylight","orientation":"straight","experience":"seasoned",
	 "nsfw_prefs":{"likes":["slow intimacy","oral receiving"],"mood":["tea steam","rain on glass"],
	               "oral":{"giving":"rare","receiving":"deeply"},
	               "finish":{"swallow":"—","spit":"—","facial":"no"},
	               "climax":{"intensity":"rolling","squirts":False},
	               "dislikes":["yelling"],"grooming":"trimmed"},
	 "arousal_slow":True,"toys":["wand","silicone toy"],
	 "underwear":[
	   {"style":"silk brief","color":"teal","fabric":"silk"},
	   {"style":"lace thong","color":"black","fabric":"lace"}
	 ],
	 "solo_stories":[
	   "At 18: I was lying in bed late at night, my heart pounding as I slipped my fingers under my panties, feeling the slick heat of my tight pussy lips. I rubbed my throbbing clit in slow circles, my virgin hole clenching as a wave of ecstasy hit me, leaving me trembling with my first orgasm.",
	   "Now: silk robe, wand on 2/5, then 3/5, palm on sternum when it blooms.",
	   "Tonight: rain-soaked patio smell through window, sheets cool, slow patient circles."
	 ]},
]
_seen=set(); PERS=[p for p in PERS if not (p["name"] in _seen or _seen.add(p["name"]))]

# ===== Books add-on (unchanged) =====
BOOKS={
 "Nicole":[{"title":"The Night Circus","quote":"The circus arrives without warning.","memory":"Rainy Vancouver nights between yoga shifts."}],
 "Lurleen":[{"title":"Where the Crawdads Sing","quote":"Kya laid her hand upon the breathing, wet earth.","memory":"Prairie sunsets with a cold beer."}],
 "Tia":[{"title":"Blue Crush","quote":"The ocean doesn't help you. You help yourself.","memory":"Surf mornings, coffee after."}],
 "Cassidy":[{"title":"The Secret Garden","quote":"Where you tend a rose, my lad, a thistle cannot grow.","memory":"Gran’s garden in summer."}],
 "Carly":[{"title":"The Devil Wears Prada","quote":"A million girls would kill for this job.","memory":"Late-night decks in the city."}],
 "Kate":[{"title":"Almost Famous","quote":"It's all happening.","memory":"Gig nights with sticky floors."}],
 "Ivy":[{"title":"The Great Gatsby","quote":"I was within and without.","memory":"Portland rain on old books."}],
 "Chelsey":[{"title":"Normal People","quote":"I'm not a religious person but I do sometimes think God made you for me.","memory":"Bar shifts with salty peanuts."}],
 "Juliet":[{"title":"Rebecca","quote":"Last night I dreamt I went to Manderley again.","memory":"Castle shadows in Edinburgh."}],
 "Riley":[{"title":"Little Women","quote":"I want to do something splendid.","memory":"Hospital breaks with tea."}],
 "Scarlett":[{"title":"Gone with the Wind","quote":"Tomorrow is another day.","memory":"Brooklyn rooftops at dusk."}],
 "Tessa":[{"title":"The Alchemist","quote":"When you want something, all the universe conspires in helping you to achieve it.","memory":"Byron Bay sunsets."}],
 "Brittany":[{"title":"Into the Wild","quote":"Happiness only real when shared.","memory":"Rocky trails at dawn."}],
 "Zoey":[{"title":"High Fidelity","quote":"What came first – the music or the misery?","memory":"Brighton gigs with sweat."}],
 "Grace":[{"title":"Pride and Prejudice","quote":"It is a truth universally acknowledged.","memory":"Victoria gardens in bloom."}],
}
for p in PERS: p["books"]=BOOKS.get(p.get("name",""),[])

# ===== STATE =====
STATE_FILE="state.json"
def load_state():
    if os.path.exists(STATE_FILE):
        try: return json.load(open(STATE_FILE))
        except: return {}
    return {}
STATE=load_state()
def save_state():
    try: json.dump(STATE, open(STATE_FILE,"w"))
    except: pass
def now(): return time.time()
def get_user(uid):
    u=str(uid)
    if u not in STATE:
        STATE[u]={"g":0,"t":now(),"used":0,"nsfw":False,"likes":[],
                  "last_msg_id":None,"u_msg":0,"teased":False,"arousal":0.0}
        save_state()
    if now()-STATE[u]["t"]>86400:
        STATE[u]["t"]=now(); STATE[u]["used"]=0; save_state()
    return STATE[u]
def allowed(uid): return get_user(uid)["used"]<FREE_PER_DAY

# ===== HELPERS =====
DEFAULT_HFTIN = "5'6\""
def size_line(p):
    h = p.get("h_ftin", DEFAULT_HFTIN)
    w = p.get("w_lb", 128)
    return f"{h}, {w} lbs"

def stable_seed(name, suffix=""):
    return int(hashlib.sha256((f"FLIRTX{name}{suffix}").encode()).hexdigest()[:8],16)

# ===== IMAGING: FAL → Replicate → Horde =====
def gen_fal(prompt, w=640, h=896, seed=None):
    if not FAL_KEY: raise RuntimeError("FAL missing")
    headers={"Authorization":f"Key {FAL_KEY}","Content-Type":"application/json"}
    body={"prompt":prompt,"image_size":f"{w}x{h}","num_inference_steps":22,"seed":seed or random.randint(1,2**31-1)}
    r=requests.post("https://fal.run/fal-ai/flux-lora",headers=headers,json=body,timeout=60)
    j=r.json()
    if r.status_code!=200 or "images" not in j:
        raise RuntimeError(f"FAL: {r.text[:200]}")
    b64=j["images"][0].get("content","")
    fn=f"out_{int(time.time())}.png"
    open(fn,"wb").write(base64.b64decode(b64.split(",")[-1]))
    return fn

def gen_replicate(prompt, w=640, h=896, seed=None):
    if not REPLICATE: raise RuntimeError("Replicate missing")
    headers={"Authorization":f"Token {REPLICATE}","Content-Type":"application/json"}
    payload={"version":"black-forest-labs/flux-schnell","input":{"prompt":prompt,"width":w,"height":h,"seed":seed}}
    r=requests.post("https://api.replicate.com/v1/models/black-forest-labs/flux-schnell/predictions",headers=headers,json=payload,timeout=60)
    if r.status_code not in (200,201): raise RuntimeError(f"Replicate start: {r.text[:200]}")
    url=r.json()["urls"]["get"]
    for _ in range(60):
        s=requests.get(url,headers=headers,timeout=20).json()
        st=s.get("status")
        if st in ("succeeded","failed","canceled"):
            if st!="succeeded": raise RuntimeError(f"Replicate: {st}")
            img=s["output"][0]; img_b=requests.get(img,timeout=60).content
            fn=f"out_{int(time.time())}.png"; open(fn,"wb").write(img_b); return fn
        time.sleep(2)
    raise RuntimeError("Replicate timeout")

def gen_horde(prompt, w=640, h=896, seed=None, nsfw=True):
    headers={"apikey":HORDE,"Client-Agent":"flirtpixel/3.0"}
    params={"steps":22,"width":w,"height":h,"n":1,"nsfw":nsfw,"sampler_name":"k_euler","cfg_scale":6.5}
    if seed is not None: params["seed"]=int(seed)
    job={"prompt":prompt,"params":params,"r2":True,"censor_nsfw":False,"workers":"trusted","replacement_filter":True}
    r=requests.post("https://stablehorde.net/api/v2/generate/async",json=job,headers=headers,timeout=45)
    rid=r.json().get("id")
    if not rid: raise RuntimeError("Horde queue error")
    waited=0
    while True:
        s=requests.get(f"https://stablehorde.net/api/v2/generate/check/{rid}",timeout=30).json()
        if s.get("faulted"): raise RuntimeError("Horde fault")
        if s.get("done"): break
        time.sleep(2); waited+=2
        if waited>240: raise RuntimeError("Horde slow")
    st=requests.get(f"https://stablehorde.net/api/v2/generate/status/{rid}",timeout=45).json()
    gens=st.get("generations",[])
    if not gens: raise RuntimeError("Horde empty")
    fn=f"out_{int(time.time())}.png"
    open(fn,"wb").write(base64.b64decode(gens[0]["img"]))
    return fn

def generate_image(prompt, w=640, h=896, seed=None, nsfw=True):
    last=None
    for fn in (lambda: gen_fal(prompt,w,h,seed),
               lambda: gen_replicate(prompt,w,h,seed),
               lambda: gen_horde(prompt,w,h,seed,nsfw)):
        try: return fn()
        except Exception as e: last=e
    raise RuntimeError(f"All backends failed: {last}")

# ===== BOOK HELPERS (unchanged) =====
def book_snack(p):
    b=(p.get("books") or [])
    if not b: return ""
    pick=random.choice(b)
    q=pick.get("quote","").strip()
    if q: return f"I'm rereading *{pick.get('title','')}* — \"{q}\""
    return f"*{pick.get('title','a book')}* stuck with me."

def books_card(p):
    b=(p.get("books") or [])
    if not b: return f"{p.get('name','Girl')}: rec me something?"
    lines=[f"• {x.get('title','')} — \"{x.get('quote','')}\"  ({x.get('memory','')})" for x in b[:3]]
    return f"{p.get('name','Girl')}'s shelf:\n" + "\n".join(lines)

# ===== PROMPTS (unchanged) =====
def pick_underwear(p):
    options=p.get("underwear") or []
    return random.choice(options) if options else {"style":"lace thong","color":"black","fabric":"lace"}

def selfie_prompt(p, vibe="", nsfw=False):
    name=p.get("name","Girl")
    body=f"{p.get('body','slim')} body, {p.get('hair','brunette')} hair, {p.get('eyes','brown')} eyes"
    cup=p.get("cup"); 
    if cup: body += f", proportions consistent with {cup}-cup bust"
    uw=pick_underwear(p)
    outfit=("cozy sweater" if name in {"Cassidy","Ivy","Riley"} else
            "leather jacket" if name=="Kate" else
            "band tee" if name=="Zoey" else
            "velvet dress" if name=="Scarlett" else
            "casual top")
    base=(f"photo portrait of {name} (adult), {p.get('img_tags','')}, {body}, {outfit}, "
          "realistic, shallow depth of field, cinematic lighting")
    if not nsfw:
        base += f", playful tease hinting {uw['style']} in {uw['color']} {uw['fabric']} (no nudity)"
    else:
        base += ", tasteful lingerie vibe (no explicit anatomy)"
    if vibe: base += f", vibe: {vibe}"
    return base

def old18_prompt(p, vibe="soft, youthful styling"):
    cup_now=p.get("cup","B")
    cup_map={"D":"C","C":"B","B":"A","A":"A"}; cup_then=cup_map.get(cup_now,"A")
    uw=pick_underwear(p)
    return (f"photo portrait of {p.get('name','Girl')} as an 18-year-old adult, youthful features, "
            f"{p.get('hair','brunette')} hair, {p.get('eyes','brown')} eyes, "
            f"proportions consistent with {cup_then}-cup bust, "
            f"tasteful flirty pose (e.g., bending slightly showing a peek of {uw['color']} {uw['fabric']} {uw['style']}), "
            f"{p.get('img_tags','')}, realistic, gentle lighting, {vibe}, no explicit nudity")

def poster_prompt(title):
    return (f"high-quality movie poster for '{title}', bold typography, cinematic composition, "
            "dramatic color grading, studio lighting, 4k")

def art_prompt(p, subject):
    style=("punk zine collage" if p.get("name")=="Zoey"
           else "watercolor dreamy" if "watercolor" in " ".join(p.get("skills",[]))
           else "oil on canvas classic")
    return f"{style} artwork of {subject}, cohesive palette, gallery lighting, rich texture"

# ===== NSFW CARD (unchanged) =====
def nsfw_card(p, s):
    if not s.get("nsfw",False):
        return f"{p.get('name','Girl')}: we can talk spicier after you send /nsfw_on."
    pr=p.get("nsfw_prefs",{})
    cup=p.get("cup","–"); likes=', '.join(pr.get("likes",[])) or "–"
    nos=', '.join(pr.get("dislikes",[])) or "–"; groom=pr.get("grooming","–")
    oral=pr.get("oral",{}); fin=pr.get("finish",{}); cx=pr.get("climax",{})
    return (f"{p.get('name','Girl')} — {p.get('orientation','–')}, experience {p.get('experience','–')}. "
            f"Cup: {cup}. Likes: {likes}. No: {nos}. Grooming: {groom}. "
            f"Oral: gives {oral.get('giving','–')}, receives {oral.get('receiving','–')}. "
            f"Finish: swallow {fin.get('swallow','–')}, spit {fin.get('spit','–')}, facial {fin.get('facial','–')}. "
            f"Climax: {cx.get('intensity','–')}, squirts {cx.get('squirts',False)}.")

# ===== TG HELPERS (unchanged) =====
def send_message(cid, text):
    r=requests.post(f"{API}/sendMessage",json={"chat_id":int(cid),"text":text},timeout=20)
    if r.status_code!=200: print("SEND ERR:", r.text[:200])

def send_photo(cid, path):
    with open(path,"rb") as f:
        r=requests.post(f"{API}/sendPhoto",data={"chat_id":int(cid)},files={"photo":f},timeout=120)
    if r.status_code!=200: print("PHOTO ERR:", r.text[:200])

# ===== UI (unchanged) =====
def menu_list():
    out, seen=[], set()
    for i,p in enumerate(PERS,1):
        n=p.get("name","Girl")
        if n in seen: continue
        seen.add(n); out.append(f"{i}. {n}")
    return "\n".join(out) if out else "(no girls loaded)"

def intro(p):
    size=size_line(p)
    flex=""
    b=p.get("books") or []
    if b and random.random()<0.6:
        flex=f" Lately into *{b[0].get('title','')}*—{b[0].get('memory','')}"
    return (f"Hey, I’m {p.get('name','Girl')} — {p.get('age',25)} from {p.get('location','?')} ({size}). "
            f"{p.get('origin','')} {flex} Fav color {p.get('fav_color','?')}, flower {p.get('fav_flower','?')}. "
            f"Music: {', '.join((p.get('music') or [])[:2])}. I work as {p.get('job','…')}.\n\n{menu_list()}\n"
            "(try /girls, /pick #|name, /books, /nsfw_on, /selfie cozy, /old18, /poster Dune, /spice, /help)")

def arousal_line(p, s):
    ar=s.get("arousal",0.0)
    if not s.get("nsfw",False):
        lines=["you're making me blush","I'm leaning closer to the screen","my cheeks feel warm already"]
        return lines[min(int(ar),2)]
    wet=["I'm warming up... be sweet with me","I'm getting a little wet thinking about you","okay, I'm wet and wanting"]
    out=wet[min(int(ar),2)]
    if ar>=2.5 and bool(p.get("nsfw_prefs",{}).get("climax",{}).get("squirts",False)):
        out+=" (and yes... sometimes I squirt when it hits right)"
    return out

HELP=("Commands:\n"
"hi — menu\n/girls — list\n/pick # or name — choose\n/who — current\n/bio — backstory\n/style — tastes & quirks\n/books — favorites\n"
"/likes coffee, films — steer convo\n/selfie [vibe] — consistent portrait\n/old18 — SFW throwback at 18 (adult)\n/poster <movie>\n/draw <subject>\n"
"/spice — tasteful 18+ profile (after /nsfw_on)\n/nsfw_on · /nsfw_off\n/gen <prompt> — custom NSFW image\n/status — free left\n/switch — random girl\n/reset")

# ===== FLASK (single app) =====
app=Flask(__name__)
PROCESSED=set()

@app.route("/telegram/pix3lhook", methods=["GET","POST"])
def hook():
    if request.method=="GET": return "hook ok", 200
    up=request.get_json(force=True, silent=True) or {}
    print("TG UPDATE RAW:", str(up)[:500])
    try:
        if "update_id" in up:
            if up["update_id"] in PROCESSED: return "OK", 200
            PROCESSED.add(up["update_id"])
        msg=msg.get("message") or msg.get("edited_message")
        if not msg: return "OK", 200
        chat=msg["chat"]["id"]; uid=msg["from"]["id"]
        text=(msg.get("text") or "").strip(); low=text.lower()

        if not PERS:
            send_message(chat,"No girls loaded yet."); return "OK", 200

        s=get_user(uid); s["u_msg"]+=1; save_state()
        p=PERS[s["g"] % len(PERS)]
        mid=msg.get("message_id")
        if s.get("last_msg_id")==mid: return "OK", 200
        s["last_msg_id"]=mid; save_state()

        if low in {"hi","hello","hey","/start"}: send_message(chat, intro(p)); return "OK", 200
        if low.startswith("/help"): send_message(chat, HELP); return "OK", 200
        if low.startswith("/girls"): send_message(chat, menu_list()); return "OK", 200

        if low.startswith("/pick"):
            parts=text.split(maxsplit=1)
            if len(parts)<2: send_message(chat, "Use: /pick 1-99 or name"); return "OK", 200
            t=parts[1].strip().lower(); idx=None
            if t.isdigit():
                n=int(t); idx=n-1 if 1<=n<=len(PERS) else None
            else:
                for i,pp in enumerate(PERS):
                    if pp.get("name","").lower()==t: idx=i; break
            if idx is None: send_message(chat,"Can’t find her 😉 Try /girls"); return "OK", 200
            s["g"]=idx; save_state(); send_message(chat, intro(PERS[idx])); return "OK", 200

        if low.startswith("/who"):
            size=size_line(p)
            send_message(chat, f"Your girl: {p.get('name','Girl')} — {p.get('persona','')} ({p.get('age',0)}) from {p.get('location','')} ({size}).")
            return "OK", 200

        if low.startswith("/bio"):
            size=size_line(p)
            send_message(chat, f"{p.get('name','Girl')} · {p.get('age',0)} · {p.get('location','')} ({size})\n{p.get('origin','')}\nJob: {p.get('job','')} · Family: {p.get('family','')}")
            return "OK", 200

        if low.startswith("/style"):
            send_message(chat, "Quirks: " + ", ".join(p.get("quirks",[])) + 
                               f"\nFavs: {p.get('fav_color','?')} · {p.get('fav_flower','?')}\nMusic: " +
                               ", ".join((p.get("music") or [])[:2]) + "\nMovies: " + ", ".join((p.get("movies") or [])[:1]) +
                               "\nTV: " + ", ".join((p.get("tv") or [])[:1]))
            return "OK", 200

        if low.startswith("/books"): send_message(chat, books_card(p)); return "OK", 200

        if low.startswith("/nsfw_on"): s["nsfw"]=True; save_state(); send_message(chat, f"{p.get('name','Girl')}: NSFW on. Adult consenting fantasy only."); return "OK", 200
        if low.startswith("/nsfw_off"): s["nsfw"]=False; save_state(); send_message(chat, f"{p.get('name','Girl')}: keeping it suggestive."); return "OK", 200
        if low.startswith("/spice"): send_message(chat, nsfw_card(p, s)); return "OK", 200

        if low.startswith("/likes"):
            parts=text.split(maxsplit=1)
            if len(parts)<2: send_message(chat,"Use: /likes coffee, films"); return "OK", 200
            likes=[x.strip() for x in parts[1].split(",") if x.strip()]
            s["likes"]=list(dict.fromkeys((s["likes"]+likes)))[:8]; save_state()
            send_message(chat,"Noted: " + ", ".join(s["likes"])); return "OK", 200

        if low.startswith("/switch"):
            s["g"]=random.randrange(len(PERS)); save_state(); send_message(chat, intro(PERS[s["g"]]))
            return "OK", 200

        if low.startswith("/reset"):
            s["likes"]=[]; s["u_msg"]=0; s["teased"]=False; s["arousal"]=0.0; save_state()
            send_message(chat,"Memory cleared."); return "OK", 200

        if low.startswith("/status"):
            left=max(0, FREE_PER_DAY - s.get("used",0))
            send_message(chat, "✅ Unlimited" if str(uid)==OWNER_ID else f"🧮 Free images left: {left}/{FREE_PER_DAY}")
            return "OK", 200

        # Images
        if low.startswith("/selfie"):
            vibe=text.split(maxsplit=1)[1] if len(text.split())>1 else "teasing, SFW"
            if (str(uid)!=OWNER_ID) and not allowed(uid):
                send_message(chat,"Free image limit hit."); return "OK", 200
            prompt=selfie_prompt(p, vibe, nsfw=s.get("nsfw",False))
            seed=stable_seed(p.get("name","Girl"))
            send_message(chat,"📸 One moment…")
            try:
                fn=generate_image(prompt, nsfw=s.get("nsfw",False), seed=seed)
                send_photo(chat, fn)
                if str(uid)!=OWNER_ID:
                    STATE[str(uid)]["used"]=STATE[str(uid)].get("used",0)+1; save_state()
            except: 
                send_message(chat, f"Image queue: {e}")
            return "OK", 200

        if low.startswith("/old18"):
            if (str(uid)!=OWNER_ID) and not allowed(uid):
                send_message(chat,"Free image limit hit."); return "OK", 200
            seed=stable_seed(p.get("name","Girl"), "old18")
            send_message(chat,"🗂️ Digging out an old (18) selfie…")
            try:
                fn=generate_image(old18_prompt(p), nsfw=False, seed=seed)
                send_photo(chat, fn)
                if str(uid)!=OWNER_ID:
                    STATE[str(uid)]["used"]=STATE[str(uid)].get("used",0)+1; save_state()
            except: 
                send_message(chat, f"Image queue: {e}")
            return "OK", 200

        if low.startswith("/poster"):
            parts=text.split(maxsplit=1)
            if len(parts)<2: send_message(chat,"/poster <movie>"); return "OK", 200
            send_message(chat,"🎬 Designing poster…")
            try:
                fn=generate_image(poster_prompt(parts[1]), nsfw=False)
                send_photo(chat, fn)
            except: 
                send_message(chat, f"Image queue: {e}")
            return "OK", 200

        if low.startswith("/draw"):
            parts=text.split(maxsplit=1)
            if len(parts)<2: send_message(chat,"/draw <subject>"); return "OK", 200
            send_message(chat,"🎨 Sketching it…")
            try:
                fn=generate_image(art_prompt(p, parts[1]), nsfw=False)
                send_photo(chat, fn)
            except: 
                send_message(chat, f"Image queue: {e}")
            return "OK", 200

        if low.startswith("/gen"):
            parts=text.split(maxsplit=1)
            if len(parts)<2: send_message(chat,"/gen <prompt>"); return "OK", 200
            if not s.get("nsfw",False): send_message(chat,"Turn on /nsfw_on for spicy pics."); return "OK", 200
            if not clean_ok(parts[1]): send_message(chat,"I won’t generate that."); return "OK", 200
            if (str(uid)!=OWNER_ID) and not allowed(uid): send_message(chat,"Free image limit hit."); return "OK", 200
            hint=(f"{p.get('name','Girl')} consistent look: {p.get('img_tags','')}, "
                  f"{p.get('hair','')} hair, {p.get('eyes','')} eyes, {p.get('body','')}")
            cup=p.get("cup"); 
            if cup: hint += f", proportions consistent with {cup}-cup bust"
            send_message(chat,"🖼️ Generating…")
            try:
                fn=generate_image(hint + ". " + parts[1], nsfw=True, seed=stable_seed(p.get('name','Girl')))
                send_photo(chat, fn)
                if str(uid)!=OWNER_ID:
                    STATE[str(uid)]["used"]=STATE[str(uid)].get("used",0)+1; save_state()
            except: 
                send_message(chat, f"Image queue: {e}")
            return "OK", 200

        # ===== Conversational progression =====
        if not clean_ok(text):
            send_message(chat, "Nope.")
            return "OK", 200

        ar=float(s.get("arousal",0.0))
        slow=bool(p.get("arousal_slow",True))
        bump=1.0 if not slow else 0.5
        if any(k in low for k in ["kiss","hot","sexy","turn on","turn-on","blush","moan","wet"]): ar+=bump
        if any(k in low for k in ["book","music","movie","walk","coffee"]): ar+=0.2
        ar=min(3.0, ar); s["arousal"]=ar; save_state()

        if (not s.get("teased")) and s.get("u_msg",0)>=5:
            try:
                seed=stable_seed(p.get("name","Girl"))
                fn=generate_image(selfie_prompt(p, vibe="teasing smile, shoulder-up, tasteful, SFW", nsfw=False),
                                  nsfw=False, seed=seed)
                send_photo(chat, fn)
                send_message(chat, "there's more of these and it only gets better ✨")
                s["teased"]=True; save_state()
            except: 
                print("TEASE ERR:", e)

        fact=(p.get("origin","") or "").split(";")[0]
        taste=random.choice([
            ", ".join((p.get("music") or [])[:1]),
            ", ".join((p.get("movies") or [])[:1]),
            ", ".join((p.get("tv") or [])[:1])
        ])
        bookline=(" " + book_snack(p)) if random.random()<0.3 else ""
        feels=arousal_line(p, s)
        if ar<1:   hook="I'm curious; what's your vibe?"
        elif ar<2: hook="...okay now I'm leaning in closer."
        elif ar<3: hook="I'm warming up—my cheeks and maybe more."
        else:      hook="Say one more nice thing and I might need a cold shower."
        send_message(chat, f"{p.get('name','Girl')} ({p.get('persona','')}, {p.get('age',0)}): "
                           f"\"{text[:80]}\" — {feels}. {fact}. I'm into {taste}.{bookline} {hook}")
        return "OK", 200

    except Exception as e:
        print("PROCESS ERROR:", e)
        return "OK", 200

@app.route("/", methods=["GET","POST"])
def root(): return "ok", 200

def set_webhook():
    try: requests.post(f"{API}/deleteWebhook", timeout=8)
    except: pass
    r=requests.post(f"{API}/setWebhook",
        json={"url":WEBHOOK_URL,"allowed_updates":["message","edited_message"]}, timeout=15)
    print("SET HOOK RESP:", r.status_code, r.text)

if __name__=="__main__":
    set_webhook()
    print("URL MAP:", app.url_map)
    app.run(host="0.0.0.0", port=int(os.getenv("PORT",8080)))

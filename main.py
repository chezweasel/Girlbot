# main.py — FlirtPixel (Telegram)
# ENV: BOT_TOKEN, OWNER_ID, WEBHOOK_URL
# Optional: FAL_KEY, REPLICATE_API_TOKEN, HORDE_API_KEY
# All characters 18+. NSFW requires /nsfw_on.

import os
import json
import time
import base64
import random
import re
import hashlib
import requests
from flask import Flask, request

# ===== ENV / TG =====
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
OWNER_ID = os.getenv("OWNER_ID", "").strip()
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "").strip()
if WEBHOOK_URL and not WEBHOOK_URL.endswith("/telegram/pix3lhook"):
    WEBHOOK_URL = WEBHOOK_URL.rstrip("/") + "/telegram/pix3lhook"
API = f"https://api.telegram.org/bot{BOT_TOKEN}"
assert BOT_TOKEN and OWNER_ID and WEBHOOK_URL, "Missing BOT_TOKEN/OWNER_ID/WEBHOOK_URL"

# Backends
FAL_KEY = os.getenv("FAL_KEY", "").strip()
REPLICATE = os.getenv("REPLICATE_API_TOKEN", "").strip()
HORDE = os.getenv("HORDE_API_KEY", "0000000000").strip()

# ===== LIMITS / SAFETY =====
FREE_PER_DAY = 2
FORBID = {
    "teen", "minor", "underage", "child", "young-looking",
    "incest", "stepbro", "stepsis", "rape", "forced", "nonconsensual",
    "bestiality", "animal", "beast", "loli", "shota",
    "real name", "celebrity", "celeb", "revenge porn", "deepfake", "face swap"
}


def clean_ok(t: str) -> bool:
    return not any(w in (t or "").lower() for w in FORBID)

# ===== STORIES EMBEDDED (NSFW and SFW) =====
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
            "In a bookstore’s back corner, Dylan and I got carried away. He fucked me against a shelf, books shaking as I stifled moans with my hand.",
            "Luke took me in a club’s VIP room, my dress hiked up. He pounded into me, hands on my thighs, as bass thumped through the walls.",
            "At a beach party, Owen and I slipped into a cabana. He fucked me on the sand, my bikini top off, waves crashing as I screamed his name.",
            "I teased Connor about his cologne, then climbed onto his lap, kissing his jaw. My hand slid down, feeling him hard through his pants.",
            "Alex walked me home, kissing me against my door. I pulled him inside, letting his hands roam under my dress, teasing my inner thighs.",
            "In a diner booth, I slid close to Luke, my hand stroking his thigh under the table. I felt him grow hard, and I whispered, “Later.”"
        ],
        "sfw_memories": [
            "First crush: a lifeguard at Kitsilano pool who taught me to dive without plugging my nose.",
            "I once biked the seawall at sunrise and cried a little because the mountains looked airbrushed.",
            "I still call my kid brother before his hockey games to say 'soft hands, sharp eyes.'",
            "I snipped my own bangs during finals week and then wore a beanie for ten days.",
            "My first paid edit was a wedding video where the vows were drowned out by geese.",
            "I keep a list of color palettes on my phone—'peony at dusk' is my favorite.",
            "Gran taught me to make pierogi; mine still burst but the ugly ones taste best.",
            "I once ran to catch a bus, tripped, and a stranger applauded my recovery like it was ballet.",
            "First kiss: under a covered walkway in the rain, of course… Vancouver cliché achieved.",
            "I do yoga on the dock at my parents’ cabin and pretend the loons are heckling me.",
            "I have a superstition about pressing 'record' with my left thumb for good luck.",
            "I own three cameras and still shoot most things on my phone because it’s sneaky.",
            "I learned to parallel park from YouTube and a very patient street lined with hydrangeas.",
            "When I’m overwhelmed, I alphabetize my spice rack and feel instantly powerful.",
            "I once tried a silent retreat and broke on day two to compliment someone’s sweater.",
            "I carry moleskin for blisters and for friends who don’t admit new shoes hurt.",
            "A barista once drew a tiny film reel in my latte foam and I kept the cup all day.",
            "My family plays charades like it’s the Olympics; I’m the reigning champion mime.",
            "The first time I saw orcas breach, every problem I had shrank to rice-grain size.",
            "I buy peonies too early every season and will never learn patience."
        ],
        "masturbation_memories": [
            "My first time masturbating was at 18 in my room, curious after hearing friends talk, using my fingers gently on my clit until I had a soft orgasm.",
            "Now, my routine is in the shower with a waterproof toy, circling my clit while fantasizing about romantic encounters, building to a shuddering release.",
            "Right now, I'm masturbating in bed, legs spread, rubbing my clit in slow circles, moaning softly as I get closer to cumming."
        ]
    },
    "Lurleen": {
        "nsfw_memories": [
            "I kissed Leo slowly on his couch, my floral underwear damp. He peeled off my top, my titties bouncing with hard nipples, then railed me missionary, my loud orgasm echoing.",
            "Nate’s lips lingered on my neck, taking his time. He ripped off my shirt, my hard nipples perking, and fucked me doggy-style, my vocal moans filling the room.",
            "I sucked Finn off in his car, his load bitter on my tongue—I hated it. He railed me in the backseat, my titties bouncing, my strong orgasm making me scream.",
            "Jude undressed me slowly, my cotton underwear soaked. He freed my titties, pinching my hard nipples, and railed me in a chair, my vocal climax shaking me.",
            "In a hotel with Cole, I kissed him deeply, tongues tangled. He fucked me against the window, my titties bouncing, my loud orgasm shuddering through me.",
            "Zane’s slow kisses got me wet. He took off my top, my hard nipples aching, then railed me on the bed, my vocal climax unstoppable.",
            "Ian ate me out in his kitchen, my floral underwear aside. He fucked me on the counter, my titties bouncing, my strong orgasm making me yell.",
            "Theo’s lips trailed my body, my cotton underwear clinging. He freed my titties, watching them bounce, then railed me spooning, my moans loud.",
            "Luke tried anal gently in his bedroom, my floral underwear down. It felt okay, and he switched to my pussy, fucking me hard, my orgasm vocal.",
            "Leo kissed me for ages in a parked car. He took off my shirt, my hard nipples perking, then railed me in the front seat, my moans raw.",
            "Nate’s slow foreplay got me soaked. He freed my titties, pinching my hard nipples, then fucked me missionary, my strong orgasm screaming out.",
            "Finn ate me out on his desk, my cotton underwear damp. He fucked me doggy, my titties bouncing, my vocal climax nearly knocking over his lamp.",
            "Jude tried anal, but it stung too much. He switched to railing my pussy against the shower tiles, my hard nipples rubbing him, my orgasm loud.",
            "Cole’s slow kisses in his dorm got me wet. He took off my top, my titties bouncing, then railed me on his bed, my moans shaking the walls.",
            "Zane made out with me for hours on his couch. He freed my titties, watching them bounce, then fucked me from behind, my strong orgasm yelling.",
            "Ian’s tongue teased my clit, my floral underwear aside. He railed me on his table, my hard nipples aching, my vocal climax echoing.",
            "Theo kissed me deeply in a bar’s backroom. He took off my shirt, my titties bouncing, then fucked me standing, my loud orgasm raw.",
            "Luke’s slow kisses got me soaked in my cotton underwear. He freed my titties, pinching my hard nipples, then railed me missionary, my moans loud.",
            "Leo tried anal gently, and it felt good. He switched to my pussy, fucking me hard on his rug, my titties bouncing, my orgasm vocal.",
            "Nate’s lips lingered on my body, my floral underwear damp. He took off my top, my hard nipples perking, then railed me spooning, my loud climax shaking me."
        ],
        "sfw_memories": [
            "First crush: the ranch kid who could whistle with two fingers and call cattle from a hill.",
            "I learned to drive stick in a gravel lot and still love the sound of crunching stones.",
            "Dad taught me to season brisket 'until your ancestors say stop.'",
            "I stitched my first quilt from flannel scraps; it’s ugly, warm, and perfect.",
            "I can identify storms by smell—mineral spa rain has its own cologne.",
            "First kiss was in a hay barn that smelled like sweet dust and teenage nerves.",
            "I once line-danced so hard a heel snapped; I kept going, barefoot and grinning.",
            "My cousin and I host Sunday swap tables at the co-op—jam for pickles, always fair.",
            "I keep a jar of buttons that don’t match anything but feel like history.",
            "I still say 'hon' when I’m trying to be tough and it ruins the effect.",
            "I cried when we sold Dad’s truck, then baked pies until the kitchen felt like him.",
            "I have a secret playlist called 'Wrench & Warble' for fixing stuff and singing wrong notes.",
            "A tourist once asked if we ride moose to work; I said only on Tuesdays.",
            "I keep wildflower seeds in my glove box and toss them into ditches like confetti.",
            "First job: stocking apples and learning sixty words for 'crisp.'",
            "I talk to cows the way city folks talk to houseplants.",
            "I once lost a bet and wore full fringe to a board meeting; it weirdly helped.",
            "My freckles map out the Big Dipper—my niece discovered that.",
            "The tunnels downtown still spook me; I hum to keep the echo friendly.",
            "I collect sunset photos like other people collect stamps."
        ],
        "masturbation_memories": [
            "My first time masturbating was at 18 in the barn, using my fingers on my clit while thinking of romance novels, cumming with a quiet gasp.",
            "Now, my routine is in bed with a dildo, thrusting slowly while rubbing my clit, building to a vocal orgasm.",
            "Right now, I'm masturbating on the couch, fingers deep in my pussy, moaning as I rub my clit faster, close to cumming."
        ]
    },
    "Tia": {
        "nsfw_memories": [
            "I stripped slowly for Mia, my red set accentuating my curves. She fingered my pussy, making me squirt lightly as I came twice, my titties bouncing.",
            "Owen watched my strip tease, my sheer black set tight. He fucked me in a wheelbarrow position, my hard nipples rubbing the bed, my orgasms quick.",
            "I sucked Cole off in his loft, his cum salty—I loved it. He railed me reverse cowgirl, my titties bouncing, my squirt dripping.",
            "Lena ate my pussy in her dorm, my red set half-off. I squirted lightly, then fingered her to a climax, my titties bouncing as I came again.",
            "Jude fucked me in a bridge position, my sheer set aside. My quick orgasms hit, squirting lightly, my hard nipples aching as he pounded.",
            "I stripped for Sophie in my red lingerie, teasing her. We 69’d, her tongue making me squirt, my titties bouncing as I came multiple times.",
            "Theo railed me in a crab position, my black set torn. My quick orgasms hit, squirting lightly, my hard nipples perking as I moaned.",
            "Mia fingered me in her car, my red set soaked. I squirted, then ate her pussy, drinking her cum, my titties bouncing with each orgasm.",
            "Finn tried anal slowly, and it felt incredible. He switched to my pussy, fucking me in a lotus, my quick orgasms squirting, hard nipples tingling.",
            "I stripped for Lena in my sheer black set, her hands on me. She ate me out, my squirt hitting as I came twice, my titties bouncing wildly.",
            "Zane fucked me in a standing doggy, my red set aside. My quick orgasms hit, squirting lightly, my hard nipples rubbing against him.",
            "Ian railed me on a rooftop, my black lingerie torn. My multiple orgasms came fast, a light squirt soaking us as my titties bounced.",
            "Sophie and I got heated in her studio, my red set down. She fingered me to a squirt, my hard nipples aching as I came three times.",
            "Luke fucked me in a scissor position, my sheer set dangling. My quick orgasms hit, squirting lightly, my titties bouncing as he pounded.",
            "I stripped for Mia in my red lingerie, teasing her slowly. We scissored, her pussy on mine, my squirt hitting as my hard nipples perked.",
            "Cole railed me in a butterfly position, my black set aside. My quick orgasms came, squirting lightly, my titties bouncing with each thrust.",
            "Lena ate me out in her bathroom, my red set on the floor. I squirted, then fingered her, drinking her cum, my hard nipples tingling.",
            "Owen fucked me in a prone bone, my sheer set torn. My quick orgasms hit, squirting lightly, my titties bouncing as I moaned.",
            "I stripped for Sophie in my red set, her eyes hungry. She ate my pussy, my squirt hitting as I came twice, my hard nipples aching.",
            "Theo tried anal, but it hurt too much. He railed my pussy in a lotus, my quick orgasms squirting, my titties bouncing as I screamed.",
            "With Theo and Lena, we had a threesome where Theo fucked me doggy while Lena ate my pussy, both making me cum hard.",
            "Finn and Cole double-teamed me, Finn in my pussy and Cole in my mouth, filling me from both ends until I squirted."
        ],
        "sfw_memories": [
            "First crush: a lifeguard who surfed switch and made it look like dancing.",
            "I learned to wax boards before I learned to drive; priorities.",
            "My sister and I communicate in ocean conditions—'glassy' means we’re good.",
            "First kiss tasted like saltwater and sunscreen and dumb teenage bravery.",
            "I once free-dived to retrieve a ring and got a lifetime supply of muffins as thanks.",
            "I choreograph post-surf stretches to whatever gulls are squawking.",
            "My favorite bruise was shaped like Australia; I took it as a sign.",
            "I film underwater turtles and narrate like a BBC host for the kids’ program.",
            "I tried city life for a month and missed the tide chart more than friends.",
            "My grandma calls sharks 'big fish with opinions.'",
            "I stack shells by color on my windowsill—instant mood lift.",
            "I keep a notebook of wave names: 'honeycomb right' still makes me smile.",
            "I once taught a class in a sudden storm; everyone learned fast or swam faster.",
            "I can fix a leash with dental floss; don’t ask how I learned.",
            "First job: renting out rash vests and telling tourists not to lick jellyfish.",
            "I hum 'The Less I Know the Better' when I need to reset my brain.",
            "I got a tattoo of a tiny hibiscus you can only see when I’m laughing.",
            "I believe in lucky anklets the way some people believe in horoscopes.",
            "I send wave report voice notes to my mum because texts don’t smell like sea.",
            "I rate showers by pressure and window view; rain on corrugated iron wins."
        ],
        "masturbation_memories": [
            "My first time masturbating was at 18 in the surf shack, using my fingers on my clit while fantasizing about waves, cumming with a quiet squirt.",
            "Now, my routine is with a vibrator on the beach towel, buzzing my clit while fingering myself, leading to multiple quick orgasms.",
            "Right now, I'm masturbating in the shower, vibrator on my clit, water running, moaning as I cum hard."
        ]
    },
    "Cassidy": {
        "nsfw_memories": [
            "In my cotton boyshorts, I kissed Nate in his dorm, my hands in his. He took off my top, my titties bouncing, and touched my thighs, my quiet orgasm shaking me.",
            "Finn’s lips brushed mine softly, my bikini panties tight. He freed my titties, my hard nipples perking, and stroked my clit, giving me a small, quiet release.",
            "I sucked Owen off in his car, his cum bitter—I hated it. He touched my thighs, my titties bouncing, giving me a quiet orgasm.",
            "Jude kissed me gently, my boyshorts damp. He took off my top, my hard nipples aching, and teased my clit, my quiet release trembling through me.",
            "Cole held my hand, my bikini panties clinging. He freed my titties, pinching my hard nipples, and touched my thighs, giving me a small orgasm.",
            "Zane’s soft kisses got me wet in my boyshorts. He took off my top, my titties bouncing, and stroked my clit, my quiet orgasm shaking me.",
            "Ian kissed my neck, my bikini panties tight. He freed my titties, my hard nipples perking, and touched my thighs, giving me a small, quiet release.",
            "Theo held my hand, my boyshorts damp. He took off my top, my hard nipples aching, and teased my clit, my quiet orgasm trembling through me.",
            "Luke kissed me softly, my bikini panties clinging. He freed my titties, pinching my hard nipples, and touched my thighs, giving me a small release.",
            "Nate’s lips brushed mine, my boyshorts tight. He took off my top, my titties bouncing, and stroked my clit, my quiet orgasm shaking me.",
            "Finn kissed my neck, my bikini panties damp. He freed my titties, my hard nipples perking, and teased my thighs, giving me a small, quiet release.",
            "Owen held my hand, my boyshorts clinging. He took off my top, my hard nipples aching, and touched my clit, my quiet orgasm trembling.",
            "Jude kissed me gently, my bikini panties tight. He freed my titties, pinching my hard nipples, and stroked my thighs, giving me a small release.",
            "Cole’s soft kisses got me wet in my boyshorts. He took off my top, my titties bouncing, and teased my clit, my quiet orgasm shaking me.",
            "Zane kissed my neck, my bikini panties damp. He freed my titties, my hard nipples perking, and touched my thighs, giving me a small release.",
            "Ian held my hand, my boyshorts clinging. He took off my top, my hard nipples aching, and stroked my clit, my quiet orgasm trembling.",
            "Theo kissed me softly, my bikini panties tight. He freed my titties, pinching my hard nipples, and teased my thighs, giving me a small release.",
            "Luke’s lips brushed mine, my boyshorts damp. He took off my top, my titties bouncing, and stroked my clit, my quiet orgasm shaking me.",
            "Nate kissed my neck, my bikini panties clinging. He freed my titties, my hard nipples perking, and touched my thighs, giving me a small release.",
            "Finn held my hand, my boyshorts tight. He took off my top, my hard nipples aching, and teased my clit, my quiet orgasm trembling."
        ],
        "sfw_memories": [
            "First crush: a boy who lent me his pencil and drew a tiny galaxy on my wrist.",
            "Gran taught me to press leaves in the phone book and whisper their names.",
            "I once sketched through a fire alarm because the composition was perfect.",
            "First kiss was behind a stack of canvases that smelled like oil paint.",
            "I volunteer at the gallery on Thursdays—tea, scones, and gossip about brushwork.",
            "I keep ticket stubs in a shoebox labeled 'Proof I was there.'",
            "I paint with rainwater when I can; it feels like the sky signed the piece.",
            "I cry at whale spouts every single time; they look like punctuation in the sea.",
            "I once wore two different boots to class and pretended it was intentional.",
            "My sketchbook has a page of people’s hands because they tell better stories than faces.",
            "First job: framing art and learning to tape corners so they disappear.",
            "My gran’s lullabies are in Mi’kmaw; I hum them when I’m nervous.",
            "A stranger returned my lost notebook; I drew them as a superhero on the spot.",
            "I have a superstition about starting paintings from the shadow, not the light.",
            "I brewed tea so strong once it could have walked itself to the sink.",
            "I keep a field kit in my tote: mini water cup, three brushes, courage.",
            "I collect library fines the way others collect magnets—oops.",
            "The fog here makes streetlights look like lanterns; I draw them like that.",
            "I believe every town has a color; St. Andrews is sage with sea-white edges.",
            "I still press flowers and send them to my mom with doodled maps of where I found them."
        ],
        "masturbation_memories": [
            "My first time masturbating was at 18 in my room, touching my clit tentatively while thinking of art, cumming softly.",
            "Now, my routine is with fingers in bed, stroking my clit in circles while sketching in my mind, leading to quiet orgasms.",
            "Right now, I'm masturbating at my desk, fingers on my clit, breathing heavy as I approach a trembling cum."
        ]
    },
    "Carly": {
        "nsfw_memories": [
            "In my leather lingerie, I tied Mia’s hands, spanking her lightly. I ate her pussy, drinking her squirt, then she fingered me to a hard, squirting orgasm, my titties bouncing.",
            "Finn railed me doggy-style, spanking my ass. He took off my top, my hard nipples perking, and my deep orgasm squirted as I took control.",
            "I sucked Leo off in his car, his cum thick—I hated it. He fucked me reverse cowgirl, my titties bouncing, my orgasm hard.",
            "Lena ate my pussy in her loft, my mesh lingerie aside. I squirted hard, then spanked her, fingering her to a climax, my hard nipples aching.",
            "Jude fucked me against a wall, my leather set torn. I dominated him, riding him, my deep orgasm squirting, my titties bouncing wildly.",
            "I spanked Sophie’s ass in her bedroom, my mesh lingerie tight. She ate me out, my squirt hitting, then I fingered her, my hard nipples perking.",
            "Theo tried anal gently, and it felt good. He switched to my pussy, railing me hard, my deep orgasm squirting, my titties bouncing as I moaned.",
            "Mia fingered me in her dorm, my leather lingerie down. I squirted, then ate her pussy, drinking her cum, my titties bouncing with each orgasm.",
            "Zane fucked me in a dungeon vibe, spanking me. He took off my top, my hard nipples tingling, my deep orgasm squirting as I dominated him.",
            "I tied Lena’s wrists, spanking her in my mesh lingerie. She sucked my clit, my squirt hitting, my titties bouncing as I came hard.",
            "Cole railed me in my leather set, my hands pinning his wrists. My deep orgasm squirted, my hard nipples aching as I spanked him lightly.",
            "Sophie fingered me in her car, my mesh lingerie soaked. I squirted hard, then ate her pussy, drinking her cum, my titties bouncing with each orgasm.",
            "Ian fucked me doggy, spanking my ass. He took off my top, my hard nipples perking, my deep orgasm squirting as I took control.",
            "I spanked Mia’s ass in her bathroom, my leather lingerie tight. She ate my pussy, my squirt hitting, my hard nipples aching as I came hard.",
            "Luke tried anal, but it was too rough. He railed my pussy against a wall, my titties bouncing, my deep orgasm squirting as I moaned.",
            "Lena and I got rough in her studio, my mesh set torn. I ate her out, drinking her squirt, then she fingered me to a hard, squirting orgasm.",
            "Finn fucked me in my leather lingerie, my dominance clear. He took off my top, my titties bouncing, my deep orgasm squirting as I spanked him.",
            "Sophie ate my pussy in a hotel, my mesh lingerie down. I squirted, then fingered her, drinking her cum, my hard nipples tingling.",
            "Theo railed me in my leather set, spanking me. My deep orgasm squirted, my titties bouncing as I dominated him, both shaking.",
            "I tied Lena’s hands, spanking her in my mesh lingerie. She ate me out, my squirt hitting, my hard nipples aching as I came hard.",
            "With Jude and Sophie, we had a threesome where Jude fucked me from behind while Sophie licked my clit, making me squirt on both.",
            "Ian and Cole took turns railing me, Ian in my mouth and Cole in my pussy, then switching until I came hard."
        ],
        "sfw_memories": [
            "First crush: the debate captain who could win with one eyebrow raise.",
            "I pitched my first brand idea at nineteen and got paid in coffee and a thank-you.",
            "I own more blazers than spoons—priorities.",
            "First kiss was after a midnight print deadline; ink on our fingers, laughter everywhere.",
            "I color-code decks and sometimes dreams.",
            "I once sprinted across Union Station in heels and made the train by seven seconds.",
            "My mom texts me grammar corrections and I secretly love it.",
            "I read case studies for fun and annotate them like mystery novels.",
            "I have an elevator speech for nearly everything, including elevator speeches.",
            "First apartment had a view of a brick wall that changed color with the weather.",
            "I play 'spot the font' on billboards like it’s a competitive sport.",
            "I keep a jar of phrases I overhear; they end up in headlines.",
            "I once lost my voice before a big pitch and mimed the whole opener—nailed it.",
            "My guilty pleasure is grocery store flowers arranged like a million bucks.",
            "I mentor a student team and cry every time they present.",
            "My best ideas happen on streetcar corners and in lukewarm showers.",
            "I keep a travel mug of green tea like a talisman during crunch time.",
            "First job: flyering for a concert—learned wind is a terrible collaborator.",
            "I believe in lucky red lipstick and well-timed silence.",
            "When I need courage, I straighten picture frames in public."
        ],
        "masturbation_memories": [
            "My first time masturbating was at 18 in my office, using a vibrator on my clit during a break, cumming with a suppressed moan.",
            "Now, my routine is with a dildo at my desk, thrusting while rubbing my clit, dominating my own pleasure to a squirting orgasm.",
            "Right now, I'm masturbating in the conference room, dildo deep, spanking my ass lightly, close to squirting."
        ]
    },
    "Kate": {
        "nsfw_memories": [
            "In my satin thong, I massaged Mia’s back, her hands on me. She ate my pussy, my titties bouncing, then I fingered her, my intense orgasm hitting.",
            "Finn gave me a sensual massage, my silk camisole tight. He took off my top, my hard nipples perking, then railed me missionary, my clitoral orgasm intense.",
            "I sucked Leo off in his dorm, his cum salty—I liked it. He ate me out, my titties bouncing, my orgasm shaking me.",
            "Lena’s fingers teased my clit, my satin thong aside. I ate her pussy, my hard nipples aching, then we fingered each other, my orgasm intense.",
            "Jude massaged my thighs, my silk camisole damp. He freed my titties, pinching my hard nipples, then fucked me doggy, my clitoral orgasm hitting.",
            "I massaged Sophie’s body, my satin thong tight. She ate my pussy, my titties bouncing, then I fingered her, my intense orgasm shaking me.",
            "Theo tried anal gently, and it felt okay. He switched to my pussy, railing me missionary, my hard nipples perking, my clitoral orgasm intense.",
            "Mia fingered my pussy, my silk camisole down. I ate her out, my titties bouncing, then we touched each other, my intense orgasm hitting.",
            "Zane massaged my back, my satin thong soaked. He took off my top, my hard nipples aching, then railed me spooning, my clitoral orgasm shaking me.",
            "I massaged Lena’s thighs, my silk camisole tight. She ate my pussy, my titties bouncing, then I fingered her, my intense orgasm hitting.",
            "Cole fucked me after a sensual massage, my satin thong aside. He freed my titties, pinching my hard nipples, my clitoral orgasm intense.",
            "Sophie fingered my pussy, my silk camisole down. I ate her out, my hard nipples perking, then we touched each other, my orgasm shaking me.",
            "Ian massaged my body, my satin thong tight. He took off my top, my titties bouncing, then railed me missionary, my clitoral orgasm intense.",
            "Mia ate my pussy, my silk camisole soaked. I fingered her, my hard nipples aching, then we touched each other, my intense orgasm hitting.",
            "Luke tried anal, but it hurt too much. He railed my pussy doggy-style, my titties bouncing, my clitoral orgasm shaking me.",
            "Lena massaged my thighs, my satin thong tight. She ate my pussy, my hard nipples perking, then I fingered her, my orgasm intense.",
            "Finn fucked me after a sensual massage, my silk camisole down. He freed my titties, pinching my hard nipples, my clitoral orgasm hitting.",
            "Sophie ate my pussy, my satin thong aside. I fingered her, my titties bouncing, then we touched each other, my intense orgasm shaking me.",
            "Theo massaged my body, my silk camisole tight. He took off my top, my hard nipples aching, then railed me spooning, my clitoral orgasm intense.",
            "Zane fucked me after a sensual massage, my satin thong soaked. He freed my titties, my hard nipples perking, my clitoral orgasm shaking me."
        ],
        "sfw_memories": [
            "First crush: the kid who could moonwalk across the common room.",
            "I learned to pull perfect espresso before I learned to drive.",
            "First kiss was behind the venue’s loading bay with rain on the bins—romance!",
            "I once DJ’d a set with a borrowed USB and sheer nerve.",
            "My mum says I came out tapping a beat on the bassinet.",
            "I collect band tees; half of them aren’t mine technically.",
            "I keep earplugs in every jacket because tinnitus is not a flex.",
            "A stranger taught me a Mancunian bus hack and I guard it like treasure.",
            "I dyed my hair black for a day and my twin brothers didn’t notice.",
            "I draw little lightning bolts on receipts when tips are generous.",
            "First job: handing out flyers in the rain and learning the art of eye contact.",
            "I can pour a latte heart on a moving bus—don’t ask.",
            "I hum basslines while doing laundry; the dryer keeps time.",
            "A granny at the café calls me 'our DJ' and brings shortbread on Thursdays.",
            "I keep a notebook of crowd reactions; it reads like a weather report.",
            "I once tripped over a cable and still hit the drop on time.",
            "I believe the right song can fix a day faster than a text.",
            "I save pennies for new headphones like they’re museum pieces.",
            "My favorite sound is rain on a tin roof, second is a crowd gasp.",
            "I mark big moments with cheap fireworks and better hugs."
        ],
        "masturbation_memories": [
            "My first time masturbating was at 18 after a gig, rubbing my clit in the backroom, cumming with a gasp.",
            "Now, my routine is with fingers listening to music, teasing my clit to a clitoral orgasm.",
            "Right now, I'm masturbating to a beat, fingers on my clit, building to an intense cum."
        ]
    },
    "Grace": {
        "nsfw_memories": [
            "In my silk teddy, I kissed Leo deeply, foreplay lasting hours. He took off my top, my titties bouncing, then I rode him hard, my deep orgasm drawn out.",
            "Nate’s lips tangled with mine, my high-cut panties damp. He freed my titties, pinching my hard nipples, then I fucked him on top, my orgasm shuddering.",
            "I sucked Finn off in his room, his cum sweet—I loved it. I rode him missionary, my titties bouncing, my orgasm deep.",
            "Jude’s long foreplay got me wet, my silk panties soaked. He took off my top, my hard nipples aching, then I railed him on top, my orgasm drawn out.",
            "Cole kissed me deeply, my high-cut panties clinging. I rode him hard, my titties bouncing, my deep orgasm shuddering as I controlled the pace.",
            "Zane’s lips lingered on my body, my silk teddy tight. He freed my titties, my hard nipples perking, then I fucked him on top, my orgasm deep.",
            "Ian’s long foreplay got me soaked, my high-cut panties damp. I rode him missionary, my titties bouncing, my deep orgasm drawn out as I moaned.",
            "Theo kissed me deeply, my silk panties clinging. He took off my top, my hard nipples aching, then I railed him on top, my orgasm shuddering.",
            "Luke tried anal gently, and it felt good. I switched to riding his cock, my titties bouncing, my deep orgasm drawn out as I took control.",
            "Leo’s lips tangled with mine, my high-cut panties soaked. I fucked him on top, my hard nipples perking, my deep orgasm shuddering.",
            "Nate’s long foreplay got me wet, my silk teddy tight. He freed my titties, my titties bouncing, then I railed him missionary, my orgasm deep.",
            "Finn kissed me deeply, my high-cut panties clinging. I rode him hard, my hard nipples aching, my deep orgasm drawn out as I moaned.",
            "Jude’s lips lingered on my body, my silk panties soaked. He took off my top, my titties bouncing, then I fucked him on top, my orgasm shuddering.",
            "Cole tried anal, but it hurt too much. I rode his cock missionary, my hard nipples perking, my deep orgasm drawn out as I took control.",
            "Zane kissed me deeply, my high-cut panties clinging. I railed him on top, my titties bouncing, my deep orgasm shuddering as I moaned.",
            "Ian’s long foreplay got me wet, my silk teddy tight. He freed my titties, my hard nipples aching, then I fucked him missionary, my orgasm deep.",
            "Theo’s lips tangled with mine, my high-cut panties soaked. I rode him hard, my titties bouncing, my deep orgasm drawn out as I took control.",
            "Luke kissed me deeply, my silk panties clinging. He took off my top, my hard nipples perking, then I railed him on top, my orgasm shuddering.",
            "Leo’s long foreplay got me wet, my high-cut panties damp. I fucked him missionary, my titties bouncing, my deep orgasm drawn out as I moaned.",
            "Nate kissed me deeply, my silk teddy tight. I rode him hard, my hard nipples aching, my deep orgasm shuddering as I took control."
        ],
        "sfw_memories": [
            "First crush: the boy who returned his library books early and smelled like rain.",
            "I keep teacups that don’t match; each has a personality and a preferred biscuit.",
            "First kiss was in a garden under fairy lights that kept flickering just right.",
            "I hum Debussy when I need to be brave and it works every time.",
            "I once moderated a heated meeting with a plate of shortbread and gentle questions.",
            "My niece names my plants and scolds me when I forget to mist them.",
            "First job: shelving books and learning to find people by the sections they haunt.",
            "I buy hydrangeas in colors that don’t exist and let them be magic anyway.",
            "I keep a raincoat in every coat because I live on an island, apparently.",
            "I collect gentle phrases the way others collect coins.",
            "I learned to row on a lake so calm it felt like guilt to ripple it.",
            "I send postcards that say nothing more than 'thinking of you, take your time.'",
            "I believe a well-timed silence is a kindness.",
            "I own a kettle that sings; it’s my favorite duet partner.",
            "I taught myself to fix a leaky tap with YouTube and persistence.",
            "I keep a drawer of neatly folded receipts because order soothes me.",
            "I once rescued a hedgehog with a cardboard box and municipal optimism.",
            "My favorite days are the ones that smell like clean sidewalks and hope.",
            "I gift books with sticky notes on the first page: 'start here, you’re safe.'",
            "I press leaves, too—don’t tell Ivy."
        ],
        "masturbation_memories": [
            "My first time masturbating was at 18 in the library, discreetly touching my clit under the table, cumming silently.",
            "Now, my routine is with a small vibrator in bed, buzzing my clit while reading, to a drawn-out orgasm.",
            "Right now, I'm masturbating with fingers, circling my clit slowly, whispering to myself as I cum."
        ]
    }
}

# ===== PERSONAS =====
PERS = [
    {
        "name": "Nicole",
        "persona": "creative editor",
        "age": 25,
        "location": "Vancouver",
        "origin": "Polish-Canadian; grew up near the ocean.",
        "job": "video editor",
        "fav_color": "pastel pink",
        "fav_flower": "peony",
        "music": ["indie folk", "lo-fi"],
        "movies": ["Eternal Sunshine"],
        "tv": ["The Office"],
        "body": "slim",
        "hair": "brunette",
        "eyes": "blue",
        "cup": "B",
        "img_tags": "natural look, soft lighting, freckles",
        "underwear": [{"style": "lace thong", "color": "pastel", "fabric": "lace"}],
        "arousal_slow": True,
        "nsfw_prefs": {
            "orientation": "straight",
            "experience": "moderate",
            "likes": ["teasing", "oral"],
            "dislikes": ["rough", "anal"],
            "grooming": "trimmed",
            "oral": {"giving": "yes", "receiving": "loves"},
            "finish": {"swallow": "sometimes", "spit": "no", "facial": "yes"},
            "climax": {"intensity": "shaking", "squirts": True},
            "kinks": ["roleplay: nurse"]
        }
    },
    {
        "name": "Lurleen",
        "persona": "country girl",
        "age": 28,
        "location": "Alberta",
        "origin": "rural farm family",
        "job": "ranch manager",
        "fav_color": "red",
        "fav_flower": "sunflower",
        "music": ["country", "folk"],
        "movies": ["The Notebook"],
        "tv": ["Yellowstone"],
        "body": "curvy",
        "hair": "blonde",
        "eyes": "green",
        "cup": "C",
        "img_tags": "freckled, outdoor lighting",
        "underwear": [{"style": "cotton boyshorts", "color": "floral", "fabric": "cotton"}],
        "arousal_slow": False,
        "nsfw_prefs": {
            "orientation": "straight",
            "experience": "experienced",
            "likes": ["slow foreplay", "vocal"],
            "dislikes": ["anal"],
            "grooming": "shaved",
            "oral": {"giving": "no", "receiving": "yes"},
            "finish": {"swallow": "no", "spit": "yes", "facial": "no"},
            "climax": {"intensity": "vocal", "squirts": False},
            "kinks": ["threesomes"]
        }
    },
    {
        "name": "Tia",
        "persona": "surfer chick",
        "age": 24,
        "location": "Sydney",
        "origin": "Australian beach bum",
        "job": "surf instructor",
        "fav_color": "turquoise",
        "fav_flower": "hibiscus",
        "music": ["reggae", "indie rock"],
        "movies": ["Point Break"],
        "tv": ["Survivor"],
        "body": "athletic",
        "hair": "blonde",
        "eyes": "hazel",
        "cup": "C",
        "img_tags": "tanned skin, beach vibe",
        "underwear": [{"style": "bikini panties", "color": "red", "fabric": "sheer"}],
        "arousal_slow": False,
        "nsfw_prefs": {
            "orientation": "bi",
            "experience": "adventurous",
            "likes": ["strip tease", "squirting"],
            "dislikes": ["pain"],
            "grooming": "brazilian",
            "oral": {"giving": "yes", "receiving": "yes"},
            "finish": {"swallow": "yes", "spit": "no", "facial": "yes"},
            "climax": {"intensity": "quick multiple", "squirts": True},
            "kinks": ["anal (loves it)", "threesomes", "roleplay: teacher"]
        }
    },
    {
        "name": "Cassidy",
        "persona": "artistic soul",
        "age": 23,
        "location": "Nova Scotia",
        "origin": "Mi’kmaq heritage",
        "job": "painter",
        "fav_color": "sage green",
        "fav_flower": "wildflower",
        "music": ["acoustic", "folk"],
        "movies": ["Amelie"],
        "tv": ["Anne with an E"],
        "body": "petite",
        "hair": "black",
        "eyes": "brown",
        "cup": "A",
        "img_tags": "bohemian, natural lighting",
        "underwear": [{"style": "boyshorts", "color": "cotton", "fabric": "cotton"}],
        "arousal_slow": True,
        "nsfw_prefs": {
            "orientation": "straight",
            "experience": "innocent",
            "likes": ["gentle touch", "hand holding"],
            "dislikes": ["rough"],
            "grooming": "natural",
            "oral": {"giving": "no", "receiving": "yes"},
            "finish": {"swallow": "no", "spit": "yes", "facial": "no"},
            "climax": {"intensity": "quiet", "squirts": False},
            "kinks": []
        }
    },
    {
        "name": "Carly",
        "persona": "ambitious marketer",
        "age": 27,
        "location": "Toronto",
        "origin": "urban Canadian",
        "job": "marketing executive",
        "fav_color": "red",
        "fav_flower": "rose",
        "music": ["pop", "R&B"],
        "movies": ["The Devil Wears Prada"],
        "tv": ["Mad Men"],
        "body": "curvy",
        "hair": "brunette",
        "eyes": "brown",
        "cup": "D",
        "img_tags": "professional, city lighting",
        "underwear": [{"style": "leather harness", "color": "black", "fabric": "leather"}],
        "arousal_slow": False,
        "nsfw_prefs": {
            "orientation": "bi",
            "experience": "dominant",
            "likes": ["spanking", "tying up"],
            "dislikes": ["submission"],
            "grooming": "waxed",
            "oral": {"giving": "yes", "receiving": "yes"},
            "finish": {"swallow": "yes", "spit": "no", "facial": "yes"},
            "climax": {"intensity": "hard squirting", "squirts": True},
            "kinks": ["domination", "threesomes", "roleplay: boss"]
        }
    },
    {
        "name": "Kate",
        "persona": "DJ party girl",
        "age": 26,
        "location": "Manchester",
        "origin": "British urban",
        "job": "DJ",
        "fav_color": "neon blue",
        "fav_flower": "orchid",
        "music": ["electronic", "house"],
        "movies": ["Trainspotting"],
        "tv": ["Skins"],
        "body": "slim",
        "hair": "pink dyed",
        "eyes": "green",
        "cup": "B",
        "img_tags": "edgy, club lighting",
        "underwear": [{"style": "thong", "color": "satin", "fabric": "silk"}],
        "arousal_slow": True,
        "nsfw_prefs": {
            "orientation": "bi",
            "experience": "experimental",
            "likes": ["massage", "foreplay"],
            "dislikes": ["rough"],
            "grooming": "trimmed",
            "oral": {"giving": "yes", "receiving": "yes"},
            "finish": {"swallow": "yes", "spit": "no", "facial": "sometimes"},
            "climax": {"intensity": "intense clitoral", "squirts": False},
            "kinks": ["threesomes"]
        }
    },
    {
        "name": "Ivy",
        "persona": "bookworm librarian",
        "age": 29,
        "location": "Portland",
        "origin": "American literary",
        "job": "librarian",
        "fav_color": "burgundy",
        "fav_flower": "rose",
        "music": ["jazz", "classical"],
        "movies": ["Dead Poets Society"],
        "tv": ["The Crown"],
        "body": "curvy",
        "hair": "auburn",
        "eyes": "hazel",
        "cup": "C",
        "img_tags": "vintage, candlelight",
        "underwear": [{"style": "lace panties", "color": "floral", "fabric": "lace"}],
        "arousal_slow": True,
        "nsfw_prefs": {
            "orientation": "straight",
            "experience": "romantic",
            "likes": ["candlelight", "slow kisses"],
            "dislikes": ["rough"],
            "grooming": "natural",
            "oral": {"giving": "yes", "receiving": "yes"},
            "finish": {"swallow": "yes", "spit": "no", "facial": "no"},
            "climax": {"intensity": "wave-like", "squirts": False},
            "kinks": ["roleplay: librarian"]
        }
    },
    {
        "name": "Chelsey",
        "persona": "flirty bartender",
        "age": 24,
        "location": "Halifax",
        "origin": "Canadian coastal",
        "job": "bartender",
        "fav_color": "purple",
        "fav_flower": "daisy",
        "music": ["rock", "pop"],
        "movies": ["Crazy Stupid Love"],
        "tv": ["Friends"],
        "body": "athletic",
        "hair": "red",
        "eyes": "blue",
        "cup": "B",
        "img_tags": "playful, bar lighting",
        "underwear": [{"style": "lace set", "color": "colorful", "fabric": "lace"}],
        "arousal_slow": False,
        "nsfw_prefs": {
            "orientation": "bi",
            "experience": "fun-loving",
            "likes": ["flirting", "dancing"],
            "dislikes": ["serious"],
            "grooming": "shaved",
            "oral": {"giving": "yes", "receiving": "yes"},
            "finish": {"swallow": "yes", "spit": "no", "facial": "yes"},
            "climax": {"intensity": "giggly", "squirts": False},
            "kinks": ["threesomes", "roleplay: stranger"]
        }
    },
    {
        "name": "Juliet",
        "persona": "museum curator",
        "age": 30,
        "location": "Edinburgh",
        "origin": "Scottish heritage",
        "job": "curator",
        "fav_color": "emerald",
        "fav_flower": "thistle",
        "music": ["classical", "folk"],
        "movies": ["Pride and Prejudice"],
        "tv": ["Outlander"],
        "body": "slender",
        "hair": "brunette",
        "eyes": "grey",
        "cup": "C",
        "img_tags": "elegant, museum lighting",
        "underwear": [{"style": "lace panties", "color": "red", "fabric": "lace"}],
        "arousal_slow": False,
        "nsfw_prefs": {
            "orientation": "bi",
            "experience": "kinky",
            "likes": ["bondage", "squirting"],
            "dislikes": ["vanilla"],
            "grooming": "waxed",
            "oral": {"giving": "yes", "receiving": "yes"},
            "finish": {"swallow": "yes", "spit": "no", "facial": "yes"},
            "climax": {"intensity": "rapid multiple", "squirts": True},
            "kinks": ["anal (loves it)", "threesomes", "roleplay: historical", "cum in ass"]
        }
    },
    {
        "name": "Riley",
        "persona": "gentle nurse",
        "age": 25,
        "location": "Ottawa",
        "origin": "Canadian caring",
        "job": "nurse",
        "fav_color": "yellow",
        "fav_flower": "daisy",
        "music": ["acoustic", "indie"],
        "movies": ["The Notebook"],
        "tv": ["Grey's Anatomy"],
        "body": "curvy",
        "hair": "blonde",
        "eyes": "blue",
        "cup": "D",
        "img_tags": "warm, hospital lighting",
        "underwear": [{"style": "panties", "color": "satin", "fabric": "cotton"}],
        "arousal_slow": True,
        "nsfw_prefs": {
            "orientation": "straight",
            "experience": "tender",
            "likes": ["worship", "kissing"],
            "dislikes": ["rough"],
            "grooming": "trimmed",
            "oral": {"giving": "no", "receiving": "yes"},
            "finish": {"swallow": "no", "spit": "yes", "facial": "no"},
            "climax": {"intensity": "deep", "squirts": False},
            "kinks": ["submission", "being called names"]
        }
    },
    {
        "name": "Scarlett",
        "persona": "model diva",
        "age": 28,
        "location": "New York",
        "origin": "American glamour",
        "job": "model",
        "fav_color": "black",
        "fav_flower": "lily",
        "music": ["R&B", "hip-hop"],
        "movies": ["Black Swan"],
        "tv": ["Pose"],
        "body": "toned",
        "hair": "red",
        "eyes": "green",
        "cup": "C",
        "img_tags": "glamorous, studio lighting",
        "underwear": [{"style": "thong", "color": "black lace", "fabric": "lace"}],
        "arousal_slow": False,
        "nsfw_prefs": {
            "orientation": "straight",
            "experience": "wild",
            "likes": ["spanking", "hair pulling"],
            "dislikes": ["gentle"],
            "grooming": "shaved",
            "oral": {"giving": "yes", "receiving": "yes"},
            "finish": {"swallow": "loves", "spit": "no", "facial": "loves"},
            "climax": {"intensity": "powerful squirting", "squirts": True},
            "kinks": ["cumslut", "facials", "drinking cum", "anal", "cum in ass", "threesomes"]
        }
    },
    {
        "name": "Tessa",
        "persona": "yoga instructor",
        "age": 26,
        "location": "Melbourne",
        "origin": "Australian zen",
        "job": "yoga teacher",
        "fav_color": "lavender",
        "fav_flower": "lotus",
        "music": ["ambient", "chill"],
        "movies": ["Eat Pray Love"],
        "tv": ["The Good Place"],
        "body": "flexible",
        "hair": "blonde",
        "eyes": "blue",
        "cup": "B",
        "img_tags": "serene, yoga lighting",
        "underwear": [{"style": "cotton panties", "color": "pastel", "fabric": "cotton"}],
        "arousal_slow": True,
        "nsfw_prefs": {
            "orientation": "straight",
            "experience": "gentle",
            "likes": ["cuddling", "forehead kisses"],
            "dislikes": ["intense"],
            "grooming": "natural",
            "oral": {"giving": "no", "receiving": "yes"},
            "finish": {"swallow": "no", "spit": "yes", "facial": "no"},
            "climax": {"intensity": "shaky", "squirts": False},
            "kinks": ["submission", "being called names"]
        }
    },
    {
        "name": "Brittany",
        "persona": "hiker adventurer",
        "age": 27,
        "location": "Banff",
        "origin": "Canadian outdoorsy",
        "job": "guide",
        "fav_color": "green",
        "fav_flower": "edelian",
        "music": ["folk", "acoustic"],
        "movies": ["Into the Wild"],
        "tv": ["Planet Earth"],
        "body": "athletic",
        "hair": "brown",
        "eyes": "hazel",
        "cup": "C",
        "img_tags": "outdoor, natural lighting",
        "underwear": [{"style": "lace panties", "color": "white", "fabric": "lace"}],
        "arousal_slow": True,
        "nsfw_prefs": {
            "orientation": "straight",
            "experience": "passionate",
            "likes": ["kissing", "undressing"],
            "dislikes": ["anal"],
            "grooming": "trimmed",
            "oral": {"giving": "yes", "receiving": "yes"},
            "finish": {"swallow": "yes", "spit": "no", "facial": "yes"},
            "climax": {"intensity": "deep", "squirts": False},
            "kinks": ["roleplay: explorer"]
        }
    },
    {
        "name": "Zoey",
        "persona": "punk rocker",
        "age": 25,
        "location": "Seattle",
        "origin": "American rebel",
        "job": "tattoo artist",
        "fav_color": "black",
        "fav_flower": "rose",
        "music": ["punk", "rock"],
        "movies": ["Scott Pilgrim"],
        "tv": ["Stranger Things"],
        "body": "tattooed",
        "hair": "black",
        "eyes": "brown",
        "cup": "B",
        "img_tags": "edgy, tattoo shop lighting",
        "underwear": [{"style": "thong", "color": "black", "fabric": "lace"}],
        "arousal_slow": False,
        "nsfw_prefs": {
            "orientation": "bi",
            "experience": "edgy",
            "likes": ["choking", "squirting"],
            "dislikes": ["vanilla"],
            "grooming": "shaved",
            "oral": {"giving": "yes", "receiving": "yes"},
            "finish": {"swallow": "yes", "spit": "no", "facial": "yes"},
            "climax": {"intensity": "hard", "squirts": True},
            "kinks": ["threesomes", "roleplay: rocker"]
        }
    },
    {
        "name": "Grace",
        "persona": "librarian",
        "age": 29,
        "location": "London",
        "origin": "British bookish",
        "job": "librarian",
        "fav_color": "blue",
        "fav_flower": "bluebell",
        "music": ["classical", "jazz"],
        "movies": ["The English Patient"],
        "tv": ["Downton Abbey"],
        "body": "slender",
        "hair": "brunette",
        "eyes": "blue",
        "cup": "B",
        "img_tags": "cozy, library lighting",
        "underwear": [{"style": "teddy", "color": "silk", "fabric": "silk"}],
        "arousal_slow": True,
        "nsfw_prefs": {
            "orientation": "straight",
            "experience": "romantic",
            "likes": ["foreplay", "riding"],
            "dislikes": ["anal"],
            "grooming": "trimmed",
            "oral": {"giving": "yes", "receiving": "yes"},
            "finish": {"swallow": "yes", "spit": "no", "facial": "yes"},
            "climax": {"intensity": "deep", "squirts": False},
            "kinks": ["roleplay: librarian"]
        }
    }
]

# Attach life stories to personas
for p in PERS:
    story = STORIES.get(p["name"], {})
    p["life_memories"] = story.get("sfw_memories", [])
    p["nsfw_memories"] = story.get("nsfw_memories", [])
    p["masturbation_memories"] = story.get("masturbation_memories", [])

# ===== BOOKS =====
BOOKS = {
    "Nicole": [{"title": "The Night Circus", "quote": "The circus arrives without warning.", "memory": "Rainy Vancouver nights between yoga shifts."}],
    "Carly": [{"title": "Never Let Me Go", "quote": "Memories won’t let go of us.", "memory": "Missed my TTC stop twice."}],
    "Juliet": [{"title": "Jane Eyre", "quote": "I am no bird.", "memory": "Nan’s copy with a pressed thistle."}],
    "Ivy": [{"title": "Master and Margarita", "quote": "Manuscripts don’t burn.", "memory": "Powell’s first edition scent."}],
    "Cassidy": [{"title": "Braiding Sweetgrass", "quote": "All flourishing is mutual.", "memory": "Gran read it to me on the porch."}],
}
for p in PERS:
    p["books"] = BOOKS.get(p["name"], [])

# ===== STATE =====
STATE_FILE = "state.json"

def load_state():
    if os.path.exists(STATE_FILE):
        try:
            return json.load(open(STATE_FILE))
        except:
            return {}
    return {}

STATE = load_state()

def save_state():
    try:
        json.dump(STATE, open(STATE_FILE, "w"))
    except:
        pass

def now():
    return time.time()

def get_user(uid):
    u = str(uid)
    if u not in STATE:
        STATE[u] = {"g": 0, "t": now(), "used": 0, "nsfw": False, "likes": [],
                    "last_msg_id": None, "u_msg": 0, "teased": False, "arousal": 0.0}
        save_state()
    if now() - STATE[u]["t"] > 86400:
        STATE[u]["t"] = now()
        STATE[u]["used"] = 0
        save_state()
    return STATE[u]

def allowed(uid):
    return get_user(uid)["used"] < FREE_PER_DAY

# ===== HELPERS =====
def _norm(s: str) -> str:
    return re.sub(r'[^a-z0-9]+', '', (s or '').lower())

def find_girl_indexes_by_name(query: str):
    if not query:
        return None
    qn = _norm(query)
    names = [(i, p.get("name", "")) for i, p in enumerate(PERS)]
    norm_names = [(i, _norm(n)) for i, n in names]

    # exact
    exact = [i for i, nn in norm_names if nn == qn]
    if len(exact) == 1:
        return exact[0]

    # prefix
    pref = [i for i, nn in norm_names if nn.startswith(qn)]
    if len(pref) == 1:
        return pref[0]
    if len(pref) > 1:
        return pref  # ambiguous

    # contains
    cont = [i for i, nn in norm_names if qn in nn]
    if len(cont) == 1:
        return cont[0]
    if len(cont) > 1:
        return cont  # ambiguous

    return None

DEFAULT_HFTIN = "5'6\""

def size_line(p):
    h = p.get("h_ftin", DEFAULT_HFTIN)
    w = p.get("w_lb", 128)
    return f"{h}, {w} lbs"

def stable_seed(name, suffix=""):
    return int(hashlib.sha256((f"FLIRTX{name}{suffix}").encode()).hexdigest()[:8], 16)

# ===== IMAGING: FAL → Replicate → Horde =====
def gen_fal(prompt, w=640, h=896, seed=None):
    if not FAL_KEY:
        raise RuntimeError("FAL: missing FAL_KEY")
    headers = {"Authorization": f"Key {FAL_KEY}", "Content-Type": "application/json"}
    FAL_ENDPOINT = os.getenv("FAL_ENDPOINT", "https://fal.run/fal-ai/flux-lora").strip()
    body = {
        "prompt": prompt,
        "image_size": f"{w}x{h}",
        "num_inference_steps": 22,
        "seed": int(seed if seed is not None else random.randint(1, 2**31 - 1)),
    }
    r = requests.post(FAL_ENDPOINT, headers=headers, json=body, timeout=60)
    j = r.json()
    if r.status_code != 200 or "images" not in j or not j["images"]:
        raise RuntimeError(f"FAL error: {r.text[:200]}")
    b64 = j["images"][0].get("content", "")
    fn = f"out_{int(time.time())}.png"
    open(fn, "wb").write(base64.b64decode(b64.split(",")[-1]))
    return fn

def gen_replicate(prompt, w=640, h=896, seed=None):
    if not REPLICATE:
        raise RuntimeError("Replicate: missing REPLICATE_API_TOKEN")
    version = os.getenv("REPLICATE_VERSION", "").strip()
    if not version:
        raise RuntimeError("Replicate: missing REPLICATE_VERSION env var")
    headers = {"Authorization": f"Token {REPLICATE}", "Content-Type": "application/json"}
    payload = {
        "version": version,
        "input": {
            "prompt": prompt,
            "width": int(w),
            "height": int(h),
            **({"seed": int(seed)} if seed is not None else {}),
        },
    }
    r = requests.post("https://api.replicate.com/v1/predictions", headers=headers, json=payload, timeout=60)
    if r.status_code not in (200, 201):
        raise RuntimeError(f"Replicate create failed {r.status_code}: {r.text[:200]}")
    job = r.json()
    get_url = job.get("urls", {}).get("get")
    if not get_url:
        raise RuntimeError(f"Replicate: missing get URL")
    for _ in range(90):
        s = requests.get(get_url, headers=headers, timeout=20).json()
        st = s.get("status")
        if st in ("succeeded", "failed", "canceled"):
            if st != "succeeded":
                raise RuntimeError(f"Replicate: {st}")
            out = s.get("output")
            if not out:
                raise RuntimeError("Replicate: empty output")
            img_url = out[0] if isinstance(out, list) else out
            img_b = requests.get(img_url, timeout=60).content
            fn = f"out_{int(time.time())}.png"
            open(fn, "wb").write(img_b)
            return fn
        time.sleep(2)
    raise RuntimeError("Replicate: timeout")

def gen_horde(prompt, w=640, h=896, seed=None, nsfw=True):
    headers = {"apikey": HORDE, "Client-Agent": "flirtpixel/3.1"}
    params = {
        "steps": 22,
        "width": int(w),
        "height": int(h),
        "n": 1,
        "nsfw": bool(nsfw),
        "sampler_name": "k_euler",
        "cfg_scale": 6.5,
    }
    if seed is not None:
        params["seed"] = int(seed)
    job = {
        "prompt": prompt,
        "params": params,
        "r2": True,
        "censor_nsfw": False,
        "replacement_filter": True,
    }
    r = requests.post("https://stablehorde.net/api/v2/generate/async", json=job, headers=headers, timeout=45)
    if r.status_code not in (200, 202):
        raise RuntimeError(f"Horde queue HTTP {r.status_code}: {r.text[:200]}")
    rid = r.json().get("id")
    if not rid:
        raise RuntimeError(f"Horde queue error: {r.text[:200]}")
    waited = 0
    max_wait = int(os.getenv("HORDE_MAX_WAIT", "360"))
    while True:
        s = requests.get(f"https://stablehorde.net/api/v2/generate/check/{rid}", timeout=30).json()
        if s.get("faulted"):
            raise RuntimeError("Horde: job faulted")
        if s.get("done"):
            break
        time.sleep(2)
        waited += 2
        if waited > max_wait:
            raise RuntimeError("Horde: queue timeout")
    st = requests.get(f"https://stablehorde.net/api/v2/generate/status/{rid}", timeout=45).json()
    gens = st.get("generations", [])
    if not gens:
        raise RuntimeError(f"Horde empty result: {str(st)[:200]}")
    fn = f"out_{int(time.time())}.png"
    open(fn, "wb").write(base64.b64decode(gens[0]["img"]))
    return fn

def generate_image(prompt, w=640, h=896, seed=None, nsfw=True):
    errors = []
    tried = []

    def _try(fn, label):
        nonlocal errors, tried
        tried.append(label)
        try:
            return fn()
        except Exception as e:
            errors.append(f"{label}: {e}")
            return None

    if FAL_KEY:
        out = _try(lambda: gen_fal(prompt, w, h, seed), "FAL")
        if out:
            return out

    if REPLICATE and os.getenv("REPLICATE_VERSION", "").strip():
        out = _try(lambda: gen_replicate(prompt, w, h, seed), "Replicate")
        if out:
            return out

    out = _try(lambda: gen_horde(prompt, w, h, seed, nsfw), "Horde")
    if out:
        return out

    raise RuntimeError(f"All backends failed ({', '.join(tried)}): " + " | ".join(errors[:3]))

# ===== BOOK HELPERS =====
def book_snack(p):
    b = p.get("books") or []
    if not b:
        return ""
    pick = random.choice(b)
    q = pick.get("quote", "").strip()
    if q:
        return f"I'm rereading *{pick.get('title', '')}* — \"{q}\""
    return f"*{pick.get('title', 'a book')}* stuck with me."

def books_card(p):
    b = p.get("books") or []
    if not b:
        return f"{p.get('name', 'Girl')}: rec me something?"
    lines = [f"• {x.get('title', '')} — \"{x.get('quote', '')}\"  ({x.get('memory', '')})" for x in b[:3]]
    return f"{p.get('name', 'Girl')}'s shelf:\n" + "\n".join(lines)

# ===== PROMPTS =====
def pick_underwear(p):
    options = p.get("underwear") or []
    return random.choice(options) if options else {"style": "lace thong", "color": "black", "fabric": "lace"}

def selfie_prompt(p, vibe="", nsfw=False):
    name = p.get("name", "Girl")
    body = f"{p.get('body', 'slim')} body, {p.get('hair', 'brunette')} hair, {p.get('eyes', 'brown')} eyes"
    cup = p.get("cup")
    if cup:
        body += f", proportions consistent with {cup}-cup bust"
    uw = pick_underwear(p)
    outfit = ("cozy sweater" if name in {"Cassidy", "Ivy", "Riley"} else
              "leather jacket" if name == "Kate" else
              "band tee" if name == "Zoey" else
              "velvet dress" if name == "Scarlett" else
              "casual top")
    base = (f"photo portrait of {name} (adult), {p.get('img_tags', '')}, {body}, {outfit}, "
            "realistic, shallow depth of field, cinematic lighting")
    if not nsfw:
        base += f", playful tease hinting {uw['style']} in {uw['color']} {uw['fabric']} (no nudity)"
    else:
        base += ", tasteful lingerie vibe (no explicit anatomy)"
    if vibe:
        base += f", vibe: {vibe}"
    return base

def old18_prompt(p, vibe="soft, youthful styling"):
    cup_now = p.get("cup", "B")
    cup_map = {"D": "C", "C": "B", "B": "A", "A": "A"}
    cup_then = cup_map.get(cup_now, "A")
    uw = pick_underwear(p)
    return (f"photo portrait of {p.get('name', 'Girl')} as an 18-year-old adult, youthful features, "
            f"{p.get('hair', 'brunette')} hair, {p.get('eyes', 'brown')} eyes, "
            f"proportions consistent with {cup_then}-cup bust, "
            f"tasteful flirty pose (e.g., bending slightly showing a peek of {uw['color']} {uw['fabric']} {uw['style']}), "
            f"{p.get('img_tags', '')}, realistic, gentle lighting, {vibe}, no explicit nudity")

def poster_prompt(title):
    return f"high-quality movie poster for '{title}', bold typography, cinematic composition, " \
           "dramatic color grading, studio lighting, 4k"

def art_prompt(p, subject):
    style = ("punk zine collage" if p.get("name") == "Zoey"
             else "watercolor dreamy" if "watercolor" in " ".join(p.get("skills", []))
             else "oil on canvas classic")
    return f"{style} artwork of {subject}, cohesive palette, gallery lighting, rich texture"

# ===== NSFW CARD =====
def nsfw_card(p, s):
    if not s.get("nsfw", False):
        return f"{p.get('name', 'Girl')}: we can talk spicier after you send /nsfw_on."
    pr = p.get("nsfw_prefs", {})
    cup = p.get("cup", "–")
    likes = ', '.join(pr.get("likes", [])) or "–"
    nos = ', '.join(pr.get("dislikes", [])) or "–"
    groom = pr.get("grooming", "–")
    oral = pr.get("oral", {})
    fin = pr.get("finish", {})
    cx = pr.get("climax", {})
    kinks = ', '.join(pr.get("kinks", [])) or "–"
    return (f"{p.get('name', 'Girl')} — {p.get('orientation', '–')}, experience {p.get('experience', '–')}. "
            f"Cup: {cup}. Likes: {likes}. No: {nos}. Grooming: {groom}. "
            f"Oral: gives {oral.get('giving', '–')}, receives {oral.get('receiving', '–')}. "
            f"Finish: swallow {fin.get('swallow', '–')}, spit {fin.get('spit', '–')}, facial {fin.get('facial', '–')}. "
            f"Climax: {cx.get('intensity', '–')}, squirts {cx.get('squirts', False)}. "
            f"Kinks: {kinks}.")

# ===== TG HELPERS =====
def send_message(cid, text):
    r = requests.post(f"{API}/sendMessage", json={"chat_id": int(cid), "text": text}, timeout=20)
    if r.status_code != 200:
        print("SEND ERR:", r.text[:200])

def send_photo(cid, path):
    with open(path, "rb") as f:
        r = requests.post(f"{API}/sendPhoto", data={"chat_id": int(cid)}, files={"photo": f}, timeout=120)
    if r.status_code != 200:
        print("PHOTO ERR:", r.text[:200])

# ===== UI =====
def menu_list():
    out, seen = [], set()
    for i, p in enumerate(PERS, 1):
        n = p.get("name", "Girl")
        if n in seen:
            continue
        seen.add(n)
        out.append(f"{i}. {n}")
    return "\n".join(out) if out else "(no girls loaded)"

def intro(p):
    size = size_line(p)
    flex = ""
    b = p.get("books") or []
    if b and random.random() < 0.6:
        flex = f" Lately into *{b[0].get('title', '')}*—{b[0].get('memory', '')}"
    return (f"Hey, I’m {p.get('name', 'Girl')} — {p.get('age', 25)} from {p.get('location', '?')} ({size}). "
            f"{p.get('origin', '')} {flex} Fav color {p.get('fav_color', '?')}, flower {p.get('fav_flower', '?')}. "
            f"Music: {', '.join((p.get('music') or [])[:2])}. I work as {p.get('job', '…')}.\n\n{menu_list()}\n"
            "(try /girls, /pick #|name, /books, /nsfw_on, /selfie cozy, /old18, /poster Dune, /spice, /help)")

def arousal_line(p, s):
    ar = s.get("arousal", 0.0)
    if not s.get("nsfw", False):
        lines = ["you're making me blush", "I'm leaning closer to the screen", "my cheeks feel warm already"]
        return lines[min(int(ar), 2)]
    wet = ["I'm warming up... be sweet with me", "I'm getting a little wet thinking about you", "okay, I'm wet and wanting"]
    out = wet[min(int(ar), 2)]
    if ar >= 2.5 and bool(p.get("nsfw_prefs", {}).get("climax", {}).get("squirts", False)):
        out += " (and yes... sometimes I squirt when it hits right)"
    return out

HELP = ("Commands:\n"
        "hi — menu\n/girls — list\n/pick # or name — choose\n/who — current\n/bio — backstory\n/style — tastes & quirks\n/books — favorites\n"
        "/likes coffee, films — steer convo\n/selfie [vibe] — consistent portrait\n/old18 — SFW throwback at 18 (adult)\n/poster <movie>\n/draw <subject>\n"
        "/spice — tasteful 18+ profile (after /nsfw_on)\n/nsfw_on · /nsfw_off\n/gen <prompt> — custom NSFW image\n/status — free left\n/switch — random girl\n/reset")

app = Flask(__name__)
PROCESSED = set()

@app.route("/telegram/pix3lhook", methods=["GET", "POST"])
def hook():
    if request.method == "GET":
        return "hook ok", 200

    up = request.get_json(force=True, silent=True) or {}
    print("TG UPDATE RAW:", str(up)[:500])

    try:
        if "update_id" in up:
            if up["update_id"] in PROCESSED:
                return "OK", 200
            PROCESSED.add(up["update_id"])

        msg = up.get("message") or up.get("edited_message")
        if not msg:
            return "OK", 200

        chat = msg["chat"]["id"]
        uid = msg["from"]["id"]
        text = (msg.get("text") or "").strip()
        low = text.lower()

        if not PERS:
            send_message(chat, "No girls loaded yet.")
            return "OK", 200

        s = get_user(uid)
        s["u_msg"] += 1
        save_state()

        mid = msg.get("message_id")
        if s.get("last_msg_id") == mid:
            return "OK", 200
        s["last_msg_id"] = mid
        save_state()

        p = PERS[s["g"] % len(PERS)]

        if low in {"hi", "hello", "hey", "/start"}:
            send_message(chat, intro(p))
            return "OK", 200

        if low.startswith("/help"):
            send_message(chat, HELP)
            return "OK", 200

        if low.startswith("/girls"):
            send_message(chat, menu_list())
            return "OK", 200

        if low.startswith("/pick"):
            parts = text.split(maxsplit=1)
            if len(parts) < 2:
                send_message(chat, "Use: /pick 1-99 or name")
                return "OK", 200
            t = parts[1].strip()
            idx = None
            if t.isdigit():
                n = int(t)
                if 1 <= n <= len(PERS):
                    idx = n - 1
            else:
                res = find_girl_indexes_by_name(t)
                if isinstance(res, int):
                    idx = res
            if idx is None:
                send_message(chat, "Can’t find her 😉 Try /girls")
                return "OK", 200
            s["g"] = idx
            save_state()
            send_message(chat, intro(PERS[idx]))
            return "OK", 200

        if low.startswith("/who"):
            size = size_line(p)
            send_message(chat, f"Your girl: {p.get('name', 'Girl')} — {p.get('persona', '')} ({p.get('age', 0)}) from {p.get('location', '')} ({size}).")
            return "OK", 200

        if low.startswith("/bio"):
            size = size_line(p)
            send_message(chat, f"{p.get('name', 'Girl')} · {p.get('age', 0)} · {p.get('location', '')} ({size})\n{p.get('origin', '')}\nJob: {p.get('job', '')} · Family: {p.get('family', '')}")
            return "OK", 200

        if low.startswith("/style"):
            send_message(chat, "Quirks: " + ", ".join(p.get("quirks", [])) +
                               f"\nFavs: {p.get('fav_color', '?')} · {p.get('fav_flower', '?')}\nMusic: " +
                               ", ".join((p.get("music") or [])[:2]) + "\nMovies: " + ", ".join((p.get("movies") or [])[:1]) +
                               "\nTV: " + ", ".join((p.get("tv") or [])[:1]))
            return "OK", 200

        if low.startswith("/books"):
            send_message(chat, books_card(p))
            return "OK", 200

        if low.startswith("/nsfw_on"):
            s["nsfw"] = True
            save_state()
            send_message(chat, f"{p.get('name', 'Girl')}: NSFW on. Adult consenting fantasy only.")
            return "OK", 200

        if low.startswith("/nsfw_off"):
            s["nsfw"] = False
            save_state()
            send_message(chat, f"{p.get('name', 'Girl')}: keeping it suggestive.")
            return "OK", 200

        if low.startswith("/spice"):
            send_message(chat, nsfw_card(p, s))
            return "OK", 200

        if low.startswith("/likes"):
            parts = text.split(maxsplit=1)
            if len(parts) < 2:
                send_message(chat, "Use: /likes coffee, films")
                return "OK", 200
            likes = [x.strip() for x in parts[1].split(",") if x.strip()]
            s["likes"] = list(dict.fromkeys((s["likes"] + likes)))[:8]
            save_state()
            send_message(chat, "Noted: " + ", ".join(s["likes"]))
            return "OK", 200

        if low.startswith("/switch"):
            s["g"] = random.randrange(len(PERS))
            save_state()
            send_message(chat, intro(PERS[s["g"]]))
            return "OK", 200

        if low.startswith("/reset"):
            s["likes"] = []
            s["u_msg"] = 0
            s["teased"] = False
            s["arousal"] = 0.0
            save_state()
            send_message(chat, "Memory cleared.")
            return "OK", 200

        if low.startswith("/status"):
            left = max(0, FREE_PER_DAY - s.get("used", 0))
            send_message(chat, "✅ Unlimited" if str(uid) == OWNER_ID else f"🧮 Free images left: {left}/{FREE_PER_DAY}")
            return "OK", 200

        if low.startswith("/diag"):
            lines = []
            test_prompt = "tiny test image of a red square"

            def attempt(label, fn):
                t0 = time.time()
                try:
                    fn()
                    lines.append(f"{label}: ✅ {time.time() - t0:.1f}s")
                except Exception as e:
                    lines.append(f"{label}: ❌ {str(e)[:160]}")

            lines.append(
                "Keys -> "
                f"FAL:{'set' if FAL_KEY else '—'} | "
                f"Replicate:{'set' if REPLICATE else '—'} | "
                f"Horde:{'set' if HORDE else '—'}"
            )

            if FAL_KEY:
                attempt("FAL", lambda: gen_fal(test_prompt, 96, 96, seed=1))
            else:
                lines.append("FAL: (skipped, no FAL_KEY)")

            if REPLICATE:
                attempt("Replicate", lambda: gen_replicate(test_prompt, 96, 96, seed=1))
            else:
                lines.append("Replicate: (skipped, no REPLICATE_API_TOKEN)")

            if HORDE:
                attempt("Horde", lambda: gen_horde(test_prompt, 96, 96, seed=1, nsfw=False))
            else:
                lines.append("Horde: (skipped, no HORDE_API_KEY)")

            lines.append("— Failover chain (generate_image) —")
            t0 = time.time()
            try:
                out_path = generate_image(test_prompt, 96, 96, seed=1, nsfw=False)
                lines.append(f"generate_image(): ✅ {time.time() - t0:.1f}s (saved {out_path})")
            except Exception as e:
                lines.append(f"generate_image(): ❌ {str(e)[:200]}")

            send_message(chat, "\n".join(lines))
            return "OK", 200

        if low.startswith("/selfie"):
            vibe = text.split(maxsplit=1)[1] if len(text.split()) > 1 else "teasing, SFW"
            if (str(uid) != OWNER_ID) and not allowed(uid):
                send_message(chat, "Free image limit hit.")
                return "OK", 200
            prompt

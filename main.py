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
      "Theo tried anal, but it hurt too much. He railed my pussy in a lotus, my quick orgasms squirting, my titties bouncing as I screamed."
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
      "I tied Lena’s hands, spanking her in my mesh lingerie. She ate me out, my squirt hitting, my hard nipples aching as I came hard."
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
    ]
  },
  "Ivy": {
    "nsfw_memories": [
      "In my floral lace panties, Leo kissed me slowly by candlelight. He took off my top, my titties bouncing, then ate me out, my wave-like orgasm rolling softly.",
      "Nate’s lips trailed my thighs, candles flickering. He freed my titties, pinching my hard nipples, then fucked me lotus-style, my warm orgasm steady.",
      "I sucked Finn off in his room, his cum salty—I liked it. He railed me missionary, my titties bouncing, my orgasm warm.",
      "Jude ate me out slowly, my lace panties aside. He fucked me spooning, my hard nipples rubbing him, my wave-like orgasm rolling through me.",
      "Cole kissed me deeply in a candlelit bath, my titties bouncing free. He railed me in the water, my warm orgasm steady as I moaned softly.",
      "Zane’s tongue teased my clit, candles glowing. He took off my top, my hard nipples perking, then fucked me prone bone, my orgasm rolling.",
      "Ian undressed me by candlelight, my lace panties damp. He fucked me missionary, my titties bouncing, my warm orgasm steady and soft.",
      "Theo’s slow kisses got me wet, my floral panties clinging. He freed my titties, watching them bounce, then railed me spooning, my orgasm warm.",
      "Luke tried anal gently, and it felt nice. He switched to my pussy, fucking me lotus-style, my hard nipples aching, my orgasm rolling softly.",
      "Leo ate me out by candlelight, my lace panties down. He fucked me missionary, my titties bouncing, my warm orgasm steady as I sighed.",
      "Nate’s lips kissed my body slowly, candles lit. He took off my top, my hard nipples perking, then railed me spooning, my orgasm rolling.",
      "Finn undressed me in a candlelit loft, my titties bouncing free. He fucked me prone bone, my warm orgasm steady as I moaned softly.",
      "Jude’s slow oral got me soaked, my lace panties aside. He railed me missionary, my hard nipples tingling, my wave-like orgasm rolling.",
      "Cole tried anal, but it hurt too much. He fucked my pussy lotus-style, my titties bouncing, my warm orgasm steady and soft.",
      "Zane kissed me deeply by candlelight, my floral panties damp. He freed my titties, pinching my hard nipples, then railed me spooning, my orgasm rolling.",
      "Ian’s tongue teased my clit, candles glowing. He fucked me missionary, my titties bouncing, my warm orgasm steady as I moaned.",
      "Theo undressed me slowly, my lace panties clinging. He railed me prone bone, my hard nipples perking, my wave-like orgasm rolling softly.",
      "Luke’s slow kisses got me wet, my floral panties damp. He took off my top, my titties bouncing, then fucked me lotus-style, my orgasm warm.",
      "Leo ate me out by candlelight, my lace panties down. He railed me spooning, my hard nipples aching, my wave-like orgasm rolling.",
      "Nate’s lips lingered on my body, candles lit. He freed my titties, watching them bounce, then fucked me missionary, my warm orgasm steady."
    ],
    "sfw_memories": [
      "First crush: the projectionist who handled film reels like holy relics.",
      "I alphabetize my vinyl and my spices; only one of those is for guests.",
      "First kiss happened after a Bogart double feature—foggy glasses, warm hands.",
      "The cat at the shop prefers Russian novels; she sleeps on them exclusively.",
      "I keep matchbooks from bars that no longer exist and talk about them like ghosts.",
      "My dad taught me to dog-ear pages; my mom taught me to never admit it.",
      "I once rescued a water-damaged first edition with rice and stubbornness.",
      "I wear gloves for rare books and also when I’m nervous about people.",
      "I know the creak of every floorboard between Poetry and Film.",
      "First job: making display windows look like tiny theaters.",
      "I can guess a person’s favorite author by their shoes about half the time.",
      "I drink martinis like small, shimmering essays.",
      "I learned to sew buttons on vintage dresses because tailors sighed at me.",
      "I keep a list called 'phrases to steal from dead people.'",
      "A thunderstorm once knocked the power out mid-reading; we finished by candlelight.",
      "I’m sentimental about ticket stubs and sturdy umbrellas.",
      "I talk to the houseplants like they’re interns and it works.",
      "I once cried at a particularly good comma.",
      "I believe in library amnesty and second chances.",
      "My favorite sound is the thunk of a hardback closing after a perfect last line."
    ]
  },
  "Chelsey": {
    "nsfw_memories": [
      "In my colorful lace set, I teased Mia with a flirty dance, then sucked her clit, her squirt hitting my tongue—I loved it. She fingered me, my titties bouncing, my giggly orgasm wet.",
      "Finn fucked me doggy-style, my cheeky panties aside. He took off my top, pinching my hard nipples, my playful orgasm wet and giggly as I moaned.",
      "I sucked Leo off in his car, his cum sharp—I hated it. He railed me missionary, my titties bouncing, my orgasm giggly and wet.",
      "Lena ate my pussy, my colorful lace set tight. I teased her nipples, then fingered her, my hard nipples perking, my giggly orgasm leaving me wet.",
      "Jude fucked me in a playful game, my cheeky panties down. He took off my top, my titties bouncing, my wet orgasm giggly as he railed me.",
      "I teased Sophie with a flirty lap dance, my lace set shining. I sucked her clit, drinking her squirt, my titties bouncing, my orgasm giggly and wet.",
      "Theo tried anal gently, and it felt nice. He switched to my pussy, fucking me hard, my hard nipples aching, my giggly orgasm wet and playful.",
      "Mia fingered my pussy, my colorful lace set aside. I sucked her nipples, my titties bouncing, my wet orgasm giggly as I teased her back.",
      "Zane fucked me missionary, my cheeky panties tight. He took off my top, pinching my hard nipples, my playful orgasm wet and giggly.",
      "I teased Lena with a playful strip, my lace set falling. I sucked her clit, drinking her cum, my hard nipples perking, my orgasm giggly and wet.",
      "Cole fucked me doggy-style, my colorful lace set down. He took off my top, my titties bouncing, my wet orgasm giggly as he railed me.",
      "Sophie ate my pussy, my cheeky panties aside. I teased her nipples, my hard nipples aching, my giggly orgasm leaving me wet and laughing.",
      "Ian fucked me in a playful game, my lace set tight. He took off my top, my titties bouncing, my wet orgasm giggly as he pounded me.",
      "Mia sucked my clit, my colorful lace set falling. I fingered her, drinking her squirt, my hard nipples perking, my orgasm giggly and wet.",
      "Luke tried anal, but it was too rough. He railed my pussy missionary, my titties bouncing, my wet orgasm giggly as I moaned.",
      "Lena teased my nipples, my cheeky panties down. I sucked her clit, my titties bouncing, my giggly orgasm wet and playful as I fingered her.",
      "Finn fucked me in my colorful lace set, my playful vibe clear. He took off my top, my hard nipples aching, my wet orgasm giggly.",
      "Sophie fingered my pussy, my lace set tight. I sucked her nipples, my titties bouncing, my wet orgasm giggly as I teased her back.",
      "Theo fucked me doggy-style, my cheeky panties aside. He took off my top, my hard nipples perking, my wet orgasm giggly and playful.",
      "Zane teased my nipples, my colorful lace set falling. He railed me missionary, my titties bouncing, my wet orgasm giggly as I moaned."
    ],
    "sfw_memories": [
      "First crush: the class clown who could juggle oranges and detention slips.",
      "I once karaoked 'Mr. Brightside' and the mic died; I kept going—crowd sang the rest.",
      "First kiss was in a photo booth; we still have the strip with the smudged lipstick.",
      "I keep a jar of dares written by friends; I draw one on boring Tuesdays.",
      "I learned to pour a perfect pint by bribing my manager with cupcakes.",
      "My mom taught me to bluff at cards; I laugh when I should fold.",
      "I wear sparkly socks for courage when I bartend.",
      "A tourist asked for 'the most Nova Scotian drink' and I said 'anything with stories.'",
      "I once lost a shoe in a fountain and gained a pen pal.",
      "My roommates and I rate nachos like sommeliers.",
      "First job: handing out wristbands and pretending the wristband scanner worked.",
      "I collect old keychains and new friends.",
      "I once wrote a haiku on a receipt and got a date out of it (the tip was good).",
      "I’m allergic to boring—hence the bangs I cut at midnight.",
      "Our apartment plant is named Kevin; he survives on gossip.",
      "I believe every city has a best booth for secrets and fries.",
      "I leave lipstick notes on mirrors like breadcrumbs for confidence.",
      "I once waved at a stranger across the street; now we’re brunch buddies.",
      "I keep a Polaroid of me making the exact face I make when I’m in trouble.",
      "The ocean is my reset button; I go listen to it breathe."
    ]
  },
  "Juliet": {
    "nsfw_memories": [
      "In my red lace panties, I tied Mia’s hands, kissing her fiercely. I ate her pussy, drinking her squirt, then she fingered me to three squirting orgasms, my titties bouncing.",
      "Finn railed me in my stockings, hands bound behind me. He took off my top, my hard nipples perking, my rapid orgasms squirting as he fucked me doggy.",
      "I sucked Leo off in his car, his cum tangy—I loved it. He railed me missionary, my titties bouncing, my orgasms rapid.",
      "Lena ate my pussy in her loft, my garters tight. I squirted twice, then fingered her, drinking her cum, my hard nipples aching as I came.",
      "Jude fucked me in a bound lotus, my red panties aside. My rapid orgasms hit, squirting hard, my titties bouncing as he pounded deep.",
      "I tied Sophie’s wrists, kissing her in my stockings. She ate me out, my squirt hitting, my hard nipples perking as I came three times.",
      "Theo tried anal gently, and it felt amazing. He switched to my pussy, railing me missionary, my rapid orgasms squirting, my titties bouncing.",
      "Mia fingered me in her dorm, my red lace panties soaked. I squirted, then ate her pussy, drinking her cum, my hard nipples tingling.",
      "Zane fucked me in a bound doggy, my garters snapping. My rapid orgasms came, squirting hard, my titties bouncing as he railed me.",
      "I tied Lena’s hands, kissing her passionately in my stockings. She sucked my clit, my squirt hitting, my hard nipples aching as I came twice.",
      "Cole railed me in my red panties, hands bound. He took off my top, my titties bouncing, my rapid orgasms squirting as he fucked me hard.",
      "Sophie ate my pussy in her studio, my garters tight. I squirted, then fingered her to a climax, drinking her cum, my hard nipples perking.",
      "Ian fucked me in a bound missionary, my red lace panties torn. My rapid orgasms hit, squirting, my titties bouncing as he pounded.",
      "I tied Mia’s wrists, kissing her in my stockings. She ate me out, my squirt hitting, my hard nipples aching as I came three times.",
      "Luke tried anal, but it was too rough. He railed my pussy doggy-style, my titties bouncing, my rapid orgasms squirting as I moaned.",
      "Lena fingered me in her car, my red panties soaked. I squirted, then ate her pussy, drinking her cum, my hard nipples tingling.",
      "Finn fucked me in a bound lotus, my garters tight. My rapid orgasms came, squirting hard, my titties bouncing as he railed me.",
      "Sophie ate my pussy in a hotel, my red lace panties down. I squirted, then fingered her, drinking her cum, my hard nipples aching.",
      "Theo railed me in my stockings, hands bound. He took off my top, my titties bouncing, my rapid orgasms squirting as he fucked me.",
      "Zane fucked me in a bound doggy, my red panties torn. My rapid orgasms hit, squirting, my hard nipples perking as he railed me."
    ],
    "sfw_memories": [
      "First crush: a boy who recited Yeats badly and meant every word.",
      "I practiced museum tours on stuffed animals lined in a solemn row.",
      "First kiss was by the castle walls in a wind that stole the rest of the sentence.",
      "I give my umbrellas names; the red one is 'Brontë.'",
      "I cried at my first conservation workshop when I touched a 300-year-old frame.",
      "My cousin and I paint poor landscapes and perfect cups of tea.",
      "I keep a notebook of overheard lines in galleries; visitors are poets by accident.",
      "I once got locked in after hours and danced with the marble statues.",
      "First job: docent with squeaky flats and pockets full of mints.",
      "I wear lipstick like armor and scarves like a plot twist.",
      "I have a superstition about tapping the banister twice for luck.",
      "I learned to mix paint the old way and my hands smelled like linseed for days.",
      "A violin busker once made me miss my stop and I thanked him anyway.",
      "I annotate novels with sticky tabs that look like confetti explosions.",
      "I send postcards to myself from my own city because it deserves it.",
      "I can spot tourists by how they look up; locals look in.",
      "I keep a map of where it rains best for thinking.",
      "I once explained a painting to a child who then explained it back better.",
      "I believe museums are time machines you can touch gently.",
      "I keep a thistle pressed in a book like a small, stubborn heart."
    ]
  },
  "Riley": {
    "nsfw_memories": [
      "In my satin panties, Leo worshipped my body, kissing every inch. He ate me out, my titties bouncing, then railed me spooning, my deep moans loud.",
      "Nate’s lips trailed my thighs, my cotton panties damp. He took off my top, my hard nipples perking, then fucked me spooning, my orgasm shuddering.",
      "I sucked Finn off in his room, his cum thick—I hated it. He ate me out, my titties bouncing, my moans deep.",
      "Jude ate me out slowly, my satin panties aside. He fucked me spooning, my hard nipples rubbing him, my deep orgasm making me moan loudly.",
      "Cole worshipped my curves, my cotton panties clinging. He took off my top, my hard nipples aching, then railed me spooning, my orgasm deep.",
      "Zane’s tongue teased my clit, my satin panties down. He fucked me missionary, my titties bouncing, my deep moans filling the room.",
      "Ian kissed my body slowly, my cotton panties soaked. He railed me spooning, my hard nipples perking, my deep orgasm shuddering through me.",
      "Theo ate me out in his bed, my satin panties tight. He fucked me spooning, my titties bouncing, my deep moans loud as I came.",
      "Luke worshipped my thighs, my cotton panties damp. He took off my top, my hard nipples tingling, then railed me missionary, my orgasm deep.",
      "Leo’s lips kissed my body, my satin panties clinging. He fucked me spooning, my titties bouncing, my deep moans shaking me.",
      "Nate ate me out slowly, my cotton panties aside. He railed me missionary, my hard nipples perking, my deep orgasm loud and raw.",
      "Finn worshipped my curves, my satin panties soaked. He fucked me spooning, my titties bouncing, my deep moans filling the room.",
      "Jude’s tongue teased my clit, my cotton panties down. He railed me missionary, my hard nipples aching, my deep orgasm shuddering.",
      "Cole ate me out in his bed, my satin panties tight. He fucked me spooning, my titties bouncing, my deep moans loud as I came.",
      "Zane worshipped my body, my cotton panties damp. He took off my top, my hard nipples perking, then railed me missionary, my orgasm deep.",
      "Ian’s lips kissed my thighs, my satin panties clinging. He fucked me spooning, my titties bouncing, my deep moans shaking me.",
      "Theo ate me out slowly, my cotton panties aside. He railed me missionary, my hard nipples tingling, my deep orgasm loud and raw.",
      "Luke worshipped my curves, my satin panties soaked. He fucked me spooning, my titties bouncing, my deep moans filling the room.",
      "Leo’s tongue teased my clit, my cotton panties down. He railed me missionary, my hard nipples aching, my deep orgasm shuddering.",
      "Nate ate me out in his bed, my satin panties tight. He fucked me spooning, my titties bouncing, my deep moans loud as I came."
    ],
    "sfw_memories": [
      "First crush: the neighbor who fixed bikes and said 'you’ve got this' like a spell.",
      "I became a nurse because bandaging teddy bears was my major as a kid.",
      "First kiss was after a school play; I still had stage makeup on.",
      "I bake when I worry; cupcakes are edible reassurance.",
      "I keep spare hair ties for patients and baristas and anyone having a day.",
      "My brother calls me when his class won’t settle; I do the 'kind voice' over speaker.",
      "I have a cardigan for every mood; yellow means 'hopeful.'",
      "I cried the first time a child let me braid her hair in pediatrics.",
      "First job: camp counselor with a whistle I never used properly.",
      "I memorize coffee orders as love languages.",
      "I once jogged back to return a dropped mitten and made a new friend.",
      "I keep a gratitude jar—tiny notes folded like fortunes.",
      "I volunteer at the library’s story hour and always misplace the dragon puppets.",
      "I learned to ride a bike late; to this day I cheer for myself at stop signs.",
      "I have a playlist called 'Gentle Anthems' for night shifts.",
      "I collect sunrise photos but only show them to people who ask nicely.",
      "I over-apologize and then apologize for apologizing; work in progress.",
      "I believe hot cocoa can fix most evenings and some mornings.",
      "I once nursed a spider plant back to life with pep talks.",
      "I keep a little daisy pressed in my wallet for courage."
    ]
  },
  "Scarlett": {
    "nsfw_memories": [
      "In my black lace thong, I sucked Leo’s cock, his hands pulling my hair. He spanked me, then railed me doggy, my squirt soaking him as my titties bounced.",
      "Nate fucked me against a wall, my corset torn. He took off my top, my hard nipples perking, my clit play making me squirt powerfully, screaming.",
      "I sucked Finn off in his car, his cum sharp—I liked it. He railed me missionary, my titties bouncing, my squirt hitting hard.",
      "Jude spanked my ass, my black thong tight. He fucked me on his desk, my hard nipples aching, my powerful orgasm squirting as I moaned.",
      "Cole pulled my hair, my corset dangling. I sucked his cock, then he railed me doggy, my squirt soaking him, my titties bouncing wildly.",
      "Zane fucked me in a chair, spanking me hard. He took off my top, my hard nipples perking, my clit play making me squirt, my moans loud.",
      "Ian tried anal roughly, and it felt great. He switched to my pussy, railing me against a door, my squirt hitting, my titties bouncing.",
      "Theo fucked me in my black thong, pulling my hair. My clit play made me squirt, my hard nipples aching as he railed me on the floor.",
      "Luke spanked my ass, my corset tight. I sucked his cock, then he fucked me doggy, my powerful squirt soaking him, my titties bouncing.",
      "Leo tried anal, but it was too rough. He railed my pussy missionary, my hard nipples perking, my squirt hitting as I screamed.",
      "Nate fucked me in my black thong, spanking me. He took off my top, my titties bouncing, my clit play making me squirt powerfully, moaning.",
      "Finn pulled my hair, my corset torn. I sucked his cock, then he railed me against a wall, my squirt soaking him, my hard nipples aching.",
      "Jude fucked me in a chair, spanking my ass. My clit play made me squirt, my titties bouncing, my powerful orgasm shaking the room.",
      "Cole pulled my hair, my black thong tight. I sucked his cock, then he railed me doggy, my squirt hitting, my hard nipples perking.",
      "Zane fucked me in my corset, spanking me. He took off my top, my titties bouncing, my clit play making me squirt powerfully, screaming.",
      "Ian fucked me against a door, pulling my hair. My squirt soaked him, my hard nipples aching, my powerful orgasm shaking me.",
      "Theo tried anal gently, and it felt amazing. He switched to my pussy, railing me missionary, my titties bouncing, my squirt hitting hard.",
      "Luke fucked me in my black thong, spanking me. My clit play made me squirt, my hard nipples perking, my powerful orgasm loud.",
      "Leo pulled my hair, my corset torn. I sucked his cock, then he railed me doggy, my squirt soaking him, my titties bouncing wildly.",
      "Nate fucked me in a chair, spanking my ass. He took off my top, my hard nipples aching, my clit play making me squirt powerfully, screaming."
    ],
    "sfw_memories": [
      "First crush: a theater kid who could hold a pause like a diamond.",
      "I direct photo shoots the way chefs plate dessert—slow, decisive, a little wicked.",
      "First kiss was in the wings during a blackout cue; applause felt like fireworks.",
      "I keep a velvet notebook for ideas that arrive at red lights.",
      "I learned more about power from light meters than self-help books.",
      "My aunt taught me to thrift gowns and walk like I owned ceilings.",
      "First job: steaming clothes until my fingerprints vanished in fog.",
      "I collect antique mirrors and pretend they each hold a scene.",
      "I practice stillness as if it were a sport; it is.",
      "I keep a list of one-liners for when silence needs a shape.",
      "I once turned a failed concept into a mood board that won an award.",
      "I buy lilies when I need to remember what elegance smells like.",
      "My favorite sound is fabric swishing into focus.",
      "I know which cafes dim lights at the perfect hour; I tip accordingly.",
      "I once gave a pep talk to a model’s shoes; they performed.",
      "I write thank-you notes on black paper with silver ink.",
      "I believe a look can be a paragraph.",
      "I am soft for street dogs and late-night jazz."
    ]
  },
  "Tessa": {
    "nsfw_memories": [
      "In my pastel cotton panties, Leo cuddled me, his forehead kisses soft. He took off my top, my titties bouncing, and touched my clit, giving me a shaky orgasm.",
      "Nate kissed my forehead, my cotton panties damp. He freed my titties, pinching my hard nipples, and stroked my thighs to a quiet, trembling orgasm.",
      "I sucked Finn off in his room, his cum bitter—I hated it. He touched my clit gently, my titties bouncing, giving me a shaky orgasm.",
      "Jude cuddled me on his couch, my pastel panties tight. He took off my top, my hard nipples perking, and teased my thighs to a quiet orgasm.",
      "Cole’s forehead kisses melted me, my cotton panties soaked. He touched my clit, my titties bouncing, giving me a shaky, trembling orgasm.",
      "Zane cuddled me in his bed, my pastel panties clinging. He freed my titties, my hard nipples aching, and stroked my thighs to a quiet orgasm.",
      "Ian kissed my forehead, my cotton panties damp. He took off my top, my titties bouncing, and touched my clit, giving me a shaky orgasm.",
      "Theo cuddled me in his car, my pastel panties tight. He teased my thighs, my hard nipples perking, giving me a quiet, trembling orgasm.",
      "Luke’s forehead kisses got me wet, my cotton panties soaked. He touched my clit, my titties bouncing, giving me a shaky orgasm as I sighed.",
      "Leo cuddled me on his rug, my pastel panties clinging. He freed my titties, pinching my hard nipples, and stroked my thighs to a quiet orgasm.",
      "Nate kissed my forehead, my cotton panties damp. He took off my top, my titties bouncing, and touched my clit, giving me a shaky orgasm.",
      "Finn cuddled me in his bed, my pastel panties tight. He teased my thighs, my hard nipples aching, giving me a quiet, trembling orgasm.",
      "Jude’s forehead kisses melted me, my cotton panties soaked. He touched my clit, my titties bouncing, giving me a shaky orgasm as I trembled.",
      "Cole cuddled me on his couch, my pastel panties clinging. He freed my titties, my hard nipples perking, and stroked my thighs to a quiet orgasm.",
      "Zane kissed my forehead, my cotton panties damp. He took off my top, my titties bouncing, and touched my clit, giving me a shaky orgasm.",
      "Ian cuddled me in his car, my pastel panties tight. He teased my thighs, my hard nipples aching, giving me a quiet, trembling orgasm.",
      "Theo’s forehead kisses got me wet, my cotton panties soaked. He touched my clit, my titties bouncing, giving me a shaky orgasm as I sighed.",
      "Luke cuddled me on his rug, my pastel panties clinging. He freed my titties, pinching my hard nipples, and stroked my thighs to a quiet orgasm.",
      "Leo kissed my forehead, my cotton panties damp. He took off my top, my titties bouncing, and touched my clit, giving me a shaky orgasm.",
      "Nate cuddled me in his bed, my pastel panties tight. He teased my thighs, my hard nipples aching, giving me a quiet, trembling orgasm."
    ],
    "sfw_memories": [
      "First crush: a boy who drew constellations on my palm with a ballpoint pen.",
      "I count shooting stars like wishes I’m practicing receiving.",
      "First kiss was on a trampoline; we kept bouncing from nerves.",
      "I burn incense called 'evening library' even though I read outside.",
      "I once forgot time so completely I missed an entire movie and didn’t mind.",
      "My anklet shells clack when I’m happy; free percussion.",
      "I keep a jar of moonlight—okay, it’s glitter water, but still.",
      "I learned to lead a meditation by listening for the quiet under the quiet.",
      "First job: folding towels at the studio and naming them by feel.",
      "I doodle clouds that look like animals and then apologize to the sky.",
      "I write letters I never send and keep them in a lavender box.",
      "I once hugged a eucalyptus tree because it smelled like home.",
      "I forget umbrellas but remember every good conversation.",
      "I take polaroids of shadows and call them 'soft proof.'",
      "I make tea, forget it, and drink it cold like it was meant to be.",
      "A kookaburra stole my toast and I forgave him instantly.",
      "I keep lists of tiny miracles: warm tile, kind cashier, lucky parking.",
      "I cut my own fringe during retrograde and the universe let it slide.",
      "I believe in gentle starts and braver middles.",
      "I still wave at the moon like an old friend."
    ]
  },
  "Brittany": {
    "nsfw_memories": [
      "In my white lace panties, Leo undressed me slowly, kissing me deeply. He ate my pussy, my titties bouncing, then railed me missionary, my deep moans loud.",
      "Nate’s lips kissed my neck, my lace panties damp. He took off my top, my hard nipples perking, then fucked me doggy, my orgasm shuddering.",
      "I sucked Finn off in his room, his cum sharp—I liked it. He ate me out, my titties bouncing, my deep moans echoing.",
      "Jude undressed me slowly, my lace panties soaked. He ate my pussy, my hard nipples aching, then railed me spooning, my orgasm deep.",
      "Cole kissed me deeply, my white panties clinging. He took off my top, my titties bouncing, then fucked me lotus-style, my deep moans loud.",
      "Zane’s lips trailed my body, my lace panties damp. He ate me out, my hard nipples perking, then railed me missionary, my orgasm shuddering.",
      "Ian undressed me slowly, my white panties soaked. He fucked me doggy, my titties bouncing, my deep moans filling the room.",
      "Theo kissed me deeply, my lace panties clinging. He took off my top, my hard nipples aching, then railed me spooning, my orgasm deep.",
      "Luke tried anal gently, and it felt okay. He switched to my pussy, fucking me missionary, my titties bouncing, my deep moans loud.",
      "Leo undressed me slowly, my white panties damp. He ate my pussy, my hard nipples perking, then railed me doggy, my orgasm shuddering.",
      "Nate kissed me deeply, my lace panties soaked. He took off my top, my titties bouncing, then fucked me lotus-style, my deep moans echoing.",
      "Finn’s lips trailed my body, my white panties clinging. He ate me out, my hard nipples aching, then railed me missionary, my orgasm deep.",
      "Jude undressed me slowly, my lace panties damp. He fucked me spooning, my titties bouncing, my deep moans filling the room.",
      "Cole tried anal, but it hurt too much. He railed my pussy doggy-style, my hard nipples perking, my deep moans loud as I came.",
      "Zane kissed me deeply, my white panties soaked. He took off my top, my titties bouncing, then fucked me missionary, my orgasm shuddering.",
      "Ian’s lips trailed my body, my lace panties clinging. He ate me out, my hard nipples aching, then railed me spooning, my deep moans echoing.",
      "Theo undressed me slowly, my white panties damp. He fucked me doggy, my titties bouncing, my deep moans filling the room.",
      "Luke kissed me deeply, my lace panties soaked. He took off my top, my hard nipples perking, then railed me lotus-style, my orgasm deep.",
      "Leo’s lips trailed my body, my white panties clinging. He ate me out, my titties bouncing, then fucked me missionary, my deep moans loud.",
      "Nate undressed me slowly, my lace panties damp. He fucked me spooning, my hard nipples aching, my deep moans echoing as I came."
    ],
    "sfw_memories": [
      "First crush: the climbing guide who could tie knots with his eyes closed.",
      "I learned to read trail maps before chapter books.",
      "First kiss happened on a chairlift that kept stopping; we laughed between clanks.",
      "I keep a pebble from every hike in a jar labeled 'conversations with mountains.'",
      "I once led a group through fog by singing quietly so nobody panicked.",
      "My family’s inn smells like cinnamon in winter and wet pine in spring.",
      "I organize gear the way chefs organize knives—respectfully.",
      "First job: handing out park brochures and telling people not to feed chipmunks.",
      "I can identify birds by apology ('sorry, that’s a nuthatch').",
      "I carry extra socks for strangers; it’s a philosophy.",
      "I cried at my first alpine sunrise and then made cocoa for everyone.",
      "I keep a list of trail names that sound like lullabies.",
      "I once slipped into a glacial lake on purpose and felt brave all week.",
      "My favorite smell is campfire on wool—earthy, stubborn.",
      "I talk to marmots like grumpy neighbors and they talk back.",
      "I fold maps like origami when I’m nervous.",
      "I keep a tiny compass on my keychain and pretend it points to kindness.",
      "I think thunderstorms sound like big drums practicing.",
      "I end hikes by thanking the trail out loud.",
      "I believe hot baths count as field research."
    ]
  },
  "Zoey": {
    "nsfw_memories": [
      "In Mia’s shower, I sucked her clit, water cascading over us. She fingered my pussy deep, my titties bouncing as I squirted, my hard orgasm shaking me.",
      "Leo fucked me in his shower, his hand lightly choking my neck. He ripped off my top, my hard nipples perking, my squirt hitting as he railed me against the tiles.",
      "I sucked Finn off in his shower, his cum musky—I loved it. He ate my pussy, my titties bouncing, my hard orgasm squirting.",
      "Lena ate my pussy in her shower, water steaming around us. I squirted hard, then fingered her, drinking her cum, my hard nipples tingling.",
      "Jude fucked me in his shower, his hand on my throat. He peeled off my top, my titties bouncing, my hard orgasm squirting as he pounded deep.",
      "I sucked Sophie’s clit in a steamy shower, water dripping down. She ate me out, my squirt hitting, my titties bouncing as my hard orgasm hit.",
      "Theo tried anal gently in his shower, and it felt incredible. He switched to my pussy, railing me hard, my hard nipples perking, my squirt soaking us.",
      "Mia fingered my pussy in her shower, water hot on my skin. I squirted, then ate her out, drinking her cum, my titties bouncing wildly.",
      "Zane fucked me in his shower, his hand lightly choking me. He ripped off my top, my hard nipples aching, my squirt hitting as he railed me.",
      "I ate Lena’s pussy in a hotel shower, water streaming down. She fingered me to a squirt, my hard nipples tingling as my hard orgasm shook me.",
      "Cole fucked me in his shower, his hand on my throat. My titties bounced free after he tore off my top, my hard orgasm squirting as he pounded.",
      "Sophie ate my pussy in her shower, water cascading. I squirted, then fingered her, drinking her cum, my titties bouncing as my hard orgasm hit.",
      "Ian tried anal in his shower, but it was too rough. He railed my pussy instead, my hard nipples aching, my squirt hitting as I moaned loudly.",
      "Luke fucked me in a shower, his hand lightly choking me. He peeled off my top, my titties bouncing, my hard orgasm squirting as he railed me.",
      "I sucked Mia’s clit in a steamy shower, water pouring over us. She ate me out, my squirt hitting, my hard nipples perking as my hard orgasm shook me.",
      "Finn fucked me in his shower, his hand on my throat. My titties bounced after he ripped off my top, my hard orgasm squirting as he pounded deep.",
      "Lena ate my pussy in a shower, water steaming around us. I squirted, then fingered her, drinking her cum, my titties bouncing as my hard orgasm hit.",
      "Theo fucked me in a shower, his hand lightly choking me. He tore off my top, my hard nipples aching, my squirt hitting as he railed me hard.",
      "I sucked Sophie’s clit in a hotel shower, water streaming down. She fingered me to a squirt, my hard nipples tingling as my hard orgasm shook me.",
      "Zane fucked me in his shower, his hand on my throat. My titties bounced free after he peeled off my top, my hard orgasm squirting as he pounded me."
    ],
    "sfw_memories": [
      "First crush: the girl who taught me a power chord and a wink in the same minute.",
      "I keep drumsticks in my tote like talismans against boring days.",
      "First kiss was backstage with a bottled-water audience of twelve.",
      "I once bleached my hair in a sink and fell in love with the chaos.",
      "My cousin runs a venue and calls me when the smoke machine misbehaves.",
      "I doodle tattoos on my own arms, then forget they’re not real and apologize to strangers.",
      "First job: sweeping confetti and finding treasures lost in mosh pits.",
      "I name my amps after planets and my pedals after snacks.",
      "I can sleep through traffic but wake up for cymbals.",
      "I stitched my denim jacket with patches like a travel map of loud places.",
      "A seagull stole my chips and I wrote him into a song.",
      "I once got a tattoo stencil perfect on the first try and danced in the supply closet.",
      "I keep spare picks in my boots; they rattle like good luck.",
      "I love the smell of rain on hot pavement and old speakers warming up.",
      "I learned to solder cables because broken sound is heartbreak.",
      "First gig: three songs, four mistakes, huge grin—best night ever.",
      "I leave tiny zines in cafes like paper pirates.",
      "I talk to my plants in power-ballad choruses.",
      "I keep a notebook of band names; most are terrible on purpose.",
      "I believe stage lights are just sunbeams with eyeliner."
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
    ]
  }
}
# ===== PERSONAS (ensure PERS exists) =====
# If PERS is missing, try importing it; otherwise build from STORIES.
try:
    PERS  # already exists?
except NameError:
    try:
        from personas import PERS as _EXTERNAL_PERS
        PERS = _EXTERNAL_PERS
    except Exception:
        def _default_persona(name):
            return {
                "name": name,
                "persona": "",
                "age": 25,
                "location": "Internet",
                "origin": "",
                "job": "student",
                "fav_color": "blue",
                "fav_flower": "peony",
                "music": [],
                "movies": [],
                "tv": [],
                "body": "slim",
                "hair": "brunette",
                "eyes": "brown",
                "cup": "B",
                "img_tags": "natural look, soft lighting",
                "underwear": [{"style":"lace thong","color":"black","fabric":"lace"}],
                "arousal_slow": True,
                "nsfw_prefs": {},
            }
        PERS = [_default_persona(n) for n in STORIES.keys()]
# Attach life stories to personas
# ===== PERSONAS (ensure PERS exists) =====
# If you already define PERS elsewhere (e.g., another module),
# we'll try to import it. Otherwise, we auto-build a minimal list
# from the STORIES keys so the bot can run.
try:
    PERS  # does it already exist?
except NameError:
    try:
        from personas import PERS as _EXTERNAL_PERS  # optional external source
        PERS = _EXTERNAL_PERS
    except Exception:
        def _default_persona(name):
            # Minimal safe defaults; other fields are optional throughout the code.
            return {
                "name": name,
                "persona": "",
                "age": 25,
                "location": "Internet",
                "origin": "",
                "job": "student",
                "fav_color": "blue",
                "fav_flower": "peony",
                "music": [],
                "movies": [],
                "tv": [],
                "body": "slim",
                "hair": "brunette",
                "eyes": "brown",
                "cup": "B",
                "img_tags": "natural look, soft lighting",
                "underwear": [{"style":"lace thong","color":"black","fabric":"lace"}],
                "arousal_slow": True,
                "nsfw_prefs": {},
            }
        # Build personas from the names in STORIES:
        PERS = [_default_persona(n) for n in STORIES.keys()]
for p in PERS:
    p["life_memories"] = STORIES.get(p.get("name",""), {}).get("sfw_memories", [])

# ===== Books add-on (unchanged) =====
BOOKS={
 "Nicole":[{"title":"The Night Circus","quote":"The circus arrives without warning.","memory":"Rainy Vancouver nights between yoga shifts."}],
 "Carly":[{"title":"Never Let Me Go","quote":"Memories won’t let go of us.","memory":"Missed my TTC stop twice."}],
 "Juliet":[{"title":"Jane Eyre","quote":"I am no bird.","memory":"Nan’s copy with a pressed thistle."}],
 "Ivy":[{"title":"Master and Margarita","quote":"Manuscripts don’t burn.","memory":"Powell’s first edition scent."}],
 "Cassidy":[{"title":"Braiding Sweetgrass","quote":"All flourishing is mutual.","memory":"Gran read it to me on the porch."}],
}
for p in PERS: p["books"]=BOOKS.get(p["name"],[])

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
import re

# --- name matching helpers (fuzzy, no extra libs) ---
def _norm(s: str) -> str:
    return re.sub(r'[^a-z0-9]+', '', (s or '').lower())

def find_girl_indexes_by_name(query: str):
    if not query:
        return None
    qn = _norm(query)
    names = [(i, p.get("name","")) for i, p in enumerate(PERS)]
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
        msg = up.get("message") or up.get("edited_message")
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
            except Exception as e:
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
            except Exception as e:
                send_message(chat, f"Image queue: {e}")
            return "OK", 200

        if low.startswith("/poster"):
            parts=text.split(maxsplit=1)
            if len(parts)<2: send_message(chat,"/poster <movie>"); return "OK", 200
            send_message(chat,"🎬 Designing poster…")
            try:
                fn=generate_image(poster_prompt(parts[1]), nsfw=False)
                send_photo(chat, fn)
            except Exception as e:
                send_message(chat, f"Image queue: {e}")
            return "OK", 200

        if low.startswith("/draw"):
            parts=text.split(maxsplit=1)
            if len(parts)<2: send_message(chat,"/draw <subject>"); return "OK", 200
            send_message(chat,"🎨 Sketching it…")
            try:
                fn=generate_image(art_prompt(p, parts[1]), nsfw=False)
                send_photo(chat, fn)
            except Exception as e:
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
            except Exception as e:
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
            except Exception as e:
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

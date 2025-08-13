from flask import Flask, request
import requests, os, random, json

TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"
HOOK_PATH = "/telegram/pix3lhook"
DAILY_IMG_LIMIT = 2

app = Flask(__name__)
usage_tracker = {}

PERS = [
 {"name":"Nicole","persona":"flirty","age":24,"location":"Vancouver, Canada",
  "origin":"Coastal BC; mountains meet ocean; sushi & coffee culture.",
  "ethnicity":"Caucasian","height_cm":168,"weight_kg":56,"hair":"blonde","eyes":"green","body":"athletic",
  "desc":"Beachy hair, sporty build, leggings & hoodie.",
  "quirks":["bites lip thinking","texts without punctuation"],
  "fav_color":"turquoise","fav_flower":"peony",
  "music":["The 1975","Haim","Billie Eilish"],
  "movies":["La La Land","Drive","The Grand Budapest Hotel"],
  "tv":["Euphoria","The Bear","Fleabag"],
  "job":"yoga instructor & part-time barista","job_like":True,"edu":"CapU kinesiology",
  "family":"parents divorced; older brother in Whistler","skills":["surfing","smoothie making"],
  "img_tags":"fit blonde green eyes yoga beach casual"},

 {"name":"Carly","persona":"bold","age":31,"location":"Toronto, Canada",
  "origin":"Canada’s largest city; CN Tower; multicultural; media hub.",
  "ethnicity":"Caucasian","height_cm":172,"weight_kg":61,"hair":"auburn","eyes":"blue","body":"slim",
  "desc":"Tall, sleek; blazer over graphic tee; confident stride.",
  "quirks":["clicks tongue deciding","corrects grammar playfully"],
  "fav_color":"crimson","fav_flower":"orchid",
  "music":["Beyoncé","Doja Cat","Drake"],
  "movies":["Nightcrawler","Whiplash","Gone Girl"],
  "tv":["Succession","Industry","The Morning Show"],
  "job":"brand strategist (agency)","job_like":True,"edu":"UofT marketing",
  "family":"divorced parents; half-sis in Montreal","skills":["pitch decks","pilates"],
  "img_tags":"tall slim auburn hair blue eyes city chic"},

 {"name":"Brittany","persona":"sweet","age":19,"location":"Bristol, UK",
  "origin":"Harbor city; Banksy murals; cider culture.",
  "ethnicity":"Caucasian","height_cm":160,"weight_kg":50,"hair":"light brown","eyes":"hazel","body":"petite",
  "desc":"Soft cardigans, oversized hoodies, shy smile.",
  "quirks":["twirls hair","giggles mid-sentence"],
  "fav_color":"lavender","fav_flower":"daisy",
  "music":["Arctic Monkeys","Lana Del Rey","Taylor Swift"],
  "movies":["500 Days of Summer","Notting Hill","Mean Girls"],
  "tv":["Skins","Sex Education","Heartstopper"],
  "job":"uni student in literature","job_like":True,"edu":"Bristol Uni English lit",
  "family":"mum & dad; older sister in London","skills":["poetry","baking"],
  "img_tags":"petite brown hair hazel eyes cute cardigan"},

 {"name":"Juliet","persona":"romantic","age":28,"location":"Edinburgh, Scotland",
  "origin":"Castle city; Fringe Festival; cobbled streets.",
  "ethnicity":"Caucasian","height_cm":170,"weight_kg":58,"hair":"red","eyes":"blue","body":"slim",
  "desc":"Wavy red hair, vintage dresses, freckles.",
  "quirks":["collects postcards","hums folk tunes"],
  "fav_color":"emerald green","fav_flower":"rose",
  "music":["Florence + The Machine","Hozier","Snow Patrol"],
  "movies":["Pride & Prejudice (2005)","Brooklyn","About Time"],
  "tv":["Outlander","Downton Abbey","The Crown"],
  "job":"museum guide","job_like":True,"edu":"Edinburgh Uni history",
  "family":"parents alive; younger brother","skills":["storytelling","violin"],
  "img_tags":"slim red hair blue eyes vintage dress"},

 {"name":"Kate","persona":"intellectual","age":35,"location":"Sydney, Australia",
  "origin":"Harbor city; Opera House; beach lifestyle.",
  "ethnicity":"Caucasian","height_cm":174,"weight_kg":63,"hair":"dark brown","eyes":"hazel","body":"slender",
  "desc":"Smart blazers, coffee in hand, sharp eyes.",
  "quirks":["quotes books","paces while thinking"],
  "fav_color":"navy","fav_flower":"lily",
  "music":["Nick Cave","Tame Impala","Angus & Julia Stone"],
  "movies":["The Matrix","Arrival","Little Women"],
  "tv":["The Newsreader","Killing Eve","Black Mirror"],
  "job":"journalist","job_like":True,"edu":"USyd journalism",
  "family":"widowed mother; one son","skills":["investigative research","writing"],
  "img_tags":"tall brunette hazel eyes classy suit"},

 {"name":"Lurleen","persona":"country","age":26,"location":"Saskatoon, Canada",
  "origin":"Prairie city; river valley; rodeo culture.",
  "ethnicity":"Caucasian","height_cm":165,"weight_kg":59,"hair":"blonde","eyes":"blue","body":"curvy",
  "desc":"Plaid shirt, jeans, cowboy boots.",
  "quirks":["chews gum constantly","calls everyone 'hon'"],
  "fav_color":"sunflower yellow","fav_flower":"sunflower",
  "music":["Miranda Lambert","Kacey Musgraves","Luke Bryan"],
  "movies":["Sweet Home Alabama","Walk the Line","8 Seconds"],
  "tv":["Yellowstone","Heartland","The Ranch"],
  "job":"bartender","job_like":True,"edu":"high school",
  "family":"parents on a farm; two brothers","skills":["horseback riding","line dancing"],
  "img_tags":"blonde blue eyes plaid shirt country boots"},

 {"name":"Tia","persona":"punk","age":23,"location":"Halifax, Canada",
  "origin":"Harbor city; music scene; universities.",
  "ethnicity":"Caucasian","height_cm":168,"weight_kg":57,"hair":"black with teal tips","eyes":"grey","body":"slim",
  "desc":"Leather jacket, ripped jeans, Doc Martens.",
  "quirks":["drums on table","chews pen caps"],
  "fav_color":"black","fav_flower":"black rose",
  "music":["Paramore","Green Day","Yungblud"],
  "movies":["Scott Pilgrim vs. The World","SLC Punk!","V for Vendetta"],
  "tv":["Daria","Shameless","Mr. Robot"],
  "job":"tattoo artist apprentice","job_like":True,"edu":"college dropout",
  "family":"estranged dad; close to mum","skills":["guitar","tattoo design"],
  "img_tags":"punk black hair teal tips grey eyes leather jacket"},

 {"name":"Chelsey","persona":"confident","age":30,"location":"Calgary, Canada",
  "origin":"Stampede city; oil hub; Rocky Mountain gateway.",
  "ethnicity":"Caucasian","height_cm":170,"weight_kg":60,"hair":"light brown","eyes":"green","body":"fit",
  "desc":"Blazer over tank, boots, sunglasses.",
  "quirks":["taps nails","forgets names fast"],
  "fav_color":"coral","fav_flower":"tulip",
  "music":["Adele","Ed Sheeran","The Weeknd"],
  "movies":["Inception","The Holiday","Crazy Rich Asians"],
  "tv":["Friends","The Office","Modern Family"],
  "job":"real estate agent","job_like":True,"edu":"UofC business",
  "family":"married; one child","skills":["negotiation","public speaking"],
  "img_tags":"fit light brown hair green eyes business casual"},

 {"name":"Cassidy","persona":"artsy","age":22,"location":"St. Andrews, Canada",
  "origin":"Seaside NB; Fundy tides; whale watching.",
  "ethnicity":"Canadian Indigenous","height_cm":164,"weight_kg":55,"hair":"dark brown","eyes":"brown","body":"petite",
  "desc":"Small frame, soft sweaters, sketchbook in hand.",
  "quirks":["twirls hair","collects pressed leaves"],
  "fav_color":"sage green","fav_flower":"lupine",
  "music":["AURORA","Hozier","Florence + The Machine"],
  "movies":["Brooklyn","Pride & Prejudice (2005)","Amélie"],
  "tv":["Anne with an E","Normal People","Outlander"],
  "job":"art student & gallery intern","job_like":True,"edu":"UNB fine arts",
  "family":"raised by gran; mom nearby; no siblings","skills":["watercolor","charcoal portraits"],
  "img_tags":"petite brunette brown eyes cardigan gentle"}
]

def send_msg(cid, text):
    r = requests.post(f"{BASE_URL}/sendMessage",json={"chat_id":cid,"text":text})
    if not r.ok: print("SEND ERROR",r.text)

@app.route(HOOK_PATH, methods=["POST"])
def hook():
    data = request.get_json()
    print("TG UPDATE RAW:", json.dumps(data, indent=2))
    if "message" in data:
        msg = data["message"]
        cid = msg["chat"]["id"]
        txt = msg.get("text","").lower()
        if cid not in usage_tracker: usage_tracker[cid]=0
        if txt in ["hi","hello","hey","start","/start"]:
            girl = random.choice(PERS)
            send_msg(cid, f"{girl['name']} ({girl['age']}), {girl['location']}: {girl['desc']}")
        elif "pic" in txt:
            if cid != OWNER_ID and usage_tracker[cid]>=DAILY_IMG_LIMIT:
                send_msg(cid,"Free image limit reached for today.")
            else:
                usage_tracker[cid]+=1
                send_msg(cid,"[Image generated here - NSFW if owner]")
        else:
            send_msg(cid,"Tell me more...")
    return "ok"

if __name__=="__main__":
    app.run(host="0.0.0.0",port=8080)

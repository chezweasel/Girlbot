import os, json, time, base64, random, re, requests
from flask import Flask, request

# ===== ENV =====
BOT_TOKEN=os.getenv("BOT_TOKEN","").strip()
OWNER_ID=os.getenv("OWNER_ID","").strip()
WEBHOOK_URL=os.getenv("WEBHOOK_URL","").strip()
HORDE_KEY=os.getenv("HORDE_API_KEY","0000000000").strip()
API=f"https://api.telegram.org/bot{BOT_TOKEN}"
assert BOT_TOKEN and OWNER_ID and WEBHOOK_URL, "Missing BOT_TOKEN/OWNER_ID/WEBHOOK_URL"

# ===== Safety / limits =====
FREE_PER_DAY=2
FORBID={"teen","minor","underage","child","young-looking","incest","stepbro","stepsis",
        "rape","forced","nonconsensual","bestiality","animal","beast","loli","shota",
        "real name","celebrity","celeb","revenge porn","deepfake","face swap"}

def clean_ok(text:str)->bool:
    t=(text or "").lower()
    return not any(bad in t for bad in FORBID)

# ===== Personas (15) =====
# fields: name, persona, age, location, origin_facts, ethnicity, height_cm, weight_kg, hair, eyes, body, description, music, movies
PERS=[
 {"name":"Nicole","persona":"playful","age":24,"location":"Vancouver, Canada",
  "origin":"Coastal city with mountains, Stanley Park, big film/TV hub; mild Canadian climate.",
  "ethnicity":"Caucasian","height_cm":168,"weight_kg":57,"hair":"blonde","eyes":"blue","body":"slim",
  "desc":"Athletic but slender; hikes & yoga.","music":["Dua Lipa","The Weeknd","Fred again..","Kaytranada"],
  "movies":["La La Land","Past Lives","Everything Everywhere All at Once"]},

 {"name":"Lurleen","persona":"down home country girl","age":29,"location":"Moose Jaw, Canada",
  "origin":"Prairie city in Saskatchewan; underground tunnels; mineral spa; big skies.",
  "ethnicity":"Caucasian","height_cm":165,"weight_kg":63,"hair":"light brown","eyes":"hazel","body":"curvy",
  "desc":"Freckles, soft curves, cozy smile.","music":["Kacey Musgraves","Luke Combs","Zach Bryan"],
  "movies":["Walk the Line","A Star Is Born (2018)","O Brother, Where Art Thou?"]},

 {"name":"Tia","persona":"adventurous","age":27,"location":"Gold Coast, Australia",
  "origin":"Queensland surf city; theme parks; sub-tropical weather; famous breaks.",
  "ethnicity":"Caucasian","height_cm":170,"weight_kg":60,"hair":"sun-bleached blonde","eyes":"green","body":"fit",
  "desc":"Surfer build, golden tan.","music":["Rüfüs Du Sol","Tame Impala","Fisher"],
  "movies":["Point Break","Mad Max: Fury Road","Blue Crush"]},

 {"name":"Cassidy","persona":"romantic","age":22,"location":"St. Andrews, Canada",
  "origin":"Historic seaside town in New Brunswick; whale watching; quaint downtown.",
  "ethnicity":"Indigenous Canadian","height_cm":164,"weight_kg":55,"hair":"dark brown","eyes":"brown","body":"petite",
  "desc":"Small frame, long straight hair, gentle eyes.",
  "music":["AURORA","Hozier","Florence + The Machine"],"movies":["Pride & Prejudice (2005)","Brooklyn","{"name":"Carly","persona":"bold","age":31,"location":"Toronto, Canada",
 "origin":"Canada’s biggest city; CN Tower; wildly multicultural; major finance/media hub.",
 "ethnicity":"Caucasian","height_cm":172,"weight_kg":61,"hair":"auburn","eyes":"blue","body":"slim",
 "desc":"Tall, sleek; blazer over graphic tee; power-walk energy.",
 "quirks":["clicks tongue deciding","corrects grammar playfully"],"fav_color":"crimson","fav_flower":"orchid",
 "music":["Beyoncé","Doja Cat","Drake"],"movies":["Nightcrawler","Whiplash","Gone Girl"],
 "tv":["Succession","Industry","The Morning Show"],
 "job":"brand strategist (agency)","job_like":True,"edu":"UofT marketing",
 "family":"divorced parents; one half-sis in Montreal","skills":["decks & pitches","pilates"],
 "img_tags":"tall slim auburn hair blue eyes city chic blazer confident"},

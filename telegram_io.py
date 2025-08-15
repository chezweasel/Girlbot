import requests
from settings import BOT_TOKEN

API = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send_message(cid, text):
    r = requests.post(f"{API}/sendMessage", json={"chat_id": int(cid), "text": text}, timeout=20)
    if r.status_code != 200:
        print("SEND ERR:", r.text[:200])

def send_audio(cid, path):
    try:
        with open(path, "rb") as f:
            r = requests.post(f"{API}/sendAudio",
                              data={"chat_id": int(cid)},
                              files={"audio": f}, timeout=120)
        if r.status_code == 200:
            return
        # Fallback to document
        with open(path, "rb") as f2:
            r2 = requests.post(f"{API}/sendDocument",
                               data={"chat_id": int(cid)},
                               files={"document": f2}, timeout=120)
        if r2.status_code != 200:
            print("AUDIO ERR:", r2.text[:200])
    except Exception as e:
        print("AUDIO SEND EXC:", e)
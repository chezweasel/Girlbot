oimport json, os, time
from settings import STATE_FILE, FREE_PER_DAY

def now(): return time.time()

def load_state():
    try:
        if not os.path.exists(STATE_FILE): return {}
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except Exception:
        # Safe fallback on corruption
        try: os.rename(STATE_FILE, STATE_FILE + ".corrupt")
        except Exception: pass
        return {}

STATE = load_state()

def save_state():
    tmp = STATE_FILE + ".tmp"
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(STATE, f, ensure_ascii=False)
        os.replace(tmp, STATE_FILE)
    except Exception:
        try:
            if os.path.exists(tmp): os.remove(tmp)
        except Exception: pass

def get_user(uid):
    u = str(uid)
    if u not in STATE:
        STATE[u] = {
            "g": 0, "t": now(), "used": 0, "nsfw": False, "likes": [],
            "last_msg_id": None, "u_msg": 0, "teased": False, "arousal": 0.0,
            "tease_count": 0, "paid_until": 0
        }
        save_state()
    # daily reset
    if now() - STATE[u]["t"] > 86400:
        STATE[u]["t"] = now()
        STATE[u]["used"] = 0
        save_state()
    # Owner unlimited access - replace with your Telegram user ID
    if u == "7414541468":
        STATE[u]["paid_until"] = now() + 31536000  # 1 year
    return STATE[u]

def allowed(uid):
    return get_user(uid)["used"] < FREE_PER_DAY
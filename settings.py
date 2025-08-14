# settings.py
import os
import hashlib

# Telegram / Webhook
BOT_TOKEN   = os.getenv("BOT_TOKEN", "").strip()
OWNER_ID    = os.getenv("OWNER_ID", "").strip()
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "").strip()

# Image backends
HF_TOKEN     = (os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACE_TOKEN") or "").strip()
HF_MODEL     = os.getenv("HF_MODEL", "SG161222/RealVisXL_V4.0").strip()
FAL_KEY      = os.getenv("FAL_KEY", "").strip()
REPLICATE    = os.getenv("REPLICATE_API_TOKEN", "").strip()
HORDE        = os.getenv("HORDE_API_KEY", "").strip()

# Limits / safety
FREE_PER_DAY = int(os.getenv("FREE_PER_DAY", "2"))
STATE_FILE   = os.getenv("STATE_FILE", "state.json")

# Used many places
def stable_seed(name: str, suffix: str = "") -> int:
    return int(hashlib.sha256((f"FLIRTX{name}{suffix}").encode()).hexdigest()[:8], 16)

# Simple safety filter
FORBID = {
    "teen","minor","underage","child",
    "incest","stepbro","stepsis","rape","forced","nonconsensual",
    "bestiality","animal","beast","shota",
    "real name","celebrity","celeb","revenge porn","deepfake","face swap"
}
def clean_ok(t: str) -> bool:
    return not any(w in (t or "").lower() for w in FORBID)
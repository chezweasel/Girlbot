# image_backends.py
import os, io, requests
from PIL import Image
from settings import HF_TOKEN, HF_MODEL
from telegram_io import API

def _prep_for_telegram(path: str) -> str:
    try:
        im = Image.open(path)
        im.load()
        if im.mode != "RGB":
            im = im.convert("RGB")
        out = os.path.splitext(path)[0] + "_tg.jpg"
        im.save(out, "JPEG", quality=92, optimize=True)
        return out if os.path.exists(out) and os.path.getsize(out)>0 else path
    except Exception:
        return path

def send_photo(cid, path, caption=None):
    try:
        safe = _prep_for_telegram(path)
        with Image.open(safe) as im:
            buf = io.BytesIO()
            im.convert("RGB").save(buf, "JPEG", quality=95)
            buf.seek(0)
        files = {"photo": ("image.jpg", buf, "image/jpeg")}
        data = {"chat_id": int(cid)}
        if caption: data["caption"] = caption
        r = requests.post(f"{API}/sendPhoto", data=data, files=files, timeout=60)
        if r.status_code != 200:
            print("sendPhoto ERR:", r.text[:200])
    except Exception as e:
        print("send_photo EXC:", e)

def generate_image(prompt, w=576, h=704, seed=None, nsfw=False):
    """Simple HF text-to-image. Returns file path."""
    if not HF_TOKEN:
        raise RuntimeError("HF_TOKEN missing (set HF_TOKEN or HUGGINGFACE_TOKEN env)")
    api_url = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {
        "inputs": prompt,
        "parameters": {"width": int(w), "height": int(h)}
    }
    r = requests.post(api_url, headers=headers, json=payload, timeout=120)
    if r.status_code != 200:
        raise RuntimeError(f"HF error: {r.status_code} {r.text[:200]}")
    out = f"out_{abs(hash(prompt))%10_000_000}.png"
    with open(out, "wb") as f:
        f.write(r.content)
    return out
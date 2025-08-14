# image_gen.py
# Ultra-realistic image generation via Hugging Face Inference API
# Default model: SG161222/Realistic_Vision_V6.0_B1  (very realistic portraits)

import os
import io
import time
import base64
import requests
from PIL import Image

HF_TOKEN = (os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACE_TOKEN") or "").strip()
HF_MODEL_ID = os.getenv("HF_MODEL_ID", "SG161222/Realistic_Vision_V6.0_B1").strip()
HF_API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL_ID}"

# Simple safety check (DO NOT allow anything under 18)
_MINOR_WORDS = {
    "minor","underage","child","kid","shota","school boy",
def contains_minor_terms(s: str) -> bool:
    s = (s or "").lower()
    return any(w in s for w in _MINOR_WORDS)

def _ensure_rgb_jpeg(bytes_or_path: str | bytes) -> str:
    """
    Save to a Telegram-safe JPEG file and return the path.
    Accepts raw bytes or a path to an existing image file.
    """
    if isinstance(bytes_or_path, bytes):
        data = bytes_or_path
    else:
        with open(bytes_or_path, "rb") as f:
            data = f.read()

    im = Image.open(io.BytesIO(data))
    if im.mode in ("RGBA","P","LA"):
        im = im.convert("RGB")
    elif im.mode != "RGB":
        im = im.convert("RGB")

    out = f"out_{int(time.time())}.jpg"
    im.save(out, "JPEG", quality=90, optimize=True)
    return out

def gen_hf_image(prompt: str, w: int = 640, h: int = 896, nsfw: bool = False, seed: int | None = None) -> str:
    """
    Calls HF Inference API for text->image. Returns a local JPEG path.
    Notes:
      - Some hosted pipelines ignore width/height/seed; we pass them when supported.
      - Ensure your HF model can do text-to-image.
    """
    if not HF_TOKEN:
        raise RuntimeError("HF_TOKEN missing (set HF_TOKEN or HUGGINGFACE_TOKEN).")
    if not HF_MODEL_ID:
        raise RuntimeError("HF_MODEL_ID missing.")

    # Light negative prompt to enhance realism and avoid weird artifacts
    negative = "lowres, blurry, extra fingers, malformed hands, cartoon, anime, 3d, jpeg artifacts, oversaturated"

    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {
        "inputs": prompt,
        "parameters": {
            # Some hosted SD pipelines respect these keys; harmless if ignored.
            "negative_prompt": negative,
            "width": int(w),
            "height": int(h),
            "num_inference_steps": 28,
            "guidance_scale": 7.0,
        }
    }

    r = requests.post(HF_API_URL, headers=headers, json=payload, timeout=120)
    if r.status_code != 200:
        # For some repos, HF returns a JSON error; surface it for debugging
        raise RuntimeError(f"HF API {r.status_code}: {r.text[:300]}")

    # HF returns image bytes (PNG) for most text->image tasks
    img_bytes = r.content
    if not img_bytes or len(img_bytes) < 1000:
        raise RuntimeError("HF returned empty or tiny image payload.")

    return _ensure_rgb_jpeg(img_bytes)

def generate_image(prompt: str, w: int = 640, h: int = 896, seed: int | None = None, nsfw: bool = False) -> str:
    """
    Public entry the rest of your bot already expects.
    - Blocks any prompt that appears to describe minors.
    - Returns local path to a JPEG ready for Telegram.
    """
    if contains_minor_terms(prompt):
        raise RuntimeError("Blocked: under-18 / young-looking content is not allowed.")
    # Clamp friendly size (Telegram + latency); tune as desired
    w = max(256, min(int(w), 896))
    h = max(256, min(int(h), 1152))
    return gen_hf_image(prompt, w=w, h=h, nsfw=nsfw, seed=seed)
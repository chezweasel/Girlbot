# Ultra-realistic image generation via Hugging Face Inference API
# Now with: Persona integration, consistent seeds, NSFW allowance in spicy mode, enhanced prompts.

import os
import io
import time
import requests
from PIL import Image
from settings import stable_seed  # For deterministic seeds

HF_TOKEN = (os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACE_TOKEN") or "").strip()
HF_MODEL_ID = os.getenv("HF_MODEL_ID", "CompVis/stable-diffusion-v1-4").strip()  # Hosted, supports NSFW prompts
HF_API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL_ID}"

# Strict blocks (always, regardless of mode)
_MINOR_WORDS = {"minor", "underage", "child", "kid", "shota", "school boy", "school girl", "infant", "toddler", "beast", "animal"}
def contains_minor_terms(s: str) -> bool:
    s = (s or "").lower()
    return any(w in s for w in _MINOR_WORDS)

def _ensure_rgb_jpeg(bytes_or_path: str | bytes) -> str:
    if isinstance(bytes_or_path, bytes):
        data = bytes_or_path
    else:
        with open(bytes_or_path, "rb") as f:
            data = f.read()
    im = Image.open(io.BytesIO(data))
    if im.mode in ("RGBA", "P", "LA"):
        im = im.convert("RGB")
    elif im.mode != "RGB":
        im = im.convert("RGB")
    out = f"out_{int(time.time())}.jpg"
    im.save(out, "JPEG", quality=90, optimize=True)
    return out

def gen_hf_image(prompt: str, w: int = 512, h: int = 512, seed: int | None = None, nsfw: bool = False) -> str:
    if not HF_TOKEN:
        raise RuntimeError("HF_TOKEN missing.")
    if not HF_MODEL_ID:
        raise RuntimeError("HF_MODEL_ID missing.")

    # Enhance for realism/consistency
    enhanced_prompt = f"hyper-realistic, detailed, high resolution, {prompt}"
    if nsfw:
        enhanced_prompt += ", NSFW, explicit, uncensored"
    negative = "blurry, low quality, deformed"

    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {
        "inputs": enhanced_prompt,
        "parameters": {
            "negative_prompt": negative,
            "width": int(w),
            "height": int(h),
            "num_inference_steps": 30,
            "guidance_scale": 7.5,
            "seed": seed
        }
    }

    r = requests.post(HF_API_URL, headers=headers, json=payload, timeout=120)
    if r.status_code != 200:
        raise RuntimeError(f"HF API {r.status_code}: {r.text[:300]}")

    img_bytes = r.content
    if not img_bytes or len(img_bytes) < 1000:
        raise RuntimeError("HF returned empty or tiny image.")
    return _ensure_rgb_jpeg(img_bytes)

def generate_image(prompt: str, user_id: str, persona: dict, w: int = 512, h: int = 512, nsfw: bool = False) -> str:
    if contains_minor_terms(prompt):
        raise RuntimeError("Blocked: under-18 / young-looking content not allowed.")
    
    # Clamp size
    w = max(256, min(int(w), 512))
    h = max(256, min(int(h), 512))

    # Deterministic seed
    seed = stable_seed(user_id, persona.get("name", "default"), prompt)

    # Enhance prompt with persona
    body_desc = f"{persona.get('ethnicity', 'Caucasian')} woman, {persona.get('age', 25)} years old, {persona.get('body', 'slim')} build, {persona.get('height', '5\'6\"')}, {persona.get('weight', '120 lbs')}, cup {persona.get('cup', 'B')}, detailed face, natural expression"
    full_prompt = f"{body_desc}, {prompt}"

    return gen_hf_image(full_prompt, w=w, h=h, seed=seed, nsfw=nsfw)
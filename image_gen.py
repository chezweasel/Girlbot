import os
import requests
import time

# API key from Railway variables
MODELSLAB_KEY = os.getenv("MODELSLAB_KEY", "").strip()
if not MODELSLAB_KEY:
    raise RuntimeError("MODELSLAB_KEY missing in Railway variables.")

# ModelsLab NSFW photoreal model
MODEL_ID = "newrealityxl-global-nsfw"

def generate_image(prompt, negative_prompt=None, width=512, height=512):
    url = "https://stablediffusionapi.com/api/v4/dreambooth"

    payload = {
        "key": MODELSLAB_KEY,
        "model_id": MODEL_ID,
        "prompt": prompt,
        "negative_prompt": negative_prompt or "",
        "width": width,
        "height": height,
        "samples": 1,
        "num_inference_steps": 25,
        "safety_checker": "no",  # allow NSFW
        "enhance_prompt": "yes",
        "guidance_scale": 7.5
    }

    r = requests.post(url, json=payload)
    if r.status_code != 200:
        raise RuntimeError(f"ModelsLab API error {r.status_code}: {r.text}")

    data = r.json()
    if not data.get("status") == "success":
        raise RuntimeError(f"Generation failed: {data}")

    # The API sometimes needs a short wait before image is ready
    time.sleep(2)
    image_url = data["output"][0]
    return image_url
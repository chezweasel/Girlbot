# image_backends.py
import os
import requests

HF_MODEL = os.getenv("HF_MODEL", "SG161222/Realistic_Vision_V6.0_B1_noVAE")
HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

FORBIDDEN_TERMS = ["minor", "child", "infant", "beast", "animal", "underage"]

def hf_txt2img(prompt, width=512, height=512):
    # Filter prompt for forbidden terms
    low_prompt = prompt.lower()
    if any(term in low_prompt for term in FORBIDDEN_TERMS):
        return None, "❌ Forbidden term detected. Try something else."

    api_url = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {
        "inputs": prompt,
        "parameters": {"width": width, "height": height}
    }
    response = requests.post(api_url, headers=headers, json=payload, timeout=300)

    if response.status_code != 200:
        return None, f"HF API error {response.status_code}: {response.text[:200]}"

    try:
        image_bytes = response.content
        return image_bytes, None
    except Exception as e:
        return None, f"Processing error: {str(e)}"
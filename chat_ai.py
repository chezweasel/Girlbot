# chat_ai.py
# Minimal, self-contained Hugging Face chat + voice helpers for your Telegram bot.

import os, time, json, requests

# ---------- ENV ----------
HF_TOKEN = (os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACE_TOKEN") or "").strip()
HF_TEXT_MODEL_ID = os.getenv("HF_TEXT_MODEL_ID", "mistralai/Mistral-7B-Instruct-v0.3").strip()
HF_ASR_MODEL_ID  = os.getenv("HF_ASR_MODEL_ID",  "openai/whisper-small").strip()
HF_TTS_MODEL_ID  = os.getenv("HF_TTS_MODEL_ID",  "coqui/XTTS-v2").strip()

# Toggle features
ENABLE_AI_CHAT  = (os.getenv("ENABLE_AI_CHAT", "1") == "1")
ENABLE_VOICE_OUT = (os.getenv("ENABLE_VOICE_OUT", "0") == "1")   # reply with audio too

# ---------- UTIL ----------
def _need_token():
    if not HF_TOKEN:
        raise RuntimeError("HF_TOKEN (or HUGGINGFACE_TOKEN) is missing in environment.")

def _trim(s: str, n: int = 4000) -> str:
    s = str(s or "")
    return s if len(s) <= n else s[:n] + "…"

# ---------- TEXT GEN (chat) ----------
def ai_complete_text(persona: dict, state: dict, user_text: str, history=None, max_new=180) -> str:
    """
    Calls a chat-capable HF model through the Inference API.
    history: optional list[{"role":"user"/"assistant","content": "..."}]
    """
    _need_token()
    url = f"https://api-inference.huggingface.co/models/{HF_TEXT_MODEL_ID}"
    hdrs = {"Authorization": f"Bearer {HF_TOKEN}"}

    name = persona.get("name", "Girl")
    loc  = persona.get("location", "")
    style = persona.get("persona", "")
    likes = ", ".join(state.get("likes", [])[:4])

    system = (
        f"You are {name}, an adult character. Speak naturally, briefly, and do not repeat the user's exact words. "
        f"Location: {loc}. Style/personality: {style}. If you don't know, be playful (never say 'I don't know'). "
        f"Use 1-3 sentences, ask a small follow-up occasionally. Likes: {likes or 'varied'}."
    )

    msgs = [{"role": "system", "content": system}]
    if history:
        msgs.extend(history[-8:])
    msgs.append({"role": "user", "content": user_text})

    payload = {
        "inputs": msgs,
        "parameters": {
            "max_new_tokens": int(max_new),
            "temperature": 0.85,
            "top_p": 0.95,
            "repetition_penalty": 1.1,
            "truncate": 3500
        },
        "options": {"wait_for_model": True}
    }

    r = requests.post(url, headers=hdrs, json=payload, timeout=120)
    if r.status_code != 200:
        raise RuntimeError(f"HF text error {r.status_code}: {_trim(r.text,300)}")

    # Responses vary by model—try common shapes
    try:
        j = r.json()
    except Exception:
        return _trim(r.text, 400)

    if isinstance(j, dict) and "generated_text" in j:
        return _trim(j["generated_text"], 800)

    if isinstance(j, list) and j and isinstance(j[0], dict):
        if "generated_text" in j[0]:
            return _trim(j[0]["generated_text"], 800)
        # Some chat models return a conversation object—fallback to str
        return _trim(json.dumps(j), 800)

    return _trim(j, 800)

# ---------- ASR (voice in) ----------
def transcribe_audio_bytes(audio_bytes: bytes, model_id: str = None, timeout=180) -> str:
    """
    Sends raw audio bytes to a HF ASR model (Whisper). OGG/Opus is usually fine.
    """
    _need_token()
    mid = (model_id or HF_ASR_MODEL_ID).strip()
    url = f"https://api-inference.huggingface.co/models/{mid}"
    hdrs = {"Authorization": f"Bearer {HF_TOKEN}"}
    r = requests.post(url, headers=hdrs, data=audio_bytes, timeout=timeout)
    if r.status_code != 200:
        raise RuntimeError(f"HF ASR error {r.status_code}: {_trim(r.text,300)}")
    try:
        j = r.json()
    except Exception:
        # Sometimes models return text/plain
        return _trim(r.text, 800)

    if isinstance(j, dict):
        return _trim(j.get("text") or j.get("text_transcription") or j.get("generated_text") or "", 800)
    if isinstance(j, list) and j and isinstance(j[0], dict):
        return _trim(j[0].get("text", ""), 800)
    return ""

# ---------- TTS (voice out) ----------
def tts_speak_to_file(text: str, model_id: str = None, timeout=180) -> str:
    """
    Calls HF TTS (e.g., coqui/XTTS-v2). Returns path to a .wav file. 
    Telegram accepts MP3/M4A best, but WAV also works via sendAudio or sendDocument; we fall back if needed.
    """
    _need_token()
    mid = (model_id or HF_TTS_MODEL_ID).strip()
    url = f"https://api-inference.huggingface.co/models/{mid}"
    hdrs = {"Authorization": f"Bearer {HF_TOKEN}"}

    payload = {"inputs": text}
    r = requests.post(url, headers=hdrs, json=payload, timeout=timeout)
    if r.status_code != 200:
        raise RuntimeError(f"HF TTS error {r.status_code}: {_trim(r.text,300)}")

    fn = f"tts_{int(time.time())}.wav"
    with open(fn, "wb") as f:
        f.write(r.content)
    return fn

# ---------- Telegram helpers for voice ----------
def download_telegram_file(file_id: str, bot_token: str) -> bytes:
    api = f"https://api.telegram.org/bot{bot_token}"
    r = requests.get(f"{api}/getFile", params={"file_id": file_id}, timeout=20)
    r.raise_for_status()
    file_path = r.json().get("result", {}).get("file_path")
    if not file_path:
        raise RuntimeError("Telegram getFile: missing file_path")
    file_url = f"https://api.telegram.org/file/bot{bot_token}/{file_path}"
    a = requests.get(file_url, timeout=120)
    a.raise_for_status()
    return a.content

def handle_telegram_voice_message(msg: dict, bot_token: str, chat_id: int, 
                                  send_message, send_audio, persona: dict, state: dict):
    """
    - Downloads the voice note from Telegram
    - Transcribes with HF ASR
    - Generates a chat reply
    - Sends text + optional TTS audio
    """
    if not ENABLE_AI_CHAT:
        send_message(chat_id, "Voice received. (AI chat disabled)")
        return

    v = msg.get("voice") or {}
    file_id = v.get("file_id")
    if not file_id:
        send_message(chat_id, "No voice file found.")
        return

    try:
        audio_bytes = download_telegram_file(file_id, bot_token)
        user_text = transcribe_audio_bytes(audio_bytes)
        if not user_text:
            send_message(chat_id, "I couldn't catch that—try again?")
            return

        reply = ai_complete_text(persona, state, user_text)
        send_message(chat_id, reply)

        if ENABLE_VOICE_OUT:
            try:
                wav = tts_speak_to_file(reply)
                send_audio(chat_id, wav)  # You’ll add this in main.py
            except Exception as e_tts:
                send_message(chat_id, f"(TTS failed: {e_tts})")

    except Exception as e:
        send_message(chat_id, f"Voice error: {e}")
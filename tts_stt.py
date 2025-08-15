# Voice features: Text-to-Speech (TTS) for replies.
# Uses ElevenLabs by default (great voices). Optionally OpenAI TTS if you set OPENAI_API_KEY + model.
# If no keys present, returns None (voice disabled).

import os
import time
import requests

ELEVEN_KEY = os.getenv("ELEVENLABS_API_KEY", "").strip()
ELEVEN_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM").strip()  # default: Rachel
ELEVEN_URL = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVEN_VOICE_ID}"

OPENAI_KEY = os.getenv("OPENAI_API_KEY", "").strip()
OPENAI_TTS_MODEL = os.getenv("OPENAI_TTS_MODEL", "gpt-4o-mini-tts").strip()  # if you want OpenAI TTS

def tts_say(text: str) -> str | None:
    t = (text or "").strip()
    if not t:
        return None

    # 1) ElevenLabs (MP3)
    if ELEVEN_KEY:
        try:
            headers = {
                "xi-api-key": ELEVEN_KEY,
                "accept": "audio/mpeg",
                "content-type": "application/json",
            }
            payload = {"text": t, "voice_settings": {"stability": 0.4, "similarity_boost": 0.75}}
            r = requests.post(ELEVEN_URL, headers=headers, json=payload, timeout=60)
            if r.status_code == 200 and r.content:
                path = f"voice_{int(time.time())}.mp3"
                with open(path, "wb") as f:
                    f.write(r.content)
                return path
        except Exception as e:
            print("ELEVEN TTS ERR:", e)

    # 2) OpenAI TTS (MP3) — optional
    if OPENAI_KEY:
        try:
            # Simple REST call pattern (some SDKs vary; this uses audio.speech in REST-style)
            import json
            headers = {
                "Authorization": f"Bearer {OPENAI_KEY}",
                "Content-Type": "application/json",
            }
            data = {
                "model": OPENAI_TTS_MODEL,
                "input": t,
                "voice": "alloy",     # pick any available voice
                "format": "mp3"
            }
            r = requests.post("https://api.openai.com/v1/audio/speech", headers=headers, data=json.dumps(data), timeout=60)
            if r.status_code == 200 and r.content:
                path = f"voice_{int(time.time())}.mp3"
                with open(path, "wb") as f:
                    f.write(r.content)
                return path
            else:
                print("OPENAI TTS ERR:", r.text[:200])
        except Exception as e:
            print("OPENAI TTS EXC:", e)

    return None
import os, requests
from flask import Flask, request

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = os.getenv("OWNER_ID")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

app = Flask(__name__)

def set_webhook():
    r = requests.get(f"{API_URL}/setWebhook", params={"url": WEBHOOK_URL})
    print("SET HOOK RESP:", r.status_code, r.text)

@app.route(f"/telegram/pix3lhook", methods=["POST"])
def telegram_webhook():
    update = request.json
    print("TG UPDATE RAW:", update)
    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "")
        if text.lower() in ["hi","hello","hey"]:
            send_message(chat_id, "Hey there 😉 Which girl would you like to chat with?")
    return "OK"

def send_message(chat_id, text):
    r = requests.post(f"{API_URL}/sendMessage", json={"chat_id": chat_id, "text": text})
    print("API_SEND RESP:", r.status_code, r.text)

if __name__ == "__main__":
    set_webhook()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)))

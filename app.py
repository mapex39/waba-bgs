# app.py
from flask import Flask, request
from dotenv import load_dotenv
from variants import generate_response
from utils import send_whatsapp_message, log_message
import os

# Ortam değişkenlerini yükle
load_dotenv()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
app = Flask(__name__)

@app.route("/webhook", methods=["GET"])
def verify():
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if token == VERIFY_TOKEN:
        return challenge, 200
    return "Verification token mismatch", 403

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    try:
        for entry in data.get("entry", []):
            for change in entry.get("changes", []):
                value = change.get("value", {})
                messages = value.get("messages")

                if messages:
                    message = messages[0]
                    wa_id = message["from"]
                    text = message["text"]["body"]

                    result = generate_response(text)
                    reply = result["text"]

                    send_whatsapp_message(wa_id, reply)

                    log_message(
                        user_id=wa_id,
                        message=f"Gelen: {text} | Yanıt: {reply} | Tür: {result['category']} | Niyet: {result['intent_score']} | Kullanıcı: {result['user_type']}",
                        status_code=200,
                        api_response="sent"
                    )

    except Exception as e:
        log_message("system", f"⚠️ Hata: {str(e)}", 500, str(data))
    
    return "OK", 200

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, request
import openai
import requests
import os
from dotenv import load_dotenv

# Ortam değişkenlerini yükle
load_dotenv()

# API anahtarları
openai.api_key = os.getenv("OPENAI_API_KEY")
fb_token = os.getenv("FB_PAGE_TOKEN")
verify_token = os.getenv("FB_VERIFY_TOKEN")

app = Flask(__name__)

# Ana route kontrolü (opsiyonel)
@app.route('/', methods=['GET'])
def home():
    return "Webhook çalışıyor!", 200

# Webhook endpoint
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Doğrulama (Meta developer panelinde kullanılıyor)
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode == "subscribe" and token == verify_token:
            return challenge, 200
        else:
            return "Verification failed", 403

    elif request.method == 'POST':
        data = request.get_json()
        print("📥 Gelen Veri:", data)

        try:
            # Mesajı yakala
            for entry in data.get("entry", []):
                for change in entry.get("changes", []):
                    value = change.get("value", {})
                    messages = value.get("messages", [])

                    for message in messages:
                        sender = message["from"]
                        text = message["text"]["body"]

                        print(f"👤 {sender} dedi ki: {text}")

                        # GPT ile yanıt üret
                        gpt_response = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo",
                            messages=[
                                {"role": "system", "content": "Sen bir müşteri temsilcisisin."},
                                {"role": "user", "content": text}
                            ]
                        )

                        reply = gpt_response.choices[0].message["content"]
                        print("🤖 GPT yanıtı:", reply)

                        # Meta mesajı gönder
                        send_message(sender, reply)

        except Exception as e:
            print("❌ Hata:", e)

        return "OK", 200

# Mesaj gönderme fonksiyonu
def send_message(recipient, message_text):
    url = "https://graph.facebook.com/v18.0/me/messages"
    headers = {"Content-Type": "application/json"}
    payload = {
        "messaging_product": "whatsapp",
        "to": recipient,
        "type": "text",
        "text": {
            "body": message_text
        }
    }
    params = {"access_token": fb_token}
    response = requests.post(url, headers=headers, json=payload, params=params)

    print("📤 Yanıt Gönderildi:", response.status_code, response.text)

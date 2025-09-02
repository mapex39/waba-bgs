from flask import Flask, request
from openai import OpenAI
import requests
import os
from dotenv import load_dotenv

# Yükle .env dosyası
load_dotenv()

# OpenAI istemcisi
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Meta doğrulama bilgileri
VERIFY_TOKEN = os.getenv("FB_VERIFY_TOKEN")
PAGE_TOKEN = os.getenv("FB_PAGE_TOKEN")

app = Flask(__name__)

def send_message(recipient_id, message_text):
    url = f"https://graph.facebook.com/v18.0/me/messages?access_token={PAGE_TOKEN}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "messaging_type": "RESPONSE",
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    response = requests.post(url, headers=headers, json=payload)
    print(f"📤 Yanıt gönderildi: {response.status_code} - {response.text}")

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if mode == "subscribe" and token == VERIFY_TOKEN:
            print("✅ Doğrulama başarılı")
            return challenge, 200
        else:
            print("❌ Doğrulama başarısız")
            return "Verification failed", 403

    elif request.method == "POST":
        data = request.get_json()
        print("📥 Gelen mesaj:", data)

        if data.get("object") == "page":
            for entry in data.get("entry", []):
                messaging_events = entry.get("messaging", [])
                for event in messaging_events:
                    sender_id = event["sender"]["id"]
                    if "message" in event and "text" in event["message"]:
                        message_text = event["message"]["text"]
                        print(f"📩 {sender_id} mesaj gönderdi: {message_text}")

                        # GPT'den yanıt al
                        try:
                            response = client.chat.completions.create(
                                model="gpt-4",
                                messages=[
                                    {"role": "system", "content": "Sen güneş enerjili ve şehir şebekeli aydınlatma ürünlerini anlatan bir satış temsilcisisin."},
                                    {"role": "user", "content": message_text}
                                ],
                                temperature=0.7
                            )
                            reply = response.choices[0].message.content
                        except Exception as e:
                            reply = "Üzgünüm, bir hata oluştu. Daha sonra tekrar dener misiniz?"
                            print("❌ GPT Hatası:", e)

                        send_message(sender_id, reply)

        return "OK", 200

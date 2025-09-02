from flask import Flask, request
import openai
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Env değişkenleri
openai.api_key = os.getenv("OPENAI_API_KEY")
PAGE_ACCESS_TOKEN = os.getenv("FB_PAGE_TOKEN")
VERIFY_TOKEN = os.getenv("FB_VERIFY_TOKEN")

# WABA mesaj gönderme fonksiyonu
def send_message(recipient_id, message_text):
    url = f"https://graph.facebook.com/v18.0/{os.getenv('PHONE_NUMBER_ID')}/messages"
    headers = {
        "Authorization": f"Bearer {PAGE_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": recipient_id,
        "type": "text",
        "text": {
            "body": message_text
        }
    }
    response = requests.post(url, headers=headers, json=data)
    print("📤 Gönderilen yanıt:", response.text)

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        if (request.args.get("hub.mode") == "subscribe" and
            request.args.get("hub.verify_token") == VERIFY_TOKEN):
            return request.args.get("hub.challenge"), 200
        else:
            return "Verification failed", 403

    elif request.method == 'POST':
        data = request.get_json()
        print("📥 Gelen mesaj:", data)

        try:
            entry = data['entry'][0]
            changes = entry['changes'][0]
            value = changes['value']
            messages = value.get('messages')

            if messages:
                message = messages[0]
                sender_id = message['from']
                message_text = message['text']['body']

                # GPT ile cevap oluştur
                completion = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "Sen güneş enerjili ve şehir şebekeli aydınlatma ürünlerini anlatan bir satış temsilcisisin."},
                        {"role": "user", "content": message_text}
                    ]
                )
                reply = completion['choices'][0]['message']['content']
                send_message(sender_id, reply)

        except Exception as e:
            print("❌ Hata:", e)

        return "OK", 200

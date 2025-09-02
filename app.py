from flask import Flask, request
import openai
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
PAGE_ACCESS_TOKEN = os.getenv("FB_PAGE_TOKEN")
VERIFY_TOKEN = os.getenv("FB_VERIFY_TOKEN")

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return "Verification failed", 403

    elif request.method == 'POST':
        data = request.get_json()
        print("📥 Gelen mesaj:", data)

        # Mesaj kontrolü
        try:
            message_text = data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
            sender_id = data['entry'][0]['changes'][0]['value']['messages'][0]['from']
        except KeyError:
            return "No message found", 200

        # GPT yanıtı al
        try:
            completion = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Sen bir satış temsilcisisin. Solar ve şehir şebekeli aydınlatma ürünleri hakkında detaylı, ama sade ve anlaşılır bilgiler veriyorsun."},
                    {"role": "user", "content": message_text}
                ]
            )
            reply = completion.choices[0].message.content
        except Exception as e:
            reply = "Üzgünüm, şu anda teknik bir sorun nedeniyle yanıt veremiyorum. Lütfen daha sonra tekrar deneyin."
            print("❌ GPT Hatası:", e)

        # Yanıtı gönder
        send_message(sender_id, reply)
        return "OK", 200

def send_message(recipient_id, message_text):
    url = f"https://graph.facebook.com/v18.0/{os.getenv('PHONE_NUMBER_ID')}/messages"
    headers = {
        "Authorization": f"Bearer {PAGE_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": recipient_id,
        "type": "text",
        "text": {
            "body": message_text
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    print("📤 Yanıt gönderildi:", response.status_code, response.text)

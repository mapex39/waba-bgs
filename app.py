from flask import Flask, request
import openai
import requests
import os
from dotenv import load_dotenv

# Ortam değişkenlerini yükle
load_dotenv()

app = Flask(__name__)

# API Anahtarları
openai.api_key = os.getenv("OPENAI_API_KEY")
fb_token = os.getenv("FB_PAGE_TOKEN")
verify_token = os.getenv("FB_VERIFY_TOKEN")

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Meta doğrulama adımı
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode == "subscribe" and token == verify_token:
            return challenge, 200
        else:
            return "Verification failed", 403

    elif request.method == 'POST':
        data = request.get_json()
        print("📥 Gelen veri:", data)

        try:
            # Mesajı çıkaralım
            entry = data['entry'][0]
            changes = entry['changes'][0]
            value = changes['value']
            messages = value.get('messages')

            if messages:
                message = messages[0]
                phone_number = message['from']  # Gönderen numara
                user_message = message['text']['body']  # Kullanıcı mesajı

                print(f"👤 Kullanıcı mesajı: {user_message}")

                # GPT ile cevap üret
                gpt_reply = generate_gpt_reply(user_message)

                print(f"🤖 GPT yanıtı: {gpt_reply}")

                # Yanıtı kullanıcıya gönder
                send_whatsapp_message(phone_number, gpt_reply)

        except Exception as e:
            print("❌ Hata:", e)

        return "OK", 200

def generate_gpt_reply(prompt):
    """OpenAI API ile yanıt üret"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # veya gpt-4
            messages=[
                {"role": "system", "content": "Sen kibar ve bilgili bir müşteri temsilcisisin. Kısa ve net cevaplar ver."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content'].strip()

    except Exception as e:
        print("❌ GPT hatası:", e)
        return "Size yardımcı olurken bir sorun oluştu. Lütfen daha sonra tekrar deneyin."

def send_whatsapp_message(to, message):
    """WhatsApp mesajını gönder"""
    url = f"https://graph.facebook.com/v18.0/{os.getenv('PHONE_NUMBER_ID')}/messages"
    headers = {
        "Authorization": f"Bearer {fb_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": message}
    }

    try:
        r = requests.post(url, headers=headers, json=payload)
        print("📤 Mesaj gönderme sonucu:", r.status_code, r.text)
    except Exception as e:
        print("❌ Mesaj gönderme hatası:", e)

if __name__ == '__main__':
    app.run(port=5000)

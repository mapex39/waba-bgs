from flask import Flask, request
import openai
import requests
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# API anahtarları
openai.api_key = os.getenv("OPENAI_API_KEY")
fb_token = os.getenv("FB_PAGE_TOKEN")
verify_token = os.getenv("FB_VERIFY_TOKEN")

# Basit skorlandırma fonksiyonu
def estimate_purchase_intent(message_text):
    high_intent_keywords = ["fiyat", "kurulum", "kaç para", "almak istiyorum", "teklif", "montaj", "ne kadar", "kredi kartı", "teslimat"]
    low_intent_keywords = ["merhaba", "adres", "telefon", "açık mısınız", "neredesiniz"]

    score = 3  # orta seviye başla

    for word in high_intent_keywords:
        if word in message_text.lower():
            score += 1
    for word in low_intent_keywords:
        if word in message_text.lower():
            score -= 1

    return max(1, min(score, 5))

# GPT yanıtı üret
def generate_response(message_text):
    intent_score = estimate_purchase_intent(message_text)

    messages = [
        {"role": "system", "content": "Sen güneş enerjili ve şehir şebekeli aydınlatma ürünlerini anlatan bir satış temsilcisisin. Teknik terim kullanma, kullanıcıya göre konuş."},
        {"role": "user", "content": message_text}
    ]

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=messages
    )
    reply = response.choices[0].message.content.strip()

    log_interaction(message_text, reply, intent_score)

    return reply

# Mesaj ve skorları logla
def log_interaction(question, answer, score):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("chat_log.csv", "a", encoding="utf-8") as f:
        f.write(f'"{now}","{question}","{answer}",{score}\n')

# WABA mesaj gönderme
def send_message(recipient_id, message_text):
    url = f"https://graph.facebook.com/v18.0/{os.getenv('PHONE_NUMBER_ID')}/messages"
    headers = {
        "Authorization": f"Bearer {fb_token}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": recipient_id,
        "type": "text",
        "text": {"body": message_text}
    }
    response = requests.post(url, headers=headers, json=data)
    print("📤 Yanıt gönderildi:", response.status_code, response.text)

# Webhook
@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode == "subscribe" and token == verify_token:
            return challenge, 200
        else:
            return "Verification failed", 403

    elif request.method == "POST":
        data = request.get_json()
        print("📥 Gelen mesaj:", data)

        try:
            message_text = data["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]
            sender_id = data["entry"][0]["changes"][0]["value"]["messages"][0]["from"]
            reply = generate_response(message_text)
            send_message(sender_id, reply)
        except Exception as e:
            print("⚠️ Hata:", e)

        return "OK", 200

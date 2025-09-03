from flask import Flask, request
import openai
import requests
import os
from dotenv import load_dotenv
import json
from core.variants import generate_response
from helpers import choose_variant
from core.classifier import classify_message
from core.logger import log_message, evaluate_potential, analyze_buyer_type

app = Flask(__name__)
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
fb_token = os.getenv("FB_PAGE_TOKEN")
verify_token = os.getenv("FB_VERIFY_TOKEN")


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
        print("📥 Gelen mesaj:", json.dumps(data, indent=2))

        try:
            message = data['entry'][0]['changes'][0]['value']['messages'][0]
            sender_id = message['from']
            message_text = message['text']['body']

            # Kategori belirleme
            category = classify_message(message_text)

            # Variant seçimi
            variant = choose_variant()

            # Cevap üret
            reply = generate_response(category, variant)

            # Kullanıcı tipi ve potansiyel analiz
            buyer_type = analyze_buyer_type(message_text)
            potential_score = evaluate_potential(message_text)

            # Cevabı özelleştir
            reply += f"\n\n(Satın alma potansiyeli: {potential_score}/5, Alıcı tipi: {buyer_type})"

            # Mesaj gönder
            send_message(sender_id, reply)

            # Loglama
            log_message(sender_id, message_text, reply, category, variant, potential_score, buyer_type)

        except Exception as e:
            print(f"❌ Hata: {e}")

        return "OK", 200


def send_message(recipient_id, text):
    url = f"https://graph.facebook.com/v18.0/{os.getenv('PHONE_NUMBER_ID')}/messages"
    headers = {
        "Authorization": f"Bearer {fb_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": recipient_id,
        "type": "text",
        "text": {
            "body": text
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    print("📤 Yanıt gönderildi:", response.status_code, response.text)

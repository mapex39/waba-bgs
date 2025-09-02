from flask import Flask, request
import openai
import requests
import os
app = Flask(__name__)

VERIFY_TOKEN = "solar-whatsapp-bgs"  # 👈 Bu değeri sen belirle, aynı değeri Meta'da kullanacaksın
from dotenv import load_dotenv

load_dotenv()  # .env dosyasını yükler

openai.api_key = os.getenv("OPENAI_API_KEY")
fb_token = os.getenv("FB_PAGE_TOKEN")
verify_token = os.getenv("FB_VERIFY_TOKEN")
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

        # Burada mesaj içeriğini al ve GPT'den yanıt al
        # GPT cevabını WABA API ile gönder

        return "OK", 200

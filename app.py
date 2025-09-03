from flask import Flask, request
import openai
import requests
import os
import logging
from datetime import datetime
from dotenv import load_dotenv

app = Flask(__name__)

# 📁 Log klasörü oluştur
os.makedirs("logs", exist_ok=True)
log_filename = datetime.now().strftime("logs/app_%Y-%m-%d.log")

# 📝 Logging yapılandırması
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    encoding='utf-8'
)

# ✅ Meta bilgileri (gizlilik için örnek değerler)
ACCESS_TOKEN = "YOUR_WHATSAPP_TOKEN"
PHONE_NUMBER_ID = "YOUR_PHONE_NUMBER_ID"
WHATSAPP_API_URL = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"

# 🔁 Otomatik cevap üretici (kısa örnek versiyon)
def generate_response(message_text):
    message_text = message_text.lower()

    if "ev" in message_text or "sistem" in message_text:
        return "Ev tipi güneş enerji sistemlerimiz mevcut. Size uygun paketleri paylaşabiliriz."
    elif "aydınlatma" in message_text or "lamba" in message_text:
        return "Bahçeniz veya sokak için solar aydınlatmalarımız var. Kaç adet düşünüyorsunuz?"
    elif "sulama" in message_text:
        return "Tarla veya hobi bahçesi için solar sulama sistemlerimiz mevcut. Lokasyon bilgisini paylaşabilir misiniz?"
    else:
        return "İlgilendiğiniz ürünü biraz daha detaylı anlatabilir misiniz? Size en doğru çözümü sunmak isteriz."

# 📤 WhatsApp mesajı gönderici
def send_whatsapp_message(phone_number, message_text):
    data = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "text",
        "text": {"body": message_text}
    }

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.post(WHATSAPP_API_URL, headers=headers, json=data)
    logging.info(f"📤 Yanıt gönderildi: {response.status_code} {response.text}")
    return response

# 🔄 Webhook endpoint
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    logging.info(f"📥 Gelen mesaj: {data}")

    try:
        for entry in data.get("entry", []):
            for change in entry.get("changes", []):
                value = change.get("value", {})

                # Kullanıcı mesajı varsa
                if "messages" in value:
                    message = value["messages"][0]
                    phone = message["from"]
                    text = message.get("text", {}).get("body", "")

                    response = generate_response(text)
                    send_whatsapp_message(phone, response)

                # Mesaj durumu (sent, delivered vs.)
                elif "statuses" in value:
                    status_info = value["statuses"][0]
                    logging.info(f"Mesaj durumu: {status_info.get('status')} - ID: {status_info.get('id')}")

                else:
                    logging.warning(f"Bilinmeyen değişiklik tipi: {value}")

    except Exception as e:
        logging.exception(f"⚠️ Webhook işlenirken hata: {str(e)}")

    return "OK", 200

# 🌐 Meta doğrulama
@app.route("/webhook", methods=["GET"])
def verify():
    verify_token = "TEST_TOKEN"
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode and token and token == verify_token:
        return challenge, 200
    else:
        return "Verification failed", 403

# 🚀 Başlatıcı
if __name__ == "__main__":
    app.run(debug=True)

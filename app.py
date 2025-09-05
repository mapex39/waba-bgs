import os
import json
import requests
from flask import Flask, request

from utils import extract_text, send_whatsapp_message, send_message_with_buttons
from variants import generate_response, classify_intent
from logger import log_message as log

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    
    try:
        entry = data["entry"][0]
        change = entry["changes"][0]["value"]

        if "messages" in change:
            message = change["messages"][0]
            phone_number_id = change["metadata"]["phone_number_id"]
            from_number = message["from"]
            message_text = extract_text(message)

            # 🔍 Kullanıcının niyeti
            intent = classify_intent(message_text)
            print(f"🎯 Kullanıcı niyeti: {intent}")

            # 💾 Gelen mesajı logla
            log_message(
                message=message_text,
                intent=intent,
                answer="-",         # henüz cevap verilmedi
                category="-",       # henüz sınıflandırılmadı
                variant="-",        # varyant bilgisi yok
                potential="-",      # lead skorlaması yapılmadı
                buyer_type="-"      # kullanıcı tipi belli değil
            )

            # 💬 Eğer ilk mesajsa buton gönder
            if message["type"] == "text" and intent == "first_contact":
                send_message_with_buttons(
                    phone_id=phone_number_id,
                    access_token=os.getenv("ACCESS_TOKEN"),
                    recipient_phone=from_number,
                    text="📌 Merhaba! Size nasıl yardımcı olabiliriz?",
                    buttons=[
                        {
                            "type": "reply",
                            "reply": {"id": "solar_ev", "title": "🌞 Güneş Enerjili Sistemler"}
                        },
                        {
                            "type": "reply",
                            "reply": {"id": "solar_aydinlatma", "title": "💡 Solar Aydınlatma"}
                        },
                        {
                            "type": "reply",
                            "reply": {"id": "uzman_gorus", "title": "📞 Uzmanla Görüşmek"}
                        }
                    ]
                )
            else:
                response_text = generate_response(message_text)
                send_whatsapp_message(
                    phone_id=phone_number_id,
                    access_token=os.getenv("ACCESS_TOKEN"),
                    recipient_phone=from_number,
                    text=response_text
                )

        return "OK", 200

    except Exception as e:
        print(f"⚠️ Hata: {str(e)}")
        return "error", 500

@app.route('/meta-webhook', methods=['GET'])
def meta_webhook_verify():
    if request.args.get("hub.verify_token") == os.getenv("META_VERIFY_TOKEN"):
        return request.args.get("hub.challenge")
    return "Doğrulama başarısız", 403

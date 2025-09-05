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
    print("📥 Gelen mesaj:", json.dumps(data, ensure_ascii=False, indent=2))

    try:
        entry = data["entry"][0]
        change = entry["changes"][0]["value"]

        if "messages" in change:
            message = change["messages"][0]
            phone_number_id = change["metadata"]["phone_number_id"]
            from_number = message["from"]
            message_text = extract_text(message)

            # 🎯 Kullanıcının niyeti
            intent = classify_intent(message_text)
            log(f"🎯 Kullanıcı niyeti: {intent}")

            access_token = os.getenv("ACCESS_TOKEN")

            if message["type"] == "text" and intent == "first_contact":
                send_message_with_buttons(
                    phone_id=phone_number_id,
                    access_token=access_token,
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
                    access_token=access_token,
                    recipient_phone=from_number,
                    text=response_text
                )

        return "OK", 200

    except Exception as e:
        log(f"⚠️ Hata: {str(e)}")
        return "error", 500


@app.route('/meta-webhook', methods=['POST'])
def meta_webhook():
    data = request.get_json()
    log("📥 Yeni lead verisi geldi:", data)

    try:
        entry = data['entry'][0]
        changes = entry['changes'][0]
        lead_id = changes['value']['leadgen_id']
    except Exception as e:
        log(f"[HATA] Lead ID çıkarılamadı: {str(e)}")
        return "Hatalı format", 400

    try:
        graph_token = os.getenv("META_GRAPH_ACCESS_TOKEN")
        lead_info = requests.get(
            f"https://graph.facebook.com/v18.0/{lead_id}?access_token={graph_token}"
        ).json()

        def extract_phone_number(lead_info):
            for field in lead_info.get("field_data", []):
                if field["name"] == "phone_number":
                    return field["values"][0]
            return None

        phone_number = extract_phone_number(lead_info)

        if phone_number:
            intro_message = (
                "Merhaba! ☀️ Güneş enerjili sisteminizi doğru hesaplayabilmemiz için\n"
                "elektrikle hangi cihazların çalışacağını ve\n"
                "kurulum yapılacak şehri bilmemiz gerekiyor.\n\n"
                "Lütfen bu bilgileri eksiksiz şekilde bizimle paylaşır mısınız?"
            )

            phone_id = os.getenv("PHONE_ID")
            access_token = os.getenv("ACCESS_TOKEN")

            send_whatsapp_message(
                phone_id=phone_id,
                access_token=access_token,
                recipient_phone=phone_number,
                text=intro_message
            )

    except Exception as e:
        log(f"[HATA] Lead verisi işlenemedi: {str(e)}")
        return "Hata", 500

    return "OK", 200


@app.route('/meta-webhook', methods=['GET'])
def meta_webhook_verify():
    if request.args.get("hub.verify_token") == os.getenv("META_VERIFY_TOKEN"):
        return request.args.get("hub.challenge")
    return "Doğrulama başarısız", 403

import os
from flask import Flask, request
from utils import extract_text, send_whatsapp_message, send_message_with_buttons
from variants import generate_response, classify_intent

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("📥 Gelen mesaj:", data)

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
            print("🎯 Kullanıcı niyeti:", intent)

            # 💬 Eğer ilk mesajsa buton gönder

            if message["type"] == "text" and intent == "first_contact":
                send_message_with_buttons(
                    phone_id,
                    recipient_phone,
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
                send_whatsapp_message(phone_number_id, from_number, response_text)

        return "OK", 200

    except Exception as e:
        print("⚠️ Hata:", e)
        return "error", 500

if __name__ == "__main__":
    app.run(debug=True)

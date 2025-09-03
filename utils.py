import requests
import json
from logger import log_message

WHATSAPP_API_URL = "https://graph.facebook.com/v18.0"

# --- Yardımcı Fonksiyon: Buton başlıklarını kırpar ---
def truncate_button_titles(buttons, max_length=20):
    for btn in buttons:
        if "reply" in btn and "title" in btn["reply"]:
            title = btn["reply"]["title"]
            if len(title) > max_length:
                log(f"[UYARI] Buton başlığı çok uzun: '{title}' => kısaltıldı.")
                btn["reply"]["title"] = title[:max_length]
    return buttons

# --- WhatsApp Mesaj Gönderici ---
def send_message_with_buttons(phone_id, access_token, recipient_phone, text, buttons):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # Önce buton başlıklarını kontrol edip kesiyoruz
    buttons = truncate_button_titles(buttons)

    payload = {
        "messaging_product": "whatsapp",
        "to": recipient_phone,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {
                "text": text
            },
            "action": {
                "buttons": buttons
            }
        }
    }

    url = f"{WHATSAPP_API_URL}/{phone_id}/messages"

    try:
        response = requests.post(url, headers=headers, json=payload)
        log(f"📤 Butonlu mesaj gönderildi: {response.status_code} {response.text}")
        return response.json()
    except Exception as e:
        log(f"[HATA] Mesaj gönderimi başarısız: {str(e)}")
        return None

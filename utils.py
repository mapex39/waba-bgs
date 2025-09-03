import os
import requests

def extract_text(message):
    return message.get("text", {}).get("body", "").strip()

def send_whatsapp_message(phone_number_id, recipient_phone, text):
    headers = {
        "Authorization": f"Bearer {os.environ['WHATSAPP_TOKEN']}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": recipient_phone,
        "type": "text",
        "text": {"body": text}
    }

    response = requests.post(
        f"https://graph.facebook.com/v18.0/{phone_number_id}/messages",
        headers=headers,
        json=payload
    )
    print("📤 Yanıt gönderildi:", response.status_code, response.text)

def send_button_message(phone_number_id, recipient_phone, text, buttons):
    headers = {
        "Authorization": f"Bearer {os.environ['WHATSAPP_TOKEN']}",
        "Content-Type": "application/json"
    }

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

    response = requests.post(
        f"https://graph.facebook.com/v18.0/{phone_number_id}/messages",
        headers=headers,
        json=payload
    )
    print("📤 Butonlu mesaj gönderildi:", response.status_code, response.text)

import openai
import os
import json
import requests
import random


def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

def choose_variant():
    config = load_config()
    variants = ["A1", "A2", "A3"]

    if config["ab_testing_enabled"] and config["use_random_variant"]:
        return random.choice(variants)
    else:
        return config["default_variant"]
        
        
def detect_profile_and_score(message_text):
    # Kullanıcı profili analizini GPT ile yap
    prompt = f"""
Aşağıdaki müşteri mesajını analiz et ve 1) hangi alıcı profiline uyduğunu, 2) satın alma potansiyelini 5 üzerinden puanla. 
Profiller:
- Cekingen: Bilgi almak isteyen ama temkinli
- Fiyat Odaklı: Fiyat veya kampanya sorar
- Hızlı Karar Veren: Hemen almak isteyen, hızlı dönüş ister
- Teknik: Teknik detaylara yoğunlaşır
- Kararsız: Belirsiz ve çok soru soran
- Sadece İnceleyen: Şimdilik bilgi alıyor

Mesaj: \"{message_text}\"
Çıktıyı şu formatta ver:
{{
  "profile_id": "fiyat_odakli",
  "profile_name": "Fiyat Odaklı",
  "score": 3
}}
    """

    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Sen kısa ve yapılandırılmış cevaplar veren bir analiz botusun."},
            {"role": "user", "content": prompt}
        ]
    )

    output = completion.choices[0].message.content
    try:
        result = json.loads(output)
        return result['profile_id'], result['profile_name'], result['score']
    except:
        return "belirsiz", "Belirsiz", 2

def generate_reply(user_message, profile_id):
    try:
        with open("profiles.json", "r") as f:
            profiles = json.load(f)

        instructions = profiles.get(profile_id, profiles["belirsiz"])

        system_prompt = instructions.get("prompt", "")
        temperature = instructions.get("temperature", 0.7)

        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=temperature
        )

        return completion.choices[0].message.content
    except Exception as e:
        print("❌ GPT yanıt üretme hatası:", e)
        return "Mesajınızı aldık, en kısa sürede dönüş yapacağız."

def send_message(recipient_id, message_text):
    url = f"https://graph.facebook.com/v18.0/{os.getenv('PHONE_NUMBER_ID')}/messages"
    headers = {
        "Authorization": f"Bearer {os.getenv('FB_PAGE_TOKEN')}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": recipient_id,
        "type": "text",
        "text": {
            "body": message_text
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    print("📤 Yanıt gönderildi:", response.status_code, response.text)

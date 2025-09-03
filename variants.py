# variants.py
import openai
import json
import re

def classify_message(message):
    message = message.lower()

    if any(word in message for word in ["güneş", "solar", "panel", "enerji", "off grid", "şebekesiz"]):
        return "solar_system"

    if any(word in message for word in ["lamba", "aydınlatma", "led", "direk", "sokak lambası"]):
        return "lighting"

    if any(word in message for word in ["adres", "nerede", "konum", "gelmek istiyorum"]):
        return "address"

    if any(word in message for word in ["telefon", "aradım", "ulaşamadım", "numara"]):
        return "contact"

    if any(word in message for word in ["açık", "kaçta kapanıyor", "mesai", "çalışma saati"]):
        return "opening_hours"

    if any(word in message for word in ["fiyat", "ne kadar", "ücret", "kaç tl"]):
        return "pricing"

    return "general"

def estimate_purchase_intent(message):
    score = 1
    message_lower = message.lower()

    if any(word in message_lower for word in ["kaç", "fiyat", "ücret", "stok", "var mı", "hazır mı"]):
        score += 1

    if any(word in message_lower for word in ["hemen", "bugün", "şimdi", "acele", "acil", "sipariş", "kurulum"]):
        score += 2

    if "adres" in message_lower or "konum" in message_lower:
        score += 1

    return min(score, 5)

def detect_user_type(message):
    msg = message.lower()
    if any(word in msg for word in ["çok pahalı", "daha ucuz", "indirim", "taksit", "peşin"]):
        return "fiyat_odakli"
    if any(word in msg for word in ["emin değilim", "bilmiyorum", "yardım eder misiniz"]):
        return "çekingen"
    if any(word in msg for word in ["şunu istiyorum", "şunu gönderin", "bu lazım"]):
        return "kararlı"
    return "genel"

def generate_response(message, user_type="genel"):
    category = classify_message(message)
    intent_score = estimate_purchase_intent(message)
    user_type = detect_user_type(message)

    responses = {
        "solar_system": "Bahçeniz veya eviniz için güneş enerjili sistemlerimiz mevcut. Kullanım amacınızı paylaşırsanız size uygun olanı birlikte seçebiliriz.",
        "lighting": "LED aydınlatmalar ve güneş enerjili lambalar stoklarımızda mevcut. Kullanım alanınızı paylaşırsanız örnek gönderebilirim.",
        "address": "Mağazamız OSTİM OSB'de. Konum linki isterseniz hemen paylaşabilirim.",
        "contact": "Bize bu numaradan ulaşabilirsiniz: 0312 340 4040",
        "opening_hours": "Hafta içi 09:00 - 18:00 arası açığız. Cumartesi 13:00’e kadar hizmet veriyoruz.",
        "pricing": "Fiyatlar ürün modeline göre değişiyor. Hangi ürünle ilgilendiğinizi söylerseniz detaylı bilgi verebilirim.",
        "general": "Size nasıl yardımcı olabilirim? Güneş enerjili sistemler, aydınlatma ve diğer ürünlerimiz hakkında bilgi verebilirim."
    }

    reply_text = responses.get(category, responses["general"])

    return {
        "text": reply_text,
        "category": category,
        "intent_score": intent_score,
        "user_type": user_type
    }

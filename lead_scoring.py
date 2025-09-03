import re

# Lead skoru (1-5)
def score_lead(message):
    text = message.lower()
    score = 1

    buying_intent_keywords = [
        "fiyat", "ne kadar", "stok", "kaç watt", "kurulum", "kaç tl", "acil", "hemen", "satın al", "elimde var", "ihtiyacım var"
    ]
    for keyword in buying_intent_keywords:
        if keyword in text:
            score += 1

    question_words = ["mi", "mı", "musunuz", "nedir", "var mı", "kaç", "ne zaman", "kuruluyor mu"]
    if any(word in text for word in question_words):
        score += 1

    if len(text) > 30:
        score += 1

    return min(score, 5)


# Alıcı tipi tahmini
def detect_buyer_type(message):
    text = message.lower()

    if re.search(r"\b(fiyat|kaç para|indirim|ucuz)\b", text):
        return "fiyat odaklı"

    if re.search(r"\b(kararsızım|bilmiyorum|emin değilim|bir bakayım)\b", text):
        return "kararsız"

    if re.search(r"\b(kapasite|kaç watt|kaç saat|şarj süresi|panel boyutu)\b", text):
        return "araştırmacı"

    if len(text) < 15 or "bilgi verir misiniz" in text:
        return "çekingen"

    return "genel"

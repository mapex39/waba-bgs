import datetime

def log_message(user_id, question, answer, category, variant, potential, buyer_type):
    log = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "user_id": user_id,
        "question": question,
        "answer": answer,
        "category": category,
        "variant": variant,
        "potential": potential,
        "buyer_type": buyer_type
    }

    with open("logs.jsonl", "a") as f:
        f.write(str(log) + "\n")


def evaluate_potential(text):
    keywords = ["fiyat", "kaç", "ne kadar", "stok", "acil", "hemen", "almak", "kurulum"]
    score = sum(1 for word in keywords if word in text.lower())
    return min(score + 1, 5)


def analyze_buyer_type(text):
    text = text.lower()
    if "kaç para" in text or "fiyat" in text:
        return "fiyat odaklı"
    elif "tam bilmiyorum" in text or "kararsızım" in text:
        return "çekingen"
    elif "teknik detay" in text or "verim" in text:
        return "teknik"
    else:
        return "genel"

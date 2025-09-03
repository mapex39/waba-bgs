import json
import datetime

# Kategorileri yükler
def load_categories():
    with open("data_layers/category_map.json", "r", encoding="utf-8") as f:
        return json.load(f)

# Gelen mesajdaki kategori tahmini
def detect_category(message_text):
    categories = load_categories()
    message_text = message_text.lower()

    for item in categories:
        for keyword in item["keywords"]:
            if keyword.lower() in message_text:
                return item["category"]

    return "diğer"

# Loglama fonksiyonu
def log_conversation(wa_id, name, message_text, category, lead_score, buyer_type, variant):
    now = datetime.datetime.now().isoformat()

    log_entry = {
        "timestamp": now,
        "wa_id": wa_id,
        "name": name,
        "message": message_text,
        "detected_category": category,
        "lead_score": lead_score,
        "buyer_type": buyer_type,
        "reply_variant": variant
    }

    try:
        with open("data_layers/conversation_logs.json", "r+", encoding="utf-8") as f:
            data = json.load(f)
            data.append(log_entry)
            f.seek(0)
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print("❌ Loglama hatası:", e)

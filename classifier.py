def classify_message(text):
    text = text.lower()

    if "karavan" in text or "bahçe" in text or "elektrik yok" in text or "güneş enerjili sistem" in text:
        return "solar_offgrid"
    elif "villa" in text or "şebeke bağlantılı" in text or "fatura" in text:
        return "solar_ongrid"
    elif "direk" in text and "solar" in text:
        return "lighting_solar"
    elif "direk" in text:
        return "lighting_grid"
    elif "sulama" in text or "tarla" in text or "pompa" in text:
        return "agriculture_irrigation"
    elif "adres" in text or "telefon" in text or "açık mısınız" in text:
        return "contact_info"
    else:
        return "general_info"

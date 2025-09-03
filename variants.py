# core/variants.py

def generate_response(category, variant="A1"):
    """
    Kategoriye göre, farklı stillerde yanıt verir.
    """
    responses = {
        "solar_offgrid": {
            "A1": "Güneş enerjili sistemlerimizle elektrik olmayan alanlarda aydınlatma ve enerji sağlayabilirsiniz. Nerede kullanmayı düşünüyorsunuz?",
            "A2": "Merhaba! Elektrik olmayan yerler için güneş enerjili çözümler sunuyoruz. Ne tür cihazları çalıştırmak istiyorsunuz?",
            "A3": "Selamlar! Güneş enerjili sistemlerimiz, özellikle bahçeler ve karavanlar için ideal. Kurulum yeri ve cihaz bilgisi verir misiniz?"
        },
        "solar_ongrid": {
            "A1": "Şebeke bağlantılı sistemlerimiz sayesinde elektrik faturanızı azaltabilirsiniz. Eviniz nerede?",
            "A2": "Merhaba! Güneş panellerimizle şebeke elektriğini destekleyebilirsiniz. Çatı alanınız uygun mu?",
            "A3": "Selamlar! Şebeke destekli sistem kurmak istiyorsanız evinizin çatı bilgilerini alabilir miyiz?"
        },
        "lighting_grid": {
            "A1": "Şehir elektriğiyle çalışan aydınlatma direkleri için size katalog gönderebilirim. Nerede kullanacaksınız?",
            "A2": "Merhaba! Şebeke elektriğiyle çalışan LED direklerimiz mevcuttur. Projeniz için kaç adet gerekiyor?",
            "A3": "Selamlar! Aydınlatma ihtiyacınıza göre uygun direk tipini birlikte seçebiliriz. Açık alan mı, sokak mı?"
        },
        "lighting_solar": {
            "A1": "Güneş enerjili aydınlatma direkleri, elektrik olmayan bölgeler için idealdir. Alan neresi?",
            "A2": "Merhaba! Solar aydınlatma sistemleri stoklarımızda mevcut. Ne büyüklükte bir alan aydınlatılacak?",
            "A3": "Selamlar! Solar direkler gece boyunca aydınlatma sağlar. Proje detaylarını iletir misiniz?"
        },
        "agriculture_irrigation": {
            "A1": "Tarımsal sulama sistemlerimizde güneş panelli çözümlerle kuyudan su çekebilirsiniz. Araziniz nerede?",
            "A2": "Merhaba! Tarla sulamak için RF kontrollü sistemler kuruyoruz. Kuyu ile mesafe nedir?",
            "A3": "Selamlar! Güneş enerjili sulama sistemlerimiz kuruluma hazır. Alan büyüklüğü ve pompa tipi önemli."
        },
        "general_info": {
            "A1": "Elbette! Size yardımcı olabilmem için neyle ilgilendiğinizi öğrenebilir miyim?",
            "A2": "Merhaba! Solar sistemler, aydınlatma ürünleri ve sulama çözümleri sunuyoruz. Hangi konuda destek istersiniz?",
            "A3": "Selamlar! Size en iyi çözümü sunmak için neye ihtiyacınız olduğunu öğrenmem yeterli."
        },
        "contact_info": {
            "A1": "İletişim bilgilerimiz: 📞 0 (312) 123 45 67 – 📍 Ostim/ANKARA. Hafta içi 09:00–18:00 arası açığız.",
            "A2": "Bize ulaşmak isterseniz 0312 123 45 67 numaralı hattımızı arayabilirsiniz. Mağazamız Ostim'de.",
            "A3": "Adres: Ostim OSB. Telefon: 0312 123 45 67. Hafta içi her gün buradayız, bekleriz!"
        }
    }

    return responses.get(category, {}).get(variant, "Size yardımcı olabilmem için biraz daha detay verebilir misiniz?")

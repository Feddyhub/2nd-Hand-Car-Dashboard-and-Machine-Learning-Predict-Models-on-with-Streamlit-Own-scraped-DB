import requests
from bs4 import BeautifulSoup as bs

# URL ve kullanıcı temsilcisi tanımlama
url = "https://www.cardekho.com/used-sedan+cars+in+delhi-ncr"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
}

# Sayfayı çek ve BeautifulSoup ile işle
response = requests.get(url, headers=headers)

# Sayfa durumu kontrolü
if response.status_code != 200:
    print(f"Sayfa yüklenemedi, durum kodu: {response.status_code}")
else:
    soup = bs(response.content, "lxml")

    # Fiyatı bul (doğru class adıyla)
    price_divs = soup.find_all('div', class_="Price hover")

    # Fiyatları listeye ekle
    prices = []
    for price_div in price_divs:
        p_tags = price_div.find_all('p')
        for p_tag in p_tags:
            price_text = p_tag.get_text(strip=True)  # HTML içeriğini temizle
            prices.append(price_text)

    # Listeyi yazdır
    if prices:
        print("Bulunan fiyatlar:", prices)
    else:
        print("Çalışmadı veya fiyat bulunamadı. Attribute adını kontrol edin.")
    
# HTTP yanıt durum kodunu yazdır
print(response.status_code)

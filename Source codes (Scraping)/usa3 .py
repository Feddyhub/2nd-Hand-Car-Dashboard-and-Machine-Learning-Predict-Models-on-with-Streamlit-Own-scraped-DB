import requests
from bs4 import BeautifulSoup as bs

# URL ve kullanıcı temsilcisi tanımlama
url = "https://www.ebay.com/b/Cars-Trucks/6001/bn_1865117"
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

    # Fiyatı bul (doğru sınıf adıyla)
    price_elements = soup.find_all('span', class_="textual-display bsig__price bsig__price--displayprice")


    # Fiyatları listeye ekle
    prices = []
    for price_element in price_elements:
        price_text = price_element.get_text(strip=True)  # HTML içeriğini temizle
        prices.append(price_text)

    # Listeyi yazdır
    if prices:
        print("Bulunan fiyatlar:", prices)
    else:
        print("Çalışmadı veya fiyat bulunamadı. Sınıf adını kontrol edin.")
print(response.status_code)

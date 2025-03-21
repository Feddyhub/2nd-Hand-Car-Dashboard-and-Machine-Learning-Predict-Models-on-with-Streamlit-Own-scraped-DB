import requests
from bs4 import BeautifulSoup as bs

# URL ve kullanıcı temsilcisi tanımlama
url = "https://www.cars.com/shopping/results/?dealer_id=&include_shippable=true&keyword=&list_price_max=&list_price_min=&makes[]=bmw&maximum_distance=all&mileage_max=&monthly_payment=&page_size=20&sort=best_match_desc&stock_type=all&year_max=&year_min=&zip="
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
    price_elements = soup.find_all('span', class_="mileage")


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

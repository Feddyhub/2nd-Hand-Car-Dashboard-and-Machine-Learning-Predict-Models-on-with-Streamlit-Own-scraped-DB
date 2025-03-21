import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import re
import time

# Başlangıç URL'si
base_url = "https://www.autotrader.ca/cars/on/toronto/?rcp=0&rcs=0&prx=100&prv=Ontario&loc=M4B%202J8&hprc=True&wcp=True&sts=New-Used&inMarket=basicSearch&mdl=1%20Series&make=BMW"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
}

# Boş veri yapısı oluştur
data = []

# Sayfa numarası
page_num = 0

while True:
    # URL'yi oluştur
    url = base_url.format(page_num)
    print(f"İşleniyor: {url}")  # Her URL'yi yazdır
    retry_count = 0
    max_retries = 3  # Her sayfa için maksimum yeniden deneme sayısı
    success = False

    while retry_count < max_retries and not success:
        try:
            response = requests.get(url, headers=headers, timeout=20)
            if response.status_code == 200:
                success = True
            else:
                print(f"Sayfa yüklenemedi, durum kodu: {response.status_code}")
                retry_count += 1
                time.sleep(5)  # 5 saniye bekle ve yeniden dene
        except requests.exceptions.RequestException as e:
            print(f"Bağlantı hatası: {e}")
            retry_count += 1
            time.sleep(5)  # 5 saniye bekle ve yeniden dene

    if not success:
        print("Başarısızlık sınırına ulaşıldı, program durduruluyor.")
        break

    soup = bs(response.content, "lxml")

    # Fiyatı bul (doğru sınıf adıyla)
    price_elements = soup.find_all('span', class_="price-amount")

    # Km bilgilerini bul (doğru sınıf adıyla)
    km_elements = soup.find_all('span', class_="odometer-proximity")

    # Model bilgilerini bul (doğru sınıf adıyla)
    model_elements = soup.find_all('span', class_="title-with-trim")

    # Hiç eleman bulunamazsa (son sayfa olabilir), döngüyü kır
    if not price_elements and not km_elements and not model_elements:
        print("Son sayfaya ulaşıldı veya veri bulunamadı.")
        break

    # Tüm verileri aynı anda çek ve kaydet
    for price_element, km_element, model_element in zip(price_elements, km_elements, model_elements):
        price_text = price_element.get_text(strip=True)  # Fiyatı temizle
        km_text = km_element.get_text(strip=True)  # Km bilgisini temizle
        model_text = model_element.get_text(strip=True)  # Model bilgisini temizle

        # Yılı ayıkla
        match = re.search(r'\b\d{4}\b', model_text)
        year = match.group() if match else 'N/A'  # Yıl bulunamazsa 'N/A'

        # Markayı ve modeli ayır
        brand_model = model_text.split(' ', 2)
        brand = brand_model[1] if len(brand_model) >= 2 else 'N/A'
        model = brand_model[2] if len(brand_model) >= 3 else 'N/A'

        # Verileri kaydet
        data.append({'Brand': brand, 'Model': model, 'Year': year, 'KM': km_text, 'Price': price_text})

    # Çekilen veri miktarını ve sayfa numarasını yazdır
    print(f"Sayfa numarası: {page_num}, Çekilen veri sayısı: {len(data)}")

    # Bir sonraki sayfaya geç
    page_num += 1

# DataFrame'e dönüştür ve excele kaydet
df = pd.DataFrame(data)
df.to_excel('BMW_1_series_dataset.xlsx', index=False)
print("Veriler başarıyla excele kaydedildi.")

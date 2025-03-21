from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import os

# Selenium WebDriver'ı başlatmak için ayarlar
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--headless")  # Tarayıcıyı headless modda çalıştırır (isteğe bağlı)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Başlangıç URL'si (BMW 1 Series 2005 yılı)
base_url = "https://www.autoscout24.com/lst/bmw/1-series-(all)/re_2005?atype=C&cy=D&damaged_listing=exclude&desc=1&ocs_listing=include&powertype=kw&search_id=25ihx35mx83&sort=year&source=listpage_pagination&ustate=N%2CU"
driver.get(base_url)

# Dinamik bekleme
wait = WebDriverWait(driver, 20)

# Verileri çekecek yer
car_list = []

page_number = 1
while True:
    try:
        # Sonuç sayfasındaki araç kartlarını bul
        cars = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "ListItem_wrapper__TxHWu")))

        for car in cars:
            car_data = {}

            # Araç başlığı
            try:
                title = car.find_element(By.CLASS_NAME, "ListItem_title__ndA4s")
                car_data["Title"] = title.text.strip()
            except NoSuchElementException:
                car_data["Title"] = None

            # Fiyat bilgisi
            try:
                price = car.find_element(By.CLASS_NAME, "Price_price__APlgs")
                car_data["Price"] = price.text.strip()
            except NoSuchElementException:
                car_data["Price"] = None

            # Yıl bilgisi
            try:
                year = car.find_element(By.XPATH, ".//span[@data-testid='VehicleDetails-calendar']")
                year_text = year.text.strip()
                if "/" in year_text:
                    car_data["Year"] = year_text.split("/")[1].strip()
                else:
                    car_data["Year"] = None
            except NoSuchElementException:
                car_data["Year"] = None

            # KM bilgisi
            try:
                mileage = car.find_element(By.XPATH, ".//span[@data-testid='VehicleDetails-mileage_road']")
                car_data["Mileage"] = mileage.text.strip()
            except NoSuchElementException:
                car_data["Mileage"] = None

            # Vites bilgisi
            try:
                transmission = car.find_element(By.XPATH, ".//span[@data-testid='VehicleDetails-transmission']")
                car_data["Transmission"] = transmission.text.strip()
            except NoSuchElementException:
                car_data["Transmission"] = None

            # Yakıt tipi bilgisi
            try:
                fuel_type = car.find_element(By.XPATH, ".//span[@data-testid='VehicleDetails-gas_pump']")
                car_data["Fuel Type"] = fuel_type.text.strip()
            except NoSuchElementException:
                car_data["Fuel Type"] = None

            # Beygir gücü bilgisi
            try:
                power = car.find_element(By.XPATH, ".//span[@data-testid='VehicleDetails-speedometer']")
                car_data["Power"] = power.text.strip()
            except NoSuchElementException:
                car_data["Power"] = None

            car_list.append(car_data)

        # Bir sonraki sayfaya geçmek için URL'yi güncelle
        page_number += 1
        next_url = f"https://www.autoscout24.com/lst/bmw/1-series-(all)/re_2005?atype=C&cy=D&damaged_listing=exclude&desc=1&ocs_listing=include&powertype=kw&page={page_number}&search_id=25ihx35mx83&sort=year&source=listpage_pagination&ustate=N%2CU"

        # Yeni sayfayı yükle
        driver.get(next_url)
        wait.until(EC.staleness_of(cars[0]))

    except TimeoutException:
        print("Araç kartları bulunamadı veya sayfa zamanında yüklenemedi.")
        break

    except NoSuchElementException:
        print(f"{page_number}. sayfada bir hata oluştu. Sayfa geçişi yapılamıyor.")
        break

# Veriyi DataFrame'e dönüştür
df = pd.DataFrame(car_list)

# Dosya yolunu belirle
save_path = "/Users/ahmetfurkanarikan/Desktop/car_project/DATA/ALM/BMW/1_series/germany_bmw_1series_2005.xlsx"

# Veriyi belirtilen klasöre Excel dosyasına kaydet
df.to_excel(save_path, index=False)

# WebDriver'ı kapat
driver.quit()

print(f"{len(df)} araç verisi Excel dosyasına kaydedildi: {save_path}")

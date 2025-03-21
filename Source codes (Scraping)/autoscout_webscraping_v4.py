from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import os
from multiprocessing import Pool

# Web scraping işlevi
def scrape_data_for_year(year):
    # Tarayıcı ayarlarını yapma
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")  # Tarayıcıyı headless modda çalıştırma

    # WebDriver'ı başlatma
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # URL oluşturma
    base_url = f"https://www.autoscout24.com.tr/lst/toyota/yaris/re_{year}?atype=C&cy=F&damaged_listing=exclude&desc=0&ocs_listing=include&powertype=kw&search_id=stug2of498&sort=standard&source=homepage_search-mask&ustate=N%2CU"
    driver.get(base_url)

    # Dinamik bekleme
    wait = WebDriverWait(driver, 20)
    car_list = []
    page_number = 1

    while True:
        try:
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ListItem_wrapper__TxHWu")))
            cars = driver.find_elements(By.CLASS_NAME, "ListItem_wrapper__TxHWu")
            for car in cars:
                car_data = {}
                try:
                    car_data["Title"] = car.find_element(By.CLASS_NAME, "ListItem_title__ndA4s").text.strip()
                except NoSuchElementException:
                    car_data["Title"] = None
                try:
                    car_data["Price"] = car.find_element(By.CLASS_NAME, "Price_price__APlgs").text.strip()
                except NoSuchElementException:
                    car_data["Price"] = None
                try:
                    year_text = car.find_element(By.XPATH,
                                                 ".//span[@data-testid='VehicleDetails-calendar']").text.strip()
                    car_data["Year"] = year_text.split("/")[1].strip() if "/" in year_text else None
                except NoSuchElementException:
                    car_data["Year"] = None
                try:
                    car_data["Mileage"] = car.find_element(By.XPATH,
                                                           ".//span[@data-testid='VehicleDetails-mileage_road']").text.strip()
                except NoSuchElementException:
                    car_data["Mileage"] = None
                try:
                    car_data["Transmission"] = car.find_element(By.XPATH,
                                                                ".//span[@data-testid='VehicleDetails-transmission']").text.strip()
                except NoSuchElementException:
                    car_data["Transmission"] = None
                try:
                    car_data["Fuel Type"] = car.find_element(By.XPATH,
                                                             ".//span[@data-testid='VehicleDetails-gas_pump']").text.strip()
                except NoSuchElementException:
                    car_data["Fuel Type"] = None
                try:
                    car_data["Power"] = car.find_element(By.XPATH,
                                                         ".//span[@data-testid='VehicleDetails-speedometer']").text.strip()
                except (NoSuchElementException, StaleElementReferenceException):
                    car_data["Power"] = None
                car_list.append(car_data)

            page_number += 1
            next_url = f"https://www.autoscout24.com.tr/lst/toyota/yaris/re_{year}?atype=C&cy=F&damaged_listing=exclude&desc=0&ocs_listing=include&powertype=kw&page={page_number}&search_id=stug2of498&sort=standard&source=homepage_search-mask&ustate=N%2CU"
            driver.get(next_url)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ListItem_wrapper__TxHWu")))
        except TimeoutException:
            print(f"{year}: Araç kartları bulunamadı veya sayfa zamanında yüklenemedi.")
            break
        except NoSuchElementException:
            print(f"{year}: {page_number}. sayfada bir hata oluştu. Sayfa geçişi yapılamıyor.")
            break

    # Veriyi kaydetme
    df = pd.DataFrame(car_list)
    save_path = f"/Users/ahmetfurkanarikan/Desktop/car_project/DATA/FRA/TOYOTA/yaris_series/toyota_yaris_{year}.xlsx"
    df.to_excel(save_path, index=False)
    print(f"{year}: {len(df)} araç verisi Excel dosyasına kaydedildi: {save_path}")

    # WebDriver'ı kapat
    driver.quit()

# Paralel olarak veri çekme
if __name__ == "__main__":
    years = list(range(2005, 2026))

    # Gruplar halinde işlerin yapılmasını sağlıyoruz
    grouped_years = [years[i:i+4] for i in range(0, len(years), 4)]

    # Her grubu sırasıyla işleme
    for group in grouped_years:
        with Pool(processes=4) as pool:  # Aynı anda 4 işlem çalıştırıyoruz
            pool.map(scrape_data_for_year, group)
        print(f"Grup tamamlandı: {group}")

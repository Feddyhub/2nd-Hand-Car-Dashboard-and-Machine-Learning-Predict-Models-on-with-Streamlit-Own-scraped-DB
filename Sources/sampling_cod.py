from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# chromedriver'ın yolunu belirtin
service = Service("/Applications/chromedriver.exe")
driver = webdriver.Chrome(service=service)

# Web sitesini açın
driver.get("https://www.webmotors.com.br/carros/estoque/bmw?estadocidade=estoque&marca1=BMW&autocomplete=bmw&autocompleteTerm=BMW&lkid=1704")

try:
    # Sayfanın fiyat elementinin yüklenmesini bekleyin
    wait = WebDriverWait(driver, timeout=20)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-test-id="price-current-price"]')))

    # Fiyatı içeren elementleri bulun
    elements = driver.find_elements(By.CSS_SELECTOR, 'div[data-test-id="price-current-price"]')

    print(len(elements))  # Seçilen elementlerin sayısını kontrol edin
    for element in elements:
        print(element.text)  # Fiyatı yazdır

    # Elementlerden metinleri çıkarın ve listelere kaydedin
    price_list = [element.text for element in elements]

    # Listelerden bir DataFrame oluşturun
    df = pd.DataFrame({"Price": price_list})

    # DataFrame'i Excel dosyasına kaydedin
    df.to_excel("ak.xlsx", index=False)

finally:
    # WebDriver'ı kapatın
    driver.quit()
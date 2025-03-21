import pandas as pd
import os
import streamlit as st
import plotly.express as px
import numpy as np
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# Sidebar başlıkları
st.sidebar.header("🛠️ Ülke, Marka, Metrik ve Fiyat Seçimleri")

# 1. İlk iki selectbox'un yan yana olmasını sağlamak (sidebar içinde)
col1, col2 = st.sidebar.columns(2)

with col1:
    country1 = st.selectbox("1. Ülke Seçin", ["Canada", "France", "Germany"], key="country1")

with col2:
    country2 = st.selectbox("2. Ülke Seçin", ["Canada", "France", "Germany"], key="country2")

# 2. İkinci ve üçüncü selectbox'ların yan yana olmasını sağlamak (sidebar içinde)
col3, col4 = st.sidebar.columns(2)

with col3:
    metric1 = st.sidebar.radio("Karşılaştırma Metrik Seçin", ["Fiyat", "Yil", "Km"], key="metric_radio")

# Yıl seçimi için yan yana iki input kutusu
year_col1, year_col2 = st.sidebar.columns(2)
with year_col1:
    start_year = st.number_input("Başlangıç Yılı", min_value=1998, max_value=2025, value=2000)
with year_col2:
    end_year = st.number_input("Bitiş Yılı", min_value=1998, max_value=2025, value=2025)

brand = st.sidebar.selectbox("Marka Seçin", ["BMW", "MERCEDES", "AUDI", "TOYOTA", "FORD"])


# Model Seçimi
model_options = {
    "BMW": ["1_series", "3_series", "5_series", "7_series"],
    "MERCEDES": ["a1_series", "a3_series", "a5_series", "a7_series"],
    "AUDI": ["a3", "a4", "a6", "a8"],
    "TOYOTA": ["corolla", "camry", "rav4", "highlander"],
    "FORD": ["focus", "fiesta", "mondeo", "mustang"]
}

model = st.sidebar.selectbox("Model Seçin", model_options.get(brand, []))

## tags ve slider bir + hareket olmali bir kere acinca 2 sini kullanabil yoksa kullanma ve ayrica altta brandi yukariya alabiliyorsak alalim ya da asagi atalim.

# 4. Select slider 0'dan 80,000 dolara kadar (sidebar içinde)
price = st.sidebar.slider("Fiyat Seçin (0 - 80,000 $)", 0, 80000, 20000, step=1000)  # Select slider


# 5. Toggle için switch ekleyelim (Slider'ı aktif etmek için)
activate_slider = st.sidebar.checkbox("Fiyat Seçimini Aktif Et", value=True)

price_text = f"${price:,} 💰" if activate_slider else "Fiyat seçimi devre dışı 🚫"





# 3. Tags bölümü: st.multiselect kullanarak birden fazla etiket seçilebilecek şekilde
tags = st.sidebar.multiselect("Tags Seçin", 
    ["Lux", "Old", "New", "Factory New"], 
    default=["New", "Lux"], 
    key="tags_selectbox")  # Multiple selection for tags


    
st.markdown("# 🚗 2nd Hand Car Comparison by Countries")


st.markdown(f"""
    <div style="
        border: 2px solid #ddd; 
        padding: 15px; 
        border-radius: 10px; 
        background-color: rgb(255, 255, 255);
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
    ">
        <h3>{country1} 🇺🇸 vs {country2} 🇩🇪</h3>
        <p><strong>Seçilen Veriler:</strong></p>
        <p><strong>Ülkeler:</strong> {country1} ve {country2} 🌍</p>
        <p><strong>Metrik:</strong> {metric1} 📊</p>
        <p><strong>Taglar:</strong> {", ".join(tags)} 🏷️</p>
        <p><strong>Marka:</strong> {brand} 🚘</p>
        <p><strong>Seçilen Fiyat Aralığı:</strong> {"Fiyat seçimi devre dışı 🚫" if not activate_slider else f"${price:,} 💰"}</p>
    </div>
""", unsafe_allow_html=True)





# Ülke adlarını klasör isimleriyle eşleştirme
country_folder_map = {
    "Canada": "CANADA",
    "France": "FRANCE",
    "Germany": "GERMANY"
}

# Klasörlerin bulunduğu ana dizin
base_path = "CarPrices_Database"  # Sabit dizin yolu

country_folder1 = country_folder_map.get(country1)
country_folder2 = country_folder_map.get(country2)



# İlk ülke ve ikinci ülkenin klasör yolları
country_path1 = os.path.join(base_path, country_folder1)
country_path2 = os.path.join(base_path, country_folder2)

# st.write(f"**1. Ülke Klasörü:** {country_path1}")
# st.write(f"**2. Ülke Klasörü:** {country_path2}")






# Marka adlarını klasör isimleriyle eşleştirme
brand_folder_map = {
    "BMW": "BMW",
    "MERCEDES": "MERCEDES",
    "AUDI": "AUDI",
    "TOYOTA": "TOYOTA",
    "FORD": "FORD"
}

brand_folder = brand_folder_map.get(brand)
brand_path1 = os.path.join(country_path1, brand_folder)
brand_path2 = os.path.join(country_path2, brand_folder)

st.write(f"**Seçilen Marka Klasörü (1. Ülke):** {brand_path1}")
st.write(f"**Seçilen Marka Klasörü (2. Ülke):** {brand_path2}")








# Dosya yollarını oluşturma
if model:
    # Marka adını küçük harfe çevirip, modeli ve yılı ekleyerek dosya adını oluştur
    brand_lower = brand.lower()
    
    # İlk ülke için tüm yılların verilerini birleştir
    df1_list = []
    for year in range(start_year, end_year + 1):
        file_name = f"{brand_lower}_{model.lower()}_{year}.xlsx"
        file_path1 = os.path.join(brand_path1, file_name)
        if os.path.exists(file_path1):
            temp_df = pd.read_excel(file_path1)
            df1_list.append(temp_df)
    
    # İkinci ülke için tüm yılların verilerini birleştir
    df2_list = []
    for year in range(start_year, end_year + 1):
        file_name = f"{brand_lower}_{model.lower()}_{year}.xlsx"
        file_path2 = os.path.join(brand_path2, file_name)
        if os.path.exists(file_path2):
            temp_df = pd.read_excel(file_path2)
            df2_list.append(temp_df)
    
    # Eğer veri varsa birleştir
    if df1_list:
        df1 = pd.concat(df1_list, ignore_index=True)
        st.write(f"**{country1} - {brand} - {model} -- 1. Ülke için veriler başarıyla yüklendi.**")
    else:
        df1 = None
        st.write(f"**{country1} için {start_year}-{end_year} arası veri bulunamadı.**")
    
    if df2_list:
        df2 = pd.concat(df2_list, ignore_index=True)
        st.write(f"**{country2} - {brand} - {model} -- 2. Ülke için veriler başarıyla yüklendi.**")
    else:
        df2 = None
        st.write(f"**{country2} için {start_year}-{end_year} arası veri bulunamadı.**")






    # Eğer her iki veri de yüklendiyse yan yana göster
    if df1 is not None and df2 is not None:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"### {country1} Verileri")
            st.dataframe(df1)

        with col2:
            st.markdown(f"### {country2} Verileri")
            st.dataframe(df2)

        # Verileri karşılaştırma
        if df1 is not None and df2 is not None:
            st.subheader(f"{metric1} Karşılaştırması")

            # Hangi metrik seçildiyse, o sütunu karşılaştır
            if metric1 == "Fiyat":
                metric_column = "Price"
            elif metric1 == "Km":
                metric_column = "KM"
            else:
                metric_column = "Year"

            # Verileri birleştir
            df1["Country"] = country1
            df2["Country"] = country2

            # Eğer metrik sütunu her iki DataFrame içinde de varsa
            if metric_column in df1.columns and metric_column in df2.columns:
                df1_copy = df1.copy()
                df2_copy = df2.copy()
                
                # Dataset sütunu ekle
                df1_copy["Dataset"] = country1
                df2_copy["Dataset"] = country2
                
                # Metrik sütununu sayısal formata dönüştür
                if metric1 in ["Price", "Km"]:
                    df1_copy[metric_column] = pd.to_numeric(df1_copy[metric_column], errors='coerce')
                    df2_copy[metric_column] = pd.to_numeric(df2_copy[metric_column], errors='coerce')
                
                # NaN değerleri temizle
                df1_copy = df1_copy.dropna(subset=[metric_column])
                df2_copy = df2_copy.dropna(subset=[metric_column])
                
                # Veri var mı kontrol et
                if not df1_copy.empty and not df2_copy.empty:
                    combined_df = pd.concat([df1_copy, df2_copy])

                    # Grafik hazırlığı
                    plt.figure(figsize=(10, 6))

                    # df1 verisini çiz
                    sns.lineplot(data=df1_copy, x="Year", y=metric_column, color="blue", label=country1)
                    
                    # df2 verisini çiz
                    sns.lineplot(data=df2_copy, x="Year", y=metric_column, color="red", label=country2)
                    
                    # Başlık ve etiketler
                    plt.title(f"{metric1} Karşılaştırması: {country1} vs {country2}")
                    plt.xlabel("Yıl")
                    plt.ylabel(f"{metric1} Değeri")
                    plt.legend()

                    # Streamlit ile grafik gösterimi
                    st.pyplot(plt)

                    # Violin Plot
                    plt.figure(figsize=(10, 6))
                    sns.violinplot(data=combined_df, x="Dataset", y=metric_column, palette=["blue", "red"])
                    plt.title(f"{metric1} Dağılımı: {country1} vs {country2}")
                    plt.xlabel("Ülke")
                    plt.ylabel(f"{metric1} Değeri")
                    plt.xticks([0, 1], [country1, country2])
                    st.pyplot(plt)

                    # Yatay Bar Plot (Yıllara göre ortalama değerler)
                    plt.figure(figsize=(10, 6))
                    yearly_avg = combined_df.groupby(['Year', 'Dataset'])[metric_column].mean().unstack()
                    yearly_avg.plot(kind='barh', color=['blue', 'red'])
                    plt.title(f"{metric1} Yıllık Ortalamaları: {country1} vs {country2}")
                    plt.xlabel(f"{metric1} Değeri")
                    plt.ylabel("Yıl")
                    plt.legend([country1, country2])
                    st.pyplot(plt)

                else:
                    st.warning("Seçilen metrik için geçerli veri bulunamadı.")
            else:
                st.warning(f"{metric_column} sütunu veri setlerinde bulunamadı.")
        else:
            st.write("Veriler yüklenemedi.")


# x ve y paramatrelerini min yil max yil olarak secilen sekilde yap bunu da grafikte yerine koydur
# grafikte cok fazla fiyat degerini yazdirmak yerine araliklari yazdirsa kafi
# cekilen ve cekilecek verileri bir yere not et.
#oncelikle canada 1 series ve eu bmw 1 series den veri cek
# veri sayisini dogru cek.
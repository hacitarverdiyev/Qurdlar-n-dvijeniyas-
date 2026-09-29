import streamlit as st
import pandas as pd
import os

DATA_FILE = "tapshiriqlar.csv"
EXCEL_FILE = "Umumi_Tedbirler_Plani_Senedlerle_Is.xlsx"

st.title("📊 Şöbə İdarəetmə və Tədbirlər Paneli")

# 1. Bütün məlumatların (Excel cədvəlinin) işçilər tərəfindən görünməsi
st.subheader("📁 Şöbələrin Ümumi Tədbirlər Planı")
if os.path.exists(EXCEL_FILE):
    excel_df = pd.read_excel(EXCEL_FILE)
    st.dataframe(excel_df, use_container_width=True)
    
    with open(EXCEL_FILE, "rb") as f:
        st.download_button(
            label="📥 Excel Faylını Yüklə",
            data=f,
            file_name=EXCEL_FILE,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
else:
    st.info("Hələ ki Excel fayl yüklənməyib.")

st.markdown("---")

# 2. Operativ Tapşırıqlar Siyahısı (Bütün işçilər bütün tapşırıqları görür)
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=["Tapşırıq", "İcraçı", "Status"])

st.subheader("📌 Bütün Cari Tapşırıqlar")

# Yeni tapşırıq əlavə etmək (rəis və ya işçi)
yeni = st.text_input("Yeni tapşırıq əlavə et:")
icraci = st.selectbox("İcraçı seçin:", ["İşçi 1", "İşçi 2", "İşçi 3"])

if st.button("Əlavə Et"):
    if yeni:
        yeni_setir = pd.DataFrame({"Tapşırıq": [yeni], "İcraçı": [icraci], "Status": ["Gözləmədə"]})
        df = pd.concat([df, yeni_setir], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("Tapşırıq əlavə olundu!")
        st.rerun()

if not df.empty:
    # Cədvəli tam olaraq göstəririk ki, hər kəs bütün işləri görsün
    st.dataframe(df, use_container_width=True)
    
    st.subheader("🔄 Tapşırıq Statusunu Yenilə")
    index = st.number_input("Tapşırıq nömrəsi (Index):", min_value=0, max_value=max(0, len(df)-1), step=1)
    status = st.selectbox("Yeni status:", ["Gözləmədə", "İcrada", "Tamamlandı"])
    
    if st.button("Statusu Yenilə"):
        df.loc[index, "Status"] = status
        df.to_csv(DATA_FILE, index=False)
        st.success("Status yeniləndi!")
        st.rerun()
else:
    st.info("Hələ ki operativ tapşırıq yoxdur.")

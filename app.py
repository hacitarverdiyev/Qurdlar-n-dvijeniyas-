import streamlit as st
import pandas as pd
import os

DATA_FILE = "tapshiriqlar.csv"

if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=["Tapşırıq", "İcraçı", "Status"])

st.title("📌 Şöbə İdarəetmə Paneli")

# Yeni tapşırıq əlavə etmək
yeni = st.text_input("Yeni tapşırıq daxil edin:")
icraci = st.selectbox("İcraçı seçin:", ["İşçi 1", "İşçi 2", "İşçi 3"])

if st.button("Əlavə Et"):
    if yeni:
        yeni_setir = pd.DataFrame({"Tapşırıq": [yeni], "İcraçı": [icraci], "Status": ["Gözləmədə"]})
        df = pd.concat([df, yeni_setir], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("Tapşırıq əlavə olundu!")
        st.rerun()

st.subheader("Cari Tapşırıqlar Siyahısı")
if not df.empty:
    st.dataframe(df, use_container_width=True)
    
    # Statusu dəyişmək
    index = st.number_input("Tapşırıq nömrəsi (Index):", min_value=0, max_value=max(0, len(df)-1), step=1)
    status = st.selectbox("Yeni status:", ["Gözləmədə", "İcrada", "Tamamlandı"])
    
    if st.button("Statusu Yenilə"):
        df.loc[index, "Status"] = status
        df.to_csv(DATA_FILE, index=False)
        st.success("Status yeniləndi!")
        st.rerun()
else:
    st.info("Hələ ki tapşırıq yoxdur.")

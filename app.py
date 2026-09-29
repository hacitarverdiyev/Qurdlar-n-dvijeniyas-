import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Kasıb otağı", page_icon="👥")

DATA_FILE = "tapshiriqlar.csv"
EXCEL_FILE = "Umumi_Tedbirler_Plani_Senedlerle_Is.xlsx"

st.title("👥 Kasıb otağı")

# Əgər əvvəlcədən daxil olmayıbsa, şifrə istə
if "giris" not in st.session_state:
    st.session_state.giris = False

if not st.session_state.giris:
    sifre = st.text_input("Şifrəni daxil edin:", type="password")
    if st.button("Daxil ol"):
        if sifre == "123":
            st.session_state.giris = True
            st.rerun()
        else:
            st.error("Yanlış şifrə!")
else:
    if st.button("Çıxış"):
        st.session_state.giris = False
        st.rerun()

    st.subheader("📁 Şöbələrin Ümumi Tədbirlər Planı")
    if os.path.exists(EXCEL_FILE):
        excel_df = pd.read_excel(EXCEL_FILE)
        st.dataframe(excel_df, use_container_width=True)
        
        with open(EXCEL_FILE, "rb") as f:
            st.download_button("📥 Excel Yüklə", f, file_name=EXCEL_FILE)

    st.markdown("---")
    
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
    else:
        df = pd.DataFrame(columns=["Tapşırıq", "İcraçı", "Status"])

    st.subheader("📌 Tapşırıqlar")
    yeni = st.text_input("Yeni tapşırıq:")
    icraci = st.selectbox("İcraçı:", ["kasib 1", "kasib 2", "kasib 3"])

    if st.button("Əlavə Et"):
        if yeni:
            yeni_setir = pd.DataFrame({"Tapşırıq": [yeni], "İcraçı": [icraci], "Status": ["Gözləmədə"]})
            df = pd.concat([df, yeni_setir], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.rerun()

    if not df.empty:
        st.dataframe(df, use_container_width=True)
        index = st.number_input("Tapşırıq nömrəsi:", min_value=0, max_value=max(0, len(df)-1), step=1)
        status = st.selectbox("Status:", ["Gözləmədə", "İcrada", "Tamamlandı"])
        
        if st.button("Statusu Yenilə"):
            df.loc[index, "Status"] = status
            df.to_csv(DATA_FILE, index=False)
            st.rerun()

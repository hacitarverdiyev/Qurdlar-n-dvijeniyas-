import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Şöbə İdarəetmə", page_icon="👥")

DATA_FILE = "tapshiriqlar.csv"
EXCEL_FILE = "Umumi_Tedbirler_Plani_Senedlerle_Is.xlsx"

st.title("👥 Şöbə İdarəetmə və Tədbirlər Paneli - Giriş")

# Sessiyada giriş statusunu yoxlayırıq
if "giris_etdi" not in st.session_state:
    st.session_state.giris_etdi = False
    st.session_state.istifadeci = ""

if not st.session_state.giris_etdi:
    secilen_isci = st.selectbox("İşçi seçin:", ["Seçin...", "kasib 1", "kasib 2", "kasib 3"])
    sifre = st.text_input("Şifrənizi daxil edin:", type="password")
    
    if st.button("Daxil ol"):
        # Hər 3 işçi üçün ümumi və ya ayrı şifrə (məsələn: 123)
        if secilen_isci != "Seçin..." and sifre == "123":
            st.session_state.giris_etdi = True
            st.session_state.istifadeci = secilen_isci
            st.success(f"Xoş gəldiniz, {secilen_isci}!")
            st.rerun()
        else:
            st.error("Zəhmət olmasa işçi seçin və düzgün şifrə daxil edin! (Şifrə: 123)")
                
else:
    # Əgər daxil olubsa
    st.success(f"Sistemdəsiniz: **{st.session_state.istifadeci}**")
    if st.button("Çıxış et"):
        st.session_state.giris_etdi = False
        st.session_state.istifadeci = ""
        st.rerun()

    st.markdown("---")
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
    
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
    else:
        df = pd.DataFrame(columns=["Tapşırıq", "İcraçı", "Status"])

    st.subheader("📌 Bütün Cari Tapşırıqlar")
    
    yeni = st.text_input("Yeni tapşırıq əlavə et:")
    icraci = st.selectbox("İcraçı təyin et:", ["kasib 1", "kasib 2", "kasib 3"])

    if st.button("Əlavə Et"):
        if yeni:
            yeni_setir = pd.DataFrame({"Tapşırıq": [yeni], "İcraçı": [icraci], "Status": ["Gözləmədə"]})
            df = pd.concat([df, yeni_setir], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("Tapşırıq əlavə olundu!")
            st.rerun()

    if not df.empty:
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

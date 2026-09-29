import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Kasıb otağı", page_icon="👥")

EXCEL_FILE = "kasib_otagi_excel.xlsx"

st.title("👥 Kasıb otağı")

# Giriş sistemi (şifrə: 123)
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

    st.subheader("📁 Komanda Cədvəli və Excel Yükləmə")

    # Fayl yükləmə paneli (Upload)
    yuklenen_fayl = st.file_uploader("Excel faylını yüklə (.xlsx)", type=["xlsx", "xls"])
    
    if yuklenen_fayl is not None:
        # Fayl yüklənən kimi onu serverdə yadda saxlayırıq
        with open(EXCEL_FILE, "wb") as f:
            f.write(yuklenen_fayl.getbuffer())
        st.success("Excel fayl uğurla yükləndi!")

    # Mövcud faylı oxumaq və göstərmək
    if os.path.exists(EXCEL_FILE):
        try:
            df = pd.read_excel(EXCEL_FILE)
            st.markdown("---")
            st.subheader("📊 Cari Cədvəl Görünüşü")
            st.dataframe(df, use_container_width=True)
            
            # Faylı endirmək üçün düymə
            with open(EXCEL_FILE, "rb") as f:
                st.download_button(
                    label="📥 Cədvəli Excel Olaraq Endir",
                    data=f,
                    file_name="Kasib_Otagi_Plan.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        except Exception as e:
            st.error(f"Fayl oxunarkən xəta baş verdi: {e}")
    else:
        st.info("Zəhmət olmasa yuxarıdakı paneldən Excel faylınızı yükləyin.")

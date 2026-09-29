import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Kasıb otağı", page_icon="👥")

EXCEL_FILE = "yuklenen_sablon.xlsx"

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

    st.markdown("---")
    st.subheader("📁 Excel Faylını Yüklə")

    # Fayl yükləmə paneli
    yuklenen_fayl = st.file_uploader("Şablon Excel faylınızı seçin (.xlsx)", type=["xlsx", "xls"])
    
    if yuklenen_fayl is not None:
        with open(EXCEL_FILE, "wb") as f:
            f.write(yuklenen_fayl.getbuffer())
        st.success("Excel fayl uğurla yükləndi və vizuallaşdırıldı!")
        st.rerun()

    # Yüklənmiş fayl varsa, vizual olaraq ekranda göstəririk
    if os.path.exists(EXCEL_FILE):
        try:
            df = pd.read_excel(EXCEL_FILE)
            
            st.markdown("---")
            st.subheader("📊 Yüklənmiş Cədvəl Vizualı (Hər kəs üçün görünür)")
            
            # Cədvəli səliqəli şəkildə ekrana çıxarırıq
            st.dataframe(df, use_container_width=True)
            
            # Cədvəli yenidən endirmək üçün düymə
            with open(EXCEL_FILE, "rb") as f:
                st.download_button(
                    label="📥 Cari Excel Faylını Endir",
                    data=f,
                    file_name="Kasib_Otagi_Guncel.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        except Exception as e:
            st.error(f"Fayl oxunarkən xəta baş verdi: {e}")
    else:
        st.info("💡 Hələ ki Excel fayl yüklənməyib. Zəhmət olmasa kompüterinizdəki şablon Excel faylını yuxarıdan yükləyin.")

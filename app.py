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
    st.subheader("📁 Excel Faylını Yüklə və İdarə Et")

    # Fayl yükləmə paneli
    yuklenen_fayl = st.file_uploader("Şablon Excel faylınızı seçin (.xlsx)", type=["xlsx", "xls"])
    
    if yuklenen_fayl is not None:
        with open(EXCEL_FILE, "wb") as f:
            f.write(yuklenen_fayl.getbuffer())
        st.success("Excel fayl uğurla yadda saxlandı!")
        st.rerun()

    # Yüklənmiş faylı oxumağa çalışırıq
    df = None
    if os.path.exists(EXCEL_FILE):
        try:
            df = pd.read_excel(EXCEL_FILE)
        except Exception as e:
            st.warning(f"Fayl oxunarkən xəta oldu, standart cədvəl göstərilir: {e}")

    # Əgər hələ fayl yüklənməyibsə və ya oxunmursa, avtomatik nümunə göstəririk ki, ekran boş qalmasın
    if df is None or df.empty:
        data = {
            "Sıra sayı": [1, 2],
            "VÖEN": ["1234567890", "9876543210"],
            "VÖ": ["VÖ-01", "VÖ-02"],
            "Görülmüş işlər": ["Nümunə iş 1", "Nümunə iş 2"],
            "Görüləcək işlər": ["Nümunə plan 1", "Nümunə plan 2"],
            "Qeyd": ["Vacib", "Normal"]
        }
        df = pd.DataFrame(data)
        st.info("💡 Hələ ki öz Excel faylınızı yükləməmisiniz. Aşağıda nümunə cədvəl göstərilir. Fayl yüklədiyiniz zaman öz məlumatlarınız görünəcək:")

    st.markdown("---")
    st.subheader("📊 Cari Cədvəl Görünüşü")
    st.dataframe(df, use_container_width=True)
    
    # Endirmə düyməsi
    with open(EXCEL_FILE, "rb") if os.path.exists(EXCEL_FILE) else open("yuklenen_sablon.xlsx", "wb") as f:
        pass
    
    if os.path.exists(EXCEL_FILE):
        with open(EXCEL_FILE, "rb") as f:
            st.download_button(
                label="📥 Cari Excel Faylını Endir",
                data=f,
                file_name="Kasib_Otagi_Guncel.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

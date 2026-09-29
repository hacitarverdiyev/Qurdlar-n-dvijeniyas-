import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Kasıb otağı", page_icon="👥")

DATA_FILE = "kasib_otagi_melumatlar.csv"

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
    st.subheader("📁 Excel və ya CSV Faylını Yüklə (Upload)")

    # Fayl yükləmə paneli (həm .xlsx, həm .xls, həm .csv dəstəklənir)
    yuklenen_fayl = st.file_uploader("Faylınızı seçin (.xlsx, .xls, .csv)", type=["xlsx", "xls", "csv"])
    
    if yuklenen_fayl is not None:
        try:
            if yuklenen_fayl.name.endswith('.csv'):
                # Fərqli kodlaşdırmaları yoxlayaraq CSV oxuyuruq
                bytes_data = yuklenen_fayl.getvalue()
                yuklenen_df = None
                for encoding in ['utf-8', 'cp1251', 'latin-1', 'iso-8859-9']:
                    try:
                        from io import BytesIO
                        yuklenen_df = pd.read_csv(BytesIO(bytes_data), encoding=encoding)
                        break
                    except UnicodeDecodeError:
                        continue
            else:
                # Excel faylını openpyxl vasitəsilə oxuyuruq
                yuklenen_df = pd.read_excel(yuklenen_fayl)
            
            if yuklenen_df is not None:
                yuklenen_df.to_csv(DATA_FILE, index=False, encoding='utf-8-sig')
                st.success("Fayl uğurla yükləndi və cədvəl yeniləndi!")
                st.rerun()
            else:
                st.error("Fayl oxuna bilmədi.")
        except Exception as e:
            st.error(f"Fayl oxunarkən xəta baş verdi: {e}")

    st.markdown("---")
    st.subheader("📊 Komanda İdarəetmə Cədvəli")

    # Məlumatları oxumaq və ya ilkin cədvəl yaratmaq
    if os.path.exists(DATA_FILE):
        try:
            df = pd.read_csv(DATA_FILE, encoding='utf-8-sig')
        except:
            df = pd.read_csv(DATA_FILE, encoding='cp1251')
    else:
        data = {
            "Sıra sayı": [1, 2],
            "VÖEN": ["1234567890", "9876543210"],
            "VÖ": ["VÖ-01", "VÖ-02"],
            "Görülmüş işlər": ["Nümunə görülmüş iş 1", "Nümunə görülmüş iş 2"],
            "Görüləcək işlər": ["Nümunə görüləcək iş 1", "Nümunə görüləcək iş 2"],
            "Qeyd": ["Vacib", "Normal"]
        }
        df = pd.DataFrame(data)
        df.to_csv(DATA_FILE, index=False, encoding='utf-8-sig')

    # Cədvəli ekranda vizual olaraq göstəririk
    st.dataframe(df, use_container_width=True)

    # Cədvəli endirmək üçün düymə
    csv_data = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 Cədvəli Fayl Olaraq Endir",
        data=csv_data,
        file_name="Kasib_Otagi_Plan.csv",
        mime="text/csv"
    )

    st.markdown("---")
    st.subheader("➕ Cədvəliyə Yeni Məlumat Əlavə Et")

    with st.form("yeni_melumat_formu"):
        sira = st.number_input("Sıra sayı", min_value=1, step=1, value=len(df)+1)
        voen = st.text_input("VÖEN")
        vo = st.text_input("VÖ")
        gorulmus = st.text_area("Görülmüş işlər")
        gorulecek = st.text_area("Görüləcək işlər")
        qeyd = st.text_input("Qeyd")
        
        submit = st.form_submit_button("Əlavə Et")
        
        if submit:
            yeni_setir = pd.DataFrame({
                "Sıra sayı": [sira],
                "VÖEN": [voen],
                "VÖ": [vo],
                "Görülmüş işlər": [gorulmus],
                "Görüləcək işlər": [gorulecek],
                "Qeyd": [qeyd]
            })
            df = pd.concat([df, yeni_setir], ignore_index=True)
            df.to_csv(DATA_FILE, index=False, encoding='utf-8-sig')
            st.success("Məlumat uğurla əlavə olundu!")
            st.rerun()

    # Sətir silmək bölməsi
    if not df.empty:
        st.markdown("---")
        st.subheader("🗑️ Sətir Sil")
        silinecek_index = st.number_input("Silinəcək sətrin nömrəsi (Index)", min_value=0, max_value=max(0, len(df)-1), step=1)
        if st.button("Seçilmiş Sətri Sil"):
            df = df.drop(silinecek_index).reset_index(drop=True)
            df.to_csv(DATA_FILE, index=False, encoding='utf-8-sig')
            st.success("Sətir silindi!")
            st.rerun()

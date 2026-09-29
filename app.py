import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Kasıb otağı", page_icon="👥")

DATA_FILE = "kasib_otagi_cedvel.csv"

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

    st.subheader("📋 Komanda İzləmə Cədvəli")

    # Məlumatları oxumaq və ya yaratmaq
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
    else:
        df = pd.DataFrame(columns=[
            "Sıra sayı", 
            "VÖEN", 
            "VÖ", 
            "Görülmüş işlər", 
            "Görüləcək işlər", 
            "Qeyd"
        ])

    # Cədvəli ekranda göstərmək
    st.dataframe(df, use_container_width=True)

    st.markdown("---")
    st.subheader("➕ Yeni Məlumat / Sətir Əlavə Et")

    with st.form("yeni_melumat_formu"):
        sira = st.number_input("Sıra sayı", min_value=1, step=1, value=len(df)+1)
        voen = st.text_input("VÖEN")
        vo = st.text_input("VÖ")
        gorulmus = st.text_area("Görülmüş işlər")
        gorulecek = st.text_area("Görüləcək işlər")
        qeyd = st.text_input("Qeyd")
        
        submit = st.form_submit_button("Cədvəliyə Əlavə Et")
        
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
            df.to_csv(DATA_FILE, index=False)
            st.success("Məlumat uğurla əlavə olundu!")
            st.rerun()

    # Məlumat silmək və ya təmizləmək üçün imkan
    if not df.empty:
        st.markdown("---")
        st.subheader("🗑️ Sətir Sil")
        silinecek_index = st.number_input("Silinəcək sətrin nömrəsi (Index)", min_value=0, max_value=max(0, len(df)-1), step=1)
        if st.button("Seçilmiş Sətri Sil"):
            df = df.drop(silinecek_index).reset_index(drop=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("Sətir silindi!")
            st.rerun()

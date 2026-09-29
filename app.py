import streamlit as st

# Sadə şifrə sistemi
st.title("🔐 Şöbə İdarəetmə Sistemi - Giriş")

rol = st.selectbox("Giriş növünü seçin:", ["İşçi", "Rəis"])

if rol == "İşçi":
    sifre = st.text_input("İşçi şifrəsini daxil edin:", type="password")
    if sifre == "isçi123": # İşçilər üçün ümumi şifrə
        st.success("Xoş gəldiniz, İşçi!")
        # İşçinin görəcəyi və status yeniləyəcəyi hissə bura yazılır
    elif sifre != "":
        st.error("Yanlış şifrə!")

elif rol == "Rəis":
    sifre = st.text_input("Rəis şifrəsini daxil edin:", type="password")
    if sifre == "rəis123": # Rəis üçün xüsusi şifrə
        st.success("Xoş gəldiniz, Rəis!")
        # Rəisin yeni tapşırıq təyin etmə və bütün cədvəli görmə paneli bura yazılır
    elif sifre != "":
        st.error("Yanlış şifrə!")

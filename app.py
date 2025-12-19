import streamlit as st
import google.generativeai as genai

# --- YAPILANDIRMA ---
# Ücretsiz (Free Tier) API Anahtarın
GOOGLE_API_KEY = "AIzaSyBD7bkSlO50pqkOlHjPj7LYBddP8J25REk"
genai.configure(api_key=GOOGLE_API_KEY)

# Free Tier'da en stabil çalışan ana model ismi
model = genai.GenerativeModel('gemini-pro')

st.set_page_config(page_title="Xreas AI - İçerik Botu", layout="wide", page_icon="🤖")

# --- GİRİŞ SİSTEMİ ---
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🔐 Xreas AI Giriş")
    pw = st.text_input("Demo Şifresi:", type="password")
    if st.button("Sistemi Başlat"):
        if pw == "R10DEMO":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Hatalı Şifre!")
else:
    # --- ANA PANEL ---
    st.sidebar.title("🚀 Xreas AI v2.5")
    st.sidebar.info("Mod: Ücretsiz Sürüm")
    
    topic = st.sidebar.text_input("Anahtar Kelime:", placeholder="Örn: Araba bakımı")
    
    st.title("📝 Yapay Zeka İçerik Editörü")
    st.write("Konunuzu yazın ve yapay zekanın makaleyi hazırlamasını bekleyin.")

    if st.sidebar.button("İçerik Üret ✨"):
        if topic:
            with st.spinner("İçerik hazırlanıyor..."):
                try:
                    # En sade prompt yapısı
                    prompt = f"Write a detailed blog post in Turkish about '{topic}'. Use SEO headers."
                    response = model.generate_content(prompt)
                    
                    if response.text:
                        # Görsel ve Metin Gösterimi
                        clean_topic = topic.replace(" ", "_")
                        img_url = f"https://pollinations.ai/p/{clean_topic}?width=800&height=400"
                        
                        st.image(img_url, caption="AI Kapak Görseli")
                        st.markdown("---")
                        st.markdown(response.text)
                        st.success("İçerik başarıyla üretildi!")
                except Exception as e:
                    st.error(f"Hata oluştu: {str(e)}")
                    st.info("Not: API kotanız dolmuş olabilir veya anahtarınız pasif olabilir.")
        else:
            st.warning("Lütfen bir konu girin.")

# --- FOOTER ---
st.sidebar.markdown("---")
st.sidebar.write("Developed for R10")

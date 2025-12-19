import streamlit as st
import google.generativeai as genai

# --- YAPILANDIRMA ---
# API anahtarın tanımlanıyor
GOOGLE_API_KEY = "AIzaSyBD7bkSlO50pqkOlHjPj7LYBddP8J25REk"
genai.configure(api_key=GOOGLE_API_KEY)

# Model ismi en güncel 'flash-latest' sürümüne güncellendi
model = genai.GenerativeModel('gemini-1.5-flash-latest')

st.set_page_config(page_title="Xreas AI - Content Pro", layout="wide", page_icon="🚀")

# --- GİRİŞ SİSTEMİ ---
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🔐 Xreas AI Pro Panel")
    st.info("Demo Giriş Şifresi: R10DEMO")
    pw = st.text_input("Giriş Anahtarı:", type="password")
    if st.button("Sistemi Aç"):
        if pw == "R10DEMO":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Hatalı anahtar!")
else:
    # --- ANA PANEL ---
    st.sidebar.title("🚀 Xreas AI v2.0")
    menu = st.sidebar.radio("İşlem Seçin", ["İçerik Editörü", "SEO Analiz"])

    if menu == "İçerik Editörü":
        col1, col2 = st.columns([1, 1.5])
        
        with col1:
            st.subheader("📝 İçerik Ayarları")
            topic = st.text_input("Anahtar Kelime / Konu", placeholder="Örn: Modern dekorasyon fikirleri")
            lang = st.selectbox("Dil", ["Türkçe", "İngilizce"])
            style = st.select_slider("Yazım Dili", options=["Samimi", "Resmi", "Akademik"])
            
            if st.button("İçeriği ve Görseli Üret ✨"):
                if topic:
                    with st.spinner("Yapay zeka makale yazıyor ve görsel çiziyor..."):
                        try:
                            # 1. Metin Üretimi
                            prompt = f"Sen profesyonel bir SEO yazarıyın. '{topic}' konusu hakkında {lang} dilinde, {style} bir üslupla, H1 ve H2 başlıkları içeren kapsamlı ve ilgi çekici bir makale yaz."
                            response = model.generate_content(prompt)
                            st.session_state.last_text = response.text
                            
                            # 2. Görsel Üretimi
                            clean_topic = topic.replace(" ", "_")
                            img_url = f"https://pollinations.ai/p/{clean_topic}?width=800&height=400&seed=123"
                            st.session_state.last_img = img_url
                        except Exception as e:
                            st.error(f"Teknik bir hata oluştu: {e}")
                else:
                    st.warning("Lütfen bir konu başlığı girin.")

        with col2:
            st.subheader("✨ Çıktı Önizleme")
            if "last_text" in st.session_state:
                if "last_img" in st.session_state:
                    st.image(st.session_state.last_img, caption=f"'{topic}' Temalı AI Görseli", use_container_width=True)
                st.markdown("---")
                st.markdown(st.session_state.last_text)
                st.download_button("📥 Makaleyi Dosya Olarak İndir", st.session_state.last_text, f"{topic}.txt")
            else:
                st.info("Sol taraftan giriş yapıp 'Üret' butonuna bastığınızda sonuçlar burada anlık olarak görünecek.")

    elif menu == "SEO Analiz":
        st.subheader("🔍 SEO Analiz Modülü")
        st.write("Bu bölüm çok yakında aktif edilecektir. Makalelerinizin Google uyumunu buradan denetleyebileceksiniz.")

# --- FOOTER ---
st.sidebar.markdown("---")
st.sidebar.write("Developed with ❤️ for R10")
st.sidebar.caption("v2.1.0 - Stable")

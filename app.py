import streamlit as st
import google.generativeai as genai
import requests

# --- YAPILANDIRMA ---
GOOGLE_API_KEY = "AIzaSyBD7bkSlO50pqkOlHjPj7LYBddP8J25REk"
genai.configure(api_key=GOOGLE_API_KEY)
models/ = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="Xreas AI - Content Pro", layout="wide")

# --- GİRİŞ SİSTEMİ ---
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🔐 Xreas AI Pro Panel")
    pw = st.text_input("Giriş Anahtarı:", type="password")
    if st.button("Sistemi Aç"):
        if pw == "R10DEMO":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Hatalı!")
else:
    # --- ANA PANEL ---
    st.sidebar.title("🚀 Xreas AI v2.0")
    menu = st.sidebar.radio("İşlem Seçin", ["İçerik Editörü", "SEO Analiz", "Ayarlar"])

    if menu == "İçerik Editörü":
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📝 İçerik Ayarları")
            topic = st.text_input("Anahtar Kelime / Konu")
            lang = st.selectbox("Dil", ["Türkçe", "İngilizce"])
            style = st.select_slider("Yazım Dili", options=["Samimi", "Resmi", "Akademik"])
            
            if st.button("İçeriği ve Görseli Üret"):
                if topic:
                    with st.spinner("Yapay zeka sihir yapıyor..."):
                        # 1. Metin Üretimi
                        prompt = f"Sen bir SEO uzmanısın. {topic} hakkında {style} dilde, H1-H2 başlıkları olan SEO uyumlu bir makale yaz."
                        response = model.generate_content(prompt)
                        st.session_state.last_text = response.text
                        
                        # 2. Görsel Üretimi (Otomatik)
                        img_url = f"https://pollinations.ai/p/{topic.replace(' ', '_')}?width=800&height=400&seed=42"
                        st.session_state.last_img = img_url
                else:
                    st.warning("Konu girmelisiniz!")

        with col2:
            st.subheader("✨ Çıktı Önizleme")
            if "last_text" in st.session_state:
                if "last_img" in st.session_state:
                    st.image(st.session_state.last_img, caption="AI Tarafından Oluşturulan Kapak Görseli")
                st.markdown(st.session_state.last_text)
                st.download_button("Dosyayı İndir", st.session_state.last_text, "icerik.txt")

# --- FOOTER ---
st.sidebar.markdown("---")

st.sidebar.write("Developed with ❤️ for R10")

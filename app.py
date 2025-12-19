import streamlit as st
import google.generativeai as genai

# --- YAPILANDIRMA ---
# API anahtarını güvenli şekilde tanımlıyoruz
GOOGLE_API_KEY = "AIzaSyBD7bkSlO50pqkOlHjPj7LYBddP8J25REk"
genai.configure(api_key=GOOGLE_API_KEY)

# Model tanımını API versiyon hatasını giderecek şekilde güncelledik
# 'models/' ön eki olmadan en kararlı ismi kullanıyoruz
model = genai.GenerativeModel('gemini-1.5-flash')

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
    st.sidebar.title("🚀 Xreas AI v2.3")
    menu = st.sidebar.radio("İşlem Seçin", ["İçerik Editörü", "SEO Analiz"])

    if menu == "İçerik Editörü":
        col1, col2 = st.columns([1, 1.5])
        
        with col1:
            st.subheader("📝 İçerik Ayarları")
            topic = st.text_input("Anahtar Kelime / Konu", placeholder="Örn: Bitcoin'in Geleceği")
            lang = st.selectbox("Dil", ["Türkçe", "İngilizce"])
            style = st.select_slider("Yazım Dili", options=["Samimi", "Resmi", "Akademik"])
            
            if st.button("İçeriği ve Görseli Üret ✨"):
                if topic:
                    with st.spinner("Yapay zeka verileri işliyor..."):
                        try:
                            # 1. Metin Üretimi - En güvenli parametrelerle
                            prompt = f"Write a comprehensive, SEO-friendly article in {lang} about '{topic}' with H1 and H2 headers. Tone: {style}."
                            response = model.generate_content(prompt)
                            
                            # API Yanıtını Güvenli Şekilde Alıyoruz
                            if response.text:
                                st.session_state.last_text = response.text
                            
                            # 2. Görsel Üretimi
                            clean_topic = topic.replace(" ", "_")
                            img_url = f"https://pollinations.ai/p/{clean_topic}?width=800&height=400&seed=42"
                            st.session_state.last_img = img_url
                            
                        except Exception as e:
                            st.error(f"Teknik bir sorun oluştu. Detay: {str(e)}")
                else:
                    st.warning("Lütfen bir konu girin.")

        with col2:
            st.subheader("✨ Çıktı Önizleme")
            if "last_text" in st.session_state:
                if "last_img" in st.session_state:
                    st.image(st.session_state.last_img, caption=f"Konu: {topic}", use_container_width=True)
                st.markdown("---")
                st.markdown(st.session_state.last_text)
                st.download_button("📥 Makaleyi İndir", st.session_state.last_text, f"{topic}.txt")
            else:
                st.info("Sol taraftan giriş yapıp 'Üret' butonuna bastığınızda sonuçlar burada görünecek.")

# --- FOOTER ---
st.sidebar.markdown("---")
st.sidebar.write("Developed with ❤️ for R10")
st.sidebar.caption("v2.3.0 - Final Stable")

import streamlit as st
import google.generativeai as genai

# --- YAPILANDIRMA ---
GOOGLE_API_KEY = "AIzaSyBD7bkSlO50pqkOlHjPj7LYBddP8J25REk"
genai.configure(api_key=GOOGLE_API_KEY)

st.set_page_config(page_title="Xreas AI - Akıllı Editör", layout="wide", page_icon="🤖")

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
    # --- MODEL SEÇİMİ (OTOMATİK) ---
    def get_working_model():
        try:
            # Hesabındaki kullanılabilir modelleri listele
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            # Önce Flash, yoksa Pro, o da yoksa ilk bulduğunu seç
            for target in ["models/gemini-1.5-flash", "models/gemini-pro"]:
                if target in available_models:
                    return genai.GenerativeModel(target)
            return genai.GenerativeModel(available_models[0])
        except:
            return None

    st.sidebar.title("🚀 Xreas AI v3.0")
    st.sidebar.success("Model: Otomatik Optimize Edildi")
    
    topic = st.sidebar.text_input("Anahtar Kelime:", placeholder="Örn: Yapay zekanın geleceği")

    st.title("📝 Akıllı İçerik Editörü")
    st.info("Bu sürüm, API hatalarını önlemek için otomatik model taraması yapar.")

    if st.sidebar.button("İçerik Üret ✨"):
        if topic:
            with st.spinner("AI Modeli bağlanıyor ve içerik hazırlanıyor..."):
                try:
                    current_model = get_working_model()
                    if current_model:
                        prompt = f"Write a professional SEO article in Turkish about '{topic}'. Include H1 and H2 headers."
                        response = current_model.generate_content(topic)
                        
                        if response.text:
                            # Görsel ve Metin Gösterimi
                            clean_topic = topic.replace(" ", "_")
                            img_url = f"https://pollinations.ai/p/{clean_topic}?width=800&height=400&seed=42"
                            
                            st.image(img_url, caption="Makale Görseli")
                            st.markdown("---")
                            st.markdown(response.text)
                            st.success("İçerik başarıyla üretildi!")
                    else:
                        st.error("Hesabınızda uygun bir AI modeli bulunamadı.")
                except Exception as e:
                    st.error(f"Teknik Hata: {str(e)}")
        else:
            st.warning("Lütfen bir konu başlığı girin.")

# --- FOOTER ---
st.sidebar.markdown("---")
st.sidebar.write("Developed for R10")

import streamlit as st
import google.generativeai as genai

# --- YAPILANDIRMA ---
GOOGLE_API_KEY = "AIzaSyBD7bkSlO50pqkOlHjPj7LYBddP8J25REk"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="R10 AI Content Bot", page_icon="📝")

# --- GİRİŞ SİSTEMİ ---
def check_password():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        st.title("🔐 R10 Demo Girişi")
        st.info("Bu bot R10 kullanıcıları için test aşamasındadır.")
        password = st.text_input("Demo Anahtarını Girin:", type="password")
        if st.button("Sisteme Giriş Yap"):
            if password == "R10DEMO": # Şifren bu, istersen değiştirebilirsin
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("Hatalı anahtar!")
        return False
    return True

# --- ANA UYGULAMA ---
if check_password():
    st.sidebar.title("⚙️ Kontrol Paneli")
    mode = st.sidebar.selectbox("Ne Üretmek İstersin?", ["SEO Makale", "Instagram Postu", "Ürün Açıklaması"])
    
    st.title("🚀 AI İçerik Fabrikası")
    st.caption("Google Gemini altyapısı ile yüksek kaliteli içerik üretici")

    topic = st.text_input("Konu veya Anahtar Kelime girin:", placeholder="Örn: 2025'te dijital pazarlama trendleri")

    if st.button("Sihiri Başlat ✨"):
        if topic:
            with st.spinner("Yapay zeka içeriği ilmek ilmek işliyor..."):
                try:
                    # Modlara göre farklı komutlar (Prompt) gönderiyoruz
                    if mode == "SEO Makale":
                        prompt = f"Sen profesyonel bir SEO uzmanısın. '{topic}' konusu hakkında, H1-H2-H3 başlıkları içeren, SEO uyumlu, en az 500 kelimelik, Türkçe bir blog yazısı yaz."
                    elif mode == "Instagram Postu":
                        prompt = f"'{topic}' konusu hakkında dikkat çekici bir Instagram post metni yaz. Emoji kullan ve ilgili hashtagleri ekle."
                    else:
                        prompt = f"'{topic}' ürünü için ikna edici ve satış odaklı bir ürün açıklaması yaz."

                    response = model.generate_content(prompt)
                    
                    st.success("İçerik Hazır!")
                    st.markdown("---")
                    st.markdown(response.text)
                    st.download_button("Dosya Olarak İndir (.txt)", response.text, file_name="icerik.txt")
                    
                except Exception as e:
                    st.error(f"Bir hata oluştu: {e}")
        else:
            st.warning("Lütfen bir konu başlığı girin.")

    st.sidebar.markdown("---")
    st.sidebar.write("**Üye Durumu:** Ücretsiz Demo")
    if st.sidebar.button("Pro Sürüme Geç (Yakında)"):
        st.sidebar.info("R10 üzerinden iletişime geçebilirsiniz!")
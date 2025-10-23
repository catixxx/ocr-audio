import streamlit as st
import os
import time
import glob
import cv2
import numpy as np
import pytesseract
from PIL import Image
from gtts import gTTS
from googletrans import Translator

# ============================
# CONFIGURACIÓN DE LA PÁGINA
# ============================
st.set_page_config(page_title="🌸 Reconocimiento Óptico de Caracteres", layout="wide")

# === ESTILO CSS FLORAL Y FONDO BLANCO ===
st.markdown("""
<style>
/* Fondo blanco total */
[data-testid="stAppViewContainer"] {
    background-color: #ffffff !important;
}

/* Barra lateral con verde menta muy claro */
[data-testid="stSidebar"] {
    background-color: #f1faee !important;
    border-right: 3px solid #a5d6a7;
}

/* Títulos con tonos florales */
h1, h2, h3 {
    color: #7b4b94;
    font-family: 'Georgia', serif;
    text-align: center;
}

/* Botones suaves con efecto pastel */
.stButton>button {
    background-color: #f8bbd0 !important;
    color: white !important;
    border-radius: 15px !important;
    border: none !important;
    font-size: 16px !important;
    padding: 0.5em 1.5em !important;
    font-weight: bold !important;
}

.stButton>button:hover {
    background-color: #f48fb1 !important;
    transition: 0.3s;
}

/* Cuadro de carga de archivos */
[data-testid="stFileUploader"] {
    background-color: #fffafc !important;
    border-radius: 10px;
    border: 2px dashed #f8bbd0;
    padding: 10px;
}

/* Texto general */
body, label, p, span {
    color: #444444 !important;
    font-family: 'Trebuchet MS', sans-serif !important;
}
</style>
""", unsafe_allow_html=True)

# ============================
# FUNCIONES
# ============================
def text_to_speech(input_language, output_language, text, tld):
    translator = Translator()
    translation = translator.translate(text, src=input_language, dest=output_language)
    trans_text = translation.text
    tts = gTTS(trans_text, lang=output_language, tld=tld, slow=False)
    try:
        my_file_name = text[0:20]
    except:
        my_file_name = "audio"
    os.makedirs("temp", exist_ok=True)
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, trans_text

# ============================
# INTERFAZ
# ============================
st.title("🌷 Reconocimiento Óptico de Caracteres 🌷")
st.markdown("**Captura o carga una imagen para extraer su texto y traducirlo con un estilo floral. 💐**")

cam_ = st.checkbox("📸 Usar Cámara")

if cam_:
    img_file_buffer = st.camera_input("Toma una Foto")
else:
    img_file_buffer = None

bg_image = st.file_uploader("📁 Cargar Imagen:", type=["png", "jpg", "jpeg"])

# --- Sidebar floral ---
with st.sidebar:
    st.header("🌼 Procesamiento de imagen")
    filtro = st.radio("¿Aplicar filtro de inversión de color?", ('Sí', 'No'))

    st.header("🌻 Parámetros de Traducción")
    in_lang = st.selectbox("Lenguaje de entrada", ("Inglés", "Español", "Francés", "Italiano", "Alemán"))
    out_lang = st.selectbox("Lenguaje de salida", ("Inglés", "Español", "Francés", "Italiano", "Alemán"))
    accent = st.selectbox("🎧 Selecciona el acento", ("Default", "India", "United Kingdom", "United States", "Australia"))
    display_output_text = st.checkbox("🌸 Mostrar texto traducido")

# ============================
# PROCESAMIENTO DE IMAGEN
# ============================
text = ""

if bg_image is not None:
    img_cv = cv2.imdecode(np.frombuffer(bg_image.read(), np.uint8), cv2.IMREAD_COLOR)
    if filtro == 'Sí':
        img_cv = cv2.bitwise_not(img_cv)
    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
    text = pytesseract.image_to_string(img_rgb)
    st.subheader("🪷 Texto detectado:")
    st.write(text)

if img_file_buffer is not None:
    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    if filtro == 'Sí':
        cv2_img = cv2.bitwise_not(cv2_img)
    img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    text = pytesseract.image_to_string(img_rgb)
    st.subheader("🌹 Texto detectado (desde cámara):")
    st.write(text)

# ============================
# TRADUCCIÓN Y AUDIO
# ============================
if st.button("🎧 Convertir a Audio"):
    if text.strip():
        input_lang = {'Inglés': 'en', 'Español': 'es', 'Francés': 'fr', 'Italiano': 'it', 'Alemán': 'de'}[in_lang]
        output_lang = {'Inglés': 'en', 'Español': 'es', 'Francés': 'fr', 'Italiano': 'it', 'Alemán': 'de'}[out_lang]
        tld = "com"
        result, translated_text = text_to_speech(input_lang, output_lang, text, tld)
        audio_file = open(f"temp/{result}.mp3", "rb")
        st.audio(audio_file.read(), format="audio/mp3")
        if display_output_text:
            st.subheader("🌺 Texto traducido:")
            st.write(translated_text)
    else:
        st.warning("⚠️ Por favor, carga o captura una imagen con texto antes de convertir.")

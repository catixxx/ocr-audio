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
st.set_page_config(page_title="Reconocimiento Óptico de Caracteres 🌸", layout="wide")

# Fondo verde claro con flores decorativas
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #e8f5e9; /* Verde claro */
    background-image: url("https://i.imgur.com/h2YtPqK.png");
    background-size: contain;
}

h1, h2, h3 {
    color: #3d5c3d;
    font-family: "Georgia", serif;
}

.sidebar .sidebar-content {
    background-color: #f0fff0;
}

.stButton>button {
    background-color: #c8e6c9;
    color: #2e7d32;
    border-radius: 10px;
    border: 1px solid #81c784;
    font-size: 16px;
    font-weight: bold;
}

.stButton>button:hover {
    background-color: #a5d6a7;
    color: #1b5e20;
}

.css-1v3fvcr {
    background-color: #f8fff8;
}

[data-testid="stSidebar"] {
    background: #f1f8e9;
    border-right: 2px solid #a5d6a7;
}

[data-testid="stSidebar"] h2 {
    color: #2e7d32;
}

hr {
    border: 1px solid #81c784;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# ============================
# FUNCIONES
# ============================
text = " "

def text_to_speech(input_language, output_language, text, tld):
    translator = Translator()
    translation = translator.translate(text, src=input_language, dest=output_language)
    trans_text = translation.text
    tts = gTTS(trans_text, lang=output_language, tld=tld, slow=False)
    my_file_name = text[:20] if text else "audio"
    if not os.path.exists("temp"):
        os.makedirs("temp")
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, trans_text

def remove_files(n):
    mp3_files = glob.glob("temp/*.mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)
                print("Deleted ", f)

remove_files(7)

# ============================
# INTERFAZ PRINCIPAL
# ============================
st.title("🌷 Reconocimiento Óptico de Caracteres 🌷")
st.subheader("Captura o carga una imagen para extraer su texto y traducirlo con estilo floral 💐")

cam_ = st.checkbox("📸 Usar Cámara")

if cam_:
    img_file_buffer = st.camera_input("Toma una Foto")
else:
    img_file_buffer = None

with st.sidebar:
    st.header("🌼 Procesamiento de imagen")
    filtro = st.radio("¿Aplicar filtro de inversión de color?", ('Sí', 'No'))

bg_image = st.file_uploader("🌺 Cargar Imagen:", type=["png", "jpg"])
if bg_image is not None:
    uploaded_file = bg_image
    st.image(uploaded_file, caption='🌸 Imagen cargada.', use_container_width=True)
    with open(uploaded_file.name, 'wb') as f:
        f.write(uploaded_file.read())
    st.success(f"Imagen guardada como {uploaded_file.name}")
    img_cv = cv2.imread(uploaded_file.name)
    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
    text = pytesseract.image_to_string(img_rgb)
    st.write("🌿 Texto detectado:")
    st.write(text)

if img_file_buffer is not None:
    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    if filtro == 'Sí':
        cv2_img = cv2.bitwise_not(cv2_img)
    img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    text = pytesseract.image_to_string(img_rgb)
    st.write("🌷 Texto detectado:")
    st.write(text)

with st.sidebar:
    st.header("🌻 Parámetros de Traducción")

    translator = Translator()

    in_lang = st.selectbox("Lenguaje de entrada", ["Inglés", "Español", "Bengalí", "Coreano", "Mandarín", "Japonés"])
    out_lang = st.selectbox("Lenguaje de salida", ["Inglés", "Español", "Bengalí", "Coreano", "Mandarín", "Japonés"])

    lang_codes = {
        "Inglés": "en", "Español": "es", "Bengalí": "bn",
        "Coreano": "ko", "Mandarín": "zh-cn", "Japonés": "ja"
    }

    input_language = lang_codes[in_lang]
    output_language = lang_codes[out_lang]

    english_accent = st.selectbox(
        "🌸 Selecciona el acento",
        ["Default", "India", "United Kingdom", "United States", "Canada", "Australia", "Ireland", "South Africa"]
    )

    tld_map = {
        "Default": "com", "India": "co.in", "United Kingdom": "co.uk",
        "United States": "com", "Canada": "ca", "Australia": "com.au",
        "Ireland": "ie", "South Africa": "co.za"
    }
    tld = tld_map[english_accent]

    display_output_text = st.checkbox("🌼 Mostrar texto traducido")

    if st.button("🎧 Convertir a Audio"):
        if text.strip() != "":
            result, output_text = text_to_speech(input_language, output_language, text, tld)
            audio_file = open(f"temp/{result}.mp3", "rb")
            audio_bytes = audio_file.read()
            st.markdown("## 🌿 Tu audio:")
            st.audio(audio_bytes, format="audio/mp3")
            if display_output_text:
                st.markdown("## 🌸 Texto traducido:")
                st.write(output_text)
        else:
            st.warning("Por favor, carga una imagen o toma una foto para procesar 🌷")

            st.warning("🌷 No hay texto para convertir. Captura o carga una imagen primero.")

# 🌻 Pie de página
st.markdown("---")

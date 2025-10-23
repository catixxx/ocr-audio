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

# 🌸 Configuración general de la app
st.set_page_config(
    page_title="🌷 OCR Floral Traductor y Lector",
    page_icon="🌸",
    layout="wide"
)

# 🌺 Estilo floral personalizado
st.markdown("""
<style>
body {
    background: linear-gradient(120deg, #ffeef2, #fef6e4, #e7f9ed, #f8e8ff);
    background-size: 400% 400%;
    animation: gradientBG 15s ease infinite;
    font-family: 'Poppins', cursive;
}
@keyframes gradientBG {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}
h1, h2, h3 {
    color: #b35ea0;
    text-align: center;
    font-weight: 700;
}
.sidebar .sidebar-content {
    background: linear-gradient(180deg, #fff0f6, #fce1f7, #f4e1ff);
    border-radius: 15px;
    padding: 25px;
    border: 2px solid #f9d7ea;
}
.stButton > button {
    background: linear-gradient(90deg, #fbc2eb, #a6c1ee);
    color: white;
    border: none;
    border-radius: 25px;
    font-size: 17px;
    padding: 10px 30px;
    font-weight: 600;
    transition: all 0.3s ease;
}
.stButton > button:hover {
    background: linear-gradient(90deg, #fda085, #f6d365);
    transform: scale(1.05);
}
.stCheckbox, .stRadio {
    background-color: #fffafc;
    border-radius: 15px;
    padding: 10px;
    margin-top: 10px;
}
.stFileUploader {
    border: 2px dashed #f5c6e2;
    border-radius: 15px;
    background-color: #fff7fa;
}
</style>
""", unsafe_allow_html=True)

# 🌷 Funciones principales
def text_to_speech(input_language, output_language, text, tld):
    translation = translator.translate(text, src=input_language, dest=output_language)
    trans_text = translation.text
    tts = gTTS(trans_text, lang=output_language, tld=tld, slow=False)
    try:
        my_file_name = text[0:20]
    except:
        my_file_name = "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, trans_text

def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)
                print("Deleted ", f)

remove_files(7)

# 🌼 Encabezado
st.title("🌸 Reconocimiento Óptico de Caracteres con Encanto Floral 🌼")
st.subheader("✨ Extrae texto, tradúcelo y escúchalo, rodeada de un toque de naturaleza y color ✨")

# 🌹 Selección de fuente de imagen
cam_ = st.checkbox("📸 Usar Cámara")

if cam_:
    img_file_buffer = st.camera_input("Toma una Foto 🌷")
else:
    img_file_buffer = None

# 🌼 Barra lateral decorada
with st.sidebar:
    st.header("🌿 Configuración de la Imagen 🌿")
    filtro = st.radio("¿Deseas aplicar un filtro floral a la imagen?", ('Sí', 'No'))
    st.markdown("---")
    st.header("🌸 Parámetros de Traducción 🌸")

    try:
        os.mkdir("temp")
    except:
        pass

    translator = Translator()

    in_lang = st.selectbox(
        "🌼 Lenguaje de entrada:",
        ("Inglés", "Español", "Bengalí", "Coreano", "Mandarín", "Japonés"),
    )
    input_codes = {
        "Inglés": "en",
        "Español": "es",
        "Bengalí": "bn",
        "Coreano": "ko",
        "Mandarín": "zh-cn",
        "Japonés": "ja"
    }
    input_language = input_codes[in_lang]

    out_lang = st.selectbox(
        "🌸 Lenguaje de salida:",
        ("Inglés", "Español", "Bengalí", "Coreano", "Mandarín", "Japonés"),
    )
    output_language = input_codes[out_lang]

    english_accent = st.selectbox(
        "🌺 Acento del audio:",
        (
            "Default", "India", "United Kingdom", "United States",
            "Canada", "Australia", "Ireland", "South Africa"
        ),
    )

    accents = {
        "Default": "com",
        "India": "co.in",
        "United Kingdom": "co.uk",
        "United States": "com",
        "Canada": "ca",
        "Australia": "com.au",
        "Ireland": "ie",
        "South Africa": "co.za",
    }
    tld = accents[english_accent]

    display_output_text = st.checkbox("🌻 Mostrar texto traducido")

# 🌸 Cargar imagen desde archivo
bg_image = st.file_uploader("🌼 Cargar Imagen desde tu dispositivo:", type=["png", "jpg", "jpeg"])
text = " "

if bg_image is not None:
    uploaded_file = bg_image
    st.image(uploaded_file, caption='🌸 Imagen cargada exitosamente', use_container_width=True)

    with open(uploaded_file.name, 'wb') as f:
        f.write(uploaded_file.read())

    img_cv = cv2.imread(uploaded_file.name)
    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
    text = pytesseract.image_to_string(img_rgb)
    st.success("🌷 Texto extraído con éxito:")
    st.write(text)

# 📷 Si se usa la cámara
if img_file_buffer is not None:
    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

    if filtro == 'Sí':
        cv2_img = cv2.bitwise_not(cv2_img)

    img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    text = pytesseract.image_to_string(img_rgb)
    st.success("🌺 Texto detectado:")
    st.write(text)

# 🌸 Botón de conversión
with st.sidebar:
    if st.button("🌼 Convertir a Audio"):
        if text.strip():
            result, output_text = text_to_speech(input_language, output_language, text, tld)
            audio_file = open(f"temp/{result}.mp3", "rb")
            audio_bytes = audio_file.read()
            st.markdown("### 🎧 Tu Audio Floral:")
            st.audio(audio_bytes, format="audio/mp3", start_time=0)

            if display_output_text:
                st.markdown("### 🌸 Texto traducido:")
                st.write(output_text)
        else:
            st.warning("🌷 No hay texto para convertir. Captura o carga una imagen primero.")

# 🌻 Pie de página
st.markdown("---")

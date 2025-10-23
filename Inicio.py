import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import re
from nltk.stem import SnowballStemmer

# =======================
# 🎧 CONFIGURACIÓN DE PÁGINA
# =======================
st.set_page_config(page_title="MusicSense – Analizador de Letras", layout="centered")

# =======================
# 🎨 ESTILO
# =======================
st.markdown("""
    <style>
        body { background-color: #0E1117; color: #E0E0E0; }
        .title { color: #E91E63; text-align: center; font-size: 2.4em; font-weight: bold; }
        .subtitle { text-align: center; color: #A0A0A0; font-size: 1.1em; }
        .stButton > button {
            background-color: #E91E63; color: white; border-radius: 10px;
            border: none; font-weight: bold; font-size: 1em;
        }
        .stButton > button:hover { background-color: #C2185B; }
        .emotion { font-size: 1.2em; text-align: center; margin-top: 10px; }
    </style>
""", unsafe_allow_html=True)

# =======================
# 🎵 TÍTULO Y DESCRIPCIÓN
# =======================
st.markdown("<div class='title'>🎶 MusicSense</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Analiza letras y descubre su energía emocional 🎧</div>", unsafe_allow_html=True)
st.write("")

# =======================
# 📝 EJEMPLOS DE LETRAS
# =======================
default_lyrics = """Hoy el sol brilla más fuerte y no puedo dejar de bailar.
Sigo atrapado en mis pensamientos, sin poder escapar.
Tu voz me eleva, me hace sentir en las nubes.
Nada tiene sentido cuando tú no estás.
Cantando en la lluvia, sin miedo a perder.
El silencio suena más alto cuando me faltas tú.
Una nueva melodía nació en mi corazón."""

stemmer = SnowballStemmer("spanish")

def tokenize_and_stem(text):
    text = text.lower()
    text = re.sub(r'[^a-záéíóúüñ\s]', ' ', text)
    tokens = [t for t in text.split() if len(t) > 1]
    stems = [stemmer.stem(t) for t in tokens]
    return stems

# =======================
# 🧠 INTERFAZ PRINCIPAL
# =======================
st.markdown("### Escribe o pega una letra musical 🎤")
text_input = st.text_area("Cada línea será una frase o verso:", default_lyrics, height=180)

st.markdown("### Tema principal o frase de referencia 🎵")
question = st.text_input("Por ejemplo:", "alegría y esperan_


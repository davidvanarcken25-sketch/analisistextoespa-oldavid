import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import re
from nltk.stem import SnowballStemmer

# --- ESTILO VISUAL ---
st.markdown(
    """
    <style>
    .title {
        color: #ff66b2; /* Rosado */
        text-align: center;
        font-size: 38px;
        font-weight: bold;
    }
    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #666;
    }
    .center-img {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 140px;
        border-radius: 10px;
    }
    .stButton>button {
        background-color: #ff66b2;
        color: white;
        border-radius: 10px;
        height: 3em;
        width: 100%;
        font-size: 1em;
        border: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- TÍTULOS ---
st.markdown('<h1 class="title">Word Factory 🔤</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Analiza cómo tus frases se conectan en esta fábrica de palabras inteligentes</p>', unsafe_allow_html=True)

# --- GIF temático ---
st.image(
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZ3A0cG1hYnFoN2YxYW9nOWtpZmhrY3NsZ3puc3B5ZnU4bnNhd2d3MiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/v1.Y2lkPTc5MGI3NjExbWptYml2Y3NzaXJyaGhhdzNraHc3M3lyYmN4eWFjcnl0ZWJ0bXEycyZjdD1n/MX6Q1CqZkFi0A6kU5p/giphy.gif",
    use_container_width=False,
    width=160
)

# --- DESCRIPCIÓN ---
st.write("""
Bienvenido a la **Word Factory**, donde tus textos se convierten en piezas de un rompecabezas lingüístico.  
Cada línea que escribas será una “pieza” o “ingrediente” que nuestra máquina analizará para descubrir cuál encaja mejor con tu pregunta.
""")

# --- ENTRADAS ---
text_input = st.text_area(
    "Ingresa tus documentos (uno por línea, en inglés):",
    "The robot loves words.\nThe factory creates new sentences.\nMachines can learn to understand language."
)

question = st.text_input("Escribe tu pregunta (en inglés):", "What does the factory create?")

# --- PROCESAMIENTO ---
stemmer = SnowballStemmer("english")

def tokenize_and_stem(text: str):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', ' ', text)
    tokens = [t for t in text.split() if len(t) > 1]
    stems = [stemmer.stem(t) for t in tokens]
    return stems

# --- ANÁLISIS TF-IDF ---
if st.button("Procesar en la fábrica de palabras"):
    documents = [d.strip() for d in text_input.split("\n") if d.strip()]
    if len(documents) < 1:
        st.warning("Por favor, ingresa al menos un documento.")
    else:
        vectorizer = TfidfVectorizer(
            tokenizer=tokenize_and_stem,
            stop_words="english",
            token_pattern=None
        )

        X = vectorizer.fit_transform(documents)

        df_tfidf = pd.DataFrame(
            X.toarray(),
            columns=vectorizer.get_feature_names_out(),
            index=[f"Doc {i+1}" for i in range(len(documents))]
        )

        st.write("### Mapa de ingredientes lingüísticos (TF-IDF)")
        st.dataframe(df_tfidf.round(3))

        question_vec = vectorizer.transform([question])
        similarities = cosine_similarity(question_vec, X).flatten()

        best_idx = similarities.argmax()
        best_doc = documents[best_idx]
        best_score = similarities[best_idx]

        st.write("### Resultado del análisis de la fábrica")
        st.write(f"**Tu pregunta:** {question}")
        st.write(f"**Texto más conectado (Doc {best_idx+1}):** {best_doc}")
        st.write(f"**Nivel de coincidencia:** {best_score:.3f}")

        sim_df = pd.DataFrame({
            "Documento": [f"Doc {i+1}" for i in range(len(documents))],
            "Texto": documents,
            "Similitud": similarities
        })
        st.write("### Puntuaciones de similitud entre piezas")
        st.dataframe(sim_df.sort_values("Similitud", ascending=False))

        vocab = vectorizer.get_feature_names_out()
        q_stems = tokenize_and_stem(question)
        matched = [s for s in q_stems if s in vocab and df_tfidf.iloc[best_idx].get(s, 0) > 0]
        st.write("### Palabras clave conectadas en el texto elegido:", matched)

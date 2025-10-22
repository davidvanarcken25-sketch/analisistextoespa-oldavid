import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import re
from nltk.stem import SnowballStemmer

# ======================
# CONFIGURACIÓN DE PÁGINA
# ======================
st.set_page_config(
    page_title="Análisis de texto (inglés) - Word Factory",
    page_icon="🧠",
    layout="wide"
)

# ======================
# ESTILO Y TÍTULO
# ======================
st.markdown("""
<div style='text-align:center'>
    <h1 style='color:#E91E63;'>Análisis de texto (inglés)</h1>
    <h3 style='color:#F06292;'>Word Factory — donde tus palabras cobran vida</h3>
</div>
""", unsafe_allow_html=True)

st.write("""
Bienvenido a **Word Factory**, un laboratorio lingüístico donde analizamos tus textos 
y descubrimos qué tan relacionados están con tus preguntas.  
Cada línea que escribas será tratada como un **documento** (una frase o párrafo independiente).

El sistema usa **TF-IDF** y *stemming* para reconocer similitudes, 
tratando palabras como *playing*, *played* o *play* como equivalentes.
""")

# ======================
# ENTRADAS
# ======================
text_input = st.text_area(
    "Escribe tus documentos (uno por línea, en inglés):",
    "The dog barks loudly.\nThe cat meows at night.\nThe dog and the cat play together."
)

question = st.text_input("Escribe una pregunta (en inglés):", "Who is playing?")

# ======================
# TOKENIZACIÓN Y STEMMING
# ======================
stemmer = SnowballStemmer("english")

def tokenize_and_stem(text: str):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', ' ', text)
    tokens = [t for t in text.split() if len(t) > 1]
    stems = [stemmer.stem(t) for t in tokens]
    return stems

# ======================
# PROCESAMIENTO
# ======================
if st.button("Analizar texto"):
    documents = [d.strip() for d in text_input.split("\n") if d.strip()]
    if len(documents) < 1:
        st.warning("Por favor, ingresa al menos un documento.")
    else:
        # Crear vectorizador TF-IDF
        vectorizer = TfidfVectorizer(
            tokenizer=tokenize_and_stem,
            stop_words="english",
            token_pattern=None
        )

        X = vectorizer.fit_transform(documents)

        # Mostrar matriz TF-IDF
        df_tfidf = pd.DataFrame(
            X.toarray(),
            columns=vectorizer.get_feature_names_out(),
            index=[f"Doc {i+1}" for i in range(len(documents))]
        )

        st.markdown("### Matriz TF-IDF (stems)")
        st.dataframe(df_tfidf.round(3))

        # Similitud con la pregunta
        question_vec = vectorizer.transform([question])
        similarities = cosine_similarity(question_vec, X).flatten()

        best_idx = similarities.argmax()
        best_doc = documents[best_idx]
        best_score = similarities[best_idx]

        st.markdown("### Resultado del análisis")
        st.write(f"**Tu pregunta:** {question}")
        st.write(f"**Documento más relevante (Doc {best_idx+1}):** {best_doc}")
        st.write(f"**Puntaje de similitud:** {best_score:.3f}")

        # Mostrar todas las similitudes
        sim_df = pd.DataFrame({
            "Documento": [f"Doc {i+1}" for i in range(len(documents))],
            "Texto": documents,
            "Similitud": similarities
        })
        st.markdown("### Puntajes de similitud")
        st.dataframe(sim_df.sort_values("Similitud", ascending=False))

        # Mostrar coincidencias de stems
        vocab = vectorizer.get_feature_names_out()
        q_stems = tokenize_and_stem(question)
        matched = [s for s in q_stems if s in vocab and df_tfidf.iloc[best_idx].get(s, 0) > 0]

        st.markdown("### Stems de la pregunta presentes en el documento elegido")
        st.write(matched)

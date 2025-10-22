import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import re
from nltk.stem import SnowballStemmer

# --- ESTILO VISUAL ---
st.markdown("""
    <style>
        body {
            background-color: #0E1117;
            color: #E0E0E0;
        }
        .title {
            color: #00BCD4;
            text-align: center;
            font-size: 2.2em;
            font-weight: bold;
        }
        .subtitle {
            text-align: center;
            color: #A0A0A0;
            font-size: 1.1em;
        }
        .stButton > button {
            background-color: #00BCD4;
            color: white;
            border-radius: 8px;
            border: none;
            font-weight: bold;
        }
        .stButton > button:hover {
            background-color: #0097A7;
        }
    </style>
""", unsafe_allow_html=True)

# --- TÍTULOS Y DESCRIPCIÓN ---
st.markdown("<div class='title'>TextoBot 3000</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Asistente de análisis textual con IA — versión de demostración</div>", unsafe_allow_html=True)
st.write("")

# --- DOCUMENTOS DE EJEMPLO ---
default_docs = """El perro ladra fuerte en el parque.
El gato maúlla suavemente durante la noche.
El perro y el gato juegan juntos en el jardín.
Los niños corren y se divierten en el parque.
La música suena muy alta en la fiesta.
Los pájaros cantan hermosas melodías al amanecer."""

stemmer = SnowballStemmer("spanish")

def tokenize_and_stem(text):
    text = text.lower()
    text = re.sub(r'[^a-záéíóúüñ\s]', ' ', text)
    tokens = [t for t in text.split() if len(t) > 1]
    stems = [stemmer.stem(t) for t in tokens]
    return stems

# --- INTERFAZ ---
col1, col2 = st.columns([2, 1])

with col1:
    text_input = st.text_area("📄 Documentos (uno por línea):", default_docs, height=150)
    question = st.text_input("❓ Escribe tu consulta:", "¿Dónde juegan el perro y el gato?")

with col2:
    st.markdown("### Sugerencias rápidas:")
    if st.button("¿Dónde juegan el perro y el gato?", use_container_width=True):
        st.session_state.question = "¿Dónde juegan el perro y el gato?"
        st.rerun()
    if st.button("¿Qué hacen los niños en el parque?", use_container_width=True):
        st.session_state.question = "¿Qué hacen los niños en el parque?"
        st.rerun()
    if st.button("¿Cuándo cantan los pájaros?", use_container_width=True):
        st.session_state.question = "¿Cuándo cantan los pájaros?"
        st.rerun()
    if st.button("¿Dónde suena la música alta?", use_container_width=True):
        st.session_state.question = "¿Dónde suena la música alta?"
        st.rerun()
    if st.button("¿Qué animal maúlla durante la noche?", use_container_width=True):
        st.session_state.question = "¿Qué animal maúlla durante la noche?"
        st.rerun()

if 'question' in st.session_state:
    question = st.session_state.question

# --- ANÁLISIS TF-IDF ---
if st.button("Analizar con TextoBot", type="primary"):
    documents = [d.strip() for d in text_input.split("\n") if d.strip()]
    if len(documents) < 1:
        st.error("Por favor, ingresa al menos un documento.")
    elif not question.strip():
        st.error("Escribe una pregunta o consulta para analizar.")
    else:
        vectorizer = TfidfVectorizer(
            tokenizer=tokenize_and_stem,
            min_df=1
        )
        X = vectorizer.fit_transform(documents)
        st.markdown("### Matriz TF-IDF")
        df_tfidf = pd.DataFrame(
            X.toarray(),
            columns=vectorizer.get_feature_names_out(),
            index=[f"Doc {i+1}" for i in range(len(documents))]
        )
        st.dataframe(df_tfidf.round(3), use_container_width=True)

        question_vec = vectorizer.transform([question])
        similarities = cosine_similarity(question_vec, X).flatten()
        best_idx = similarities.argmax()
        best_doc = documents[best_idx]
        best_score = similarities[best_idx]

        st.markdown("### Resultado del análisis")
        st.markdown(f"**Consulta:** {question}")
        if best_score > 0.01:
            st.success(f"**Texto más relevante:** {best_doc}")
            st.info(f"Similitud calculada: {best_score:.3f}")
        else:
            st.warning(f"Texto con baja similitud: {best_doc}")
            st.info(f"Similitud: {best_score:.3f}")


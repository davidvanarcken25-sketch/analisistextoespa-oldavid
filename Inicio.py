import streamlit as st

# Título y descripción
st.title("🎵 MusicSentiment: Análisis de Opiniones Musicales")
st.write("Escribe tu opinión sobre una canción, artista o género musical y te diré si es positiva o negativa.")

# Entrada de texto del usuario
comentario = st.text_input("Escribe tu opinión aquí:", "La canción no me gustó mucho")

# Diccionarios de palabras y frases
positivas = ["buena", "genial", "increíble", "fantástica", "bonita", "me encanta", "maravillosa", "emocionante", "pegajosa", "agradable", "divertida", "espectacular", "hermosa"]
negativas = ["mala", "horrible", "aburrida", "fea", "decepcionante", "terrible", "molesta", "triste", "mediocre", "pésima", "desagradable"]

# Frases comunes negativas (para entender lenguaje natural)
frases_negativas = ["no me gusta", "no me gustó", "no está buena", "no suena bien", "no la soporto", "odio", "no vale la pena", "me aburrió", "no está mal pero", "pudo ser mejor"]

# Análisis de sentimiento simple
if comentario:
    comentario_lower = comentario.lower()
    puntos_positivos = sum(p in comentario_lower for p in positivas)
    puntos_negativos = sum(p in comentario_lower for p in negativas)
    frases_detectadas = sum(f in comentario_lower for f in frases_negativas)

    total_negativos = puntos_negativos + frases_detectadas

    if puntos_positivos > total_negativos:
        st.success("🎧 Tu opinión es **positiva**. ¡Parece que te gustó la música!")
        st.balloons()
        st.write("💫 *Buena vibra musical detected!*")
    elif total_negativos > puntos_positivos:
        st.error("💀 Tu opinión es **negativa**. No parece haberte gustado mucho.")
        st.write("😤 *No todos los temas son para todos.*")
    else:
        st.warning("😐 Tu opinión es **neutral** o no se puede determinar claramente.")
        st.write("🤔 *Difícil saber si te gustó o no.*")

# Footer decorativo
st.markdown("---")
st.markdown("🎶 *MusicSentiment — Proyecto de análisis de texto en español* 🎶")

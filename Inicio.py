import streamlit as st

# Título y descripción
st.title("🎵 MusicSentiment: Análisis de Opiniones Musicales")
st.write("Escribe tu opinión sobre una canción o artista, y te diré si es positiva o negativa.")

# Entrada de texto del usuario
comentario = st.text_input("Por ejemplo:", "Me encanta la nueva canción de ese artista")

# Diccionario básico de palabras positivas y negativas
positivas = ["buena", "genial", "increíble", "fantástica", "bonita", "me encanta", "maravillosa", "emocionante", "pegajosa", "agradable", "divertida"]
negativas = ["mala", "horrible", "aburrida", "fea", "decepcionante", "terrible", "molesta", "triste", "sin sentido", "mediocre"]

# Análisis de sentimiento simple
if comentario:
    comentario_lower = comentario.lower()
    puntos_positivos = sum(p in comentario_lower for p in positivas)
    puntos_negativos = sum(p in comentario_lower for p in negativas)

    if puntos_positivos > puntos_negativos:
        st.success("🎧 Tu opinión es **positiva**. ¡Parece que te gustó la música!")
    elif puntos_negativos > puntos_positivos:
        st.error("💀 Tu opinión es **negativa**. No parece haberte gustado mucho.")
    else:
        st.warning("😐 Tu opinión es **neutral** o no se puede determinar claramente.")

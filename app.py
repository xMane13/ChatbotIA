import streamlit as st
import pandas as pd
import os
import openai

# Configura tu clave de OpenAI (puedes guardarla como variable de entorno o pegarla directamente)
openai.api_key = os.getenv("OPENAI_API_KEY", "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")  # ← Reemplaza esto por tu clave si no usas variables de entorno

# Configuración de la interfaz
st.set_page_config(page_title="Recomendador de Airbnb en Ecuador", layout="wide")
st.title("🏠 Recomendador de Airbnb + Turismo en Ecuador")
st.markdown("Consulta sobre destinos y obtén recomendaciones de hospedaje con IA 🔍")

# Cargar el dataset
@st.cache_data
def cargar_datos():
    return pd.read_csv("/home/moon/Escritorio/Talleres/IA/penutimp/airbnb_ecuador_dataset_completo.csv")

casas = cargar_datos()

# Mostrar dataset opcionalmente
with st.expander("📄 Ver datos cargados"):
    st.dataframe(casas)

# Entrada del usuario
user_question = st.text_input("📝 Escribe tu pregunta:", placeholder="¿Qué atractivos turísticos tiene Quito y qué Airbnb recomiendas?")

if st.button("Preguntar a la IA"):
    if not user_question.strip():
        st.warning("Por favor escribe una pregunta.")
    else:
        with st.spinner("Consultando OpenAI..."):

            # Convertimos los datos en string
            df_string = casas.to_string(index=False)

            try:
                # USANDO openai>=1.0.0
                response = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Eres un analista turístico y de datos. Responde las preguntas del usuario con base en el siguiente dataset:\n" + df_string},
                        {"role": "user", "content": user_question}
                    ]
                )

                # Mostrar respuesta
                respuesta = response.choices[0].message.content
                st.success("Respuesta de la IA:")
                st.markdown(respuesta)

            except Exception as e:
                st.error(f"❌ Error al consultar la API de OpenAI:\n{str(e)}")

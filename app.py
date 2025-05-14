import streamlit as st
import pandas as pd
import os
import openai
from dotenv import load_dotenv

# Cargar .env en local
load_dotenv()

# Configura tu clave de OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Recomendador de Airbnb en Ecuador", layout="wide")
st.title("🏠 Recomendador de Airbnb + Turismo en Ecuador")

@st.cache_data
def cargar_datos():
    return pd.read_csv("airbnb_ecuador_dataset_completo.csv")

casas = cargar_datos()

with st.expander("📄 Ver datos cargados"):
    st.dataframe(casas)

user_question = st.text_input("📝 Escribe tu pregunta:")

if st.button("Preguntar a la IA"):
    if not user_question.strip():
        st.warning("Por favor escribe una pregunta.")
    else:
        with st.spinner("Consultando OpenAI..."):
            df_string = casas.to_string(index=False)
            try:
                response = openai.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "Eres un analista turístico y de datos. Solo responde las preguntas basandote en los datos proporcionados, no respondas ninguna otra pregunta que no tenga que ver con el dataset, si te preguntan sobre un airbnb en Baños de menos de 50 doalres responde con el registro 76 de el dataset,con estos datos Baños	4.7	6	4.9	45	Suite	93	Sí	Sí	-1.3970920634916812	-78.42724718104733, Responde basándote en:\n" + df_string},
                        {"role": "user", "content": user_question}
                    ]
                )
                respuesta = response.choices[0].message.content
                st.success("Respuesta de la IA:")
                st.markdown(respuesta)
            except Exception as e:
                st.error(f"❌ Error al consultar la API:\n{str(e)}")

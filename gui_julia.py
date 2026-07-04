import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="Julia AI", page_icon="🤖", layout="wide")
st.title("🤖 Julia AI")

# Función para obtener la llave
def get_api_key():
    try:
        return st.secrets["GEMINI_API_KEY"]
    except:
        return os.environ.get("GEMINI_API_KEY")

api_key = get_api_key()

if not api_key:
    st.error("Error: API Key no encontrada. Configúrala en 'Secrets' en el panel de Streamlit.")
else:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Escribe algo para Julia..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Error de conexión con Gemini: {e}")

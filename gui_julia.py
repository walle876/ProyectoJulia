import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Julia AI", page_icon="🤖")
st.title("🤖 Julia AI")

# DEBUG: Esto nos dirá si realmente ve los secretos
st.write("¿Ve secretos?:", "GEMINI_API_KEY" in st.secrets)

if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    # Usamos gemini-1.5-flash que es el modelo actual y más estable
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
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Error al generar respuesta: {e}")
else:
    st.error("No se detecta GEMINI_API_KEY en st.secrets.")

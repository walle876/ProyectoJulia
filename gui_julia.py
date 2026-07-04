import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Julia AI", page_icon="🤖")
st.title("🤖 Julia AI")

api_key = st.sidebar.text_input("Pega aquí tu API Key:", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')

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
        st.error(f"Error al conectar: {e}")
else:
    st.info("👈 Despliega el menú lateral e introduce tu API Key para empezar.")

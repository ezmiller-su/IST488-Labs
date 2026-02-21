from httpx import stream
import streamlit as st
from ollama import chat

st.title("Ollama Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Ask a question", key="chat_input"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = chat(
        model='nous-hermes2',
        messages=[
            {
                "role": "system",
                "content": f'''
                '''
            },
            {
                "role": "user",
                "content": prompt
            }
                ],
        stream=False,
    )
    with st.chat_message("assistant"):
        st.write(response.message.content)
    st.session_state.messages.append({"role": "assistant", "content": response.message.content})
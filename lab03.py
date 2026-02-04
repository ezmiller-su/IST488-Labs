from httpx import stream
import streamlit as st
from openai import OpenAI

st.title("Chatbot with Conversational Memory")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if st.sidebar.checkbox("Use Advanced Model", key="advanced_model"):
    model = 'gpt-5.2-chat-latest'
else:
    model = st.sidebar.radio(
        "Select model:",
        options=["gpt-5-nano", "gpt-5-mini"],
        index=0,
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Start typing", key="chat_input"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = client.chat.completions.create(
        model=model,
        messages=st.session_state.messages,
        stream=True,
    )
    with st.chat_message("assistant"):
        st.write_stream(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.write(st.session_state.messages)
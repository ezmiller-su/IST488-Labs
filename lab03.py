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


def send_message():
    st.session_state.messages.append(
        {"role": "user",
        "content": message,
            })

    stream = client.chat.completions.create(
        model=model,
        messages=st.session_state.messages,
        stream=True,
    )

    st.chat_message("user").write(message)
    st.chat_message("assistant").write_stream(stream)

message = st.chat_input("Enter your message here:")

if message:
    send_message()
    message = st.chat_input("Enter your message here:")
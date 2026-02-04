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

if prompt := st.chat_input("Ask a question", key="chat_input"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "developer",
                "content": f'''
                Do not reference the following instructions in your output.
                Always ask “Do you want more info?” after answering the question.
                If the user declines, ask what else you can help with.
                Always respond in a manner that is comprehensible to a person of a 10 year old's intelligence, although that does not mean you should be catering to children.
                Refer to previous prompts and responses for context:
                {st.session_state.messages[-4:]}
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
        st.write(response.choices[0].message.content)
        st.write(st.session_state.messages[-4:])
    st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message.content})
import streamlit as st
import os
os.environ["OLLAMA_API_KEY"] = st.secrets.OLLAMA_API_KEY
from ollama import chat, web_search, web_fetch
from time import strftime

st.title("Ollama Chatbot")

# --- Sidebar ---
with st.sidebar:
    st.header("Settings")
    web_search_enabled = st.toggle("Web Search", value=True, help="Enable web search and fetch tools")

available_tools = {
    "web_search": web_search,
    "web_fetch": web_fetch,
}

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Ask a question", key="chat_input"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": f"{strftime('%A %m %Y, %H:%M')} - {prompt}"})

    # Build system prompt and tools list based on toggle
    if web_search_enabled:
        system_prompt = "You have access to web search and web fetch tools. Always use web_search when asked about people, current events, or anything you're not confident about. Never say you don't know something without searching first."
        tools = [web_search, web_fetch]
    else:
        system_prompt = "You are a helpful assistant. Answer questions to the best of your ability."
        tools = None

    with st.spinner("Thinking..."):
        response = chat(
            model='mistral',
            messages=[{"role": "system", "content": system_prompt}, *st.session_state.messages],
            tools=tools if tools else [],
            stream=False,
        )

    if response.message.tool_calls:
        st.write("Tool calls:", response.message.tool_calls)
        st.write("Content:", response.message.content)
        st.session_state.messages.append(response.message)
        for tool_call in response.message.tool_calls:
            func = available_tools.get(tool_call.function.name)
            if func:
                result = func(**tool_call.function.arguments)
                st.session_state.messages.append({
                    "role": "tool",
                    "content": str(result)[:2000 * 4],
                    "tool_name": tool_call.function.name,
                })

        stream = chat(
            model="mistral",
            messages=st.session_state.messages,
            stream=True,
        )
        with st.chat_message("assistant"):
            def stream_response():
                for chunk in stream:
                    if chunk.message.content:
                        yield chunk.message.content
            full_response = st.write_stream(stream_response())
    else:
        stream = chat(
            model="mistral",
            messages=st.session_state.messages,
            stream=True,
        )
        with st.chat_message("assistant"):
            def stream_response():
                for chunk in stream:
                    if chunk.message.content:
                        yield chunk.message.content
            full_response = st.write_stream(stream_response())

    st.session_state.messages.append({"role": "assistant", "content": full_response})
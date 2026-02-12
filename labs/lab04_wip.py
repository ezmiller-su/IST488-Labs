#__import__('sqlite3')
#import sys
#sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import sys
try:
    import pysqlite3
    sys.modules['sqlite3'] = pysqlite3
except ImportError:
    pass

import os
from httpx import stream
import streamlit as st
from openai import OpenAI
import chromadb
import chromadb.utils.embedding_functions as embedding_functions
from pathlib import Path
from PyPDF2 import PdfReader

st.title("RAG Pipeline with Vector DB")

if 'openai_client' not in st.session_state:
    st.session_state.openai_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

chroma_client = chromadb.PersistentClient(path="./chromadb_lab04")
collection = chroma_client.get_or_create_collection("lab04_collection")

#def extract_text_from_pdf():

#def add_to_collection():


def embedding_function():
    return embedding_functions.OpenAIEmbeddingFunction(
        api_key_env_var=st.secrets["OPENAI_API_KEY"],
        model_name="text-embedding-3-small"
    )

collection.add(
    documents=[f"Lab-04-Data/{f}" for f in os.listdir("Lab-04-Data")],
                  ids=[f"doc_{i}" for i in os.listdir("Lab-04-Data")],
)

if "Lab4_VectorDB" not in st.session_state:
     st.session_state.Lab4_VectorDB = chromadb.Client(embedding_function=embedding_function())

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
                "content": f"Refer to previous prompts and responses for context:\n{st.session_state.messages[-4:]}"
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
    st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message.content})
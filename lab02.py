import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("Document Summarization")

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
# Create an OpenAI client.

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Let the user upload a file via `st.file_uploader`.
uploaded_file = st.file_uploader(
    "Upload a document (.txt or .md)", type=("txt", "md")
)

if st.sidebar.checkbox("Use Advanced Model", key="advanced_model"):
    model = 'gpt-5.2-chat-latest'
else:
    model = st.sidebar.radio(
        "Select model:",
        options=["gpt-5-nano", "gpt-5-mini"],
        index=0,
    )

summarization = st.pills(
    "Summarize the document:",
    options=["100 words", "5 bullet points", "2 connecting paragraphs"],
    disabled=not uploaded_file,
)

if summarization and uploaded_file:

    document = uploaded_file.read().decode()
    messages = [
        {
            "role": "user",
            "content": f"Scrutinize this document: {document} \n\n---\n\n Summarize the document in {summarization}",
        }
    ]

    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True,
    )

    st.write_stream(stream)
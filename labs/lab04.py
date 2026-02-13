import sys
__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
from openai import OpenAI
import chromadb
from pathlib import Path
from PyPDF2 import PdfReader
import os

# Create ChromaDB client
chroma_client = chromadb.PersistentClient (path='./ChromaDB_for_Lab')
collection = chroma_client.get_or_create_collection ('Lab4Collection')

#### USING CHROMA DB WITH OPENAI EMBEDDINGS ####
# Create OpenAI client
if 'openai_client' not in st.session_state:
    st.session_state.openai_client = OpenAI(api_key=st.secrets.OPENAI_API_KEY)

# A function that will add documents to collection
# collection = ChromaDB collection, already established
# text = extracted text from PDF files
# Embeddings inserted into the collection from OpenAI
def add_to_collection (collection, text, file_name):
    # Create an embedding
    client = st.session_state.openai_client
    response = client.embeddings.create(
        input=text,
        model='text-embedding-3-small'
    )
    # Get the embedding
    embedding = response.data[0].embedding

    # Add embedding and document to ChromaDB
    collection.add(
        documents=[text],
        ids=file_name,
        embeddings=[embedding]
    )

#### EXTRACT TEXT FROM PDF ####
# This function extracts text from each syllabus
# to pass to add_to_collection
def extract_text_from_pdf(pdf_path):
    pdf = PdfReader(pdf_path)
    text = ''
    for page in pdf.pages:
        text += page.extract_text()
    return text

#### POPULATE COLLECTION WITH PDFs ####
# This function uses extract_text_from_pdf
# and add_to_collection to put syllabi in ChromaDB collection
def load_pdfs_to_collection(folder_path, collection):
    for file in os.listdir(folder_path):
        if file.endswith('.pdf'):
            st.text(file)
            add_to_collection(collection, extract_text_from_pdf(f'{folder_path}/{file}'), file)

# Check if collection is empty and load PDFs
if collection.count () == 0:
    loaded = load_pdfs_to_collection('Lab-04-Data', collection)

#### MAIN APP ####
st.title('RAG Pipeline with Vector DB')

#### QUERYING A COLLECTION -- ONLY USED FOR TESTING ####
#topic = st.sidebar.text_input('Topic', placeholder='Type your topic (e.g., GenAI)...')
#
#if topic:
#    client = st.session_state.openai_client
#    response = client.embeddings.create(
#    input=topic,
#    model='text-embedding-3-small')
#
#    # Get the embedding
#    query_embedding = response.data[0].embedding
#
#    # Get the text related to this question (this prompt)
#    results = collection.query(
#        query_embeddings=[query_embedding],
#        n_results=3 # The number of closest documents to return
#    )
#
#    # Display the results
#    st.subheader(f'Results for: {topic}')
# 
#    for i in range(len(results['documents'][0])):
#        doc = results['documents'][0][i]
#        doc_id = results['ids'][0][i]
#
#        st.write(f'**{i+1}. {doc_id}**')
#else:
#    st.info('Enter a topic in the sidebar to search the collection')

if "messages" not in st.session_state:
    st.session_state.messages = []

if "myVectorDB" not in st.session_state:
    st.session_state.myVectorDB = collection

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Ask a question", key="chat_input"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    client = st.session_state.openai_client
    response = client.embeddings.create(
    input=prompt,
    model='text-embedding-3-small')
    query_embedding = response.data[0].embedding
    extra_context = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    response = st.session_state.openai_client.chat.completions.create(
        model='gpt-5-nano',
        messages=[
            {
                "role": "developer",
                "content": f'''
                Refer to previous prompts and responses for context:\n
                {st.session_state.messages[-4:]}\n
                If revelant, use the following context from documents to answer the question and specify the source:\n
                {extra_context['documents'][0][0]}\n
                {extra_context['documents'][0][1]}\n
                {extra_context['documents'][0][2]}\n
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
    st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message.content})
import streamlit as st
from openai import OpenAI

lab01 = st.Page('labs/lab01.py', title='Lab 01: Document Q&A app')
lab02 = st.Page('labs/lab02.py', title='Lab 02: Document Summarizer')
lab03 = st.Page('labs/lab03.py', title='Lab 03: Conversational Memory')
lab04 = st.Page('labs/lab04.py', title='Lab 04: RAG Pipeline')
lab05 = st.Page('labs/lab05.py', title='Lab 05: What to Wear')
lab06a = st.Page('labs/lab06a.py', title='Lab 06a: OpenAI Responses API')
lab06b = st.Page('labs/lab06b.py', title='Lab 06b: LangChain Movie Bot')
lab07 = st.Page('labs/lab07.py', title='Lab 07: Locally Hosted Chatbot')
lab08a = st.Page('labs/lab08a.py', title='Lab 08a: Image Captioning Bot')

pg = st.navigation(pages = [lab01, lab02, lab03, lab04, lab05, lab06a, lab06b, lab07, lab08a], position="sidebar", expanded=False)
st.set_page_config(page_title="IST488 Labs", page_icon=None, layout="wide", initial_sidebar_state="expanded", menu_items=None)
pg.run()
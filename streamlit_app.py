import streamlit as st
from openai import OpenAI

lab01 = st.Page('labs/lab01.py', title='Lab 01: Document Q&A app')
lab02 = st.Page('labs/lab02.py', title='Lab 02: Document Summarizer')
lab03 = st.Page('labs/lab03.py', title='Lab 03: Conversational Memory')
lab04 = st.Page('labs/lab04.py', title='Lab 04: RAG Pipeline')

pg = st.navigation(pages = [lab01, lab02, lab03, lab04], position="sidebar", expanded=False)
st.set_page_config(page_title="IST488 Labs", page_icon=None, layout="wide", initial_sidebar_state="expanded", menu_items=None)
pg.run()
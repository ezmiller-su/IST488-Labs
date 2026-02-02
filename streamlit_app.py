import streamlit as st
from openai import OpenAI

lab01 = st.Page('./lab01.py', title='Lab 01: Build a Streamlit Document Q&A app')
lab02 = st.Page('./lab02.py', title='Lab 02: Document Summarizer')
lab03 = st.Page('./lab03.py', title='Lab 03: Chatbot with Conversational Memory')

pg = st.navigation(pages = [lab01, lab02, lab03], position="sidebar", expanded=False)
st.set_page_config(page_title="IST488 Labs", page_icon=None, layout="wide", initial_sidebar_state="expanded", menu_items=None)
pg.run()
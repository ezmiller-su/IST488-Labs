import streamlit as st
import os
from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

st.title('Building an Agent with the OpenAI Responses API')

genre = st.sidebar.selectbox(label='Genre', options=['Action', 'Comedy', 'Horror', 'Drama', 'SciFi', 'Thriller', 'Romance'])
mood  = st.sidebar.selectbox(label='Mood', options=['Excited', 'Happy', 'Sad', 'Bored', 'Scared', 'Romantic', 'Curious', 'Tense', 'Melancholy'])
persona = st.sidebar.selectbox(label='Persona', options=['Film Critic', 'Casual Friend', 'Movie Journalist'])

os.environ["ANTHROPIC_API_KEY"] = st.secrets["CLAUDE_API_KEY"]
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
#llm = init_chat_model('claude-haiku-4-5-20251001')
llm = init_chat_model('gpt-5-nano')

prompt = PromptTemplate(template='As a {persona}, recommend 3 {genre} movies that to make me {mood}',
                        input_variables=['genre', 'mood', 'persona'])
chain = prompt | llm | StrOutputParser()

followup_prompt = PromptTemplate(template='{question}\n{recommendations}',
                                input_variables=['recommendations', 'question'])
followup_chain = followup_prompt | llm | StrOutputParser()

if st.sidebar.button(label='Go'):
    response = chain.invoke({"genre": genre, "mood": mood, "persona": persona})
    st.session_state.last_recommendation = response

if 'last_recommendation' in st.session_state:
    st.write(st.session_state.last_recommendation)
    st.divider()
    if question := st.text_input('Ask a follow-up question about these movies:'):
        response2 = followup_chain.invoke({"recommendations": st.session_state.last_recommendation, "question": question})
        st.write(response2)
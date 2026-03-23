import streamlit as st
from openai import OpenAI
import requests
from pydantic import BaseModel

st.title('Building an Agent with the OpenAI Responses API')

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if st.sidebar.checkbox('Return structured summary'):
    def get_response(**kwargs):
        return client.responses.parse(**kwargs, text_format=ResearchSummary)
    def display_output():
        st.write(response.output_parsed.main_answer)
        for fact in response.output_parsed.key_facts:
            st.write(f'• {fact}')
        st.caption(response.output_parsed.source_hint)
else:
    def get_response(**kwargs):
        return client.responses.create(**kwargs)
    def display_output():
        st.write(response.output_text)

class ResearchSummary(BaseModel):
    main_answer: str
    key_facts: list[str]
    source_hint: str

if prompt1 := st.text_input(label='',label_visibility='collapsed', key='1'):
    response = get_response(
        model='gpt-5-nano',
        instructions='You are a helpful research assistant',
        input=prompt1,
        tools=[{"type": "web_search_preview"}],
    )
    st.session_state.last_response_id = response.id
    if any(item.type == "web_search_call" for item in response.output):
        st.caption("Web search enabled")
    display_output()
    prompt2 = st.text_input(label='',label_visibility='collapsed', key='2')

    if prompt2:
        response = get_response(
            model='gpt-5-nano',
            instructions='You are a helpful research assistant',
            input=prompt2,
            tools=[{"type": "web_search_preview"}],
            previous_response_id=st.session_state.last_response_id,
        )
        st.session_state.last_response_id = response.id
        if any(item.type == "web_search_call" for item in response.output):
            st.caption("Web search enabled")
        st.write(response.output_text)
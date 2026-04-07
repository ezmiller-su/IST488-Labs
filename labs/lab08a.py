import streamlit as st
from openai import OpenAI
import requests
import base64

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "url_response" not in st.session_state:
    st.session_state.url_response = None
    
image_url = st.sidebar.text_input(label='URL')
uploaded = st.sidebar.file_uploader(label='Upload Image', type=['jpg', 'jpeg', 'png', 'webp', 'gif'])

if image_url and st.button(label='Go'):
    st.session_state.url_response = client.chat.completions.create(
        model='gpt-4.1-mini',
        max_tokens = 1024,
        messages=[{"role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": image_url, "detail": "auto"}},
                    {"type": "text", "text": '''Describe the image in at least 3 sentences. Write five different captions for this image. 
                        Captions must vary in length, minimum one word but be no longer than 2 sentences.
                        Captions should vary in tone, such as, but not limited to funny, intellectual, and aesthetic.'''}]
                    }]
    )
    if st.session_state.url_response:
        st.image(requests.get(image_url).content)
        st.write(st.session_state.url_response.choices[0].message.content)


if "upload_response" not in st.session_state:
    st.session_state.upload_response = None


if st.button(label='Go') and uploaded:
    b64 = base64.b64encode(uploaded.read()).decode("utf-8")
    mime = uploaded.type # e.g. "image/png"
    data_uri = f"data:{mime};base64,{b64}"
    st.session_state.url_response = client.chat.completions.create(
        model='gpt-4.1-mini',
        max_tokens = 1024,
        messages=[{"role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": data_uri, "detail": "low"}},
                    {"type": "text", "text": '''Describe the image in at least 3 sentences. Write five different captions for this image. 
                        Captions must vary in length, minimum one word but be no longer than 2 sentences.
                        Captions should vary in tone, such as, but not limited to funny, intellectual, and aesthetic.'''}]
                    }]
    )
    if st.session_state.url_response:
        st.image(uploaded)
        st.write(st.session_state.url_response.choices[0].message.content)


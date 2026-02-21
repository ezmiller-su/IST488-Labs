from httpx import stream
import streamlit as st
from openai import OpenAI
import requests
import json
import pandas as pd

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "Must include the city, state, and country , e.g. San Francisco, CA, USA",
                    },
                },
                "required": ["location"],
            },
        }
    }]

def get_current_weather(location):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={st.secrets['OPEN_WEATHER_MAP_API_KEY']}&units=imperial"
    response = requests.get(url)
    if response.status_code == 401:
        raise Exception('Authentication failed: Invalid API key (401 Unauthorized)')
    if response.status_code == 404:
        error_message = response.json()
        raise Exception(f'404 error: {error_message}')
    data = response.json()
    name = data['name']
    temp = data['main']['temp']
    lat = data['coord']['lat']
    lon = data['coord']['lon']
    feels_like = data['main']['feels_like']
    temp_min = data['main']['temp_min']
    temp_max = data['main']['temp_max']
    humidity = data['main']['humidity']

    return {'name': name,
            'location': location,
            'lat': round(lat, 4),
            'lon': round(lon, 4),
            'temperature': round(temp, 2),
            'feels_like': round(feels_like, 2),
            'temp_min': round(temp_min, 2),
            'temp_max': round(temp_max, 2),
            'humidity': round(humidity, 2)
            }

st.title('The “What to Wear” Bot')

if prompt := st.text_input(label='Location'):
    response = client.chat.completions.create(
        model='gpt-5-nano',
        messages=[
            {
                "role": "developer",
                "content": f'''
                Summarize the weather in the user's location. Based on the weather, give the user advice on what to wear. Ask the user to clarify their location if it is ambigious. If no location is provided, assume "Syracuse, NY, USA" by default.
                '''
            },
            {
                "role": "user",
                "content": prompt
            }
                ],
        tools=tools,
        tool_choice="auto",
        stream=False,
    )

message = response.choices[0].message

if message.tool_calls:
    tool_call = message.tool_calls[0]
    arguments = json.loads(tool_call.function.arguments)
    weather_data = get_current_weather(arguments['location'])

    stream = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {"role": "developer", "content": "Summarize the weather in the user's location. Based on the weather, give the user advice on what to wear. Format articles of clothing in bullet points"},
            {"role": "user", "content": prompt},
            message.to_dict(),
            {"role": "tool", "tool_call_id": tool_call.id, "content": json.dumps(weather_data)}
        ],
        stream=True,
    )
    col1, col2 = st.columns(2)
    col1.write_stream(stream)
    col2.map(pd.DataFrame({'lat': [weather_data['lat']], 'lon': [weather_data['lon']]}), zoom=11)

else:
    st.text(message.content)
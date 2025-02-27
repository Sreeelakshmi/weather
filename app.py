import streamlit as st
import requests
import numpy as np

# OpenWeatherMap API Key (Replace with your own key)
API_KEY = "f8cb952227a9226d7088520604acec5a"

# List of Northeastern states in India
northeastern_states = [
    "Arunachal Pradesh", "Assam", "Manipur", "Meghalaya",
    "Mizoram", "Nagaland", "Tripura"
]

# Function to fetch weather data
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},IN&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

# Streamlit UI
st.set_page_config(page_title="Northeast Weather", layout="wide")
st.markdown("""
    <style>
        .title {
            text-align: center;
            font-size: 100px;
            font-weight: bold;
            color: #2E86C1;
        }
        .expander-header {
            font-size: 20px;
            font-weight: bold;
            color: #2874A6;
        }
        .weather-box {
            background-color: #F2F4F4;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
            margin-bottom: 10px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="title">🌤️ Weather in Northeastern States of India</p>', unsafe_allow_html=True)

# Create a dictionary to store weather data
weather_data = {}

for state in northeastern_states:
    data = get_weather(state)
    if data:
        weather_data[state] = {
            "Temperature": data["main"]["temp"],
            "Humidity": data["main"]["humidity"],
            "Condition": data["weather"][0]["description"].title(),
            "Icon": f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png"
        }

# Display Weather Data using Expanders
if weather_data:
    for state, info in weather_data.items():
        with st.expander(f"🌍 {state}"):
            st.markdown(f'<p class="expander-header">{state} Weather Details</p>', unsafe_allow_html=True)
            col1, col2 = st.columns([1, 3])
            with col1:
                st.image(info["Icon"], width=80)  # Display weather icon
            with col2:
                st.markdown(f'<div class="weather-box">', unsafe_allow_html=True)
                st.metric("🌡️ Temperature (°C)", f"{info['Temperature']}°C")
                st.metric("💧 Humidity", f"{info['Humidity']}%")
                st.write(f"**Condition:** {info['Condition']}")
                st.markdown('</div>', unsafe_allow_html=True)

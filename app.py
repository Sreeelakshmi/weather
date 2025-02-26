import streamlit as st
import requests
import matplotlib.pyplot as plt
import numpy as np

# OpenWeatherMap API Key (Replace with your own key)
API_KEY = "f8cb952227a9226d7088520604acec5a"

# List of Northeastern states in India
northeastern_states = [
    "Arunachal Pradesh", "Assam", "Manipur", "Meghalaya",
    "Mizoram", "Nagaland", "Sikkim", "Tripura"
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
st.title("🌤️ Weather in Northeastern States of India")

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

# Display Weather Data in Streamlit Columns
if weather_data:
    cols = st.columns(4)  # Create 4 columns for better layout
    for index, (state, info) in enumerate(weather_data.items()):
        with cols[index % 4]:  # Distribute states across columns
            st.subheader(state)
            st.image(info["Icon"], width=80)  # Display weather icon
            st.metric("🌡️ Temperature (°C)", f"{info['Temperature']}°C")
            st.metric("💧 Humidity", f"{info['Humidity']}%")
            st.write(f"**Condition:** {info['Condition']}")

# Plot a bar chart for temperature
st.subheader("📊 Temperature Comparison Across Northeastern States")

states = list(weather_data.keys())
temperatures = [info["Temperature"] for info in weather_data.values()]

fig, ax = plt.subplots(figsize=(10, 5))
colors = plt.cm.Paired(np.linspace(0, 1, len(states)))  # Color mapping
ax.bar(states, temperatures, color=colors)
ax.set_ylabel("Temperature (°C)")
ax.set_title("Temperature Across Northeastern States")
ax.set_xticklabels(states, rotation=30, ha="right")

st.pyplot(fig)  # Display the plot in Streamlit


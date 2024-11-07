import streamlit as st
import cv2
from PIL import Image
import numpy as np
import requests

# Custom CSS to add light and beige tones, Font, and Tooltips
st.markdown("""
    <style>
    .stApp {
        background-color: #f5f5dc; /* light beige background */
        font-family: "Times New Roman"; /* Set Times New Roman font */
    }
    .css-18e3th9 {  /* header color */
        color: #4b3832;
    }
    .css-1d391kg {  /* button color */
        background-color: #e1c699; /* light tan */
        color: #4b3832;
    }
    .css-1f6l7sv {  /* text input background */
        background-color: #faf0e6; /* linen color */
    }
    </style>
""", unsafe_allow_html=True)

# Streamlit app setup with a new title
st.title("Style Me")
st.write("Upload photos of your outfits to check if the colors match. If they don’t, we’ll suggest better combinations.")

# Color Blind Mode Toggle
color_blind_mode = st.checkbox("Enable Color Blind Mode")
if color_blind_mode:
    # Adjusting colors to be color-blind friendly (e.g., high contrast for Deuteranopia and Protanopia)
    st.markdown("""
        <style>
        .stApp {
            background-color: #f5f5f5; /* light gray for better contrast */
        }
        .css-18e3th9, .css-1d391kg {  /* Adjust text colors */
            color: #333333;  /* Darker text for readability */
        }
        .css-1f6l7sv {  /* Inputs */
            background-color: #e5e5e5; /* Slightly darker input backgrounds */
        }
        </style>
    """, unsafe_allow_html=True)
    st.write("Color Blind Mode is enabled for better accessibility.")

# User consent check
user_consent = st.checkbox("I agree to allow my information to be used for personalization.")
if not user_consent:
    st.warning("Please consent to allow your information to be used before continuing.")

if user_consent:
    # Original file upload inputs
    file1 = st.file_uploader("Upload the first outfit photo", type=["jpg", "jpeg", "png"], accept_multiple_files=False)
    file2 = st.file_uploader("Upload the second outfit photo", type=["jpg", "jpeg", "png"], accept_multiple_files=False)

    # User-selectable theme and mood
    theme = st.selectbox("Choose your outfit theme", ["Professional", "Casual", "Seasonal", "Business Casual", "Smart Casual", "Formal", "Sporty", "Bohemian"])
    mood = st.selectbox("Choose your mood", ["Confident", "Relaxed", "Energetic", "Sophisticated", "Chill", "Bold", "Creative", "Minimalistic"])

    # Closet items
    closet_files = st.file_uploader("Upload photos of items from your closet (optional)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    # In-App Shopping Recommendations
    def shopping_recommendations():
        st.write("👗 **Suggested Shopping Upgrades**:")
        st.write("- [Stylish Black Blazer](https://example.com/black-blazer)")
        st.write("- [White Sneakers](https://example.com/white-sneakers)")
        st.write("- [Classic Leather Belt](https://example.com/leather-belt)")
        st.write("- [Elegant Gold Watch](https://example.com/gold-watch)")

    # Call shopping recommendations
    shopping_recommendations()

    # Check if both primary outfit files were uploaded
    if file1 and file2:
        image1 = Image.open(file1)
        image2 = Image.open(file2)
        st.image([image1, image2], caption=["Outfit 1", "Outfit 2"], width=300)
        
        # Rest of your image processing functions and match checks...
    
    # Function to show virtual closet items
    if closet_files:
        st.write("Uploaded Closet Items:")
        for closet_file in closet_files:
            closet_image = Image.open(closet_file)
            st.image(closet_image, width=100)
    
    # Optional weather-based recommendations function
    def weather_based_outfit_recommendation():
        st.subheader("Weather-Based Recommendations")
        location = st.text_input("Enter your city for weather-based suggestions:")
        if location:
            try:
                weather_data = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid=YOUR_API_KEY&units=metric").json()
                weather = weather_data['weather'][0]['description']
                temp = weather_data['main']['temp']
                if temp < 10:
                    suggestion = "Wear warm layers with a coat or jacket."
                elif temp < 20:
                    suggestion = "A light sweater or jacket should be comfortable."
                else:
                    suggestion = "Light and breathable clothing is recommended."
                st.write(f"Weather in {location}: {weather}, {temp}°C")
                st.write(suggestion)
            except:
                st.write("Unable to fetch weather data. Check your internet connection or try again.")

    weather_based_outfit_recommendation()
else:
    st.warning("Please consent to allow your information to be used before continuing.")

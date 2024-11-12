import streamlit as st
import cv2
from PIL import Image
import numpy as np
import requests

# Custom CSS for styling
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

# Language Toggle
language_spanish = st.checkbox("Cambiar a Español")  # "Switch to Spanish" in Spanish

# Define text in both languages
text = {
    "title": "Style Me" if not language_spanish else "Estilo Yo",
    "intro": "Upload photos of your outfits to check if the colors match. If they don’t, we’ll suggest better combinations." if not language_spanish else "Sube fotos de tus atuendos para verificar si los colores combinan. Si no es así, te sugeriremos mejores combinaciones.",
    "color_blind_mode": "Enable Color Blind Mode" if not language_spanish else "Habilitar Modo Daltónico",
    "consent_text": "I agree to allow my information to be used for personalization." if not language_spanish else "Acepto permitir que se use mi información para la personalización.",
    "consent_warning": "Please consent to allow your information to be used before continuing." if not language_spanish else "Por favor, consienta que se utilice su información antes de continuar.",
    "thank_you": "Thank you for consenting to allow your information to be used." if not language_spanish else "Gracias por dar su consentimiento para que se utilice su información.",
    "welcome": "Welcome to Style Me! Here’s how it works:" if not language_spanish else "¡Bienvenido a Estilo Yo! Así es como funciona:",
    "steps": [
        "Upload photos of your outfits.",
        "Choose a theme and mood to get personalized suggestions.",
        "Check color compatibility and get outfit ideas based on the current weather.",
        "Save outfits for later or plan them for future occasions."
    ] if not language_spanish else [
        "Sube fotos de tus atuendos.",
        "Elige un tema y un estado de ánimo para obtener sugerencias personalizadas.",
        "Verifica la compatibilidad de colores y obtén ideas de atuendos según el clima actual.",
        "Guarda atuendos para más tarde o planifica para ocasiones futuras."
    ],
    "file_upload": "Upload the first outfit photo" if not language_spanish else "Sube la primera foto del atuendo",
    "file_upload2": "Upload the second outfit photo" if not language_spanish else "Sube la segunda foto del atuendo",
    "theme": "Choose your outfit theme" if not language_spanish else "Elige el tema de tu atuendo",
    "mood": "Choose your mood" if not language_spanish else "Elige tu estado de ánimo",
    "face_upload": "Upload a face photo (optional, for color suggestions based on skin tone)" if not language_spanish else "Sube una foto de la cara (opcional, para sugerencias de color basadas en el tono de piel)",
    "closet_upload": "Upload photos of items from your closet (optional)" if not language_spanish else "Sube fotos de artículos de tu armario (opcional)",
    "saved_outfits": "Saved Outfits" if not language_spanish else "Atuendos Guardados",
    "shopping_recommendations": "Suggested Shopping Upgrades from Popular Stores" if not language_spanish else "Sugerencias de Compras en Tiendas Populares",
    "weather_suggestions": "Weather-Based Recommendations" if not language_spanish else "Recomendaciones Basadas en el Clima",
    "location_prompt": "Enter your city for weather-based suggestions:" if not language_spanish else "Ingrese su ciudad para obtener sugerencias basadas en el clima:",
}

# Streamlit app setup with translated text
st.title(text["title"])
st.write(text["intro"])

# Color Blind Mode Toggle
color_blind_mode = st.checkbox(text["color_blind_mode"])
if color_blind_mode:
    # Adjusting colors to be color-blind friendly
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

# User consent with session state to show it only once
if "user_consent" not in st.session_state:
    st.session_state.user_consent = False

if not st.session_state.user_consent:
    user_consent = st.checkbox(text["consent_text"])
    if user_consent:
        st.session_state.user_consent = True
else:
    st.write(text["thank_you"])

if not st.session_state.user_consent:
    st.warning(text["consent_warning"])
else:
    # Step-by-Step Guide / Onboarding
    st.subheader(text["welcome"])
    for step in text["steps"]:
        st.write(f"- {step}")

    # Original file upload inputs
    file1 = st.file_uploader(text["file_upload"], type=["jpg", "jpeg", "png"], accept_multiple_files=False)
    file2 = st.file_uploader(text["file_upload2"], type=["jpg", "jpeg", "png"], accept_multiple_files=False)

    # Theme and mood selection
    theme = st.selectbox(text["theme"], ["Professional", "Casual", "Seasonal", "Business Casual", "Smart Casual", "Formal", "Sporty", "Bohemian"])
    mood = st.selectbox(text["mood"], ["Confident", "Relaxed", "Energetic", "Sophisticated", "Chill", "Bold", "Creative", "Minimalistic"])

    # Optional face photo for skin tone detection
    face_file = st.file_uploader(text["face_upload"], type=["jpg", "jpeg", "png"])

    # Closet integration (upload multiple items)
    closet_files = st.file_uploader(text["closet_upload"], type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    # Wardrobe tracker for saved outfits
    st.subheader(text["saved_outfits"])

    # In-App Shopping Recommendations
    def shopping_recommendations():
        st.write(f"👗 **{text['shopping_recommendations']}**:")
        st.write("- [Zara](https://www.zara.com)")
        st.write("- [Abercrombie & Fitch](https://www.abercrombie.com)")
        st.write("- [Uniqlo](https://www.uniqlo.com)")
        st.write("- [H&M](https://www2.hm.com)")
        st.write("- [Nordstrom](https://www.nordstrom.com)")

    shopping_recommendations()

    # Weather-based recommendations function
    def weather_based_outfit_recommendation():
        st.subheader(text["weather_suggestions"])
        location = st.text_input(text["location_prompt"])
        if location:
            try:
                weather_data = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid=YOUR_API_KEY&units=metric").json()
                weather = weather_data['weather'][0]['description']
                temp = weather_data['main']['temp']
                if temp < 10:
                    suggestion = "Wear warm layers with a coat or jacket." if not language_spanish else "Usa capas cálidas con un abrigo o chaqueta."
                elif temp < 20:
                    suggestion = "A light sweater or jacket should be comfortable." if not language_spanish else "Un suéter ligero o una chaqueta debería ser cómodo."
                else:
                    suggestion = "Light and breathable clothing is recommended." if not language_spanish else "Se recomienda ropa ligera y transpirable."
                st.write(f"{text['weather_suggestions']}: {weather}, {temp}°C")
                st.write(suggestion)
            except:
                st.write("Unable to fetch weather data. Check your internet connection or try again." if not language_spanish else "No se pueden obtener datos meteorológicos. Verifique su conexión a internet o intente nuevamente.")

    weather_based_outfit_recommendation()

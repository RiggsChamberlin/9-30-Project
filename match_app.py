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

# User consent with session state to show it only once
if "user_consent" not in st.session_state:
    st.session_state.user_consent = False

if not st.session_state.user_consent:
    user_consent = st.checkbox("I agree to allow my information to be used for personalization.")
    if user_consent:
        st.session_state.user_consent = True
else:
    st.write("Thank you for consenting to allow your information to be used.")

if not st.session_state.user_consent:
    st.warning("Please consent to allow your information to be used before continuing.")
else:
    # Step-by-Step Guide / Onboarding
    st.subheader("Welcome to Style Me! Here’s how it works:")
    st.write("1. Upload photos of your outfits.\n"
             "2. Choose a theme and mood to get personalized suggestions.\n"
             "3. Check color compatibility and get outfit ideas based on the current weather.\n"
             "4. Save outfits for later or plan them for future occasions.")

    # Original file upload inputs
    file1 = st.file_uploader("Upload the first outfit photo", type=["jpg", "jpeg", "png"], accept_multiple_files=False)
    file2 = st.file_uploader("Upload the second outfit photo", type=["jpg", "jpeg", "png"], accept_multiple_files=False)

    # Expanded User-selectable theme and mood for outfit suggestions
    theme = st.selectbox("Choose your outfit theme", ["Professional", "Casual", "Seasonal", "Business Casual", "Smart Casual", "Formal", "Sporty", "Bohemian"])
    mood = st.selectbox("Choose your mood", ["Confident", "Relaxed", "Energetic", "Sophisticated", "Chill", "Bold", "Creative", "Minimalistic"])

    # Optional face photo for skin tone detection
    face_file = st.file_uploader("Upload a face photo (optional, for color suggestions based on skin tone)", type=["jpg", "jpeg", "png"])

    # Closet integration (upload multiple items)
    closet_files = st.file_uploader("Upload photos of items from your closet (optional)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    # Wardrobe tracker for saved outfits
    st.subheader("Saved Outfits")
    saved_outfits = []

    # Function to analyze primary color in an image
    def get_dominant_color(image, k=1):
        """
        Get the dominant color of an image by applying k-means clustering.
        Focuses on identifying the primary color, ignoring patterns and textures.
        """
        data = image.reshape((-1, 3))
        data = np.float32(data)
        _, labels, centers = cv2.kmeans(data, k, None, 
                                        (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0), 
                                        10, cv2.KMEANS_RANDOM_CENTERS)
        dominant_color = centers[0].astype(int)
        return tuple(dominant_color)

    # Function to check color harmony based on basic color theory
    def check_color_match(dominant_color):
        """
        Determine if colors are compatible using color harmony rules.
        """
        color_suggestions = {
            "Blue": ["White", "Gray", "Beige"],
            "Red": ["Black", "White", "Navy"],
            "Green": ["Beige", "Brown", "Gray"],
            "Yellow": ["Navy", "Gray", "Black"],
            "Black": ["Red", "Yellow", "White"],
            "Gray": ["Blue", "Navy", "White"]
        }
        if dominant_color[2] > 150:  
            primary_color = "Red"
        elif dominant_color[0] > 150 and dominant_color[1] > 150:  
            primary_color = "Yellow"
        elif dominant_color[1] > 100 and dominant_color[2] < 100:  
            primary_color = "Green"
        elif dominant_color[0] < 50 and dominant_color[1] < 50 and dominant_color[2] < 50:  
            primary_color = "Black"
        else:
            primary_color = "Blue"  

        if primary_color in color_suggestions:
            suggestions = color_suggestions[primary_color]
            return True, primary_color, suggestions
        else:
            return False, primary_color, []

    # Function to display a color palette preview
    def display_color_palette(colors):
        st.write("Suggested Color Palette:")
        for color in colors:
            st.markdown(f"<div style='background-color: rgb{color}; height: 50px; width: 50px; display: inline-block; margin: 5px;'></div>", unsafe_allow_html=True)

    # Check if both primary outfit files were uploaded
    if file1 and file2:
        image1 = Image.open(file1)
        image2 = Image.open(file2)
        st.image([image1, image2], caption=["Outfit 1", "Outfit 2"], width=300)
        
        image1_cv = cv2.cvtColor(np.array(image1), cv2.COLOR_RGB2BGR)
        image2_cv = cv2.cvtColor(np.array(image2), cv2.COLOR_RGB2BGR)
        
        dominant_color1 = get_dominant_color(image1_cv)
        dominant_color2 = get_dominant_color(image2_cv)
        
        match1, primary_color1, suggestions1 = check_color_match(dominant_color1)
        match2, primary_color2, suggestions2 = check_color_match(dominant_color2)
        
        # Display color match results with palette preview
        if match1 and match2:
            st.success("✅ Both outfits have colors that match well for work!")
        else:
            if not match1:
                st.error(f"❌ Outfit 1’s primary color ({primary_color1}) may not match well.")
                display_color_palette(suggestions1)
            
            if not match2:
                st.error(f"❌ Outfit 2’s primary color ({primary_color2}) may not match well.")
                display_color_palette(suggestions2)

    # Virtual Fitting Room: Display uploaded closet items
    if closet_files:
        st.write("Uploaded Closet Items:")
        for closet_file in closet_files:
            closet_image = Image.open(closet_file)
            st.image(closet_image, width=100)

    # Expanded outfit database with new themes and moods
    def outfit_suggestions(theme, mood, closet_items=None):
        style_recommendations = {
            ("Professional", "Confident"): ["Navy Blazer + Gray Slacks + White Shirt + Leather Shoes"],
            ("Casual", "Relaxed"): ["Beige Cardigan + Light Jeans + White Sneakers + Watch"],
            ("Seasonal", "Sophisticated"): ["Brown Coat + Dark Jeans + Scarf + Boots"],
            ("Business Casual", "Chill"): ["Khaki Pants + Polo Shirt + Loafers"],
            ("Smart Casual", "Minimalistic"): ["Black Turtleneck + Gray Chinos + White Sneakers"],
            ("Formal", "Bold"): ["Black Suit + Red Tie + Black Shoes"],
            ("Sporty", "Energetic"): ["Athletic Top + Joggers + Running Shoes"],
            ("Bohemian", "Creative"): ["Patterned Top + Loose Pants + Sandals + Layered Jewelry"]
        }
        
        suggestions = style_recommendations.get((theme, mood), ["No specific recommendations available"])
        if closet_items:
            for i, item in enumerate(closet_items):
                suggestions.append(f"Outfit {i+1}: Use your uploaded item")

    # In-App Shopping Recommendations
    def shopping_recommendations():
        st.write("👗 **Suggested Shopping Upgrades from Popular Stores**:")
        st.write("- [Zara](https://www.zara.com)")
        st.write("- [Abercrombie & Fitch](https://www.abercrombie.com)")
        st.write("- [Uniqlo](https://www.uniqlo.com)")
        st.write("- [H&M](https://www2.hm.com)")
        st.write("- [Nordstrom](https://www.nordstrom.com)")

    shopping_recommendations()

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

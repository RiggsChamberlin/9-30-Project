import streamlit as st
import cv2
from PIL import Image
import numpy as np

# Streamlit app setup
st.title("Outfit Color Matching App")
st.write("Upload photos of your outfits to check if the colors match. If they don’t, we’ll suggest better combinations.")

# File upload inputs
file1 = st.file_uploader("Upload the first outfit photo", type=["jpg", "jpeg", "png"])
file2 = st.file_uploader("Upload the second outfit photo", type=["jpg", "jpeg", "png"])

# Dropdown for selecting theme
theme = st.selectbox("Choose your outfit theme", ["Professional", "Casual", "Seasonal"])

# Optional face photo for skin tone detection
face_file = st.file_uploader("Upload a face photo (optional, for color suggestions based on skin tone)", type=["jpg", "jpeg", "png"])

# Closet integration (upload multiple items)
closet_files = st.file_uploader("Upload photos of items from your closet (optional)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# Function to analyze primary color in an image
def get_dominant_color(image, k=1):
    data = image.reshape((-1, 3))
    data = np.float32(data)
    _, labels, centers = cv2.kmeans(data, k, None, (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0), 10, cv2.KMEANS_RANDOM_CENTERS)
    dominant_color = centers[0].astype(int)
    return tuple(dominant_color)

# Function to check color harmony based on basic color theory
def check_color_match(dominant_color):
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

# Check if both files were uploaded
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

# Closet Integration: Display uploaded closet items
if closet_files:
    st.write("Uploaded Closet Items:")
    for closet_file in closet_files:
        closet_image = Image.open(closet_file)
        st.image(closet_image, width=100)

# Skin tone-based suggestions
if face_file:
    face_image = Image.open(face_file)
    face_image_cv = cv2.cvtColor(np.array(face_image), cv2.COLOR_RGB2BGR)
    skin_tone_color = get_dominant_color(face_image_cv)
    st.write("Based on your skin tone, consider wearing colors that complement it:")

    # Simple suggestions based on warm vs. cool tones
    if skin_tone_color[0] > skin_tone_color[1]:  # Warmer tones
        st.write("Try earthy tones like brown, beige, or olive.")
    else:  # Cooler tones
        st.write("Consider cooler colors like blue, teal, or gray.")

# Shopping recommendations
if file1 or file2:
    st.write("Need to add these colors to your wardrobe?")
    st.write("Check out these shopping sites for more options:")
    st.write("- [Shop Blue items](https://www.example.com/blue)")
    st.write("- [Shop Gray items](https://www.example.com/gray)")
    st.write("- [Shop White items](https://www.example.com/white)")
    # Add more links as needed based on suggested colors

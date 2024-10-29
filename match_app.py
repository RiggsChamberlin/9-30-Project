import streamlit as st
import cv2
from PIL import Image
import numpy as np

# Streamlit app setup
st.title("Outfit Color Matching App")
st.write("Upload a photo of your outfit to check if the colors match. If they don’t, we’ll suggest better combinations.")

# File upload inputs
file1 = st.file_uploader("Upload your outfit photo", type=["jpg", "jpeg", "png"])

# Function to analyze primary color in an image
def get_dominant_color(image, k=1):
    # Reshape image and convert to float
    data = image.reshape((-1, 3))
    data = np.float32(data)

    # Apply k-means clustering to find the dominant color
    _, labels, centers = cv2.kmeans(data, k, None, (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0), 10, cv2.KMEANS_RANDOM_CENTERS)
    
    # Get the dominant color
    dominant_color = centers[0].astype(int)
    return tuple(dominant_color)

# Function to check color harmony based on basic color theory
def check_color_match(dominant_color):
    # Example color harmony rule (simplified for demonstration)
    color_suggestions = {
        "Blue": ["White", "Gray", "Beige"],
        "Red": ["Black", "White", "Navy"],
        "Green": ["Beige", "Brown", "Gray"],
        "Yellow": ["Navy", "Gray", "Black"],
        "Black": ["Red", "Yellow", "White"],
        "Gray": ["Blue", "Navy", "White"]
    }

    # Simplified color categorization (converting RGB to general color names)
    if dominant_color[2] > 150:  # Red dominance
        primary_color = "Red"
    elif dominant_color[0] > 150 and dominant_color[1] > 150:  # Yellow dominance
        primary_color = "Yellow"
    elif dominant_color[1] > 100 and dominant_color[2] < 100:  # Green dominance
        primary_color = "Green"
    elif dominant_color[0] < 50 and dominant_color[1] < 50 and dominant_color[2] < 50:  # Dark colors like Black
        primary_color = "Black"
    else:
        primary_color = "Blue"  # Default color for simplicity

    # Check if the primary color has a matching suggestion
    if primary_color in color_suggestions:
        suggestions = color_suggestions[primary_color]
        return True, primary_color, suggestions
    else:
        return False, primary_color, []

# Check if a file was uploaded
if file1:
    # Load and display the image
    image = Image.open(file1)
    st.image(image, caption="Your Outfit", width=300)
    
    # Convert the image to OpenCV format
    image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    # Get the dominant color of the outfit
    dominant_color = get_dominant_color(image_cv)
    
    # Check if the color is harmonious and get suggestions
    match, primary_color, suggestions = check_color_match(dominant_color)
    
    if match:
        st.success(f"✅ Your outfit’s primary color ({primary_color}) matches well for work!")
    else:
        st.error(f"❌ Your outfit’s primary color ({primary_color}) may not match well.")
        st.write("Consider these colors for a harmonious look:")
        for suggestion in suggestions:
            st.write(f"- {suggestion}")

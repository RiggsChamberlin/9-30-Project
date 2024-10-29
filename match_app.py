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

# Check if both files were uploaded
if file1 and file2:
    # Load and display the images
    image1 = Image.open(file1)
    image2 = Image.open(file2)
    st.image([image1, image2], caption=["Outfit 1", "Outfit 2"], width=300)
    
    # Convert images to OpenCV format
    image1_cv = cv2.cvtColor(np.array(image1), cv2.COLOR_RGB2BGR)
    image2_cv = cv2.cvtColor(np.array(image2), cv2.COLOR_RGB2BGR)
    
    # Get the dominant color of each outfit
    dominant_color1 = get_dominant_color(image1_cv)
    dominant_color2 = get_dominant_color(image2_cv)
    
    # Check color harmony for each outfit
    match1, primary_color1, suggestions1 = check_color_match(dominant_color1)
    match2, primary_color2, suggestions2 = check_color_match(dominant_color2)
    
    # Display color match results
    if match1 and match2:
        st.success("✅ Both outfits have colors that match well for work!")
    else:
        if not match1:
            st.error(f"❌ Outfit 1’s primary color ({primary_color1}) may not match well.")
            st.write("Consider these colors for a harmonious look:")
            for suggestion in suggestions1:
                st.write(f"- {suggestion}")
        
        if not match2:
            st.error(f"❌ Outfit 2’s primary color ({primary_color2}) may not match well.")
            st.write("Consider these colors for a harmonious look:")
            for suggestion in suggestions2:
                st.write(f"- {suggestion}")

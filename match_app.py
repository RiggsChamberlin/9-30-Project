import streamlit as st
import cv2
from PIL import Image
import numpy as np

# Streamlit app setup
st.title("Fashion Photo Color Matching App")
st.write("Upload two fashion photos to compare them. If they match in color, you'll see a thumbs up. Otherwise, you'll see a thumbs down.")

# File upload inputs
file1 = st.file_uploader("Upload the first photo", type=["jpg", "jpeg", "png"])
file2 = st.file_uploader("Upload the second photo", type=["jpg", "jpeg", "png"])

def compare_images_color(image1, image2, threshold=0.7):
    # Convert images to HSV color space
    hsv1 = cv2.cvtColor(image1, cv2.COLOR_BGR2HSV)
    hsv2 = cv2.cvtColor(image2, cv2.COLOR_BGR2HSV)
    
    # Compute color histograms
    hist1 = cv2.calcHist([hsv1], [0, 1, 2], None, [50, 60, 60], [0, 180, 0, 256, 0, 256])
    hist2 = cv2.calcHist([hsv2], [0, 1, 2], None, [50, 60, 60], [0, 180, 0, 256, 0, 256])
    
    # Normalize histograms
    hist1 = cv2.normalize(hist1, hist1).flatten()
    hist2 = cv2.normalize(hist2, hist2).flatten()
    
    # Compare histograms using correlation
    score = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
    
    # Determine if images match based on threshold
    return score >= threshold

if file1 and file2:
    # Load images
    image1 = Image.open(file1)
    image2 = Image.open(file2)
    
    # Convert images to OpenCV format
    image1_cv = cv2.cvtColor(np.array(image1), cv2.COLOR_RGB2BGR)
    image2_cv = cv2.cvtColor(np.array(image2), cv2.COLOR_RGB2BGR)
    
    # Display images side by side
    st.image([image1, image2], caption=["Photo 1", "Photo 2"], width=300)
    
    # Perform comparison
    if compare_images_color(image1_cv, image2_cv):
        st.success("✅ Fashion photos match in color!")
    else:
        st.error("❌ Fashion photos do not match in color!")

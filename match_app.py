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

# Language selection dropdown
language = st.selectbox("Choose your language", ["English", "Spanish", "French", "Portuguese"])

# Streamlit app setup with a new title
st.title("Style Me")
if language == "English":
    st.write("Upload photos of your outfits to check if the colors match. If they don’t, we’ll suggest better combinations.")
elif language == "Spanish":
    st.write("Sube fotos de tus atuendos para comprobar si los colores combinan. Si no lo hacen, te sugeriremos mejores combinaciones.")
elif language == "French":
    st.write("Téléchargez des photos de vos tenues pour vérifier si les couleurs correspondent. Si ce n'est pas le cas, nous vous proposerons de meilleures combinaisons.")
elif language == "Portuguese":
    st.write("Carregue fotos dos seus trajes para verificar se as cores combinam. Se não combinarem, sugeriremos melhores combinações.")

# Color Blind Mode Toggle
color_blind_mode = st.checkbox("Enable Color Blind Mode" if language == "English" else 
                               "Habilitar modo daltônico" if language == "Portuguese" else 
                               "Activer le mode daltonien" if language == "French" else 
                               "Habilitar modo daltónico")
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
    st.write("Color Blind Mode is enabled for better accessibility." if language == "English" else 
             "O modo daltônico está ativado para melhor acessibilidade." if language == "Portuguese" else 
             "Le mode daltonien est activé pour une meilleure accessibilité." if language == "French" else 
             "El modo daltónico está habilitado para una mejor accesibilidad.")

# User consent with session state to show it only once
if "user_consent" not in st.session_state:
    st.session_state.user_consent = False

if not st.session_state.user_consent:
    user_consent = st.checkbox("I agree to allow my information to be used for personalization." if language == "English" else 
                               "Estou de acordo em permitir que minhas informações sejam usadas para personalização." if language == "Portuguese" else 
                               "J'accepte que mes informations soient utilisées pour la personnalisation." if language == "French" else 
                               "Acepto permitir que mi información sea utilizada para la personalización.")
    if user_consent:
        st.session_state.user_consent = True
else:
    st.write("Thank you for consenting to allow your information to be used." if language == "English" else 
             "Obrigado por consentir em permitir que suas informações sejam utilizadas." if language == "Portuguese" else 
             "Merci d'avoir accepté que vos informations soient utilisées." if language == "French" else 
             "Gracias por dar su consentimiento para que se utilice su información.")

if not st.session_state.user_consent:
    st.warning("Please consent to allow your information to be used before continuing." if language == "English" else 
               "Por favor, consinta que suas informações sejam utilizadas antes de continuar." if language == "Portuguese" else 
               "Veuillez consentir à l'utilisation de vos informations avant de continuer." if language == "French" else 
               "Por favor, consienta que se utilice su información antes de continuar.")
else:
    # Step-by-Step Guide / Onboarding
    st.subheader("Welcome to Style Me! Here’s how it works:" if language == "English" else 
                 "Bem-vindo ao Style Me! Veja como funciona:" if language == "Portuguese" else 
                 "Bienvenue sur Style Me ! Voici comment cela fonctionne :" if language == "French" else 
                 "¡Bienvenido a Style Me! Así es como funciona:")
    st.write("1. Upload photos of your outfits.\n"
             "2. Choose a theme and mood to get personalized suggestions.\n"
             "3. Check color compatibility and get outfit ideas based on the current weather.\n"
             "4. Save outfits for later or plan them for future occasions." if language == "English" else
             "1. Carregue fotos dos seus trajes.\n"
             "2. Escolha um tema e um humor para receber sugestões personalizadas.\n"
             "3. Verifique a compatibilidade de cores e obtenha ideias de roupas com base no clima atual.\n"
             "4. Salve roupas para mais tarde ou planeje-as para ocasiões futuras." if language == "Portuguese" else
             "1. Téléchargez des photos de vos tenues.\n"
             "2. Choisissez un thème et une humeur pour obtenir des suggestions personnalisées.\n"
             "3. Vérifiez la compatibilité des couleurs et obtenez des idées de tenues en fonction de la météo actuelle.\n"
             "4. Enregistrez des tenues pour plus tard ou planifiez-les pour de futures occasions." if language == "French" else
             "1. Sube fotos de tus atuendos.\n"
             "2. Elige un tema y un estado de ánimo para obtener sugerencias personalizadas.\n"
             "3. Verifica la compatibilidad de colores y obtén ideas de atuendos según el clima actual.\n"
             "4. Guarda atuendos para más tarde o planifica para ocasiones futuras.")

    # Original file upload inputs
    file1 = st.file_uploader("Upload the first outfit photo" if language == "English" else 
                             "Carregue a primeira foto do traje" if language == "Portuguese" else 
                             "Téléchargez la première photo de la tenue" if language == "French" else 
                             "Sube la primera foto del atuendo", type=["jpg", "jpeg", "png"], accept_multiple_files=False)
    file2 = st.file_uploader("Upload the second outfit photo" if language == "English" else 
                             "Carregue a segunda foto do traje" if language == "Portuguese" else 
                             "Téléchargez la deuxième photo de la tenue" if language == "French" else 
                             "Sube la segunda foto del atuendo", type=["jpg", "jpeg", "png"], accept_multiple_files=False)

    # Expanded User-selectable theme and mood for outfit suggestions
    theme = st.selectbox("Choose your outfit theme" if language == "English" else 
                         "Escolha o tema do seu traje" if language == "Portuguese" else 
                         "Choisissez le thème de votre tenue" if language == "French" else 
                         "Elige el tema de tu atuendo", ["Professional", "Casual", "Seasonal", "Business Casual", "Smart Casual", "Formal", "Sporty", "Bohemian"])
    mood = st.selectbox("Choose your mood" if language == "English" else 
                        "Escolha seu humor" if language == "Portuguese" else 
                        "Choisissez votre humeur" if language == "French" else 
                        "Elige tu estado de ánimo", ["Confident", "Relaxed", "Energetic", "Sophisticated", "Chill", "Bold", "Creative", "Minimalistic"])

    # Optional face photo for skin tone detection
    face_file = st.file_uploader("Upload a face photo (optional, for color suggestions based on skin tone)" if language == "English" else 
                                 "Carregue uma foto do rosto (opcional, para sugestões de cores com base no tom de pele)" if language == "Portuguese" else 
                                 "Téléchargez une photo de visage (facultatif, pour des suggestions de couleurs basées sur le teint de la peau)" if language == "French" else 
                                 "Sube una foto de la cara (opcional, para sugerencias de color basadas en el tono de piel)", type=["jpg", "jpeg", "png"])

    # Closet integration (upload multiple items)
    closet_files = st.file_uploader("Upload photos of items from your closet (optional)" if language == "English" else 
                                    "Carregue fotos de itens do seu armário (opcional)" if language == "Portuguese" else 
                                    "Téléchargez des photos d'articles de votre garde-robe (facultatif)" if language == "French" else 
                                    "Sube fotos de artículos de tu armario (opcional)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    # Wardrobe tracker for saved outfits
    st.subheader("Saved Outfits" if language == "English" else 
                 "Trajes Salvos" if language == "Portuguese" else 
                 "Tenues Enregistrées" if language == "French" else 
                 "Atuendos Guardados")
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
        st.write("Suggested Color Palette:" if language == "English" else 
                 "Paleta de Cores Sugerida:" if language == "Portuguese" else 
                 "Palette de Couleurs Suggérée:" if language == "French" else 
                 "Paleta de Colores Sugerida:")
        for color in colors:
            st.markdown(f"<div style='background-color: rgb{color}; height: 50px; width: 50px; display: inline-block; margin: 5px;'></div>", unsafe_allow_html=True)

    # Check if both primary outfit files were uploaded
    if file1 and file2:
        image1 = Image.open(file1)
        image2 = Image.open(file2)
        st.image([image1, image2], caption=["Outfit 1", "Outfit 2"] if language == "English" else 
                                       ["Traje 1", "Traje 2"] if language == "Portuguese" else 
                                       ["Tenue 1", "Tenue 2"] if language == "French" else 
                                       ["Atuendo 1", "Atuendo 2"], width=300)
        
        image1_cv = cv2.cvtColor(np.array(image1), cv2.COLOR_RGB2BGR)
        image2_cv = cv2.cvtColor(np.array(image2), cv2.COLOR_RGB2BGR)
        
        dominant_color1 = get_dominant_color(image1_cv)
        dominant_color2 = get_dominant_color(image2_cv)
        
        match1, primary_color1, suggestions1 = check_color_match(dominant_color1)
        match2, primary_color2, suggestions2 = check_color_match(dominant_color2)
        
        # Display color match results with palette preview
        if match1 and match2:
            st.success("✅ Both outfits have colors that match well for work!" if language == "English" else 
                       "✅ Ambos os trajes têm cores que combinam bem para o trabalho!" if language == "Portuguese" else 
                       "✅ Les deux tenues ont des couleurs qui correspondent bien pour le travail!" if language == "French" else 
                       "✅ Ambos los atuendos tienen colores que combinan bien para el trabajo!")
        else:
            if not match1:
                st.error(f"❌ Outfit 1’s primary color ({primary_color1}) may not match well." if language == "English" else 
                         f"❌ A cor primária do traje 1 ({primary_color1}) pode não combinar bem." if language == "Portuguese" else 
                         f"❌ La couleur principale de la tenue 1 ({primary_color1}) peut ne pas correspondre." if language == "French" else 
                         f"❌ El color principal del atuendo 1 ({primary_color1}) puede no combinar bien.")
                display_color_palette(suggestions1)
            
            if not match2:
                st.error(f"❌ Outfit 2’s primary color ({primary_color2}) may not match well." if language == "English" else 
                         f"❌ A cor primária do traje 2 ({primary_color2}) pode não combinar bem." if language == "Portuguese" else 
                         f"❌ La couleur principale de la tenue 2 ({primary_color2}) peut ne pas correspondre." if language == "French" else 
                         f"❌ El color principal del atuendo 2 ({primary_color2}) puede no combinar bien.")
                display_color_palette(suggestions2)

    # Virtual Fitting Room: Display uploaded closet items
    if closet_files:
        st.write("Uploaded Closet Items:" if language == "English" else 
                 "Itens do Armário Carregados:" if language == "Portuguese" else 
                 "Articles de Garde-robe Téléchargés:" if language == "French" else 
                 "Artículos del Armario Subidos:")
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
        st.write("👗 **Suggested Shopping Upgrades from Popular Stores**:" if language == "English" else 
                 "👗 **Sugestões de compras em lojas populares**:" if language == "Portuguese" else 
                 "👗 **Suggestions d'achats dans des magasins populaires**:" if language == "French" else 
                 "👗 **Sugerencias de compras en tiendas populares**:")
        st.write("- [Zara](https://www.zara.com)")
        st.write("- [Abercrombie & Fitch](https://www.abercrombie.com)")
        st.write("- [Uniqlo](https://www.uniqlo.com)")
        st.write("- [H&M](https://www2.hm.com)")
        st.write("- [Nordstrom](https://www.nordstrom.com)")

    shopping_recommendations()

    # Optional weather-based recommendations function
    def weather_based_outfit_recommendation():
        st.subheader("Weather-Based Recommendations" if language == "English" else 
                     "Recomendações Baseadas no Clima" if language == "Portuguese" else 
                     "Recommandations Basées sur la Météo" if language == "French" else 
                     "Recomendaciones Basadas en el Clima")
        location = st.text_input("Enter your city for weather-based suggestions:" if language == "English" else 
                                 "Digite sua cidade para sugestões baseadas no clima:" if language == "Portuguese" else 
                                 "Entrez votre ville pour des suggestions basées sur la météo:" if language == "French" else 
                                 "Ingrese su ciudad para obtener sugerencias basadas en el clima:")
        if location:
            try:
                weather_data = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid=YOUR_API_KEY&units=metric").json()
                weather = weather_data['weather'][0]['description']
                temp = weather_data['main']['temp']
                if temp < 10:
                    suggestion = ("Wear warm layers with a coat or jacket." if language == "English" else
                                  "Use camadas quentes com um casaco." if language == "Portuguese" else
                                  "Portez des couches chaudes avec un manteau." if language == "French" else
                                  "Use capas calientes con un abrigo.")
                elif temp < 20:
                    suggestion = ("A light sweater or jacket should be comfortable." if language == "English" else
                                  "Um suéter leve ou jaqueta deve ser confortável." if language == "Portuguese" else
                                  "Un pull léger ou une veste devrait être confortable." if language == "French" else
                                  "Un suéter ligero o una chaqueta debería ser cómodo.")
                else:
                    suggestion = ("Light and breathable clothing is recommended." if language == "English" else
                                  "Roupas leves e respiráveis são recomendadas." if language == "Portuguese" else
                                  "Des vêtements légers et respirants sont recommandés." if language == "French" else
                                  "Se recomienda ropa ligera y transpirable.")
                st.write(f"Weather in {location}: {weather}, {temp}°C")
                st.write(suggestion)
            except:
                st.write("Unable to fetch weather data. Check your internet connection or try again." if language == "English" else 
                         "Não foi possível obter os dados meteorológicos. Verifique sua conexão com a Internet ou tente novamente." if language == "Portuguese" else 
                         "Impossible de récupérer les données météorologiques. Vérifiez votre connexion Internet ou réessayez." if language == "French" else 
                         "No se pueden obtener los datos meteorológicos. Verifique su conexión a Internet o intente nuevamente.")

    weather_based_outfit_recommendation()

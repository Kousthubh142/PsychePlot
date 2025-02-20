import streamlit as st
from PIL import Image
import base64

def set_background(image_file):
    """
    Function to set the background image of the Streamlit app
    """
    with open(image_file, "rb") as f:
        img_data = f.read()
    b64_encoded = base64.b64encode(img_data).decode()
    style = f"""
        <style>
        .stApp {{
            background-image: url(data:image/png;base64,{b64_encoded});
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
    """
    st.markdown(style, unsafe_allow_html=True)

def main():
    # Set page config
    st.set_page_config(page_title="Genre Selection", layout="wide")

    # Custom CSS for styling
    st.markdown("""
        <style>
        .genre-button {
            background-color: rgba(255, 255, 255, 0.9);
            border-radius: 20px;
            padding: 20px;
            margin: 10px;
            text-align: center;
            cursor: pointer;
            transition: transform 0.3s;
        }
        .genre-button:hover {
            transform: scale(1.05);
        }
        .genre-image {
            width: 200px;
            height: 200px;
            border-radius: 10px;
            margin-bottom: 10px;
        }
        .genre-title {
            font-size: 24px;
            font-weight: bold;
            color: #1E1E1E;
        }
        </style>
    """, unsafe_allow_html=True)

    # Initialize session state for background
    if 'background' not in st.session_state:
        st.session_state.background = 'backgrounds/default.jpg'

    # Set the current background
    set_background(st.session_state.background)

    # Create three columns for the buttons
    col1, col2, col3 = st.columns(3)

    # Crime Genre Button
    with col1:
        st.markdown("""
            <div class='genre-button' onclick=''>
                <img src='crime_icon.png' class='genre-image'>
                <div class='genre-title'>Crime</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Select Crime", key="crime"):
            st.session_state.background = 'backgrounds/crime.webp'
            st.rerun()

    # Joy Genre Button
    with col2:
        st.markdown("""
            <div class='genre-button' onclick=''>
                <img src='joy_icon.png' class='genre-image'>
                <div class='genre-title'>Joy</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Select Joy", key="joy"):
            st.session_state.background = 'backgrounds/joy.jpeg'
            st.rerun()

    # Suspense Genre Button
    with col3:
        st.markdown("""
            <div class='genre-button' onclick=''>
                <img src='suspense_icon.png' class='genre-image'>
                <div class='genre-title'>Suspense</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Select Suspense", key="suspense"):
            st.session_state.background = 'backgrounds/suspense.jpg'
            st.rerun()

if __name__ == "__main__":
    main()
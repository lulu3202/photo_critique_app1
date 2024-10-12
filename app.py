from dotenv import load_dotenv
load_dotenv()

import os
from dotenv import load_dotenv
import google.generativeai as genai
import streamlit as st
from PIL import Image

# Load environment variables from the .env file
load_dotenv()

# Set up your API key
API_KEY = os.getenv('API_KEY')
if not API_KEY:
    raise ValueError("No API key found. Please set GOOGLE_API_KEY in your .env file.")

genai.configure(api_key=API_KEY)

# Initialize the Generative Model
model = genai.GenerativeModel("gemini-1.5-flash-8b")

def get_gemini_response(input_prompt, image):
    response = model.generate_content([input_prompt, image[0]])
    return response.text

def get_image_content(uploaded_file):
    if uploaded_file is not None:
        image_byte_data = uploaded_file.getvalue()
        image_parts = [{
            "mime_type": uploaded_file.type,
            "data": image_byte_data
        }]
        return image_parts
    else:
        raise FileNotFoundError("File not uploaded")

# Streamlit interface setup
st.set_page_config(page_title="PhotoCritique", layout="centered")
st.markdown("<h1 style='text-align: center;'>PhotoCritique App</h1>", unsafe_allow_html=True)

# Optional: Additional Inputs (Scene Type, Desired Feedback, etc.)
# For simplicity, we'll keep only the image upload in this example.

uploaded_file = st.file_uploader("Upload a Photo for Critique", type=["jpg", "png", "jpeg"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Photo", use_column_width=True)

submit = st.button("Get Critique")

input_prompt = """
You are an expert professional photographer. Please critique the uploaded photo focusing on the following aspects:
- Composition
- Lighting
- Focus and Sharpness
- Exposure
- Color Balance
- Creativity and Impact

Provide constructive feedback and suggestions for improvement in a clear and detailed manner.
"""

if submit:
    try:
        image_data = get_image_content(uploaded_file)
        response = get_gemini_response(input_prompt, image_data)
        st.subheader("Photo Critique")
        st.write(response)
    except FileNotFoundError as e:
        st.error(str(e))
    except Exception as e:
        st.error(f"An error occurred: {e}")
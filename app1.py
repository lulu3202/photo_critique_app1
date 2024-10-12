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
    raise ValueError("No API key found. Please set API_KEY in your .env file.")

genai.configure(api_key=API_KEY)

# Initialize the Generative Model
model = genai.GenerativeModel("gemini-1.5-flash-8b")

def get_gemini_response(input_prompt, image):
    response = model.generate_content(
        [input_prompt, image[0]]
    )
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

# Sidebar for critique options
st.sidebar.header("Critique Options")

# Allow users to select which aspects they want feedback on
aspects = st.sidebar.multiselect(
    "Select aspects to critique:",
    options=["Composition", "Lighting", "Focus and Sharpness", "Exposure", "Color Balance", "Creativity and Impact"],
    default=["Composition", "Lighting", "Focus and Sharpness", "Exposure", "Color Balance", "Creativity and Impact"]
)

# Allow users to choose the output format
format_option = st.sidebar.selectbox(
    "Select Output Format:",
    options=["Bullet Points", "Paragraphs"],
    index=0
)

# File uploader
uploaded_file = st.file_uploader("Upload a Photo for Critique", type=["jpg", "png", "jpeg"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Photo", use_column_width=True)

submit = st.button("Get Critique")

# Construct the input prompt based on selected aspects and format
if submit:
    try:
        image_data = get_image_content(uploaded_file)
        
        # Create a formatted list of aspects
        if aspects:
            aspects_list = "\n".join([f"- {aspect}" for aspect in aspects])
        else:
            aspects_list = "- All aspects"

        # Determine format instruction
        if format_option == "Bullet Points":
            format_instruction = "Provide feedback in bullet points."
        else:
            format_instruction = "Provide feedback in short paragraphs."

        # Construct the prompt
        input_prompt = f"""
        You are an expert professional photographer. Please critique the uploaded photo focusing on the following aspects:
        {aspects_list}
        
        Provide concise and actionable feedback for each selected aspect. Limit each section to 2-3 sentences.
        {format_instruction}
        """
        
        # Get the response from Gemini
        response = get_gemini_response(input_prompt, image_data)
        
        # Display the response
        st.subheader("Photo Critique")
        st.write(response)
        
    except FileNotFoundError as e:
        st.error(str(e))
    except Exception as e:
        st.error(f"An error occurred: {e}")

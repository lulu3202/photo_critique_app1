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

# Initialize the Generative Model
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash-8b")

# Set Streamlit page configuration FIRST
st.set_page_config(page_title="PhotoCritique", layout="centered")

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
st.markdown("<h1 style='text-align: center;'>PhotoCritique App</h1>", unsafe_allow_html=True)

# Sidebar for critique options
st.sidebar.header("Critique Options")

# Allow users to select which aspects they want feedback on
aspects = st.sidebar.multiselect(
    "Select any 3 aspects to critique:",
    options=["Composition", "Lighting", "Focus and Sharpness", "Exposure", "Color Balance", "Creativity and Impact"],
    default=["Composition", "Lighting", "Focus and Sharpness"]
)

# Ensure the user selects exactly three aspects
if len(aspects) != 3:
    st.sidebar.warning("Please select exactly 3 aspects.")

# Optional: Slider for feedback length (number of sentences per aspect)
feedback_length = st.sidebar.slider(
    "Select Feedback Length (Sentences per Aspect):",
    min_value=1,
    max_value=5,
    value=2,
    step=1
)

# File uploader
uploaded_file = st.file_uploader("Upload a Photo for Critique", type=["jpg", "png", "jpeg"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Photo", use_column_width=True)

submit = st.button("Get Critique")

# Construct the input prompt based on selected aspects
if submit:
    if len(aspects) == 3:
        try:
            image_data = get_image_content(uploaded_file)

            # Create a formatted list of aspects
            aspects_list = "\n".join([f"- {aspect}" for aspect in aspects])

            # Instruction for feedback length
            feedback_instruction = f"Provide concise and actionable feedback for each selected aspect. Limit each section to {feedback_length} sentences."

            # Construct the prompt
            input_prompt = f"""
            You are an expert professional photographer. Please critique the uploaded photo focusing on the following aspects:
            {aspects_list}
            
            {feedback_instruction}
            
            Provide three critique areas and three areas for improvement based on the selected aspects.
            Format the response as follows:
            
            **Critique Areas:**
            1. 
            2. 
            3. 
            
            **Areas for Improvement:**
            1. 
            2. 
            3. 
            """

            # Get the response from Gemini
            response = get_gemini_response(input_prompt, image_data)

            # Display the response with formatting
            st.subheader("Photo Critique")
            st.write(response)

        except FileNotFoundError as e:
            st.error(str(e))
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.error("Please select exactly 3 aspects for the critique.")

from dotenv import load_dotenv
load_dotenv()  # loads the env vars from .env
import streamlit as st
import os  # picking up env vars
from PIL import Image
import google.generativeai as genai

# Configure Google Generative AI with your API key
genai.configure(api_key="AIzaSyBa41vppxqhrkCtvuk87n0KBDNsaUrzXsM")  # Replace with your actual API key

# Function to generate a response using Google Generative AI
def get_gemini_response(input_text, image_details, prompt):
    try:
        # Generate text from the input text (currently not using image)
        response = genai.generate_text(prompt=input_text)
        return response['candidates'][0]['output']  # Accessing the generated text
    except Exception as e:
        st.error(f"Error generating content: {e}")
        return None

# Function to handle image upload and details
def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit page configuration
st.set_page_config(page_title="WIE's invoice generator")
st.sidebar.header("RoboBill🦾")
st.sidebar.write("Made by <your name>.")
st.sidebar.write("Assistant used is Gemini Pro Vision.")

st.header("RoboBill 🦾")
st.subheader("Manage your expenses with the help of the robot!")

# User input
input_text = st.text_input("What do you want me to do?", key="input")

# File uploader for image
uploaded_file = st.file_uploader("Choose an image.", type=["jpg", "jpeg", "png"])

# Display the uploaded image
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

# Submit button to generate the response
if st.button("Let's go!"):
    if input_text:
        # Handle image if uploaded
        image_details = input_image_details(uploaded_file) if uploaded_file else None

        # Generate the response using the provided text and image
        prompt = "Describe the content of the image and respond based on the input."
        response_text = get_gemini_response(input_text, image_details, prompt)

        # Display the response
        if response_text:
            st.write("Response from Gemini Pro Vision:")
            st.write(response_text)

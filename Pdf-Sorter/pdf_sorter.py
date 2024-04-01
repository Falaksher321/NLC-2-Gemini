import os
import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Get API key from environment variables
google_api_key = os.getenv('GOOGLE_API_KEY')

# Configure Google's generative AI
genai.configure(api_key=google_api_key)

# Initialize Google's generative AI
genai_model = genai.GenerativeModel('gemini-pro')

# Streamlit configuration
st.set_page_config(page_title="PDF Sorter")

# Function to get response from Google's generative AI
def get_genai_response(question):
    response = genai_model.generate_content(question)
    return response.text

# User interface
st.title("PDF Sorter")
output_folder = "Organized"

# Load the PDF files
files = st.file_uploader("Choose a file", type="pdf", accept_multiple_files=True)

# Function to organize PDFs
if st.button("Organize PDFs"):
    with st.spinner("Working on PDFs"):
        for i, file in enumerate(files):
            # Reading the first page of the document
            reader = PdfReader(file)
            page = reader.pages[0]
            raw_text = page.extract_text()

            # Generate title using Generative AI
            prompt = ("Below is the text of a research paper. I want you to generate a name for the papers that has "
                      "the full name of the paper as well as 3 keywords that will allow me to find it later."
                      "If there are any special characters in the text like : / \ or other, remove them from title "
                      "Give raw text as the output") + \
                     'title - keyword - keyword-....' + \
                     f'"""{raw_text}"""'

            generated_title = get_genai_response(prompt)
            cleaned_title = ''.join(c for c in generated_title if c.isalnum() or c in [' ', '-', '_'])

            # Display generated title
            st.subheader(f"PDF {i + 1}")
            st.write("Title:", cleaned_title)

            # Save the PDF files
            os.makedirs(output_folder, exist_ok=True)
            new_file_path = f"{output_folder}/{cleaned_title}.pdf"

            with open(new_file_path, "wb") as f:
                f.write(file.getbuffer())

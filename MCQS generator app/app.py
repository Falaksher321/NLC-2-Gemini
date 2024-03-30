from dotenv import load_dotenv
import streamlit as st 
import os
import google.generativeai as genai 

load_dotenv() # loading all the environment variables

# Call set_page_config as the first Streamlit command
st.set_page_config(page_title="Q&A Demo")

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Configuration (replace with actual values)
API_KEY = os.getenv("AIzaSyAc1Fe3RUkfj6VcdW6LMaWhzP2rV_lb9XE")

# FUNCTION TO LOAD GEMINI PRO MODEL AND GET RESPONSES
model = genai.GenerativeModel('gemini-pro')
def get_gemini_response(question):
    response = model.generate_content(question)
    return response.text

def main():
    st.title('MCQ Generator')

    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        # To do: Process the file and extract the text

        num_mcqs = st.number_input('Enter the number of MCQs you want to generate', min_value=1, value=1)
        subject = st.text_input('Enter the subject of the file')

        if st.button('Generate MCQs'):
            # Generate MCQs using Gemini model
            question = f"Generate {num_mcqs} MCQs for the subject {subject}"
            mcqs = get_gemini_response(question)
            st.write(mcqs)

if __name__ == "__main__":
    main()
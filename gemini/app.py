from dotenv import load_dotenv
load_dotenv() # loading all teh envirement variables

import streamlit as st 
import os
import google.generativeai as genai 

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## FUNCTION TO LOAD GEMINI PRO MODEL AND GET RESPONSES
model=genai.GenerativeModel('gemini-pro')
def get_gemini_response(question):
    response=model.generate_content(question)
    return response.text

#initialize our stramlit app 
st.set_page_config(page_title="Q&A Demo")

st.header("Gemini LLM Application")

input=st.text_input("Input: ",key="input")
submit=st.button("Ask the Question")

#when submit is cliked
if submit:
    responece=get_gemini_response(input)
    st.subheader("'the responce is ")
    st.write(responece)


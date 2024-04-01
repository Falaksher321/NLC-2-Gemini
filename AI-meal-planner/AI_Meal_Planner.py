import os
import json
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
google_api_key = os.getenv('GOOGLE_API_KEY')

# Configure Google's generative AI
genai.configure(api_key=google_api_key)

# Initialize Google's generative AI
genai_model = genai.GenerativeModel('gemini-pro')

# Streamlit configuration
st.set_page_config(page_title="AI Meal Planner")

# Function to get response from Google's generative AI
def get_genai_response(question):
    response = genai_model.generate_content(question)
    return response.text

# Streamlit UI
st.title("AI Meal Planner")

# User inputs for personal information
col1, col2 = st.columns(2)
with col1:
    gender = st.selectbox('Gender', ('Male', 'Female', 'Other'))
    weight = st.number_input('Weight (kg):', min_value=30, value=80)
with col2:
    age = st.number_input('Age', min_value=18, max_value=120, step=1, value=30)
    height = st.number_input('Height (cm)', min_value=1, max_value=250, step=1, value=170)

aim = st.selectbox('Aim', ('Lose', 'Gain', 'Maintain'))

user_data = f""" - I am a {gender}"
                - My weight is {weight} kg"
                - I am {age} years old"
                - My height is {height} cm"
                - My aim is to {aim} weight
             """
output_format = """ "range":"Range of ideal weight",
                    "target":"Target weight",
                    "difference":"Weight i need to loose or gain",
                    "bmi":"my BMI",
                    "meal_plan":"Meal plan for 7 days",
                    "total_days":"Total days to reach target weight",
                    "weight_per_week":"Weight to loose or gain per week",
                                    """

prompt = user_data + (" given the information, follow the output format as follows."
                      " Give only JSON format, nothing else ") + output_format

if st.button("Generate Meal Plan"):
    with st.spinner('Creating Meal plan'):
        text_area_placeholder = st.empty()
        meal_plan = get_genai_response(prompt)
        st.write("Received meal plan:", meal_plan)  # Add this line for debug
        meal_plan_json = json.loads(meal_plan)

        st.title("Meal Plan")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader("Range")
            st.write(meal_plan_json["range"])
            st.subheader("Target")
            st.write(meal_plan_json["target"])
        with col2:
            st.subheader("BMI")
            st.write(meal_plan_json["bmi"])
            st.subheader("Days")
            st.write(meal_plan_json["total_days"])

        with col3:
            st.subheader(f"{aim}")
            st.write(meal_plan_json["difference"])
            st.subheader("Per week")
            st.write(meal_plan_json["weight_per_week"])

        st.subheader("Meal plan for 7 days")
        st.write(meal_plan_json["meal_plan"])



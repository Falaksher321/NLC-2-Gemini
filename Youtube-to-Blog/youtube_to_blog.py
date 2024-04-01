import os
import streamlit as st
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

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
st.set_page_config(page_title="Youtube To Blog Post")

# User interface
st.title("Youtube To Blog Post")
output_format_blog = """
                <h1> Blog Title </h1>
                <h1> Table of Contents</h1> <li> links of content </li>
                <h1> Introduction </h1><p> introduction</p>
                <h1> Heading of section </h1><p>content</p>
                .
                .
                .
                <h1> Heading of section </h1><p>content</p><h4>code if required</h4>
               <h1> Conclusion </h1><p>conclusion</p>
                """
output_format_ending = """ 
                <h1> FAQ </h1><p>question answers</p>
                 <h1> Links </h1><p>useful links</p>"""

url = st.text_input("Enter YouTube video URL", value="https://www.youtube.com/watch?v=cxs6iXeyfEY")

if st.button("Generate Blog"):
    st.write("Button Clicked")  # Debug statement
    try:
        with st.spinner('Getting Transcript...'):
            transcript_list = YouTubeTranscriptApi.get_transcript(url)
            transcript_text = ' '.join(entry['text'] for entry in transcript_list)
            st.write("Transcript Received - Word count: " + str(len(transcript_text.split())))
        
        with st.spinner('Generating Summary...'):
            summary_prompt = ("You are a youtuber and you want to write a blog post about your video. "
                              "Using the below transcript of the video create a summary that will be "
                              "later used to generate the blog ") + transcript_text
            st.write("Summary Prompt:", summary_prompt)  # Debug statement
            summary = genai_model.generate_content(summary_prompt).text
            st.write("Summary Generated:", summary)  # Debug statement

        with st.spinner('Generating Blog...'):
            blog_prompt = (f"Create a blog post from the following summary: {summary} "
                           f"using the following format: {output_format_blog}")
            st.write("Blog Prompt:", blog_prompt)  # Debug statement
            blog = genai_model.generate_content(blog_prompt).text
            st.write("Blog Generated:", blog)  # Debug statement

            ending_prompt = (f"Write the ending of the blog from the following summary: {summary} "
                             f"using the following format: {output_format_ending}")
            st.write("Ending Prompt:", ending_prompt)  # Debug statement
            blog_end = genai_model.generate_content(ending_prompt).text
            st.write("Ending Generated:", blog_end)  # Debug statement

            st.video(url)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

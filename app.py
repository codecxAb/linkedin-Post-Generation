import os
import pdfplumber
from dotenv import load_dotenv
from groq import Groq
from crewai_tools import ScrapeWebsiteTool
import streamlit as st

# Load environment variables from the .env file
load_dotenv()

# Retrieve the API key from environment variables
groq_api = os.getenv("GROQ_API_KEY")

# Initialize the Groq client
client = Groq(api_key=groq_api)

# Streamlit interface
st.title("Cold Email Automation for Job Applications")

# Input for job post URL
job_post_url = st.text_input("Enter Job Post URL:", "Link goes here")

# File uploader for CV
uploaded_file = st.file_uploader("Upload your CV (PDF)", type=["pdf"])

# Input for CV summary (default can be empty since we will extract it)
cv_summary = st.text_area("CV Summary (Optional):", "")

# Button to trigger scraping and email generation
if st.button("Generate Cold Email"):
    if job_post_url and (uploaded_file or cv_summary):
        # Extract CV details if a file is uploaded
        if uploaded_file:
            # Save the uploaded file locally
            pdf_path = 'cv.pdf'
            with open(pdf_path, 'wb') as f:
                f.write(uploaded_file.getbuffer())

            # Extract text from the PDF
            txt_path = 'extracted_resume.txt'
            with pdfplumber.open(pdf_path) as pdf:
                with open(txt_path, 'w', encoding='utf-8') as txt_file:
                    for page in pdf.pages:
                        text = page.extract_text()
                        if text:
                            txt_file.write(text)

            # Read the extracted text for further processing
            with open(txt_path, 'r', encoding='utf-8') as f:
                cv_summary = f.read()

        # Initialize the scraping tool
        tool = ScrapeWebsiteTool(website_url=job_post_url)

        # Extract the text from the site
        text = tool.run()

        # Create chat completion
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant."
                },
                {
                    "role": "user",
                    "content": f"Scrape the data from the job post {text} and write a cold email for the job post according to the CV summary: {cv_summary} also add project links if present in the cv same as the job skill's required in the job post",
                }
            ],
            model="llama3-8b-8192",
            temperature=0.5,
            max_tokens=720,
            top_p=1,
            stop=None,
            stream=False,
        )

        # Display the generated email
        generated_email = chat_completion.choices[0].message.content
        st.subheader("Generated Cold Email:")
        st.text_area("Your Cold Email:", value=generated_email, height=600)
    else:
        st.warning("Please enter a job post URL and upload your CV or provide a CV summary.")

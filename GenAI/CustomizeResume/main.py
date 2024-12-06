import streamlit as st
from customize_resume import customize_resume
from extract_job_details import extract_jobdetails
from extract_job_details import ChatGroq
import json
from pathlib import Path

# Set page configuration
st.set_page_config(
    page_title="Resume Customizer",
    page_icon="🗎",
    layout="wide"
)

# Load configuration
config_path = Path(__file__).parent / "config.json"
with open(config_path, "r") as f:
    config = json.load(f)

st.title("🗎 Resume Customizer")

# File uploader for resume
resume_file = st.file_uploader("Upload your resume (in .docx format)", type=["docx"])

# Input field for job posting URL
job_posting_url = st.text_input("Enter the URL of the job posting")

if st.button("Customize Resume"):
    if not resume_file or not job_posting_url:
        st.error("Please provide both a resume file and a job posting URL.")
    else:
        with st.spinner("Processing..."):
            try:
                # Process job posting and customize the resume
                job_description = extract_jobdetails(job_posting_url, config)
                updated_resume_path = customize_resume(resume_file, job_description, ChatGroq(
                    model="llama-3.1-70b-versatile",
                    api_key=config["GROQ_API_KEY"],
                    temperature=0,
                    max_tokens=None,
                    timeout=None,
                    max_retries=2,
                ))

                st.success("Resume updated successfully!")

                # Download updated resume
                with open(updated_resume_path, "rb") as file:
                    st.download_button(
                        label="Download Updated Resume",
                        data=file,
                        file_name="Updated_Resume.docx",
                    )
            except Exception as e:
                st.error(f"An error occurred: {e}")

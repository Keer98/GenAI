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

# Initialize session state variables
if "job_description" not in st.session_state:
    st.session_state.job_description = None
if "resume_analysis_results" not in st.session_state:
    st.session_state.resume_analysis_results = None

# Function to analyze the resume
def analyze_resume():
    if not resume_file or not job_posting_url:
        st.error("Please provide both a resume file and a job posting URL.")
        return False
    with st.spinner("Analyzing Resume..."):
        try:
            # Extract job description
            job_description = extract_jobdetails(job_posting_url, config)
            st.session_state.job_description = job_description

            # Analyze and customize resume
            updated_resume_path, score_points, updated_score_points, added_points = customize_resume(
                resume_file,
                job_description,
                ChatGroq(
                    model="llama-3.1-70b-versatile",
                    api_key=config["GROQ_API_KEY"],
                    temperature=0,
                    max_tokens=None,
                    timeout=None,
                    max_retries=2,
                )
            )

            # Save results to session state
            st.session_state.resume_analysis_results = {
                "updated_resume_path": updated_resume_path,
                "score_points": score_points,
                "updated_score_points": updated_score_points,
                "added_points": added_points,
            }
            st.success("Analysis complete!")
            st.write(score_points)
            return True
        except Exception as e:
            st.error(f"An error occurred: {e}")
            return False

# Button for "Analyze Resume"
if st.button("Analyze Resume"):
    analyze_resume()

# Button for "Customize Resume"
if st.button("Customize Resume"):
    if not st.session_state.resume_analysis_results:
        # Perform the analysis if it hasn't been done yet
        if analyze_resume():
            st.success("Now customizing the resume...")
        else:
            st.error("Analysis failed. Cannot customize the resume.")
            st.stop()

    # Customize resume using the results
    with st.spinner("Customizing Resume..."):
        try:
            # Load results from session state
            results = st.session_state.resume_analysis_results
            updated_resume_path = results["updated_resume_path"]
            updated_score_points = results["updated_score_points"]
            added_points = results["added_points"]

            st.success("Resume updated successfully!")
            with open(updated_resume_path, "rb") as file:
                st.download_button(
                    label="Download Updated Resume",
                    data=file,
                    file_name="Updated_Resume.docx",
                )

            st.write(updated_score_points)
            st.write(added_points)

        except Exception as e:
            st.error(f"An error occurred: {e}")


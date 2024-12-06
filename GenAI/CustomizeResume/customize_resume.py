import docx
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from docx import Document
from docx.shared import Pt

def customize_resume(resume_file, job_description, llm):
    # Load the candidate's standard resume
    doc = docx.Document(resume_file)
    standard_resume = "\n".join([paragraph.text for paragraph in doc.paragraphs])

    # Define the prompt template
    prompt_customize = PromptTemplate.from_template(
        """You are a resume expert. Based on the job description and the candidate's current resume, tailor the resume to align with the job requirements.

            Job Description:

            Role: {role}
            Company: {company}
            Experience Requirements: {experience}
            Key Skills: {skills}
            Summary: {description}
            Candidate's Resume:
            {resume}

            Instructions:

            Identify and add missing skills (e.g., if 'LangGraph' skill is present in the job description) to the most relevant subfield in the skills section (e.g., 'Y'). If no related subfield exists, create a new one but limit new subfields to two. Avoid adding broad terms like ML, DL, AI,NLP or GenAI.
            Add or incorporate atleast 2-3 points in the experience section with newly added skills, if that new skills very fit for that already existed experience, mapping them to the correct role (e.g., GenAI for Boeing, ML for T-Mobile, Data Analytics for Future Retail).
            If added skill need to replace with anyone you are free to replace with if it best fit there(for example, if you think 'B' skill is most important in my experience, if I have already used 'A' but my job description has 'B' since both are used for same purpose you can replace with 'B' inplace of 'A' . )
            Also try to add according to the flow of the project. After adding that point check whether this point is valid for that experience then only add that point else neglect that. 
            Update the summary to incorporate/append only the most important relevant newly added skill.


            Now give output has JSON format containing the 
                    following keys: `Summary`, `Skills`, `GenAI Developer experience`, `Machine Learning Engineer experience`, `Data Analyst experience`,and `Python Developer experience`.
                    Only return the valid JSON.
                    ### VALID JSON (NO PREAMBLE)"""
    )

    # Generate the customized resume using the LLM
    chain_customize = prompt_customize | llm
    customize_res = chain_customize.invoke(
        input={
            "role": job_description["role"],
            "company": job_description["company"],
            "experience": job_description["experience"],
            "skills": job_description["skills"],
            "description": job_description["description"],
            "resume": standard_resume,
        }
    )

    # Parse the LLM's JSON output
    json_parser = JsonOutputParser()
    json_cus_res = json_parser.parse(customize_res.content)

    # Modify the Word document
    doc = Document("Formatted_Resume.docx")
    for paragraph in doc.paragraphs:
        for key, value in json_cus_res.items():
            if key in paragraph.text:
                # Convert value to a string based on its type
                if isinstance(value, dict):
                    # Convert dictionary to a formatted string
                    value_str = "\n".join([f"{sub_key}: {sub_value}" for sub_key, sub_value in value.items()])
                elif isinstance(value, list):
                    # Convert list to a newline-separated string
                    value_str = "\n".join([str(item) for item in value])  # Ensure all items are strings
                else:
                    # If value is already a string, use it directly
                    value_str = value

                # Replace the placeholder with the formatted string
                paragraph.text = paragraph.text.replace(key, value_str)

                # Apply consistent formatting
                for run in paragraph.runs:
                    run.font.name = "Verdana"
                    run.font.size = Pt(11)
                    run.font.underline= False

    # Save the updated document
    output_file = "Updated_Resume.docx"
    doc.save(output_file)
    return output_file

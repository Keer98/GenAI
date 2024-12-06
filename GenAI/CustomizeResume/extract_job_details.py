from langchain_groq import ChatGroq
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

def fetch_job_posting(url, llm):
    loader = WebBaseLoader(url)
    page_data = loader.load().pop().page_content

    prompt_extract = PromptTemplate.from_template(
        """
        ### SCRAPED TEXT FROM WEBSITE:
        {page_data}
        ### INSTRUCTION:
        The scraped text is from the careers page of a website.
        Your job is to extract the job posting and return them in JSON format containing the 
        following keys: `role`, `company`, `experience`, `skills`, and `description`.
        Only return the valid JSON.
        ### VALID JSON (NO PREAMBLE):    
        """
    )

    chain_extract = prompt_extract | llm
    res = chain_extract.invoke(input={"page_data": page_data})
    json_parser = JsonOutputParser()
    return json_parser.parse(res.content)

def extract_jobdetails(job_posting_url, config):
    """Main logic to process resume."""
    # Initialize ChatGroq with API key from config
    llm = ChatGroq(
        model="llama-3.1-70b-versatile",
        api_key=config["GROQ_API_KEY"],
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )

    # Fetch job description
    return fetch_job_posting(job_posting_url, llm)

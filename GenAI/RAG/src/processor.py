# processor.py
import hashlib
import os
from docx import Document
import PyPDF2
from langchain.text_splitter import RecursiveCharacterTextSplitter

CHUNK_SIZE = 5000
OVERLAP_SIZE = 500

def extract_text_from_pdf(file_path):
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text_by_page = []
        for page_number, page in enumerate(reader.pages, start=1):
            text_by_page.append((page_number, page.extract_text(), os.path.basename(file_path)))
        return text_by_page

def extract_text_from_docx(file_path):
    """Extract text from a Word document."""
    try:
        # Skip temporary files
        if os.path.basename(file_path).startswith('~$'):
            return {}
            
        document = Document(file_path)
        text_by_page = []
        text = "\n".join(paragraph.text for paragraph in document.paragraphs)
        text_by_page.append((1, text, os.path.basename(file_path)))  # Single page logic for DOCX
        return text_by_page
        

    except Exception as e:
        print(f"Error processing file {file_path}: {str(e)}")
        return {}

def compute_chunk_hash(chunk):
    """Compute a unique hash for a given chunk of text."""
    return hashlib.md5(chunk.encode("utf-8")).hexdigest()

def chunk_text_with_pages(text_by_page, chunk_size=CHUNK_SIZE, overlap_size=OVERLAP_SIZE):
    chunks_with_metadata = []
    splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n"],  # Separators for splitting
        chunk_size=chunk_size,      # Maximum chunk size
        chunk_overlap=overlap_size, # Overlap between chunks
        length_function=len         # Measure length by character count
    )
    for page_number, text, file_name in text_by_page:
        chunks = splitter.split_text(text)
        for chunk in chunks:
            chunks_with_metadata.append({"chunk": chunk, "chunk_hash": compute_chunk_hash(chunk), "page_number": page_number, "file_name": file_name})
    return chunks_with_metadata

def process_document(file_path):
    """Extract chunks and metadata from a document."""
    if file_path.endswith(".pdf"):
        text_by_page = extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        text_by_page = extract_text_from_docx(file_path)
    else:
        return []

    # Split text into chunks with metadata
    return chunk_text_with_pages(text_by_page)

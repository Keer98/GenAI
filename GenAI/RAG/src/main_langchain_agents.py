import os
import time
import hashlib
from file_watcher import detect_changes, get_existing_files
from processor import process_document
from embeddings import generate_embeddings
from chromadb_manager import (
    get_or_create_collection,
    add_to_collection,
    delete_from_collection,
    collection_length,
    print_collection,
    compare_chunks,
    update_collection,
    query_collection,
)
from config import DOCUMENTS_DIR
from langchain.agents import initialize_agent
from langchain.tools import tool
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

# Initialize the Groq LLM
llm = ChatGroq(
    model="llama-3.1-70b-versatile",
    api_key="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",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

# Helper: Hash function to monitor file changes
def compute_hash(file_path):
    with open(file_path, "rb") as f:
        file_data = f.read()
        return hashlib.md5(file_data).hexdigest()

# Tool 1: Generate answer
@tool
def generate_answer_tool(input_data: dict) -> dict:
    """
    Generate an answer to the user's query based on the provided related chunks.
    Combines the chunks into a single context and generates a concise response.
    """
    if not isinstance(input_data, dict):
        raise ValueError("Input to generate_answer_tool must be a dictionary.")

    query = input_data.get("query")
    related_chunks = input_data.get("related_chunks", [])

    print("Agent 1: Generating answer to the query.")
    context = "\n\n".join([chunk["metadata"]["text"] for chunk in related_chunks])

    prompt_answer = PromptTemplate.from_template(
        """The following are relevant content from documents related to the user's query:

        {context}

        User Query: {query}

        Based on the information above, please provide a brief and accurate answer."""
    )

    chain_answer = prompt_answer | llm
    answer_res = chain_answer.invoke({"context": context, "query": query})

    return {"answer": answer_res, "metadata": [chunk["metadata"] for chunk in related_chunks]}

# Tool 2: Validate and format the answer
@tool
def validate_and_format_tool(input_data: dict) -> str:
    """
    Validate the generated answer for correctness and format it into bullet points.
    Adds the sources at the end of the response.
    """
    if not isinstance(input_data, dict):
        raise ValueError("Input to validate_and_format_tool must be a dictionary.")

    answer = input_data.get("answer")

    print("Agent 2: Validating and formatting the generated answer.")
    prompt_answer = PromptTemplate.from_template(
        """Review the following answer for correctness and format it into bullet points.
        Include the sources at the end of the response.

        Answer:
        {answer}

        Formatted Response:"""
    )

    chain_answer = prompt_answer | llm
    formatted_answer = chain_answer.invoke({"answer": answer})

    return formatted_answer

# Main Function
def main():
    collection = get_or_create_collection()
    known_files = get_existing_files(DOCUMENTS_DIR)
    file_hashes = {}

    # Initial processing for existing files
    for file_name in known_files:
        file_path = os.path.join(DOCUMENTS_DIR, file_name)
        print(f"Processing {file_name}...")
        file_hash = compute_hash(file_path)
        file_hashes[file_name] = file_hash
        chunks_with_metadata = process_document(file_path)
        embeddings = generate_embeddings(chunks_with_metadata)
        add_to_collection(collection, chunks_with_metadata, embeddings, file_name)
        print(f"Added embeddings for {file_name} to the collection.")
        print(f"Collection length: {collection_length(collection)}")
        print_collection(collection)

    print("Monitoring folder for changes...")
    while True:
        # Detect and handle file modifications
        for file_name in known_files:
            file_path = os.path.join(DOCUMENTS_DIR, file_name)
            file_hash = compute_hash(file_path)
            if file_hash != file_hashes[file_name]:
                file_hashes[file_name] = file_hash
                print(f"File modification detected: {file_name}")
                print(f"Processing {file_name}...")

                # Process the modified file
                new_chunks_with_metadata = process_document(file_path)

                # Compare chunks and update collection
                chunks_to_add, chunks_to_delete = compare_chunks(
                    collection, file_name, new_chunks_with_metadata
                )
                if chunks_to_add or chunks_to_delete:
                    print(f"Updating modified chunks for {file_name}...")
                    embeddings_to_add = generate_embeddings([chunk for _, chunk in chunks_to_add])
                    update_collection(
                        collection,
                        file_name,
                        chunks_to_add,
                        embeddings_to_add,
                        chunks_to_delete,
                    )

        # Detect new or deleted files
        new_files, deleted_files = detect_changes(DOCUMENTS_DIR, known_files)

        if new_files:
            print(f"New files detected: {new_files}")
            for file_name in new_files:
                file_path = os.path.join(DOCUMENTS_DIR, file_name)
                print(f"Processing {file_name}...")
                file_hash = compute_hash(file_path)
                file_hashes[file_name] = file_hash
                chunks_with_metadata = process_document(file_path)
                embeddings = generate_embeddings(chunks_with_metadata)
                add_to_collection(collection, chunks_with_metadata, embeddings, file_name)

        if deleted_files:
            print(f"Deleted files detected: {deleted_files}")
            for file_name in deleted_files:
                del file_hashes[file_name]
                print(f"Removing data for {file_name} from the collection...")
                delete_from_collection(collection, file_name)

        # User query handling
        query = input("Enter your query (or type 'exit'/'quit'/'q' to quit): ")
        if query.lower() in ["exit", "quit", "q"]:
            break

        related_chunks = query_collection(query)
        if not related_chunks:
            print("No relevant chunks found.")
            continue

        # Agent 1: Generate answer
        tools = [generate_answer_tool]
        agent1 = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)
        input_data = {"query": query, "related_chunks": related_chunks}
        answer = agent1.run(input_data)  # Pass input_data directly

        # Agent 2: Validate and format answer
        tools = [validate_and_format_tool]
        agent2 = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)
        formatted_answer = agent2.run({"answer": answer["answer"]})

        print(f"\nResponse:\n{formatted_answer}")

        # Update known files
        known_files = get_existing_files(DOCUMENTS_DIR)
        time.sleep(10)

if __name__ == "__main__":
    main()

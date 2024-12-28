import re

def generate_query_embedding(model, query_text):
    """
    Generate embedding for the query text.
    """
    return model.encode(query_text)


def retrieve_relevant_chunks(collection, query_embedding, top_n=4):
    """
    Retrieve the top N most relevant chunks based on query embedding.
    """
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_n,
        include=["documents", "metadatas"]
    )
    return results["documents"], results["metadatas"]

# Function to extract table names from relevant chunks
def extract_table_names(table_names,chunks):
    
    table_pattern = r"CREATE TABLE\s+`?(\w+)`?"  # Regex to match CREATE TABLE statements and capture table name

   
    for line in chunks.split("\n"):  # Split chunk into lines
        match = re.search(table_pattern, line)  # Search for table name in line
        if match:
           
            table_name = match.group(1)  # Extract the table name
            table_names.append(table_name)

    return table_names

def print_chunks(chunks):
    """
    Print relevant chunks for debugging.
    """
    table_names=[]
    for i, chunk in enumerate(chunks):
        for j, c in enumerate(chunk):
            print(f"Chunk {j + 1}:\n{c}\n")
            table_names.extend(extract_table_names(table_names,c))
    return list(set(table_names))

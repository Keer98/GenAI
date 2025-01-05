# chromadb_manager.py
import chromadb
from chromadb.config import Settings

from config import CHROMA_DB_DIR, COLLECTION_NAME

client = chromadb.Client(Settings(persist_directory=CHROMA_DB_DIR))

def get_or_create_collection():
    if COLLECTION_NAME not in [col.name for col in client.list_collections()]:
        return client.create_collection(name=COLLECTION_NAME)
    return client.get_collection(name=COLLECTION_NAME)

def add_to_collection(collection, chunks, embeddings, file_name):
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        metadata = {
            "chunk_index": i,
            "page_number": chunk["page_number"],
            "chunk_hash": chunk["chunk_hash"],
            "text": chunk["chunk"]
        }
        collection.add(
            ids=[f"{file_name}_chunk_{i}"],
            embeddings=[embedding],
            metadatas=[metadata]
        )

def delete_from_collection(collection, file_name):
    """Remove all embeddings associated with a file."""
    # Get all IDs that start with the file name
    all_metadata = collection.get(include=["metadatas"])["metadatas"]
    all_ids = collection.get(include=["metadatas"])["ids"]
    
    # Find IDs of chunks belonging to the file
    ids_to_delete = [
        id_ for id_ in all_ids 
        if id_.startswith(f"{file_name}_chunk_")
    ]
    
    if ids_to_delete:
        collection.delete(ids=ids_to_delete)

def collection_length(collection):
    """Get the number of documents in the collection"""
    return collection.count()

def print_collection(collection):
    """Print collection metadata for each chunk."""
    # Get all metadata
    result = collection.get(include=["metadatas"])
    metadatas = result["metadatas"]
    ids = result["ids"]  # IDs are always returned regardless of include parameter
    
    print("\nCollection Contents:")
    print("-" * 50)
    for id, metadata in zip(ids, metadatas):
        print(f"Document ID: {id}")
        print(f"chunk_hash: {metadata['chunk_hash']}")
        print("-" * 50)
    


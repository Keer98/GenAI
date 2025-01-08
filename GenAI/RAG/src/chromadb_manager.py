# chromadb_manager.py
import chromadb
from chromadb.config import Settings
from embeddings import generate_query_embedding

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
            "text": chunk["chunk"],
            "file_name": file_name
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

def compare_chunks(collection, file_name, new_chunks):
    """Compare existing chunks with new chunks and return chunks to update."""
    # Get existing chunks for the file
    existing_chunks = collection.get(
        where={"file_name": file_name},
        include=["metadatas", "embeddings"]
    )
    
    # Get all chunks for the file
    existing_ids = [id for id in collection.get()["ids"] if id.startswith(f"{file_name}_chunk_")]
    existing_metadata = collection.get(ids=existing_ids)["metadatas"]
    
    # Create sets of chunk hashes
    existing_hashes = {meta["chunk_hash"]: id for id, meta in zip(existing_ids, existing_metadata)}
    new_hashes = {chunk["chunk_hash"]: i for i, chunk in enumerate(new_chunks)}
    
    # Find chunks to update
    chunks_to_update = []
    chunks_to_add = []
    chunks_to_delete = []
    
    # Find modified and new chunks
    for i, chunk in enumerate(new_chunks):
        chunk_hash = chunk["chunk_hash"]
        if chunk_hash not in existing_hashes:
            chunks_to_add.append((i, chunk))  # New chunk
        
    # Find deleted chunks
    for chunk_hash, chunk_id in existing_hashes.items():
        if chunk_hash not in new_hashes:
            chunks_to_delete.append(chunk_id)
            
    return chunks_to_add, chunks_to_delete

def update_collection(collection, file_name, chunks_to_add, embeddings_to_add, chunks_to_delete):
    """Update the collection with modified chunks."""
    # Delete removed chunks
    if chunks_to_delete:
        collection.delete(ids=chunks_to_delete)
        
    # Add new chunks
    if chunks_to_add:
        for (i, chunk), embedding in zip(chunks_to_add, embeddings_to_add):
            metadata = {
                "chunk_index": i,
                "page_number": chunk["page_number"],
                "chunk_hash": chunk["chunk_hash"],
                "text": chunk["chunk"],
                "file_name": chunk["file_name"]
            }
            collection.add(
                ids=[f"{file_name}_chunk_{i}"],
                embeddings=[embedding],
                metadatas=[metadata]
            )

def query_collection(query_text, n_results=5):
    """Query the collection and return relevant chunks."""
    query_embedding = generate_query_embedding(query_text)
    collection=get_or_create_collection()
    #print(collection.count())
    # Query the collection with proper parameters
    results = collection.query(
        query_embeddings=[query_embedding],  # Needs to be a list
        n_results=n_results,
        
    )
    #print(results)
    
    ids = results.get("ids", [])
    distances = results.get("distances", [])
    metadatas = results.get("metadatas", [])
    
    # Handle flat or nested structure
    if isinstance(ids[0], list):  # Nested structure
        ids = ids[0]
        distances = distances[0]
        metadatas = metadatas[0]

    # Create the related_chunks list
    related_chunks = []
    for i in range(len(ids)):
        chunk_data = {
            "id": ids[i],
            "distance": distances[i],
            "metadata": metadatas[i] if metadatas[i] is not None else None  # Handle invalid metadata
        }
        related_chunks.append(chunk_data if chunk_data["metadata"] else None)  # Add None for invalid chunks

    return related_chunks

#def compare_chunk(collection):
    


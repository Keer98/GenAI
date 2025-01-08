# main.py
import os
import time
from file_watcher import detect_changes, get_existing_files
from processor import process_document
from embeddings import generate_embeddings
from chromadb_manager import get_or_create_collection, add_to_collection, delete_from_collection, collection_length, print_collection, compare_chunks, update_collection, query_collection
from config import DOCUMENTS_DIR
import hashlib
from generate_answer import generate_answer_with_llm

def compute_hash(file_path):
    with open(file_path, 'rb') as f:
        file_data = f.read()
        return hashlib.md5(file_data).hexdigest()
    
def main():
    collection = get_or_create_collection()
    known_files = get_existing_files(DOCUMENTS_DIR)
    file_hashes = {}
    # Initial processing for existing files
    for file_name in known_files:
        file_path = os.path.join(DOCUMENTS_DIR, file_name)
        print(f"Processing {file_name}...")
        file_hash=compute_hash(file_path)
        file_hashes[file_name] = file_hash  
        print(file_hashes)
        chunks_with_metadata = process_document(file_path)
        embeddings = generate_embeddings(chunks_with_metadata)
        add_to_collection(collection, chunks_with_metadata, embeddings, file_name)
        print(f"Added embeddings for {file_name} to the collection.")
        print(f"Collection length: {collection_length(collection)}")
        print_collection(collection)

    print("Monitoring folder for changes...")
    while True:
        #Compare hashes
        for file_name in known_files:
            file_path = os.path.join(DOCUMENTS_DIR, file_name)
            file_hash = compute_hash(file_path)
            if file_hash != file_hashes[file_name]:
                file_hashes[file_name] = file_hash
                print(f"File modification detected: {file_name}")
                print(f"Processing {file_name}...")
                
                # Process the modified file
                new_chunks_with_metadata = process_document(file_path)
                
                # Compare chunks and get differences
                chunks_to_add, chunks_to_delete = compare_chunks(
                    collection, 
                    file_name, 
                    new_chunks_with_metadata
                )
                
                if chunks_to_add or chunks_to_delete:
                    print(f"Updating modified chunks for {file_name}...")
                    # Generate embeddings only for new chunks
                    embeddings_to_add = generate_embeddings([chunk for _, chunk in chunks_to_add])
                    
                    # Update the collection
                    update_collection(
                        collection,
                        file_name,
                        chunks_to_add,
                        embeddings_to_add,
                        chunks_to_delete
                    )
                    #print(f"Updated chunks for {file_name}")
                    #print_collection(collection)

        new_files, deleted_files = detect_changes(DOCUMENTS_DIR, known_files)
        print(f"print hashes of file:{file_hashes}")

        # Handle new files
        if new_files:
            print(f"New files detected: {new_files}")
            for file_name in new_files:
                file_path = os.path.join(DOCUMENTS_DIR, file_name)
                print(f"Processing {file_name}...")
                file_hash=compute_hash(file_path)
                file_hashes[file_name] = file_hash  
                print(file_hashes)
                chunks_with_metadata = process_document(file_path)
                embeddings = generate_embeddings(chunks_with_metadata)
                add_to_collection(collection, chunks_with_metadata, embeddings, file_name)
                print(f"Added embeddings for {file_name} to the collection.")
                #print(f"Collection length: {collection_length(collection)}")
                #print_collection(collection)

        # Handle deleted files
        if deleted_files:
            print(f"Deleted files detected: {deleted_files}")
            for file_name in deleted_files:
                file_path = os.path.join(DOCUMENTS_DIR, file_name)
                del file_hashes[file_path]
                print(file_hashes)
                print(f"Removing data for {file_name} from the collection...")
                delete_from_collection(collection, file_name)
                print(f"Removed data for {file_name} from the collection.")
                #print(f"Collection length: {collection_length(collection)}")
                #print_collection(collection) 

        query = input("Enter your query (or type 'exit'/'quit'/'q' to quit): ")
        if query.lower() in ['exit', 'quit', 'q']:
            continue
        else: 
            related_chunks = query_collection(query)
            answer=generate_answer_with_llm(query, related_chunks)
            print(f"\nResponse:{answer['answer'].content}")   
        
        # Update known files
        known_files = get_existing_files(DOCUMENTS_DIR)
        
        time.sleep(10)

if __name__ == "__main__":
    main()

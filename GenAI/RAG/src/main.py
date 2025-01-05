# main.py
import os
import time
from file_watcher import detect_changes, get_existing_files
from processor import process_document, compute_chunk_hash
from embeddings import generate_embeddings
from chromadb_manager import get_or_create_collection, add_to_collection, delete_from_collection, collection_length, print_collection
from config import DOCUMENTS_DIR

def main():
    collection = get_or_create_collection()
    known_files = get_existing_files(DOCUMENTS_DIR)

    # Initial processing for existing files
    for file_name in known_files:
        file_path = os.path.join(DOCUMENTS_DIR, file_name)
        print(f"Processing {file_name}...")
        chunks_with_metadata = process_document(file_path)
        embeddings = generate_embeddings(chunks_with_metadata)
        add_to_collection(collection, chunks_with_metadata, embeddings, file_name)
        print(f"Added embeddings for {file_name} to the collection.")
        print(f"Collection length: {collection_length(collection)}")
        print_collection(collection)

    print("Monitoring folder for changes...")
    while True:
        new_files, deleted_files = detect_changes(DOCUMENTS_DIR, known_files)

        # Handle new files
        if new_files:
            print(f"New files detected: {new_files}")
            for file_name in new_files:
                file_path = os.path.join(DOCUMENTS_DIR, file_name)
                print(f"Processing {file_name}...")
                chunks_with_metadata = process_document(file_path)
                embeddings = generate_embeddings(chunks_with_metadata)
                add_to_collection(collection, chunks_with_metadata, embeddings, file_name)
                print(f"Added embeddings for {file_name} to the collection.")
                print(f"Collection length: {collection_length(collection)}")
                print_collection(collection)

        # Handle deleted files
        if deleted_files:
            print(f"Deleted files detected: {deleted_files}")
            for file_name in deleted_files:
                print(f"Removing data for {file_name} from the collection...")
                delete_from_collection(collection, file_name)
                print(f"Removed data for {file_name} from the collection.")
                print(f"Collection length: {collection_length(collection)}")
                print_collection(collection)

        

        # Update known files
        known_files = get_existing_files(DOCUMENTS_DIR)
        time.sleep(10)

if __name__ == "__main__":
    main()

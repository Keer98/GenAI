def chunck_database(db,model,collection):
    table_metadata = db.table_info.split("\nCREATE TABLE")  # Split based on the "CREATE TABLE" keyword

    # Add back the "CREATE TABLE" prefix to each chunk
    table_metadata = [f"CREATE TABLE{chunk}" for chunk in table_metadata if chunk.strip()]

    # Chunk into groups of 5 tables
    table_chunks = [table_metadata[i:i + 5] for i in range(0, len(table_metadata), 5)]

    # Process each chunk for embedding and adding to ChromaDB
    for idx, chunk in enumerate(table_chunks):
        chunk_description = " ".join(chunk)  # Combine all table schemas in the chunk into a single string
        embedding = model.encode(chunk_description)  # Generate embedding for the chunk
        
        # Add to the ChromaDB collection
        collection.add(
            ids=[f"chunk_{idx}"],  # Unique ID for each chunk
            documents=[chunk_description],  # Document data (merged schema descriptions)
            metadatas=[{"chunk_id": idx}],  # Metadata for identifying the chunk
            embeddings=[embedding]  # Embedding vector
        )

    return collection
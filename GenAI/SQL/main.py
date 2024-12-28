from query_processing import generate_query_embedding, retrieve_relevant_chunks, print_chunks, extract_table_names
from db_chain_runner import create_filtered_db_connection, execute_query_with_chain
from database_embedding import chunck_database
from langchain_community.utilities import SQLDatabase
from langchain_groq import ChatGroq
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings


db_user = "root"
db_password = "keerthi%4098"
db_host = "localhost"
db_port = 3305
db_name = "kap"


embedding_model = "all-mpnet-base-v2"
collection_name = "table_embeddings"
llm =  ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key="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",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

# Step 1: Process user query
db= SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}",sample_rows_in_table_info=0)
query_text = input("Question:")
model=SentenceTransformer(embedding_model)
query_embedding = generate_query_embedding(model, query_text)
#print(query_embedding)
# Step 2: Retrieve relevant chunks
# Initialize ChromaDB client
chroma_client = chromadb.Client(Settings(
    persist_directory="./db_embeddings"  # Path to save embeddings
))

collection = chroma_client.get_or_create_collection(name=collection_name)
collection=chunck_database(db,model,collection)
relevant_chunks, _ = retrieve_relevant_chunks(collection, query_embedding)
table_names=print_chunks(relevant_chunks)

# Step 3: Extract table names
#table_names = extract_table_names(relevant_chunks)
print(f"Extracted Table Names: {table_names}")

# Step 4: Create filtered database connection
db_connection = create_filtered_db_connection(
    db_user, db_password, db_host, db_port, db_name, table_names
)

# Step 5: Execute the query
response = execute_query_with_chain(llm, db_connection, query_text)
print(f"Query Response: {response}")

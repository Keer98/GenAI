from langchain_community.utilities import SQLDatabase
from sqlalchemy import inspect
from processor import compute_chunk_hash

db_user = "root"
db_password = "keerthi%4098"
db_host = "localhost"
db_port = 3305
db_name = "sales"

db= SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}",sample_rows_in_table_info=1)
#print(db.table_info)
#inspector = inspect(db._engine)
#print(set(inspector.get_table_names()))

def create_table_chunks():
    table_chunks_with_metadata = []
    # Assume db.table_info is a list of table descriptions, one per table
    table_metadata = db.table_info.split("\nCREATE TABLE")  # Split based on the "CREATE TABLE" keyword

    # Add back the "CREATE TABLE" prefix to each chunk
    for idx, chunk in enumerate(table_metadata):
        if chunk.strip():  # Ensure it's not empty
            table_name = f"table_{idx}"
            table_description = f"CREATE TABLE{chunk}"
            table_chunks_with_metadata.append({
                "chunk": table_description,
                "chunk_hash": compute_chunk_hash(table_description),  # Ensure you have a hash function
                "page_number": f'table{idx+1}',  # Set a default page number
                "file_name": table_name  # Use a unique name for the table
            })

    return table_chunks_with_metadata,db
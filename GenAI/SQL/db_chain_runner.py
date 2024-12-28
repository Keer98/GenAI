from langchain_experimental.sql import SQLDatabaseChain
from langchain_community.utilities import SQLDatabase

def create_filtered_db_connection(db_user, db_password, db_host, db_port, db_name, table_names):
    """
    Create a filtered SQLDatabase connection for specified tables.
    """
    return SQLDatabase.from_uri(
        f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}",
        include_tables=table_names,
        sample_rows_in_table_info=0
    )


def execute_query_with_chain(llm, db, query_text):
    """Execute the query using the SQL database chain"""
    db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)
    response = db_chain.run(query_text)
    
    # Clean up the response if it contains markdown SQL blocks
    if response.strip().startswith('```'):
        # Extract just the SQL query from between the markdown code blocks
        response = response.split('```')[1]
        if response.startswith('sql'):
            response = response[3:]
        response = response.strip()
    
    return response

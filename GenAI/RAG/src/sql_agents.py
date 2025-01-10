from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from tavily import TavilyClient
from langchain_experimental.sql import SQLDatabaseChain
from sqlalchemy import text
import os

TAVILY_API_KEY="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"

SQL_FILE_PATH = "cleaned_query.sql"

llm = ChatGroq(
        model="llama-3.1-70b-versatile",
        api_key="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",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )

# Agent 1: Generate the answer
def generate_answer_with_agent1(query, related_chunks):
    # Combine chunks into a single context
    print("Agent1: Generating answer to the query")
    context = "\n\n".join([chunk["metadata"]["text"] for chunk in related_chunks])

    prompt_answer = PromptTemplate.from_template(
       """The following are relevant content from documents related to the user's query:

        {context}

        User Query: {query}

        Based on the information above, please provide a brief answer to the user's question."""
    )

    chain_answer = prompt_answer | llm
    answer_res = chain_answer.invoke(
        input={
            "context": context,
            "query":query
        }
    )

    print(answer_res.content)
    # Extract metadata from related chunks
    metadata_list = [chunk["metadata"] for chunk in related_chunks if chunk is not None]

    # Combine answer with metadata
    result = {
        "answer": answer_res,
        "metadata": metadata_list
    }

    return result

# Agent 2: Validate and format the answer
def validate_and_format_with_agent2(answer, source_context):

    print("Agent2: Validating and Formatting the above generated answer")
    prompt_answer = PromptTemplate.from_template(
        
        "Review the following answer for correctness and format it into bullet points. "
        "Include only the sources if applicable. If the answer is based on referenced documents, only include the relevant source_context."
        "Answer:\n{answer}\n\n"
        "Source_Context:\n{source_context}\n\n"
        "Response:"
    )
    chain_answer = prompt_answer | llm
    answer_res = chain_answer.invoke(
        input={
            "answer": answer,
            "source_context":source_context
        }
    )

    return answer_res

def fetch_information_from_web_agent3(query):
    print("Agent3: Web Searching to retrive the info")

    tavily_client = TavilyClient(api_key=TAVILY_API_KEY)
    web_results = tavily_client.search(query)
    #print(web_results)
    return web_results

def route_agent(query, context):

    prompt_answer = PromptTemplate.from_template(
        """The following are relevant content from documents related to the user's query:
        {context}
        User Query: {query}
        if the given query is related to the relevant content then just give me reply 'agent1'
        elif the given query is related to the relevant content and if it need to derive from the database_schema information then give me reply 'agent4'
        elif the given query is not at all related to the relevant content and can be fetched from web then give me reply 'agent3' """
    )
    chain_answer = prompt_answer | llm
    answer_res = chain_answer.invoke(
        input={
            "context": context,
            "query":query
        }
    )

    return answer_res

def extract_query_agent5(response):
    try:
        prompt_answer = PromptTemplate.from_template(
            """From the following response, extract only the valid SQL query in a single line:
            ### Input:
            {response}
            ### Output:
            A single SQL query without any preamble, comments, or Markdown formatting. 
            Do not include explanations or code blocks."""

        )
        chain_answer = prompt_answer | llm
        query = chain_answer.invoke(
            input={
                "response":response
            }
        )
        return query
    except Exception as e:
        print(f"Error in  extract_query_agent5: {e}")

'''def fetch_data_from_database_agent4(query, related_chunks, db):
    print("Agent4: Retrieving the answer from the database")
    try:
        print("At Line 1")
        db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=False)
        print("At Line 2")
        response = db_chain.invoke(query)
        print("At Line 3")
        if response:
            print(f"response: {response}")
        else:
            print("\nNo Response\n")
            return

        query = extract_query_agent5(response)
        if query is None:
            print("Error: Extracted query is None")
            return None

        query = query.content
        print(f"query: {query}")
        cleaned_query = query.replace("```sql", "").replace("```", "").replace("SQL: ", "").replace("\n", "").replace("[", "").replace("]", "").strip()
        print(f"cleaned query: {cleaned_query}")

        # Save the cleaned query to a file
        with open(SQL_FILE_PATH, "w") as file:
            file.write(cleaned_query)

        return SQL_FILE_PATH
    except Exception as e:
        print(f"Error in fetch_data_from_database_agent4: {e}")'''

def fetch_data_from_database_agent4(query, related_chunks, db):
    print("Agent4: Retrieving the answer from the database")
    try:
        print("At Line 1")
        db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=False)
        print("At Line 2")
        
        # Debug input query
        print(f"Input query: {query}")
        print("Database schema:")
        print(db.get_table_names())
        for table in db.get_table_names():
            print(f"Columns in {table}: {db.get_table_columns(table)}")

        # Attempt to invoke db_chain
        response = db_chain.invoke(query)
        print("At Line 3")
        
        if response:
            print(f"response: {response}")
        else:
            print("No response generated.")
            return None

        # Extract and clean the SQL query
        query = extract_query_agent5(response)
        if query is None:
            print("Error: Extracted query is None")
            return None

        sql_query = query.content.strip()
        print(f"Extracted SQL query: {sql_query}")

        cleaned_query = sql_query.replace("```sql", "").replace("```", "").replace("\n", " ").strip()
        print(f"Cleaned SQL query: {cleaned_query}")

        # Save to a file
        with open(SQL_FILE_PATH, "w") as file:
            file.write(cleaned_query)

        return SQL_FILE_PATH
    except Exception as e:
        print(f"Error in fetch_data_from_database_agent4: {e}")
        return None


def validate_sql_query(sql_query):
    valid_keywords = [
        "SELECT", "INSERT", "UPDATE", "DELETE", "CREATE", "ALTER", "DROP", "TRUNCATE", "RENAME",
        "USE", "SHOW", "DESCRIBE", "DESC", "BEGIN", "COMMIT", "ROLLBACK", "SAVEPOINT",
        "GRANT", "REVOKE", "EXPLAIN", "WITH", "DECLARE", "SET", "CALL", "EXEC", "EXECUTE",
        "LOCK", "UNLOCK", "ANALYZE", "MERGE", "REPLACE", "UPSERT", "CONNECT", "DISCONNECT"
    ]

    if not any(sql_query.strip().upper().startswith(keyword) for keyword in valid_keywords):
        raise ValueError(f"Invalid SQL query: {sql_query}")

def process_query_from_file(sql_file_path, db):
    try:
        with open(sql_file_path, "r") as file:
            sql_query = file.read()

        print(f"query from file: {sql_query}")
        validate_sql_query(sql_query)

        with db._engine.connect() as connection:
            result = connection.execute(text(sql_query))
            return result.fetchall()  # Fetch all results
    except Exception as e:
        print(f"Error in process_query_from_file: {e}")


def get_answer_with_agents(query, related_chunks, db):
    print("AgentManager: Route to the required agents")

    agent = route_agent(query, related_chunks)

    if "agent1" in agent.content:
        answer = generate_answer_with_agent1(query, related_chunks)
    elif "agent3" in agent.content:
        answer = fetch_information_from_web_agent3(query)
    elif "agent4" in agent.content:
        sql_file_path = fetch_data_from_database_agent4(query, related_chunks, db)
        if sql_file_path is None:
            print("SQL Query file is None")
            return

        sql_response = process_query_from_file(sql_file_path, db)
        for row in sql_response:
            print(row)
        return

    formatted_answer = validate_and_format_with_agent2(answer, related_chunks)
    return formatted_answer

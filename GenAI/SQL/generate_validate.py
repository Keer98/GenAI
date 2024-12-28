import mysql.connector
from mysql.connector import Error
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import re  # To clean unwanted formatting from the SQL query

# Initialize the language model
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key="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",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

# Function to retrieve schema information for the entire database
def get_schema_info(connection):
    schema_info = ""
    try:
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        
        for (table_name,) in tables:
            schema_info += f"Table: {table_name}\n"
            cursor.execute(f"DESCRIBE {table_name};")
            columns = cursor.fetchall()
            schema_info += "Columns: " + ", ".join([col[0] for col in columns]) + "\n\n"
        
        cursor.close()
    except Error as e:
        print(f"Error retrieving schema information: {e}")
    return schema_info

# Function to clean and extract valid SQL query
def clean_sql_query(sql_query):
    # Remove any unwanted formatting like ```sql ... ```
    cleaned_query = re.sub(r"```(?:sql)?\n?|```", "", sql_query).strip()
    return cleaned_query

# Define the prompt template
prompt_template = PromptTemplate(
    input_variables=["text", "schema_info"],
    template="""
You are an expert SQL query writer. You have the following schema information:
{schema_info}
Convert the following text into a valid SQL query:
Text: {text}
SQL:
No preamble, just give the SQL query.
"""
)

# Create an LLM chain
chain = LLMChain(llm=llm, prompt=prompt_template)

# Initialize the database connection
connection = None

try:
    # Establish the connection
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='keerthi@98',
        database='kap',
        port=3305
    )

    if connection.is_connected():
        print("Connection to database established.")
        
        # Retrieve schema information
        schema_info = get_schema_info(connection)
        if not schema_info:
            raise ValueError("Schema information is empty. Please check your database connection and data.")
        
        # Input natural language text
        text_input = input("Enter your query: ")
        
        # Generate SQL query using LLM
        raw_sql_query = chain.run({"text": text_input, "schema_info": schema_info}).strip()
        sql_query = clean_sql_query(raw_sql_query)
        
        print("\nGenerated SQL Query:")
        print(sql_query)

        # Validate and execute the SQL query
        if sql_query.lower().startswith("select"):
            cursor = connection.cursor()
            cursor.execute(sql_query)  # Execute the cleaned SQL query
            
            # Fetch all results
            results = cursor.fetchall()
            print("\nQuery Results:")
            for row in results:
                print(row)
        else:
            print("Generated SQL query is not a valid SELECT statement. Only SELECT queries are allowed.")
except Error as e:
    print(f"Error: {e}")
except ValueError as ve:
    print(f"Validation Error: {ve}")
finally:
    # Close the connection
    if connection and connection.is_connected():
        connection.close()
        print("\nMySQL connection is closed.")

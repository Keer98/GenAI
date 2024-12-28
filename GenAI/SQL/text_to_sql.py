from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import mysql.connector
from mysql.connector import Error

# Initialize the language model
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key="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",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

# Define the prompt template
prompt = PromptTemplate(
    input_variables=["text"],
    template="""
You are an expert SQL query writer. Convert the following text into a valid SQL query:
Text: {text}
SQL:[No preamble]
"""
)

# Create an LLM chain
chain = LLMChain(llm=llm, prompt=prompt)

# Input natural language text
text_input = input("Enter your query: ")
sql_query = chain.run({"text": text_input}).strip()  # Generate and clean the SQL query

# Print the generated SQL query for debugging
print("Generated SQL Query:")
print(sql_query)

# Initialize the database connection
connection = None

try:
    # Establish the connection
    print("Attempting to connect to the database...")  # Debug statement
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='keerthi@98',
        database='kap',
        port=3305
    )

    if connection.is_connected():
        print("Connection established.")  # Debug statement
        cursor = connection.cursor()
        
        # Execute the SQL query
        cursor.execute(sql_query)  # Execute the generated SQL query
        
        # Fetch all results
        results = cursor.fetchall()
        
        # Print the results
        for row in results:
            print(row)

except Error as e:
    print(f"Error executing query: {e}")

finally:
    # Close the connection
    if connection and connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
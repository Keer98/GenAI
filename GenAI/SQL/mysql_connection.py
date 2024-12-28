import mysql.connector
from mysql.connector import Error


try:
    # Establish the connection
    print("Attempting to connect to the database...")  # Debug statement
    connection = mysql.connector.connect(
        host='localhost',          # e.g., 'localhost' or an IP address
        user='root',      # e.g., 'root'
        password='keerthi@98',  # your database password
        database='kap',   # the database you want to connect to
        port=3305 
    )

    if connection.is_connected():
        print("Connection established.")  # Debug statement
        db_info = connection.get_server_info()
        print(f"Connected to MySQL Server version {db_info}")
        cursor = connection.cursor()
        cursor.execute("SELECT DATABASE();")
        record = cursor.fetchone()
        print(f"You're connected to database: {record}")

        # Execute the SQL query
        cursor.execute("SELECT DISTINCT startDate FROM enrollmentdetailcalendars; limit 5;")
        
        # Fetch all results
        results = cursor.fetchall()
        
        # Print the results
        for row in results:
            print(row)

except Error as e:
    print(f"Error while connecting to MySQL: {e}")

finally:
    # Close the connection
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")

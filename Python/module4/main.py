import os
import sys
import json
import datetime
import math
import re
from importlib import reload
import random

# Importing the custom module
import mymodule

def load_json_file(file_path):
    """Function to load JSON data with file handling and exception management."""
    try:
        # Checking if the file exists
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                data = json.load(file)
                print("JSON Data Loaded Successfully.")
                return data
        else:
            raise FileNotFoundError(f"{file_path} not found.")
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        print(f"Attempted to open {file_path}. Closing file if it was opened.")
        
def use_mymodule():
    """Demonstrate usage of custom module functions."""
    print("Using square_root(16) from mymodule:", mymodule.square_root(16))
    print("Current Time from mymodule:", mymodule.current_time())
    
    # Testing regular expression function
    email = "test@example.com"
    print(f"Is {email} a valid email? {mymodule.validate_email(email)}")

if __name__ == "__main__":
    # First use of the module
    use_mymodule()
    
    # Now let's modify the module manually before reloading it
    print("\nModifying and reloading the module...")

    # Simulating modification in 'mymodule.py' at runtime.
    with open('mymodule.py', 'a') as module_file:
        module_file.write("\n# New function added during runtime\n")
        module_file.write("def cube_root(x):\n")
        module_file.write("    return x ** (1/3)\n")

    try:
        print("Using cube_root(27) from the reloaded mymodule:", mymodule.cube_root(27))
    except:
        print("cube_root function not found in the mymodule. if you update it recently, please reload the module and try again.")
    # Reload the modified module
    reload(mymodule)

    # Now using the modified module with the new cube_root function
    print("Using cube_root(27) from the reloaded mymodule:", mymodule.cube_root(27))

    # Example of exception handling with file operations
    json_data = load_json_file('data.json')
    
    # Using standard libraries
    print("Math module usage (logarithm of 1000):", math.log(1000))
    print("Current date and time:", datetime.datetime.now())
    print("Random number between 1 and 10:", random.randint(1, 10))
    
    print(f"Command-line arguments: {sys.argv}")

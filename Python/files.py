import os

folder_path = r'C:\Users\windows-user\Desktop\GenAI-1'
file_path = os.path.join(folder_path, 'my_file.txt')

try:
    with open(file_path, 'r') as file:
        print(f"File already exists at: {file_path}")
        for line in file:
            print(line)

except FileNotFoundError:
    
    print(f"File does not exist. Creating file at: {file_path}")
  
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    with open(file_path, 'w') as file:
        file.write("This is the content of the file.")
    
    print(f"File created at: {file_path}")

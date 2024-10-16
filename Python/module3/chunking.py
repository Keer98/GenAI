import os


input_file_path = r'C:\Users\windows-user\Desktop\GenAI-1\chunck.txt'
output_directory = r'C:\Users\windows-user\Desktop\GenAI-1'

try:
    with open(input_file_path, 'r') as file:
        content = file.read()
        paragraphs = content.split('\n\n')
        print(paragraphs)

        for i, paragraph in enumerate(paragraphs):
            paragraph_file_name = f'paragraph_{i + 1}.txt'
            paragraph_file_path = os.path.join(output_directory, paragraph_file_name)

            with open(paragraph_file_path, 'w') as paragraph_file:
                paragraph_file.write(paragraph.strip())

            print(f'Created file: {paragraph_file_path}')

except FileNotFoundError:
    print(f'The file {input_file_path} does not exist.')


#skills=json_cus_res['Skills']
#print(skills)
def format_skills(skills):
    formatted_skills = {}
    for key, values in skills.items():
        # Join list items into a single string and remove unwanted characters
        formatted_skills[key] = ','.join(values)
    return formatted_skills

# Format the dictionary



def format_responsibilities(data):
    for idx in range(len(data)):
        data[idx] = " . " + data[idx]  # Update the element in the list directly
        
    return data
    

# Call the function to print the data

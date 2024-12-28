import re

def extract_table_names(chunks):
    """
    Extract table names from the provided SQL chunks.

    Args:
        chunks (list): List of SQL chunk strings.

    Returns:
        list: Extracted table names.
    """
    table_names = []
    table_pattern = r"CREATE TABLE\s+`?(\w+)`?"  # Regex to match table names

    
    for line in chunks.split("\n"):  # Split chunk into lines
        match = re.search(table_pattern, line)
        if match:
            table_name = match.group(1)
            table_names.append(table_name)

    return table_names

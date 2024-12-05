import warnings

warnings.filterwarnings("ignore")

def format_output(text):
    """Formats the output for readability."""
    # Split lines and strip unnecessary spaces
    lines = text.split("\n")
    formatted_lines = [line.strip() for line in lines if line.strip() != ""]
    return "\n".join(formatted_lines)
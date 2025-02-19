import math
import datetime

def square_root(x):
    return math.sqrt(x)

def current_time():
    return datetime.datetime.now()

def validate_email(email):
    import re
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None



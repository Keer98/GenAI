# utils.py
import time

def monitor_folder(directory, check_interval=10):
    """Monitor a folder for new files."""
    known_files = set()
    while True:
        yield known_files
        time.sleep(check_interval)

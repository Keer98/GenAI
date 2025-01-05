# file_watcher.py
import os

def get_existing_files(directory):
    """Return a set of files in the directory."""
    return {file for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))}

def detect_changes(directory, known_files):
    """Detect new and deleted files in the directory."""
    current_files = get_existing_files(directory)
    new_files = current_files - known_files
    deleted_files = known_files - current_files
    return new_files, deleted_files

import os
import re
from collections import defaultdict

def sanitize_filename(filename):
    """Sanitize a file name to remove or replace invalid characters."""
    # Remove all special characters, including underscores and periods
    return re.sub(r'[^a-zA-Z0-9]', '', filename)

def process_directory(directory_path):
    """Process files in the directory, deduplicate by normalized names."""
    # Dictionary to track the first encountered file for each normalized name
    seen_files = {}
    
    # Traverse all files in the directory
    for file_name in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file_name)

        # Skip directories, focus only on files
        if not os.path.isfile(file_path):
            continue

        # Get file extension and sanitize the base name
        base_name, ext = os.path.splitext(file_name)
        sanitized_name = sanitize_filename(base_name) + ext
        print(sanitized_name)

        if sanitized_name in seen_files:
            # Duplicate detected, delete the file
            print(f"Deleting duplicate file: {file_path}")
            os.remove(file_path)
        else:
            # Mark this sanitized name as seen
            seen_files[sanitized_name] = file_path

if __name__ == "__main__":
    # Directory path to process
    directory_path = input("Enter the path of the directory to process: ").strip()

    if not os.path.exists(directory_path):
        print("The specified directory does not exist.")
    else:
        process_directory(directory_path)
        print("Deduplication process completed.")

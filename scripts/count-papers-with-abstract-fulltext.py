import csv
import os
import re
import sys

# Increase field size limit to handle large fields
csv.field_size_limit(min(sys.maxsize, 2**31 - 1))

def sanitize_filename(filename):
    filename = filename.replace("/", "_")
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def compare_dois_with_files(csv_path, folder_path):
    try:
        # Read DOIs from CSV and normalize them
        with open(csv_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            csv_dois = set(sanitize_filename(row['DOI']) for row in reader if row['DOI'].strip())

        # List normalized filenames in the folder (excluding extensions)
        folder_files = set(
            os.path.splitext(f)[0] for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))
        )

        # Compare DOIs with files
        unmatched_files = folder_files - csv_dois
        unmatched_count = len(unmatched_files)

        # Print results
        print(f"Total DOIs in CSV: {len(csv_dois)}")
        print(f"Total files in folder: {len(folder_files)}")
        print(f"Unmatched files count: {unmatched_count}")
        if unmatched_files:
            print("Unmatched files:")
            for file in unmatched_files:
                print(file)

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except KeyError as e:
        print(f"Error: Missing expected column {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
csv_path = input("Enter the path to the CSV file: ")
folder_path = input("Enter the path to the folder: ")
compare_dois_with_files(csv_path, folder_path)
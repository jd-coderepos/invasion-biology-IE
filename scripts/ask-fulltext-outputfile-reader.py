import csv
import sys
import statistics

# Set a reasonable large limit for CSV field size
csv.field_size_limit(10**7)  # Setting limit to 10 million characters

# Function to count tokens by splitting text on spaces
def count_tokens(text):
    return len(text.split())

def read_csv_and_process(file_path):
    total_rows = 0
    no_abstract_no_fulltext = 0
    abstract_no_fulltext = 0
    both_abstract_and_fulltext = 0

    # Lists to store abstract and full-text lengths
    abstract_lengths = []
    full_text_lengths = []
    
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            total_rows += 1
            doi = row["DOI"]
            abstract = row["Abstract"]
            full_text = row["Full-text"]

            print(f"Processing row {total_rows}: DOI = {doi}")
            
            abstract_token_count = count_tokens(abstract)
            full_text_token_count = count_tokens(full_text)
            
            has_abstract = abstract != "N/A" and abstract_token_count >= 10
            has_fulltext = full_text != "N/A" and full_text_token_count >= 10
            
            if not has_abstract and not has_fulltext:
                no_abstract_no_fulltext += 1
                print("No abstract and no full-text available")
            elif has_abstract and not has_fulltext:
                abstract_no_fulltext += 1
                abstract_lengths.append(abstract_token_count)
                print(f"Abstract token length: {abstract_token_count}")
                print("No full-text available")
            elif has_abstract and has_fulltext:
                both_abstract_and_fulltext += 1
                abstract_lengths.append(abstract_token_count)
                full_text_lengths.append(full_text_token_count)
                print(f"Abstract token length: {abstract_token_count}")
                print(f"Full-text token length: {full_text_token_count}")
            elif has_abstract:
                abstract_lengths.append(abstract_token_count)
        
        # Print total rows count
        print(f"\nTotal DOIs (rows) processed: {total_rows}")
        print(f"Rows with no abstracts and no full-text: {no_abstract_no_fulltext}")
        print(f"Rows with abstracts but no full-text: {abstract_no_fulltext}")
        print(f"Rows with both abstracts and full-text: {both_abstract_and_fulltext}")

        # Compute and print statistics for abstract lengths for all rows with abstracts
        if abstract_lengths:
            print(f"\nAbstract Length Statistics (for all rows with abstracts):")
            print(f"Min Abstract Length: {min(abstract_lengths)}")
            print(f"Max Abstract Length: {max(abstract_lengths)}")
            print(f"Avg Abstract Length: {statistics.mean(abstract_lengths)}")

        # Compute and print statistics for full-text lengths where both abstract and full-text are present
        if full_text_lengths:
            print(f"\nFull-text Length Statistics (only where full-text is present):")
            print(f"Min Full-text Length: {min(full_text_lengths)}")
            print(f"Max Full-text Length: {max(full_text_lengths)}")
            print(f"Avg Full-text Length: {statistics.mean(full_text_lengths)}")

# Get the input file path from the user
file_path = input("Please enter the path to the CSV file: ")

read_csv_and_process(file_path)

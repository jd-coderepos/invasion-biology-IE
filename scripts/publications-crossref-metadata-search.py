import csv
import requests
import time
import os

# Function to get metadata from Crossref API using DOI
def get_metadata_from_doi(doi, failed_dois_file):
    api_url = f"https://api.crossref.org/works/{doi}"
    try:
        response = requests.get(api_url)
        if response.status_code == 429:  # Rate limit hit, need to back off
            print(f"Rate limit reached. Backing off for 12 seconds...")
            time.sleep(12)  # Backoff for 12 seconds
            return get_metadata_from_doi(doi, failed_dois_file)  # Retry the request after backoff
        response.raise_for_status()  # Raise an error for other bad status codes
        data = response.json()
        if data['status'] == 'ok':
            message = data['message']
            
            # Extract the published-print date parts
            date_parts_print = message.get('published-print', {}).get('date-parts', [['N/A', 'N/A', 'N/A']])[0]
            print_year = date_parts_print[0] if len(date_parts_print) > 0 else 'N/A'
            print_month = date_parts_print[1] if len(date_parts_print) > 1 else 'N/A'
            print_day = date_parts_print[2] if len(date_parts_print) > 2 else 'N/A'
            
            # Extract the published date parts (general published)
            date_parts_published = message.get('published', {}).get('date-parts', [['N/A', 'N/A', 'N/A']])[0]
            pub_year = date_parts_published[0] if len(date_parts_published) > 0 else 'N/A'
            pub_month = date_parts_published[1] if len(date_parts_published) > 1 else 'N/A'
            pub_day = date_parts_published[2] if len(date_parts_published) > 2 else 'N/A'
            
            # Handle empty container-title gracefully
            journal_title = message.get('container-title', [])
            journal = journal_title[0] if journal_title else 'N/A'
            
            # Handle empty title gracefully
            title = message.get('title', [])
            title = title[0] if title else 'N/A'
            
            # Extract the required metadata
            metadata = {
                "DOI": message.get('DOI', 'N/A'),
                "Title": title,
                "Type": message.get('type', 'N/A'),
                "Published Print Year": print_year,
                "Published Print Month": print_month,
                "Published Print Day": print_day,
                "Published Year": pub_year,
                "Published Month": pub_month,
                "Published Day": pub_day,
                "Journal": journal,
                "Volume": message.get('volume', 'N/A'),
                "Issue": message.get('issue', 'N/A'),
                "Page Range": message.get('page', 'N/A'),
                "Publisher": message.get('publisher', 'N/A'),
                "Authors": ", ".join([f"{author.get('given', '')} {author.get('family', '')}".strip() for author in message.get('author', [])]),
                "Is Referenced By Count": message.get('is-referenced-by-count', 'N/A'),
                "Subtitle": ", ".join(message.get('subtitle', [])) if message.get('subtitle') else 'N/A',
                "Short Title": ", ".join(message.get('short-title', [])) if message.get('short-title') else 'N/A'
            }
            return metadata
    except requests.exceptions.RequestException as e:
        print(f"Error fetching metadata for DOI {doi}: {e}")
        # Log the failed DOI to the file
        with open(failed_dois_file, mode='a', newline='', encoding='utf-8') as failed_file:
            writer = csv.writer(failed_file)
            writer.writerow([doi])
    return None

# Function to save progress after every batch
def write_results_to_file(output_file_path, results, write_header=False):
    fieldnames = [
        "DOI", "Title", "Type", "Published Print Year", "Published Print Month", "Published Print Day",
        "Published Year", "Published Month", "Published Day", "Journal", "Volume", "Issue", "Page Range",
        "Publisher", "Authors", "Is Referenced By Count", "Subtitle", "Short Title"
    ]
    
    mode = 'a' if not write_header else 'w'
    with open(output_file_path, mode=mode, newline='', encoding='utf-8') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()
        writer.writerows(results)

# Function to track processed DOIs in a file and resume from where it left off
def get_processed_dois(processed_dois_file):
    if os.path.exists(processed_dois_file):
        with open(processed_dois_file, mode='r', newline='', encoding='utf-8') as file:
            return set(line.strip() for line in file)
    return set()

# Function to append processed DOIs in batch after writing to the output file
def append_processed_dois(processed_dois_file, processed_dois):
    with open(processed_dois_file, mode='a', newline='', encoding='utf-8') as file:
        for doi in processed_dois:
            file.write(f"{doi}\n")

# Main function to read DOIs from CSV, fetch metadata, and save progress periodically
def process_csv_and_fetch_metadata(csv_file_path, output_file_path, failed_dois_file, processed_dois_file, batch_size=100):
    processed_dois_set = get_processed_dois(processed_dois_file)
    results = []
    batch_dois = []  # Track DOIs for the current batch
    count = 0
    write_header = not os.path.exists(output_file_path)  # Write header if file doesn't exist

    # Open the CSV file and read rows
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            doi = row.get('doi.value', '').strip()
            if doi and doi not in processed_dois_set:
                metadata = get_metadata_from_doi(doi, failed_dois_file)
                if metadata:
                    results.append(metadata)
                    batch_dois.append(doi)  # Add DOI to the current batch
                    count += 1
                
                # Every batch_size (e.g., 100), write the results and processed DOIs to the files
                if count % batch_size == 0:
                    write_results_to_file(output_file_path, results, write_header)
                    append_processed_dois(processed_dois_file, batch_dois)
                    results = []  # Reset the results list
                    batch_dois = []  # Reset the batch DOI list
                    write_header = False  # Only write header once
                    print(f"Processed {count} records so far.")
        
        # Write any remaining results and DOIs at the end
        if results:
            write_results_to_file(output_file_path, results, write_header)
            append_processed_dois(processed_dois_file, batch_dois)
            print(f"Final batch processed, total {count} records.")

    print(f"Metadata for {count} articles written to {output_file_path}")
    print(f"Failed DOIs written to {failed_dois_file}")

# Example usage
csv_file_path = "..\\wikidata-invasion-biology-corpus\\Publications.csv"  # Path to the input CSV file with DOIs
output_file_path = "..\\data\\all-publications\\crossref-metadata\\publications_metadata.csv"  # Path to save the fetched metadata
failed_dois_file = "..\\data\\all-publications\\crossref-metadata\\failed_dois.csv"  # Path to save the DOIs that failed
processed_dois_file = "..\\data\\all-publications\\crossref-metadata\\processed_dois.txt"  # File to keep track of processed DOIs

# Ensure the failed DOIs file is initialized with headers
with open(failed_dois_file, mode='w', newline='', encoding='utf-8') as failed_file:
    writer = csv.writer(failed_file)
    writer.writerow(["DOI"])

process_csv_and_fetch_metadata(csv_file_path, output_file_path, failed_dois_file, processed_dois_file)

import requests
import json
import pandas as pd
import csv
import time
import os

# Function to make the GET request and fetch data from the API using the provided DOI
def fetch_orkg_data_by_doi(doi, retry_count=1, max_retries=2, backoff_time=12):
    url = f"https://api.ask.orkg.org/index/explore?filter=doi%20IN%20[%22{doi}%22]"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for HTTP errors

        # Parse the JSON response
        data = response.json()

        # Access the total number of hits and the items
        total_hits = data['payload'].get('total_hits', 0)
        items = data['payload'].get('items', [])

        # If no items are found
        if not items:
            return None
        
        # Only process the first item if there are multiple (to avoid duplicates)
        return process_item(items[0])

    except requests.exceptions.HTTPError as http_err:
        if response.status_code in [404, 422]:
            error_type = "404 Client Error" if response.status_code == 404 else "422 Validation Error"
            if retry_count < max_retries:
                time.sleep(backoff_time)  # Backoff before retrying
                return fetch_orkg_data_by_doi(doi, retry_count + 1)  # Retry with the same DOI
            else:
                return {'error': error_type, 'message': str(http_err)}
        else:
            return {'error': 'HTTPError', 'message': str(http_err)}
    except Exception as err:
        return {'error': 'GeneralError', 'message': str(err)}

# Function to process each item from the API response and return a formatted row
def process_item(item):
    # Extract relevant fields
    item_id = item.get('id', 'N/A')
    doi = item.get('doi', 'N/A')
    title = item.get('title', 'N/A')
    
    # Escape abstract and full-text fields to avoid noise in CSV output
    abstract = clean_text(item.get('abstract', 'N/A'))
    full_text = clean_text(item.get('full_text', 'N/A'))
    
    # Return as a list for writing to CSV
    return [item_id, doi, title, abstract, full_text]

# Function to clean and escape text (for handling potential noise in abstract/full-text fields)
def clean_text(text):
    if text and text != 'N/A':
        # Replace problematic newlines but keep commas intact for proper formatting
        return text.replace('\n', ' ').replace('\r', ' ').strip()
    return 'N/A'

# Function to log DOIs that were not found
def log_not_found(doi, not_found_file):
    with open(not_found_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([doi])

# Function to log DOIs with errors
def log_error(doi, error_details, error_file):
    with open(error_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([doi, error_details.get('error', 'UnknownError'), error_details.get('message', 'No message')])

# Function to log processed DOIs
def log_processed(doi, processed_file):
    with open(processed_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([doi])

# Function to read already processed DOIs from the log file
def load_processed_dois(processed_file):
    if os.path.exists(processed_file):
        with open(processed_file, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            return set(row[0] for row in reader)  # Return set of processed DOIs
    return set()  # If file does not exist, return an empty set

# Function to read DOIs from the CSV file, fetch data for each DOI, and write the output to another CSV
def process_dois_from_csv(input_file_path, output_file_path, not_found_file, error_file, processed_file):
    try:
        # Load already processed DOIs
        processed_dois = load_processed_dois(processed_file)

        # Read the CSV file
        df = pd.read_csv(input_file_path)

        # Check if the DOI column exists (case insensitive)
        if 'DOI' in df.columns:
            doi_column = 'DOI'
        elif 'doi' in df.columns:
            doi_column = 'doi'
        else:
            print("No DOI column found in the CSV file.")
            return

        # Open the output CSV file for writing
        with open(output_file_path, mode='w', newline='', encoding='utf-8') as output_file:
            csv_writer = csv.writer(output_file, quoting=csv.QUOTE_ALL)  # Quote all fields to preserve commas

            # Write the header row
            csv_writer.writerow(['ASK ID', 'DOI', 'Title', 'Abstract', 'Full-text'])

            # Iterate through the DOIs and fetch data for each
            for i, doi in enumerate(df[doi_column].dropna(), start=1):
                if doi in processed_dois:
                    continue  # Skip already processed DOIs

                result = fetch_orkg_data_by_doi(doi)

                if result is None:
                    # Log DOIs not found
                    log_not_found(doi, not_found_file)
                elif 'error' in result:
                    # Log DOIs with errors
                    log_error(doi, result, error_file)
                else:
                    # Write the processed data to the output CSV
                    csv_writer.writerow(result)

                # Log the DOI as processed
                log_processed(doi, processed_file)
                
                # Rate limiting: sleep for 0.1 seconds to ensure no more than 10 queries per second
                time.sleep(0.1)

                # Print progress every 100 DOIs processed
                if i % 100 == 0:
                    print(f"{i} DOIs processed.")

        print(f"\nData successfully written to {output_file_path}")

    except FileNotFoundError:
        print(f"File not found: {input_file_path}")
    except Exception as e:
        print(f"An error occurred while processing the CSV: {e}")

# Entry point of the script
if __name__ == "__main__":
    # Prompt the user to enter the input CSV file path, output file path, not found file path, and error file path
    input_file_path = input("Please enter the path to the input CSV file containing DOIs: ")
    output_file_path = input("Please enter the path to the output CSV file: ")
    not_found_file = input("Please enter the path to the CSV file to log DOIs not found in ASK: ")
    error_file = input("Please enter the path to the CSV file to log errors: ")
    processed_file = input("Please enter the path to the CSV file to log processed DOIs: ")
    
    process_dois_from_csv(input_file_path, output_file_path, not_found_file, error_file, processed_file)

import csv
import requests
import json

# Input and output file paths
input_file = "C:\\Users\\dsouzaj\\Desktop\\Datasets\\orkg-ask-ecology\\wikidata-invasion-biology-corpus\\Publications.csv"  # Replace with your actual input file path
output_file = "C:\\Users\\dsouzaj\\Desktop\\Datasets\\invasion-biology-ask-dataset\\data\\publications-with-full_text.csv"
error_log_file = "C:\\Users\\dsouzaj\\Desktop\\Datasets\\invasion-biology-ask-dataset\\data\\publications-error_log.csv"  # File to store erroneous DOIs

# API base URL
base_url = "https://api.ask.orkg.org/index/get/"

# Headers for the output CSV file
output_headers = ["title", "doi", "authors", "year", "abstract", "full_text", "subjects", "topics", "journals", "publisher"]

def fetch_metadata(doi):
    # Construct the URL with the document_id being the DOI
    url = f"{base_url}{doi}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json().get("payload", {})
        
        # Check if 'full_text' is present
        if data.get("full_text"):
            # Extract relevant fields from the payload
            metadata = {
                "title": data.get("title", ""),
                "doi": data.get("doi", ""),
                "authors": ", ".join(data.get("authors", [])),
                "year": data.get("year", ""),
                "abstract": data.get("abstract", ""),
                "full_text": data.get("full_text", ""),
                "subjects": ", ".join(data.get("subjects", [])),
                "topics": ", ".join(data.get("topics", [])),
                "journals": ", ".join(data.get("journals", [])),
                "publisher": data.get("publisher", "")
            }
            return metadata
        else:
            return None  # Full text not available
    except requests.RequestException as e:
        print(f"Error fetching metadata for DOI {doi}: {e}")
        # Log the erroneous DOI to the error log file
        with open(error_log_file, mode='a', newline='', encoding='utf-8') as error_file:
            error_writer = csv.writer(error_file)
            error_writer.writerow([doi, str(e)])
        return None

# Read the input CSV with UTF-8 encoding, fetch data from the API, and write to output CSV
with open(input_file, newline='', encoding='utf-8') as infile, open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
    reader = csv.DictReader(infile)
    writer = csv.DictWriter(outfile, fieldnames=output_headers)
    writer.writeheader()  # Write header to the output CSV
    
    # Initialize error log file with a header if it doesn't already exist
    with open(error_log_file, mode='w', newline='', encoding='utf-8') as error_file:
        error_writer = csv.writer(error_file)
        error_writer.writerow(["doi", "error_message"])

    for row in reader:
        doi = row.get("doi.value")
        if doi:  # Check if DOI is present
            metadata = fetch_metadata(doi)
            if metadata:
                writer.writerow(metadata)  # Write row only if full_text is available

print(f"Metadata fetched and written to {output_file}")
print(f"DOIs with errors written to {error_log_file}")

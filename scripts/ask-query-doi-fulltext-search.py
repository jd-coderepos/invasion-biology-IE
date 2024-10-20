import requests
import json

# Function to make the GET request and fetch data from the API using the provided DOI
def fetch_orkg_data_by_doi(doi):
    url = f"https://api.ask.orkg.org/index/explore?filter=doi%20IN%20[%22{doi}%22]"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for HTTP errors

        # Parse the JSON response
        data = response.json()

        # Access the total number of hits and the items
        total_hits = data['payload'].get('total_hits', 0)
        items = data['payload'].get('items', [])
        
        # Log the number of items retrieved
        print(f"Retrieved {len(items)} out of {total_hits} records")

        # If no items are found
        if not items:
            print(f"No records found for DOI: {doi}")
            return
        
        # Iterate through and process each item
        for item in items:
            process_item(item)

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")

# Function to process each item from the API response
def process_item(item):
    # Extract relevant fields (example fields shown below)
    item_id = item.get('id', 'N/A')
    doi = item.get('doi', 'N/A')
    title = item.get('title', 'N/A')
    year = item.get('year', 'N/A')
    
    # Print the basic information
    print(f"ID: {item_id}, DOI: {doi}, Title: {title}, Year: {year}")
    
    # Check if abstract is available and calculate token count
    abstract = item.get('abstract', None)
    if abstract:
        abstract_token_count = len(abstract.split())
        print(f"Abstract is available. Token count: {abstract_token_count}")
    else:
        print("Abstract is not available.")
    
    # Check if full-text is available and calculate token count
    full_text = item.get('full_text', None)
    if full_text:
        full_text_token_count = len(full_text.split())
        print(f"Full-text is available. Token count: {full_text_token_count}")
    else:
        print("Full-text is not available.")

# Entry point of the script
if __name__ == "__main__":
    # Prompt the user to enter the DOI
    user_doi = input("Please enter the DOI: ")
    fetch_orkg_data_by_doi(user_doi)

import requests
import csv
import pandas as pd

def sanitize(text):
    """
    Sanitize the text for CSV output by removing newline characters and escaping quotes.
    If text is None, convert it to an empty string before processing.
    """
    if text is None:
        text = ''
    return text.replace('\n', ' ').replace('\r', ' ').replace('"', '""')

def sanitize_list(items):
    """
    Sanitize and convert a list of items to a single string for CSV output.
    """
    return ', '.join([sanitize(item) for item in items if item])

def search_publications(hypothesis):
    """
    Perform an API GET request to search for the top 50 relevant publications based on a hypothesis.
    """
    url = 'https://api.ask.orkg.org/index/search'
    params = {
        'query': hypothesis,
        'limit': 50#,
        #'filter': 'year > 2010'  # Example filter, modify as needed
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()['payload']['items']
    else:
        print(f"Failed to fetch data for hypothesis: {hypothesis}")
        return []

def main(input_file_path, output_file_path):
    """
    Read hypotheses from an input CSV file, search for publications, and write results to an output CSV file.
    """
    df = pd.read_csv(input_file_path)
    with open(output_file_path, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = [
            'hypothesis', 'publication_id', 'title', 'doi', 'authors', 'year', 'abstract', 
            'full_text', 'subjects', 'topics', 'journals', 'publisher'
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        
        for hypothesis in df['itemLabel.value']:
            print(f"Searching for: {hypothesis}")
            publications = search_publications(hypothesis)
            for pub in publications:
                writer.writerow({
                    'hypothesis': hypothesis,
                    'publication_id': pub.get('id', ''),
                    'title': sanitize(pub.get('title', '')),
                    'doi': pub.get('doi', ''),
                    'authors': sanitize(', '.join(pub.get('authors', []))),
                    'year': pub.get('year', ''),
                    'abstract': sanitize(pub.get('abstract', '')),
                    'full_text': sanitize(pub.get('full_text', '')),
                    'subjects': sanitize_list(pub.get('subjects', [])),
                    'topics': sanitize_list(pub.get('topics', [])),
                    'journals': sanitize_list(pub.get('journals', [])),
                    'publisher': sanitize(pub.get('publisher', ''))
                })

if __name__ == "__main__":
    input_file_path = 'C:\\Users\\dsouzaj\\Desktop\\Datasets\\orkg-ask-ecology\\wikidata-invasion-biology-corpus\\Hypotheses.csv'  # Path to the input CSV file containing hypotheses
    output_file_path = 'hypotheses-based-publications.csv'  # Path to the output CSV file to store the search results
    main(input_file_path, output_file_path)

import requests
from stringmatch import Ratio

# Initialize the Ratio class from stringmatch library
ratio = Ratio()

def get_paper_data(title):
    # API endpoint
    endpoint = "https://api.semanticscholar.org/graph/v1/paper/search/match"
    
    # Query parameters
    params = {
        'query': title,
        'fields': 'paperId,title,matchScore,authors,citations.title,citations.abstract,embedding.specter_v2,fieldsOfStudy'
    }

    # Send the request to the API
    response = requests.get(endpoint, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()

        # Extract and print relevant information
        if data:
            paper_id = data.get('paperId', 'No paper ID available')
            paper_title = data.get('title', 'No title available')
            match_score = data.get('matchScore', 'No match score available')
            authors = ', '.join([author['name'] for author in data.get('authors', [])])
            citations = data.get('citations', [])
            embedding = data.get('embedding', {}).get('specter_v2', 'No embedding available')
            fields_of_study = ', '.join(data.get('fieldsOfStudy', []))

            # Calculate string match ratio between the input title and the returned title
            match_ratio = ratio.ratio(title, paper_title)

            print(f"Input Title: {title}")
            print(f"Returned Title: {paper_title}")
            print(f"Title Match Ratio: {match_ratio:.2f}%")
            print(f"Paper ID: {paper_id}")
            print(f"Match Score: {match_score}")
            print(f"Authors: {authors}")
            print(f"Fields of Study: {fields_of_study}")
            print(f"Specter V2 Embedding: {embedding}")
            
            print("\nCitations:")
            for citation in citations:
                citation_title = citation.get('title', 'No title available')
                citation_abstract = citation.get('abstract', 'No abstract available')
                print(f" - Title: {citation_title}")
                print(f"   Abstract: {citation_abstract}")
        else:
            print("No data found for the given title.")
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")

# User input for the paper title
paper_title_input = input("Enter the paper title: ")

# Fetch and print the data
get_paper_data(paper_title_input)

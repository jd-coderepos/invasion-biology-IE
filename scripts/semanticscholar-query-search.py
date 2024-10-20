import requests

def get_top_papers(title):
    # API endpoint
    endpoint = "https://api.semanticscholar.org/graph/v1/paper/search"
    
    # Query parameters
    params = {
        'query': title,
        'offset': 0,  # Start from the first result
        'limit': 5,   # Limit the results to the top 5
        'fields': 'paperId,title,matchScore,authors,citations.title,citations.abstract,embedding.specter_v2,fieldsOfStudy'
    }

    try:
        # Send the request to the API
        response = requests.get(endpoint, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()

            # Extract and print relevant information from the results
            papers = data.get('data', [])
            if papers:
                for i, paper in enumerate(papers, 1):
                    paper_id = paper.get('paperId', 'No paper ID available')
                    paper_title = paper.get('title', 'No title available')
                    match_score = paper.get('matchScore', 'No match score available')
                    authors = ', '.join([author['name'] for author in paper.get('authors', [])])
                    fields_of_study = ', '.join(paper.get('fieldsOfStudy', []))
                    embedding = paper.get('embedding', {}).get('specter_v2', 'No embedding available')

                    print(f"Result {i}:")
                    print(f"Paper ID: {paper_id}")
                    print(f"Title: {paper_title}")
                    print(f"Match Score: {match_score}")
                    print(f"Authors: {authors}")
                    print(f"Fields of Study: {fields_of_study}")
                    print(f"Specter V2 Embedding: {embedding}")
                    print("="*40)
            else:
                print("No papers found for the given query.")
        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
            print(f"Response content: {response.content}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# User input for the paper title
paper_title_input = input("Enter the paper title or query: ")

# Fetch and print the top 5 papers
get_top_papers(paper_title_input)

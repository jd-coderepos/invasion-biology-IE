import pandas as pd

def count_publications_by_category(input_file, output_file, category_column):
    # Read the CSV file
    data = pd.read_csv(input_file)
    
    # Filter out rows where the specified 'category_column' might be missing
    data = data[data[category_column].notna()]
    
    # Count the occurrences of each category in the specified 'category_column'
    publication_counts = data[category_column].value_counts().reset_index()
    publication_counts.columns = [category_column, 'Total Publications']
    
    # Sort the results by the category
    publication_counts = publication_counts.sort_values(by=category_column)
    
    # Write the results to a new CSV file
    publication_counts.to_csv(output_file, index=False)
    print(f"Output written to {output_file}")

# Example usage
input_file_path = 'C:\\Users\\dsouzaj\\Desktop\\Datasets\\invasion-biology-ask-dataset\\data\\crossref_publications_metadata.csv'
#output_file_path = 'C:\\Users\\dsouzaj\\Desktop\\Datasets\\invasion-biology-ask-dataset\\data-plots\\data\\crossref_publication_counts_by_year.csv'
output_file_path = input("Enter the output file name (e.g., publication_counts_by_publisher.csv): ")
category_column = input("Enter the column name to count publications by (e.g., Publisher): ")
count_publications_by_category(input_file_path, output_file_path, category_column)

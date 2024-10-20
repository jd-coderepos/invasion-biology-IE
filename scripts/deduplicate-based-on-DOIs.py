import pandas as pd

def deduplicate_data(input_file, output_file):
    # Load the data from the CSV file
    data = pd.read_csv(input_file)
    
    # Check for duplicates in the 'DOI' column, keep the first occurrence
    deduplicated_data = data.drop_duplicates(subset='DOI', keep='first')
    
    # Write the deduplicated data to a new CSV file
    deduplicated_data.to_csv(output_file, index=False)
    print(f"Deduplicated data written to {output_file}")

# Example usage
input_file_path = '..\\data\\all-publications\\crossref-metadata\\publications_metadata.csv'
output_file_path = '..\\data\\all-publications\\crossref-metadata\\publications_metadata_deduplicated.csv'
deduplicate_data(input_file_path, output_file_path)

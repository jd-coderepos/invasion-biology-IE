import pandas as pd

def count_publications_by_category(crossref_file, ask_file, output_file, category_column):
    # Read the CSV files
    crossref_data = pd.read_csv(crossref_file)
    ask_data = pd.read_csv(ask_file)
    
    # Filter the crossref metadata based on matching DOIs from the ask publications data
    matched_data = crossref_data[crossref_data['DOI'].isin(ask_data['DOI'])]

    # Merge the ask_data to add Abstract and Full-text columns to matched_data based on DOI
    merged_data = pd.merge(matched_data, ask_data[['DOI', 'Abstract', 'Full-text']], on='DOI', how='left')
    
    # Filter out rows where the specified category column might be missing
    merged_data = merged_data[merged_data[category_column].notna()]

    # Count the total publications by category
    total_publications = merged_data.groupby(category_column).size().reset_index(name='Total Publications')

    # Add a column for "Total Publications with Abstract" where Abstract is not NA and token count >= 10
    def valid_abstract(abstract):
        return pd.notna(abstract) and len(str(abstract).split()) >= 10
    
    total_publications['Total Publications with Abstract'] = merged_data.groupby(category_column).apply(
        lambda x: sum(valid_abstract(abstract) for abstract in x['Abstract'])
    ).values

    # Add a column for "Total Publications with Full-text" where Full-text is not NA and token count >= 10
    def valid_full_text(full_text):
        return pd.notna(full_text) and len(str(full_text).split()) >= 10
    
    total_publications['Total Publications with Full-text'] = merged_data.groupby(category_column).apply(
        lambda x: sum(valid_full_text(full_text) for full_text in x['Full-text'])
    ).values

    # Ensure "Total Publications with Abstract" and "Total Publications with Full-text" don't exceed "Total Publications"
    total_publications['Total Publications with Abstract'] = total_publications[['Total Publications', 'Total Publications with Abstract']].min(axis=1)
    total_publications['Total Publications with Full-text'] = total_publications[['Total Publications', 'Total Publications with Full-text']].min(axis=1)

    # Sort the results by total publications in descending order
    total_publications = total_publications.sort_values(by='Total Publications', ascending=False)

    # Write the results to a new CSV file
    total_publications.to_csv(output_file, index=False)
    print(f"Output written to {output_file}")

# Take file paths and category input from the user
crossref_file_path = input("Enter the path for the Crossref metadata file: ")
ask_file_path = input("Enter the path for the ASK publications file: ")
output_file_path = input("Enter the output file name (e.g., publication_counts_by_category.csv): ")
category_column = input("Enter the column name to count publications by (e.g., Publisher): ")

# Call the function
count_publications_by_category(crossref_file_path, ask_file_path, output_file_path, category_column)

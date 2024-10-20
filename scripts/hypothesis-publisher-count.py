import pandas as pd

def count_publishers(output_file_path, total_output_path, per_hypothesis_output_path):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(output_file_path)
    
    # Ensure 'publisher' and 'hypothesis' columns handle any NaN values
    df['publisher'] = df['publisher'].fillna('Unknown')
    df['hypothesis'] = df['hypothesis'].fillna('No Hypothesis Provided')

    # Count total occurrences of each publisher
    total_counts = df['publisher'].value_counts()
    total_counts_df = total_counts.reset_index()
    total_counts_df.columns = ['Publisher', 'Total Count']
    total_counts_df.to_csv(total_output_path, index=False)
    print("Total publications per publisher have been written to:", total_output_path)

    # Count occurrences of each publisher per hypothesis
    hypothesis_publisher_counts = df.groupby('hypothesis')['publisher'].value_counts()
    hypothesis_publisher_counts_df = hypothesis_publisher_counts.unstack(fill_value=0).stack().reset_index()
    hypothesis_publisher_counts_df.columns = ['Hypothesis', 'Publisher', 'Count']
    hypothesis_publisher_counts_df.to_csv(per_hypothesis_output_path, index=False)
    print("Publications per publisher for each hypothesis have been written to:", per_hypothesis_output_path)

if __name__ == "__main__":
    output_file_path = 'hypotheses-based-publications.csv'  # Path to the original output CSV file
    total_output_path = 'total_publisher_counts_no_date_filter.csv'  # Path for saving overall publisher counts
    per_hypothesis_output_path = 'publisher_counts_per_hypothesis.csv'  # Path for saving publisher counts per hypothesis
    count_publishers(output_file_path, total_output_path, per_hypothesis_output_path)


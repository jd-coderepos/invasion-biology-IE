import pandas as pd

def count_full_texts(output_file_path):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(output_file_path)
    
    # Fill NaN values in the 'full_text' column with an empty string
    df['full_text'] = df['full_text'].fillna('')
    
    # Group by 'hypothesis' and count non-empty 'full_text' entries
    result = df.groupby('hypothesis').apply(lambda x: (x['full_text'] != '').sum())
    
    # Print results
    print("Number of publications with full text available per hypothesis:")
    for hypothesis, count in result.items():
        print(f"{hypothesis}: {count}")

if __name__ == "__main__":
    output_file_path = 'hypotheses-based-publications-after-2010.csv'  # Path to the output CSV file
    count_full_texts(output_file_path)

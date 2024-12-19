import os
import json
import csv

def process_json_files(directory, output_csv):
    # Dictionary to store counts of (relationship name, type) combinations
    relationship_counts = {}
    unique_relationship_types = set()

    # Iterate through all files in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                try:
                    data = json.load(file)

                    # Extract relationships and count (name, type) combinations
                    relationships = data.get('relationships', [])
                    for relationship in relationships:
                        name = relationship['relationship_properties'].get('name', 'unknown')
                        rtype = relationship['relationship_properties'].get('type', 'unknown')

                        # Add the relationship type to the set of unique types
                        unique_relationship_types.add(rtype)

                        key = (name, rtype)
                        if key in relationship_counts:
                            relationship_counts[key] += 1
                        else:
                            relationship_counts[key] = 1

                except json.JSONDecodeError:
                    print(f"Error decoding JSON in file: {filename}")

    # Write the results to a CSV file
    with open(output_csv, 'w', encoding='utf-8', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        # Write header
        csvwriter.writerow(['Relationship Name', 'Type', 'Count'])

        # Write data
        for (name, rtype), count in relationship_counts.items():
            csvwriter.writerow([name, rtype, count])

    # Print all unique relationship types to the console
    print("Unique Relationship Types:")
    for rtype in sorted(unique_relationship_types):
        print(rtype)

if __name__ == "__main__":
    directory = input("Enter the directory containing JSON files: ").strip()
    output_csv = input("Enter the output CSV filename: ").strip()

    process_json_files(directory, output_csv)
    print(f"Counts of (relationship name, type) combinations have been written to {output_csv}")
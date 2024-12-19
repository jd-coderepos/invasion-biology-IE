import os
import json
import csv
from collections import Counter

def count_species_roles(directory_path, output_csv):
    species_counter = Counter()
    unique_roles = set()

    # Iterate through all JSON files in the directory
    for file_name in os.listdir(directory_path):
        if file_name.endswith('.json'):
            file_path = os.path.join(directory_path, file_name)
            
            # Read and parse the JSON file
            with open(file_path, 'r') as file:
                try:
                    data = json.load(file)
                    # Extract species name and role
                    if "species" in data:
                        for species in data["species"]:
                            species_name = species.get("name", "Unknown").lower()
                            role = species.get("properties", {}).get("role", "Unknown").lower()
                            unique_roles.add(role)
                            species_counter[(species_name, role)] += 1
                except json.JSONDecodeError:
                    print(f"Error reading JSON file: {file_name}")

    # Print unique roles to the console
    print("Unique roles:")
    for role in sorted(unique_roles):
        print(role)

    # Write the results to a CSV file
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Species Name", "Role", "Count"])
        for (species_name, role), count in species_counter.items():
            csv_writer.writerow([species_name, role, count])

if __name__ == "__main__":
    # Take input and output paths from the user
    directory_path = input("Enter the directory path containing JSON files: ").strip()
    output_csv = input("Enter the output CSV file path: ").strip()

    # Execute the counting function
    count_species_roles(directory_path, output_csv)
    print(f"Species-role counts have been written to {output_csv}")

import os
import json
import csv
from collections import Counter

# Take input directory and output CSV file path from the user
input_directory = input("Enter the path to the directory containing JSON files: ").strip()
output_csv_file = input("Enter the path for the output CSV file: ").strip()

# Counter for (ecosystem_name, type) tuples
ecosystem_counter = Counter()

# Iterate through all JSON files in the directory
for filename in os.listdir(input_directory):
    if filename.endswith(".json"):
        file_path = os.path.join(input_directory, filename)
        
        # Open and parse the JSON file
        with open(file_path, 'r', encoding='utf-8') as json_file:
            try:
                data = json.load(json_file)

                # Extract ecosystem data
                if "ecosystem" in data:
                    for ecosystem in data["ecosystem"]:
                        ecosystem_name = ecosystem.get("name", "Unknown")
                        ecosystem_type = ecosystem.get("properties", {}).get("type", "Unknown")

                        # Count the (ecosystem_name, type) tuple
                        ecosystem_counter[(ecosystem_name, ecosystem_type)] += 1
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON in file {filename}: {e}")

# Write the results to a CSV file
with open(output_csv_file, 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Ecosystem Name", "Type", "Count"])
    
    for (ecosystem_name, ecosystem_type), count in ecosystem_counter.items():
        writer.writerow([ecosystem_name, ecosystem_type, count])

print(f"Ecosystem counts have been written to {output_csv_file}")

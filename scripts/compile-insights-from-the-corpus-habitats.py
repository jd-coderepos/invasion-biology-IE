import os
import json
import csv

# Get input directory and output file from the user
input_directory = input("Enter the path to the directory containing JSON files: ").strip()
output_csv = input("Enter the name of the output CSV file (including .csv extension): ").strip()

# Dictionary to store counts of (habitat_name, type) combinations and ecosystem type
habitat_data = {}

# Iterate over JSON files in the directory
for filename in os.listdir(input_directory):
    if filename.endswith(".json"):
        file_path = os.path.join(input_directory, filename)
        
        with open(file_path, 'r', encoding='utf-8') as json_file:
            try:
                data = json.load(json_file)

                # Extract habitat information
                habitats = data.get("habitat", [])
                
                # Ensure habitats is a list
                if isinstance(habitats, list):
                    for habitat in habitats:
                        if isinstance(habitat, dict):
                            name = habitat.get("name", "unknown")
                            habitat_type = habitat.get("properties", {}).get("type", "unknown")
                            ecosystem_type = habitat.get("properties", {}).get("subcomponent_of", "unknown")

                            # Create the tuple
                            key = (name, habitat_type, ecosystem_type)

                            # Increment the count
                            if key in habitat_data:
                                habitat_data[key] += 1
                            else:
                                habitat_data[key] = 1

            except json.JSONDecodeError:
                print(f"Error decoding JSON in file: {filename}")

# Write the results to a CSV file
with open(output_csv, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)

    # Write header
    csv_writer.writerow(["Habitat Name", "Type", "Ecosystem Type", "Count"])

    # Write data
    for (habitat_name, habitat_type, ecosystem_type), count in habitat_data.items():
        csv_writer.writerow([habitat_name, habitat_type, ecosystem_type, count])

print(f"Counts of (habitat name, type, ecosystem type) combinations have been saved to {output_csv}")

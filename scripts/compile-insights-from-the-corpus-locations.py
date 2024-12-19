import os
import json
import csv
from collections import Counter

def count_location_tuples():
    # Get input directory and output file names from the user
    json_dir = input("Enter the directory containing JSON files: ").strip()
    output_csv = input("Enter the output CSV file name: ").strip()

    # Initialize a counter for (location_name, geopolitical_info) tuples
    location_counter = Counter()
    geopolitical_info_set = set()

    # Iterate through all JSON files in the directory
    for filename in os.listdir(json_dir):
        if filename.endswith('.json'):
            filepath = os.path.join(json_dir, filename)
            
            # Read the JSON file
            with open(filepath, 'r', encoding='utf-8') as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    print(f"Skipping invalid JSON file: {filename}")
                    continue

                # Extract location data and count the tuples
                if "location" in data:
                    for location in data["location"]:
                        location_name = location.get("name")
                        geopolitical_info = location.get("properties", {}).get("geopolitical_info")

                        if location_name and geopolitical_info:
                            location_counter[(location_name, geopolitical_info)] += 1
                            geopolitical_info_set.add(geopolitical_info)

    # Write the counts to a CSV file
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        writer.writerow(["Location Name", "Geopolitical Info", "Count"])

        for (location_name, geopolitical_info), count in location_counter.items():
            writer.writerow([location_name, geopolitical_info, count])

    # Print all unique Geopolitical Info tags
    print("Unique Geopolitical Info tags:")
    for tag in sorted(geopolitical_info_set):
        print(tag)

    print(f"Counts written to {output_csv}")

# Run the function
count_location_tuples()
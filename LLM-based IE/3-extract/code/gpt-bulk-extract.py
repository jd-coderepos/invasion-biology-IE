import os
import csv
import json
import re
from openai import OpenAI

def get_openai_api_key():
    """Prompt the user for the OpenAI API key."""
    return input("Enter your OpenAI API key: ").strip()

def get_file_locations():
    """Prompt the user for the input CSV file and output folder locations."""
    input_csv = input("Enter the path to the input CSV file: ").strip()
    output_folder = input("Enter the path to the output folder: ").strip()
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    return input_csv, output_folder

def sanitize_filename(filename):
    """Sanitize a file name to remove or replace invalid characters."""
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def get_processed_dois(output_folder):
    """Retrieve the list of already processed DOIs from the output folder."""
    processed_dois = set()
    for filename in os.listdir(output_folder):
        if filename.endswith(".json") or filename.endswith(".txt"):
            processed_doi = os.path.splitext(filename)[0]
            processed_dois.add(processed_doi)
    return processed_dois

def validate_extraction(cleaned_data):
    """Validate the extracted data against the schema."""
    try:
        json_data = json.loads(cleaned_data)
        required_keys = ["species", "location", "ecosystem", "habitat", "relationships"]
        
        # Check for missing keys in the schema
        missing_keys = [key for key in required_keys if key not in json_data]
        if missing_keys:
            print(f"Validation failed: Missing keys - {missing_keys}")
            return False

        return True
    except json.JSONDecodeError as e:
        print(f"Validation failed: JSON decode error - {e}")
        print(f"Raw extracted data: {cleaned_data}")
        return False
    except Exception as e:
        print(f"Validation failed: Unexpected error - {e}")
        print(f"Raw extracted data: {cleaned_data}")
        return False

def extract_information(client, title, abstract):
    """Extract information using OpenAI API."""
    system_instructions = """
	**Your role**
    You are a research assistant specializing in invasion biology or ecology. Your primary task is to read and analyze the content of provided papers to extract relevant information.

    The field of invasion biology is defined as follows: a research area focusing on the translocation, establishment, spread, impact, and management of species outside of their native ranges, where they are referred to as non-native or alien species.

    The information extraction task is centered on the following entities: species, habitat, location, and ecosystem.
	
	The entities are defined as:
    1. **Species**: This includes both specific, formally named species (e.g., *Asterias amurensis*) and broader categories of organisms relevant to the study (e.g., "demersal fish" or "aquatic invertebrates"). These may include plants, animals, fungi, or microbes that are translocated to new environments, where they establish, spread, and potentially cause ecological or economic impacts. The term may also encompass higher-level taxonomic groups or functional groups when specific species are not identified in the text.
    2. **Location**: The study site, which could range from a specific geographic feature (e.g., "Port Phillip Bay, southern Australia") to broader geopolitical regions (e.g., "southern Australia" or "the Amazon rainforest"). Locations may include natural features such as rivers, bays, or mountains, as well as administrative areas like cities, states, or countries.
    3. **Ecosystem**: A system comprising interacting biological and abiotic components. Ecosystems often extend beyond specific locations (e.g., the savannah ecosystem spans geopolitical boundaries such as Kenya and Tanzania).
    4. **Habitat**: A subcomponent of an ecosystem where a specific organism lives. For example, crocodiles inhabit freshwater habitats (e.g., rivers) within the broader savannah ecosystem.

	**Your tasks:**
	1. Upon receiving an article, identify and extract data according to the predefined schema specified below. Record values for each entity specified in the schema and relations between the extracted entities as well as their specified properties. If a property is not mentioned in the article, denote this with a "-".
    2. Note that not all papers that might be provided by the user are addressing a problem in invasion biology. If you are provided a paper input that is not an invasion biology paper, return N/A as your response.	

	**Extraction schema**
	{
	  "species": [
		{
		  "name": "species_name",
		  "properties": {
			"role": "native/introduced/alien/invasive",
			"taxonomy_level": "species/genus/family"
		  }
		}
	  ],
	  "location": [
		{
		  "name": "location_name",
		  "properties": {
			"category": "natural/administrative",
			"geopolitical_info": "country/region/city",
			"additional_details": "climatic/physiographic"
		  }
		}
	  ],
	  "ecosystem": [
		{
		  "name": "ecosystem_name",
		  "properties": {
			"type": "aquatic/terrestrial/marine",
			"scope": "local/regional/global"
		  }
		}
	  ],
	  "habitat": [
		{
		  "name": "habitat_name",
		  "properties": {
			"type": "aquatic/terrestrial/marine",
			"subcomponent_of": "ecosystem_name",
			"specifics": "e.g., benthic, litoral"
		  }
		}
	  ],
	  "relationships": [
		{
		  "related_entities": ["entity1", "entity2", "..."],
		  "relationship_properties": {
			"name": "relationship_name",
			"type": "biological/physical/ecological/anthropogenic",
			"directionality": "unidirectional/bidirectional",
			"context": "relationship_contextual_description"
		  }
		}
	  ]
	}	

	**Output Response Format:**
	1. Your response must always be in valid JSON format conforming to the specified schema.
	2. If the paper is not relevant to invasion biology, return:
      "N/A"
    """

    user_message = f"Extract the information as instructed from this article title and abstract.\n\nTitle: {title}\nAbstract: {abstract}"
    messages = [
        {"role": "system", "content": system_instructions},
        {"role": "user", "content": user_message},
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=1,
            max_tokens=2048,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        cleaned_data = response.choices[0].message.content.strip().removeprefix("```json").removesuffix("```").strip()
        return cleaned_data
    except Exception as e:
        print(f"An error occurred during extraction: {e}")
        return None

def process_csv(input_csv, output_folder, client):
    """Read the input CSV, process each row, and write output files."""
    csv.field_size_limit(10**7)
    processed_dois = get_processed_dois(output_folder)

    total_rows = 0
    skipped_rows = 0

    with open(input_csv, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        if not {'Title', 'Abstract', 'DOI'}.issubset(reader.fieldnames):
            print("Input CSV file must contain 'Title', 'Abstract', and 'DOI' headers.")
            return

        for row in reader:
            total_rows += 1
            doi = row.get("DOI", "").strip()

            if not doi:
                print(f"Row {total_rows} without a DOI detected. Ignoring this row entirely.")
                skipped_rows += 1
                continue

            doi_cleaned = sanitize_filename(doi.replace("/", "_"))
            if doi_cleaned in processed_dois:
                print(f"Skipping already processed DOI: {doi}")
                continue

            title = row.get("Title", "").strip()
            abstract = row.get("Abstract", "").strip()

            print(f"Processing row {total_rows}: DOI = {doi}")
            cleaned_data = extract_information(client, title, abstract)

            if cleaned_data is None:
                print(f"Skipping {doi} due to extraction error.")
                continue

            if "N/A" in cleaned_data and len(cleaned_data) < 10:
                print(f"Writing N/A response for {doi}.")
                na_file_path = os.path.join(output_folder, f"{doi_cleaned}.txt")
                with open(na_file_path, "w", encoding="utf-8") as na_file:
                    na_file.write("N/A\n")
            else:
                if validate_extraction(cleaned_data):
                    output_file_path = os.path.join(output_folder, f"{doi_cleaned}.json")
                    print(f"Writing extracted data for {doi}.")
                    with open(output_file_path, "w", encoding="utf-8") as json_file:
                        json.dump(json.loads(cleaned_data), json_file, indent=4)
                else:
                    print(f"Invalid data format for {doi}.")
    print(f"\nTotal rows processed: {total_rows}")
    print(f"Rows skipped due to missing DOI: {skipped_rows}")

if __name__ == "__main__":
    api_key = get_openai_api_key()
    client = OpenAI(api_key=api_key)
    input_csv, output_folder = get_file_locations()
    process_csv(input_csv, output_folder, client)

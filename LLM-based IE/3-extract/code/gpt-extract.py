import json
from openai import OpenAI

def get_openai_api_key():
    """Prompt the user for the OpenAI API key."""
    return input("Enter your OpenAI API key: ").strip()

def get_user_input():
    """Prompt the user for paper input type and content."""
    print("Choose the input type:")
    print("1. Title and Abstract")
    print("2. Full Text")
    print("Type 'exit' to quit the program.")
    input_type = input("Enter your choice (1, 2, or 'exit'): ").strip()

    if input_type == "1":
        title = input("Enter the paper title: ").strip()
        abstract = input("Enter the paper abstract: ").strip()
        return "title_abstract", title, abstract
    elif input_type == "2":
        full_text = input("Enter the full paper text: ").strip()
        return "full_text", full_text, None
    elif input_type.lower() == "exit":
        print("Exiting the program.")
        exit()
    else:
        print("Invalid choice. Please restart and select 1, 2, or 'exit'.")
        exit()

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

        # Additional validation can go here if needed
        return True

    except json.JSONDecodeError as e:
        print(f"Validation failed: JSON decode error - {e}")
        print(f"Raw extracted data: {cleaned_data}")  # Log raw response for debugging
        return False
    except Exception as e:
        print(f"Validation failed: Unexpected error - {e}")
        print(f"Raw extracted data: {cleaned_data}")
        return False

def extract_information(client, input_type, title=None, abstract=None, full_text=None):
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
    2. Note that not all papers that might be provided by the user are addressing a problem in invasion biology. If you are provided a paper input that is not an invasion biology paper, return "N/A" as your response.	

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
	2. If the paper is not relevant to invasion biology, return: "N/A"
    """

    if input_type == "title_abstract":
        user_message = f"Extract the information as instructed from this article title and abstract.\n\nTitle: {title}\nAbstract: {abstract}"
    elif input_type == "full_text":
        user_message = f"Extract the information as instructed from this full paper text.\n\n{full_text}"
    else:
        raise ValueError("Invalid input type.")

    messages = [
        {"role": "system", "content": system_instructions},
        {"role": "user", "content": user_message},
    ]

    try:
        # Query the model
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

        # Check for empty response
        if not cleaned_data:
            print("Extraction failed: Received an empty response from the model.")
            return

        # Validate the extracted data
        if "N/A" in cleaned_data and len(cleaned_data) < 10:
            print("\nThe paper is not relevant to invasion biology.")
            print("Model response:")
            print(cleaned_data)
        elif validate_extraction(cleaned_data):
            print("\nExtracted Data:")
            print(json.dumps(json.loads(cleaned_data), indent=4))
        else:
            print("Validation failed. See above logs for details.")

    except Exception as e:
        print(f"An error occurred during extraction: {e}")


if __name__ == "__main__":
    api_key = get_openai_api_key()
    client = OpenAI(api_key=api_key)
    
    while True:
        input_type, content1, content2 = get_user_input()

        if input_type == "title_abstract":
            extract_information(client, input_type, title=content1, abstract=content2)
        elif input_type == "full_text":
            extract_information(client, input_type, full_text=content1)

from openai import OpenAI

# Function to extract information
def extract_information(client, input_type, title=None, abstract=None, full_text=None):
    # System instructions
    system_instructions = """
    **Your role**
    You are a research assistant specializing in invasion biology or ecology. Your primary task is to read and analyze the content of provided papers to extract relevant information.

    The field of invasion biology is defined as follows: a research area focusing on the translocation, establishment, spread, impact, and management of species outside of their native ranges, where they are referred to as non-native or alien species.

    The information extraction task is centered on the following entities: species, habitat, location, and ecosystem.
    
    The entities are defined as:
    1. **Species**: This includes both specific, formally named species (e.g., *Asterias amurensis*) and broader categories of organisms relevant to the study (e.g., "demersal fish" or "aquatic invertebrates"). These may include plants, animals, fungi, or microbes that are translocated to new environments, where they establish, spread, and potentially cause ecological or economic impacts. The term may also encompass higher-level taxonomic groups or functional groups when specific species are not identified in the text. Note generic terms like "invasive species" is not considered a species name.
    2. **Location**: The study site, which could range from a specific geographic feature (e.g., "Port Phillip Bay, southern Australia") to broader geopolitical regions (e.g., "southern Australia" or "the Amazon rainforest"). Locations may include natural features such as rivers, bays, or mountains, as well as administrative areas like cities, states, or countries.
    3. **Ecosystem**: A system comprising interacting biological and abiotic components. Ecosystems often extend beyond specific locations (e.g., the savannah ecosystem spans geopolitical boundaries such as Kenya and Tanzania).
    4. **Habitat**: A subcomponent of an ecosystem where a specific organism lives. For example, crocodiles inhabit freshwater habitats (e.g., rivers) within the broader savannah ecosystem.

    **Your tasks:**
    1. Extract the terms for the four defined entities found in the provided paper text.
    2. Additionally, as part of the extraction task, you must determine whether any relationships exist between the extracted entity terms. If relationships are identified, extract the relevant information by specifying the related entity terms, and assign a name to each relationship. The name should clearly reflect the semantic nature of the interaction between the related entity terms, particularly within the context of invasion biology. Finally, for each identified relationship, provide the context from the paper text where it was found.
    3. Note that not all papers that might be provided by the user are addressing a problem in invasion biology. If you are provided a paper input that is not an invasion biology paper, return N/A as your response.    

    **Response Format:**
    1. Your response must always be in valid JSON format.
    2. If the paper is not relevant to invasion biology, return: "N/A"
    """

    # Construct user message based on input type
    if input_type == "title_abstract":
        user_message = f"Extract the information as instructed from this article title and abstract.\n\nTitle: {title}\nAbstract: {abstract}"
    elif input_type == "full_text":
        user_message = f"Extract the information as instructed from this full paper text.\n\n{full_text}"
    else:
        raise ValueError("Invalid input type. Choose 'title_abstract' or 'full_text'.")

    # Create messages for the query
    messages = [
        {"role": "system", "content": system_instructions},
        {"role": "user", "content": user_message},
    ]

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

    # Return the assistant's response
    return response.choices[0].message.content

# Main loop for user input
if __name__ == "__main__":
    print("Research Assistant for Invasion Biology")

    # Prompt user for API key
    api_key = input("Please enter your OpenAI API key: ").strip()
    if not api_key:
        print("API key is required to proceed.")
        exit()

    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)

    print("Type 'exit' to quit the session.")

    while True:
        print("\nChoose input type:")
        print("1. Title and Abstract")
        print("2. Full Paper Text")
        print("Type 'exit' to quit the program.")
        input_type = input("Enter your choice (1, 2, or 'exit'): ").strip()

        if input_type.lower() == "exit":
            print("Exiting the program. Goodbye!")
            break

        if input_type == "1":
            input_type = "title_abstract"
            title = input("Enter article title: ").strip()
            if title.lower() == "exit":
                print("Exiting the program. Goodbye!")
                break

            abstract = input("Enter article abstract: ").strip()
            if abstract.lower() == "exit":
                print("Exiting the program. Goodbye!")
                break

            try:
                # Extract information
                result = extract_information(client, input_type, title=title, abstract=abstract)
                print("\nExtracted Information:\n", result)
            except Exception as e:
                print("An error occurred while processing your request:", str(e))

        elif input_type == "2":
            input_type = "full_text"
            full_text = input("Enter full paper text: ").strip()
            if full_text.lower() == "exit":
                print("Exiting the program. Goodbye!")
                break

            try:
                # Extract information
                result = extract_information(client, input_type, full_text=full_text)
                print("\nExtracted Information:\n", result)
            except Exception as e:
                print("An error occurred while processing your request:", str(e))

        else:
            print("Invalid choice. Please enter 1, 2, or 'exit'.")

from openai import OpenAI

# Function to extract information
def extract_information(client, title, abstract):
    # System instructions
    system_instructions = """
    You are a research assistant in invasion biology or ecology. Your task is to read and analyze the content of provided papers to extract relevant information from the papers provided by the user.

    The field of invasion biology is defined as follows: a research area dealing with the translocation, establishment, spread, impact and management of species outside of their native ranges, where they are called non-native or alien species.

    The following entities define the information extraction objective: species, habitat, location, ecosystem.

    As the extraction task, you need to identify if there are any relations between the entities defined above, and if so extract the information with the relations.

    Respond in a valid JSON format.

    Note that not all papers that might be provided by the user are addressing a problem in invasion biology. If you are provided a paper input that is not an invasion biology paper, return N/A as your response.
    """

    # Create messages for the query
    messages = [
        {"role": "system", "content": system_instructions},
        {
            "role": "user",
            "content": f"Extract the information as instructed from this article title and abstract.\n\nTitle: {title}\nAbstract: {abstract}",
        },
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
        # Get title and abstract from user
        title = input("Enter article title (or type 'exit' to quit): ").strip()
        if title.lower() == "exit":
            break

        abstract = input("Enter article abstract: ").strip()
        if abstract.lower() == "exit":
            break

        try:
            # Extract information
            result = extract_information(client, title, abstract)
            print("\nExtracted Information:\n", result)
        except Exception as e:
            print("An error occurred while processing your request:", str(e))

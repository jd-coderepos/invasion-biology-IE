import os

def count_txt_files(directory_path):
    try:
        # Ensure the provided path exists and is a directory
        if not os.path.exists(directory_path):
            print(f"Error: The path '{directory_path}' does not exist.")
            return

        if not os.path.isdir(directory_path):
            print(f"Error: The path '{directory_path}' is not a directory.")
            return

        # Count .txt files in the directory
        txt_files = [f for f in os.listdir(directory_path) if f.endswith('.txt')]
        txt_count = len(txt_files)

        print(f"The directory '{directory_path}' contains {txt_count} .txt file(s).")
        return txt_count

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
directory_path = input("Enter the path to the directory: ")
count_txt_files(directory_path)

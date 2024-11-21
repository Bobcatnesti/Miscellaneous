import json

def remove_words_with_backslash(input_file, output_file):
    # Open and load the JSON file
    with open(input_file, 'r', encoding='utf-8') as file:
        banned_words = json.load(file)
    
    # Create a new list to store words that do not contain a backslash
    cleaned_words = [word for word in banned_words if '\\' not in word]

    # Save the cleaned list of words to a new JSON file
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(cleaned_words, file, indent=4)
    
    print(f"Cleaned words saved to {output_file}")

if __name__ == "__main__":
    input_file = "banned_words.json"  # Input JSON file with banned words
    output_file = "cleaned_banned_words.json"  # Output cleaned JSON file

    remove_words_with_backslash(input_file, output_file)

import requests
import json

# List of URLs to fetch the banned words from (duplicates removed)
urls = [
    'https://raw.githubusercontent.com/zacanger/profane-words/master/words.json',
    'https://raw.githubusercontent.com/etylermoss/swears/master/swears.txt',
    'https://raw.githubusercontent.com/dsojevic/profanity-list/main/en.txt',
    'https://raw.githubusercontent.com/tjackiw/obscenity/master/config/blacklist.yml',
    'https://raw.githubusercontent.com/chrisvfritz/language_filter/ea6677d35768f1729effe51bf159962617aed259/config/matchlists/mccormick.txt',
    'https://gist.githubusercontent.com/briankung/e085841a7a13fa4945a0cf482950436a/raw/326b4078db98541204e3d192d7cf84f63cd4c87a/bad_words.txt',
    'https://raw.githubusercontent.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/refs/heads/master/tr',
    'https://raw.githubusercontent.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/refs/heads/master/tlh',
    'https://raw.githubusercontent.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/refs/heads/master/th',
    'https://raw.githubusercontent.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/refs/heads/master/sv',
    'https://raw.githubusercontent.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/refs/heads/master/ru',
    'https://raw.githubusercontent.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/refs/heads/master/pt',
    'https://raw.githubusercontent.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/refs/heads/master/pl',
    'https://raw.githubusercontent.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/refs/heads/master/no',
    'https://raw.githubusercontent.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/refs/heads/master/nl',
    'https://raw.githubusercontent.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/refs/heads/master/ko',
    'https://raw.githubusercontent.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/refs/heads/master/kab',
    'https://raw.githubusercontent.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/refs/heads/master/ja',
    'https://raw.githubusercontent.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/refs/heads/master/it',
    'https://raw.githubusercontent.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/refs/heads/master/hu',
    'https://raw.githubusercontent.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/refs/heads/master/hi',
    'https://raw.githubusercontent.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/refs/heads/master/fr-CA-u-sd-caqc',
    'https://raw.githubusercontent.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/refs/heads/master/fr',
    'https://raw.githubusercontent.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/refs/heads/master/fil',
    'https://raw.githubusercontent.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/refs/heads/master/fi',
    'https://raw.githubusercontent.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/refs/heads/master/fa',
    'https://raw.githubusercontent.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/refs/heads/master/es',
    'https://raw.githubusercontent.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/refs/heads/master/eo',
    'https://raw.githubusercontent.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/refs/heads/master/en',
    'https://raw.githubusercontent.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/refs/heads/master/de',
    'https://raw.githubusercontent.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/refs/heads/master/da',
    'https://raw.githubusercontent.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/refs/heads/master/cs',
    'https://raw.githubusercontent.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/refs/heads/master/ar'
]

def fetch_and_process_urls(url_list):
    banned_words = set()  # Using a set to automatically handle duplicates
    word_sources = []  # To store words along with their sources

    # Remove duplicate URLs
    url_list = list(set(url_list))

    # Iterate through the list of URLs
    for url in url_list:
        try:
            # Send a GET request to fetch the data
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad responses
            print(f"Successfully fetched data from: {url}")

            # Check the content type and process accordingly
            if response.headers['Content-Type'] == 'application/json':
                # If it's JSON, we can directly process it
                data = response.json()
                for word in data:
                    # Clean the word: lowercase and remove escape characters
                    cleaned_word = word.lower().replace('\\"', '').replace('"', '')
                    banned_words.add(cleaned_word)  # Add to set
                    word_sources.append({'word': cleaned_word, 'source': url})  # Add word with source

            else:
                # If it's a text-based file (txt, yml, etc.), split by lines
                lines = response.text.splitlines()
                for line in lines:
                    # Clean up the line by removing unwanted symbols (e.g., "- " or extra spaces)
                    cleaned_line = line.strip().lower().lstrip("- ").replace('\\"', '').replace('"', '')
                    if cleaned_line:  # Ensure the line is not empty
                        banned_words.add(cleaned_line)
                        word_sources.append({'word': cleaned_line, 'source': url})  # Add word with source

        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch data from {url}: {e}")

    return list(banned_words), word_sources  # Return both sets

def save_to_json(data, filename="banned_words.json"):
    # Write the banned words to a JSON file
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    print(f"Saved cleaned banned words to {filename}")

def save_words_with_sources(data, filename="banned_words_with_sources.json"):
    # Write the banned words with their sources to a JSON file
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    print(f"Saved banned words with sources to {filename}")

if __name__ == "__main__":
    # Fetch and process all URLs
    banned_words, word_sources = fetch_and_process_urls(urls)
    
    # Save the cleaned banned words list to a JSON file (only words)
    save_to_json(banned_words, filename="banned_words.json")
    
    # Save the banned words with their sources to a different JSON file
    save_words_with_sources(word_sources, filename="banned_words_with_sources.json")

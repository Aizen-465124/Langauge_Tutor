import nltk
from nltk.corpus import wordnet as wn

# Download the necessary NLTK data 
nltk.download('wordnet')
nltk.download('omw-1.4')

def read_file(file_path):
    '''
    Reads the content of a file and returns it as a list of words.
    
    Args:
    - file_path (str): The path to the file to be read.
    
    Returns:
    - list: A list of words from the file, or None if an error occurs.
    '''
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            return content.split()
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
    except UnicodeDecodeError as e:
        print(f"An error occurred while decoding the file: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def get_translation(word, target_lang='spa'):
    '''
    Translates a word to the target language using WordNet.
    
    Args:
    - word (str): The word to be translated.
    - target_lang (str): The target language code (default is 'spa' for Spanish).
    
    Returns:
    - str: The translated word if found, otherwise the original word.
    '''
    try:
        synsets = wn.synsets(word)
        if not synsets:
            return word  # Return the original word if no translation is found
        synset = synsets[0]
        translations = synset.lemmas(target_lang)
        if translations:
            return translations[0].name()
        return word
    except Exception as e:
        print(f"An error occurred while translating the word '{word}': {e}")
        return word

def translate_every_fourth_word(content, target_lang='spa'):
    '''
    Translates every fourth word in a list of words to the target language.
    
    Args:
    - content (list): A list of words to be processed.
    - target_lang (str): The target language code (default is 'spa' for Spanish).
    
    Returns:
    - None: The function modifies the input list in place.
    '''
    try:
        for i in range(3, len(content), 4):  
            content[i] = get_translation(content[i].strip(",.!?").lower(), target_lang)
    except Exception as e:
        print(f"An error occurred while translating every fourth word: {e}")

# Example usage
file_path = 'sample.txt'
content = read_file(file_path)

'''
TARGET LANGUAGES
- French ('fra')
- Italian ('ita')
- Russian ('rus')
- Spanish ('spa')
''' 
if content:
    translate_every_fourth_word(content, 'spa')
    print("Russian Translation:", *content)

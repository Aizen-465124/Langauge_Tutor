import nltk
from nltk.corpus import wordnet as wn

# Download the necessary NLTK data 
# -> comment these {2 LINES } after running once, it just donwload langauge pack
nltk.download('wordnet')
nltk.download('omw-1.4')

def read_file(file_path):
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
    synsets = wn.synsets(word)
    if not synsets:
        return word  # Return the original word if no translation is found
    synset = synsets[0]
    translations = synset.lemmas(target_lang)
    if translations:
        return translations[0].name()
    return word

def translate_every_fourth_word(content):
    for i in range(3, len(content), 4):  
        content[i] = get_translation(content[i].strip(",.!?").lower())

# Example usage
file_path = 'sample.txt'
content = read_file(file_path)
# text = "I want to live in Europe where I fell in love with my wife."
translate_every_fourth_word(content)
print(*content)

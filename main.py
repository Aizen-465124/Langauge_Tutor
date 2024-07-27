from concurrent.futures import ThreadPoolExecutor, as_completed
from transformers import MarianMTModel, MarianTokenizer

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
    return []  # Return an empty list if there is an error

def translate_word(word, model, tokenizer):
    try:
        # Ensure the input is a string
        if not isinstance(word, str):
            raise ValueError("The word to be translated must be a string.")
        
        # Tokenize and translate the word
        inputs = tokenizer(word, return_tensors="pt", padding=True)
        translated = model.generate(**inputs)
        translated_word = tokenizer.decode(translated[0], skip_special_tokens=True)
        return translated_word
    except ValueError as ve:
        print(f"ValueError: {ve}")
    except Exception as e:
        print(f"An error occurred during translation: {e}")
    return word  # return the original word if translation fails

def translate_fourth_words(content, model, tokenizer):
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(translate_word, content[i], model, tokenizer): i for i in range(3, len(content), 4)}
        for future in as_completed(futures):
            idx = futures[future]
            try:
                content[idx] = future.result()
            except Exception as e:
                print(f"An error occurred while processing word at index {idx}: {e}")

def read_and_translate_file(file_path, target_lang='es'):
    """
    Reads a file, processes the content to extract every fourth word,
    and translates those words to the desired language (Spanish in this case).

    :param file_path: Path to the file to read.
    :return: The modified content with every fourth word translated, or an empty list if an error occurred.
    """
    content = read_file(file_path)
    if not content:
        return []

    try:
        # Initialize the translation model and tokenizer
        model_name = f"Helsinki-NLP/opus-mt-en-{target_lang}"
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)
    except Exception as e:
        print(f"An error occurred while loading the model or tokenizer: {e}")
        return []

    try:
        translate_fourth_words(content, model, tokenizer)
    except Exception as e:
        print(f"An error occurred during the translation process: {e}")

    return content

# Example usage
file_path = 'sample.txt'
'''
TARGET LANGUAGES
- French ('fr')
- Italian ('it')
- Russian ('ru')
- Spanish ('es')
'''
content = read_and_translate_file(file_path,"es")
if content:
    print(*content)

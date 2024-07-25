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

def translate_word(word, model, tokenizer):
    try:
        translated = model.generate(**tokenizer(word, return_tensors="pt", padding=True))
        translated_word = tokenizer.decode(translated[0], skip_special_tokens=True)
        return translated_word
    except Exception as e:
        print(f"An error occurred during translation: {e}")
        return word  # return the original word if translation fails

def translate_fourth_words(content, model, tokenizer):
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(translate_word, content[i], model, tokenizer): i for i in range(3, len(content), 4)}
        for future in as_completed(futures):
            idx = futures[future]
            content[idx] = future.result()

def read_and_translate_file(file_path):
    """
    Reads a file, processes the content to extract every fourth word,
    and translates those words to the desired language (Spanish in this case).

    :param file_path: Path to the file to read.
    :return: The modified content with every fourth word translated.
    """
    content = read_file(file_path)
    if content is None:
        return None

    # Initialize the translation model and tokenizer
    model_name = "Helsinki-NLP/opus-mt-en-es"
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    
    translate_fourth_words(content, model, tokenizer)
    
    return content

# Example usage
file_path = 'sample.txt'
content = read_and_translate_file(file_path)
if content:
    print(*content)
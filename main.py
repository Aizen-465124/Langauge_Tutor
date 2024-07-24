from transformers import MarianMTModel, MarianTokenizer

def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            return content
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

def read_and_translate_file(content):
    """
    Processes the content of a file, extracts every fourth word,
    and translates it to the desired language (Spanish in this case).

    :param content: The content of the file as a string.
    :return: The modified content with every fourth word translated.
    """
    
    # Initialize the translation model and tokenizer
    model_name = "Helsinki-NLP/opus-mt-en-es"
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    
    words = content.split()
    for i in range(3, len(words), 4):  # Start at the 4th word and step by 4
        words[i] = translate_word(words[i], model, tokenizer)
    
    return ' '.join(words)

# Example usage
file_path = 'sample.txt'
content = read_file(file_path)
if content:
    translated_content = read_and_translate_file(content)
    print(translated_content)

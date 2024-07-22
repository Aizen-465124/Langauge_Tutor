from transformers import MarianMTModel, MarianTokenizer

def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            # print(content)
            return content
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
    except UnicodeDecodeError as e:
        print(f"An error occurred while decoding the file: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def read_and_translate_file(content):
    """
    Processes the content of a file, extracts every fourth word,
    and translates it to the desired language (Spanish in this case).
    Please write out the requirements file as well

    :param content: The content of the file as a string.
    :return: translation
    """
    

    translation = ""

    try:
        # translate from English to Spanish
        model_name = "Helsinki-NLP/opus-mt-en-es"
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)
        translated_content = model.generate(**tokenizer(content, return_tensors="pt", padding=True))
        
        for t in translated_content:
            translation = tokenizer.decode(t, skip_special_tokens=True)

        return translation
    except Exception as e:
        print(f"An error occurred: {e}")


# Example usage
content = read_file('sample.txt')
tranlsation = read_and_translate_file(content)
print(tranlsation)
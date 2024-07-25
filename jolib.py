from joblib import Parallel, delayed
from transformers import MarianMTModel, MarianTokenizer
from time import time

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


def translate_word(word, model_name):
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    translated = model.generate(**tokenizer(word, return_tensors="pt", padding=True))
    return tokenizer.decode(translated[0], skip_special_tokens=True)

def read_and_translate_file(content, model_name):
    indices = range(3, len(content), 4) # get all indices
    translations = Parallel(n_jobs=-1)(delayed(translate_word)(content[i], model_name) for i in indices)
    # translations = Parallel(n_jobs=-1)(delayed(translate_word)(content[i], model_name) for i in range(3, len(content), 4))
    # print("Done")
    # print(translations)
    
    for idx, word in zip(indices, translations):
        content[idx] = word

# Example usage
start = time()
file_path = 'sample.txt'
content = read_file(file_path)
if content:
    model_name = "Helsinki-NLP/opus-mt-en-es"
    read_and_translate_file(content, model_name)
    print("DONE")
    # print(*content)

end = time()
print(f'Completion time {end-start}')
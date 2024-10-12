import logging
import os
import json
import ast
import backoff
import openai
import re
import numpy as np
import sys 

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

backoff_logger = logging.getLogger('backoff')
backoff_logger.setLevel(logging.INFO)
file_handler_backoff = logging.FileHandler('backoff_log.txt')
file_handler_backoff.setFormatter(formatter)
backoff_logger.addHandler(file_handler_backoff)

error_logger = logging.getLogger('errors')
error_logger.setLevel(logging.ERROR)
file_handler_errors = logging.FileHandler('errors.txt')
file_handler_errors.setFormatter(formatter)
error_logger.addHandler(file_handler_errors)

RED = '\033[91m'
MAGENTA = '\033[95m'
DARK_GRAY = '\033[90m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
DARK_GREEN = '\033[32m'
RESET = '\033[0m'  # Reset to default color

try:
    api_key = os.environ.get("OPENAI_API_KEY")
except Exception as e:
    print(f"Something unexpected happened with your API key: {e}")
    sys.exit()

client = openai.OpenAI(api_key= api_key)


@backoff.on_exception(backoff.expo, (openai.RateLimitError, openai.APIConnectionError, openai.Timeout), max_tries=20, logger=backoff_logger)
def get_completion_from_messages(messages, model="gpt-4-1106-preview", response_format = False, temperature=0):
    try:
        if not response_format:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature
            )
            return response.choices[0].message.content
        else:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                response_format={"type": "json_object"}
            )
            return response.choices[0].message.content

    except Exception as e:
        logging.error(f"Something unexpected happened. Error: {e}")
        raise

@backoff.on_exception(backoff.expo, (openai.RateLimitError, openai.APIConnectionError, openai.Timeout), max_tries=20, logger=backoff_logger)
def get_embedding(text, model="text-embedding-3-small"):
    text = text.replace("\n", " ")
    embeddings = client.embeddings.create(input = [text], model=model)
    return embeddings.data[0].embedding

def clean_up(text):
    numbered_list = re.findall(r'\d+\..*?(?=\n\s*\d+\.|\Z)', text, re.DOTALL)
    numbered_list = [re.sub(r'\n\s*', ' ', item.strip()) for item in numbered_list]
    return "\n".join(numbered_list)

def extract_numbers(input_string):
    pattern = re.compile(r'\d+')
    numbers = pattern.findall(input_string)
    return numbers

def xmile_name(display_name):
    return "_".join( display_name.split() )
 
def clean_symbol(symbol):
    return symbol.replace('(','').replace(')','')

def get_json(text):
    match = re.search(r'```json\n(.*?)```', text, re.DOTALL)
    if match:
        json_string = match.group(1)
        return load_json(json_string)
    else:
        if not text == "{}":
            return load_json(text)
        elif text == "{}":
            return None

def load_json(text):
    try:
        json_obj = json.loads(text)
        return json_obj
    except TypeError:
        unformatted_text = ast.literal_eval(text)
        unformatted_text["Step 6"]["steps"] = str(unformatted_text["Step 6"]["steps"])
        formatted_text = json.dumps(unformatted_text, indent=2)
        return json.loads(formatted_text)
    except Exception as e:
        print(f"Something unexpected happened! Exception: {e}. Text: {text}")

def cosine_similarity(vector_A, vector_B):
    dot_product = np.dot(vector_A, vector_B)
    magnitude_A = np.linalg.norm(vector_A)
    magnitude_B = np.linalg.norm(vector_B)

    if magnitude_A == 0 or magnitude_B == 0:
        raise ValueError("One or both input vectors have zero magnitude. Cosine similarity is undefined.")

    similarity = dot_product / (magnitude_A * magnitude_B)
    return similarity
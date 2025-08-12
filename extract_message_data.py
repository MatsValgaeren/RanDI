import os
from dotenv import load_dotenv
import json

load_dotenv()

messages_json_file = os.getenv('JSON_FILE')
extracted_file_name_combo = os.getenv('FILE_NAME_COMBO')
accepted_names = os.getenv('ACCEPTED_NAMES')

def output_json(data, name):
    json_str = json.dumps(data, indent=4)
    with open(name + ".json", "w") as f:
        f.write(json_str)

with open(messages_json_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

file_name_combo = {}
seen_authors = set()

for message in data['messages']:
    files = message['attachments']
    author = message['author']['name']
    for file in files:
        file_name = file['fileName']
        if author in accepted_names:
            seen_authors.add(author)
            file_name_combo[file_name] = author

output_json(file_name_combo, extracted_file_name_combo)



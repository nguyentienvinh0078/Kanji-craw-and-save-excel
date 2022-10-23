import json
import os

def json_write(json_file_path, json_data):
    with open(json_file_path, mode='w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, indent=4, separators=(',', ': '), ensure_ascii=False)

def json_read(json_file):
    resultData = {}
    with open(json_file, mode='r', encoding='utf-8') as json_file:
        resultData = json.load(json_file)
    return resultData
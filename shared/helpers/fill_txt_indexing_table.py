import collections
import json
import os

from shared.helpers.clean_text import clean_text


def save_txt_indexing_table(txt_indexing_table_path, indexing_table):
    with open(txt_indexing_table_path, 'w') as f:
        json.dump(indexing_table, f, indent=2)


def delete(txt_indexing_table_path, filename):
    with open(txt_indexing_table_path, 'r') as f:
        indexing_table = json.loads(f.read())

    for key in indexing_table:
        if indexing_table[key][filename]:
            indexing_table[key].pop(filename)

    save_txt_indexing_table(txt_indexing_table_path, indexing_table)


def process_txt(file_name, content_of_txt_file, indexing_table):
    content_of_txt_file_cleaned = clean_text(content_of_txt_file)
    for term in content_of_txt_file_cleaned.split(" "):
        if term in indexing_table:
            indexing_table[term].append(file_name)
        else:
            indexing_table[term] = [file_name]
    sorted_index = collections.OrderedDict(sorted(indexing_table.items()))
    return sorted_index


def compute_indexing_table(txt_documents_path: list, txt_indexing_table_path: str):
    indexing_table: dict = {}
    for file_path in txt_documents_path:
        if file_path.endswith(".txt"):
            with open(file_path, "r") as file:
                content = file.read()

                indexing_table = process_txt(file_path, content, indexing_table)

    save_txt_indexing_table(indexing_table=indexing_table, txt_indexing_table_path=txt_indexing_table_path)
    return {
        "status": "Success",
        "data": f"Checked {len(txt_documents_path)} files"
    }


def add_single_file_to_indexing_table(path_to_file: str, txt_indexing_table_path: str):
    # Open the JSON file and load its content into a dictionary
    with open(txt_indexing_table_path, 'r') as json_file:
        indexing_table = json.load(json_file)

    with open(path_to_file, "r") as file:
        content = file.read()

    indexing_table = process_txt(os.path.basename(path_to_file), content, indexing_table)

    save_txt_indexing_table(indexing_table=indexing_table, txt_indexing_table_path=txt_indexing_table_path)

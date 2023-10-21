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


def compute_indexing_table(txt_documents_path: str, txt_indexing_table_path: str):
    def process_txt(file_name, content_of_txt_file, indexing_table):
        content_of_txt_file_cleaned = clean_text(content_of_txt_file)
        for term in content_of_txt_file_cleaned.split(" "):
            if term in indexing_table:
                indexing_table[term].append(file_name)
            else:
                indexing_table[term] = [file_name]
        sorted_index = collections.OrderedDict(sorted(indexing_table.items()))
        return sorted_index

    indexing_table: dict = {}
    for file_name in os.listdir(txt_documents_path):
        if file_name.endswith(".txt"):
            with open(os.path.join(txt_documents_path, file_name), "r") as file:
                content = file.read()

                indexing_table = process_txt(file_name, content, indexing_table)

    save_txt_indexing_table(indexing_table=indexing_table, txt_indexing_table_path=txt_indexing_table_path)

import collections
import json
import os

from shared.helpers.clean_text import clean_text


def save_txt_indexing_table(txt_indexing_table_path, indexing_table):
    try:
        with open(txt_indexing_table_path, 'w') as f:
            json.dump(indexing_table, f, indent=2)
    except Exception as e:
        print(f"An error occurred while saving the indexing table: {e}")


def delete(txt_indexing_table_path, filename):
    try:
        with open(txt_indexing_table_path, 'r') as f:
            indexing_table = json.load(f)

        for key in indexing_table:
            if filename in indexing_table[key]:
                del indexing_table[key][filename]

        save_txt_indexing_table(txt_indexing_table_path, indexing_table)

    except FileNotFoundError:
        print(f"File '{txt_indexing_table_path}' not found.")
    except json.JSONDecodeError:
        print(f"Invalid JSON format in file '{txt_indexing_table_path}'.")
    except Exception as e:
        print(f"An error occurred: {e}")


def process_txt(file_name, content_of_txt_file, indexing_table):
    content_of_txt_file_cleaned = clean_text(content_of_txt_file)
    updated_indexing_table = indexing_table.copy()  # Make a copy to avoid modifying the original

    for term in content_of_txt_file_cleaned.split():
        if term in updated_indexing_table:
            if file_name not in updated_indexing_table[term]:
                updated_indexing_table[term].append(file_name)
        else:
            updated_indexing_table[term] = [file_name]

    sorted_index = collections.OrderedDict(sorted(updated_indexing_table.items()))
    return sorted_index


def compute_indexing_table(txt_documents_path: list, txt_indexing_table_path: str):
    indexing_table = {}
    processed_files = 0

    for file_path in txt_documents_path:
        if file_path.endswith(".txt"):
            try:
                with open(file_path, "r") as file:
                    content = file.read()
                    indexing_table = process_txt(file_path, content, indexing_table)
                    processed_files += 1
            except FileNotFoundError:
                print(f"File '{file_path}' not found.")
            except Exception as e:
                print(f"An error occurred while processing '{file_path}': {e}")

    save_txt_indexing_table(txt_indexing_table_path, indexing_table)
    return {
        "status": "Success",
        "data": f"Processed {processed_files} out of {len(txt_documents_path)} files"
    }


def add_single_file_to_indexing_table(path_to_file: str, txt_indexing_table_path: str):
    try:
        with open(txt_indexing_table_path, 'r') as json_file:
            indexing_table = json.load(json_file)

        with open(path_to_file, "r") as file:
            content = file.read()

        updated_indexing_table = process_txt(os.path.basename(path_to_file), content, indexing_table)

        save_txt_indexing_table(updated_indexing_table, txt_indexing_table_path)
        print(f"File '{os.path.basename(path_to_file)}' added to the indexing table.")

    except FileNotFoundError:
        print(f"File '{txt_indexing_table_path}' or '{path_to_file}' not found.")
    except json.JSONDecodeError:
        print(f"Invalid JSON format in file '{txt_indexing_table_path}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

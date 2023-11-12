import json
import os
import shutil
import time
import xml.etree.ElementTree as et

from fastapi import UploadFile

from domain.contracts.repositories.abstract_path_service import AbstractPathService
from domain.contracts.services.abstract_info_retrieval_service import AbstractInfoRetrievalService
from domain.contracts.services.abstract_vsm_service import AbstractVSMService
from shared.helpers.binary_search import binary_search
from shared.helpers.clean_text import clean_text
from shared.helpers.fill_txt_indexing_table import compute_indexing_table, add_single_file_to_indexing_table
from shared.helpers.knn_range_selector import knn_range_selector
from shared.helpers.text_to_xml_tree import preprocessing, transform_text_to_xml, find_term_context


class InfoRetrievalService(AbstractInfoRetrievalService):

    def __init__(self, path_service: AbstractPathService, vsm_service: AbstractVSMService):
        self.path_service = path_service
        self.vsm_service = vsm_service

    def search_between_txt_files_structured(self, query: str, name_query_file: str, indexing: bool, weight_strategy,
                                            similarity_strategy, nearest_neighbor: int, range_selector: float):
        start = time.time()
        similarity_results = {}
        query_cleaned = clean_text(query)

        root_element_of_tree_one, xml_version_of_text_one = transform_text_to_xml(query)
        path_xml_file_one = os.path.join(self.path_service.paths.xml_version_of_txt,
                                         name_query_file.replace(".txt", ".xml"))
        with open(path_xml_file_one, 'w') as file:
            file.write(str(xml_version_of_text_one))

        xml_version_of_text_one_processed = preprocessing(et.parse(path_xml_file_one).getroot())
        term_context_tree_one = find_term_context(xml_version_of_text_one_processed)

        if indexing:
            relevant_documents_paths = set()
            with open(self.path_service.paths.txt_indexing_table, 'r') as file:
                txt_indexing_table = json.load(file)

            # BinarySearch for each term of the query in the Indexing Table
            for word in query_cleaned.split():
                if binary_search(list(txt_indexing_table.keys()), word) is not None:
                    for document_path in txt_indexing_table[word]:
                        relevant_documents_paths.add(document_path)
                else:
                    print("Term not found")

            if not relevant_documents_paths:
                return None

            for relevant_document_path in relevant_documents_paths:
                with open(relevant_document_path, 'r') as file:
                    file_content = file.read()

                if "structured" in relevant_document_path:
                    similarity_results[
                        relevant_document_path] = self.vsm_service.compute_similarity_content_and_structure(
                        content_txt_one=query,
                        name_file_one=name_query_file,
                        content_txt_two=file_content,
                        name_file_two=os.path.basename(relevant_document_path),
                        weight_strategy=weight_strategy,
                        similarity_strategy=similarity_strategy)["similarity"]

                elif "flat" in relevant_document_path:
                    similarity_results[relevant_document_path] = self.vsm_service.compute_similarity_content_only(
                        content_txt_one=query,
                        content_txt_two=file_content,
                        weight_strategy=weight_strategy,
                        similarity_strategy=similarity_strategy)["similarity"]

            documents_selected = knn_range_selector(nearest_neighbor=nearest_neighbor, range_parameter=range_selector,
                                                    similarity_results=similarity_results)

            # Sort the dictionary by values in descending order
            sorted_dict = {k: v for k, v in sorted(documents_selected.items(), key=lambda item: item[1], reverse=True)}
            end = time.time()
            return {
                "similarity": sorted_dict,
                "time": end - start,
            }

        else:
            files_flat: list = [os.path.join(self.path_service.paths.data_input_txt_docs_flat, file_name) for file_name
                                in
                                os.listdir(self.path_service.paths.data_input_txt_docs_flat)]
            files_structured: list = [os.path.join(self.path_service.paths.data_input_txt_docs_structured, file_name)
                                      for
                                      file_name in os.listdir(self.path_service.paths.data_input_txt_docs_structured)]

            for flat_file_path in files_flat:
                with open(flat_file_path, 'r') as file:
                    file_content = file.read()

                try:
                    similarity = self.vsm_service.compute_similarity_content_only(content_txt_one=query,
                                                                                  content_txt_two=file_content,
                                                                                  weight_strategy=weight_strategy,
                                                                                  similarity_strategy=similarity_strategy)["similarity"]
                except Exception as e:
                    continue
                if similarity != 0:
                    similarity_results[os.path.join(flat_file_path)] = similarity

            for structured_file_path in files_structured:
                with open(structured_file_path, 'r') as file:
                    file_content = file.read()

                try:
                    similarity = self.vsm_service.compute_similarity_content_and_structure(content_txt_one=query,
                                                                                           name_file_one=name_query_file,
                                                                                           content_txt_two=file_content,
                                                                                           name_file_two=os.path.basename(
                                                                                               structured_file_path),
                                                                                           weight_strategy=weight_strategy,
                                                                                           similarity_strategy=similarity_strategy)["similarity"]
                except Exception as e:
                    continue
                if similarity != 0:
                    similarity_results[structured_file_path] = similarity

            documents_selected = knn_range_selector(nearest_neighbor=nearest_neighbor, range_parameter=range_selector,
                                                    similarity_results=similarity_results)

            # Sort the dictionary by values in descending order
            sorted_dict = {k: v for k, v in sorted(documents_selected.items(), key=lambda item: item[1], reverse=True)}
            end = time.time()
            return {
                "similarity": sorted_dict,
                "time": end - start,
            }

    def search_between_txt_files_flat(self, query: str, indexing: bool, weight_strategy, similarity_strategy,
                                      nearest_neighbor: int, range_selector: float):
        start = time.time()
        query_cleaned = clean_text(query)
        similarity_results = {}
        if indexing:
            relevant_documents_paths = set()
            with open(self.path_service.paths.txt_indexing_table, 'r') as file:
                txt_indexing_table = json.load(file)

            # BinarySearch for each term of the query in the Indexing Table
            for word in query_cleaned.split():
                if binary_search(list(txt_indexing_table.keys()), word) is not None:
                    for document_path in txt_indexing_table[word]:
                        relevant_documents_paths.add(document_path)
                else:
                    print("Term not found")

            if not relevant_documents_paths:
                return None
            for relevant_document_path in relevant_documents_paths:
                with open(relevant_document_path, 'r') as file:
                    file_content = file.read()

                similarity_results[relevant_document_path] = self.vsm_service.compute_similarity_content_only(
                    content_txt_one=query,
                    content_txt_two=file_content,
                    weight_strategy=weight_strategy,
                    similarity_strategy=similarity_strategy)[
                        "similarity"]

            documents_selected = knn_range_selector(nearest_neighbor=nearest_neighbor, range_parameter=range_selector,
                                                    similarity_results=similarity_results)

            # Sort the dictionary by values in descending order
            sorted_dict = {k: v for k, v in sorted(documents_selected.items(), key=lambda item: item[1], reverse=True)}
            end = time.time()
            return {
                "similarity": sorted_dict,
                "time": end - start,
            }

        else:
            files_flat = os.listdir(self.path_service.paths.data_input_txt_docs_flat)
            files_structured = os.listdir(self.path_service.paths.data_input_txt_docs_structured)

            for file_name in files_flat:
                with open(os.path.join(self.path_service.paths.data_input_txt_docs_flat, file_name), 'r') as file:
                    file_content = file.read()

                try:
                    similarity = self.vsm_service.compute_similarity_content_only(content_txt_one=query,
                                                                                  content_txt_two=file_content,
                                                                                  weight_strategy=weight_strategy,
                                                                                  similarity_strategy=similarity_strategy)[
                        "similarity"]
                except Exception as e:
                    continue
                if similarity != 0:
                    similarity_results[
                        os.path.join(self.path_service.paths.data_input_txt_docs_flat, file_name)] = similarity

            for file_name in files_structured:
                with open(os.path.join(self.path_service.paths.data_input_txt_docs_structured, file_name), 'r') as file:
                    file_content = file.read()

                try:
                    similarity = self.vsm_service.compute_similarity_content_only(content_txt_one=query,
                                                                                  content_txt_two=file_content,
                                                                                  weight_strategy=weight_strategy,
                                                                                  similarity_strategy=similarity_strategy)[
                        "similarity"]

                except Exception as e:
                    continue
                if similarity != 0:
                    similarity_results[
                        os.path.join(self.path_service.paths.data_input_txt_docs_structured, file_name)] = similarity

            documents_selected = knn_range_selector(nearest_neighbor=nearest_neighbor, range_parameter=range_selector,
                                                    similarity_results=similarity_results)

            # Sort the dictionary by values in descending order
            sorted_dict = {k: v for k, v in sorted(documents_selected.items(), key=lambda item: item[1], reverse=True)}
            end = time.time()
            return {
                "similarity": sorted_dict,
                "time": end - start,
            }

    def compute_txt_indexing_table(self):
        files_flat: list = [os.path.join(self.path_service.paths.data_input_txt_docs_flat, file_name) for file_name in
                            os.listdir(self.path_service.paths.data_input_txt_docs_flat)]
        files_structured: list = [os.path.join(self.path_service.paths.data_input_txt_docs_structured, file_name) for
                                  file_name in os.listdir(self.path_service.paths.data_input_txt_docs_structured)]
        compute_indexing_table(txt_indexing_table_path=self.path_service.paths.txt_indexing_table,
                               txt_documents_path=files_flat + files_structured)

    def add_file_to_txt_collection(self, file: UploadFile, with_indexing: bool = True):
        if file.filename in os.listdir(self.path_service.paths.data_input_txt_docs):
            print("file name matches a file name in our dataset")

        else:
            # Create a unique file path in the upload directory
            file_path = os.path.join(self.path_service.paths.data_input_txt_docs, file.filename)
            with open(file_path, "wb") as f:
                shutil.copyfileobj(file.file, f)

            if with_indexing:
                add_single_file_to_indexing_table(path_to_file=file_path,
                                                  txt_indexing_table_path=self.path_service.paths.txt_indexing_table)

    def get_txt_file(self, txt_file_name):
        # txt_file_path = os.path.join(self.path_service.paths.data_input_txt_docs, txt_file_name)
        if os.path.isfile(txt_file_name):
            return txt_file_name

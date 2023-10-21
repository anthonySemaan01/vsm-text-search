import json
import os

from fastapi import UploadFile

from domain.contracts.repositories.abstract_path_service import AbstractPathService
from domain.contracts.services.abstract_info_retrieval_service import AbstractInfoRetrievalService
from domain.contracts.services.abstract_vsm_service import AbstractVSMService
from shared.helpers.binary_search import binary_search
from shared.helpers.clean_text import clean_text
from shared.helpers.fill_txt_indexing_table import compute_indexing_table
from shared.helpers.knn_range_selector import knn_range_selector


class InfoRetrievalService(AbstractInfoRetrievalService):
    def __init__(self, path_service: AbstractPathService, vsm_service: AbstractVSMService):
        self.path_service = path_service
        self.vsm_service = vsm_service

    def search_between_txt_files(self, query: str, indexing: bool, weight_strategy, similarity_strategy,
                                 nearest_neighbor: int, range_selector: float):
        query_cleaned = clean_text(query)
        similarity_results = {}
        if indexing:
            relevant_documents_names = set()
            with open(self.path_service.paths.txt_indexing_table, 'r') as file:
                txt_indexing_table = json.load(file)

            # BinarySearch for each term of the query in the Indexing Table
            for word in query.split():
                if binary_search(list(txt_indexing_table.keys()), word) is not None:
                    for document_name in txt_indexing_table[word]:
                        relevant_documents_names.add(document_name)
                else:
                    print("Term not found")

            if not relevant_documents_names:
                return None
            for relevant_document_name in relevant_documents_names:
                with open(os.path.join(self.path_service.paths.data_input_txt_docs, relevant_document_name),
                          'r') as file:
                    file_content = file.read()

                similarity_results[relevant_document_name] = self.vsm_service.compute_similarity(
                    content_txt_one=query,
                    content_txt_two=file_content,
                    weight_strategy=weight_strategy,
                    similarity_strategy=similarity_strategy)

            print(similarity_results)
            documents_selected = knn_range_selector(nearest_neighbor=nearest_neighbor, range_parameter=range_selector,
                                                    similarity_results=similarity_results).keys()
            print(documents_selected)

            return documents_selected

        else:
            for file_name in os.listdir(self.path_service.paths.data_input_txt_docs):
                with open(os.path.join(self.path_service.paths.data_input_txt_docs, file_name), 'r') as file:
                    file_content = file.read()

                print(f"file content: {file_content}")
                try:
                    similarity = self.vsm_service.compute_similarity(content_txt_one=query, content_txt_two=file_content,
                                                                     weight_strategy=weight_strategy,
                                                                     similarity_strategy=similarity_strategy)
                except Exception as e:
                    continue
                if similarity != 0:
                    similarity_results[file_name] = similarity

            documents_selected = knn_range_selector(nearest_neighbor=nearest_neighbor, range_parameter=range_selector,
                                                    similarity_results=similarity_results).keys()

            return documents_selected

    def compute_txt_indexing_table(self):
        compute_indexing_table(txt_indexing_table_path=self.path_service.paths.txt_indexing_table,
                               txt_documents_path=self.path_service.paths.data_input_txt_docs)

    def add_file_to_txt_collection(self, file: UploadFile, with_indexing: bool = True):
        pass

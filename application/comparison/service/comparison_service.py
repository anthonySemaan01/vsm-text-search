import os

from domain.contracts.repositories.abstract_path_service import AbstractPathService
from domain.contracts.services.abstract_comparison_service import AbstractComparisonService
from domain.contracts.services.abstract_info_retrieval_service import AbstractInfoRetrievalService
from domain.contracts.services.abstract_vsm_service import AbstractVSMService
from domain.models.comparison_request import ComparisonRequest
from domain.models.search_request import SearchRequestFlat, SearchRequestStructure


class ComparisonService(AbstractComparisonService):
    def __init__(self, path_service: AbstractPathService, vsm_service: AbstractVSMService,
                 info_retrieval_service: AbstractInfoRetrievalService):
        self.path_service = path_service
        self.vsm_service = vsm_service
        self.info_retrieval_service = info_retrieval_service

    def compare_content_only(self, comparison_request: ComparisonRequest):
        content_txt_one = None
        content_txt_two = None

        with open(os.path.join(self.path_service.paths.uploaded_files,
                               comparison_request.content_to_compare.name_file_one), 'r') as file:
            content_txt_one = file.read()

        with open(os.path.join(self.path_service.paths.uploaded_files,
                               comparison_request.content_to_compare.name_file_two), 'r') as file:
            content_txt_two = file.read()
        return self.vsm_service.compute_similarity_content_only(
            content_txt_one=content_txt_one,
            content_txt_two=content_txt_two,
            weight_strategy=comparison_request.weight_strategy.value,
            similarity_strategy=comparison_request.similarity_strategy.value)

    def compare_content_and_structure(self, comparison_request: ComparisonRequest):
        content_txt_one = None
        content_txt_two = None

        with open(os.path.join(self.path_service.paths.uploaded_files,
                               comparison_request.content_to_compare.name_file_one), 'r') as file:
            content_txt_one = file.read()

        with open(os.path.join(self.path_service.paths.uploaded_files,
                               comparison_request.content_to_compare.name_file_two), 'r') as file:
            content_txt_two = file.read()
        return self.vsm_service.compute_similarity_content_and_structure(
            content_txt_one=content_txt_one,
            name_file_one=comparison_request.content_to_compare.name_file_one,
            content_txt_two=content_txt_two,
            name_file_two=comparison_request.content_to_compare.name_file_two,
            weight_strategy=comparison_request.weight_strategy.value,
            similarity_strategy=comparison_request.similarity_strategy.value)

    def search_between_txt_files_flat(self, search_request: SearchRequestFlat):
        return self.info_retrieval_service.search_between_txt_files_flat(query=search_request.query,
                                                                         range_selector=search_request.range_selector,
                                                                         nearest_neighbor=search_request.nearest_neighbor,
                                                                         weight_strategy=search_request.weight_strategy.value,
                                                                         similarity_strategy=search_request.similarity_strategy.value,
                                                                         indexing=search_request.indexing)

    def search_between_txt_files_structured(self, search_request: SearchRequestStructure):
        with open(os.path.join(self.path_service.paths.uploaded_files,
                               search_request.file_name), 'r') as file:
            content_txt_one = file.read()
        return self.info_retrieval_service.search_between_txt_files_structured(query=content_txt_one,
                                                                               name_query_file=search_request.file_name,
                                                                               range_selector=search_request.range_selector,
                                                                               nearest_neighbor=search_request.nearest_neighbor,
                                                                               weight_strategy=search_request.weight_strategy.value,
                                                                               similarity_strategy=search_request.similarity_strategy.value,
                                                                               indexing=search_request.indexing)

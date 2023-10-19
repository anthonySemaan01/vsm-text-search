from domain.contracts.repositories.abstract_path_service import AbstractPathService
from domain.contracts.services.abstract_comparison_service import AbstractComparisonService
from domain.contracts.services.abstract_info_retrieval_service import AbstractInfoRetrievalService
from domain.contracts.services.abstract_vsm_service import AbstractVSMService
from domain.models.comparison_request import ComparisonRequest
from domain.models.search_request import SearchRequest


class ComparisonService(AbstractComparisonService):
    def __init__(self, path_service: AbstractPathService, vsm_service: AbstractVSMService,
                 info_retrieval_service: AbstractInfoRetrievalService):
        self.path_service = path_service
        self.vsm_service = vsm_service
        self.info_retrieval_service = info_retrieval_service

    def compare(self, comparison_request: ComparisonRequest):
        return self.vsm_service.compute_similarity(
            content_txt_one=comparison_request.content_to_compare.content_txt_one,
            content_txt_two=comparison_request.content_to_compare.content_txt_two,
            weight_strategy=comparison_request.weight_strategy.value,
            similarity_strategy=comparison_request.similarity_strategy.value)

    def search_between_txt_files(self, search_request: SearchRequest):
        return self.info_retrieval_service.search_between_txt_files(query=search_request.query,
                                                                    range_selector=search_request.range_selector,
                                                                    nearest_neighbor=search_request.nearest_neighbor,
                                                                    weight_strategy=search_request.weight_strategy.value,
                                                                    similarity_strategy=search_request.similarity_strategy.value,
                                                                    indexing=search_request.indexing)

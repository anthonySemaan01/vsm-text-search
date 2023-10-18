from domain.contracts.repositories.abstract_path_service import AbstractPathService
from domain.contracts.services.abstract_comparison_service import AbstractComparisonService
from domain.contracts.services.abstract_vsm_service import AbstractVSMService
from domain.models.comparison_request import ComparisonRequest


class ComparisonService(AbstractComparisonService):
    def __init__(self, path_service: AbstractPathService, vsm_service: AbstractVSMService):
        self.path_service = path_service
        self.vsm_service = vsm_service

    def compare(self, comparison_request: ComparisonRequest):
        return self.vsm_service.compute_similarity(
            content_txt_one=comparison_request.content_to_compare.content_txt_one,
            content_txt_two=comparison_request.content_to_compare.content_txt_two,
            weight_strategy=comparison_request.weight_strategy.value,
            similarity_strategy=comparison_request.similarity_strategy.value)

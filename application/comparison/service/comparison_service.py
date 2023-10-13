from domain.contracts.repositories.abstract_path_service import AbstractPathService
from domain.contracts.services.abstract_comparison_service import AbstractComparisonService
from domain.models.comparison_request import ComparisonRequest


class ComparisonService(AbstractComparisonService):
    def __init__(self, path_service: AbstractPathService):
        self.path_service = path_service

    def compare(self, comparison_request: ComparisonRequest):
        return "Hello World"

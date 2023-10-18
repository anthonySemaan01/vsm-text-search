from domain.contracts.repositories.abstract_path_service import AbstractPathService
from domain.contracts.services.abstract_info_retrieval_service import AbstractInfoRetrievalService


class InfoRetrievalService(AbstractInfoRetrievalService):
    def __init__(self, path_service: AbstractPathService):
        self.path_service = path_service

    def search_between_txt_files(self, query: str, indexing: bool, weight_strategy, similarity_strategy):
        pass

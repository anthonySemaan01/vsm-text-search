from abc import abstractmethod, ABC, ABCMeta

from fastapi import UploadFile


class AbstractInfoRetrievalService(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def search_between_txt_files(self, query: str, indexing: bool, weight_strategy,
                                 similarity_strategy, nearest_neighbor: int,
                                 range_selector: float): raise NotImplementedError

    @abstractmethod
    def compute_txt_indexing_table(self): raise NotImplementedError

    @abstractmethod
    def add_file_to_txt_collection(self, file: UploadFile, with_indexing: bool = True): raise NotImplementedError

    @abstractmethod
    def get_txt_file(self, txt_file_name): raise NotImplementedError

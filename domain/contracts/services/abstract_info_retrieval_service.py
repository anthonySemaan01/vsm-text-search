from abc import abstractmethod, ABC, ABCMeta


class AbstractInfoRetrievalService(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def search_between_txt_files(self, query: str, indexing: bool, weight_strategy,
                                 similarity_strategy): raise NotImplementedError

from abc import abstractmethod, ABC, ABCMeta

from domain.models.comparison_request import ComparisonRequest
from domain.models.search_request import SearchRequest


class AbstractComparisonService(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def compare(self, comparison_request: ComparisonRequest): raise NotImplementedError

    @abstractmethod
    def search_between_txt_files(self, search_request: SearchRequest): raise NotImplementedError

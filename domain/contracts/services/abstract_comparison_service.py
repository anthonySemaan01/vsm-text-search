from abc import abstractmethod, ABC, ABCMeta

from domain.models.comparison_request import ComparisonRequest
from domain.models.search_request import SearchRequestStructure
from domain.models.search_request import SearchRequestFlat


class AbstractComparisonService(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def compare_content_only(self, comparison_request: ComparisonRequest): raise NotImplementedError

    @abstractmethod
    def compare_content_and_structure(self, comparison_request: ComparisonRequest): raise NotImplementedError

    @abstractmethod
    def search_between_txt_files_flat(self, search_request: SearchRequestFlat): raise NotImplementedError

    @abstractmethod
    def search_between_txt_files_structured(self, search_request: SearchRequestStructure): raise NotImplementedError

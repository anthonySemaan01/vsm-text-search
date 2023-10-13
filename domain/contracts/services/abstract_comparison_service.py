from abc import abstractmethod, ABC, ABCMeta

from domain.models.comparison_request import ComparisonRequest


class AbstractComparisonService(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def compare(self, comparison_request: ComparisonRequest): raise NotImplementedError

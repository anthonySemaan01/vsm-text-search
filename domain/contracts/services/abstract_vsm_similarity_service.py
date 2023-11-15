from abc import abstractmethod, ABC, ABCMeta
from typing import List


class AbstractVSMSimilarityService(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def compute_cosine_similarity(self, vector_a: List, vector_b: List) -> float: raise NotImplementedError

    @abstractmethod
    def compute_pcc_similarity(self, vector_a, vector_b) -> float: raise NotImplementedError

    @abstractmethod
    def compute_euclidean_similarity(self, vector_a, vector_b) -> float: raise NotImplementedError

    @abstractmethod
    def compute_manhattan_similarity(self, vector_a, vector_b) -> float: raise NotImplementedError

    @abstractmethod
    def compute_jaccard_similarity(self, vector_a, vector_b) -> float: raise NotImplementedError

    @abstractmethod
    def compute_dice_similarity(self, vector_a, vector_b) -> float: raise NotImplementedError

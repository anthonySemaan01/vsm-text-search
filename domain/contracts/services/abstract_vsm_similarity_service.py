from abc import abstractmethod, ABC, ABCMeta


class AbstractVSMSimilarityService(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def compute_cosine_similarity(self, vector_one, vector_two): raise NotImplementedError

    @abstractmethod
    def compute_pcc_similarity(self, vector_one, vector_two): raise NotImplementedError

    @abstractmethod
    def compute_euclidian_similarity(self, vector_one, vector_two): raise NotImplementedError

    @abstractmethod
    def compute_manhattan_similarity(self, vector_one, vector_two): raise NotImplementedError

    @abstractmethod
    def compute_jaccard_similarity(self, vector_one, vector_two): raise NotImplementedError

    @abstractmethod
    def compute_dice_similarity(self, vector_one, vector_two): raise NotImplementedError

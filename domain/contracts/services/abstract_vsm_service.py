from abc import abstractmethod, ABC, ABCMeta


class AbstractVSMService(ABC):
    __metaclass__ = ABCMeta


    @abstractmethod
    def compute_similarity(self, content_txt_one, content_txt_two, weight_strategy,
                           similarity_strategy): raise NotImplementedError

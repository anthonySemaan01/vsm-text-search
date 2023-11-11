from abc import abstractmethod, ABC, ABCMeta


class AbstractVSMService(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def compute_similarity_content_only(self, content_txt_one, content_txt_two, weight_strategy,
                                        similarity_strategy): raise NotImplementedError

    @abstractmethod
    def compute_similarity_content_and_structure(self, content_txt_one, name_file_one, content_txt_two, name_file_two,
                                                 weight_strategy,
                                                 similarity_strategy): raise NotImplementedError

from abc import abstractmethod, ABC, ABCMeta
from typing import List


class AbstractVSMWeightService(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def compute_tf_weight(self, content_txt_one, content_txt_two): raise NotImplementedError

    @abstractmethod
    def compute_idf_weight(self, term, documents_paths_list): raise NotImplementedError

    @abstractmethod
    def compute_tf_idf_weight(self, term, document_being_analyzed: str,
                              other_documents_list: List[str]): raise NotImplementedError

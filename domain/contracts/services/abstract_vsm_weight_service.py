from abc import abstractmethod, ABC, ABCMeta
from typing import List


class AbstractVSMWeightService(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def compute_tf_weight(self, content_txt_one, content_txt_two): raise NotImplementedError

    @abstractmethod
    def compute_tf_idf_weight_txt(self, term, document_being_analyzed: str,
                                  other_txt_documents_list: List[str]): raise NotImplementedError

    @abstractmethod
    def compute_tf_idf_weight_xml(self, term, xml_version_of_document_processed,
                                  other_xml_trees_list: List): raise

    @abstractmethod
    def compute_idf_weight_txt(self, term, other_txt_documents_list: List[str]): raise NotImplementedError

    @abstractmethod
    def compute_idf_weight_xml(self, term, other_xml_trees_list: List, approach: str = "TC"): raise NotImplementedError

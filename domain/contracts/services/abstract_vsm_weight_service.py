from abc import abstractmethod, ABC, ABCMeta
from typing import List, Tuple, Dict, Optional


class AbstractVSMWeightService(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def compute_tf_weight(self, content_text_one: Optional[str] = None, content_text_two: Optional[str] = None) -> \
            Tuple[Dict[str, int], Dict[str, int]]: raise NotImplementedError

    @abstractmethod
    def compute_tf_idf_weight_txt(self, term, document_being_analyzed: str,
                                  other_txt_documents_list: List[str]): raise NotImplementedError

    @abstractmethod
    def compute_tf_idf_weight_xml(self, term, xml_version_of_document_processed,
                                  other_xml_trees_list: List): raise

    @abstractmethod
    def compute_idf_weight_txt(self, term: str, other_txt_documents_list: List[str]) -> float: raise NotImplementedError

    @abstractmethod
    def compute_idf_weight_xml(self, term: str, other_xml_trees_list: List,
                               approach: str = "TC") -> float: raise NotImplementedError

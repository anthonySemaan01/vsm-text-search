import math
from collections import Counter
from typing import List, Optional, Dict, Tuple

from domain.contracts.repositories.abstract_path_service import AbstractPathService
from domain.contracts.services.abstract_vsm_weight_service import AbstractVSMWeightService
from shared.helpers.clean_text import clean_text
from shared.helpers.text_to_xml_tree import find_term_context


class VSMWeightService(AbstractVSMWeightService):

    def __init__(self, path_service: AbstractPathService):
        self.path_service = path_service

    def compute_tf_weight(self, content_text_one: Optional[str] = None, content_text_two: Optional[str] = None) -> \
            Tuple[
                Dict[str, int], Dict[str, int]]:
        term_frequency_one: Dict[str, int] = {}
        term_frequency_two: Dict[str, int] = {}

        if content_text_one:
            term_frequency_one = dict(Counter(content_text_one.split()))

        if content_text_two:
            term_frequency_two = dict(Counter(content_text_two.split()))

        return term_frequency_one, term_frequency_two

    def compute_idf_weight_txt(self, term: str, other_txt_documents_list: List[str]) -> float:
        term_occurrences = 0

        # Count how many documents contain the term
        for document in other_txt_documents_list:
            if term in clean_text(document).split():
                term_occurrences += 1

        # Calculate IDF using the formula
        idf = math.log((len(other_txt_documents_list) + 1) / (term_occurrences + 1), 10)
        return idf

    def compute_idf_weight_xml(self, term: str, other_xml_trees_list: List, approach: str = "TC") -> float:
        term_occurrences = 0

        # Count how many XML trees contain the term based on the selected approach
        for xml_tree in other_xml_trees_list:
            if term in find_term_context(xml_tree):
                term_occurrences += 1

        # Calculate IDF using the formula
        idf = math.log((len(other_xml_trees_list) + 1) / (term_occurrences + 1), 10)
        return idf

    def compute_tf_idf_weight_txt(self, term, document_being_analyzed: str, other_txt_documents_list: List[str]):
        tf_weights = self.compute_tf_weight(clean_text(document_being_analyzed))[0]
        return tf_weights[term] * self.compute_idf_weight_txt(term, other_txt_documents_list)

    def compute_tf_idf_weight_xml(self, term, xml_version_of_document_processed, other_xml_trees_list: List):
        tf_weights = self.compute_tf_weight(" ".join(find_term_context(tree=xml_version_of_document_processed)))[0]
        return tf_weights[term] * self.compute_idf_weight_xml(term, other_xml_trees_list)

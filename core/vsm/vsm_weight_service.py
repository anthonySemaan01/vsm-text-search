import math
from typing import List

from domain.contracts.repositories.abstract_path_service import AbstractPathService
from domain.contracts.services.abstract_vsm_weight_service import AbstractVSMWeightService
from shared.helpers.clean_text import clean_text
from shared.helpers.text_to_xml_tree import preprocessing, find_term_context, find_tag_based


class VSMWeightService(AbstractVSMWeightService):

    def __init__(self, path_service: AbstractPathService):
        self.path_service = path_service

    def compute_tf_weight(self, content_txt_one: str = None, content_txt_two: str = None):
        tf1 = {}
        tf2 = {}
        if content_txt_one is not None:
            for term in content_txt_one.split():
                if term in tf1:
                    tf1[term] += 1
                else:
                    tf1[term] = 1
        if content_txt_two is not None:
            for term in content_txt_two.split():
                if term in tf2:
                    tf2[term] += 1
                else:
                    tf2[term] = 1
        return tf1, tf2

    def compute_idf_weight_txt(self, term, other_txt_documents_list: List[str]):
        occurrences = 0
        for document in other_txt_documents_list:
            if term in clean_text(document).split():
                occurrences += 1

        return math.log((len(other_txt_documents_list) + 1) / occurrences, 10)

    def compute_idf_weight_xml(self, term, other_xml_trees_list: List, approach: str = "TC"):
        occurrences = 0
        for xml_tree in other_xml_trees_list:
            if approach == "TC":
                if term in find_term_context(xml_tree):
                    occurrences += 1
            else:
                if term in find_tag_based(xml_tree):  # Tag Based Approach (when dealing with query)
                    occurrences += 1

        return math.log((len(other_xml_trees_list) + 1) / occurrences, 10)

    def compute_tf_idf_weight_txt(self, term, document_being_analyzed: str, other_txt_documents_list: List[str]):
        tf_weights = self.compute_tf_weight(clean_text(document_being_analyzed))[0]
        return tf_weights[term] * self.compute_idf_weight_txt(term, other_txt_documents_list)

    def compute_tf_idf_weight_xml(self, term, xml_version_of_document_processed, other_xml_trees_list: List):
        tf_weights = self.compute_tf_weight(" ".join(find_term_context(tree=xml_version_of_document_processed)))[0]
        return tf_weights[term] * self.compute_idf_weight_xml(term, other_xml_trees_list)


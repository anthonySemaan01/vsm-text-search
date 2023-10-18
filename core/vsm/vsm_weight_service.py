import math
from typing import List

from domain.contracts.repositories.abstract_path_service import AbstractPathService
from domain.contracts.services.abstract_vsm_weight_service import AbstractVSMWeightService
from shared.helpers.clean_text import clean_text


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

    def compute_idf_weight(self, term, other_documents_list: List[str]):
        occurrences = 0
        for document in other_documents_list:
            if term in clean_text(document).split():
                occurrences += 1

        return math.log((len(other_documents_list) + 1) / occurrences, 10)

    def compute_tf_idf_weight(self, term, document_being_analyzed: str, other_documents_list: List[str]):
        tf_weights = self.compute_tf_weight(clean_text(document_being_analyzed))[0]
        return tf_weights[term] * self.compute_idf_weight(term, other_documents_list)

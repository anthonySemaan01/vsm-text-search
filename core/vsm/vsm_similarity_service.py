import math

from domain.contracts.repositories.abstract_path_service import AbstractPathService
from domain.contracts.services.abstract_vsm_similarity_service import AbstractVSMSimilarityService


class VSMSimilarityService(AbstractVSMSimilarityService):
    def __init__(self, path_service: AbstractPathService):
        self.path_service = path_service

    def compute_cosine_similarity(self, vector_one, vector_two):
        num = denom = denom1 = denom2 = 0
        for i in range(len(vector_one)):
            num += vector_one[i] * vector_two[i]
            denom1 += vector_one[i] ** 2
            denom2 += vector_two[i] ** 2
        denom = math.sqrt(denom1 * denom2)
        return float(num / denom)

    def compute_pcc_similarity(self, vector_one, vector_two):
        sum1 = sum(vector_one)
        sum2 = sum(vector_two)
        mean1 = sum1 / len(vector_one)
        mean2 = sum2 / len(vector_two)
        num = denom1 = denom2 = denom = 0
        for i in range(len(vector_one)):
            num += (vector_one[i] - mean1) * (vector_two[i] - mean2)
            denom1 += (vector_one[i] - mean1) ** 2
            denom2 += (vector_two[i] - mean2) ** 2
        denom = math.sqrt(denom1 * denom2)
        return num / denom

    def compute_euclidian_similarity(self, vector_one, vector_two):
        dist = 0
        for i in range(len(vector_one)):
            dist += (vector_one[i] - vector_two[i]) ** 2
        dist = math.sqrt(dist)
        return 1 / (1 + dist)

    def compute_manhattan_similarity(self, vector_one, vector_two):
        dist = 0
        for i in range(len(vector_one)):
            dist += abs(vector_one[i] - vector_two[i])
        return 1 / (1 + dist)

    def compute_jaccard_similarity(self, vector_one, vector_two):
        num = vector_one.intersection(vector_two)
        denom = vector_one.union(vector_two)
        return len(num) / len(denom)

    def compute_dice_similarity(self, vector_one, vector_two):
        num = 2 * (vector_one.intersection(vector_two))
        denom = (abs(vector_one) + abs(vector_two))
        return num / denom

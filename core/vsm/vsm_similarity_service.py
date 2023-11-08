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
        # Check if the lists have the same length
        if len(vector_one) != len(vector_two):
            raise ValueError("Lists must have the same length")

        n = len(vector_one)

        # Calculate the mean of each list
        mean1 = sum(vector_one) / n
        mean2 = sum(vector_two) / n

        # Calculate the covariance
        covariance = sum((vector_one[i] - mean1) * (vector_two[i] - mean2) for i in range(n))

        # Calculate the standard deviation of each list
        std_dev1 = math.sqrt(sum((vector_one[i] - mean1) ** 2 for i in range(n)))
        std_dev2 = math.sqrt(sum((vector_two[i] - mean2) ** 2 for i in range(n)))

        # Calculate the Pearson Correlation Coefficient
        if std_dev1 == 0 or std_dev2 == 0:
            return 0  # To avoid division by zero in case of constant lists
        else:
            pcc = covariance / (std_dev1 * std_dev2)
            return pcc

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
        set_one = set(vector_one)
        set_two = set(vector_two)
        intersection = len(set_one.intersection(set_two))
        union = len(set_one.union(set_two))
        return intersection / union

    def compute_dice_similarity(self, vector_one:list, vector_two:list):
            set_one = set(vector_one)
            set_two = set(vector_two)
            num = 2 * len(set_one.intersection(set_two))
            denom = len(set_one) + len(set_two)
            return num / denom

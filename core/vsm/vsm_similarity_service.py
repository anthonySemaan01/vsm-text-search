import math

import numpy as np
from typing import List

from domain.contracts.repositories.abstract_path_service import AbstractPathService
from domain.contracts.services.abstract_vsm_similarity_service import AbstractVSMSimilarityService


class VSMSimilarityService(AbstractVSMSimilarityService):

    def __init__(self, path_service: AbstractPathService):
        self.path_service = path_service

    def compute_cosine_similarity(self, vector_a: List, vector_b: List) -> float:
        dot_product = sum(a * b for a, b in zip(vector_a, vector_b))
        magnitude_a = math.sqrt(sum(a ** 2 for a in vector_a))
        magnitude_b = math.sqrt(sum(b ** 2 for b in vector_b))

        # Avoid division by zero
        if magnitude_a == 0 or magnitude_b == 0:
            return 0.0

        similarity = dot_product / (magnitude_a * magnitude_b)
        return similarity

    def compute_pcc_similarity(self, vector_a: List, vector_b: List) -> float:
        # Check if the lists have the same length
        if len(vector_a) != len(vector_b):
            raise ValueError("Lists must have the same length")

        n = len(vector_a)

        # Calculate the mean of each list
        mean_a = sum(vector_a) / n
        mean_b = sum(vector_b) / n

        # Calculate the covariance
        covariance = sum((vector_a[i] - mean_a) * (vector_b[i] - mean_b) for i in range(n))

        # Calculate the standard deviation of each list
        std_dev_a = math.sqrt(sum((vector_a[i] - mean_a) ** 2 for i in range(n)))
        std_dev_b = math.sqrt(sum((vector_b[i] - mean_b) ** 2 for i in range(n)))

        # Calculate the Pearson Correlation Coefficient
        if std_dev_a == 0 or std_dev_b == 0:
            return 0  # Avoid division by zero for constant lists
        else:
            pcc = covariance / (std_dev_a * std_dev_b)
            return pcc

    def compute_euclidean_similarity(self, vector_a: List, vector_b: List) -> float:
        if len(vector_a) != len(vector_b):
            raise ValueError("Vectors must have the same length")

        euclidean_distance = 0
        for i in range(len(vector_a)):
            euclidean_distance += (vector_a[i] - vector_b[i]) ** 2
        euclidean_distance = math.sqrt(euclidean_distance)

        # Avoid division by zero
        if euclidean_distance == 0:
            return 1.0  # If the vectors are identical, return maximum similarity

        similarity = 1 / (1 + euclidean_distance)
        return similarity

    def compute_manhattan_similarity(self, vector_a: List, vector_b: List) -> float:
        if len(vector_a) != len(vector_b):
            raise ValueError("Vectors must have the same length")

        manhattan_distance = sum(abs(a - b) for a, b in zip(vector_a, vector_b))

        # Avoid division by zero
        if manhattan_distance == 0:
            return 1.0  # If the vectors are identical, return maximum similarity

        similarity = 1 / (1 + manhattan_distance)
        return similarity

    def compute_jaccard_similarity(self, vector_a: List, vector_b: List) -> float:
        set_a = set(vector_a)
        set_b = set(vector_b)

        intersection_size = len(set_a.intersection(set_b))
        union_size = len(set_a.union(set_b))

        if union_size == 0:
            return 0.0  # Avoid division by zero for empty sets

        similarity = intersection_size / union_size
        return similarity

    def compute_dice_similarity(self, vector_a: List, vector_b: List) -> float:
        set_a = set(vector_a)
        set_b = set(vector_b)

        intersection_size = 2 * len(set_a.intersection(set_b))
        union_size = len(set_a) + len(set_b)

        if union_size == 0:
            return 0.0  # Avoid division by zero for empty sets

        dice_similarity = intersection_size / union_size
        return dice_similarity

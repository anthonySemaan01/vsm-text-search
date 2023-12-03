from pydantic import BaseModel
from domain.models.enums.weight_strategy import WeightStrategy
from domain.models.enums.similarity_strategy import SimilarityStrategy


class KMeansClusteringRequest(BaseModel):
    directory_name: str
    weight_strategy: WeightStrategy
    similarity_strategy: SimilarityStrategy
    number_of_clusters: int
    maximum_number_of_iterations: int

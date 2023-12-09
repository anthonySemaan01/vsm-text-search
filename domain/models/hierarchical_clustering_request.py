from pydantic import BaseModel

from domain.models.enums.similarity_strategy import SimilarityStrategy
from domain.models.enums.weight_strategy import WeightStrategy
from domain.models.enums.cluster_distance_strategy import ClusterDistanceStrategy


class HierarchicalClusteringRequest(BaseModel):
    directory_name: str
    weight_strategy: WeightStrategy
    similarity_strategy: SimilarityStrategy
    cluster_distance_strategy: ClusterDistanceStrategy
    number_of_clusters: int


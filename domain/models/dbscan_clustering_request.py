from pydantic import BaseModel

from domain.models.enums.similarity_strategy import SimilarityStrategy
from domain.models.enums.weight_strategy import WeightStrategy
from domain.models.enums.cluster_distance_strategy import ClusterDistanceStrategy


class DBScanClusteringRequest(BaseModel):
    directory_name: str
    min_samples: int
    eps: float
    weight_strategy: WeightStrategy
    similarity_strategy: SimilarityStrategy



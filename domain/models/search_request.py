from pydantic import BaseModel

from domain.models.enums.similarity_strategy import SimilarityStrategy
from domain.models.enums.weight_strategy import WeightStrategy


class SearchRequest(BaseModel):
    query: str
    indexing: bool
    weight_strategy: WeightStrategy
    similarity_strategy: SimilarityStrategy
    nearest_neighbor: int  # if 0 means all
    range_selector: float

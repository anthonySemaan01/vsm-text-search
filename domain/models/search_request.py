from pydantic import BaseModel

from domain.models.enums.similarity_strategy import SimilarityStrategy
from domain.models.enums.weight_strategy import WeightStrategy


class SearchRequestFlat(BaseModel):
    query: str
    indexing: bool
    weight_strategy: WeightStrategy
    similarity_strategy: SimilarityStrategy
    nearest_neighbor: int  # if 0 means all
    range_selector: float


class SearchRequestStructure(BaseModel):
    file_name: str
    indexing: bool
    weight_strategy: WeightStrategy
    similarity_strategy: SimilarityStrategy
    nearest_neighbor: int  # if 0 means all
    range_selector: float

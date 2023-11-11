from pydantic import BaseModel, validator
from domain.models.enums.weight_strategy import WeightStrategy
from domain.models.enums.similarity_strategy import SimilarityStrategy


class ContentToCompare(BaseModel):
    name_file_one: str
    name_file_two: str


class ComparisonRequest(BaseModel):
    content_to_compare: ContentToCompare
    weight_strategy: WeightStrategy
    similarity_strategy: SimilarityStrategy


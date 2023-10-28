from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from containers import Services
from domain.contracts.services.abstract_comparison_service import AbstractComparisonService
from domain.models.comparison_request import ComparisonRequest
from domain.models.search_request import SearchRequest

router = APIRouter()


@router.post("/compare")
@inject
def compare(comparison_request: ComparisonRequest,
            comparison_service: AbstractComparisonService = Depends(Provide[Services.comparison_service])):
    data = comparison_service.compare(comparison_request)
    return data


@router.post("/search")
@inject
def search_between_txt_files(search_request: SearchRequest,
                             comparison_service: AbstractComparisonService = Depends(
                                 Provide[Services.comparison_service])):
    return comparison_service.search_between_txt_files(search_request)

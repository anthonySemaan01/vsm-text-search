from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from containers import Services
from domain.contracts.services.abstract_comparison_service import AbstractComparisonService
from domain.models.comparison_request import ComparisonRequest
from domain.models.search_request import SearchRequestFlat, SearchRequestStructure

router = APIRouter()


@router.post("/compare_content_only")
@inject
def compare(comparison_request: ComparisonRequest,
            comparison_service: AbstractComparisonService = Depends(Provide[Services.comparison_service])):
    data = comparison_service.compare_content_only(comparison_request)
    return data


@router.post("/compare_content_and_structure")
@inject
def compare(comparison_request: ComparisonRequest,
            comparison_service: AbstractComparisonService = Depends(Provide[Services.comparison_service])):
    data = comparison_service.compare_content_and_structure(comparison_request)
    return data


@router.post("/search_flat")
@inject
def search_between_txt_files_flat(search_request: SearchRequestFlat,
                                  comparison_service: AbstractComparisonService = Depends(
                                      Provide[Services.comparison_service])):
    return comparison_service.search_between_txt_files_flat(search_request)


@router.post("/search_structured")
@inject
def search_between_txt_files_flat(search_request: SearchRequestStructure,
                                  comparison_service: AbstractComparisonService = Depends(
                                      Provide[Services.comparison_service])):
    return comparison_service.search_between_txt_files_structured(search_request=search_request)

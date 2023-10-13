"""
All endpoints for generation related functionalities.

The prefix endpoint is '/generate'
"""

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from containers import Services
from domain.contracts.services.abstract_comparison_service import AbstractComparisonService
from domain.models.comparison_request import ComparisonRequest

router = APIRouter()


@router.post("")
@inject
def compare(comparison_request: ComparisonRequest,
            comparison_service: AbstractComparisonService = Depends(Provide[Services.comparison_service])):
    data = comparison_service.compare(comparison_request)
    return data

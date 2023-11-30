from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from containers import Services
from domain.contracts.services.abstract_clustering_service import AbstractClusteringService
from domain.models.kmeans_clustering_request import KMeansClusteringRequest

router = APIRouter()


@router.post("/cluster_k_means")
@inject
def compare(kmeans_clustering_request: KMeansClusteringRequest,
            clustering_service: AbstractClusteringService = Depends(Provide[Services.comparison_service])):
    data = clustering_service.cluster_using_kmeans(kmeans_clustering_request)
    return data

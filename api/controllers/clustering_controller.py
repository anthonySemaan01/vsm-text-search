from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Response

from containers import Services
from domain.contracts.services.abstract_clustering_service import AbstractClusteringService
from domain.models.kmeans_clustering_request import KMeansClusteringRequest
from domain.models.hierarchical_clustering_request import HierarchicalClusteringRequest

router = APIRouter()


@router.post("/cluster_k_means")
@inject
def kmeans(kmeans_clustering_request: KMeansClusteringRequest,
           clustering_service: AbstractClusteringService = Depends(Provide[Services.clustering_service])):
    data = clustering_service.cluster_using_kmeans(kmeans_clustering_request)
    return data


@router.post("/cluster_hierarchical")
@inject
def hierarchical(hierarchical_clustering_request: HierarchicalClusteringRequest,
                 clustering_service: AbstractClusteringService = Depends(Provide[Services.clustering_service])):
    data = clustering_service.cluster_using_hierarchical(hierarchical_clustering_request)
    return data
    # return Response(content=data, media_type='image/png')

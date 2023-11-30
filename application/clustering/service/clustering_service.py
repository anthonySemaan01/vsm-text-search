from domain.contracts.repositories.abstract_path_service import AbstractPathService
from domain.contracts.services.abstract_clustering_service import AbstractClusteringService
from domain.models.kmeans_clustering_request import KMeansClusteringRequest


class ClusteringService(AbstractClusteringService):

    def __init__(self, path_service: AbstractPathService):
        self.path_service = path_service

    def cluster_using_kmeans(self, kmeans_clustering_request: KMeansClusteringRequest):
        pass

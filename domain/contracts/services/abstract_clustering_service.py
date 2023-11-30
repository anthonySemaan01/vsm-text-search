from abc import abstractmethod, ABC, ABCMeta
from domain.models.kmeans_clustering_request import KMeansClusteringRequest


class AbstractClusteringService(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def cluster_using_kmeans(self, kmeans_clustering_request: KMeansClusteringRequest): raise NotImplementedError


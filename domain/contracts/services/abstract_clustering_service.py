from abc import abstractmethod, ABC, ABCMeta
from domain.models.kmeans_clustering_request import KMeansClusteringRequest
from domain.models.hierarchical_clustering_request import HierarchicalClusteringRequest
from domain.models.dbscan_clustering_request import DBScanClusteringRequest


class AbstractClusteringService(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def cluster_using_kmeans(self, kmeans_clustering_request: KMeansClusteringRequest): raise NotImplementedError

    @abstractmethod
    def cluster_using_hierarchical(self,
                                   hierarchical_clustering_request: HierarchicalClusteringRequest): raise NotImplementedError

    @abstractmethod
    def cluster_using_dbscan(self, dbscan_clustering_request: DBScanClusteringRequest): raise NotImplementedError

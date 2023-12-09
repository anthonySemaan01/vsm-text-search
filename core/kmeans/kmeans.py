from typing import Dict, List


class Document:
    def __init__(self, document_path: str, document_vector: List):
        self.document_path = document_path
        self.document_vector = document_vector
        self.similarity_to_clusters: Dict[int, float] = {}


class Cluster:
    def __init__(self, cluster_id: int, centroid_coordinates: List):
        self.cluster_id: int = cluster_id
        self.centroid_coordinates: List = centroid_coordinates
        self.documents: List[Document] = []


class KMeans:
    def __init__(self, number_of_clusters, maximum_number_of_iterations):
        self.number_of_clusters = number_of_clusters
        self.maximum_number_of_iterations = maximum_number_of_iterations
        self.clusters: List[Cluster] = []
        self.documents: List[Document] = []

    def get_cluster_by_id(self, cluster_id: int):
        for cluster in self.clusters:
            if cluster.cluster_id == cluster_id:
                return cluster

    def get_document_by_path(self, document_path: str):
        for document in self.documents:
            if document.document_path == document_path:
                return document

    def get_the_cluster_of_a_doc(self, document_path: str):
        for cluster in self.clusters:
            document_paths = [document.document_path for document in cluster.documents]
            if document_path in document_paths:
                return cluster

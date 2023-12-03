import os
import time
import xml.etree.ElementTree as et

from core.kmeans.kmeans import KMeans, Cluster, Document
from domain.contracts.repositories.abstract_path_service import AbstractPathService
from domain.contracts.services.abstract_clustering_service import AbstractClusteringService
from domain.contracts.services.abstract_vsm_service import AbstractVSMService
from domain.contracts.services.abstract_vsm_similarity_service import AbstractVSMSimilarityService
from domain.contracts.services.abstract_vsm_weight_service import AbstractVSMWeightService
from domain.models.enums.similarity_strategy import SimilarityStrategy
from domain.models.enums.weight_strategy import WeightStrategy
from domain.models.kmeans_clustering_request import KMeansClusteringRequest
from shared.helpers.kmean_helpers import select_random_elements
from shared.helpers.text_to_xml_tree import transform_text_to_xml, preprocessing, find_term_context


class ClusteringService(AbstractClusteringService):

    def __init__(self, path_service: AbstractPathService, vsm_service: AbstractVSMService,
                 vsm_similarity_service: AbstractVSMSimilarityService, vsm_weight_service: AbstractVSMWeightService):
        self.path_service = path_service
        self.vsm_service = vsm_service
        self.vsm_similarity_service = vsm_similarity_service
        self.vsm_weight_service = vsm_weight_service

    def cluster_using_kmeans(self, kmeans_clustering_request: KMeansClusteringRequest):
        files_paths = [os.path.join(self.path_service.paths.data_input_txt_docs_structured, file_name) for file_name in
                       os.listdir(os.path.join(self.path_service.paths.data_input_txt_docs_structured,
                                               kmeans_clustering_request.directory_name))]

        dimensions = []
        xml_trees_processed = []
        weight_results = {}

        for file_path in files_paths:
            with open(file_path, 'r') as file:
                content_txt = file.read()

            # 1. transform text file into an xml document
            root_element_of_tree_one, xml_version_of_text_one = transform_text_to_xml(content_txt)

            path_xml_file = os.path.join(self.path_service.paths.xml_version_of_txt,
                                         os.path.basename(file_path).replace(".txt", ".xml"))

            with open(path_xml_file, 'w') as file:
                file.write(str(xml_version_of_text_one))

            # 2. preprocess the xml document
            xml_version_of_text_one_processed = preprocessing(et.parse(path_xml_file).getroot())
            xml_trees_processed.append(xml_version_of_text_one_processed)

            # 3. do term context for each
            term_context_tree = find_term_context(xml_version_of_text_one_processed)

            tf_weights, _ = self.vsm_weight_service.compute_tf_weight(content_text_one=" ".join(term_context_tree))

            dimensions = list(set(dimensions).union(set(tf_weights.keys())))

        start = time.time()

        for file_path in files_paths:
            vector = []
            with open(file_path, 'r') as file:
                content_txt = file.read()

            # 1. transform text file into an xml document
            root_element_of_tree_one, xml_version_of_text_one = transform_text_to_xml(content_txt)

            path_xml_file = os.path.join(self.path_service.paths.xml_version_of_txt,
                                         os.path.basename(file_path).replace(".txt", ".xml"))

            with open(path_xml_file, 'w') as file:
                file.write(str(xml_version_of_text_one))

            # 2. preprocess the xml document
            xml_version_of_text_one_processed = preprocessing(et.parse(path_xml_file).getroot())

            # 3. do term context for each
            term_context_tree_one = find_term_context(xml_version_of_text_one_processed)

            tf_weights, _ = self.vsm_weight_service.compute_tf_weight(
                content_text_one=" ".join(term_context_tree_one))

            # 4. compute weights
            if kmeans_clustering_request.weight_strategy.value == WeightStrategy.tf.value:
                for dimension in dimensions:
                    vector.append(tf_weights.get(dimension) or 0)

            elif kmeans_clustering_request.weight_strategy.value == WeightStrategy.tf_idf.value:
                for dimension in dimensions:
                    if dimension in tf_weights:
                        vector.append(self.vsm_weight_service.compute_tf_idf_weight_xml(
                            term=dimension,
                            xml_version_of_document_processed=xml_version_of_text_one_processed,
                            other_xml_trees_list=xml_trees_processed))
                    else:
                        vector.append(0.0)

            weight_results[file_path] = vector

        ################################################################################################
        #   START KMEANS LOGIC
        ################################################################################################

        kmeans = KMeans(number_of_clusters=kmeans_clustering_request.number_of_clusters,
                        maximum_number_of_iterations=kmeans_clustering_request.maximum_number_of_iterations)

        for document_path, weights in weight_results.items():
            kmeans.documents.append(Document(document_path=document_path, document_vector=weights))

        centroid_coordinates = select_random_elements(weight_results, kmeans_clustering_request.number_of_clusters)
        for cluster_id, centroid_coordinates in enumerate(centroid_coordinates):
            kmeans.clusters.append(Cluster(cluster_id=cluster_id, centroid_coordinates=centroid_coordinates))

        for document in kmeans.documents:
            max_similarity = None
            part_of_cluster = None

            for cluster in kmeans.clusters:
                if kmeans_clustering_request.similarity_strategy.value == SimilarityStrategy.euclidian.value:
                    similarity = self.vsm_similarity_service.compute_euclidean_similarity(cluster.centroid_coordinates,
                                                                                          document.document_vector)
                else:
                    similarity = self.vsm_similarity_service.compute_manhattan_similarity(cluster.centroid_coordinates,
                                                                                          document.document_vector)

                document.similarity_to_clusters[cluster.cluster_id] = similarity

            for cluster_id, similarity_to_cluster in document.similarity_to_clusters.items():

                if not max_similarity:
                    max_similarity = similarity_to_cluster
                    part_of_cluster = kmeans.get_cluster_by_id(cluster_id)
                else:
                    if similarity_to_cluster > max_similarity:
                        max_similarity = similarity_to_cluster
                        part_of_cluster = kmeans.get_cluster_by_id(cluster_id)

            part_of_cluster.documents.append(document)

        done = False
        while not done:
            print("iteration again")
            done = True

            # Updating the centroids coordinates of all clusters
            for cluster in kmeans.clusters:
                weights = []
                documents = cluster.documents

                if documents:
                    for document in documents:
                        weights.append(document.document_vector)
                        cluster.centroid_coordinates = list(map(lambda x: sum(x) / len(x), zip(*weights)))

            # Re-iterate over all the documents, and recompute the similarities
            for document in kmeans.documents:
                max_similarity = None
                part_of_cluster_in_previous_iteration = kmeans.get_the_cluster_of_a_doc(
                    document_path=document.document_path)
                part_of_cluster = None

                for cluster in kmeans.clusters:
                    if len(cluster.documents) != 0:
                        if kmeans_clustering_request.similarity_strategy.value == SimilarityStrategy.euclidian.value:
                            similarity = self.vsm_similarity_service.compute_euclidean_similarity(
                                cluster.centroid_coordinates,
                                document.document_vector)
                        else:
                            similarity = self.vsm_similarity_service.compute_manhattan_similarity(
                                cluster.centroid_coordinates,
                                document.document_vector)

                        document.similarity_to_clusters[cluster.cluster_id] = similarity

                max_similarity = None
                for cluster_id, similarity_to_cluster in document.similarity_to_clusters.items():
                    if not max_similarity:
                        max_similarity = similarity_to_cluster
                        part_of_cluster = kmeans.get_cluster_by_id(cluster_id)
                    else:
                        if similarity_to_cluster > max_similarity:
                            max_similarity = similarity_to_cluster
                            part_of_cluster = kmeans.get_cluster_by_id(cluster_id)

                if part_of_cluster is not part_of_cluster_in_previous_iteration:
                    part_of_cluster.documents.append(document)
                    part_of_cluster_in_previous_iteration.documents.remove(document)
                    done = False

        clusters_to_return = kmeans.clusters
        to_return = {}
        for cluster in clusters_to_return:
            to_return[cluster.cluster_id] = [document.document_path for document in cluster.documents]

        return to_return

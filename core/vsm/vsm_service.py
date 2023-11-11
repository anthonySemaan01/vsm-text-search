import os
import time
import xml.etree.ElementTree as et
import random

import pandas as pd

from domain.contracts.repositories.abstract_path_service import AbstractPathService
from domain.contracts.services.abstract_vsm_service import AbstractVSMService
from domain.contracts.services.abstract_vsm_similarity_service import AbstractVSMSimilarityService
from domain.contracts.services.abstract_vsm_weight_service import AbstractVSMWeightService
from domain.models.enums.similarity_strategy import SimilarityStrategy
from domain.models.enums.weight_strategy import WeightStrategy
from shared.helpers.clean_text import clean_text
from shared.helpers.text_to_xml_tree import transform_text_to_xml, preprocessing, find_term_context


class VSMService(AbstractVSMService):

    def __init__(self, path_service: AbstractPathService, vsm_weight_service: AbstractVSMWeightService,
                 vsm_similarity_service: AbstractVSMSimilarityService):
        self.path_service = path_service
        self.vsm_weight_service = vsm_weight_service
        self.vsm_similarity_service = vsm_similarity_service

    def compute_similarity_content_only(self, content_txt_one, content_txt_two, weight_strategy, similarity_strategy):
        start = time.time()
        vector1 = []
        vector2 = []
        content_txt_one_cleaned = clean_text(content_txt_one)
        content_txt_two_cleaned = clean_text(content_txt_two)

        tf_weights_one, tf_weights_two = self.vsm_weight_service.compute_tf_weight(
            content_txt_one=content_txt_one_cleaned,
            content_txt_two=content_txt_two_cleaned)

        # dimensions are the words found in both text 1 and 2 after cleaning
        dimensions = tf_weights_one.keys() | tf_weights_two.keys()

        if weight_strategy == WeightStrategy.tf.value:
            print(True)
            for dimension in dimensions:
                vector1.append(tf_weights_one.get(dimension) or 0)
                vector2.append(tf_weights_two.get(dimension) or 0)

        elif weight_strategy == WeightStrategy.tf_idf.value:
            for dimension in dimensions:
                if dimension in tf_weights_one:
                    vector1.append(self.vsm_weight_service.compute_tf_idf_weight_txt(dimension, content_txt_one,
                                                                                     [content_txt_one,
                                                                                      content_txt_two]))
                else:
                    vector1.append(0.0)

                if dimension in tf_weights_two:
                    vector2.append(self.vsm_weight_service.compute_tf_idf_weight_txt(dimension, content_txt_two,
                                                                                     [content_txt_one,
                                                                                      content_txt_two]))
                else:
                    vector2.append(0.0)

        df = pd.DataFrame(list(zip(vector1, vector2)), index=list(dimensions), columns=['Vector1', 'Vector2'])
        print(f"Original DataFrame :{df}")
        df.to_csv(os.path.join(self.path_service.paths.csvs, f"content_only{random.randint(100, 999)}.csv"), index=True)

        if similarity_strategy == SimilarityStrategy.cosine.value:
            similarity = self.vsm_similarity_service.compute_cosine_similarity(vector1, vector2)
        elif similarity_strategy == SimilarityStrategy.pcc.value:
            similarity = self.vsm_similarity_service.compute_pcc_similarity(vector1, vector2)
        elif similarity_strategy == SimilarityStrategy.euclidian.value:
            similarity = self.vsm_similarity_service.compute_euclidian_similarity(vector1, vector2)
        elif similarity_strategy == SimilarityStrategy.manhattan.value:
            similarity = self.vsm_similarity_service.compute_manhattan_similarity(vector1, vector2)
        elif similarity_strategy == SimilarityStrategy.jaccard.value:
            similarity = self.vsm_similarity_service.compute_jaccard_similarity(vector1, vector2)
        else:
            similarity = self.vsm_similarity_service.compute_dice_similarity(vector1, vector2)

        end = time.time()

        return {
            "similarity": similarity,
            "time": end - start,
            "dataframe":  df.to_json(orient='columns')
        }

    def compute_similarity_content_and_structure(self, content_txt_one, name_file_one, content_txt_two, name_file_two,
                                                 weight_strategy, similarity_strategy):
        start = time.time()
        vector1 = []
        vector2 = []

        # 1. transform text file into an xml document
        root_element_of_tree_one, xml_version_of_text_one = transform_text_to_xml(content_txt_one)
        root_element_of_tree_two, xml_version_of_text_two = transform_text_to_xml(content_txt_two)
        print(xml_version_of_text_two)

        path_xml_file_one = os.path.join(self.path_service.paths.xml_version_of_txt,
                                         name_file_one.replace(".txt", ".xml"))
        path_xml_file_two = os.path.join(self.path_service.paths.xml_version_of_txt,
                                         name_file_two.replace(".txt", ".xml"))
        with open(path_xml_file_one, 'w') as file:
            file.write(str(xml_version_of_text_one))
        with open(path_xml_file_two, 'w') as file:
            file.write(str(xml_version_of_text_two))

        # 2. preprocess the xml document
        xml_version_of_text_one_processed = preprocessing(et.parse(path_xml_file_one).getroot())
        print(type(xml_version_of_text_one_processed))
        xml_version_of_text_two_processed = preprocessing(et.parse(path_xml_file_two).getroot())

        # 3. do term context for each
        term_context_tree_one = find_term_context(xml_version_of_text_one_processed)
        term_context_tree_two = find_term_context(xml_version_of_text_two_processed)

        tf_weights_one, tf_weights_two = self.vsm_weight_service.compute_tf_weight(
            content_txt_one=" ".join(term_context_tree_one),
            content_txt_two=" ".join(term_context_tree_two))

        dimensions = list(tf_weights_one.keys() | tf_weights_two.keys())

        # 4. compute weights
        if weight_strategy == WeightStrategy.tf.value:
            print(True)
            for dimension in dimensions:
                vector1.append(tf_weights_one.get(dimension) or 0)
                vector2.append(tf_weights_two.get(dimension) or 0)

        elif weight_strategy == WeightStrategy.tf_idf.value:
            for dimension in dimensions:
                if dimension in tf_weights_one:
                    vector1.append(self.vsm_weight_service.compute_tf_idf_weight_xml(term=dimension,
                                                                                     xml_version_of_document_processed=xml_version_of_text_one_processed,
                                                                                     other_xml_trees_list=[
                                                                                         xml_version_of_text_one_processed,
                                                                                         xml_version_of_text_two_processed]))
                else:
                    vector1.append(0.0)

                if dimension in tf_weights_two:
                    vector2.append(self.vsm_weight_service.compute_tf_idf_weight_xml(term=dimension,
                                                                                     xml_version_of_document_processed=xml_version_of_text_two_processed,
                                                                                     other_xml_trees_list=[
                                                                                         xml_version_of_text_one_processed,
                                                                                         xml_version_of_text_two_processed]))
                else:
                    vector2.append(0.0)

        df = pd.DataFrame(list(zip(vector1, vector2)), index=list(dimensions),
                          columns=['Vector1', 'Vector2'])
        print(f"Original DataFrame :{df}")
        # Write the DataFrame to a CSV file
        df.to_csv(os.path.join(self.path_service.paths.csvs, f"{name_file_one}{name_file_two}.csv"), index=True)

        # 5. compute similarity
        if similarity_strategy == SimilarityStrategy.cosine.value:
            similarity = self.vsm_similarity_service.compute_cosine_similarity(vector1, vector2)
        elif similarity_strategy == SimilarityStrategy.pcc.value:
            similarity = self.vsm_similarity_service.compute_pcc_similarity(vector1, vector2)
        elif similarity_strategy == SimilarityStrategy.euclidian.value:
            similarity = self.vsm_similarity_service.compute_euclidian_similarity(vector1, vector2)
        elif similarity_strategy == SimilarityStrategy.manhattan.value:
            similarity = self.vsm_similarity_service.compute_manhattan_similarity(vector1, vector2)
        elif similarity_strategy == SimilarityStrategy.jaccard.value:
            similarity = self.vsm_similarity_service.compute_jaccard_similarity(vector1, vector2)
        else:
            similarity = self.vsm_similarity_service.compute_dice_similarity(vector1, vector2)

        end = time.time()

        return {
            "similarity": similarity,
            "time": end - start,
            "dataframe":  df.to_json(orient='columns')
        }

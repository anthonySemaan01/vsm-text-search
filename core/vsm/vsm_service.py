import pandas as pd

from domain.contracts.repositories.abstract_path_service import AbstractPathService
from domain.contracts.services.abstract_vsm_service import AbstractVSMService
from domain.contracts.services.abstract_vsm_similarity_service import AbstractVSMSimilarityService
from domain.contracts.services.abstract_vsm_weight_service import AbstractVSMWeightService
from domain.models.enums.similarity_strategy import SimilarityStrategy
from domain.models.enums.weight_strategy import WeightStrategy
from shared.helpers.clean_text import clean_text


class VSMService(AbstractVSMService):

    def __init__(self, path_service: AbstractPathService, vsm_weight_service: AbstractVSMWeightService,
                 vsm_similarity_service: AbstractVSMSimilarityService):
        self.path_service = path_service
        self.vsm_weight_service = vsm_weight_service
        self.vsm_similarity_service = vsm_similarity_service

    def compute_similarity_content_only(self, content_txt_one, content_txt_two, weight_strategy, similarity_strategy):
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
                    vector1.append(self.vsm_weight_service.compute_tf_idf_weight(dimension, content_txt_one,
                                                                                 [content_txt_one, content_txt_two]))
                else:
                    vector1.append(0.0)

                if dimension in tf_weights_two:
                    vector2.append(self.vsm_weight_service.compute_tf_idf_weight(dimension, content_txt_two,
                                                                                 [content_txt_one, content_txt_two]))
                else:
                    vector2.append(0.0)

        df = pd.DataFrame(list(zip(vector1, vector2)), index=list(dimensions), columns=['Vector1', 'Vector2'])
        print(f"Original DataFrame :{df}")

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

        return similarity

    def compute_similarity_content_and_structure(self, content_txt_one, content_txt_two, weight_strategy,
                                                 similarity_strategy):
        # TODO
        # 1. transform text file into an xml document
        # 2. preprocess the xml document
        # 3. do term context for each
        # 4. compute weights
        # 5. compute similarity

        return "Hello"
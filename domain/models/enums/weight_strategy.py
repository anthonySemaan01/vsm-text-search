from enum import Enum


class WeightStrategy(Enum):
    tf = "TF"
    idf = "IDF"
    tf_idf = "TF-IDF"

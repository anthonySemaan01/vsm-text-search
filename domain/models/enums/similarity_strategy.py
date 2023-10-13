from enum import Enum


class SimilarityStrategy(Enum):
    cosine = "cosine"
    pcc = "PCC"
    euclidian = "euclidian"
    manhattan = "manhattan"
    jaccard = "jaccard"
    dice = "dice"

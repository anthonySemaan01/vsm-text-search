from enum import Enum


class ClusterDistanceStrategy(Enum):
    single = "single"
    complete = "complete"
    average = "average"
    ward = "ward"

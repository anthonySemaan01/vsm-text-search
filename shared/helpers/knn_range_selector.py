def knn_operator(nearest_neighbor: int, similarity_results: dict):
    sorted_similarity_results = sorted(similarity_results.items(), key=lambda item: item[1], reverse=True)
    neighbors = dict(sorted_similarity_results[:nearest_neighbor])
    return neighbors


def knn_range_selector(nearest_neighbor: int, similarity_results: dict, range_parameter: float = 0):
    if range_parameter > 0:
        filtered_results = {key: value for key, value in similarity_results.items() if value >= range_parameter}
        return knn_operator(nearest_neighbor, filtered_results)
    else:
        return knn_operator(nearest_neighbor, similarity_results)

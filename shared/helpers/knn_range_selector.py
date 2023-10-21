def knn_operator(nearest_neighbor: int, similarity_results: dict):
    sorted_similarity_results = {k: v for k, v in
                                 sorted(similarity_results.items(), key=lambda item: item[1], reverse=True)}
    neighbors = dict(list(sorted_similarity_results.items())[0:nearest_neighbor])
    return neighbors


def range_operator(range_parameter: float, similarity_results: dict):
    # if sim >= e add term to neighbors
    sorted_similarity_results = {k: v for k, v in
                                 sorted(similarity_results.items(), key=lambda item: item[1], reverse=True)}
    in_range = {}
    for k, v in sorted_similarity_results.items():
        if v >= range_parameter:
            in_range[k] = v
        else:
            break
    return in_range


def knn_range_selector(nearest_neighbor: int, range_parameter: float, similarity_results: dict):
    return knn_operator(nearest_neighbor, range_operator(range_parameter, similarity_results))

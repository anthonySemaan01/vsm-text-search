def knn_operator(nearest_neighbor: int, similarity_results: dict):
    sorted_similarity_results = sorted(similarity_results.items(), key=lambda item: item[1], reverse=True)
    neighbors = dict(sorted_similarity_results[:nearest_neighbor])
    return neighbors



def range_operator(range_parameter: float, similarity_results: dict):
    print(similarity_results)
    print(range_parameter)
    # if sim >= e add term to neighbors
    sorted_similarity_results = sorted(similarity_results.items(), key=lambda item: item[1], reverse=True)

    in_range = {}

    for k, v in sorted_similarity_results:
        if v >= range_parameter:
            in_range[k] = v
        else:
            break

    return in_range


def knn_range_selector(nearest_neighbor: int, range_parameter: float, similarity_results: dict):
    return knn_operator(nearest_neighbor, range_operator(range_parameter, similarity_results))

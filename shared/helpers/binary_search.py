def binary_search(list_to_search_in: list, target: str):
    start = 0
    end = len(list_to_search_in) - 1

    while start <= end:
        middle = (start + end) // 2
        midpoint = list_to_search_in[middle]
        if midpoint > target:
            end = middle - 1
        elif midpoint < target:
            start = middle + 1
        else:
            return middle

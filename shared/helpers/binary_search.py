from typing import List


def binary_search(sorted_list: List[str], target: str) -> int:
    start_index = 0
    end_index = len(sorted_list) - 1

    while start_index <= end_index:
        middle_index = (start_index + end_index) // 2
        midpoint = sorted_list[middle_index]

        if midpoint > target:
            end_index = middle_index - 1
        elif midpoint < target:
            start_index = middle_index + 1
        else:
            return middle_index

    return -1  # Target not found

import random


def select_random_elements(dictionary, x):
    keys = list(dictionary.keys())
    random_keys = random.sample(keys, x)

    selected_values = [dictionary[key] for key in random_keys]

    return selected_values

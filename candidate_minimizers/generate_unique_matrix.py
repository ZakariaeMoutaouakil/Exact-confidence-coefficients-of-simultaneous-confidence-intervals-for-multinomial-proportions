from itertools import combinations_with_replacement

import numpy as np


def generate_unique_matrix(k: int, elements: np.ndarray) -> np.ndarray:
    """
    Generates a unique matrix where each row is a vector of size k,
    composed of elements from the NumPy array, and the sum of the elements in each row is ≤ 1.
    Rows are considered unique if they are not permutations of each other.

    Parameters:
        k (int): The size of each combination vector.
        elements (np.ndarray): An array of float elements to combine.

    Returns:
        np.ndarray: An array of unique vectors meeting the sum condition.
    """
    # Generate all possible combinations with replacement of the elements with size k
    all_combinations = np.array(list(combinations_with_replacement(elements, k)))

    # Filter combinations where the sum is less than or equal to 1
    sum_filter = np.sum(all_combinations, axis=1) <= 1
    valid_combinations = all_combinations[sum_filter]

    # Sort each combination to prevent permutations being treated as unique
    sorted_combinations = np.sort(valid_combinations, axis=1)

    # Use np.unique to find unique rows
    unique_combinations = np.unique(sorted_combinations, axis=0)

    return unique_combinations


if __name__ == "__main__":
    # Example usage
    k_ = 2
    elements_ = np.array([0.1, 0.2, 0.9])
    result_matrix = generate_unique_matrix(k_, elements_)
    print(result_matrix)

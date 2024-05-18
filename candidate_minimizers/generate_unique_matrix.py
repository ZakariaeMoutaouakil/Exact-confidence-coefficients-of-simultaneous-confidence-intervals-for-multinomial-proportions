from itertools import combinations_with_replacement
from typing import List


def generate_unique_matrix(k: int, elements: List[float]) -> List[List[float]]:
    """Generates a unique matrix where each row is a vector of size n,
    composed of elements from the list, and the sum of the elements in each row is ≤ 1.
    Rows are considered unique if they are not permutations of each other."""
    unique_rows = set()

    # Generate all possible combinations with replacement of the elements with size n
    for combination in combinations_with_replacement(elements, k):
        if sum(combination) <= 1:
            # Sort the combination to ensure permutations are considered identical
            sorted_combination = tuple(sorted(combination))
            unique_rows.add(sorted_combination)

    # Convert the set of unique rows back to a list of lists
    matrix = [list(row) for row in unique_rows]
    return matrix


if __name__ == "__main__":
    # Example usage
    k_ = 2
    elements_ = [0.1, 0.2, 0.9]
    result_matrix = generate_unique_matrix(k_, elements_)
    for r in result_matrix:
        print(r)

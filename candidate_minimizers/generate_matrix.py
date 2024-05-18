from itertools import product
from typing import List


def generate_matrix(n: int, elements: List[float]) -> List[List[float]]:
    """Generates a matrix where each row is a vector of size n,
    composed of elements from the list, and the sum of the elements in each row is ≤ 1."""
    matrix: List[List[float]] = []

    # Generate all possible combinations of the elements with repetition, of size n
    for vector in product(elements, repeat=n):
        if sum(vector) <= 1:
            matrix.append(list(vector))

    return matrix


# Example usage
n = 3
elements = [0.1, 0.2, 0.3]
result_matrix = generate_matrix(n, elements)
for row in result_matrix:
    print(row)

from typing import List


def filter_probability_vectors(prob_vectors: List[List[float]], threshold: float = 0.5) -> List[List[float]]:
    """
    Filters a list of probability vectors, keeping only those with at least one element greater than 0.5.

    Parameters:
        :param prob_vectors:
        :param threshold:

    Returns:
        List[List[float]]: Filtered list of probability vectors.
    """
    # Filter and keep vectors where any element is greater than 0.5
    filtered_vectors = [vector for vector in prob_vectors if any(prob > threshold for prob in vector)]
    return filtered_vectors


# Example usage
if __name__ == "__main__":
    # List of probability vectors
    probability_vectors = [
        [0.1, 0.2, 0.3],
        [0.6, 0.4, 0.2],
        [0.45, 0.55, 0.0],
        [0.25, 0.25, 0.25],
        [0.9, 0.05, 0.05]
    ]

    # Filtering the vectors
    filtered_vectors_ = filter_probability_vectors(probability_vectors)

    # Print the result
    print("Filtered Probability Vectors:")
    for vec in filtered_vectors_:
        print(vec)

from typing import List, Callable


# Define a condition where at least one element should be greater than a certain threshold
def filter_probability_vector(v: List[float], threshold: float = 0.5) -> bool:
    """
    Checks if any element in the input list is greater than 0.5.

    Parameters:
        v (list): Input list (probability vector).
        :param v: List of probability vectors.
        :param threshold: Threshold value (default is 0.5).

    Returns:
        bool: True if any element in the list is greater than 0.5, False otherwise.
    """
    return any(prob > threshold for prob in v)


def filter_probability_vectors(
        prob_vectors: List[List[float]],
        condition: Callable[[List[float]], bool]
) -> List[List[float]]:
    """
    Filters a list of probability vectors based on a specified boolean condition applied to the vectors themselves.

    Parameters:
        prob_vectors: List of probability vectors to filter.
        condition: A callable that takes a list of floats (a probability vector) and returns a boolean.
                   This function defines the condition to check for each vector.

    Returns:
        List[List[float]]: Filtered list of probability vectors where the condition is true.
    """
    # Filter and keep vectors where the condition on the vector returns True
    filtered_vectors = [vector for vector in prob_vectors if condition(vector)]
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

    # Filtering the vectors with a custom condition
    filtered_vectors_ = filter_probability_vectors(probability_vectors, filter_probability_vector)

    # Print the result
    print("Filtered Probability Vectors:")
    for vec in filtered_vectors_:
        print(vec)

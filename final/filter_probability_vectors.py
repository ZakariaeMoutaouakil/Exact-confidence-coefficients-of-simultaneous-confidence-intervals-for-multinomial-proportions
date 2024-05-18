import numpy as np


def filter_probability_vectors(prob_vectors: np.ndarray, threshold: float = 0.5) -> np.ndarray:
    """
    Filters an array of probability vectors, keeping only those with at least one element greater than 0.5.

    Parameters:
        prob_vectors (np.ndarray): Array of probability vectors.

    Returns:
        np.ndarray: Filtered array of probability vectors.
        :param prob_vectors:
        :param threshold:
    """
    # Use a vectorized condition to check if any element in each vector is greater than 0.5
    # np.any along axis=1 returns True for rows where at least one element meets the condition
    filtered_vectors = prob_vectors[np.any(prob_vectors > threshold, axis=1)]

    return filtered_vectors


# Example usage
if __name__ == "__main__":
    # List of probability vectors converted to a NumPy array
    probability_vectors = np.array([
        [0.1, 0.2, 0.3],
        [0.6, 0.4, 0.2],
        [0.45, 0.55, 0.0],
        [0.25, 0.25, 0.25],
        [0.9, 0.05, 0.05]
    ])

    # Filtering the vectors using the optimized function
    filtered_vectors_ = filter_probability_vectors(probability_vectors)

    # Print the result
    print(filtered_vectors_)

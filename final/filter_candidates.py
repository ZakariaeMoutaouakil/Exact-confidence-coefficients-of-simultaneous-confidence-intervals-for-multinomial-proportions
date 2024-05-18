import numpy as np

from final.filter_probability_vectors import filter_probability_vectors
from final.transform_to_probability_vector import transform_to_probability_vector


def filter_candidates(candidates: np.ndarray) -> np.ndarray:
    """
    Transforms candidates into probability vectors, filters them, and omits the last coordinate.

    Parameters:
        candidates (np.ndarray): An array of candidate vectors.

    Returns:
        np.ndarray: An array of processed candidate vectors, each missing the last coordinate.
    """
    # Transform candidates to probability vectors
    full_candidates = np.apply_along_axis(transform_to_probability_vector, axis=1, arr=candidates)

    # Filter candidates based on the probability vectors
    filtered_candidates = filter_probability_vectors(full_candidates)

    # Crop the last element off each candidate vector using slicing
    cropped_candidates = filtered_candidates[:, :-1]

    return cropped_candidates


# Example usage
if __name__ == "__main__":
    # Example list of candidates (vectors) initially as NumPy array
    candidates_ = np.array([
        [0.1, 0.2, 0.3],
        [0.6, 0.4, 0.2],
        [0.45, 0.55, 0.0],
        [0.25, 0.25, 0.25],
        [0.9, 0.05, 0.05]
    ])

    # Filter the candidates
    filtered_candidates_ = filter_candidates(candidates_)

    # Print the result
    print("Filtered Candidates:", filtered_candidates_)

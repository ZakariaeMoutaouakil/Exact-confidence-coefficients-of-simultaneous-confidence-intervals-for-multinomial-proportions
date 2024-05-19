from typing import List, Callable

from final.filter_probability_vectors import filter_probability_vectors, filter_probability_vector
from final.transform_to_probability_vector import transform_to_probability_vector


def filter_candidates(
        candidates: List[List[float]],
        condition: Callable[[List[float]], bool] = filter_probability_vector
) -> List[List[float]]:
    full_candidates = [transform_to_probability_vector(c) for c in candidates]
    filtered_candidates = filter_probability_vectors(full_candidates, condition)
    cropped_candidates = [c[:-1] for c in filtered_candidates]
    return cropped_candidates


# Example usage
if __name__ == "__main__":
    # Example list of candidates (vectors)
    vectors = [
        [0.1, 0.2, 0.3, 0.4],
        [0.6, 0.4, 0.2, 0.1],
        [0.45, 0.55, 0.0, 0.0],
        [0.25, 0.25, 0.25, 0.25],
        [0.9, 0.05, 0.05, 0.0]
    ]

    # Filter the candidates
    filtered_vectors = filter_candidates(vectors)

    # Print the result
    print("Filtered Candidates:")
    for candidate in filtered_vectors:
        print(candidate)

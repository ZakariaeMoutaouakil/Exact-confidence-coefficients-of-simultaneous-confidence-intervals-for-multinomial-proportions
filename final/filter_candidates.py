from typing import List

from final.filter_probability_vectors import filter_probability_vectors
from final.transform_to_probability_vector import transform_to_probability_vector


def filter_candidates(candidates: List[List[float]], threshold: float = 0.5) -> List[List[float]]:
    full_candidates = [transform_to_probability_vector(c) for c in candidates]
    filtered_candidates = filter_probability_vectors(full_candidates, threshold)
    cropped_candidates = [c[:-1] for c in filtered_candidates]
    return cropped_candidates


# Example usage
if __name__ == "__main__":
    # Example list of candidates (vectors)
    candidates_ = [
        [0.1, 0.2, 0.3, 0.4],
        [0.6, 0.4, 0.2, 0.1],
        [0.45, 0.55, 0.0, 0.0],
        [0.25, 0.25, 0.25, 0.25],
        [0.9, 0.05, 0.05, 0.0]
    ]

    # Filter the candidates
    filtered_candidates_ = filter_candidates(candidates_)

    # Print the result
    print("Filtered Candidates:")
    for candidate in filtered_candidates_:
        print(candidate)

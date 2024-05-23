from typing import Callable, List, Tuple

import numpy as np

from confidence_intervals.multinomial_confidence_intervals import multinomial_confidence_intervals
from coverage_probability.coverage_probability import coverage_probability
from final.transform_to_probability_vector import transform_to_probability_vector


def example_weight_function(vector: np.ndarray) -> float:
    # Example weight function, replace with your actual logic
    return np.sum(vector)


def find_skewed_average_minimizer(
        n: int,
        candidates: List[List[float]],
        confidence_interval_function: Callable[[List[int]], List[Tuple[float, float]]],
        weight_function: Callable[[np.ndarray], float] = example_weight_function,
        debug: bool = False
) -> Tuple[float, List[float]]:
    """Finds the skewed average minimizer of the elements in the list."""
    total_weighted_cov_prob = 0.0
    total_weight = 0.0
    weighted_candidates = []

    for p in candidates:
        cov_proba = coverage_probability(n, p, confidence_interval_function)
        print(transform_to_probability_vector(p))
        weight = weight_function(np.array(transform_to_probability_vector(p)))
        weighted_cov_proba = cov_proba * weight
        total_weighted_cov_prob += weighted_cov_proba
        total_weight += weight
        weighted_candidates.append((weighted_cov_proba, weight, p))

        if debug:
            print(
                f"Candidate: {p}, Coverage Probability: {cov_proba}, Weight: {weight}, Weighted Cov Proba: {weighted_cov_proba}")

    # Calculate the skewed average
    skewed_average_cov_prob = total_weighted_cov_prob / total_weight if total_weight != 0 else float('inf')

    # Find the minimizer which is the one closest to the skewed average
    min_value, minimizer = float('inf'), []

    for weighted_cov_proba, weight, p in weighted_candidates:
        if abs(weighted_cov_proba / weight - skewed_average_cov_prob) < min_value:
            min_value = abs(weighted_cov_proba / weight - skewed_average_cov_prob)
            minimizer = p

    return skewed_average_cov_prob, minimizer


if __name__ == '__main__':
    # Example usage
    n_example = 10
    candidates_example = [
        [0.1, 0.2, 0.3],
        [0.2, 0.3, 0.4],
        [0.3, 0.4, 0.5]
    ]

    skewed_average, minimiser = find_skewed_average_minimizer(
        n_example, candidates_example, multinomial_confidence_intervals, example_weight_function, debug=True
    )
    print(f"Skewed average coverage probability: {skewed_average}")
    print(f"Minimizing candidate: {minimiser}")

from typing import Callable, List, Tuple

from confidence_intervals.confidence_interval import confidence_interval
from coverage_probability.coverage_probability import coverage_probability


def find_minimizer(
        n: int,
        candidates: List[List[float]],
        confidence_interval_function: Callable[[float, int], Tuple[float, float]]
) -> Tuple[float, List[float]]:
    """Finds the minimizer of the elements in the list."""
    min_value, minimizer = float('inf'), []

    for p in candidates:
        intervals = [confidence_interval_function(p_i, n) for p_i in p]
        cov_proba = coverage_probability(n, p, intervals)

        if cov_proba < min_value:
            min_value, minimizer = cov_proba, p

    return min_value, minimizer


if __name__ == '__main__':
    # Example usage
    n_example = 10
    candidates_example = [
        [0.1, 0.2, 0.3],
        [0.2, 0.3, 0.4],
        [0.3, 0.4, 0.5]
    ]

    min_value, minimizer = find_minimizer(n_example, candidates_example, confidence_interval)
    print(f"Minimum coverage probability: {min_value}")
    print(f"Minimizing candidate: {minimizer}")

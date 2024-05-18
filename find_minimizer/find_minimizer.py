from typing import Callable, Tuple

import numpy as np

from confidence_intervals.multinomial_confidence_intervals import multinomial_confidence_intervals
from coverage_probability.coverage_probability import coverage_probability


def find_minimizer(
        n: int,
        candidates: np.ndarray,
        confidence_interval_function: Callable[[np.ndarray], np.ndarray],
        debug: bool = False
) -> Tuple[float, np.ndarray]:
    """
    Finds the minimizer of the elements in the array.

    Parameters:
        n (int): A parameter used in the confidence interval calculation.
        candidates (np.ndarray): Array of candidate probability vectors.
        confidence_interval_function (Callable): Function to calculate confidence intervals.
        debug (bool): If True, prints debugging information.

    Returns:
        Tuple[float, np.ndarray]: Tuple containing the minimum coverage probability and the minimizing candidate vector.
    """
    min_value = float('inf')
    minimizer = np.array([])

    for p in candidates:
        cov_proba = coverage_probability(n, p, confidence_interval_function)
        if debug:
            print(p, cov_proba)

        if cov_proba < min_value:
            min_value = cov_proba
            minimizer = p

    return min_value, minimizer


if __name__ == '__main__':
    # Example usage
    n_example = 10
    candidates_example = np.array([
        [0.1, 0.2, 0.3],
        [0.2, 0.3, 0.4],
        [0.3, 0.4, 0.5]
    ])

    min_value, minimizer = find_minimizer(n_example, candidates_example, multinomial_confidence_intervals, debug=True)
    print(f"Minimum coverage probability: {min_value}")
    print(f"Minimizing candidate: {minimizer}")

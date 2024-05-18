from itertools import product
from typing import Callable

import numpy as np
from scipy.stats import multinomial

from confidence_intervals.multinomial_confidence_intervals import multinomial_confidence_intervals
from final.transform_to_probability_vector import transform_to_probability_vector


def coverage_probability(
        n: int,
        p: np.ndarray,
        multinomial_confidence_interval: Callable[[np.ndarray], np.ndarray],
        debug: bool = False
) -> float:
    """Calculates the coverage probability using NumPy and SciPy for efficiency.

    Parameters:
        n (int): Total number of trials.
        p (np.ndarray): Probability vector for the multinomial distribution.
        multinomial_confidence_interval (Callable): Function to calculate confidence intervals for each count.
        debug (bool): If True, prints additional debug information.

    Returns:
        float: The coverage probability calculated across all valid combinations.
    """
    d = len(p)
    coverage_prob = 0.

    # Generate all possible combinations of x1, x2, ..., xd that sum to n
    xs = np.array([x for x in product(range(n + 1), repeat=(d + 1)) if sum(x) == n])

    # Calculate the confidence intervals for each combination
    interval_arrays = np.array([multinomial_confidence_interval(x) for x in xs])

    # Loop through each combination and its respective intervals
    for i, x in enumerate(xs):
        intervals = interval_arrays[i]
        if debug:
            print(intervals)

        inside_interval = all(intervals[j][0] <= p[j] <= intervals[j][1] for j in range(d))

        if inside_interval:
            # Compute the probability of this particular combination
            prob = multinomial.pmf(x, n, transform_to_probability_vector(p))
            coverage_prob += prob

            if debug:
                print(f"Combination: {x}, Probability: {prob}, Coverage: {coverage_prob}")

    return coverage_prob


if __name__ == '__main__':
    # Example usage
    n_ = 4
    p_ = np.array([0.2, 0.5])
    multinomial_confidence_intervals_ = multinomial_confidence_intervals

    print(coverage_probability(n_, p_, multinomial_confidence_intervals_, debug=True))

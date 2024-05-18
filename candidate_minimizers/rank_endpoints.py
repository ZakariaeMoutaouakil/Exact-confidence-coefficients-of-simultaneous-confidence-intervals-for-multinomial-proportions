from typing import Callable, Tuple

import numpy as np


def example_confidence_interval(p: float, n: int) -> Tuple[float, float]:
    """Placeholder for the actual confidence interval function to compute the interval for p and n."""
    # Example: using a simple symmetric interval around p
    lower_bound = max(0., p - 0.1 / n)
    upper_bound = min(1., p + 0.1 / n)
    return lower_bound, upper_bound


def rank_endpoints(
        n: int,
        confidence_interval_function: Callable[[float, int], Tuple[float, float]],
        precision: int = 10
) -> np.ndarray:
    """Ranks the endpoints of the confidence intervals generated by the provided function using NumPy."""
    # Generate probabilities for each possible count outcome
    probabilities = np.arange(n + 1) / n

    # Calculate confidence intervals
    intervals = np.array([confidence_interval_function(p, n) for p in probabilities])

    # Round endpoints to the specified precision
    rounded_endpoints = np.round(intervals, precision)

    # Flatten the array to get a single array of endpoints
    flattened_endpoints = rounded_endpoints.flatten()

    # Filter endpoints to keep those between 0 and 1
    filtered_endpoints = flattened_endpoints[(flattened_endpoints > 0) & (flattened_endpoints < 1)]

    # Rank the filtered endpoints and return as a sorted array
    ranked_endpoints = np.unique(filtered_endpoints)

    return ranked_endpoints


if __name__ == "__main__":
    # Example usage
    N = 10
    ranked_endpoints_ = rank_endpoints(N, example_confidence_interval)
    print("Ranked endpoints between 0 and 1:", ranked_endpoints_)

import time
from typing import Callable, Tuple

from candidate_minimizers.generate_unique_matrix import generate_unique_matrix
from candidate_minimizers.rank_endpoints import rank_endpoints
from confidence_intervals.confidence_interval import confidence_interval
from confidence_intervals.multinomial_confidence_intervals import multinomial_confidence_intervals
from final.filter_candidates import filter_candidates
from final.transform_to_probability_vector import transform_to_probability_vector
from find_minimizer.find_minimizer import find_minimizer


def execute_analysis(
        n: int,
        k: int, confidence_interval_function: Callable[[float, int], Tuple[float, float]],
        use_filtering: bool = True
):
    print("N =", n)
    start_time = time.time()  # Start time measurement

    ranked_endpoints = rank_endpoints(n, confidence_interval_function)
    candidates = generate_unique_matrix(k - 1, ranked_endpoints)

    if use_filtering:
        candidates = filter_candidates(candidates)

    min_value, minimizer = find_minimizer(n, candidates, multinomial_confidence_intervals)
    end_time = time.time()  # End time measurement
    elapsed_time = end_time - start_time  # Calculate elapsed time

    print(f"{'With' if use_filtering else 'Without'} Filtering:")
    print("Minimum value:", min_value)
    print("Minimizer:", transform_to_probability_vector(minimizer))
    print("Risk:", 1 - min_value)
    print("Elapsed time:", elapsed_time)


# Example usage
if __name__ == '__main__':
    N_values = [10, 20, 30]
    K = 3
    for N in N_values:
        execute_analysis(N, K, confidence_interval, use_filtering=False)
        execute_analysis(N, K, confidence_interval)

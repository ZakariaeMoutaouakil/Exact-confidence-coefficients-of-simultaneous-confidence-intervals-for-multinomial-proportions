import time
from typing import Callable, Tuple, List

from candidate_minimizers.generate_unique_matrix import generate_unique_matrix
from candidate_minimizers.rank_endpoints import rank_endpoints
from confidence_intervals.confidence_interval import confidence_interval
from confidence_intervals.multinomial_confidence_intervals import multinomial_confidence_intervals
from final.filter_candidates import filter_candidates
from final.filter_probability_vectors import filter_probability_vector
from final.transform_to_probability_vector import transform_to_probability_vector
from find_minimizer.find_minimizer import find_minimizer


def execute_analysis(
        N: int,
        K: int,
        confidence_interval_function: Callable[[float, int], Tuple[float, float]],
        condition: Callable[[List[float]], bool] = None
):
    print("N =", N)
    start_time = time.time()  # Start time measurement

    ranked_endpoints = rank_endpoints(N, confidence_interval_function)
    candidates = generate_unique_matrix(K - 1, ranked_endpoints)

    if condition:
        candidates = filter_candidates(candidates, condition)

    min_value, minimizer = find_minimizer(N, candidates, multinomial_confidence_intervals)
    end_time = time.time()  # End time measurement
    elapsed_time = end_time - start_time  # Calculate elapsed time

    print(f"{'With' if condition else 'Without'} Filtering:")
    print("Minimum value:", min_value)
    print("Minimizer:", transform_to_probability_vector(minimizer))
    print("Risk:", 1 - min_value)
    print("Elapsed time:", elapsed_time)

    return 1 - min_value


# Example usage
if __name__ == '__main__':
    N_values = [10, 20, 30]
    K = 3
    for N in N_values:
        # r1 = execute_analysis(N, K, confidence_interval, use_filtering=False)
        condition1 = lambda v: filter_probability_vector(v, threshold=0.8)
        condition2 = lambda v: filter_probability_vector(v, threshold=0.9)
        r1 = execute_analysis(N, K, confidence_interval, condition1)
        r2 = execute_analysis(N, K, confidence_interval, condition2)
        print("Risk gain:", r1 - r2)

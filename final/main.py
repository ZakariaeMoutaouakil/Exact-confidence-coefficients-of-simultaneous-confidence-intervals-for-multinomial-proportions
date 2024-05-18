import time
from typing import Callable, Tuple

from candidate_minimizers.generate_unique_matrix import generate_unique_matrix
from candidate_minimizers.rank_endpoints import rank_endpoints
from confidence_intervals.confidence_interval import confidence_interval
from confidence_intervals.multinomial_confidence_intervals import multinomial_confidence_intervals
from final.filter_candidates import filter_candidates
from final.transform_to_probability_vector import transform_to_probability_vector
from find_minimizer.find_minimizer import find_minimizer

for N in [10, 20, 30]:
    print("N =", N)
    start_time = time.time()  # Start time measurement
    K = 3
    confidence_interval_function: Callable[[float, int], Tuple[float, float]] = confidence_interval
    ranked_endpoints = rank_endpoints(N, confidence_interval_function)
    candidates = generate_unique_matrix(K - 1, ranked_endpoints)
    filtered_candidates = filter_candidates(candidates)
    min_value, minimizer = find_minimizer(N, candidates, multinomial_confidence_intervals)
    end_time = time.time()  # End time measurement
    elapsed_time = end_time - start_time  # Calculate elapsed time
    print("Without Filtering:")
    print("Minimum value:", min_value)
    print("Minimizer:", transform_to_probability_vector(minimizer))
    print("Risk:", 1 - min_value)
    print("Elapsed time:", elapsed_time)

    start_time = time.time()  # Start time measurement
    second_min_value, minimizer = find_minimizer(N, filtered_candidates, multinomial_confidence_intervals)
    end_time = time.time()  # End time measurement
    elapsed_time = end_time - start_time  # Calculate elapsed time
    print("With Filtering:")
    print("Minimum value:", second_min_value)
    print("Minimizer:", transform_to_probability_vector(minimizer))
    print("Risk:", 1 - second_min_value)
    print("Risk gain:", second_min_value - min_value)
    print("Elapsed time:", elapsed_time)

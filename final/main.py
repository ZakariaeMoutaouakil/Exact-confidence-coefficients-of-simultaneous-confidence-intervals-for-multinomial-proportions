from typing import Callable, Tuple

from candidate_minimizers.generate_unique_matrix import generate_unique_matrix
from candidate_minimizers.rank_endpoints import rank_endpoints
from confidence_intervals.confidence_interval import confidence_interval
from final.transform_to_probability_vector import transform_to_probability_vector
from find_minimizer.find_minimizer import find_minimizer

N = 15
K = 4
confidence_interval_function: Callable[[float, int], Tuple[float, float]] = confidence_interval
ranked_endpoints = rank_endpoints(N, confidence_interval_function)
print("Ranked endpoints between 0 and 1:", ranked_endpoints)
candidates = generate_unique_matrix(K - 1, ranked_endpoints)
print("Candidates:", candidates)
min_value, minimizer = find_minimizer(N, candidates, confidence_interval_function)
print("Minimum value:", min_value)
print("Minimizer:", transform_to_probability_vector(minimizer))

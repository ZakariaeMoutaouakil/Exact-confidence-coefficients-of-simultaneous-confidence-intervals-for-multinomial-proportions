from typing import Callable, Tuple

from candidate_minimizers.generate_unique_matrix import generate_unique_matrix
from candidate_minimizers.rank_endpoints import rank_endpoints
from confidence_intervals.confidence_interval import confidence_interval
from find_minimizer.find_minimizer import find_minimizer

N = 5
confidence_interval_function: Callable[[float, int], Tuple[float, float]] = confidence_interval
ranked_endpoints = rank_endpoints(N, confidence_interval_function)
# print("Ranked endpoints between 0 and 1:", ranked_endpoints)
candidates = generate_unique_matrix(N, ranked_endpoints)
min_value, minimizer = find_minimizer(N, candidates, confidence_interval_function)
print("Minimum value:", min_value)
print("Minimizer:", minimizer)
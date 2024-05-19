import os
import time
from typing import Callable, List

from candidate_minimizers.generate_unique_matrix import generate_unique_matrix
from candidate_minimizers.rank_endpoints import rank_endpoints
from confidence_intervals.confidence_interval import ConfidenceIntervalCalculator, BaseConfidenceIntervalCalculator
from confidence_intervals.multinomial_confidence_intervals import multinomial_confidence_intervals
from final.filter_candidates import filter_candidates
from final.filter_probability_vectors import filter_probability_vector
from final.transform_to_probability_vector import transform_to_probability_vector
from find_minimizer.find_minimizer import find_minimizer


def check_existing_entry(
        file_path: str,
        N: int,
        K: int,
        confidence_interval_function_name: str,
        alpha: float,
        condition_name: str
) -> bool:
    """
    Check if an entry with the specified parameters already exists in the TSV file.

    Parameters:
        file_path (str): Path to the TSV file.
        N (int): Value of N.
        K (int): Value of K.
        confidence_interval_function_name (str): Name of the confidence interval function.
        condition_name (str): Name of the condition function.

    Returns:
        bool: True if an entry with the same parameters exists, False otherwise.
    """
    if not os.path.exists(file_path):
        return False

    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith(f"{N}\t{K}\t{confidence_interval_function_name}\t{alpha}\t{condition_name}"):
                return True

    return False


def tsv_analysis(
        N: int,
        K: int,
        file_path: str,
        confidence_interval_function: BaseConfidenceIntervalCalculator,
        condition: Callable[[List[float]], bool] = None,
        alpha: float = 0.05,
        debug: bool = False
) -> float | None:
    confidence_interval_function_name = confidence_interval_function.__name__
    confidence_interval_function_alpha = confidence_interval_function.alpha
    condition_name = condition.__name__ if condition else ''

    if debug:
        print("N =", N)
        print("K =", K)
        print("Confidence Interval Function Name =", confidence_interval_function_name)
        print("Confidence Interval Function Alpha =", confidence_interval_function_alpha)
        print("Condition =", condition_name)

    if check_existing_entry(file_path, N, K, confidence_interval_function_name, confidence_interval_function_alpha,
                            condition_name):
        print(
            f"Entry for N={N}, K={K}, confidence_interval_function={confidence_interval_function_name}, alpha={alpha}, condition={condition_name} already exists. Skipping computation."
        )
        return None

    start_time = time.time()  # Start time measurement

    ranked_endpoints = rank_endpoints(N, confidence_interval_function)
    candidates = generate_unique_matrix(K - 1, ranked_endpoints)

    if condition:
        candidates = filter_candidates(candidates, condition)
        filtering_status = 'True'
    else:
        filtering_status = 'False'

    if debug:
        print("With Filtering =", filtering_status)

    min_value, minimizer = find_minimizer(N, candidates, multinomial_confidence_intervals)
    end_time = time.time()  # End time measurement
    elapsed_time = end_time - start_time  # Calculate elapsed time

    if debug:
        print("Minimum value =", min_value)
        print("Minimizer =", minimizer)
        print("Risk =", 1 - min_value)
        print("Elapsed time =", elapsed_time)

    minimizer_vector = transform_to_probability_vector(minimizer)
    risk = 1 - min_value

    # Prepare data as a string formatted for TSV
    data_row = f"{N}\t{K}\t{confidence_interval_function_name}\t{confidence_interval_function_alpha}\t{condition_name}\t{filtering_status}\t{min_value}\t{minimizer_vector}\t{risk}\t{elapsed_time}\n"

    # Write to file
    with open(file_path, 'a') as file:
        if debug:
            print("Writing to file:", data_row)
        file.write(data_row)

    return risk


def tsv_analysis_multiple(
        N_values: List[int],
        K_values: List[int],
        file_path: str,
        confidence_interval_function_values: List[BaseConfidenceIntervalCalculator],
        condition: Callable[[List[float]], bool] = None,
        alpha: float = 0.05,
        debug: bool = False
) -> List[float]:
    # Check if file exists and write headers if it doesn't
    if not os.path.exists(file_path):
        if debug:
            print(f"{file_path} does not exist. Creating file and adding headers.")
        with open(file_path, 'w') as f:
            f.write(
                "N\tK\tConfidence Interval Function\tConfidence Interval Function Alpha\tCondition\tFiltering\tMinimum Value\tMinimizer\tRisk\tElapsed Time\n"
            )

    risks = []
    for N in N_values:
        for K in K_values:
            for confidence_interval_function in confidence_interval_function_values:
                risk = tsv_analysis(N, K, file_path, confidence_interval_function, condition, alpha, debug)
                if risk is not None:
                    risks.append(risk)
    return risks


# Example usage
if __name__ == '__main__':
    file_path = 'analysis_results.tsv'
    N_values = [40, 50, 60, 70, 80]
    K_values = [3]  # Assuming we want to use a single K value, but it could be a list of values
    conf_interval = ConfidenceIntervalCalculator()
    confidence_interval_functions = [conf_interval]  # List of functions

    thresholds = [0.5, 0.6, 0.7, 0.8, 0.9]
    for th in thresholds:
        condition = lambda v: filter_probability_vector(v, threshold=th)
        condition.__name__ = f'Threshold={th}'  # Name the lambda for file recording
        # Execute analysis for each condition
        tsv_analysis_multiple(N_values, K_values, file_path, confidence_interval_functions, condition, debug=True)

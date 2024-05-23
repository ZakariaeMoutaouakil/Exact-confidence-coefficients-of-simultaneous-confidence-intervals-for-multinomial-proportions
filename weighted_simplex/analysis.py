import os
import time
from typing import Callable, List

import numpy as np

from candidate_minimizers.generate_unique_matrix import generate_unique_matrix
from candidate_minimizers.rank_endpoints import rank_endpoints
from confidence_intervals.confidence_interval import ConfidenceIntervalCalculator, BaseConfidenceIntervalCalculator
from confidence_intervals.multinomial_confidence_intervals import multinomial_confidence_intervals
from final.transform_to_probability_vector import transform_to_probability_vector
from weighted_simplex.find_minimizer import find_skewed_average_minimizer
from weighted_simplex.learn_mass_function import learn_mass_function


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
        weight_function: Callable[[np.ndarray], float],
        alpha: float = 0.05,
        debug: bool = False
) -> float | None:
    confidence_interval_function_name = confidence_interval_function.__name__
    confidence_interval_function_alpha = confidence_interval_function.alpha
    weight_function_name = weight_function.__name__ if weight_function else ''

    if debug:
        print("N =", N)
        print("K =", K)
        print("Confidence Interval Function Name =", confidence_interval_function_name)
        print("Confidence Interval Function Alpha =", confidence_interval_function_alpha)
        print("Weight Function =", weight_function_name)

    if check_existing_entry(file_path, N, K, confidence_interval_function_name, confidence_interval_function_alpha,
                            weight_function_name):
        print(
            f"Entry for N={N}, K={K}, confidence_interval_function={confidence_interval_function_name}, alpha={alpha}, weight_function={weight_function_name} already exists. Skipping computation."
        )
        return None

    start_time = time.time()  # Start time measurement

    ranked_endpoints = rank_endpoints(N, confidence_interval_function)
    candidates = generate_unique_matrix(K - 1, ranked_endpoints)
    filtering_status = 'Weighted'

    if debug:
        print("With Filtering =", filtering_status)

    min_value, minimizer = find_skewed_average_minimizer(N, candidates, multinomial_confidence_intervals,
                                                         weight_function)
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
    data_row = f"{N}\t{K}\t{confidence_interval_function_name}\t{confidence_interval_function_alpha}\t{weight_function_name}\t{filtering_status}\t{min_value}\t{minimizer_vector}\t{risk}\t{elapsed_time}\n"

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
        weight_functions: List[Callable[[np.ndarray], float]],
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
                for weight_function in weight_functions:
                    risk = tsv_analysis(N, K, file_path, confidence_interval_function, weight_function, alpha, debug)
                    if risk is not None:
                        risks.append(risk)
    return risks


# Example usage
if __name__ == '__main__':
    # Example list of probability vectors
    vectors = [
        np.array([0.8, 0.15, 0.05]),  # Highest probability at index 0
        np.array([0.7, 0.2, 0.1]),  # Highest probability at index 0
        np.array([0.6, 0.35, 0.05]),  # Highest probability at index 0
        np.array([0.05, 0.9, 0.05]),  # Highest probability at index 1
        np.array([0.1, 0.8, 0.1]),  # Highest probability at index 1
        np.array([0.05, 0.6, 0.35]),  # Highest probability at index 1
        np.array([0.1, 0.1, 0.8]),  # Highest probability at index 2
        np.array([0.05, 0.05, 0.9]),  # Highest probability at index 2
        np.array([0.2, 0.1, 0.7])  # Highest probability at index 2
    ]

    # Learn the mass function with dimensionality reduction
    mass_function = learn_mass_function(vectors, n_components=2)  # Use one less than the dimension

    # Explicit test vectors
    test_vectors = [
        np.array([0.1, 0.1, 0.8]),  # Highest probability at index 2
        np.array([0.05, 0.05, 0.9]),  # Highest probability at index 2
        np.array([0.2, 0.1, 0.7])  # Highest probability at index 2
    ]

    # Test the mass function with the explicit test vectors
    for i, test_vector in enumerate(test_vectors):
        mass = mass_function(test_vector)
        print(f"Test Vector {i + 1}: {test_vector}")
        print(f"Normalized Mass: {mass}\n")

    file_path = 'analysis_results.tsv'
    N_values = [20, 30, 40]
    K_values = [3]  # Assuming we want to use a single K value, but it could be a list of values
    conf_interval = ConfidenceIntervalCalculator()
    confidence_interval_functions = [conf_interval]  # List of functions
    weight_function = lambda vector: 1.
    weight_function.__name__ = 'ConstantWeightFunction'
    weight_functions = [weight_function]  # List of weight functions

    # Execute analysis for each condition
    tsv_analysis_multiple(N_values, K_values, file_path, confidence_interval_functions, weight_functions, debug=True)

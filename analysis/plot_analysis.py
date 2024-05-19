from typing import List, Callable, Tuple

import matplotlib.pyplot as plt

from confidence_intervals.confidence_interval import confidence_interval
from final.filter_probability_vectors import filter_probability_vector
from final.main import execute_analysis


def plot_analysis(
        N_values: List[int],
        K: int,
        confidence_interval_function: Callable[[float, int], Tuple[float, float]],
        thresholds: List[float]
):
    """
    Plots risk values for different thresholds and N values using the execute_analysis function.

    Parameters: N_values (List[int]): List of integers representing different values of N. K (int): Integer
    representing the K value. confidence_interval_function (Callable[[float, int], Tuple[float, float]]): Function
    that calculates confidence intervals. thresholds (List[float]): List of float values representing different
    probability thresholds.
    """
    results = {thr: [] for thr in thresholds}  # Dictionary to store results for each threshold

    for N in N_values:
        for thr in thresholds:
            condition = lambda v: filter_probability_vector(v, threshold=thr)  # Condition with a specific threshold
            risk = execute_analysis(N, K, confidence_interval_function, condition)
            results[thr].append(risk)
            print(f"N = {N}, Threshold = {thr}, Risk = {risk}")

    # Plotting
    plt.figure(figsize=(10, 6))
    for thr, risks in results.items():
        plt.plot(N_values, risks, label=f'Threshold = {thr}', marker='o')

    plt.title('Risk Analysis for Different Thresholds')
    plt.xlabel('N values')
    plt.ylabel('Risk Values')
    plt.legend()
    plt.grid(True)
    plt.show()


# Example usage
if __name__ == '__main__':
    N_values = [10, 15, 20, 25, 30, 35, 40]  # Example N values
    K = 3  # Example K value
    thresholds = [0.5, 0.6, 0.7, 0.8, 0.9]  # List of thresholds to analyze
    plot_analysis(N_values, K, confidence_interval, thresholds)

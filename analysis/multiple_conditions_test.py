from typing import List, Callable

from analysis.tsv_analysis import tsv_analysis_multiple
from conditions.conditions import entropy_lower_than_uniform
from confidence_intervals.confidence_interval import ConfidenceIntervalCalculator

if __name__ == '__main__':
    file_path = 'analysis_results.tsv'
    N_values = [50, 60, 70, 80, 90, 100]
    K_values = [3]  # Assuming we want to use a single K value, but it could be a list of values
    conf_interval = ConfidenceIntervalCalculator()
    confidence_interval_functions = [conf_interval]  # List of functions
    conditions: List[Callable[[List[float]], bool]] = []

    thresholds = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    for th in thresholds:
        condition = lambda v: entropy_lower_than_uniform(v, threshold=th)
        condition.__name__ = f'EntropyThreshold={th}'  # Name the lambda for file recording
        conditions.append(condition)

    # Execute analysis for each condition
    tsv_analysis_multiple(N_values, K_values, file_path, confidence_interval_functions, conditions, debug=True)

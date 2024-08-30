import math
import time
from typing import List

import pandas as pd
from mpmath import mp

# Set the precision for mpmath
mp.dps = 50  # Set the desired precision (adjust as needed)


def stirling_factorial(n: int):
    if n == 0 or n == 1:
        return 1
    else:
        return mp.sqrt(2 * mp.pi * n) * (n / mp.e) ** n


def exact_factorial(n: int):
    return math.factorial(n)


# Function to measure time complexity and precision
def compare_factorials(n_values: List[int]):
    results = []
    for n in n_values:
        # Measure time and calculate exact factorial
        start_time = time.time()
        exact = exact_factorial(n)
        exact_time = time.time() - start_time

        # Measure time and calculate Stirling's approximation
        start_time = time.time()
        approx = stirling_factorial(n)
        approx_time = time.time() - start_time

        # Calculate relative error
        relative_error = abs((approx - exact) / exact) * 100

        # Append results
        results.append((n, exact, approx, relative_error, exact_time, approx_time))
    return results


n_values_ = [1, 2, 5, 10, 15, 20, 50, 100, 200, 500, 1000]
results_ = compare_factorials(n_values_)

df = pd.DataFrame(results_,
                  columns=['n', 'Exact Factorial', 'Stirling Approximation', 'Relative Error (%)', 'Exact Time (s)',
                           'Approx Time (s)'])

# Set display options to show all rows and columns
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

print("Factorial Comparison with Time Complexity")
print(df)

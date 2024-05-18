import math
from itertools import product
from typing import List, Tuple, Callable

from confidence_intervals.multinomial_confidence_intervals import multinomial_confidence_intervals


def indicator(x: float, interval: Tuple[float, float]):
    """Indicator function that checks if x is in the interval."""
    return True if interval[0] <= x <= interval[1] else False


def multinomial_coefficient(n: int, x: Tuple[int]):
    """Calculates the multinomial coefficient."""
    return math.factorial(n) // math.prod(math.factorial(xi) for xi in x)


def coverage_probability(
        n: int,
        p: List[float],
        multinomial_confidence_interval: Callable[[List[int]], List[Tuple[float, float]]],
        debug: bool = False
):
    """Calculates the coverage probability."""
    d = len(p)
    coverage_prob = 0.

    # Generate all possible combinations of x1, x2, ..., xd
    for x in product(range(n + 1), repeat=(d + 1)):
        if sum(x) == n:
            if debug:
                print(x)

            # Calculate the confidence intervals
            intervals = multinomial_confidence_interval(x)

            if all(indicator(p[i], intervals[i]) for i in range(d)):
                # Calculate the multinomial coefficient
                multinom_coeff = multinomial_coefficient(n, x)
                # print(multinom_coeff)

                # Calculate the product of p1^x1 * p2^x2 * ... * pd^xd
                prob_product = math.prod(p[i] ** x[i] for i in range(d)) * ((1 - sum(p)) ** x[d])

                # Update the coverage probability sum
                coverage_prob += multinom_coeff * prob_product

    return coverage_prob


if __name__ == '__main__':
    # Example usage
    n_ = 4
    p_ = [0.2, 0.5]
    multinomial_confidence_intervals_ = multinomial_confidence_intervals

    print(coverage_probability(n_, p_, multinomial_confidence_intervals_, debug=True))

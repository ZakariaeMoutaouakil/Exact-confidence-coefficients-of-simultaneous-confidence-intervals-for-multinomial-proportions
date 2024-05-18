from typing import List, Tuple

from scipy.stats import norm


def multinomial_confidence_intervals(x: List[int], alpha: float = 0.05) -> List[Tuple[float, float]]:
    """
    Calculates confidence intervals for the probabilities of a multinomial distribution.

    Parameters:
        x (List[int]): List of counts for each category.
        alpha (float): Significance level for the confidence intervals, default is 0.05 for 95% confidence.

    Returns: List[Tuple[float, float]]: Each tuple contains the lower and upper bounds of the confidence interval for
    each probability.
    """
    n = sum(x)  # Total count
    z_alpha_half = norm.ppf(1 - alpha / 2)

    confidence_intervals: List[Tuple[float, float]] = []
    for count in x:
        p_hat = count / n  # MLE of probability
        margin_of_error = z_alpha_half / (2 * (n ** 0.5))

        lower_bound = max(p_hat - margin_of_error, 0)  # Ensure that probability is not negative
        upper_bound = min(p_hat + margin_of_error, 1)  # Ensure that probability does not exceed 1

        confidence_intervals.append((lower_bound, upper_bound))

    return confidence_intervals


# Example usage:
if __name__ == "__main__":
    counts = [100, 200, 700]  # Example counts for three categories
    risk = 0.05  # 95% confidence level
    results = multinomial_confidence_intervals(counts, risk)

    print("Confidence Intervals for each category:")
    for i, (lower, upper) in enumerate(results):
        print(f"Category {i + 1}: ({lower:.4f}, {upper:.4f})")

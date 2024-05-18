import numpy as np
from scipy.stats import norm


def multinomial_confidence_intervals(x: np.ndarray, alpha: float = 0.05) -> np.ndarray:
    """
    Calculates confidence intervals for the probabilities of a multinomial distribution using NumPy.

    Parameters:
        x (np.ndarray): Array of counts for each category.
        alpha (float): Significance level for the confidence intervals, default is 0.05 for 95% confidence.

    Returns: np.ndarray: Array where each row contains the lower and upper bounds of the confidence interval for each probability.
    """
    n = np.sum(x)  # Total count
    z_alpha_half = norm.ppf(1 - alpha / 2)

    # MLE of probability for each category
    p_hat = x / n

    # Margin of error for each category
    margin_of_error = z_alpha_half / (2 * np.sqrt(n))

    # Calculating lower and upper bounds ensuring bounds are within [0, 1]
    lower_bounds = np.maximum(p_hat - margin_of_error, 0)  # Ensure that probabilities are not negative
    upper_bounds = np.minimum(p_hat + margin_of_error, 1)  # Ensure that probabilities do not exceed 1

    # Combine lower and upper bounds into a single array of tuples
    confidence_intervals = np.column_stack((lower_bounds, upper_bounds))

    return confidence_intervals


# Example usage:
if __name__ == "__main__":
    counts = np.array([100, 200, 700])  # Example counts for three categories, as a NumPy array
    risk = 0.05  # 95% confidence level
    results = multinomial_confidence_intervals(counts, risk)

    print("Confidence Intervals for each category:")
    for i, (lower, upper) in enumerate(results):
        print(f"Category {i + 1}: ({lower:.4f}, {upper:.4f})")

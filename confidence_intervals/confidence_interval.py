from typing import Callable, Tuple

import scipy.stats as stats


def confidence_interval(p_hat: float, n: int, alpha: float = 0.05) -> Tuple[float, float]:
    """Calculates the confidence interval for a proportion p_hat with sample size N and significance level alpha."""
    z_alpha_half = stats.norm.ppf(1 - alpha / 2)
    margin_of_error = z_alpha_half / (2 * (n ** 0.5))

    lower_bound = p_hat - margin_of_error
    upper_bound = p_hat + margin_of_error

    return lower_bound, upper_bound


if __name__ == "__main__":
    # Example usage`
    confidence_interval_function: Callable[[float, int], Tuple[float, float]] = confidence_interval

    p_hat_example = 0.5  # Example sample proportion
    N_example = 100  # Example sample size
    alpha_example = 0.05  # Example significance level

    print(confidence_interval(p_hat_example, N_example, alpha_example))
    print(confidence_interval_function(p_hat_example, N_example))

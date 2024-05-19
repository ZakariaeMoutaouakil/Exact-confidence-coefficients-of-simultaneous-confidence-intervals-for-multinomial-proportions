from abc import ABC, abstractmethod
from typing import Tuple

import scipy.stats as stats


class BaseConfidenceIntervalCalculator(ABC):
    def __init__(self, alpha: float = 0.05):
        """
        Initializes the confidence interval calculator with a significance level alpha.
        """
        self.alpha = alpha
        self.__name__ = "BaseConfidenceIntervalCalculator"  # Assigning a name to the base class

    @abstractmethod
    def calculate(self, p_hat: float, n: int) -> Tuple[float, float]:
        """
        Abstract method to calculate the confidence interval for a proportion p_hat with sample size n.

        Parameters:
            p_hat (float): Sample proportion.
            n (int): Sample size.

        Returns:
            Tuple[float, float]: Lower and upper bounds of the confidence interval.
        """
        pass


class ConfidenceIntervalCalculator(BaseConfidenceIntervalCalculator):
    def __init__(self, alpha: float = 0.05):
        """
        Initializes the confidence interval calculator with a significance level alpha.
        """
        super().__init__(alpha)
        self.__name__ = "Fitzpatrick_and_Scott"  # Assigning a name to the derived class

    def calculate(self, p_hat: float, n: int) -> Tuple[float, float]:
        """
        Calculates the confidence interval for a proportion p_hat with sample size n.

        Parameters:
            p_hat (float): Sample proportion.
            n (int): Sample size.

        Returns:
            Tuple[float, float]: Lower and upper bounds of the confidence interval.
        """
        z_alpha_half = stats.norm.ppf(1 - self.alpha / 2)
        margin_of_error = z_alpha_half / (2 * (n ** 0.5))

        lower_bound = p_hat - margin_of_error
        upper_bound = p_hat + margin_of_error

        return lower_bound, upper_bound


if __name__ == "__main__":
    # Example usage
    ci_calculator = ConfidenceIntervalCalculator(alpha=0.05)

    p_hat_example = 0.5  # Example sample proportion
    N_example = 100  # Example sample size

    print(ci_calculator.calculate(p_hat_example, N_example))

    # If you need a callable for some reason
    confidence_interval_function = ci_calculator.calculate
    print(confidence_interval_function(p_hat_example, N_example))

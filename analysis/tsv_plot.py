import matplotlib.pyplot as plt
import pandas as pd

from confidence_intervals.confidence_interval import BaseConfidenceIntervalCalculator, ConfidenceIntervalCalculator


def plot_risks_vs_N(file_path: str, K: int, confidence_interval_function: BaseConfidenceIntervalCalculator):
    """
    Plots risks versus N for different conditions from a TSV file.

    Parameters:
        file_path (str): Path to the TSV file.
        K (int): Value of K to filter rows.
        confidence_interval_function (BaseConfidenceIntervalCalculator): Confidence interval function to use.
    """
    # Read the TSV file
    df = pd.read_csv(file_path, delimiter='\t')

    # Filter the DataFrame based on the provided parameters
    filtered_df = df[
        (df['K'] == K) &
        (df['Confidence Interval Function'] == confidence_interval_function.__name__) &
        (df['Confidence Interval Function Alpha'] == confidence_interval_function.alpha)
        ]

    # Extract unique conditions
    conditions = filtered_df['Condition'].unique()

    plt.figure(figsize=(10, 6))

    # Plot risks for each condition
    for condition in conditions:
        condition_df = filtered_df[filtered_df['Condition'] == condition].sort_values(by='N')
        plt.plot(condition_df['N'], condition_df['Risk'], marker='o', label=f'{condition}')

    # Setting the plot title and labels
    plt.title('Risks vs N for Different Conditions')
    plt.xlabel('N')
    plt.ylabel('Risk')
    plt.legend()
    plt.grid(True)

    # Show the plot
    plt.show()


if __name__ == '__main__':
    # Example usage
    file_path = 'analysis_results.tsv'  # Adjusted to correct path if necessary
    K = 3
    confidence_interval_function = ConfidenceIntervalCalculator()
    alpha = 0.05

    plot_risks_vs_N(file_path, K, confidence_interval_function)

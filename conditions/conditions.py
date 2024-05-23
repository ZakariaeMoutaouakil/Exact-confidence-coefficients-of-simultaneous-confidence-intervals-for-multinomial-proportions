# Check if the smallest probability is very small, near zero
import math
from typing import List


def min_prob_small(prob_vector: List[float], threshold: float = 0.01) -> bool:
    return min(prob_vector) < threshold


# Check if the entropy of the distribution is lower than for a uniform distribution
def entropy_lower_than_uniform(prob_vector: List[float], threshold: float = 0.1) -> bool:
    num_classes = len(prob_vector)
    if num_classes <= 1:
        return False
    uniform_entropy = math.log(num_classes)
    entropy = -sum(p * math.log(p) for p in prob_vector if p > 0)
    return uniform_entropy - entropy >= threshold


# Check if the vector is sparse: most probabilities are near zero
def sparsity(prob_vector: List[float], sparsity_threshold: float = 0.01, proportion: float = 0.8) -> bool:
    sparse_count = sum(1 for p in prob_vector if p < sparsity_threshold)
    return sparse_count / len(prob_vector) >= proportion


# Check if the highest probability significantly dominates the second highest
def decisiveness(prob_vector: List[float], dominance_ratio: float = 2.0) -> bool:
    sorted_probs = sorted(prob_vector, reverse=True)
    if len(sorted_probs) < 2:
        return True
    return sorted_probs[0] / sorted_probs[1] > dominance_ratio


# Check if the sum of probabilities for the top k categories is significantly higher than the others
def top_k_dominance(prob_vector: List[float], k: int = 2, dominance_threshold: float = 0.75) -> bool:
    sorted_probs = sorted(prob_vector, reverse=True)
    top_k_sum = sum(sorted_probs[:k])
    return top_k_sum / sum(sorted_probs) >= dominance_threshold


if __name__ == '__main__':
    # Example usage:
    example_vector = [0.9, 0.05, 0.03, 0.01, 0.01]

    # Checking the properties
    print("Min Probability Small:", min_prob_small(example_vector))
    print("Entropy Lower Than Uniform:", entropy_lower_than_uniform(example_vector))
    print("Sparsity:", sparsity(example_vector))

    # Example usage:
    example_vector = [0.4, 0.4, 0.2]

    # Checking the property with a threshold of 0.1
    print("Entropy Lower Than Uniform (Threshold 0.1):", entropy_lower_than_uniform(example_vector, threshold=0.1))

    # Checking the property with a threshold of 0.05
    print("Entropy Lower Than Uniform (Threshold 0.05):", entropy_lower_than_uniform(example_vector, threshold=0.05))

    # Example usage:
    example_vector = [0.8, 0.15, 0.04, 0.01]

    # Checking the properties
    print("Decisiveness:", decisiveness(example_vector))
    print("Top-k Dominance (k=2):", top_k_dominance(example_vector))

import numpy as np
from scipy.stats import gaussian_kde
from sklearn.decomposition import PCA


def learn_mass_function(probability_vectors, n_components=None):
    """
    Learns a continuous mass function defined on the simplex based on the given probability vectors.

    Parameters:
    probability_vectors (array-like): List or array of probability vectors.
    n_components (int, optional): Number of principal components to keep. If None, keep all components.

    Returns:
    function: A mass function that takes a probability vector and returns its mass.
    """
    # Ensure input is a numpy array
    probability_vectors = np.asarray(probability_vectors)

    # Perform PCA to reduce dimensionality
    pca = PCA(n_components=n_components)
    transformed_vectors = pca.fit_transform(probability_vectors)

    # Kernel Density Estimation on the transformed data
    kde = gaussian_kde(transformed_vectors.T)

    # Estimate the maximum density for normalization
    density_estimates = kde(transformed_vectors.T)
    max_density = np.max(density_estimates)

    # Define the mass function
    def mass_function(vector: np.ndarray) -> float:
        vector = np.asarray(vector)
        transformed_vector = pca.transform([vector])
        return kde(transformed_vector.T)[0] / max_density

    return mass_function


# Example usage
if __name__ == "__main__":
    # Example list of probability vectors
    vectors = [
        np.array([0.8, 0.15, 0.05]),  # Highest probability at index 0
        np.array([0.7, 0.2, 0.1]),  # Highest probability at index 0
        np.array([0.6, 0.35, 0.05]),  # Highest probability at index 0
        np.array([0.05, 0.9, 0.05]),  # Highest probability at index 1
        np.array([0.1, 0.8, 0.1]),  # Highest probability at index 1
        np.array([0.05, 0.6, 0.35]),  # Highest probability at index 1
        np.array([0.1, 0.1, 0.8]),  # Highest probability at index 2
        np.array([0.05, 0.05, 0.9]),  # Highest probability at index 2
        np.array([0.2, 0.1, 0.7])  # Highest probability at index 2
    ]

    # Learn the mass function with dimensionality reduction
    mass_function = learn_mass_function(vectors, n_components=2)  # Use one less than the dimension

    # Explicit test vectors
    test_vectors = [
        np.array([0.1, 0.1, 0.8]),  # Highest probability at index 2
        np.array([0.05, 0.05, 0.9]),  # Highest probability at index 2
        np.array([0.2, 0.1, 0.7])  # Highest probability at index 2
    ]

    # Test the mass function with the explicit test vectors
    for i, test_vector in enumerate(test_vectors):
        mass = mass_function(test_vector)
        print(f"Test Vector {i + 1}: {test_vector}")
        print(f"Normalized Mass: {mass}\n")

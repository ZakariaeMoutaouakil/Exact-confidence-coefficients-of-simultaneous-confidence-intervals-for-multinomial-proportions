import numpy as np


def transform_to_probability_vector(vector: np.ndarray, precision: int = 10) -> np.ndarray:
    """
    Transform a vector whose sum is less than 1 into a probability vector.
    This function appends an additional coordinate that equals 1 minus the sum of the existing coordinates,
    converting the vector into a valid probability vector if needed.

    Parameters:
    vector (np.ndarray): Input vector

    Returns:
    np.ndarray: Probability vector obtained by appending a coordinate equal to 1 minus the sum of the existing coordinates.
    """
    # Calculate the sum of the existing coordinates in the vector
    sum_of_coordinates = np.sum(vector)

    # Append the difference between 1 and the sum of existing coordinates to make it a probability vector
    appended_coordinate = np.round(1 - sum_of_coordinates, precision)  # rounding to ensure precision
    probability_vector = np.append(vector, appended_coordinate)  # append operation for numpy array
    return probability_vector


# Example usage
if __name__ == "__main__":
    # Example usage:
    input_vector = np.array([0.2, 0.3, 0.4])  # Example input vector converted to numpy array
    output_vector = transform_to_probability_vector(input_vector)
    print("Input Vector:", input_vector)
    print("Probability Vector:", output_vector)

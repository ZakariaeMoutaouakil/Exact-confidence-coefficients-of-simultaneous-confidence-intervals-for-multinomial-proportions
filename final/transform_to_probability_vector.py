from typing import List


def transform_to_probability_vector(vector: List[float], precision: int = 10):
    """
    Transform a vector whose sum is less than 1 into a probability vector.

    Parameters:
    vector (list): Input vector

    Returns:
    list: Probability vector obtained by appending a coordinate equal to 1 minus the sum of the existing coordinates.
    """
    # Calculate the sum of the existing coordinates in the vector
    sum_of_coordinates = sum(vector)

    # Append the difference between 1 and the sum of existing coordinates to make it a probability vector
    appended_coordinate = round(1 - sum_of_coordinates, precision)  # rounding to ensure precision
    probability_vector = vector + [appended_coordinate]
    return probability_vector


if __name__ == "__main__":
    # Example usage:
    input_vector = [0.2, 0.3, 0.4]  # Example input vector
    output_vector = transform_to_probability_vector(input_vector)
    print("Input Vector:", input_vector)
    print("Probability Vector:", output_vector)

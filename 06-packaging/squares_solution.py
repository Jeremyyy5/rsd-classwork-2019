"""Computation of weighted average of squares."""
import argparse
import math


def average_of_squares(list_of_numbers, list_of_weights=None):
    """
    Return the weighted average of a list of values.
    By default, all values are equally weighted, but this can be changed
    by the list_of_weights argument.
    Example:
    -------
    >>> average_of_squares([1, 2, 4])
    7.0
    >>> average_of_squares([2, 4], [1, 0.5])
    6.0
    >>> average_of_squares([1, 2, 4], [1, 0.5])
    Traceback (most recent call last):
    AssertionError: weights and numbers must have same length
    """
    if list_of_weights is not None:
        assert len(list_of_weights) == len(list_of_numbers), \
            "weights and numbers must have same length"
        effective_weights = list_of_weights
    else:
        effective_weights = [1] * len(list_of_numbers)
    squares = [
        weight * number * number
        for number, weight
        in zip(list_of_numbers, effective_weights)
    ]
    return sum(squares)


def convert_numbers(list_of_strings):
    """
    Convert a list of strings into numbers, ignoring whitespace.
    Example:
    -------
    >>> convert_numbers(["4", " 8 ", "15 16", " 23    42 "])
    [4, 8, 15, 16]
    """
    all_numbers = []
    for s in list_of_strings:
        # Take each string in the list, split it into substrings separated by
        # whitespace, and collect them into a single list...
        all_numbers.extend([token.strip() for token in s.split()])
    # ...then convert each substring into a number
    return [float(number_string) for number_string in all_numbers]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Weighted mean of squared numbers")
    parser.add_argument("numbers_file", help="the file containing the numbers")
    parser.add_argument("--weights", "-w", required=False, default=None,
                        help="the file containing the weights")
    parser.add_argument("--root", action="store_true",
                        help="compute the square root of the weighted average")
    parser.add_argument("--output", "-o", required=False, default=None,
                        help="the file to write the result in")
    arguments = parser.parse_args()
    # Read the numbers file (this must be done in every case)
    with open(arguments.numbers_file, "r") as numbers_file:
        numbers_strings = numbers_file.readlines()
    numbers = convert_numbers(numbers_strings)
    # Only use weights if the user has passed this option
    if arguments.weights:
        with open(arguments.weights, "r") as weights_file:
            weight_strings = weights_file.readlines()
            weights = convert_numbers(weight_strings)
    else:
        weights = None
    # Compute the result based on the above inputs
    result = average_of_squares(numbers, weights)
    # Take the square root if the user has specified that option
    final_result = math.sqrt(result) if arguments.root else result
    # Write the result to a file if requested...
    if arguments.output:
        with open(arguments.output, "w") as output_file:
            print(final_result, file=output_file)
    else:  # ...otherwise show it in the standard output
        print(final_result)

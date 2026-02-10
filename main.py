from sort import sort


def get_positive_number(prompt: str) -> float:
    """Prompt the user for a positive number, retrying on invalid input.

    Args:
        prompt: The message to display when requesting input.

    Returns:
        A positive float value entered by the user.
    """
    while True:
        try:
            value = float(input(prompt))
            if value > 0:
                return value
            print("Value must be positive.")
        except ValueError:
            print("Please enter a valid number.")

if __name__ == "__main__":
    width = get_positive_number("Enter width in cm: ")
    height = get_positive_number("Enter height in cm: ")
    length = get_positive_number("Enter length in cm: ")
    mass = get_positive_number("Enter mass in kg: ")
    
    result = sort(width, height, length, mass)
    
    print(f"\nLength: {length} cm \nWidth: {width} cm \nHeight: {height} cm \nMass: {mass} kg")
    print(f"The package is classified as: {result}")
"""Package classification module for robotic automation factory."""

# Classification thresholds
VOLUME_THRESHOLD = 1_000_000  # cm³
DIMENSION_THRESHOLD = 150  # cm
MASS_THRESHOLD = 20  # kg


def sort(width: float, height: float, length: float, mass: float) -> str:
    """Classify a package based on its dimensions and mass.

    A package is considered bulky if:
    - Its volume (width * height * length) >= 1,000,000 cm³, or
    - Any dimension >= 150 cm.

    A package is considered heavy if its mass >= 20 kg.

    Args:
        width: Package width in cm (must be positive).
        height: Package height in cm (must be positive).
        length: Package length in cm (must be positive).
        mass: Package mass in kg (must be positive).

    Returns:
        "REJECTED" if both bulky and heavy.
        "SPECIAL" if either bulky or heavy (but not both).
        "STANDARD" if neither bulky nor heavy.

    Raises:
        ValueError: If any dimension or mass is not positive.
    """
    if width <= 0 or height <= 0 or length <= 0 or mass <= 0:
        raise ValueError("All dimensions and mass must be positive values.")

    volume = width * height * length
    is_bulky = (
        volume >= VOLUME_THRESHOLD
        or width >= DIMENSION_THRESHOLD
        or height >= DIMENSION_THRESHOLD
        or length >= DIMENSION_THRESHOLD
    )
    is_heavy = mass >= MASS_THRESHOLD

    if is_bulky and is_heavy:
        return "REJECTED"
    elif is_bulky or is_heavy:
        return "SPECIAL"
    else:
        return "STANDARD"
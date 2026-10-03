import math

class AreaCalculator:
    def __init__(self, radius: float):
        """Initialize with a non‑negative radius."""
        if radius < 0:
            raise ValueError("Radius cannot be negative.")
        self._radius = radius

    def calculate_circle_area(self) -> float:
        """Area of a circle: π * r^2."""
        return math.pi * self._radius * self._radius

    def calculate_sphere_area(self) -> float:
        """Surface area of a sphere: 4 * π * r^2."""
        return 4 * math.pi * self._radius * self._radius

    def calculate_cylinder_area(self, height: float) -> float:
        """Surface area of a closed cylinder: 2 * π * r * (r + h)."""
        if height < 0:
            raise ValueError("Height cannot be negative.")
        return 2 * math.pi * self._radius * (self._radius + height)

    def calculate_sector_area(self, angle: float) -> float:
        """Area of a circular sector: 0.5 * r^2 * θ."""
        return 0.5 * self._radius * self._radius * angle

    def calculate_annulus_area(self, inner_radius: float, outer_radius: float) -> float:
        """Area of an annulus: π * (R^2 - r^2)."""
        if inner_radius > outer_radius:
            raise ValueError("Inner radius cannot be greater than outer radius.")
        return math.pi * (outer_radius * outer_radius - inner_radius * inner_radius)
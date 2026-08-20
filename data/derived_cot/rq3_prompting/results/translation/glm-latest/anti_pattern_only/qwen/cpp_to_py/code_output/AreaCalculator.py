import math


class AreaCalculator:
    def __init__(self, radius):
        if radius < 0:
            raise ValueError("Radius cannot be negative.")
        self._radius = radius

    def calculate_circle_area(self):
        return math.pi * self._radius * self._radius

    def calculate_sphere_area(self):
        return 4 * math.pi * self._radius * self._radius

    def calculate_cylinder_area(self, height):
        if height < 0:
            raise ValueError("Height cannot be negative.")
        return 2 * math.pi * self._radius * (self._radius + height)

    def calculate_sector_area(self, angle):
        return 0.5 * self._radius * self._radius * angle

    def calculate_annulus_area(self, inner_radius, outer_radius):
        if inner_radius > outer_radius:
            raise ValueError("Inner radius cannot be greater than outer radius.")
        return math.pi * (outer_radius * outer_radius - inner_radius * inner_radius)
import math

class AreaCalculator:
    def __init__(self, radius):
        if radius < 0:
            raise ValueError("Radius cannot be negative.")
        self.radius = radius

    def calculate_circle_area(self):
        return math.pi * self.radius ** 2

    def calculate_sphere_area(self):
        return 4 * math.pi * self.radius ** 2

    def calculate_cylinder_area(self, height):
        if height < 0:
            raise ValueError("Height cannot be negative.")
        return 2 * math.pi * self.radius * (self.radius + height)

    def calculate_sector_area(self, angle):
        return 0.5 * self.radius ** 2 * angle

    def calculate_annulus_area(self, inner_radius, outer_radius):
        if inner_radius > outer_radius:
            raise ValueError("Inner radius cannot be greater than outer radius.")
        return math.pi * (outer_radius ** 2 - inner_radius ** 2)
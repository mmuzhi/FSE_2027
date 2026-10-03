import math

class AreaCalculator:

    def __init__(self, radius: float):
        self.radius = radius

    def calculate_circle_area(self) -> float:
        return math.pi * self.radius ** 2

    def calculate_sphere_area(self) -> float:
        return 4 * math.pi * self.radius ** 2

    def calculate_cylinder_area(self, height: float) -> float:
        return 2 * math.pi * self.radius * (self.radius + height)

    def calculate_sector_area(self, angle: float) -> float:
        return self.radius ** 2 * angle / 2

    def calculate_annulus_area(self, inner_radius: float, outer_radius: float) -> float:
        return math.pi * (outer_radius ** 2 - inner_radius ** 2)

if __name__ == "__main__":
    area_calculator = AreaCalculator(2)

    print(f"Circle Area: {area_calculator.calculate_circle_area()}")
    print(f"Sphere Area: {area_calculator.calculate_sphere_area()}")
    print(f"Cylinder Area: {area_calculator.calculate_cylinder_area(3)}")
    print(f"Sector Area: {area_calculator.calculate_sector_area(math.pi)}")
    print(f"Annulus Area: {area_calculator.calculate_annulus_area(2, 3)}")
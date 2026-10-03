import math


class AreaCalculator:
    def __init__(self, radius: float) -> None:
        self.radius = radius

    def calculate_circle_area(self) -> float:
        return math.pi * math.pow(self.radius, 2)

    def calculate_sphere_area(self) -> float:
        return 4 * math.pi * math.pow(self.radius, 2)

    def calculate_cylinder_area(self, height: float) -> float:
        return 2 * math.pi * self.radius * (self.radius + height)

    def calculate_sector_area(self, angle: float) -> float:
        return math.pow(self.radius, 2) * angle / 2

    def calculate_annulus_area(self, inner_radius: float, outer_radius: float) -> float:
        return math.pi * (math.pow(outer_radius, 2) - math.pow(inner_radius, 2))


if __name__ == "__main__":
    area_calculator = AreaCalculator(2)

    print("Circle Area: " + str(area_calculator.calculate_circle_area()))
    print("Sphere Area: " + str(area_calculator.calculate_sphere_area()))
    print("Cylinder Area: " + str(area_calculator.calculate_cylinder_area(3)))
    print("Sector Area: " + str(area_calculator.calculate_sector_area(math.pi)))
    print("Annulus Area: " + str(area_calculator.calculate_annulus_area(2, 3)))
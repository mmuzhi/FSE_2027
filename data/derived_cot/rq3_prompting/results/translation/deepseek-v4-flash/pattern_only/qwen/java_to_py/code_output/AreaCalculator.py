import math

class AreaCalculator:
    def __init__(self, radius):
        self.radius = radius

    def calculateCircleArea(self):
        return math.pi * self.radius ** 2

    def calculateSphereArea(self):
        return 4 * math.pi * self.radius ** 2

    def calculateCylinderArea(self, height):
        return 2 * math.pi * self.radius * (self.radius + height)

    def calculateSectorArea(self, angle):
        return self.radius ** 2 * angle / 2

    def calculateAnnulusArea(self, innerRadius, outerRadius):
        return math.pi * (outerRadius ** 2 - innerRadius ** 2)

    @staticmethod
    def main(args=None):
        areaCalculator = AreaCalculator(2)

        print("Circle Area: " + str(areaCalculator.calculateCircleArea()))
        print("Sphere Area: " + str(areaCalculator.calculateSphereArea()))
        print("Cylinder Area: " + str(areaCalculator.calculateCylinderArea(3)))
        print("Sector Area: " + str(areaCalculator.calculateSectorArea(math.pi)))
        print("Annulus Area: " + str(areaCalculator.calculateAnnulusArea(2, 3)))

if __name__ == "__main__":
    AreaCalculator.main()
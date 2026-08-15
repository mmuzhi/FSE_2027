#include <iostream>
#include <cmath>

const double PI = 3.14159265358979323846;

class AreaCalculator {
private:
    double radius;

public:
    AreaCalculator(double radius) : radius(radius) {}

    double calculateCircleArea() const {
        return PI * std::pow(radius, 2.0);
    }

    double calculateSphereArea() const {
        return 4 * PI * std::pow(radius, 2.0);
    }

    double calculateCylinderArea(double height) const {
        return 2 * PI * radius * (radius + height);
    }

    double calculateSectorArea(double angle) const {
        return std::pow(radius, 2.0) * angle / 2.0;
    }

    double calculateAnnulusArea(double innerRadius, double outerRadius) const {
        return PI * (std::pow(outerRadius, 2.0) - std::pow(innerRadius, 2.0));
    }
};

int main() {
    AreaCalculator areaCalculator(2);

    std::cout << "Circle Area: " << areaCalculator.calculateCircleArea() << std::endl;
    std::cout << "Sphere Area: " << areaCalculator.calculateSphereArea() << std::endl;
    std::cout << "Cylinder Area: " << areaCalculator.calculateCylinderArea(3) << std::endl;
    std::cout << "Sector Area: " << areaCalculator.calculateSectorArea(PI) << std::endl;
    std::cout << "Annulus Area: " << areaCalculator.calculateAnnulusArea(2, 3) << std::endl;

    return 0;
}
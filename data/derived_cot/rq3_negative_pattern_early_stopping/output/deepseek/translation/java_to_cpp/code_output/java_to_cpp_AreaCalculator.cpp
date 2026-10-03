#include <iostream>
#include <cmath>

// Define π as precisely as possible using acos
const double PI = std::acos(-1.0);

class AreaCalculator {
private:
    double radius_;

public:
    // Constructor
    AreaCalculator(double radius) : radius_(radius) {}

    // Circle area: π * r^2
    double calculateCircleArea() const {
        return PI * std::pow(radius_, 2);
    }

    // Sphere area: 4 * π * r^2
    double calculateSphereArea() const {
        return 4 * PI * std::pow(radius_, 2);
    }

    // Cylinder area: 2 * π * r * (r + h)
    double calculateCylinderArea(double height) const {
        return 2 * PI * radius_ * (radius_ + height);
    }

    // Sector area: r^2 * θ / 2
    double calculateSectorArea(double angle) const {
        return std::pow(radius_, 2) * angle / 2.0;
    }

    // Annulus area: π * (R^2 - r^2)
    double calculateAnnulusArea(double innerRadius, double outerRadius) const {
        return PI * (std::pow(outerRadius, 2) - std::pow(innerRadius, 2));
    }
};

int main() {
    AreaCalculator areaCalculator(2.0);

    std::cout << "Circle Area: " << areaCalculator.calculateCircleArea() << std::endl;
    std::cout << "Sphere Area: " << areaCalculator.calculateSphereArea() << std::endl;
    std::cout << "Cylinder Area: " << areaCalculator.calculateCylinderArea(3.0) << std::endl;
    std::cout << "Sector Area: " << areaCalculator.calculateSectorArea(PI) << std::endl;
    std::cout << "Annulus Area: " << areaCalculator.calculateAnnulusArea(2.0, 3.0) << std::endl;

    return 0;
}
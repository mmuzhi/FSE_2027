#define _USE_MATH_DEFINES
#include <iostream>
#include <cmath>
#include <iomanip>
#include <limits>

class AreaCalculator {
private:
    double radius;

public:
    // Idiomatic C++: using a member initializer list
    AreaCalculator(double radius) : radius(radius) {}

    double calculateCircleArea() {
        return M_PI * std::pow(this->radius, 2);
    }

    double calculateSphereArea() {
        return 4 * M_PI * std::pow(this->radius, 2);
    }

    double calculateCylinderArea(double height) {
        return 2 * M_PI * this->radius * (this->radius + height);
    }

    double calculateSectorArea(double angle) {
        return std::pow(this->radius, 2) * angle / 2;
    }

    double calculateAnnulusArea(double innerRadius, double outerRadius) {
        return M_PI * (std::pow(outerRadius, 2) - std::pow(innerRadius, 2));
    }
};

int main() {
    AreaCalculator areaCalculator(2);

    // Set precision to match Java's Double.toString() output, which prints 
    // the minimum number of digits required to uniquely represent the double.
    std::cout << std::setprecision(std::numeric_limits<double>::max_digits10);

    std::cout << "Circle Area: " << areaCalculator.calculateCircleArea() << std::endl;
    std::cout << "Sphere Area: " << areaCalculator.calculateSphereArea() << std::endl;
    std::cout << "Cylinder Area: " << areaCalculator.calculateCylinderArea(3) << std::endl;
    std::cout << "Sector Area: " << areaCalculator.calculateSectorArea(M_PI) << std::endl;
    std::cout << "Annulus Area: " << areaCalculator.calculateAnnulusArea(2, 3) << std::endl;

    return 0;
}
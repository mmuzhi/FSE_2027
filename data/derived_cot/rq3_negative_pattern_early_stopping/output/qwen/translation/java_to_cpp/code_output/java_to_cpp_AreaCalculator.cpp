#include <iostream>
#include <cmath>

class AreaCalculator {
private:
    static const double PI;
    double radius;

public:
    AreaCalculator(double radius) : radius(radius) {}

    double calculateCircleArea() {
        return PI * std::pow(radius, 2);
    }

    double calculateSphereArea() {
        return 4 * PI * std::pow(radius, 2);
    }

    double calculateCylinderArea(double height) {
        return 2 * PI * radius * (radius + height);
    }

    double calculateSectorArea(double angle) {
        return std::pow(radius, 2) * angle / 2;
    }

    double calculateAnnulusArea(double innerRadius, double outerRadius) {
        return PI * (std::pow(outerRadius, 2) - std::pow(innerRadius, 2));
    }

    static void main() {
        AreaCalculator areaCalculator(2);

        std::cout << "Circle Area: " << areaCalculator.calculateCircleArea() << std::endl;
        std::cout << "Sphere Area: " << areaCalculator.calculateSphereArea() << std::endl;
        std::cout << "Cylinder Area: " << areaCalculator.calculateCylinderArea(3) << std::endl;
        std::cout << "Sector Area: " << areaCalculator.calculateSectorArea(M_PI) << std::endl;
        std::cout << "Annulus Area: " << areaCalculator.calculateAnnulusArea(2, 3) << std::endl;
    }
};

// Define the static member PI
const double AreaCalculator::PI = 3.14159265358979323846;

// Note: In C++, we don't have a main method in the class. We can define a main function in the global scope.
// But the problem says to keep behavior identical. The original Java code has a main method in the class.
// However, in C++, we can't have a main method in a class. We can either:
//   a) Define a global main function that uses the AreaCalculator::main method.
//   b) Or, define the main function outside the class.

// Let's define a global main function to run the example.
int main() {
    AreaCalculator::main();
    return 0;
}
#include <charconv>
#include <cmath>
#include <iostream>
#include <string>

namespace {
// Same value as Java's Math.PI (the double closest to pi)
constexpr double PI = 3.141592653589793;

// Reproduces Java's Double.toString(double): shortest decimal string that
// round-trips to the same double value.
std::string javaDouble(double value) {
    char buf[64];
    std::to_chars_result res = std::to_chars(buf, buf + sizeof(buf), value);
    return std::string(buf, res.ptr);
}
}  // namespace

class AreaCalculator {
private:
    double radius;

public:
    explicit AreaCalculator(double radius) : radius(radius) {}

    double calculateCircleArea() const {
        return PI * std::pow(this->radius, 2);
    }

    double calculateSphereArea() const {
        return 4 * PI * std::pow(this->radius, 2);
    }

    double calculateCylinderArea(double height) const {
        return 2 * PI * this->radius * (this->radius + height);
    }

    double calculateSectorArea(double angle) const {
        return std::pow(this->radius, 2) * angle / 2;
    }

    double calculateAnnulusArea(double innerRadius, double outerRadius) const {
        return PI * (std::pow(outerRadius, 2) - std::pow(innerRadius, 2));
    }
};

int main() {
    AreaCalculator areaCalculator(2);

    std::cout << "Circle Area: " << javaDouble(areaCalculator.calculateCircleArea()) << '\n';
    std::cout << "Sphere Area: " << javaDouble(areaCalculator.calculateSphereArea()) << '\n';
    std::cout << "Cylinder Area: " << javaDouble(areaCalculator.calculateCylinderArea(3)) << '\n';
    std::cout << "Sector Area: " << javaDouble(areaCalculator.calculateSectorArea(PI)) << '\n';
    std::cout << "Annulus Area: " << javaDouble(areaCalculator.calculateAnnulusArea(2, 3)) << '\n';
    return 0;
}
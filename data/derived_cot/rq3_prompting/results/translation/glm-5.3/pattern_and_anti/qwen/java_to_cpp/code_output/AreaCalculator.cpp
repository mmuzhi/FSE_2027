#include <charconv>
#include <cmath>
#include <iostream>
#include <string>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

class AreaCalculator {
private:
    double radius;

public:
    explicit AreaCalculator(double radius) : radius(radius) {}

    double calculateCircleArea() const {
        return M_PI * std::pow(this->radius, 2);
    }

    double calculateSphereArea() const {
        return 4 * M_PI * std::pow(this->radius, 2);
    }

    double calculateCylinderArea(double height) const {
        return 2 * M_PI * this->radius * (this->radius + height);
    }

    double calculateSectorArea(double angle) const {
        return std::pow(this->radius, 2) * angle / 2;
    }

    double calculateAnnulusArea(double innerRadius, double outerRadius) const {
        return M_PI * (std::pow(outerRadius, 2) - std::pow(innerRadius, 2));
    }
};

// Replicates Java's Double.toString (used by println(double)):
// shortest decimal string that round-trips to the same double.
static std::string javaToString(double value) {
    char buffer[64];
    const auto result = std::to_chars(buffer, buffer + sizeof(buffer), value);
    std::string s(buffer, result.ptr);

    if (s == "inf")  return "Infinity";
    if (s == "-inf") return "-Infinity";
    if (s == "nan" || s == "-nan") return "NaN";

    // Java always shows a fractional part in plain notation ("2.0", not "2").
    if (s.find_first_of(".e") == std::string::npos) {
        s += ".0";
    }
    return s;
}

int main() {
    AreaCalculator areaCalculator(2);

    std::cout << "Circle Area: " << javaToString(areaCalculator.calculateCircleArea()) << std::endl;
    std::cout << "Sphere Area: " << javaToString(areaCalculator.calculateSphereArea()) << std::endl;
    std::cout << "Cylinder Area: " << javaToString(areaCalculator.calculateCylinderArea(3)) << std::endl;
    std::cout << "Sector Area: " << javaToString(areaCalculator.calculateSectorArea(M_PI)) << std::endl;
    std::cout << "Annulus Area: " << javaToString(areaCalculator.calculateAnnulusArea(2, 3)) << std::endl;

    return 0;
}
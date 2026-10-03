#include <cmath>

class AreaCalculator {
private:
    double radius;
    static constexpr double pi = std::acos(-1.0);

public:
    explicit AreaCalculator(double radius) : radius(radius) {}

    double calculate_circle_area() const {
        return pi * radius * radius;
    }

    double calculate_sphere_area() const {
        return 4 * pi * radius * radius;
    }

    double calculate_cylinder_area(double height) const {
        return 2 * pi * radius * (radius + height);
    }

    double calculate_sector_area(double angle) const {
        return radius * radius * angle / 2;
    }

    double calculate_annulus_area(double inner_radius, double outer_radius) const {
        return pi * (outer_radius * outer_radius - inner_radius * inner_radius);
    }
};
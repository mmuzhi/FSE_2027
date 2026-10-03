#include <cmath>

class AreaCalculator {
private:
    double radius;
    // Python's math.pi is exactly 3.141592653589793
    static constexpr double PI = 3.141592653589793;

public:
    AreaCalculator(double radius) : radius(radius) {}

    double calculate_circle_area() const {
        return PI * (radius * radius);
    }

    double calculate_sphere_area() const {
        return 4 * PI * (radius * radius);
    }

    double calculate_cylinder_area(double height) const {
        return 2 * PI * radius * (radius + height);
    }

    double calculate_sector_area(double angle) const {
        return (radius * radius) * angle / 2;
    }

    double calculate_annulus_area(double inner_radius, double outer_radius) const {
        return PI * (outer_radius * outer_radius - inner_radius * inner_radius);
    }
};
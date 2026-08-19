#include <cmath>

// Python's math.pi is the double closest to pi; this literal is the same double.
static const double kPi = 3.141592653589793;

class AreaCalculator {
public:
    // Initialize the radius for shapes.
    explicit AreaCalculator(double radius) : radius_(radius) {}

    double calculate_circle_area() const {
        return kPi * radius_ * radius_;
    }

    double calculate_sphere_area() const {
        return 4 * kPi * radius_ * radius_;
    }

    double calculate_cylinder_area(double height) const {
        return 2 * kPi * radius_ * (radius_ + height);
    }

    double calculate_sector_area(double angle) const {
        return radius_ * radius_ * angle / 2;
    }

    double calculate_annulus_area(double inner_radius, double outer_radius) const {
        return kPi * (outer_radius * outer_radius - inner_radius * inner_radius);
    }

private:
    double radius_;
};
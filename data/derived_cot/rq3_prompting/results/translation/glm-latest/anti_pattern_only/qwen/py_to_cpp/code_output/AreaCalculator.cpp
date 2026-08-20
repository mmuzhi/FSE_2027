#include <cmath>

class AreaCalculator {
public:
    // Initialize the radius for shapes.
    // param radius: double
    explicit AreaCalculator(double radius) : radius(radius) {}

    // Calculate the area of circle based on this->radius.
    // return: area of circle, double
    double calculate_circle_area() const {
        return PI * radius * radius;
    }

    // Calculate the area of sphere based on this->radius.
    // return: area of sphere, double
    double calculate_sphere_area() const {
        return 4 * PI * radius * radius;
    }

    // Calculate the area of cylinder based on this->radius and height.
    // param height: height of cylinder, double
    // return: area of cylinder, double
    double calculate_cylinder_area(double height) const {
        return 2 * PI * radius * (radius + height);
    }

    // Calculate the area of sector based on this->radius and angle.
    // param angle: angle of sector, double
    // return: area of sector, double
    double calculate_sector_area(double angle) const {
        return radius * radius * angle / 2;
    }

    // Calculate the area of annulus based on inner_radius and outer_radius.
    // param inner_radius: inner radius of annulus, double
    // param outer_radius: outer radius of annulus, double
    // return: area of annulus, double
    double calculate_annulus_area(double inner_radius, double outer_radius) const {
        return PI * (outer_radius * outer_radius - inner_radius * inner_radius);
    }

private:
    double radius;
    static constexpr double PI = 3.14159265358979323846;  // same double value as Python's math.pi
};
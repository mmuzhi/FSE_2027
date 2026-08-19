#include <cmath>

class TriCalculator {
public:
    TriCalculator() {}

    // Calculate the cos value of the x-degree angle
    // >>> TriCalculator().cos(60) -> 0.5
    double cos(double x) {
        return round_n(taylor(x, 50), 10);
    }

    // Calculate the factorial of a
    // >>> TriCalculator().factorial(5) -> 120
    double factorial(int a) {
        double b = 1;
        while (a != 1) {
            b *= a;
            a -= 1;
        }
        return b;
    }

    // Finding the n-order Taylor expansion value of cos (x/180 * pi)
    // >>> TriCalculator().taylor(60, 50) -> 0.5000000000000001
    double taylor(double x, int n) {
        double a = 1;
        x = x / 180 * PI;
        int count = 1;
        for (int k = 1; k < n; k++) {
            if (count % 2 != 0) {
                a -= std::pow(x, 2 * k) / factorial(2 * k);
            } else {
                a += std::pow(x, 2 * k) / factorial(2 * k);
            }
            count += 1;
        }
        return a;
    }

    // Calculate the sin value of the x-degree angle
    // >>> TriCalculator().sin(30) -> 0.5
    double sin(double x) {
        x = x / 180 * PI;
        double g = 0;
        double t = x;
        int n = 1;
        while (std::fabs(t) >= 1e-15) {
            g += t;
            n += 1;
            t = -t * x * x / (2 * n - 1) / (2 * n - 2);
        }
        return round_n(g, 10);
    }

    // Calculate the tan value of the x-degree angle
    // >>> TriCalculator().tan(45) -> 1.0
    double tan(double x) {
        if (cos(x) != 0) {
            double result = sin(x) / cos(x);
            return round_n(result, 10);
        } else {
            return false;  // Python returns False; as a double this is 0.0
        }
    }

private:
    static constexpr double PI = 3.141592653589793;

    // Mimics Python's round(value, digits)
    static double round_n(double value, int digits) {
        double scale = std::pow(10.0, digits);
        return std::round(value * scale) / scale;
    }
};
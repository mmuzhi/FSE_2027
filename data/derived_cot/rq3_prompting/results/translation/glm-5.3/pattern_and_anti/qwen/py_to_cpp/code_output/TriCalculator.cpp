#include <cmath>

// Python's round(v, 10): rounds to 10 decimal places using
// round-half-even (the default FP rounding mode used by nearbyint).
static double round10(double v) {
    return std::nearbyint(v * 1e10) / 1e10;
}

static const double PY_PI = 3.14159265358979323846; // == math.pi (M_PI)

class TriCalculator {
public:
    TriCalculator() {}

    // Calculate the cos value of the x-degree angle
    // >>> tricalculator.cos(60) -> 0.5
    double cos(double x) {
        return round10(taylor(x, 50));
    }

    // Calculate the factorial of a
    // >>> tricalculator.factorial(5) -> 120
    // Python uses exact big integers; double is used here because the
    // results are only consumed by float division in taylor(), and the
    // final values are rounded to 10 decimals (differences are far below
    // that scale).
    double factorial(double a) {
        double b = 1;
        while (a != 1) {
            b *= a;
            a -= 1;
        }
        return b;
    }

    // Finding the n-order Taylor expansion value of cos (x/180 * pi)
    // >>> tricalculator.taylor(60, 50) -> 0.5000000000000001
    double taylor(double x, int n) {
        double a = 1;
        x = x / 180 * PY_PI; // true division, as in Python (x is double)
        int count = 1;
        for (int k = 1; k < n; ++k) {
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
    // >>> tricalculator.sin(30) -> 0.5
    double sin(double x) {
        x = x / 180 * PY_PI;
        double g = 0;
        double t = x;
        int n = 1;

        while (std::fabs(t) >= 1e-15) {
            g += t;
            n += 1;
            t = -t * x * x / (2 * n - 1) / (2 * n - 2);
        }
        return round10(g);
    }

    // Calculate the tan value of the x-degree angle
    // >>> tricalculator.tan(45) -> 1.0
    double tan(double x) {
        if (this->cos(x) != 0) {
            double result = this->sin(x) / this->cos(x);
            return round10(result);
        } else {
            // Python returns False (falsy, numerically equal to 0)
            return 0;
        }
    }
};
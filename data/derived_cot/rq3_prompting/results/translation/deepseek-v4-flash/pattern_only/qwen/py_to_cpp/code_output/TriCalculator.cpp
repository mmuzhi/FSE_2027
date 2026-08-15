#include <cmath>

class TriCalculator {
public:
    double cos(double x) {
        return py_round(taylor(x, 50), 10);
    }

    double factorial(int a) {
        double b = 1.0;
        while (a > 1) {
            b *= a;
            --a;
        }
        return b;
    }

    double taylor(double x, int n) {
        double a = 1.0;
        x = x / 180.0 * PI;
        int count = 1;
        for (int k = 1; k < n; ++k) {
            if (count % 2 != 0) {
                a -= std::pow(x, 2 * k) / factorial(2 * k);
            } else {
                a += std::pow(x, 2 * k) / factorial(2 * k);
            }
            ++count;
        }
        return a;
    }

    double sin(double x) {
        x = x / 180.0 * PI;
        double g = 0.0;
        double t = x;
        int n = 1;
        while (std::fabs(t) >= 1e-15) {
            g += t;
            ++n;
            t = -t * x * x / (2 * n - 1) / (2 * n - 2);
        }
        return py_round(g, 10);
    }

    double tan(double x) {
        double c = cos(x);
        if (c != 0.0) {
            double result = sin(x) / c;
            return py_round(result, 10);
        } else {
            return 0.0;
        }
    }

private:
    static double py_round(double value, int ndigits) {
        double p = std::pow(10.0, ndigits);
        return std::nearbyint(value * p) / p;
    }

    static constexpr double PI = 3.14159265358979323846;
};
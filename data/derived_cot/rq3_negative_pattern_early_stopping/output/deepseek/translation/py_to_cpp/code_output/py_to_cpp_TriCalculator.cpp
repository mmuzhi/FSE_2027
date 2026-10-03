#include <cmath>
#include <stdexcept>
#include <string>

class TriCalculator {
public:
    TriCalculator() {}

    double cos(double x) {
        double val = taylor(x, 50);
        // Round to 10 decimal places
        return std::round(val * 1e10) / 1e10;
    }

    long long factorial(int a) {
        long long b = 1;
        while (a != 1) {
            b *= a;
            --a;
        }
        return b;
    }

    double taylor(double x, int n) {
        double a = 1.0;
        x = x / 180.0 * M_PI;
        int count = 1;
        for (int k = 1; k < n; ++k) {
            double term = std::pow(x, 2 * k) / static_cast<double>(factorial(2 * k));
            if (count % 2 != 0) {
                a -= term;
            } else {
                a += term;
            }
            ++count;
        }
        return a;
    }

    double sin(double x) {
        x = x / 180.0 * M_PI;
        double g = 0.0;
        double t = x;
        int n = 1;
        while (std::abs(t) >= 1e-15) {
            g += t;
            ++n;
            t = -t * x * x / (2.0 * n - 1.0) / (2.0 * n - 2.0);
        }
        // Round to 10 decimal places
        return std::round(g * 1e10) / 1e10;
    }

    double tan(double x) {
        double c = cos(x);
        if (c != 0.0) {
            double s = sin(x);
            double result = s / c;
            return std::round(result * 1e10) / 1e10;
        } else {
            // Return NaN to indicate undefined (equivalent to Python False)
            return std::numeric_limits<double>::quiet_NaN();
        }
    }

private:
    static constexpr double M_PI = 3.14159265358979323846;
};
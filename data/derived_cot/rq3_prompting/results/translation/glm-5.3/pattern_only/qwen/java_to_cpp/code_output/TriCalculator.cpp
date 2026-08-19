#include <cmath>
#include <limits>
#include <stdexcept>

class TriCalculator {
public:
    TriCalculator() {}

    double cos(double x) {
        return round(taylor(x, 50), 10);
    }

    // Java returned BigDecimal; the value is carried as double here
    // (factorials up to 98! stay within double range)
    double factorial(int a) {
        double result = 1.0;
        while (a > 1) {
            result *= a;
            a--;
        }
        return result;
    }

    double taylor(double x, int n) {
        double a = 1.0;
        x = x / 180 * PI;
        int count = 1;
        for (int k = 1; k < n; k++) {
            double p = std::pow(x, 2 * k);
            // BigDecimal.valueOf(double) throws NumberFormatException on non-finite values
            if (!std::isfinite(p)) {
                throw std::invalid_argument("Infinite or NaN");
            }
            double term = p / factorial(2 * k);
            if (count % 2 != 0) {
                a = a - term;
            } else {
                a = a + term;
            }
            count++;
        }
        return a;
    }

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
        return round(g, 10);
    }

    double tan(double x) {
        double cosValue = cos(x);
        if (cosValue != 0) {
            return round(sin(x) / cosValue, 10);
        } else {
            return std::numeric_limits<double>::quiet_NaN();
        }
    }

private:
    static constexpr double PI = 3.14159265358979323846; // == Math.PI as a double

    double round(double value, int places) {
        double scale = std::pow(10.0, places);
        // std::round is half-away-from-zero, matching RoundingMode.HALF_UP;
        // "+ 0.0" normalizes -0.0 the way BigDecimal.doubleValue() does
        return std::round(value * scale) / scale + 0.0;
    }
};
#include <cmath>
#include <iostream>
#include <string>
#include <stdexcept>
#include <iomanip>
#include <sstream>
#include <cmath>
#include <limits>

class TriCalculator {

public:
    TriCalculator() {
    }

    double cos(double x) {
        return round(taylor(x, 50), 10);
    }

    double factorial(int a) {
        if (a < 0) {
            throw std::domain_error("Factorial is not defined for negative numbers");
        }
        double result = 1.0;
        for (int i = 2; i <= a; i++) {
            result *= i;
        }
        return result;
    }

    double taylor(double x, int n) {
        // Convert degrees to radians
        x = x * M_PI / 180.0;
        double a = 1.0;
        int count = 1;
        for (int k = 1; k < n; k++) {
            double term = std::pow(x, 2 * k) / factorial(2 * k);
            if (count % 2 != 0) {
                a -= term;
            } else {
                a += term;
            }
            count++;
        }
        return a;
    }

    double sin(double x) {
        x = x * M_PI / 180.0;
        double g = 0.0;
        double t = x;
        int n = 1;

        while (std::abs(t) >= 1e-15) {
            g += t;
            n += 1;
            t = -t * x * x / ((2 * n - 1) * (2 * n - 2));
        }
        return round(g, 10);
    }

    double tan(double x) {
        double cosValue = cos(x);
        if (std::abs(cosValue) < 1e-10) {
            return std::numeric_limits<double>::quiet_NaN();
        }
        return round(sin(x) / cosValue, 10);
    }

    double round(double value, int places) {
        if (places < 0) {
            throw std::domain_error("Negative number of decimal places not allowed");
        }
        double factor = std::pow(10.0, places);
        double temp = value * factor;
        double rounded = std::round(temp);
        return rounded / factor;
    }
};
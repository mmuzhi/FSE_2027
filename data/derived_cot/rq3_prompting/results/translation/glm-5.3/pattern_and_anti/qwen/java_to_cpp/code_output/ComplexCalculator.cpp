#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <string>

namespace org {
namespace example {

// Mimics Java's Double.toString so that toString()/output matches exactly
// (always at least one fractional digit, "E" notation outside [1e-3, 1e7), etc.)
static std::string javaDoubleToString(double value) {
    if (std::isnan(value)) return "NaN";
    if (std::isinf(value)) return value > 0 ? "Infinity" : "-Infinity";

    const bool neg = std::signbit(value);
    const std::string sign = neg ? "-" : "";

    // Shortest round-tripping scientific representation.
    char buf[64];
    for (int prec = 0; prec <= 17; ++prec) {
        std::snprintf(buf, sizeof(buf), "%.*e", prec, value);
        if (std::strtod(buf, nullptr) == value) break;
    }

    const char* p = buf;
    if (*p == '-') ++p;
    std::string digits(1, *p++);
    if (*p == '.') {
        ++p;
        while (*p != 'e' && *p != '\0') digits += *p++;
    }
    const int exp10 = std::atoi(p + 1);  // value = d1.d2... * 10^exp10
    const int k = static_cast<int>(digits.size());

    std::string out;
    if (exp10 >= -3 && exp10 < 7) {
        if (exp10 >= k - 1) {
            out = digits + std::string(exp10 - (k - 1), '0') + ".0";
        } else if (exp10 >= 0) {
            out = digits.substr(0, exp10 + 1) + "." + digits.substr(exp10 + 1);
        } else {
            out = "0." + std::string(-exp10 - 1, '0') + digits;
        }
    } else {
        out = digits.substr(0, 1) + "." + (k > 1 ? digits.substr(1) : std::string("0"));
        out += "E" + std::to_string(exp10);
    }
    return sign + out;
}

// Mimics Java's Double.compare(a, b) == 0: NaN equals NaN, -0.0 != 0.0.
static bool doubleEquals(double a, double b) {
    if (std::isnan(a) && std::isnan(b)) return true;
    return a == b && std::signbit(a) == std::signbit(b);
}

class ComplexCalculator {
public:
    class ComplexNumber {
    public:
        ComplexNumber(double real, double imaginary) : real(real), imaginary(imaginary) {}

        double getReal() const { return real; }
        double getImaginary() const { return imaginary; }

        bool equals(const ComplexNumber& other) const {
            if (this == &other) return true;
            return doubleEquals(other.real, real) && doubleEquals(other.imaginary, imaginary);
        }

        bool operator==(const ComplexNumber& other) const { return equals(other); }
        bool operator!=(const ComplexNumber& other) const { return !equals(other); }

        std::string toString() const {
            return javaDoubleToString(real) +
                   (imaginary >= 0 ? "+" : "") +
                   javaDoubleToString(imaginary) + "j";
        }

    private:
        double real;
        double imaginary;
    };

    ComplexNumber add(const ComplexNumber& c1, const ComplexNumber& c2) const {
        double real = c1.getReal() + c2.getReal();
        double imaginary = c1.getImaginary() + c2.getImaginary();
        return ComplexNumber(real, imaginary);
    }

    ComplexNumber subtract(const ComplexNumber& c1, const ComplexNumber& c2) const {
        double real = c1.getReal() - c2.getReal();
        double imaginary = c1.getImaginary() - c2.getImaginary();
        return ComplexNumber(real, imaginary);
    }

    ComplexNumber multiply(const ComplexNumber& c1, const ComplexNumber& c2) const {
        double real = c1.getReal() * c2.getReal() - c1.getImaginary() * c2.getImaginary();
        double imaginary = c1.getReal() * c2.getImaginary() + c1.getImaginary() * c2.getReal();
        return ComplexNumber(real, imaginary);
    }

    ComplexNumber divide(const ComplexNumber& c1, const ComplexNumber& c2) const {
        double denominator = c2.getReal() * c2.getReal() + c2.getImaginary() * c2.getImaginary();
        double real = (c1.getReal() * c2.getReal() + c1.getImaginary() * c2.getImaginary()) / denominator;
        double imaginary = (c1.getImaginary() * c2.getReal() - c1.getReal() * c2.getImaginary()) / denominator;
        return ComplexNumber(real, imaginary);
    }
};

}  // namespace example
}  // namespace org
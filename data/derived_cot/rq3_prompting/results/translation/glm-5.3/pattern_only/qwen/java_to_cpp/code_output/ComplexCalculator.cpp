#include <algorithm>
#include <charconv>
#include <cmath>
#include <cstdint>
#include <cstring>
#include <string>

namespace org {
namespace example {
namespace detail {

// Mimics java.lang.Double.compare: NaN > everything (NaN == NaN), +0.0 < -0.0.
inline int doubleCompare(double a, double b) {
    if (std::isnan(a)) return std::isnan(b) ? 0 : 1;
    if (std::isnan(b)) return -1;
    if (a == b) {
        std::int64_t abits, bbits;
        std::memcpy(&abits, &a, sizeof(abits));
        std::memcpy(&bbits, &b, sizeof(bbits));
        if (abits == bbits) return 0;
        return abits == 0 ? -1 : 1;  // +0.0 sorts before -0.0
    }
    return a < b ? -1 : 1;
}

// Mimics java.lang.Double.toString: shortest round-trip digits; plain decimal
// form iff 1e-3 <= |v| < 1e7; at least one fraction digit; "E" exponent form
// otherwise; NaN / Infinity / -Infinity spellings.
inline std::string javaDoubleToString(double value) {
    if (std::isnan(value)) return "NaN";
    if (std::isinf(value)) return value > 0 ? "Infinity" : "-Infinity";
    if (value == 0.0) return std::signbit(value) ? "-0.0" : "0.0";

    const bool negative = value < 0;
    const double mag = negative ? -value : value;

    char buf[64];
    auto res = std::to_chars(buf, buf + sizeof(buf), mag, std::chars_format::scientific);
    std::string sci(buf, res.ptr);

    const std::size_t epos = sci.find('e');
    std::string digits = sci.substr(0, epos);
    digits.erase(std::remove(digits.begin(), digits.end(), '.'), digits.end());
    const int e = std::stoi(sci.substr(epos + 1));
    const int n = static_cast<int>(digits.size());

    std::string out;
    if (e >= -3 && e < 7) {
        if (e >= n - 1) {
            out = digits + std::string(e - (n - 1), '0') + ".0";
        } else if (e >= 0) {
            out = digits.substr(0, e + 1) + "." + digits.substr(e + 1);
        } else {
            out = "0." + std::string(-e - 1, '0') + digits;
        }
    } else {
        out = digits.substr(0, 1) + "." + (n > 1 ? digits.substr(1) : "0")
            + "E" + std::to_string(e);
    }
    return negative ? "-" + out : out;
}

}  // namespace detail

class ComplexCalculator {
public:
    class ComplexNumber {
    private:
        double real;
        double imaginary;

    public:
        ComplexNumber(double real, double imaginary) : real(real), imaginary(imaginary) {}

        double getReal() const { return real; }
        double getImaginary() const { return imaginary; }

        bool equals(const ComplexNumber& obj) const {
            return detail::doubleCompare(obj.real, real) == 0
                && detail::doubleCompare(obj.imaginary, imaginary) == 0;
        }

        bool operator==(const ComplexNumber& other) const { return equals(other); }
        bool operator!=(const ComplexNumber& other) const { return !equals(other); }

        std::string toString() const {
            return detail::javaDoubleToString(real)
                 + (imaginary >= 0 ? "+" : "")
                 + detail::javaDoubleToString(imaginary)
                 + "j";
        }
    };

    ComplexNumber add(const ComplexNumber& c1, const ComplexNumber& c2) {
        double real = c1.getReal() + c2.getReal();
        double imaginary = c1.getImaginary() + c2.getImaginary();
        return ComplexNumber(real, imaginary);
    }

    ComplexNumber subtract(const ComplexNumber& c1, const ComplexNumber& c2) {
        double real = c1.getReal() - c2.getReal();
        double imaginary = c1.getImaginary() - c2.getImaginary();
        return ComplexNumber(real, imaginary);
    }

    ComplexNumber multiply(const ComplexNumber& c1, const ComplexNumber& c2) {
        double real = c1.getReal() * c2.getReal() - c1.getImaginary() * c2.getImaginary();
        double imaginary = c1.getReal() * c2.getImaginary() + c1.getImaginary() * c2.getReal();
        return ComplexNumber(real, imaginary);
    }

    ComplexNumber divide(const ComplexNumber& c1, const ComplexNumber& c2) {
        double denominator = c2.getReal() * c2.getReal() + c2.getImaginary() * c2.getImaginary();
        double real = (c1.getReal() * c2.getReal() + c1.getImaginary() * c2.getImaginary()) / denominator;
        double imaginary = (c1.getImaginary() * c2.getReal() - c1.getReal() * c2.getImaginary()) / denominator;
        return ComplexNumber(real, imaginary);
    }
};

}  // namespace example
}  // namespace org
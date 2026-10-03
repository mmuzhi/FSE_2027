#include <cmath>
#include <string>
#include <cstdio>

class ComplexCalculator {
public:
    class ComplexNumber {
    private:
        double real;
        double imaginary;

        static bool double_equals(double d1, double d2) {
            if (std::isnan(d1) && std::isnan(d2)) return true;
            if (d1 == d2) {
                if (d1 == 0.0) return std::signbit(d1) == std::signbit(d2);
                return true;
            }
            return false;
        }

        static std::string double_to_string(double d) {
            if (std::isnan(d)) return "NaN";
            if (std::isinf(d)) return d > 0 ? "Infinity" : "-Infinity";
            if (d == 0.0) {
                if (std::signbit(d)) return "-0.0";
                return "0.0";
            }
            char buf[32];
            std::snprintf(buf, sizeof(buf), "%.17g", d);
            std::string s = buf;
            
            size_t e_pos = s.find('e');
            if (e_pos != std::string::npos) {
                s[e_pos] = 'E';
                if (e_pos + 1 < s.length() && s[e_pos + 1] == '+') {
                    s.erase(e_pos + 1, 1);
                }
            }

            if (s.find('.') == std::string::npos && s.find('E') == std::string::npos) {
                s += ".0";
            }
            return s;
        }

    public:
        ComplexNumber(double real, double imaginary) : real(real), imaginary(imaginary) {}

        double getReal() const {
            return real;
        }

        double getImaginary() const {
            return imaginary;
        }

        bool equals(const ComplexNumber& that) const {
            return double_equals(that.real, real) && double_equals(that.imaginary, imaginary);
        }

        bool operator==(const ComplexNumber& that) const {
            return equals(that);
        }

        std::string toString() const {
            return double_to_string(real) + (imaginary >= 0 ? "+" : "") + double_to_string(imaginary) + "j";
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
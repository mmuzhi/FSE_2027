#include <cmath>
#include <iostream>
#include <string>

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

        bool operator==(const ComplexNumber& other) const {
            // Mimic Java's Double.compare semantics exactly
            auto doubleEqual = [](double a, double b) -> bool {
                // Both NaN: equal
                if (std::isnan(a) && std::isnan(b)) return true;
                // One NaN: not equal
                if (std::isnan(a) || std::isnan(b)) return false;
                // Handle signed zero: treat -0.0 and 0.0 as different
                if (a == 0.0 && b == 0.0) {
                    return std::signbit(a) == std::signbit(b);
                }
                return a == b;
            };
            return doubleEqual(real, other.real) && doubleEqual(imaginary, other.imaginary);
        }

        bool operator!=(const ComplexNumber& other) const {
            return !(*this == other);
        }

        std::string toString() const {
            std::string result = std::to_string(real);
            if (imaginary >= 0) {
                result += "+";
            }
            result += std::to_string(imaginary) + "j";
            return result;
        }

        friend std::ostream& operator<<(std::ostream& os, const ComplexNumber& c) {
            os << c.toString();
            return os;
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
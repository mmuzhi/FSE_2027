#include <complex>
#include <stdexcept>
#include <string>

// Equivalent of Python's ZeroDivisionError, raised when dividing by a
// complex number whose real and imaginary parts are both zero.
class ZeroDivisionError : public std::runtime_error {
public:
    explicit ZeroDivisionError(const std::string& message)
        : std::runtime_error(message) {}
};

// This is a class that implements addition, subtraction, multiplication,
// and division operations for complex numbers.
class ComplexCalculator {
public:
    ComplexCalculator() = default;

    // Adds two complex numbers.
    static std::complex<double> add(const std::complex<double>& c1,
                                    const std::complex<double>& c2) {
        double real = c1.real() + c2.real();
        double imaginary = c1.imag() + c2.imag();
        std::complex<double> answer(real, imaginary);
        return answer;
    }

    // Subtracts two complex numbers.
    static std::complex<double> subtract(const std::complex<double>& c1,
                                         const std::complex<double>& c2) {
        double real = c1.real() - c2.real();
        double imaginary = c1.imag() - c2.imag();
        return std::complex<double>(real, imaginary);
    }

    // Multiplies two complex numbers.
    static std::complex<double> multiply(const std::complex<double>& c1,
                                         const std::complex<double>& c2) {
        double real = c1.real() * c2.real() - c1.imag() * c2.imag();
        double imaginary = c1.real() * c2.imag() + c1.imag() * c2.real();
        return std::complex<double>(real, imaginary);
    }

    // Divides two complex numbers.
    static std::complex<double> divide(const std::complex<double>& c1,
                                       const std::complex<double>& c2) {
        double denominator = c2.real() * c2.real() + c2.imag() * c2.imag();
        if (denominator == 0.0) {
            // Python raises ZeroDivisionError ("float division by zero")
            // instead of producing inf/nan; mirror that behavior.
            throw ZeroDivisionError("float division by zero");
        }
        double real =
            (c1.real() * c2.real() + c1.imag() * c2.imag()) / denominator;
        double imaginary =
            (c1.imag() * c2.real() - c1.real() * c2.imag()) / denominator;
        return std::complex<double>(real, imaginary);
    }
};
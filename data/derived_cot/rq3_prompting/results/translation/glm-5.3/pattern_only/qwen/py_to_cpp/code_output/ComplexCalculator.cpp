#include <complex>
#include <stdexcept>

class ComplexCalculator {
public:
    ComplexCalculator() {}

    static std::complex<double> add(const std::complex<double>& c1, const std::complex<double>& c2) {
        double real = c1.real() + c2.real();
        double imaginary = c1.imag() + c2.imag();
        return std::complex<double>(real, imaginary);
    }

    static std::complex<double> subtract(const std::complex<double>& c1, const std::complex<double>& c2) {
        double real = c1.real() - c2.real();
        double imaginary = c1.imag() - c2.imag();
        return std::complex<double>(real, imaginary);
    }

    static std::complex<double> multiply(const std::complex<double>& c1, const std::complex<double>& c2) {
        double real = c1.real() * c2.real() - c1.imag() * c2.imag();
        double imaginary = c1.real() * c2.imag() + c1.imag() * c2.real();
        return std::complex<double>(real, imaginary);
    }

    static std::complex<double> divide(const std::complex<double>& c1, const std::complex<double>& c2) {
        double denominator = c2.real() * c2.real() + c2.imag() * c2.imag();
        // Python raises ZeroDivisionError when dividing by 0+0j; preserve that behavior.
        if (denominator == 0.0) {
            throw std::runtime_error("complex division by zero");
        }
        double real = (c1.real() * c2.real() + c1.imag() * c2.imag()) / denominator;
        double imaginary = (c1.imag() * c2.real() - c1.real() * c2.imag()) / denominator;
        return std::complex<double>(real, imaginary);
    }
};
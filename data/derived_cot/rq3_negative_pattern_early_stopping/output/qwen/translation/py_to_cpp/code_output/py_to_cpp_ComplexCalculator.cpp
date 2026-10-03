#include <complex>
#include <stdexcept>

class ComplexCalculator {
public:
    static std::complex<double> add(const std::complex<double>& c1, const std::complex<double>& c2) {
        return c1 + c2;
    }

    static std::complex<double> subtract(const std::complex<double>& c1, const std::complex<double>& c2) {
        return c1 - c2;
    }

    static std::complex<double> multiply(const std::complex<double>& c1, const std::complex<double>& c2) {
        return c1 * c2;
    }

    static std::complex<double> divide(const std::complex<double>& c1, const std::complex<double>& c2) {
        double denominator = c2.real() * c2.real() + c2.imag() * c2.imag();
        if (denominator == 0) {
            throw std::runtime_error("Division by zero");
        }
        double real = (c1.real() * c2.real() + c1.imag() * c2.imag()) / denominator;
        double imag = (c1.imag() * c2.real() - c1.real() * c2.imag()) / denominator;
        return std::complex<double>(real, imag);
    }
};
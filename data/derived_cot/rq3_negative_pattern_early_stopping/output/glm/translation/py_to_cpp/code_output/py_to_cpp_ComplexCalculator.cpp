#include <complex>

class ComplexCalculator {
public:
    ComplexCalculator() {}

    static std::complex<double> add(std::complex<double> c1, std::complex<double> c2) {
        double real = c1.real() + c2.real();
        double imaginary = c1.imag() + c2.imag();
        std::complex<double> answer(real, imaginary);
        return answer;
    }

    static std::complex<double> subtract(std::complex<double> c1, std::complex<double> c2) {
        double real = c1.real() - c2.real();
        double imaginary = c1.imag() - c2.imag();
        return std::complex<double>(real, imaginary);
    }

    static std::complex<double> multiply(std::complex<double> c1, std::complex<double> c2) {
        double real = c1.real() * c2.real() - c1.imag() * c2.imag();
        double imaginary = c1.real() * c2.imag() + c1.imag() * c2.real();
        return std::complex<double>(real, imaginary);
    }

    static std::complex<double> divide(std::complex<double> c1, std::complex<double> c2) {
        double denominator = c2.real() * c2.real() + c2.imag() * c2.imag();
        double real = (c1.real() * c2.real() + c1.imag() * c2.imag()) / denominator;
        double imaginary = (c1.imag() * c2.real() - c1.real() * c2.imag()) / denominator;
        return std::complex<double>(real, imaginary);
    }
};
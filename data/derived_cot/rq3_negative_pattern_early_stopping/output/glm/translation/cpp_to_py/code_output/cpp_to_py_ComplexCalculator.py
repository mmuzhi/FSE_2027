class ComplexCalculator:
    @staticmethod
    def add(c1: complex, c2: complex) -> complex:
        real = c1.real + c2.real
        imaginary = c1.imag + c2.imag
        return complex(real, imaginary)

    @staticmethod
    def subtract(c1: complex, c2: complex) -> complex:
        real = c1.real - c2.real
        imaginary = c1.imag - c2.imag
        return complex(real, imaginary)

    @staticmethod
    def multiply(c1: complex, c2: complex) -> complex:
        real = c1.real * c2.real - c1.imag * c2.imag
        imaginary = c1.real * c2.imag + c1.imag * c2.real
        return complex(real, imaginary)

    @staticmethod
    def divide(c1: complex, c2: complex) -> complex:
        denominator = c2.real * c2.real + c2.imag * c2.imag
        real = (c1.real * c2.real + c1.imag * c2.imag) / denominator
        imaginary = (c1.imag * c2.real - c1.real * c2.imag) / denominator
        return complex(real, imaginary)
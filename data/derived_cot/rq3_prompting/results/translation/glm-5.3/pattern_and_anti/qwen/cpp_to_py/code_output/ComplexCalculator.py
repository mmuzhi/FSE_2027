import math


def _ieee_div(n: float, d: float) -> float:
    # Emulate C++ double division: unlike Python, x / 0.0 does not raise,
    # it yields +/-inf (nonzero numerator) or nan (zero / NaN numerator).
    if d != 0.0:
        return n / d
    # d is 0.0 (d = a*a + b*b is never negative for finite doubles)
    if math.isnan(n) or n == 0.0:
        return math.nan
    return math.copysign(math.inf, n)


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
        real = _ieee_div(c1.real * c2.real + c1.imag * c2.imag, denominator)
        imaginary = _ieee_div(c1.imag * c2.real - c1.real * c2.imag, denominator)
        return complex(real, imaginary)
import math


def _ieee_divide(numerator: float, denominator: float) -> float:
    # C++ (IEEE 754) float division never throws: x/0.0 yields +/-inf,
    # while 0/0 and nan/0 yield NaN. Python raises ZeroDivisionError for a
    # zero denominator, so reproduce the C++ semantics here.
    try:
        return numerator / denominator
    except ZeroDivisionError:
        if math.isnan(numerator) or numerator == 0.0:
            return float("nan")
        sign = math.copysign(1.0, numerator) * math.copysign(1.0, denominator)
        return math.copysign(float("inf"), sign)


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
        real = _ieee_divide(c1.real * c2.real + c1.imag * c2.imag, denominator)
        imaginary = _ieee_divide(c1.imag * c2.real - c1.real * c2.imag, denominator)
        return complex(real, imaginary)
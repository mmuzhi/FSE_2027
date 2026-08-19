import math
import struct


def _double_bits(x):
    return struct.unpack(">Q", struct.pack(">d", x))[0]


def _double_compare(a, b):
    # Mimics java.lang.Double.compare: NaN == NaN, -0.0 < +0.0 (bit order)
    if a < b:
        return -1
    if a > b:
        return 1
    a_bits, b_bits = _double_bits(a), _double_bits(b)
    return 0 if a_bits == b_bits else (1 if a_bits > b_bits else -1)


def _java_double_str(value):
    # Mimics java.lang.Double.toString
    if math.isnan(value):
        return "NaN"
    if math.isinf(value):
        return "Infinity" if value > 0 else "-Infinity"
    if value == 0.0:
        return "-0.0" if math.copysign(1.0, value) < 0 else "0.0"
    s = repr(value)
    neg = s.startswith("-")
    if neg:
        s = s[1:]
    if "e" in s:
        mantissa, _, exp_part = s.partition("e")
        exp = int(exp_part)
    else:
        mantissa, exp = s, 0
    if "." in mantissa:
        int_part, frac_part = mantissa.split(".")
    else:
        int_part, frac_part = mantissa, ""
    all_digits = int_part + frac_part
    point = len(int_part) + exp  # digit count before the decimal point
    stripped = all_digits.lstrip("0")
    point -= len(all_digits) - len(stripped)
    digits = stripped.rstrip("0")  # value = 0.<digits> * 10**point
    sign = "-" if neg else ""
    if -2 <= point <= 7:  # 10^-3 <= |value| < 10^7 -> plain decimal
        if point <= 0:
            return sign + "0." + "0" * (-point) + digits
        if point >= len(digits):
            return sign + digits + "0" * (point - len(digits)) + ".0"
        return sign + digits[:point] + "." + digits[point:]
    return sign + digits[0] + "." + (digits[1:] or "0") + "E" + str(point - 1)


class ComplexCalculator:

    class ComplexNumber:
        __hash__ = object.__hash__  # Java keeps default identity hashCode

        def __init__(self, real, imaginary):
            self.real = real
            self.imaginary = imaginary

        def get_real(self):
            return self.real

        def get_imaginary(self):
            return self.imaginary

        def __eq__(self, other):
            if self is other:
                return True
            if type(other) is not ComplexCalculator.ComplexNumber:  # exact class, like getClass()
                return False
            return (_double_compare(other.real, self.real) == 0
                    and _double_compare(other.imaginary, self.imaginary) == 0)

        def __str__(self):
            return (_java_double_str(self.real)
                    + ("+" if self.imaginary >= 0 else "")
                    + _java_double_str(self.imaginary) + "j")

        __repr__ = __str__

    def add(self, c1, c2):
        real = c1.get_real() + c2.get_real()
        imaginary = c1.get_imaginary() + c2.get_imaginary()
        return ComplexCalculator.ComplexNumber(real, imaginary)

    def subtract(self, c1, c2):
        real = c1.get_real() - c2.get_real()
        imaginary = c1.get_imaginary() - c2.get_imaginary()
        return ComplexCalculator.ComplexNumber(real, imaginary)

    def multiply(self, c1, c2):
        real = c1.get_real() * c2.get_real() - c1.get_imaginary() * c2.get_imaginary()
        imaginary = c1.get_real() * c2.get_imaginary() + c1.get_imaginary() * c2.get_real()
        return ComplexCalculator.ComplexNumber(real, imaginary)

    def divide(self, c1, c2):
        denominator = c2.get_real() * c2.get_real() + c2.get_imaginary() * c2.get_imaginary()
        real = (c1.get_real() * c2.get_real() + c1.get_imaginary() * c2.get_imaginary()) / denominator
        imaginary = (c1.get_imaginary() * c2.get_real() - c1.get_real() * c2.get_imaginary()) / denominator
        return ComplexCalculator.ComplexNumber(real, imaginary)
import math


def _java_double_to_string(x):
    if math.isnan(x):
        return "NaN"
    if math.isinf(x):
        return "Infinity" if x > 0 else "-Infinity"
    if x == 0.0:
        return "-0.0" if math.copysign(1.0, x) < 0 else "0.0"

    sign = "-" if x < 0 else ""
    ax = abs(x)
    s = repr(ax)

    if 'e' in s or 'E' in s:
        mantissa, exp_str = s.replace('E', 'e').split('e')
        exp = int(exp_str)
        if '.' in mantissa:
            int_part, frac_part = mantissa.split('.')
            digits = int_part + frac_part
            exp_first = exp
        else:
            digits = mantissa
            exp_first = exp

        if len(digits) == 1:
            mantissa_java = digits + ".0"
        else:
            mantissa_java = digits[0] + "." + digits[1:]
        return sign + mantissa_java + "E" + str(exp_first)

    digits, exp_first = _parse_fixed(s)

    if ax >= 1e7 or ax < 1e-3:
        if len(digits) == 1:
            mantissa_java = digits + ".0"
        else:
            mantissa_java = digits[0] + "." + digits[1:]
        return sign + mantissa_java + "E" + str(exp_first)

    decimal_pos = exp_first + 1
    if decimal_pos >= len(digits):
        integer_str = digits + '0' * (decimal_pos - len(digits))
        return sign + integer_str + ".0"
    elif decimal_pos <= 0:
        zeros = '0' * (-decimal_pos)
        return sign + "0." + zeros + digits
    else:
        return sign + digits[:decimal_pos] + "." + digits[decimal_pos:]


def _parse_fixed(s):
    if '.' in s:
        int_part, frac_part = s.split('.')
    else:
        int_part, frac_part = s, ''

    full = int_part + frac_part
    stripped = full.lstrip('0').rstrip('0')
    if not stripped:
        return '0', 0

    if int_part.lstrip('0') != '':
        exp_first = len(int_part) - 1
    else:
        idx = 0
        while idx < len(frac_part) and frac_part[idx] == '0':
            idx += 1
        exp_first = -(idx + 1)

    return stripped, exp_first


def _java_div(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        if math.isnan(a):
            return float('nan')
        if a == 0.0:
            return float('nan')
        sign = math.copysign(1.0, a) * math.copysign(1.0, b)
        return sign * float('inf')


def _double_equals(a, b):
    return a == b or (math.isnan(a) and math.isnan(b))


class ComplexNumber:
    def __init__(self, real, imaginary):
        self._real = real
        self._imaginary = imaginary

    def getReal(self):
        return self._real

    def getImaginary(self):
        return self._imaginary

    def __eq__(self, other):
        if self is other:
            return True
        if other is None or type(other) is not type(self):
            return False
        return _double_equals(self._real, other._real) and _double_equals(self._imaginary, other._imaginary)

    __hash__ = object.__hash__

    def __str__(self):
        return (_java_double_to_string(self._real)
                + ("+" if self._imaginary >= 0 else "")
                + _java_double_to_string(self._imaginary)
                + "j")


class ComplexCalculator:
    ComplexNumber = ComplexNumber

    def add(self, c1, c2):
        return ComplexNumber(c1.getReal() + c2.getReal(),
                             c1.getImaginary() + c2.getImaginary())

    def subtract(self, c1, c2):
        return ComplexNumber(c1.getReal() - c2.getReal(),
                             c1.getImaginary() - c2.getImaginary())

    def multiply(self, c1, c2):
        real = c1.getReal() * c2.getReal() - c1.getImaginary() * c2.getImaginary()
        imaginary = c1.getReal() * c2.getImaginary() + c1.getImaginary() * c2.getReal()
        return ComplexNumber(real, imaginary)

    def divide(self, c1, c2):
        denominator = c2.getReal() * c2.getReal() + c2.getImaginary() * c2.getImaginary()
        real = _java_div(c1.getReal() * c2.getReal() + c1.getImaginary() * c2.getImaginary(), denominator)
        imaginary = _java_div(c1.getImaginary() * c2.getReal() - c1.getReal() * c2.getImaginary(), denominator)
        return ComplexNumber(real, imaginary)
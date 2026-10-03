import math

def double_compare(d1, d2):
    if math.isnan(d1) and math.isnan(d2):
        return 0
    if math.isnan(d1):
        return 1
    if math.isnan(d2):
        return -1
    if d1 == 0.0 and d2 == 0.0:
        s1 = math.copysign(1.0, d1)
        s2 = math.copysign(1.0, d2)
        if s1 > s2: return 1
        if s1 < s2: return -1
        return 0
    if d1 < d2: return -1
    if d1 > d2: return 1
    return 0

def java_float_div(num, den):
    if math.isnan(num) or math.isnan(den):
        return float('nan')
    try:
        return num / den
    except ZeroDivisionError:
        if num == 0.0:
            return float('nan')
        sign = math.copysign(1.0, num) * math.copysign(1.0, den)
        if sign > 0:
            return float('inf')
        else:
            return float('-inf')

def java_double_to_string(d):
    if math.isnan(d):
        return "NaN"
    if math.isinf(d):
        return "Infinity" if d > 0 else "-Infinity"
    if d == 0.0:
        if math.copysign(1.0, d) < 0:
            return "-0.0"
        return "0.0"
    
    abs_d = abs(d)
    if abs_d < 1e-3 or abs_d >= 1e7:
        s = f"{d:.17E}"
        mantissa, exp = s.split("E")
        mantissa = mantissa.rstrip('0')
        if mantissa.endswith('.'):
            mantissa += '0'
        exp_sign = exp[0]
        exp_val = int(exp[1:])
        return f"{mantissa}E{exp_sign}{exp_val}"
    else:
        s = f"{d:.17f}"
        s = s.rstrip('0')
        if s.endswith('.'):
            s += '0'
        return s

class ComplexCalculator:

    class ComplexNumber:
        def __init__(self, real, imaginary):
            self.real = real
            self.imaginary = imaginary

        def getReal(self):
            return self.real

        def getImaginary(self):
            return self.imaginary

        def __eq__(self, obj):
            if self is obj:
                return True
            if obj is None or type(self) != type(obj):
                return False
            return double_compare(self.real, obj.real) == 0 and double_compare(self.imaginary, obj.imaginary) == 0

        def __hash__(self):
            return id(self)

        def __str__(self):
            real_str = java_double_to_string(self.real)
            imag_str = java_double_to_string(self.imaginary)
            return real_str + ("+" if self.imaginary >= 0 else "") + imag_str + "j"

    def add(self, c1, c2):
        real = c1.getReal() + c2.getReal()
        imaginary = c1.getImaginary() + c2.getImaginary()
        return ComplexCalculator.ComplexNumber(real, imaginary)

    def subtract(self, c1, c2):
        real = c1.getReal() - c2.getReal()
        imaginary = c1.getImaginary() - c2.getImaginary()
        return ComplexCalculator.ComplexNumber(real, imaginary)

    def multiply(self, c1, c2):
        real = c1.getReal() * c2.getReal() - c1.getImaginary() * c2.getImaginary()
        imaginary = c1.getReal() * c2.getImaginary() + c1.getImaginary() * c2.getReal()
        return ComplexCalculator.ComplexNumber(real, imaginary)

    def divide(self, c1, c2):
        denominator = c2.getReal() * c2.getReal() + c2.getImaginary() * c2.getImaginary()
        real_num = c1.getReal() * c2.getReal() + c1.getImaginary() * c2.getImaginary()
        imag_num = c1.getImaginary() * c2.getReal() - c1.getReal() * c2.getImaginary()
        
        real = java_float_div(real_num, denominator)
        imaginary = java_float_div(imag_num, denominator)
        
        return ComplexCalculator.ComplexNumber(real, imaginary)
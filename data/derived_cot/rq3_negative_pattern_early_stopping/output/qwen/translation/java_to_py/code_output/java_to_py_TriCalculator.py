import decimal
from decimal import Decimal, getcontext, ROUND_HALF_UP
from math import pi as math_pi

class TriCalculator:

    PI_STRING = "3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679"

    def __init__(self):
        getcontext().prec = 128

    @staticmethod
    def factorial(a):
        result = 1
        while a > 1:
            result *= a
            a -= 1
        return result

    def taylor(self, x, n):
        x_rad = Decimal(x) * Decimal(self.PI_STRING) / Decimal(180)
        count = 1
        a = Decimal('1')
        for k in range(1, n):
            numerator = x_rad ** (2 * k)
            denominator = Decimal(self.factorial(2 * k))
            term = numerator / denominator
            if count % 2 == 1:
                a -= term
            else:
                a += term
            count += 1
        return a

    def cos(self, x):
        result = self.taylor(x, 50)
        result = result.quantize(Decimal('0.0000000001'), rounding=ROUND_HALF_UP)
        return float(result)

    def sin(self, x):
        x_rad = x * math_pi / 180.0
        g = 0.0
        t = x_rad
        n = 1
        while abs(t) >= 1e-15:
            g += t
            n += 1
            t = -t * x_rad * x_rad / (2 * n - 1) / (2 * n - 2)
        return round(g, 10)

    def tan(self, x):
        cos_value = self.cos(x)
        if cos_value != 0.0:
            sin_value = self.sin(x)
            return round(sin_value / cos_value, 10)
        else:
            return float('nan')

    @staticmethod
    def round(value, places):
        decimal_value = Decimal(str(value))
        rounded_value = decimal_value.quantize(Decimal('0.0000000001'), rounding=ROUND_HALF_UP)
        return float(rounded_value)